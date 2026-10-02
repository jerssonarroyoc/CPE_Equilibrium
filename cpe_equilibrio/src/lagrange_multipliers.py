"""
lagrange_multipliers.py
========================

Metodo de multiplicadores de Lagrange (seccion 3.2.1, pag. 31-37 de la
tesis de Tsanas). Implementa el sistema de Newton de la Ec. 3.46 y el
esquema de doble bucle descrito en la seccion 3.3 (pasos 3 y 4 del
"successive substitution algorithm"):

    - bucle interno: resuelve el sistema de Ec. 3.46 con phi/gamma
      (el factor Gamma_ik de termodinamica.py) mantenidos CONSTANTES,
      iterando x = f(lambda) via Ec. 3.34 hasta convergencia.
    - bucle externo: recalcula phi/gamma con la composicion convergida
      del bucle interno y repite, hasta que Gamma_ik deje de cambiar
      (equivalente a "all phases ideal" o a la convergencia de la
      actualizacion de no-idealidad mencionada en la pag. 44).

Ecuacion 3.46 (reconstruida y verificada por derivacion directa, ver
docstring de resolver_interno para el detalle del signo del lado
derecho, que la conversion a texto del PDF corrompio):

    [ JA   JB ] [delta_lambda]   [ b - A@N            ]
    [ JB^T  0 ] [delta_n_t   ] = [ e_NP - X^T e_NC     ]

donde (Ec. 3.41-3.44):
    JA_jq = sum_k n_t,k * sum_i A_ji A_qi x_ik   (NE x NE)
    JB_jq = sum_i A_ji x_iq  (columna q = A @ x_q)   (NE x NP)
    JC    = JB^T                                      (NP x NE)
    JD    = 0                                          (NP x NP)
    N     = sum_k n_k   (moles totales de cada componente, Ec. 3.59-ish)
    X     = matriz (NC x NP) cuyas columnas son x_k
"""

import numpy as np

from termodinamica import ln_Gamma_fase, dln_Gamma_dn_fase


def _composicion_desde_lambda(A, lam, g, ln_Gamma_fases):
    """
    Evalua x_ik = exp(sum_j A_ji*lambda_j - g_i - ln(Gamma_ik)) (Ec. 3.34)
    para cada fase.

    Retorna
    -------
    x_fases : list[ndarray], cada una shape (NC,)
    """
    exponente_base = A.T @ lam - g  # comun a todas las fases, shape (NC,)
    return [np.exp(exponente_base - ln_Gamma_k) for ln_Gamma_k in ln_Gamma_fases]


def _ensamblar_sistema_3_46(A, lam, n_t_fases, x_fases, b):
    """
    Construye la matriz J y el lado derecho del sistema de Newton
    (Ec. 3.46) para el estado actual (lambda, n_t, x por fase).

    Retorna
    -------
    J : ndarray, shape (NE+NP, NE+NP)
    rhs : ndarray, shape (NE+NP,)
    """
    NE, NC = A.shape
    NP = len(n_t_fases)

    # --- N = sum_k n_k (moles totales de cada componente, Ec. usada en 3.74) ---
    N = np.zeros(NC)
    for n_t_k, x_k in zip(n_t_fases, x_fases):
        N += n_t_k * x_k

    # --- JA (Ec. 3.41): suma ponderada por fase de A*diag(x_k)*A^T ---
    JA = np.zeros((NE, NE))
    for n_t_k, x_k in zip(n_t_fases, x_fases):
        JA += n_t_k * (A @ (x_k[:, None] * A.T))

    # --- JB (Ec. 3.42): columna q es A @ x_q ---
    JB = np.column_stack([A @ x_k for x_k in x_fases])  # (NE, NP)

    # --- Ensamblado del bloque completo ---
    J = np.zeros((NE + NP, NE + NP))
    J[:NE, :NE] = JA
    J[:NE, NE:] = JB
    J[NE:, :NE] = JB.T  # JC = JB^T (Ec. 3.43)
    # JD = 0 (Ec. 3.44): ya esta inicializado a cero.

    # --- Lado derecho: residuales -F = [b - A@N ; e_NP - X^T e_NC] ---
    residual_balance = b - A @ N  # NE componentes
    residual_normalizacion = np.array(
        [1.0 - np.sum(x_k) for x_k in x_fases]
    )  # NP componentes: 1 - suma de fracciones molares de cada fase

    rhs = np.concatenate([residual_balance, residual_normalizacion])
    return J, rhs


def resolver_interno(A, b, lam0, n_t_fases0, g, ln_Gamma_fases,
                      tol=1e-10, max_iter=100):
    """
    Bucle interno del metodo de multiplicadores de Lagrange: resuelve el
    sistema completo de Newton (Ec. 3.46) manteniendo Gamma_ik
    (phi/gamma) CONSTANTE, iterando hasta convergencia.

    Esto corresponde al paso 3 del "successive substitution algorithm"
    (pag. 43-44 de la tesis).

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
    b : ndarray, shape (NE,)
    lam0 : ndarray, shape (NE,)
        Estimacion inicial de lambda (tipicamente la salida de
        inicializacion.minimizar_Q).
    n_t_fases0 : list[float]
        Moles totales iniciales de cada fase.
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia de cada componente.
    ln_Gamma_fases : list[ndarray]
        ln(Gamma_ik) de cada fase, FIJO durante todo este bucle.
    tol : float
        Tolerancia sobre el error combinado (Ec. 3.77).
    max_iter : int
        Numero maximo de iteraciones de Newton.

    Retorna
    -------
    lam : ndarray, shape (NE,)
    n_t_fases : list[float]
    x_fases : list[ndarray]
    info : dict
    """
    NP = len(n_t_fases0)
    lam = np.array(lam0, dtype=float)
    n_t_fases = list(n_t_fases0)

    # Piso absoluto para n_t: evita que una fase recien anadida (o una
    # fase que el Newton esta "expulsando" porque en el optimo tiene
    # cantidad cero) cruce exactamente por cero y deje el sistema
    # (Ec. 3.46) numericamente singular por division entre valores de
    # punto flotante casi nulos. Si la fase realmente debe desaparecer,
    # quedara "flotando" en este piso (cantidad despreciable) y el
    # analisis de estabilidad del algoritmo que llama a esta funcion
    # (algoritmos.py) decidira si debe conservarse o no.
    piso_nt = 1e-10 * max(sum(n_t_fases0), 1.0)

    diverged = False
    historial_error = []  # para graficar convergencia (ver generar_figuras.py)
    for iteracion in range(1, max_iter + 1):
        # La aproximacion de sistema ideal (Gamma fijo dentro de este
        # bucle interno) puede generar valores extremos (overflow en
        # exp(), matrices mal condicionadas) para sistemas fuertemente
        # no ideales -- este es precisamente el problema de convergencia
        # que Greiner (1991) describe en su resumen ("severe convergence
        # problems... even if a very close estimate of the true solution
        # is available") y que motiva el metodo RAND modificado. Estos
        # overflows son ESPERADOS en ese caso (no un error de progra-
        # macion) y se capturan abajo como no-convergencia, asi que se
        # silencian para no ensuciar la salida.
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            x_fases = _composicion_desde_lambda(A, lam, g, ln_Gamma_fases)
            J, rhs = _ensamblar_sistema_3_46(A, lam, n_t_fases, x_fases, b)

            if not (np.all(np.isfinite(J)) and np.all(np.isfinite(rhs))):
                diverged = True
                error = np.inf
                break

            # En vez de propagar la excepcion de una matriz singular, lo
            # tratamos como "no convergio" para que el llamador
            # (algoritmos.combined_algorithm) pueda cambiar al metodo
            # RAND, tal como indica la Fig. 3.1b de la tesis.
            try:
                delta = np.linalg.solve(J, rhs)
            except np.linalg.LinAlgError:
                diverged = True
                error = np.inf
                break
        if not np.all(np.isfinite(delta)):
            diverged = True
            error = np.inf
            break
        delta_lam = delta[: len(lam)]
        delta_nt = delta[len(lam):]

        # --- Control de paso (damping) ---
        # La tesis presenta la Ec. 3.46 como un paso de Newton puro,
        # pero un paso completo (alpha=1) puede hacer que n_t de una
        # fase recien anadida (cantidad traza) se vuelva negativo o
        # que lambda oscile sin control, especialmente lejos de la
        # solucion. Igual que en el metodo RAND (Ec. 3.70) y en la
        # minimizacion de Q (Ec. 3.75), reducimos el paso a la mitad
        # hasta que todos los n_t se mantengan por encima del piso.
        alpha = 1.0
        for _ in range(60):
            nt_prueba = [nt + alpha * dnt for nt, dnt in zip(n_t_fases, delta_nt)]
            if all(nt > piso_nt for nt in nt_prueba):
                break
            alpha *= 0.5
        else:
            # Ni siquiera un paso minusculo evita cruzar el piso: la
            # fase esta efectivamente colapsando a cantidad cero.
            # La dejamos fija en el piso y seguimos iterando lambda.
            nt_prueba = [max(nt + alpha * dnt, piso_nt)
                         for nt, dnt in zip(n_t_fases, delta_nt)]

        lam = lam + alpha * delta_lam
        n_t_fases = nt_prueba

        # Criterio de convergencia, Ec. 3.77: norma conjunta de los
        # cambios en lambda y en los n_t de cada fase (con el paso
        # alpha efectivamente aplicado).
        error = np.sqrt(np.sum((alpha * delta_lam) ** 2) + np.sum((alpha * np.array(delta_nt)) ** 2))
        historial_error.append(error)
        if error < tol:
            break

    # Composicion final, y numero de moles por componente y fase:
    # n_ik = n_t,k * x_ik, calculado en el lambda convergido (o en el
    # ultimo lambda valido antes de divergir).
    x_fases = _composicion_desde_lambda(A, lam, g, ln_Gamma_fases)
    n_fases = [nt * x for nt, x in zip(n_t_fases, x_fases)]

    info = {"iteraciones": iteracion, "error_final": error, "diverged": diverged,
            "historial_error": historial_error}
    return lam, n_t_fases, n_fases, x_fases, info


def resolver_lagrange(A, b, lam0, n_fases0, g, modelos_fase,
                       tol_interno=1e-10, tol_externo=1e-10,
                       max_iter_interno=100, max_iter_externo=50):
    """
    Metodo de multiplicadores de Lagrange completo: doble bucle
    interno/externo (pasos 3-4 del "successive substitution algorithm",
    pag. 43-44).

        bucle interno -> resolver_interno() con Gamma fijo
        bucle externo -> recalcula Gamma con la composicion convergida
                         y repite, hasta que Gamma deje de cambiar

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
    b : ndarray, shape (NE,)
    lam0 : ndarray, shape (NE,)
        Estimacion inicial de lambda (de inicializacion.minimizar_Q).
    n_fases0 : list[ndarray]
        Estimacion inicial de moles por componente en cada fase
        (n_fases0[k], shape (NC,)); se usa solo para evaluar Gamma la
        primera vez (bucle externo, iteracion 0).
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia de cada componente.
    modelos_fase : list[dict]
        Un dict por fase describiendo su modelo termodinamico, con
        llaves compatibles con termodinamica.ln_Gamma_fase, p. ej.:
            {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}
            {"tipo": "liquido_ideal", "Psat": array([...]), "p0": 1.0}
            {"tipo": "liquido_wilson", "Psat": array([...]), "p0": 1.0,
             "Lambda": array([[...]])}
    tol_interno, tol_externo : float
        Tolerancias del bucle interno y externo.
    max_iter_interno, max_iter_externo : int
        Limites de iteracion de cada bucle.

    Retorna
    -------
    resultado : dict con llaves:
        "lambda", "n_t_fases", "n_fases", "x_fases",
        "iteraciones_externas", "iteraciones_internas_total"
    """
    n_t_fases = [float(np.sum(n_k)) for n_k in n_fases0]
    x_fases = [n_k / nt for n_k, nt in zip(n_fases0, n_t_fases)]
    lam = np.array(lam0, dtype=float)

    # Evaluacion inicial de Gamma con la composicion de arranque.
    ln_Gamma_fases = [
        ln_Gamma_fase(m["tipo"], x_k, p=m.get("p"), p0=m.get("p0"),
                      Psat=m.get("Psat"), Lambda=m.get("Lambda"),
                      T=m.get("T"), chemgroups=m.get("chemgroups"),
                      unifac_version=m.get("unifac_version", 0))
        for m, x_k in zip(modelos_fase, x_fases)
    ]

    iteraciones_internas_total = 0
    historial_error = []  # concatenado de todos los bucles internos (para graficar)

    for iteracion_externa in range(1, max_iter_externo + 1):
        # --- Bucle interno: Gamma fijo (aproximacion de sistema ideal) ---
        lam, n_t_fases, n_fases, x_fases, info_interno = resolver_interno(
            A, b, lam, n_t_fases, g, ln_Gamma_fases,
            tol=tol_interno, max_iter=max_iter_interno,
        )
        iteraciones_internas_total += info_interno["iteraciones"]
        historial_error.extend(info_interno["historial_error"])

        if info_interno["diverged"]:
            # El bucle interno con Gamma fijo diverge (sistema
            # numericamente singular o paso no finito): tipico de
            # sistemas fuertemente no ideales, ver comentario en
            # resolver_interno. Reportamos no-convergencia para que el
            # llamador pueda cambiar al metodo RAND modificado.
            return {
                "lambda": lam, "n_t_fases": n_t_fases, "n_fases": n_fases,
                "x_fases": x_fases, "ln_Gamma_fases": ln_Gamma_fases,
                "iteraciones_externas": iteracion_externa,
                "iteraciones_internas_total": iteraciones_internas_total,
                "convergido": False, "diverged": True,
                "historial_error": historial_error,
            }

        # --- Bucle externo: recalcular Gamma con la composicion nueva ---
        ln_Gamma_fases_nuevo = [
            ln_Gamma_fase(m["tipo"], x_k, p=m.get("p"), p0=m.get("p0"),
                          Psat=m.get("Psat"), Lambda=m.get("Lambda"),
                          T=m.get("T"), chemgroups=m.get("chemgroups"),
                          unifac_version=m.get("unifac_version", 0))
            for m, x_k in zip(modelos_fase, x_fases)
        ]

        # Si Gamma no cambio (dentro de tolerancia), el sistema es
        # efectivamente ideal en este punto y hemos convergido
        # (equivalente a "all phases ideal? -> proceed" de la Fig. 3.1a).
        cambio_gamma = max(
            np.max(np.abs(g_nuevo - g_viejo))
            for g_nuevo, g_viejo in zip(ln_Gamma_fases_nuevo, ln_Gamma_fases)
        )
        ln_Gamma_fases = ln_Gamma_fases_nuevo

        convergido = cambio_gamma < tol_externo
        if convergido:
            break

    resultado = {
        "lambda": lam,
        "n_t_fases": n_t_fases,
        "n_fases": n_fases,
        "x_fases": x_fases,
        "ln_Gamma_fases": ln_Gamma_fases,
        "iteraciones_externas": iteracion_externa,
        "iteraciones_internas_total": iteraciones_internas_total,
        "convergido": convergido,
        "diverged": False,
        "historial_error": historial_error,
    }
    return resultado


if __name__ == "__main__":
    # Demostracion / depuracion independiente: sistema MTBE de una sola
    # fase liquida ideal (gas ideal / solucion ideal), resuelto
    # directamente con el metodo de multiplicadores de Lagrange.
    from inicializacion import minimizar_Q

    print("lagrange_multipliers.py -- demostracion independiente")

    A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    b = A @ np.array([1.0, 1.1, 0.0])
    g = np.array([0.0, 0.0, -np.log(50.0)])
    Psat = np.array([5.59, 0.52, 0.77])  # bar, ver ejemplo_mtbe.py
    modelo_liquido = {"tipo": "liquido_ideal", "Psat": Psat, "p0": 1.01325}

    ln_Gamma0 = [ln_Gamma_fase("liquido_ideal", np.ones(3) / 3, Psat=Psat, p0=1.01325)]
    lam0, n0, _ = minimizar_Q(A, b, n_t_fases=[2.1], g=g, ln_Gamma_fases=ln_Gamma0)

    resultado = resolver_lagrange(A, b, lam0, n0, g, [modelo_liquido])
    print(f"lambda final = {resultado['lambda']}")
    print(f"n = {resultado['n_fases'][0]}")
    print(f"x = {resultado['x_fases'][0]}")
    print(f"iteraciones externas={resultado['iteraciones_externas']}, "
          f"internas_total={resultado['iteraciones_internas_total']}, "
          f"convergido={resultado['convergido']}")
    print(f"chequeo balance: A@n = {A @ resultado['n_fases'][0]}  (debe ser {b})")
