"""
modified_rand.py
=================

Metodo RAND modificado (seccion 3.2.2, pag. 37-42 de la tesis de
Tsanas). Linealiza la condicion de estacionariedad de Lagrange
(Ec. 3.14) alrededor de la estimacion actual de numero de moles,
usando derivadas composicionales de fugacidad/actividad (Ec. 3.48-3.49)
para lograr convergencia cuadratica incluso en sistemas no ideales.

Ecuaciones implementadas (verificadas contra el PDF original)
---------------------------------------------------------------
Ec. 3.48-3.49:
    M_iqk = delta_iq / n_ik + Phi_iqk,   Phi_iqk = d ln(Gamma_ik)/d n_qk

Ec. 3.56 (correccion de moles de la fase k, tras eliminar M_k):
    delta_n_k = s_k * M_k^-1 @ e_NC + M_k^-1 @ (A^T @ lambda - mu_k/RT)

Ec. 3.68 (sistema lineal final, lambda y s simultaneos):
    [ sum_k A M_k^-1 A^T     B ] [lambda]   [ sum_k A M_k^-1 (mu_k/RT) + delta_b ]
    [ B^T                    0 ] [  s   ] = [              d                     ]

    donde B = [A@n_1, ..., A@n_NP]  (NE x NP, columnas = abundancia de
    elementos por fase, Ec. 3.10-3.11), y delta_b = b - sum_k A@n_k
    (cero si el n actual ya satisface el balance de elementos; se
    mantiene por robustez ante errores de redondeo, tal como indica el
    texto tras la Ec. 3.70).

Ec. 3.69:
    d_k = n_k^T @ (mu_k/RT)

Ec. 3.70 (actualizacion con control de paso y monitoreo de Gibbs):
    n_k^(q+1) = n_k^(q) + alpha * delta_n_k^(q)
"""

import numpy as np

from termodinamica import ln_Gamma_fase, dln_Gamma_dn_fase, gibbs_reducida


def _estado_fase(n_k, g, modelo):
    """
    A partir del numero de moles de una fase, calcula composicion,
    ln(Gamma), potencial quimico reducido mu_k/RT y la matriz Phi de
    derivadas composicionales (Ec. 3.49).

    Retorna
    -------
    x_k, ln_Gamma_k, mu_k_RT, Phi_k
    """
    n_t_k = np.sum(n_k)
    x_k = n_k / n_t_k
    ln_Gamma_k = ln_Gamma_fase(
        modelo["tipo"], x_k, p=modelo.get("p"), p0=modelo.get("p0"),
        Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
        T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
        unifac_version=modelo.get("unifac_version", 0),
    )
    # mu_ik/RT = g_i(T) + ln(x_ik) + ln(Gamma_ik), ver termodinamica.py
    mu_k_RT = g + np.log(x_k) + ln_Gamma_k
    Phi_k = dln_Gamma_dn_fase(
        modelo["tipo"], n_k, Lambda=modelo.get("Lambda"),
        T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
        unifac_version=modelo.get("unifac_version", 0),
    )
    return x_k, ln_Gamma_k, mu_k_RT, Phi_k


def _paso_newton_rand(A, b, lam, n_fases, g, modelos_fase):
    """
    Un paso de Newton del metodo RAND modificado: ensambla y resuelve
    el sistema de la Ec. 3.68, y calcula las correcciones de moles
    delta_n_k (Ec. 3.56) para cada fase.

    Retorna
    -------
    lam_nuevo : ndarray, shape (NE,)
    delta_n_fases : list[ndarray]
    s : ndarray, shape (NP,)
    """
    NE, NC = A.shape
    NP = len(n_fases)

    M_inv_fases = []
    mu_fases = []
    for n_k, modelo in zip(n_fases, modelos_fase):
        _, _, mu_k_RT, Phi_k = _estado_fase(n_k, g, modelo)
        # M_iqk = delta_iq/n_ik + Phi_iqk  =>  diag(1/n_k) + Phi_k
        M_k = np.diag(1.0 / n_k) + Phi_k
        M_inv_fases.append(np.linalg.inv(M_k))
        mu_fases.append(mu_k_RT)

    # B: columnas = A @ n_k (abundancia de elementos de cada fase, Ec. 3.10)
    B = np.column_stack([A @ n_k for n_k in n_fases])  # (NE, NP)

    # d_k = n_k^T @ (mu_k/RT), Ec. 3.69
    d = np.array([n_k @ mu_k for n_k, mu_k in zip(n_fases, mu_fases)])

    # delta_b: residuo de balance de elementos con el n actual (Ec. 3.59),
    # se mantiene por robustez numerica aunque deberia ser ~0.
    N_total = sum(n_fases)
    delta_b = b - A @ N_total

    # Bloque superior izquierdo: sum_k A @ M_k^-1 @ A^T  (NE x NE)
    bloque_AA = np.zeros((NE, NE))
    rhs_top = delta_b.copy()
    for Minv, mu_k in zip(M_inv_fases, mu_fases):
        bloque_AA += A @ Minv @ A.T
        rhs_top += A @ (Minv @ mu_k)

    # Ensamblado del sistema completo (Ec. 3.68)
    J = np.zeros((NE + NP, NE + NP))
    J[:NE, :NE] = bloque_AA
    J[:NE, NE:] = B
    J[NE:, :NE] = B.T
    # bloque inferior derecho es cero (ya inicializado)

    rhs = np.concatenate([rhs_top, d])
    sol = np.linalg.solve(J, rhs)
    lam_nuevo = sol[:NE]
    s = sol[NE:]

    # Correcciones de moles por fase, Ec. 3.56
    e_NC = np.ones(NC)
    delta_n_fases = []
    for k, (n_k, modelo) in enumerate(zip(n_fases, modelos_fase)):
        Minv = M_inv_fases[k]
        mu_k = mu_fases[k]
        delta_n_k = s[k] * (Minv @ e_NC) + Minv @ (A.T @ lam_nuevo - mu_k)
        delta_n_fases.append(delta_n_k)

    return lam_nuevo, delta_n_fases, s


def resolver_rand_modificado(A, b, lam0, n_fases0, g, modelos_fase,
                              tol=1e-10, max_iter=100, max_backtracking=40):
    """
    Metodo RAND modificado completo: itera el paso de Newton de la
    Ec. 3.68, actualizando los numeros de mol (Ec. 3.70) con control de
    paso alpha que garantiza (a) numeros de mol positivos y (b)
    disminucion de la energia de Gibbs reducida G/(RT) en cada paso
    aceptado (ver comentario de la tesis tras la Ec. 3.70: "Monitoring
    of the Gibbs energy is the major advantage of the RAND method").

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
    b : ndarray, shape (NE,)
    lam0 : ndarray, shape (NE,)
        Estimacion inicial de lambda.
    n_fases0 : list[ndarray]
        Estimacion inicial de moles por componente en cada fase.
    g : ndarray, shape (NC,)
    modelos_fase : list[dict]
        Ver docstring de lagrange_multipliers.resolver_lagrange.
    tol : float
        Tolerancia sobre el error de la Ec. 3.78.
    max_iter : int
        Numero maximo de iteraciones de Newton.
    max_backtracking : int
        Numero maximo de reducciones a la mitad de alpha por iteracion.

    Retorna
    -------
    resultado : dict con llaves "lambda", "n_fases", "x_fases",
        "iteraciones", "error_final", "G_RT_historial"
    """
    lam = np.array(lam0, dtype=float)
    n_fases = [np.array(n_k, dtype=float) for n_k in n_fases0]

    def _ln_Gamma_todas(n_fases):
        salida = []
        for n_k, modelo in zip(n_fases, modelos_fase):
            x_k = n_k / np.sum(n_k)
            salida.append(ln_Gamma_fase(
                modelo["tipo"], x_k, p=modelo.get("p"), p0=modelo.get("p0"),
                Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
                T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
                unifac_version=modelo.get("unifac_version", 0),
            ))
        return salida

    G_historial = [gibbs_reducida(n_fases, g, _ln_Gamma_todas(n_fases))]
    error = np.inf  # por si el backtracking se agota en la primera iteracion
    historial_error = []  # para graficar convergencia (ver generar_figuras.py)

    for iteracion in range(1, max_iter + 1):
        lam_nuevo, delta_n_fases, s = _paso_newton_rand(
            A, b, lam, n_fases, g, modelos_fase
        )

        G_actual = G_historial[-1]
        alpha = 1.0
        for _ in range(max_backtracking):
            n_fases_prueba = [
                n_k + alpha * dn_k for n_k, dn_k in zip(n_fases, delta_n_fases)
            ]
            # (a) positividad de los numeros de mol
            if any(np.any(n_k <= 0.0) for n_k in n_fases_prueba):
                alpha *= 0.5
                continue
            # (b) descenso de la energia de Gibbs reducida
            ln_Gamma_prueba = _ln_Gamma_todas(n_fases_prueba)
            G_prueba = gibbs_reducida(n_fases_prueba, g, ln_Gamma_prueba)
            if G_prueba <= G_actual:
                break
            alpha *= 0.5
        else:
            # No se encontro un paso aceptable: nos detenemos con el
            # mejor estado encontrado hasta ahora.
            break

        # Error de convergencia, Ec. 3.78 (norma de los cambios en n_ik)
        error = np.sqrt(
            sum(np.sum((alpha * dn_k) ** 2) for dn_k in delta_n_fases)
        )

        lam = lam_nuevo
        n_fases = n_fases_prueba
        G_historial.append(G_prueba)
        historial_error.append(error)

        if error < tol:
            break

    x_fases = [n_k / np.sum(n_k) for n_k in n_fases]
    resultado = {
        "lambda": lam,
        "n_fases": n_fases,
        "x_fases": x_fases,
        "iteraciones": iteracion,
        "error_final": error,
        "G_RT_historial": G_historial,
        "historial_error": historial_error,
    }
    return resultado


if __name__ == "__main__":
    # Demostracion / depuracion independiente: sistema NO reactivo de 3
    # componentes (A = identidad) con una fase liquida fuertemente no
    # ideal (modelo de Wilson, parametros ilustrativos genericos),
    # resuelto directamente con el metodo RAND modificado. Se reporta
    # la disminucion monotonica de G/(RT) en cada iteracion (el chequeo
    # central del metodo RAND, ver docstring del modulo).
    from inicializacion import minimizar_Q

    print("modified_rand.py -- demostracion independiente")

    A = np.eye(3)
    b = A @ np.array([0.3, 0.3, 0.4])
    g = np.zeros(3)
    Psat = np.array([2.0, 1.0, 0.5])
    Lambda = np.array([[1.0, 0.3, 0.5], [2.0, 1.0, 0.4], [1.5, 1.8, 1.0]])
    modelo_vapor = {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}
    modelo_liquido = {"tipo": "liquido_wilson", "Psat": Psat, "p0": 1.0, "Lambda": Lambda}

    x0 = np.ones(3) / 3
    ln_Gamma0 = [
        ln_Gamma_fase(m["tipo"], x0, p=m.get("p"), p0=m.get("p0"),
                      Psat=m.get("Psat"), Lambda=m.get("Lambda"))
        for m in [modelo_liquido, modelo_vapor]
    ]
    lam0, n0, _ = minimizar_Q(A, b, n_t_fases=[0.5, 0.5], g=g, ln_Gamma_fases=ln_Gamma0)

    resultado = resolver_rand_modificado(A, b, lam0, n0, g, [modelo_liquido, modelo_vapor])
    print(f"iteraciones = {resultado['iteraciones']}, error_final = {resultado['error_final']:.3e}")
    print("Historial de G/(RT) (debe decrecer monotonicamente):")
    for i, G in enumerate(resultado["G_RT_historial"]):
        print(f"  iter {i}: G/RT = {G:.8f}")
    for k, x_k in enumerate(resultado["x_fases"]):
        print(f"x fase {k+1} = {x_k}")
