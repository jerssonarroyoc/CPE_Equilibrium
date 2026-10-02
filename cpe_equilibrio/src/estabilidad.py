"""
estabilidad.py
================

Analisis de estabilidad de Michelsen (seccion 3.1.3, pag. 33-34 de la
tesis de Tsanas). Determina si un conjunto de fases propuesto es
estable, o si se debe anadir una fase adicional para seguir
disminuyendo la energia de Gibbs del sistema.

Ecuaciones implementadas (verificadas contra el PDF original)
---------------------------------------------------------------
Ec. 3.26:
    TPD(w) = sum_i w_i * [mu_i(w) - mu_i(z)]

Ec. 3.27 (TPD reducida, adimensional):
    tpd(w) = sum_i w_i * [ln(w_i) + ln(Gamma_i,trial(w))
                           - ln(z_i) - ln(Gamma_i,feed(z))]

Ec. 3.28 (funcion modificada de Michelsen, en numero de moles W_i en
vez de fracciones w_i, para evitar la restriccion sum(w)=1 durante la
busqueda):
    tm(W) = 1 + sum_i W_i * [ln(W_i) + ln(Gamma_i,trial(w))
                              - ln(z_i) - ln(Gamma_i,feed(z)) - 1]
    con w_i = W_i / sum_q(W_q)

Ec. 3.29:
    w_i = W_i / sum_q(W_q)

Generalizacion usada aqui: el termino "ln(phi_i)" de la Ec. 3.27-3.28
original se reemplaza por "ln(Gamma_i)" (termodinamica.py), que incluye
tanto la no-idealidad intrinseca (gamma o phi) como el termino de
referencia de presion de vapor/presion total. Esto es valido porque el
potencial quimico reducido de referencia g_i(T) (comun a ambas fases,
msima T) se cancela identicamente en la diferencia mu_i(w) - mu_i(z);
ver derivacion en el docstring de _diferencia_potencial_quimico.

Si tm(W) < 0 para algun W probado, la fase de alimentacion z es
inestable y se debe anadir una fase nueva con composicion
w = W / sum(W) (Eq. 3.29).
"""

import numpy as np

from termodinamica import ln_Gamma_fase


def _diferencia_potencial_quimico(w, z, modelo_trial, modelo_feed):
    """
    Calcula, componente a componente, [mu_i(w) - mu_i(z)] / RT, usando
    mu_i/RT = g_i(T) + ln(x_i) + ln(Gamma_i). El termino g_i(T) es el
    mismo en ambas fases (misma temperatura) y se cancela
    identicamente, por lo que no es necesario conocerlo para el
    analisis de estabilidad:

        [mu_i(w) - mu_i(z)] / RT = [ln(w_i) + ln(Gamma_i,trial(w))]
                                  - [ln(z_i) + ln(Gamma_i,feed(z))]

    Retorna
    -------
    diferencia : ndarray, shape (NC,)
    ln_Gamma_w : ndarray, shape (NC,)
    ln_Gamma_z : ndarray, shape (NC,)
    """
    ln_Gamma_w = ln_Gamma_fase(
        modelo_trial["tipo"], w, p=modelo_trial.get("p"), p0=modelo_trial.get("p0"),
        Psat=modelo_trial.get("Psat"), Lambda=modelo_trial.get("Lambda"),
        T=modelo_trial.get("T"), chemgroups=modelo_trial.get("chemgroups"),
        unifac_version=modelo_trial.get("unifac_version", 0),
    )
    ln_Gamma_z = ln_Gamma_fase(
        modelo_feed["tipo"], z, p=modelo_feed.get("p"), p0=modelo_feed.get("p0"),
        Psat=modelo_feed.get("Psat"), Lambda=modelo_feed.get("Lambda"),
        T=modelo_feed.get("T"), chemgroups=modelo_feed.get("chemgroups"),
        unifac_version=modelo_feed.get("unifac_version", 0),
    )
    diferencia = (np.log(w) + ln_Gamma_w) - (np.log(z) + ln_Gamma_z)
    return diferencia, ln_Gamma_w, ln_Gamma_z


def tpd(w, z, modelo_trial, modelo_feed):
    """
    Funcion de distancia al plano tangente reducida, Ec. 3.27.

    Parametros
    ----------
    w : ndarray, shape (NC,)
        Composicion (fracciones molares) de la fase de prueba.
    z : ndarray, shape (NC,)
        Composicion de la fase de alimentacion.
    modelo_trial, modelo_feed : dict
        Modelos termodinamicos (ver termodinamica.ln_Gamma_fase) de la
        fase de prueba y de la fase de alimentacion, respectivamente.

    Retorna
    -------
    tpd : float
    """
    diferencia, _, _ = _diferencia_potencial_quimico(w, z, modelo_trial, modelo_feed)
    return np.sum(w * diferencia)


def tm(W, z, modelo_trial, modelo_feed):
    """
    Funcion modificada de Michelsen (1982), Ec. 3.28, en numero de
    moles W_i (sin normalizar) de la fase de prueba.

    Parametros
    ----------
    W : ndarray, shape (NC,)
        Numero de moles (no normalizado) de la fase de prueba.
    z : ndarray, shape (NC,)
    modelo_trial, modelo_feed : dict

    Retorna
    -------
    tm : float
    """
    w = W / np.sum(W)  # Ec. 3.29
    diferencia, _, _ = _diferencia_potencial_quimico(w, z, modelo_trial, modelo_feed)
    return 1.0 + np.sum(W * (diferencia - 1.0))


def _iteracion_sustitucion_sucesiva(W0, z, modelo_trial, modelo_feed,
                                     max_iter=200, tol=1e-12):
    """
    Busca un punto estacionario de tm(W) por sustitucion sucesiva
    (metodo estandar de Michelsen para el analisis de estabilidad):

        ln(W_i^(nuevo)) = ln(z_i) + ln(Gamma_i,feed(z)) - ln(Gamma_i,trial(w^(viejo)))

    No es necesario converger completamente: si tm(W) se vuelve
    negativo durante la busqueda, la fase es inestable y podemos
    detenernos de inmediato (tal como indica la tesis, pag. 34).

    Retorna
    -------
    W : ndarray
        Ultimo iterado (normalizado solo para evaluar Gamma).
    tm_min : float
        Valor minimo de tm(W) encontrado durante la busqueda.
    inestable : bool
    """
    W = np.array(W0, dtype=float)
    tm_min = tm(W, z, modelo_trial, modelo_feed)
    inestable = tm_min < 0.0

    _, _, ln_Gamma_z = _diferencia_potencial_quimico(
        W / np.sum(W), z, modelo_trial, modelo_feed
    )

    for _ in range(max_iter):
        w = W / np.sum(W)
        ln_Gamma_w = ln_Gamma_fase(
            modelo_trial["tipo"], w, p=modelo_trial.get("p"), p0=modelo_trial.get("p0"),
            Psat=modelo_trial.get("Psat"), Lambda=modelo_trial.get("Lambda"),
            T=modelo_trial.get("T"), chemgroups=modelo_trial.get("chemgroups"),
            unifac_version=modelo_trial.get("unifac_version", 0),
        )
        ln_W_nuevo = np.log(z) + ln_Gamma_z - ln_Gamma_w
        W_nuevo = np.exp(ln_W_nuevo)

        valor_tm = tm(W_nuevo, z, modelo_trial, modelo_feed)
        if valor_tm < tm_min:
            tm_min = valor_tm
        if valor_tm < 0.0:
            inestable = True
            W = W_nuevo
            break  # no hace falta converger: ya detectamos inestabilidad

        error = np.sqrt(np.sum((np.log(W_nuevo) - np.log(W)) ** 2))
        W = W_nuevo
        if error < tol:
            break

    return W, tm_min, inestable


def analizar_estabilidad(z, modelo_feed, modelos_trial_candidatos, max_iter=200):
    """
    Analiza si la fase de alimentacion z (con el modelo modelo_feed) es
    estable, probando varios modelos/tipos de fase de prueba y varias
    composiciones iniciales (practica estandar de Michelsen: una por
    cada componente puro, mas la composicion de alimentacion invertida).

    Parametros
    ----------
    z : ndarray, shape (NC,)
        Composicion de la fase de alimentacion (debe sumar 1 y no
        contener ceros exactos; usar un valor pequeno como piso si
        algun componente esta ausente).
    modelo_feed : dict
        Modelo termodinamico de la fase de alimentacion.
    modelos_trial_candidatos : list[dict]
        Lista de modelos termodinamicos candidatos para la fase de
        prueba (p. ej. un modelo de vapor y otro de liquido, para
        cubrir tanto inestabilidad LV como LL).
    max_iter : int
        Iteraciones maximas de sustitucion sucesiva por cada intento.

    Retorna
    -------
    es_estable : bool
    mejor_resultado : dict o None
        Si es inestable, contiene {"w": composicion de la fase nueva,
        "tm": valor de tm, "modelo_trial": modelo usado}.
    """
    nc = len(z)
    mejor_tm = np.inf
    mejor_resultado = None

    for modelo_trial in modelos_trial_candidatos:
        # Una composicion inicial de prueba por cada componente puro,
        # mas pequenas trazas del resto para evitar log(0).
        candidatos_W0 = []
        piso = 1e-10
        for i in range(nc):
            W0 = np.full(nc, piso)
            W0[i] = 1.0
            candidatos_W0.append(W0 / np.sum(W0))

        for W0 in candidatos_W0:
            W_final, tm_min, inestable = _iteracion_sustitucion_sucesiva(
                W0, z, modelo_trial, modelo_feed, max_iter=max_iter
            )
            if tm_min < mejor_tm:
                mejor_tm = tm_min
                mejor_resultado = {
                    "w": W_final / np.sum(W_final),
                    "tm": tm_min,
                    "modelo_trial": modelo_trial,
                }
            if inestable:
                # Encontramos inestabilidad: no hace falta seguir
                # probando mas candidatos (pag. 34: "no need to fully
                # converge... if negative tm is found, phase split
                # will occur").
                return False, mejor_resultado

    es_estable = mejor_tm >= 0.0
    return es_estable, mejor_resultado


if __name__ == "__main__":
    # Demostracion / depuracion independiente: una fase liquida de MTBE
    # (rica en producto, subenfriada segun ejemplo_mtbe.py a 1 atm) se
    # prueba por estabilidad contra una fase vapor. Se espera "estable"
    # a 1 atm y "inestable" a una presion menor (ver ejemplo_mtbe.py,
    # Caso 2, donde esta misma composicion si forma una fase vapor).
    print("estabilidad.py -- demostracion independiente")

    z = np.array([0.036340, 0.123946, 0.839714])  # liquido convergido a 1 atm
    Psat = np.array([5.593617, 0.522141, 0.773075])

    modelo_liquido = {"tipo": "liquido_ideal", "Psat": Psat, "p0": 1.01325}

    for p_prueba in [1.01325, 0.80]:
        modelo_vapor = {"tipo": "vapor_ideal", "p": p_prueba, "p0": 1.01325}
        estable, mejor = analizar_estabilidad(z, modelo_liquido, [modelo_vapor, modelo_liquido])
        print(f"p = {p_prueba:.5f} bar -> estable={estable}  "
              f"(mejor tm encontrado = {mejor['tm']:.4f})")
