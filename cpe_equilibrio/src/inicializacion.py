"""
inicializacion.py
==================

Minimizacion de la funcion Q (seccion 3.2.3, pag. 42-43 de la tesis de
Tsanas, Ec. 3.71-3.75) para obtener estimados iniciales de los
multiplicadores de Lagrange lambda, dado un numero de moles totales
por fase (n_t) ya supuesto.

Ecuaciones implementadas (verificadas contra el PDF original)
---------------------------------------------------------------
Ec. 3.71:
    Q(lambda) = sum_k n_t,k * [ sum_i x_ik(lambda) - 1 ] - sum_j lambda_j * b_j

Ec. 3.72 (paso de Newton):
    Hessiano(Q) * delta_lambda = -gradiente(Q)

Ec. 3.74 (forma explicita del Hessiano, suponiendo phi/gamma fijos):
    [A * diag(N) * A^T] * delta_lambda = b - A * N
    donde N = sum_k n_k  (vector de moles totales de cada componente,
    sumado sobre todas las fases, N_i = sum_k n_t,k * x_ik)

    NOTA SOBRE EL SIGNO: el texto convertido a Markdown (y el propio
    PDF via extraccion de texto) pierde el signo exacto de esta
    ecuacion por danos de la conversion. El signo correcto, "b - A*N"
    en el lado derecho, se rederivo aqui directamente por calculo: la
    funcion objetivo es Q(lambda), su gradiente respecto a lambda_j es
    el residuo del balance de elementos  -(A*N - b)_j = (b - A*N)_j
    (ver Ec. 3.15), y el paso de Newton exige
    Hessiano * delta_lambda = -gradiente = b - A*N.
    Esta forma fue verificada numericamente en pruebas_validacion.py
    confirmando que Q decrece monotonicamente con este signo.

Ec. 3.75:
    lambda^(q+1) = lambda^(q) + alpha * delta_lambda^(q)
    (alpha controla el paso si Q aumenta en vez de disminuir)

Ec. 3.76 (criterio de convergencia):
    error^(q) = sqrt( sum_j [lambda_j^(q) - lambda_j^(q-1)]^2 )
"""

import numpy as np


def valor_Q(A, b, lam, n_t_fases, g, ln_Gamma_fases):
    """
    Evalua la funcion Q(lambda) de la Ec. 3.71.

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
        Matriz de formula (elementos x componentes).
    b : ndarray, shape (NE,)
        Vector de abundancia de elementos (de la alimentacion, Ec. 3.9).
    lam : ndarray, shape (NE,)
        Multiplicadores de Lagrange actuales.
    n_t_fases : list[float]
        Moles totales de cada fase (fijos durante la minimizacion de Q).
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia g_i(T) de cada
        componente puro (ver termodinamica.py).
    ln_Gamma_fases : list[ndarray]
        Factor de no-idealidad ln(Gamma_ik) de cada fase, MANTENIDO FIJO
        durante toda la minimizacion de Q (aproximacion de sistema ideal,
        consistente con el texto: "Assuming composition independent
        fugacity or activity coefficients").

    Retorna
    -------
    Q : float
        Valor de la funcion Q.
    """
    Q = 0.0
    for n_t_k, ln_Gamma_k in zip(n_t_fases, ln_Gamma_fases):
        # Exponente de la Ec. 3.34: ln(x_ik) = A^T.lambda - g_i - ln(Gamma_ik)
        ln_x_k = A.T @ lam - g - ln_Gamma_k
        x_k = np.exp(ln_x_k)
        # Contribucion de la fase k: n_t,k * (suma de fracciones - 1).
        # En el optimo esta suma tiende a 1 (normalizacion), pero durante
        # la minimizacion de Q no se impone como restriccion explicita.
        Q += n_t_k * (np.sum(x_k) - 1.0)
    # Termino lineal en lambda ligado al balance de elementos objetivo.
    Q -= lam @ b
    return Q


def minimizar_Q(A, b, n_t_fases, g, ln_Gamma_fases, lam0=None,
                 tol=1e-10, max_iter=200, max_backtracking=40):
    """
    Minimiza la funcion Q (Ec. 3.71) respecto a lambda mediante el metodo
    de Newton con control de paso (Ec. 3.72-3.75), para un n_t por fase
    ya supuesto. Esto corresponde al paso 2 del "successive substitution
    algorithm" (y del "combined algorithm"): obtener una estimacion
    inicial de lambda antes de resolver el sistema completo (Ec. 3.46).

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
        Matriz de formula.
    b : ndarray, shape (NE,)
        Vector de abundancia de elementos de la alimentacion.
    n_t_fases : list[float]
        Moles totales supuestos para cada fase (paso 1 del algoritmo).
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia de cada componente puro.
    ln_Gamma_fases : list[ndarray]
        ln(Gamma_ik) de cada fase, evaluado una sola vez (ideal: phi=1
        en vapor, gamma=1 en liquido) y mantenido fijo.
    lam0 : ndarray or None
        Estimacion inicial de lambda (por defecto: vector de ceros).
    tol : float
        Tolerancia de convergencia sobre el error de la Ec. 3.76.
    max_iter : int
        Numero maximo de iteraciones de Newton.
    max_backtracking : int
        Numero maximo de reducciones a la mitad del paso alpha por
        iteracion, si Q no disminuye.

    Retorna
    -------
    lam : ndarray, shape (NE,)
        Multiplicadores de Lagrange en el minimo de Q.
    n_fases : list[ndarray]
        Numero de moles de cada componente en cada fase,
        n_ik = n_t,k * x_ik(lambda), evaluados en el lambda final.
    info : dict
        Diagnostico: numero de iteraciones y error final.
    """
    NE, NC = A.shape
    lam = np.zeros(NE) if lam0 is None else np.array(lam0, dtype=float)

    Q_actual = valor_Q(A, b, lam, n_t_fases, g, ln_Gamma_fases)

    for iteracion in range(1, max_iter + 1):
        # --- Construccion del vector N = sum_k n_k (moles totales por
        # componente, sumados sobre todas las fases) ---
        N = np.zeros(NC)
        for n_t_k, ln_Gamma_k in zip(n_t_fases, ln_Gamma_fases):
            ln_x_k = A.T @ lam - g - ln_Gamma_k
            x_k = np.exp(ln_x_k)
            N += n_t_k * x_k  # n_ik = n_t,k * x_ik; se acumula sobre fases

        # --- Hessiano de Q, Ec. 3.74: A * diag(N) * A^T ---
        JA = A @ (N[:, None] * A.T)  # equivalente a A @ diag(N) @ A.T

        # --- Lado derecho del paso de Newton (ver docstring: signo
        # rederivado directamente de la condicion de estacionariedad) ---
        rhs = b - A @ N

        # Resolvemos el sistema lineal NE x NE para obtener delta_lambda.
        delta_lam = np.linalg.solve(JA, rhs)

        # --- Control de paso (Ec. 3.75): aceptar el paso solo si Q
        # efectivamente disminuye; si no, reducir alpha a la mitad ---
        alpha = 1.0
        for _ in range(max_backtracking):
            lam_prueba = lam + alpha * delta_lam
            Q_prueba = valor_Q(A, b, lam_prueba, n_t_fases, g, ln_Gamma_fases)
            if Q_prueba <= Q_actual:
                break
            alpha *= 0.5
        else:
            # No se encontro una direccion de descenso: nos detenemos
            # con el mejor lambda encontrado hasta ahora.
            break

        # --- Error de convergencia, Ec. 3.76 (norma del cambio en lambda) ---
        error = np.sqrt(np.sum((alpha * delta_lam) ** 2))

        lam = lam_prueba
        Q_actual = Q_prueba

        if error < tol:
            break

    # Composicion y moles finales por fase, evaluados en el lambda convergido.
    n_fases = []
    for n_t_k, ln_Gamma_k in zip(n_t_fases, ln_Gamma_fases):
        ln_x_k = A.T @ lam - g - ln_Gamma_k
        x_k = np.exp(ln_x_k)
        n_fases.append(n_t_k * x_k)

    info = {"iteraciones": iteracion, "error_final": error, "Q_final": Q_actual}
    return lam, n_fases, info


if __name__ == "__main__":
    # Demostracion / depuracion independiente: sistema ideal de una sola
    # reaccion A + B <-> C (gas ideal en ambas fases, formula matrix
    # trivial A=I ya que no hay reaccion de verdad aqui -- sirve solo
    # para probar que minimizar_Q converge y reproduce el balance b=A@n).
    print("inicializacion.py -- demostracion independiente")

    A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])  # igual que MTBE
    b = A @ np.array([1.0, 1.1, 0.0])
    g = np.array([0.0, 0.0, -np.log(50.0)])
    ln_Gamma_fases = [np.zeros(3)]  # fase unica, gas ideal (phi=1, p=p0)

    lam, n_fases, info = minimizar_Q(A, b, n_t_fases=[2.1], g=g, ln_Gamma_fases=ln_Gamma_fases)
    print(f"lambda = {lam}")
    print(f"n = {n_fases[0]}  (iteraciones={info['iteraciones']}, Q_final={info['Q_final']:.3e})")
    print(f"chequeo balance: A@n = {A @ n_fases[0]}  (debe ser cercano a b = {b})")
