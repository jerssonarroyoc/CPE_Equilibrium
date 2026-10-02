"""
termodinamica.py
=================

Funciones termodinamicas base para los metodos no-estequiometricos de
Tsanas (DTU, 2018), "Simultaneous Chemical and Phase Equilibrium
Calculations with Non-Stoichiometric Method".

Formulacion adoptada (consistente con las Ec. 3.34-3.36 de la tesis,
pagina 35-36, verificadas contra el PDF original):

    mu_ik / RT = g_i(T) + ln(x_ik) + ln(Gamma_ik)                 (*)

donde:
    g_i(T)      = mu*_i(T) / RT, el potencial quimico reducido del
                  componente puro i en el estado de referencia elegido
                  (aqui: gas ideal puro a T y presion de referencia p0).
                  Es el "gauge" que fija el origen de energia de cada
                  componente; solo la combinacion sum_i nu_i * g_i(T)
                  (ligada a K_eq via Eq. 2.33 de la tesis) tiene efecto
                  fisico sobre la composicion de equilibrio.
    Gamma_ik    = factor de no-idealidad de la fase k para el
                  componente i:
                    - fase vapor (gas ideal):  Gamma_ik = phi_ik * p / p0 = p / p0
                    - fase liquida (Raoult modificada): Gamma_ik = gamma_ik * Psat_i(T) / p0

Esta forma es algebraicamente identica a la Ec. 3.34 de la tesis, solo
que se usa fugacidad (en vez de separar "ideal gas reference" /
"pure component reference") para no necesitar dos tablas de datos
distintas: la misma g_i(T) sirve para ambas fases porque la condicion
de equilibrio de fases puro-componente (f_i^L,puro = f_i^V,puro a Psat)
ya esta incorporada en el termino Psat_i(T).

ADVERTENCIA SOBRE LOS DATOS NUMERICOS
--------------------------------------
Ni equilibrio.md ni el PDF de la tesis contienen las tablas de
parametros de Wilson/UNIQUAC, los coeficientes de Antoine ni las
correlaciones K_eq(T) usadas en el Capitulo 4 (se citan de Ung and
Doherty 1995e, Xiao et al. 1989, Maurer 1986, Saito et al. 1971, que
no estan en los documentos disponibles). Las funciones de este modulo
son de proposito general: cualquier conjunto de parametros (Wilson,
Antoine, K_eq) puede pasarse como argumento. Los valores usados en
ejemplo_mtbe.py estan marcados explicitamente como "ilustrativos" o
"literatura publica (NIST)" segun corresponda -- ver docstring de ese
archivo.
"""

import numpy as np

# Penalizacion (en ln_Gamma) usada por los tipos de fase que excluyen
# especies por mascara ("condensado_puro", "vapor_ideal_con_exclusion"):
# ver el docstring de esos tipos en ln_Gamma_fase.
PENALIZACION_EXCLUSION = 300.0


# ---------------------------------------------------------------------------
# Presion de vapor (ecuacion de Antoine)
# ---------------------------------------------------------------------------

def antoine_psat(T, A, B, C):
    """
    Presion de vapor de un componente puro, ecuacion de Antoine:

        log10(Psat) = A - B / (T + C)

    Parametros
    ----------
    T : float
        Temperatura absoluta [K].
    A, B, C : float
        Coeficientes de Antoine (forma log10, T en K, Psat en bar o
        mmHg segun como se hayan ajustado los coeficientes: el llamador
        debe ser consistente con las unidades de p0 y p usadas en el
        resto del calculo).

    Retorna
    -------
    Psat : float
        Presion de vapor del componente puro a la temperatura T.
    """
    # Despejamos Psat de la forma logaritmica de Antoine.
    return 10.0 ** (A - B / (T + C))


# ---------------------------------------------------------------------------
# Fase vapor: gas ideal (phi_ik = 1 para todos los componentes)
# ---------------------------------------------------------------------------

def ln_gamma_vapor_ideal(x):
    """
    Logaritmo del coeficiente de fugacidad para un gas ideal: ln(phi) = 0.

    Parametros
    ----------
    x : ndarray, shape (NC,)
        Fracciones molares en la fase vapor (no se usan, se mantienen
        por consistencia de interfaz con los modelos no ideales).

    Retorna
    -------
    ln_phi : ndarray, shape (NC,)
        Vector de ceros (gas ideal no introduce no-idealidad).
    """
    # Gas ideal: el coeficiente de fugacidad es exactamente 1 para
    # todos los componentes, independientemente de la composicion.
    return np.zeros_like(x)


def dln_phi_dn_vapor_ideal(n):
    """
    Derivadas composicionales de ln(phi) para gas ideal: todas cero.

    Esta es la matriz Phi_iqk de la Ec. 3.49 cuando la fase es un gas
    ideal (phi_ik = 1 siempre, por lo que ninguna derivada respecto a
    n_q puede ser distinta de cero).

    Parametros
    ----------
    n : ndarray, shape (NC,)
        Numero de moles de cada componente en la fase (no se usan).

    Retorna
    -------
    Phi : ndarray, shape (NC, NC)
        Matriz de ceros.
    """
    nc = len(n)
    return np.zeros((nc, nc))


# ---------------------------------------------------------------------------
# Fase liquida: solucion ideal (gamma_ik = 1 para todos los componentes)
# ---------------------------------------------------------------------------

def gamma_ideal(x):
    """
    Coeficientes de actividad de una solucion liquida ideal: gamma_i = 1.

    Parametros
    ----------
    x : ndarray, shape (NC,)
        Fracciones molares en la fase liquida.

    Retorna
    -------
    gamma : ndarray, shape (NC,)
        Vector de unos.
    """
    # Solucion ideal: ninguna interaccion molecular adicional a la
    # entropia de mezcla ideal, por lo que gamma_i = 1 siempre.
    return np.ones_like(x)


def dln_gamma_dn_ideal(n):
    """
    Derivadas composicionales de ln(gamma) para solucion ideal: cero.

    Analogo liquido de dln_phi_dn_vapor_ideal: en una solucion ideal
    gamma_i no depende de la composicion, por lo que Phi_iqk = 0.

    Parametros
    ----------
    n : ndarray, shape (NC,)
        Numero de moles de cada componente en la fase liquida.

    Retorna
    -------
    Phi : ndarray, shape (NC, NC)
        Matriz de ceros.
    """
    nc = len(n)
    return np.zeros((nc, nc))


# ---------------------------------------------------------------------------
# Fase liquida: modelo de Wilson (1964)
# ---------------------------------------------------------------------------

def gamma_wilson(x, Lambda):
    """
    Coeficientes de actividad del modelo de Wilson (1964).

        ln(gamma_i) = 1 - ln(S_i) - sum_k [ x_k * Lambda_ki / S_k ]
        S_i = sum_j x_j * Lambda_ij

    con Lambda_ii = 1 por definicion.

    Parametros
    ----------
    x : ndarray, shape (NC,)
        Fracciones molares en la fase liquida.
    Lambda : ndarray, shape (NC, NC)
        Matriz de parametros de interaccion binaria de Wilson
        (Lambda[i, j] = Lambda_ij). Debe cumplir Lambda_ii = 1.

    Retorna
    -------
    gamma : ndarray, shape (NC,)
        Coeficientes de actividad de cada componente.
    """
    nc = len(x)
    # S_i = suma ponderada por composicion de los parametros de Wilson
    # de la fila i: representa la "interaccion efectiva" del
    # componente i con el resto de la mezcla.
    S = Lambda @ x  # S[i] = sum_j Lambda[i, j] * x[j]

    ln_gamma = np.zeros(nc)
    for i in range(nc):
        # Primer y segundo termino: contribucion directa de la mezcla
        # alrededor del componente i.
        termino_directo = 1.0 - np.log(S[i])
        # Tercer termino: suma sobre todos los componentes k de como
        # el componente i contribuye a la mezcla "vista" por k.
        suma_cruzada = np.sum(x * Lambda[:, i] / S)
        ln_gamma[i] = termino_directo - suma_cruzada
    return np.exp(ln_gamma)


def dln_gamma_dn_wilson(n, Lambda):
    """
    Derivadas composicionales ∂ln(gamma_i)/∂n_q (a T, p y n_{j!=q}
    constantes) del modelo de Wilson.

    Se deriva directamente de ln(gamma_i) escrita en numero de moles
    (no fracciones), para evitar errores de regla de la cadena:

        T_i = sum_j n_j * Lambda_ij          (nota: T_i = n_t * S_i)
        ln(gamma_i) = 1 - ln(T_i) + ln(n_t) - sum_k [ n_k * Lambda_ki / T_k ]

    Derivando respecto a n_q:

        d ln(gamma_i) / d n_q =
              - Lambda_iq / T_i
              - Lambda_qi / T_q
              + 1 / n_t
              + sum_k [ n_k * Lambda_ki * Lambda_kq / T_k^2 ]

    Esta es la matriz Phi_iqk de la Ec. 3.49 de la tesis para una fase
    liquida descrita por el modelo de Wilson.

    Parametros
    ----------
    n : ndarray, shape (NC,)
        Numero de moles de cada componente en la fase liquida.
    Lambda : ndarray, shape (NC, NC)
        Matriz de parametros de interaccion binaria de Wilson.

    Retorna
    -------
    Phi : ndarray, shape (NC, NC)
        Phi[i, q] = d ln(gamma_i) / d n_q.
    """
    nc = len(n)
    n_t = np.sum(n)  # moles totales de la fase
    # T_i = suma de interacciones de Wilson ponderada por moles
    # (version "no normalizada" de S_i, mas comoda para derivar).
    T = Lambda @ n  # T[i] = sum_j Lambda[i, j] * n[j]

    Phi = np.zeros((nc, nc))
    for i in range(nc):
        for q in range(nc):
            termino_1 = -Lambda[i, q] / T[i]
            termino_2 = -Lambda[q, i] / T[q]
            termino_3 = 1.0 / n_t
            # Suma sobre todos los componentes k de la mezcla: como el
            # cambio en n_q afecta T_k, que a su vez afecta el termino
            # cruzado de ln(gamma_i).
            termino_4 = np.sum(n * Lambda[:, i] * Lambda[:, q] / T**2)
            Phi[i, q] = termino_1 + termino_2 + termino_3 + termino_4
    return Phi


# ---------------------------------------------------------------------------
# Fase liquida: solucion regular binaria de un parametro (Margules de un
# parametro), usada para validar modified_rand.py contra el ejemplo
# numerico de Greiner (1991), Apendice B -- ver pruebas_validacion.py.
#
#   G^E/RT = Lambda * x_A * x_B   (por mol de mezcla, NC=2 unicamente)
#   ln(gamma_A) = Lambda * x_B^2
#   ln(gamma_B) = Lambda * x_A^2
# ---------------------------------------------------------------------------

def gamma_regular_binaria(x, Lambda):
    """
    Coeficientes de actividad de una solucion regular binaria de un
    parametro (resultado estandar de diferenciar G^E/RT = Lambda*x_A*x_B
    respecto al numero de moles de cada componente).

    Parametros
    ----------
    x : ndarray, shape (2,)
        Fracciones molares [x_A, x_B].
    Lambda : float
        Parametro de interaccion (adimensional, en unidades de RT).

    Retorna
    -------
    gamma : ndarray, shape (2,)
    """
    xA, xB = x
    ln_gamma = np.array([Lambda * xB ** 2, Lambda * xA ** 2])
    return np.exp(ln_gamma)


def dln_gamma_dn_regular_binaria(n, Lambda):
    """
    Derivadas composicionales d ln(gamma_i)/d n_q de la solucion regular
    binaria, obtenidas derivando dos veces la energia de Gibbs en exceso
    extensiva n_t*G^E/RT = Lambda*n_A*n_B/n_t respecto a los numeros de
    mol (Hessiano, por construccion simetrico):

        d ln(gamma_A)/d n_A = -2*Lambda*n_B^2/n_t^3
        d ln(gamma_A)/d n_B =  2*Lambda*n_A*n_B/n_t^3
        d ln(gamma_B)/d n_B = -2*Lambda*n_A^2/n_t^3
        d ln(gamma_B)/d n_A =  2*Lambda*n_A*n_B/n_t^3  (= d ln(gamma_A)/d n_B)

    Parametros
    ----------
    n : ndarray, shape (2,)
    Lambda : float

    Retorna
    -------
    Phi : ndarray, shape (2, 2)
    """
    nA, nB = n
    n_t = nA + nB
    cruzado = 2.0 * Lambda * nA * nB / n_t ** 3
    Phi = np.array([
        [-2.0 * Lambda * nB ** 2 / n_t ** 3, cruzado],
        [cruzado, -2.0 * Lambda * nA ** 2 / n_t ** 3],
    ])
    return Phi


# ---------------------------------------------------------------------------
# Fase liquida: UNIFAC (predictivo, sin parametros binarios ajustados),
# via la libreria `thermo` (Caleb Bell). Se usa cuando no se dispone de
# parametros de Wilson/NRTL/UNIQUAC ajustados para el sistema de interes
# -- ver pruebas_validacion.py, test_acetic_ethanol_esterification, para
# el caso de uso (ninguno de los libros de texto consultados trae
# parametros binarios para acido acetico/etanol/agua/acetato de etilo).
#
# Los grupos UNIFAC de cada componente (chemgroups) deben obtenerse de
# la asignacion oficial DDBST (thermo.unifac.DDBST_UNIFAC_assignments,
# indexada por InChIKey), NO fragmentando las moleculas a mano, para
# eliminar el riesgo de una fragmentacion incorrecta.
# ---------------------------------------------------------------------------

def _construir_unifac(x, T, chemgroups, version=0):
    """Construye un objeto thermo.unifac.UNIFAC para la composicion x."""
    from thermo.unifac import UFIP, UFSG, UNIFAC
    return UNIFAC.from_subgroups(
        chemgroups=chemgroups, T=T, xs=list(x),
        version=version, interaction_data=UFIP, subgroups=UFSG,
    )


def gamma_unifac(x, T, chemgroups, version=0):
    """
    Coeficientes de actividad UNIFAC, via `thermo`.

    Parametros
    ----------
    x : ndarray, shape (NC,)
        Fracciones molares.
    T : float
        Temperatura [K].
    chemgroups : list[dict]
        Un dict {subgrupo_UNIFAC: cantidad} por componente, obtenido de
        thermo.unifac.DDBST_UNIFAC_assignments (no a mano).
    version : int
        0 = UNIFAC original (Fredenslund et al.), el que se usa en este
        proyecto por ser el mas ampliamente tabulado.

    Retorna
    -------
    gamma : ndarray, shape (NC,)
    """
    GE = _construir_unifac(x, T, chemgroups, version=version)
    return np.array(GE.gammas())


def dln_gamma_dn_unifac(n, T, chemgroups, version=0):
    """
    Derivadas composicionales d ln(gamma_i)/d n_q del modelo UNIFAC,
    obtenidas de thermo.unifac.UNIFAC.dgammas_dns() (derivada de gamma_i,
    no de ln(gamma_i)) mediante la regla de la cadena:

        d ln(gamma_i)/d n_q = (1/gamma_i) * d(gamma_i)/d n_q

    Parametros
    ----------
    n : ndarray, shape (NC,)
        Numero de moles (se normaliza internamente a fracciones molares
        para construir el objeto UNIFAC).
    T : float
    chemgroups : list[dict]
    version : int

    Retorna
    -------
    Phi : ndarray, shape (NC, NC)
    """
    x = n / np.sum(n)
    GE = _construir_unifac(x, T, chemgroups, version=version)
    gammas = np.array(GE.gammas())
    dgammas_dns = np.array(GE.dgammas_dns())
    # Phi[i, q] = (1/gamma_i) * d(gamma_i)/d n_q
    return dgammas_dns / gammas[:, None]


# ---------------------------------------------------------------------------
# Energia de Gibbs reducida (para monitoreo de convergencia del RAND)
# ---------------------------------------------------------------------------

def gibbs_reducida(n_fases, g, ln_Gamma_fases):
    """
    Energia de Gibbs reducida total G/(RT) del sistema multifasico,
    consistente con la definicion usada antes de la Ec. 3.16:

        G/(RT) = sum_k sum_i n_ik * mu_ik / RT
               = sum_k sum_i n_ik * [ g_i(T) + ln(x_ik) + ln(Gamma_ik) ]

    Se usa en el metodo RAND modificado para verificar que cada paso
    de Newton efectivamente *disminuye* la energia de Gibbs (ver
    comentario tras la Ec. 3.70 de la tesis: "Monitoring of the Gibbs
    energy is the major advantage of the RAND method").

    Parametros
    ----------
    n_fases : list[ndarray]
        Lista de longitud NP; n_fases[k] son los numeros de mol de
        cada componente en la fase k (shape (NC,)).
    g : ndarray, shape (NC,)
        Potencial quimico reducido de referencia g_i(T) de cada
        componente puro.
    ln_Gamma_fases : list[ndarray]
        Lista de longitud NP; ln_Gamma_fases[k] es el vector ln(Gamma_ik)
        (no-idealidad) de la fase k, shape (NC,).

    Retorna
    -------
    G_RT : float
        Energia de Gibbs reducida total del sistema.
    """
    G_RT = 0.0
    for n_k, ln_Gamma_k in zip(n_fases, ln_Gamma_fases):
        n_t_k = np.sum(n_k)
        if n_t_k <= 0.0:
            continue  # fase inexistente (amount cero): no contribuye
        x_k = n_k / n_t_k
        # Evitar log(0) en componentes ausentes de la fase (x_ik = 0):
        # su contribucion n_ik*ln(x_ik) tiende a 0 en el limite.
        with np.errstate(divide="ignore", invalid="ignore"):
            ln_x_k = np.where(n_k > 0.0, np.log(x_k), 0.0)
        G_RT += np.sum(n_k * (g + ln_x_k + ln_Gamma_k))
    return G_RT


# ---------------------------------------------------------------------------
# Despachador generico de modelos de fase: ln(Gamma_ik) y su derivada
# composicional Phi_iqk = d ln(Gamma_ik)/d n_qk (Ec. 3.49).
#
# Gamma_ik es el factor de no-idealidad definido en el encabezado de este
# modulo:
#   - vapor (gas ideal):            Gamma_ik = p / p0            (phi=1)
#   - liquido ideal (Raoult):       Gamma_ik = Psat_i(T) / p0    (gamma=1)
#   - liquido Wilson (Raoult mod.): Gamma_ik = gamma_ik * Psat_i(T) / p0
# ---------------------------------------------------------------------------

def ln_Gamma_fase(tipo, x, p=None, p0=None, Psat=None, Lambda=None,
                   T=None, chemgroups=None, unifac_version=0):
    """
    Calcula ln(Gamma_ik) para una fase, segun el tipo de modelo.

    Parametros
    ----------
    tipo : str
        Uno de {"vapor_ideal", "liquido_ideal", "liquido_wilson",
        "liquido_regular_binaria", "liquido_unifac", "condensado_puro",
        "vapor_ideal_con_exclusion"}.
    x : ndarray, shape (NC,)
        Fracciones molares en la fase (usadas solo por modelos no
        ideales, p. ej. Wilson).
    p, p0 : float
        Presion del sistema y presion de referencia (mismas unidades).
        Requeridos para tipo="vapor_ideal".
    Psat : ndarray, shape (NC,)
        Presiones de vapor de los componentes puros a la temperatura T
        (mismas unidades que p0). Requerido para fases liquidas.
    Lambda : ndarray, shape (NC, NC)
        Matriz de parametros de Wilson. Requerido para
        tipo="liquido_wilson". Para tipo="condensado_puro" esta misma
        llave se reutiliza (ver bloque de ese tipo mas abajo) para pasar
        un vector mascara de un solo componente, en vez de una matriz:
        esto permite anadir el tipo de fase nuevo sin tener que tocar
        ningun llamador existente (lagrange_multipliers.py,
        estabilidad.py, algoritmos.py), que ya reenvian Lambda=m.get
        ("Lambda") a esta funcion para TODOS los tipos de fase.
    T : float
        Temperatura [K]. Requerido para tipo="liquido_unifac".
    chemgroups : list[dict]
        Grupos UNIFAC de cada componente (ver gamma_unifac). Requerido
        para tipo="liquido_unifac".
    unifac_version : int
        0 = UNIFAC original. Solo usado para tipo="liquido_unifac".

    Retorna
    -------
    ln_Gamma : ndarray, shape (NC,)
    """
    if tipo == "vapor_ideal":
        nc = len(x)
        # phi_ik = 1 (gas ideal): Gamma_ik = p/p0 es igual para todos
        # los componentes de la fase vapor.
        return np.full(nc, np.log(p / p0))
    elif tipo == "liquido_ideal":
        # gamma_ik = 1 (solucion ideal): Gamma_ik = Psat_i(T)/p0.
        return np.log(Psat / p0)
    elif tipo == "liquido_wilson":
        gamma = gamma_wilson(x, Lambda)
        return np.log(Psat / p0) + np.log(gamma)
    elif tipo == "liquido_regular_binaria":
        gamma = gamma_regular_binaria(x, Lambda)
        return np.log(Psat / p0) + np.log(gamma)
    elif tipo == "liquido_unifac":
        gamma = gamma_unifac(x, T, chemgroups, version=unifac_version)
        return np.log(Psat / p0) + np.log(gamma)
    elif tipo == "condensado_puro":
        # Fase condensada pura de un solo componente (solido o liquido,
        # p. ej. carbono solido/hollin, o agua liquida condensada de
        # una mezcla de combustion): no hay mezcla de otras especies en
        # esta fase por definicion, y no depende de p ni de T mas alla
        # de lo que ya esta en g_i(T) (se ignora correccion de Poynting,
        # razonable para una fase condensada casi incompresible en un
        # calculo exploratorio -- ver advertencia en combustion_gibbs.py).
        #
        # Se modela dando Gamma_ik = 1 (ln=0) a la UNICA especie que
        # puede estar en esta fase (marcada con 1.0 en el vector mascara
        # "Lambda"), y una penalizacion enorme (ln_Gamma >> 1) a todas
        # las demas, de forma que x_ik = exp(A^T*lambda - g_i - ln_Gamma_ik)
        # (Ec. 3.34) subdesborda (underflow) a 0 para cualquier especie
        # que no sea la pura, sin necesidad de restringir la forma
        # matricial compartida por todas las fases en
        # lagrange_multipliers.py. El valor exacto de la penalizacion
        # solo debe ser mucho mayor que el rango tipico de
        # (A^T*lambda - g_i) para que exp() subdesborde limpiamente (sin
        # overflow, que si ocurriria con el signo opuesto) -- no influye
        # en el resultado mientras sea "suficientemente grande".
        mascara = Lambda
        return np.where(mascara > 0.5, 0.0, PENALIZACION_EXCLUSION)
    elif tipo == "vapor_ideal_con_exclusion":
        # Identico a "vapor_ideal", pero excluyendo explicitamente las
        # especies que NO tienen sentido fisico como constituyentes de
        # la fase vapor (p. ej. "C(s)" o "H2O(l)": su g_i(T) esta
        # referida al estado de referencia CONDENSADO puro, no a gas
        # ideal puro a p0, asi que tratarlas como un componente mas de
        # la fase vapor_ideal seria termodinamicamente incorrecto --
        # vapor_ideal por si solo no distingue especies, por lo que
        # cualquier especie presente en el vector de especies compartido
        # por todas las fases "se cuela" en la fase vapor con un
        # Gamma_ik = p/p0 que no le corresponde). Se reutiliza, otra vez,
        # el mismo mecanismo de mascara + penalizacion de
        # "condensado_puro": Lambda aqui es el vector mascara de
        # especies SI permitidas en vapor (1.0 permitida, 0.0 excluida).
        mascara_permitidas = Lambda
        base = np.log(p / p0)
        return np.where(mascara_permitidas > 0.5, base, PENALIZACION_EXCLUSION)
    else:
        raise ValueError(f"Tipo de fase desconocido: {tipo!r}")


def dln_Gamma_dn_fase(tipo, n, Lambda=None, T=None, chemgroups=None, unifac_version=0):
    """
    Calcula la matriz Phi_iqk = d ln(Gamma_ik) / d n_qk (Ec. 3.49),
    usada en el metodo RAND modificado.

    Parametros
    ----------
    tipo : str
        Uno de {"vapor_ideal", "liquido_ideal", "liquido_wilson",
        "liquido_regular_binaria", "liquido_unifac", "condensado_puro",
        "vapor_ideal_con_exclusion"}.
    n : ndarray, shape (NC,)
        Numero de moles de cada componente en la fase.
    Lambda : ndarray, shape (NC, NC)
        Requerido para tipo="liquido_wilson" o "liquido_regular_binaria".
    T : float
        Temperatura [K]. Requerido para tipo="liquido_unifac".
    chemgroups : list[dict]
        Requerido para tipo="liquido_unifac".
    unifac_version : int
        Solo usado para tipo="liquido_unifac".

    Retorna
    -------
    Phi : ndarray, shape (NC, NC)
    """
    if tipo in ("vapor_ideal", "liquido_ideal", "condensado_puro",
                "vapor_ideal_con_exclusion"):
        # p/p0, Psat_i/p0 y las mascaras de "condensado_puro"/
        # "vapor_ideal_con_exclusion" no dependen de la composicion ->
        # Phi = 0 en los cuatro casos.
        nc = len(n)
        return np.zeros((nc, nc))
    elif tipo == "liquido_wilson":
        return dln_gamma_dn_wilson(n, Lambda)
    elif tipo == "liquido_regular_binaria":
        return dln_gamma_dn_regular_binaria(n, Lambda)
    elif tipo == "liquido_unifac":
        return dln_gamma_dn_unifac(n, T, chemgroups, version=unifac_version)
    else:
        raise ValueError(f"Tipo de fase desconocido: {tipo!r}")


if __name__ == "__main__":
    # Demostracion / depuracion independiente de este modulo: valida el
    # modelo de Wilson contra diferencias finitas (gamma y su derivada
    # composicional), sin depender de ningun otro archivo del proyecto.
    print("termodinamica.py -- demostracion independiente")

    rng = np.random.default_rng(1)
    nc = 3
    Lambda = np.abs(rng.random((nc, nc))) * 0.8 + 0.2
    np.fill_diagonal(Lambda, 1.0)
    x = np.array([0.5, 0.3, 0.2])
    n = x * 4.0

    gamma = gamma_wilson(x, Lambda)
    print(f"gamma_wilson(x={x}) = {gamma}")

    Phi = dln_gamma_dn_wilson(n, Lambda)
    eps = 1e-6
    Phi_num = np.zeros((nc, nc))
    for q in range(nc):
        n_mas, n_menos = n.copy(), n.copy()
        n_mas[q] += eps
        n_menos[q] -= eps
        Phi_num[:, q] = (
            np.log(gamma_wilson(n_mas / np.sum(n_mas), Lambda))
            - np.log(gamma_wilson(n_menos / np.sum(n_menos), Lambda))
        ) / (2 * eps)
    print(f"max|Phi_analitico - Phi_numerico| = {np.max(np.abs(Phi - Phi_num)):.3e}"
          "  (debe ser ~1e-9 o menor)")

    # Energia de Gibbs de una mezcla ideal de 2 fases, como chequeo rapido.
    g = np.zeros(nc)
    n_fases = [np.array([1.0, 1.0, 1.0]), np.array([0.5, 0.5, 0.5])]
    ln_Gamma_fases = [np.zeros(nc), np.zeros(nc)]
    print(f"G/(RT) de ejemplo = {gibbs_reducida(n_fases, g, ln_Gamma_fases):.6f}")
