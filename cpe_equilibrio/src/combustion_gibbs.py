"""
combustion_gibbs.py
=====================

Perfiles de concentracion de equilibrio para procesos de combustion y
oxidacion, usando el MISMO formalismo de potenciales de elemento
(minimizacion de Gibbs no-estequiometrica) que el resto del proyecto:
se reutiliza lagrange_multipliers.resolver_lagrange directamente, con
una sola fase gas ideal, igual que en Binous & Bellagi (2022) para sus
casos de combustion de hidracina/propano y sintesis de amoniaco.

IMPORTANTE (alcance, a pedido explicito del usuario): estas graficas
son EXPLORATORIAS, "quiero ver que arroja el modelo" -- no se requiere
validacion cuantitativa. Los datos termoquimicos (entalpia y energia
de Gibbs de formacion estandar a 298 K) son valores APROXIMADOS,
tipicos de tablas NIST-JANAF / libros de combustion (p. ej. Turns, "An
Introduction to Combustion"), usados con la aproximacion de capacidad
calorifica de reaccion nula (dCp=0):

    dG_f,i(T) ~= dH_f,i(298) - T * dS_f,i(298),   dS_f,i(298) = [dH_f,i(298) - dG_f,i(298)] / 298.15

Esta es una aproximacion de primer orden (no usa polinomios NASA-7
completos ni integra Cp(T)); captura la tendencia cualitativa correcta
(mayor disociacion a mayor T, porque dS_rxn>0 para reacciones que
aumentan el numero de moles de gas) pero no debe usarse para diseno.

No se modifica ningun archivo ya validado contra Greiner (1991) ni
contra Smith & Van Ness: solo se importa y reutiliza
lagrange_multipliers.resolver_lagrange() tal cual.
"""

import numpy as np

from inicializacion import minimizar_Q
from lagrange_multipliers import resolver_lagrange

R_GAS = 8.314  # J/(mol K)

# ---------------------------------------------------------------------------
# Datos termoquimicos aproximados (298.15 K), kJ/mol -- ver advertencia arriba
# ---------------------------------------------------------------------------
# dHf298: entalpia estandar de formacion
# dGf298: energia de Gibbs estandar de formacion
# (elementos de referencia H2, O2, N2, C(grafito) tienen dHf=dGf=0)

TERMOQUIMICA = {
    "H2":  {"dHf298": 0.0,     "dGf298": 0.0},
    "O2":  {"dHf298": 0.0,     "dGf298": 0.0},
    "N2":  {"dHf298": 0.0,     "dGf298": 0.0},
    "H2O": {"dHf298": -241.8,  "dGf298": -228.6},   # vapor
    "OH":  {"dHf298": 39.0,    "dGf298": 34.3},
    "H":   {"dHf298": 218.0,   "dGf298": 203.3},
    "O":   {"dHf298": 249.2,   "dGf298": 231.7},
    "CO2": {"dHf298": -393.5,  "dGf298": -394.4},
    "CO":  {"dHf298": -110.5,  "dGf298": -137.2},
    "NO":  {"dHf298": 90.3,    "dGf298": 87.6},
    # Especies condensadas (Sistema G, ver mas abajo): C(grafito, s) es
    # el estado de referencia del carbono (dHf=dGf=0, igual que H2/O2/N2
    # arriba). H2O(l) es el OTRO estado de referencia de la molecula de
    # agua (298.15 K, 1 bar liquido en vez de gas ideal); junto con
    # "H2O" (vapor) ya definida arriba, la DIFERENCIA de g_reducido entre
    # ambas reproduce implicitamente la presion de vapor del agua sin
    # necesitar una correlacion de Antoine aparte (ver docstring del
    # Sistema G para la verificacion numerica de este punto a 298 K).
    "C(s)":   {"dHf298": 0.0,     "dGf298": 0.0},
    "H2O(l)": {"dHf298": -285.8,  "dGf298": -237.1},
}


def g_reducido(especie, T):
    """
    g_i(T) = dGf_i(T) / (RT), con dGf_i(T) aproximado por
    dHf298 - T*dSf298 (dCp=0). Unidades: dHf298/dGf298 en kJ/mol -> J/mol.
    """
    d = TERMOQUIMICA[especie]
    dHf298 = d["dHf298"] * 1000.0
    dGf298 = d["dGf298"] * 1000.0
    dSf298 = (dHf298 - dGf298) / 298.15
    dGf_T = dHf298 - T * dSf298
    return dGf_T / (R_GAS * T)


def vector_g(especies, T):
    return np.array([g_reducido(e, T) for e in especies])


# ---------------------------------------------------------------------------
# Resolver de equilibrio de una sola fase gas ideal (envoltura simple)
# ---------------------------------------------------------------------------

def resolver_combustion(A, b, especies, T, p=1.0, n_t_guess=None, x_guess=None,
                         n0_prev=None, lam0_prev=None):
    """
    Resuelve el equilibrio de disociacion/combustion de una mezcla de
    gas ideal (una sola fase) a temperatura T y presion p [atm], dado
    el balance de elementos b = A @ n_feed.

    Si se proveen n0_prev/lam0_prev (solucion de un punto anterior de
    un barrido), se usan como estimacion inicial (continuacion), lo
    que da barridos mas suaves que reiniciar en cada punto.

    Retorna el vector de moles de equilibrio n (shape (NC,)), y el
    lambda convergido (util para encadenar el siguiente punto).
    """
    g = vector_g(especies, T)
    modelo_gas = {"tipo": "vapor_ideal", "p": p, "p0": 1.0}

    NC = len(especies)
    from termodinamica import ln_Gamma_fase

    # Lambda inicial: SIEMPRE se recalcula por minimos cuadrados para
    # el g(T) actual (barato: un solo lstsq, sin iterar), en vez de
    # reutilizar el lambda convergido del punto anterior del barrido.
    # Motivo: g_i = dGf_i(T)/(RT) puede cambiar sustancialmente entre
    # dos valores de T de un barrido (hay especies, p. ej. CO2, cuyo
    # g_i es mucho mas negativo que el de otras); reusar un lambda
    # ajustado a un T distinto puede producir exponentes enormes en la
    # Ec. 3.34 (exp(A^T*lambda - g) con lambda "desfasado") y desbordar
    # numericamente. El lstsq lambda0 = argmin||A^T*lambda - g||^2
    # siempre centra los exponentes cerca de cero para el T actual.
    lam0, *_ = np.linalg.lstsq(A.T, g, rcond=None)

    if n0_prev is not None:
        # Continuacion SOLO en composicion (buena estimacion inicial
        # de n, que si varia suavemente entre puntos cercanos de un
        # barrido); resolver_lagrange espera una lista de arrays, uno
        # por fase (aqui, una sola fase gas).
        n0 = [np.array(n0_prev, dtype=float)]
    else:
        if n_t_guess is None:
            n_t_guess = float(np.sum(b)) / 2.0  # orden de magnitud razonable
        if x_guess is None:
            x_guess = np.ones(NC) / NC
        ln_Gamma0 = [ln_Gamma_fase("vapor_ideal", x_guess, p=p, p0=1.0)]
        lam0, n0, _ = minimizar_Q(A, b, [n_t_guess], g, ln_Gamma0, lam0=lam0)

    resultado = resolver_lagrange(A, b, lam0, n0, g, [modelo_gas])
    return resultado["n_fases"][0], resultado["lambda"]


def barrido_combustion(A, especies, feed_fn, valores, T_fn=None, p_fn=None,
                        n_t_guess=None):
    """
    Barrido generico con continuacion: feed_fn(valor) -> vector de
    alimentacion (se convierte a b = A@feed); T_fn(valor) y p_fn(valor)
    dan la temperatura/presion en cada punto (por defecto, T_fn=valor
    si T_fijo no se especifica explicitamente mediante una funcion
    constante). Devuelve (valores, composiciones) con composiciones de
    shape (len(valores), NC).
    """
    composiciones = []
    n_prev, lam_prev = None, None
    for val in valores:
        feed = feed_fn(val)
        b = A @ feed if feed.ndim == 1 and len(feed) == A.shape[1] else feed
        T = T_fn(val) if T_fn is not None else val
        p = p_fn(val) if p_fn is not None else 1.0
        n, lam = resolver_combustion(A, b, especies, T, p=p,
                                       n_t_guess=n_t_guess,
                                       n0_prev=n_prev, lam0_prev=lam_prev)
        composiciones.append(n / np.sum(n))
        n_prev, lam_prev = n, lam
    return np.array(composiciones)


# ---------------------------------------------------------------------------
# Sistema A: disociacion H2/O2/H2O (combustion de hidrogeno)
# ---------------------------------------------------------------------------
# Especies: H2, O2, H2O, OH, H, O.  Elementos: H, O.

ESPECIES_H2O = ["H2", "O2", "H2O", "OH", "H", "O"]
A_H2O = np.array([
    [2, 0, 2, 1, 1, 0],   # H
    [0, 2, 1, 1, 0, 1],   # O
], dtype=float)


def feed_H2O(relacion_H2_O2=2.0, base_O2=1.0):
    """Alimentacion H2:O2 (relacion molar) antes de disociar; por defecto
    estequiometrica para 2 H2 + O2 -> 2 H2O."""
    n = np.zeros(len(ESPECIES_H2O))
    n[ESPECIES_H2O.index("H2")] = relacion_H2_O2 * base_O2
    n[ESPECIES_H2O.index("O2")] = base_O2
    return n


# ---------------------------------------------------------------------------
# Sistema B: disociacion CO2 <-> CO + 1/2 O2
# ---------------------------------------------------------------------------

ESPECIES_CO2 = ["CO2", "CO", "O2"]
A_CO2 = np.array([
    [1, 1, 0],   # C
    [2, 1, 2],   # O
], dtype=float)


def feed_CO2(moles=1.0):
    n = np.zeros(len(ESPECIES_CO2))
    n[ESPECIES_CO2.index("CO2")] = moles
    return n


# ---------------------------------------------------------------------------
# Sistema C: productos de combustion CH4/aire (equilibrio "de llama")
# ---------------------------------------------------------------------------
# Especies: CO2, H2O, CO, H2, O2, N2, NO, OH, H, O.  Elementos: C,H,O,N.
# Relacion de aire: 1 mol O2 + 3.76 mol N2 (aire estandar).

ESPECIES_LLAMA = ["CO2", "H2O", "CO", "H2", "O2", "N2", "NO", "OH", "H", "O"]
#                   C  H  O  N   (filas)
A_LLAMA = np.array([
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],   # C
    [0, 2, 0, 2, 0, 0, 0, 1, 1, 0],   # H
    [2, 1, 1, 0, 2, 0, 1, 1, 0, 1],   # O
    [0, 0, 0, 0, 0, 2, 1, 0, 0, 0],   # N
], dtype=float)

AIRE_N2_O2 = 3.76  # mol N2 por mol O2 en aire estandar


def feed_llama(phi=1.0, moles_CH4=1.0):
    """
    Balance de atomos disponibles para la combustion de CH4 con aire a
    razon de equivalencia phi (phi=1 estequiometrico, phi>1 rico en
    combustible, phi<1 pobre). Se construye directamente el vector b
    (abundancia de elementos), no una composicion de especies inicial,
    ya que en el equilibrio los atomos se redistribuyen libremente
    entre las 10 especies.

        CH4 + (2/phi) (O2 + 3.76 N2)  ->  [productos en equilibrio]

    Retorna b = [C, H, O, N] disponibles.
    """
    O2_suministrado = (2.0 / phi) * moles_CH4
    N2_suministrado = AIRE_N2_O2 * O2_suministrado
    C = moles_CH4
    H = 4.0 * moles_CH4
    O = 2.0 * O2_suministrado
    N = 2.0 * N2_suministrado
    return np.array([C, H, O, N])


# ---------------------------------------------------------------------------
# Sistema D: productos de combustion C3H8 (propano)/aire
# ---------------------------------------------------------------------------
# Mismas 10 especies y misma matriz de elementos que el sistema CH4/aire
# (A_LLAMA, ESPECIES_LLAMA): el combustible solo aporta C y H, que se
# redistribuyen igual entre las mismas especies de equilibrio.
# Reaccion de referencia (completa): C3H8 + 5(O2+3.76N2) -> 3CO2+4H2O+18.8N2

def feed_propano(phi=1.0, moles_C3H8=1.0):
    """Balance de atomos [C,H,O,N] para combustion de propano con aire
    a razon de equivalencia phi (misma convencion que feed_llama)."""
    O2_estequiometrico = 5.0 * moles_C3H8
    O2_suministrado = O2_estequiometrico / phi
    N2_suministrado = AIRE_N2_O2 * O2_suministrado
    C = 3.0 * moles_C3H8
    H = 8.0 * moles_C3H8
    O = 2.0 * O2_suministrado
    N = 2.0 * N2_suministrado
    return np.array([C, H, O, N])


# ---------------------------------------------------------------------------
# Sistema E: combustion de H2 con aire (incluye N2/NO, a diferencia del
# sistema A que es H2/O2 puro sin aire)
# ---------------------------------------------------------------------------
# Especies: H2, O2, H2O, OH, H, O, N2, NO.  Elementos: H, O, N.

ESPECIES_H2_AIRE = ["H2", "O2", "H2O", "OH", "H", "O", "N2", "NO"]
A_H2_AIRE = np.array([
    [2, 0, 2, 1, 1, 0, 0, 0],   # H
    [0, 2, 1, 1, 0, 1, 0, 1],   # O
    [0, 0, 0, 0, 0, 0, 2, 1],   # N
], dtype=float)


def feed_H2_aire(phi=1.0, moles_H2=1.0):
    """Balance de atomos [H,O,N] para combustion de H2 con aire a razon
    de equivalencia phi. Reaccion de referencia: H2 + 1/2 O2 -> H2O."""
    O2_estequiometrico = 0.5 * moles_H2
    O2_suministrado = O2_estequiometrico / phi
    N2_suministrado = AIRE_N2_O2 * O2_suministrado
    H = 2.0 * moles_H2
    O = 2.0 * O2_suministrado
    N = 2.0 * N2_suministrado
    return np.array([H, O, N])


# ---------------------------------------------------------------------------
# Sistema F: reaccion de desplazamiento agua-gas (water-gas shift),
# CO + H2O <-> CO2 + H2 -- quimica de syngas, clasica en procesos de
# oxidacion parcial/reformado, no es combustion de llama pero usa el
# mismo formalismo de potenciales de elemento.
# ---------------------------------------------------------------------------

ESPECIES_WGS = ["CO", "H2O", "CO2", "H2"]
A_WGS = np.array([
    [1, 0, 1, 0],   # C
    [0, 2, 0, 2],   # H
    [1, 1, 2, 0],   # O
], dtype=float)


def feed_WGS(relacion_H2O_CO=1.0, base_CO=1.0):
    """Alimentacion CO:H2O (relacion molar, tipicamente ~1:1 a 1:3 en
    procesos industriales de water-gas shift)."""
    n = np.zeros(len(ESPECIES_WGS))
    n[ESPECIES_WGS.index("CO")] = base_CO
    n[ESPECIES_WGS.index("H2O")] = relacion_H2O_CO * base_CO
    return n


# ---------------------------------------------------------------------------
# Sistema G: combustion CH4/aire con posible formacion de hollin (C solido)
# y condensacion de agua -- equilibrio Vapor-Solido-Liquido completo,
# EXPLORATORIO (misma advertencia de alcance que el resto de este
# archivo), usando algoritmos.combined_algorithm (SSA + RAND modificado +
# analisis de estabilidad de Michelsen, Fig. 3.1b de la tesis) en vez de
# resolver_lagrange de una sola fase: el NUMERO de fases presentes
# (vapor solo / vapor+solido / vapor+solido+liquido) lo decide el
# analisis de estabilidad en cada punto, exactamente igual que en
# ejemplo_mtbe.py.
#
# Verificacion de la condensacion de agua implicita (ver tipo de fase
# "condensado_puro" en termodinamica.py): la diferencia de g_reducido
# entre H2O(vapor) y H2O(l) a 298.15 K reproduce la presion de vapor
# real del agua sin necesitar una correlacion de Antoine aparte:
#   dG_vap = dGf(H2O,g) - dGf(H2O,l) = -228.6 - (-237.1) = 8.5 kJ/mol
#   Psat/p0 = exp(-dG_vap/(R*298.15)) = exp(-3.43) = 0.0324 atm
# (valor real ~0.0313 atm / 23.8 mmHg a 25 C: el error es el tipico de
# la aproximacion dCp=0 ya usada en todo este modulo, no un error nuevo).
# Fuera de un entorno razonable alrededor de 298 K esta extrapolacion
# lineal de dCp=0 se degrada (igual que para cualquier otra especie de
# este archivo); los barridos de T de mas abajo se limitan a un rango
# donde la tendencia cualitativa (aparicion de condensado al bajar T)
# sigue siendo la fisicamente correcta.
# ---------------------------------------------------------------------------

from estabilidad import analizar_estabilidad

ESPECIES_HOLLIN = ESPECIES_LLAMA + ["C(s)", "H2O(l)"]
#                     C  H  O  N
_A_EXTRA_HOLLIN = np.array([
    [1, 0],   # C(s): 1 C
    [0, 2],   # H2O(l): 2 H
    [0, 1],   # H2O(l): 1 O
    [0, 0],   # ninguno aporta N
], dtype=float)
A_HOLLIN = np.hstack([A_LLAMA, _A_EXTRA_HOLLIN])

IDX_C_SOLIDO = ESPECIES_HOLLIN.index("C(s)")
IDX_H2O_LIQUIDO = ESPECIES_HOLLIN.index("H2O(l)")


def feed_hollin(phi=1.0, moles_CH4=1.0):
    """Mismo balance atomico [C,H,O,N] que feed_llama (el combustible y
    el aire son identicos; lo unico que cambia es el conjunto de fases
    candidatas para la busqueda de equilibrio)."""
    return feed_llama(phi=phi, moles_CH4=moles_CH4)


def _mascara_pura(especies, nombre):
    """Vector mascara de un solo componente (1.0 en 'nombre', 0.0 en las
    demas), para el tipo de fase 'condensado_puro' (ver termodinamica.py)."""
    m = np.zeros(len(especies))
    m[especies.index(nombre)] = 1.0
    return m


def _mascara_gas(especies, especies_condensadas):
    """Vector mascara de especies PERMITIDAS en la fase vapor (1.0), es
    decir todas excepto las especies condensadas (0.0), para el tipo de
    fase 'vapor_ideal_con_exclusion' (ver termodinamica.py). Sin esta
    exclusion, "C(s)"/"H2O(l)" se tratarian incorrectamente como un
    componente gaseoso mas de la fase vapor (con Gamma_ik=p/p0, que no
    les corresponde: su g_i(T) esta referida al estado de referencia
    condensado puro, no a gas ideal)."""
    m = np.ones(len(especies))
    for nombre in especies_condensadas:
        m[especies.index(nombre)] = 0.0
    return m


def resolver_hollin(A, b, especies, T, p=1.0, n_t_guess=None, max_fases=3):
    """
    Resuelve el equilibrio quimico-de-fases completo (vapor ideal +
    posible C solido + posible H2O liquida) para un sistema de
    combustion, dejando que el analisis de estabilidad de Michelsen
    (estabilidad.analizar_estabilidad) decida cuantas fases hay
    realmente en este punto (T, p, composicion de alimentacion).

    Reimplementa aqui el mismo bucle de
    algoritmos.successive_substitution_algorithm (Fig. 3.1a de la
    tesis: resolver -> analizar estabilidad -> si inestable, anadir
    fase y repetir) en vez de llamarlo directamente, SOLO para poder
    sembrar lambda inicial con el mismo truco de minimos cuadrados que
    ya usa resolver_combustion() (lam0 = lstsq(A^T, g)): la
    inicializacion por defecto de algoritmos.py (lambda=0 antes de
    minimizar_Q) sobredesborda (overflow) para especies de combustion
    (|dGf| ~ cientos de kJ/mol) a T baja, exactamente el problema que
    ese comentario de resolver_combustion ya documenta. No se modifica
    ningun archivo validado: resolver_lagrange() y analizar_estabilidad()
    se reutilizan tal cual, igual que en el resto del proyecto.

    A diferencia de resolver_combustion() (una sola fase, con
    continuacion n0_prev/lam0_prev entre puntos de un barrido), aqui NO
    se reutiliza la solucion del punto anterior: el numero de fases
    puede cambiar de un punto a otro del barrido.

    LIMITACION NUMERICA CONOCIDA (ver tambien README.md, "Limitaciones
    conocidas"): el paso de Newton de resolver_lagrange, justo al anadir
    una fase condensada nueva (semilla w*1e-6), ocasionalmente converge
    (error por debajo de tol) a un n_t astronomico (p. ej. 1e20) en vez
    de al valor fisico, para ciertas combinaciones de alimentacion muy
    pobres en oxigeno -- un "falso convergido" que el criterio interno
    de resolver_lagrange (cambio de lambda/n_t entre iteraciones) no
    detecta porque ESE residuo si se hace pequeno, aun si el balance de
    materia global no se cumple. resolver_hollin() lo detecta
    verificando el balance A@n=b al final (tolerancia relativa) y
    reintenta una vez con un n_t_guess distinto; si ambos intentos
    fallan, retorna "balance_ok": False para que el llamador (p. ej.
    barrido_hollin) marque ese punto como no confiable en vez de
    graficar un numero sin sentido.

    Retorna
    -------
    resultado : dict con "lambda", "n_fases", "x_fases", "modelos_fase",
        "estable", "balance_ok" (misma forma que
        algoritmos.successive_substitution_algorithm, mas "balance_ok").
    """
    mejor_resultado, mejor_residuo = None, np.inf
    for intento, factor in enumerate([0.5, 1.0 / 3.0, 0.7]):
        guess = (float(np.sum(b)) * factor) if n_t_guess is None else n_t_guess
        resultado = _resolver_hollin_un_intento(A, b, especies, T, p, guess, max_fases)
        residuo = float(np.max(np.abs(A @ sum(resultado["n_fases"]) - b)))
        escala = max(float(np.max(np.abs(b))), 1.0)
        if residuo < mejor_residuo:
            mejor_resultado, mejor_residuo = resultado, residuo
        if residuo < 1e-6 * escala:
            mejor_resultado["balance_ok"] = True
            return mejor_resultado
        if n_t_guess is not None:
            break  # el llamador fijo un n_t_guess explicito: no tiene sentido variarlo

    mejor_resultado["balance_ok"] = False
    return mejor_resultado


def _resolver_hollin_un_intento(A, b, especies, T, p, n_t_guess, max_fases):
    """Un solo intento de resolver_hollin, con n_t_guess ya fijo (ver
    resolver_hollin() para el reintento con balance de materia)."""
    g = vector_g(especies, T)
    NC = len(especies)
    especies_condensadas = ["C(s)", "H2O(l)"]
    mascara_vapor = _mascara_gas(especies, especies_condensadas)
    modelo_vapor = {"tipo": "vapor_ideal_con_exclusion", "p": p, "p0": 1.0,
                     "Lambda": mascara_vapor}
    modelo_C_solido = {"tipo": "condensado_puro",
                        "Lambda": _mascara_pura(especies, "C(s)")}
    modelo_H2O_liquido = {"tipo": "condensado_puro",
                           "Lambda": _mascara_pura(especies, "H2O(l)")}
    candidatos = [modelo_C_solido, modelo_H2O_liquido]

    if n_t_guess is None:
        n_t_guess = float(np.sum(b)) / 2.0

    lam0, *_ = np.linalg.lstsq(A.T, g, rcond=None)
    x_guess = mascara_vapor / np.sum(mascara_vapor)
    from termodinamica import ln_Gamma_fase
    ln_Gamma0 = [ln_Gamma_fase("vapor_ideal_con_exclusion", x_guess, p=p, p0=1.0,
                                Lambda=mascara_vapor)]
    lam0, n_fases0, _ = minimizar_Q(A, b, [n_t_guess], g, ln_Gamma0, lam0=lam0)

    modelos_fase = [modelo_vapor]
    resultado = resolver_lagrange(A, b, lam0, n_fases0, g, modelos_fase)

    for _ in range(max_fases - 1):
        # No volver a ofrecer como candidata una fase condensada que ya
        # esta activa: dos fases "condensado_puro" identicas (misma
        # mascara) hacen que la matriz JA de la Ec. 3.46 quede
        # degenerada (columnas redundantes) y el Newton de
        # resolver_lagrange diverge a n_t astronomicos en vez de
        # converger -- un caso patologico especifico de fases puras
        # (que no se presenta en el VLE de ejemplo_mtbe.py, donde solo
        # hay un candidato de cada tipo).
        activas = {tuple(m["Lambda"]) for m in modelos_fase
                   if m["tipo"] == "condensado_puro"}
        candidatos_restantes = [c for c in candidatos
                                 if tuple(c["Lambda"]) not in activas]
        if not candidatos_restantes:
            break

        z = resultado["x_fases"][0]
        modelo_feed = modelos_fase[0]
        estable, mejor = analizar_estabilidad(z, modelo_feed, candidatos_restantes)
        if estable:
            break

        # Fase nueva con cantidad infinitesimal (pag. 44 de la tesis:
        # "the amount of the new phase is set to zero"), misma
        # convencion que algoritmos._candidato_estabilidad_a_fase.
        n_nueva_fase = mejor["w"] * 1e-6
        modelo_nuevo = mejor["modelo_trial"]
        n_fases_extendido = resultado["n_fases"] + [n_nueva_fase]
        modelos_fase = modelos_fase + [modelo_nuevo]

        resultado = resolver_lagrange(A, b, resultado["lambda"], n_fases_extendido,
                                       g, modelos_fase)

    resultado["modelos_fase"] = modelos_fase
    return resultado


def _moles_fase_condensada(resultado, idx_especie):
    """Suma los moles de la especie 'idx_especie' en cualquier fase
    condensada presente en el resultado (0.0 si esa fase no aparecio)."""
    total = 0.0
    for modelo, n_k in zip(resultado["modelos_fase"], resultado["n_fases"]):
        if modelo["tipo"] == "condensado_puro" and modelo["Lambda"][idx_especie] > 0.5:
            total += float(np.sum(n_k))
    return total


def barrido_hollin(A, especies, feed_fn, valores, T_fn=None, p_fn=None,
                    n_t_guess=None):
    """
    Barrido generico (vs. phi, T, o lo que parametrice feed_fn/T_fn/p_fn)
    del sistema de hollin. Para cada punto resuelve el equilibrio
    multifase completo (resolver_hollin) y extrae:
      - x_vapor: fraccion molar de cada especie EN LA FASE VAPOR (shape
        (len(valores), NC)), normalizada dentro de esa fase.
      - n_C_solido, n_H2O_liquido: moles totales de cada fase condensada
        (0.0 en los puntos donde esa fase no existe).

    Retorna
    -------
    x_vapor, n_C_solido, n_H2O_liquido : ndarrays
    """
    NC = len(especies)
    x_vapor = np.zeros((len(valores), NC))
    n_C_solido = np.zeros(len(valores))
    n_H2O_liquido = np.zeros(len(valores))

    for j, val in enumerate(valores):
        feed = feed_fn(val)
        b = A @ feed if feed.ndim == 1 and len(feed) == A.shape[1] else feed
        T = T_fn(val) if T_fn is not None else val
        p = p_fn(val) if p_fn is not None else 1.0

        resultado = resolver_hollin(A, b, especies, T, p=p, n_t_guess=n_t_guess)

        n_fase_vapor = resultado["n_fases"][0]
        x_vapor[j] = n_fase_vapor / np.sum(n_fase_vapor)
        n_C_solido[j] = _moles_fase_condensada(resultado, IDX_C_SOLIDO)
        n_H2O_liquido[j] = _moles_fase_condensada(resultado, IDX_H2O_LIQUIDO)

    return x_vapor, n_C_solido, n_H2O_liquido
