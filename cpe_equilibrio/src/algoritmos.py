"""
algoritmos.py
==============

Los dos algoritmos completos de la seccion 3.3 (pag. 43-45 de la tesis
de Tsanas), que combinan inicializacion.py, lagrange_multipliers.py,
modified_rand.py y estabilidad.py segun los pasos descritos en el
texto y en la Figura 3.1:

    successive_substitution_algorithm() -- Figura 3.1(a)
    combined_algorithm()                -- Figura 3.1(b)

Ambos algoritmos devuelven la solucion de equilibrio (lambda, n por
fase, composiciones) junto con informacion de diagnostico (numero de
fases final, iteraciones, etc.).
"""

import numpy as np

from termodinamica import ln_Gamma_fase
from inicializacion import minimizar_Q
from lagrange_multipliers import resolver_lagrange
from modified_rand import resolver_rand_modificado
from estabilidad import analizar_estabilidad


def _lambda_y_n_iniciales(A, b, n_t_fases, modelos_fase, g, tol_Q=1e-10):
    """
    Pasos 1-2 de ambos algoritmos: dado un numero de moles totales por
    fase ya supuesto, minimiza la funcion Q (Ec. 3.71-3.75) asumiendo
    phi/gamma fijos (evaluados en una composicion equimolar, ya que la
    minimizacion de Q requiere un valor fijo de partida y el sistema
    aun no tiene una composicion propia) para obtener una estimacion
    inicial de lambda y de los n por fase.
    """
    NE, NC = A.shape
    x_equimolar = np.ones(NC) / NC
    ln_Gamma_fases_fijo = [
        ln_Gamma_fase(m["tipo"], x_equimolar, p=m.get("p"), p0=m.get("p0"),
                      Psat=m.get("Psat"), Lambda=m.get("Lambda"),
                      T=m.get("T"), chemgroups=m.get("chemgroups"),
                      unifac_version=m.get("unifac_version", 0))
        for m in modelos_fase
    ]
    lam0, n_fases0, info_Q = minimizar_Q(
        A, b, n_t_fases, g, ln_Gamma_fases_fijo, tol=tol_Q
    )
    return lam0, n_fases0, info_Q


def _candidato_estabilidad_a_fase(resultado_estabilidad, n_t_trazas=1e-6):
    """
    Convierte el resultado de estabilidad.analizar_estabilidad() (una
    composicion w y un modelo de fase) en una fase nueva con cantidad
    de moles infinitesimal, lista para anadirse a la lista de fases
    (pag. 44: "the amount of the new phase is set to zero").
    """
    w = resultado_estabilidad["w"]
    modelo_trial = resultado_estabilidad["modelo_trial"]
    n_nueva_fase = w * n_t_trazas
    return n_nueva_fase, modelo_trial


def successive_substitution_algorithm(A, b, n_t_fase_inicial, modelo_fase_inicial,
                                       g, modelos_trial_candidatos,
                                       tol_Q=1e-10, tol_interno=1e-10,
                                       tol_externo=1e-10, max_fases=4):
    """
    Successive substitution algorithm (Figura 3.1a, pag. 43-45).

    Pasos:
        1. Asumir una sola fase, con n_t supuesto -> minimizar_Q (2) ->
        3. Resolver el sistema completo (Ec. 3.46) con doble bucle
           interno/externo (lagrange_multipliers.resolver_lagrange) -> 4.
        5. Analisis de estabilidad: si inestable, anadir fase y volver
           a 3 (sin reinicializar); si estable, fin.

    Parametros
    ----------
    A : ndarray, shape (NE, NC)
    b : ndarray, shape (NE,)
    n_t_fase_inicial : float
        Moles totales supuestos para la (unica) fase inicial.
    modelo_fase_inicial : dict
        Modelo termodinamico de la fase inicial (ver
        termodinamica.ln_Gamma_fase).
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia de cada componente.
    modelos_trial_candidatos : list[dict]
        Modelos de fase a probar en el analisis de estabilidad (p. ej.
        un modelo de vapor y uno de liquido).
    tol_Q, tol_interno, tol_externo : float
        Tolerancias de cada etapa.
    max_fases : int
        Limite de seguridad al numero de fases que el algoritmo puede
        anadir (evita bucles infinitos en casos patologicos).

    Retorna
    -------
    resultado : dict con "lambda", "n_fases", "x_fases", "modelos_fase",
        "estable", "historial_fases" (numero de iteraciones externas
        por cada numero de fases probado).
    """
    n_t_fases = [n_t_fase_inicial]
    modelos_fase = [modelo_fase_inicial]
    historial = []

    lam0, n_fases0, _ = _lambda_y_n_iniciales(A, b, n_t_fases, modelos_fase, g)

    resultado_lagrange = resolver_lagrange(
        A, b, lam0, n_fases0, g, modelos_fase,
        tol_interno=tol_interno, tol_externo=tol_externo,
    )
    historial.append(resultado_lagrange["iteraciones_externas"])

    for _ in range(max_fases - 1):
        # Fase de referencia para la prueba de estabilidad: la primera
        # fase convergida (cualquiera sirve, Ec. 3.30: mu_ik = mu_iq).
        z = resultado_lagrange["x_fases"][0]
        modelo_feed = modelos_fase[0]

        es_estable, mejor = analizar_estabilidad(z, modelo_feed, modelos_trial_candidatos)

        if es_estable:
            return {
                "lambda": resultado_lagrange["lambda"],
                "n_fases": resultado_lagrange["n_fases"],
                "x_fases": resultado_lagrange["x_fases"],
                "modelos_fase": modelos_fase,
                "estable": True,
                "historial_fases": historial,
            }

        # Inestable: anadir la fase nueva (sin reinicializar lambda) y
        # volver a resolver el sistema completo con una fase mas.
        n_nueva_fase, modelo_nuevo = _candidato_estabilidad_a_fase(mejor)
        n_fases_extendido = resultado_lagrange["n_fases"] + [n_nueva_fase]
        modelos_fase = modelos_fase + [modelo_nuevo]

        resultado_lagrange = resolver_lagrange(
            A, b, resultado_lagrange["lambda"], n_fases_extendido, g, modelos_fase,
            tol_interno=tol_interno, tol_externo=tol_externo,
        )
        historial.append(resultado_lagrange["iteraciones_externas"])

    # Se alcanzo el limite de fases sin confirmar estabilidad.
    return {
        "lambda": resultado_lagrange["lambda"],
        "n_fases": resultado_lagrange["n_fases"],
        "x_fases": resultado_lagrange["x_fases"],
        "modelos_fase": modelos_fase,
        "estable": False,
        "historial_fases": historial,
    }


def combined_algorithm(A, b, n_t_fase_inicial, modelo_fase_inicial,
                        g, modelos_trial_candidatos,
                        tol_Q=1e-10, tol_interno=1e-10, tol_externo=1e-10,
                        tol_rand=1e-10, max_iter_ssa_externo=3, max_fases=4):
    """
    Combined algorithm (Figura 3.1b, pag. 43-45): usa sustitucion
    sucesiva (metodo de Lagrange) para los primeros pasos y cambia al
    RAND modificado para la convergencia de segundo orden.

    Pasos:
        1. Asumir una sola fase, con n_t supuesto.
        2. Minimizar Q para lambda inicial.
        3. Repetir los pasos 3-4 de SSA hasta 3 iteraciones del bucle
           externo:
             - si converge, continuar.
             - si no converge, cambiar al RAND modificado (Ec. 3.68)
               hasta convergencia, actualizando phi/gamma en cada
               iteracion (sin bucle anidado).
        4. Analisis de estabilidad: igual que SSA.

    Parametros y retorno: identicos a successive_substitution_algorithm,
    mas "metodo_final" indicando si la convergencia final se logro con
    "lagrange" (<=3 iteraciones externas) o con "rand".
    """
    n_t_fases = [n_t_fase_inicial]
    modelos_fase = [modelo_fase_inicial]
    historial = []

    lam0, n_fases0, _ = _lambda_y_n_iniciales(A, b, n_t_fases, modelos_fase, g)

    metodo_final = None
    n_fases_actual = n_fases0
    lam_actual = lam0

    for _ in range(max_fases):
        # --- Paso 3: hasta 3 iteraciones del bucle externo de Lagrange ---
        resultado_lagrange = resolver_lagrange(
            A, b, lam_actual, n_fases_actual, g, modelos_fase,
            tol_interno=tol_interno, tol_externo=tol_externo,
            max_iter_externo=max_iter_ssa_externo,
        )
        historial.append(resultado_lagrange["iteraciones_externas"])

        if resultado_lagrange["convergido"]:
            metodo_final = "lagrange"
            lam_actual = resultado_lagrange["lambda"]
            n_fases_actual = resultado_lagrange["n_fases"]
            x_fases_actual = resultado_lagrange["x_fases"]
        else:
            # --- Cambiar al RAND modificado hasta convergencia ---
            resultado_rand = resolver_rand_modificado(
                A, b, resultado_lagrange["lambda"], resultado_lagrange["n_fases"],
                g, modelos_fase, tol=tol_rand,
            )
            metodo_final = "rand"
            lam_actual = resultado_rand["lambda"]
            n_fases_actual = resultado_rand["n_fases"]
            x_fases_actual = resultado_rand["x_fases"]

        # --- Paso 4: analisis de estabilidad (igual que SSA) ---
        z = x_fases_actual[0]
        modelo_feed = modelos_fase[0]
        es_estable, mejor = analizar_estabilidad(z, modelo_feed, modelos_trial_candidatos)

        if es_estable:
            return {
                "lambda": lam_actual,
                "n_fases": n_fases_actual,
                "x_fases": x_fases_actual,
                "modelos_fase": modelos_fase,
                "estable": True,
                "historial_fases": historial,
                "metodo_final": metodo_final,
            }

        n_nueva_fase, modelo_nuevo = _candidato_estabilidad_a_fase(mejor)
        n_fases_actual = n_fases_actual + [n_nueva_fase]
        modelos_fase = modelos_fase + [modelo_nuevo]

    return {
        "lambda": lam_actual,
        "n_fases": n_fases_actual,
        "x_fases": x_fases_actual,
        "modelos_fase": modelos_fase,
        "estable": False,
        "historial_fases": historial,
        "metodo_final": metodo_final,
    }


if __name__ == "__main__":
    # Demostracion / depuracion independiente: caso MTBE bifasico
    # (p = 0.80 bar, ver ejemplo_mtbe.py para el detalle y las
    # advertencias sobre los datos ilustrativos usados), resuelto con
    # ambos algoritmos de este modulo.
    print("algoritmos.py -- demostracion independiente")

    A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    b = A @ np.array([1.0, 1.1, 0.0])
    g = np.array([0.0, 0.0, -np.log(50.0)])
    Psat = np.array([5.593617, 0.522141, 0.773075])
    modelo_liquido = {"tipo": "liquido_ideal", "Psat": Psat, "p0": 1.01325}
    modelo_vapor = {"tipo": "vapor_ideal", "p": 0.80, "p0": 1.01325}

    r_ssa = successive_substitution_algorithm(
        A, b, n_t_fase_inicial=2.1, modelo_fase_inicial=modelo_liquido,
        g=g, modelos_trial_candidatos=[modelo_vapor, modelo_liquido],
    )
    print(f"SSA: estable={r_ssa['estable']}, fases={len(r_ssa['n_fases'])}, "
          f"historial={r_ssa['historial_fases']}")

    r_ca = combined_algorithm(
        A, b, n_t_fase_inicial=2.1, modelo_fase_inicial=modelo_liquido,
        g=g, modelos_trial_candidatos=[modelo_vapor, modelo_liquido],
    )
    print(f"Combinado: estable={r_ca['estable']}, fases={len(r_ca['n_fases'])}, "
          f"metodo_final={r_ca['metodo_final']}, historial={r_ca['historial_fases']}")

    for k, (n_ssa, n_ca) in enumerate(zip(r_ssa["n_fases"], r_ca["n_fases"])):
        print(f"Fase {k+1}: max|n_SSA - n_CA| = {np.max(np.abs(n_ssa - n_ca)):.3e}")
