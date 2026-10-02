"""
diagramas_reactivos.py
========================

Diagramas de equilibrio quimico Y de fases simultaneos (CPE), usando
los solvers YA VALIDADOS (resolver_lagrange, resolver_rand_modificado)
para los dos sistemas reactivos del proyecto: sintesis de MTBE
(ejemplo_mtbe.py) y esterificacion acido acetico/etanol
(ejemplo_acetic_etanol.py).

IMPORTANTE: graficas EXPLORATORIAS ("quiero ver que arroja el
modelo"), sin requisito de validacion cuantitativa -- a diferencia de
pruebas_validacion.py y generar_figuras.py, que sí validan. No se
modifica ningun archivo ya validado.
"""

import numpy as np

import ejemplo_mtbe as mtbe
import ejemplo_acetic_etanol as ace
from inicializacion import minimizar_Q
from lagrange_multipliers import resolver_lagrange
from termodinamica import ln_Gamma_fase


# ---------------------------------------------------------------------------
# Proyeccion ternaria (triangulo equilatero) para graficar composiciones
# de 3 componentes (a, b, c) con a+b+c=1.
# ---------------------------------------------------------------------------

def proyeccion_ternaria(a, b, c):
    """Convierte fracciones (a,b,c) a coordenadas cartesianas (x,y) en un
    triangulo equilatero con vertices en (0,0)=a puro, (1,0)=b puro,
    (0.5, sqrt(3)/2)=c puro."""
    x = b + 0.5 * c
    y = (np.sqrt(3) / 2) * c
    return x, y


# ---------------------------------------------------------------------------
# MTBE: resolucion directa de 2 fases (liquido + vapor) a (T, p) dados
# ---------------------------------------------------------------------------

def resolver_mtbe_2fases(T, p, modelo_liquido=None, n_fases_prev=None):
    """
    Resuelve el equilibrio liquido-vapor con reaccion del sistema MTBE
    a temperatura T [K] y presion p [bar], fijando de antemano 2 fases
    (evita el analisis de estabilidad, igual que en generar_figuras.py).

    Si se provee n_fases_prev (solucion del punto anterior de un
    barrido), se usa como estimacion inicial directamente (metodo de
    continuacion), en vez de reiniciar desde una composicion generica
    en cada punto. Esto mejora notablemente la suavidad de los barridos
    cerca de la ventana de transicion liquido-vapor.
    """
    if modelo_liquido is None:
        Psat_T = np.array([mtbe.psat_clausius_clapeyron(T, c) for c in mtbe.COMPONENTES])
        modelo_liquido = {"tipo": "liquido_ideal", "Psat": Psat_T, "p0": mtbe.P0}
    modelo_vapor = {"tipo": "vapor_ideal", "p": p, "p0": mtbe.P0}
    modelos = [modelo_liquido, modelo_vapor]

    if n_fases_prev is not None:
        n_fases0 = [np.array(n_fases_prev[0], dtype=float),
                    np.array(n_fases_prev[1], dtype=float)]
        lam0 = np.zeros(mtbe.A.shape[0])
        # Un primer Newton con lambda=0 solo para obtener un lambda
        # razonable antes del solve completo (barato, 1 iteracion basta
        # como "calentamiento" porque n_fases0 ya es una buena estimacion).
        x_prom = (n_fases0[0] / np.sum(n_fases0[0]) + n_fases0[1] / np.sum(n_fases0[1])) / 2
        ln_Gamma0 = [
            ln_Gamma_fase(modelo_liquido["tipo"], x_prom, Psat=modelo_liquido["Psat"], p0=mtbe.P0),
            ln_Gamma_fase(modelo_vapor["tipo"], x_prom, p=p, p0=mtbe.P0),
        ]
        lam0, _, _ = minimizar_Q(mtbe.A, mtbe.b,
                                   [np.sum(n_fases0[0]), np.sum(n_fases0[1])],
                                   mtbe.g, ln_Gamma0, lam0=lam0)
    else:
        n_t_liq0, n_t_vap0 = 0.9 * np.sum(mtbe.n_feed), 0.1 * np.sum(mtbe.n_feed)
        x0_trial = np.array([0.3, 0.3, 0.4])
        ln_Gamma0 = [
            ln_Gamma_fase(modelo_liquido["tipo"], x0_trial,
                           Psat=modelo_liquido["Psat"], p0=mtbe.P0),
            ln_Gamma_fase(modelo_vapor["tipo"], x0_trial, p=p, p0=mtbe.P0),
        ]
        lam0, n_fases0, _ = minimizar_Q(mtbe.A, mtbe.b, [n_t_liq0, n_t_vap0], mtbe.g, ln_Gamma0)

    resultado = resolver_lagrange(mtbe.A, mtbe.b, lam0, n_fases0, mtbe.g, modelos)
    return resultado["n_fases"][0], resultado["n_fases"][1]


def barrido_T_mtbe(p_bar, T_min, T_max, n_puntos=25):
    """
    Barrido de temperatura a presion fija (metodo de continuacion: cada
    punto usa la solucion del anterior como estimacion inicial, lo que
    produce curvas mucho mas suaves cerca de la transicion liquido-vapor
    que reiniciar desde cero en cada T). Si una fase colapsa (sistema
    subenfriado o sobrecalentado), se reporta su fraccion como ~0.
    """
    temperaturas = np.linspace(T_min, T_max, n_puntos)
    x_liq, x_vap, frac_vap = [], [], []
    n_fases_prev = None
    for T in temperaturas:
        n_liq, n_vap = resolver_mtbe_2fases(T, p_bar, n_fases_prev=n_fases_prev)
        nt_liq, nt_vap = np.sum(n_liq), np.sum(n_vap)
        x_liq.append(n_liq / nt_liq)
        x_vap.append(n_vap / nt_vap)
        frac_vap.append(nt_vap / (nt_liq + nt_vap))
        n_fases_prev = (n_liq, n_vap)
    return temperaturas, np.array(x_liq), np.array(x_vap), np.array(frac_vap)


def barrido_p_mtbe(T_K, p_min, p_max, n_puntos=25):
    """Barrido de presion a temperatura fija (con continuacion, ver
    barrido_T_mtbe)."""
    presiones = np.linspace(p_min, p_max, n_puntos)
    x_liq, x_vap, frac_vap = [], [], []
    n_fases_prev = None
    for p in presiones:
        n_liq, n_vap = resolver_mtbe_2fases(T_K, p, n_fases_prev=n_fases_prev)
        nt_liq, nt_vap = np.sum(n_liq), np.sum(n_vap)
        x_liq.append(n_liq / nt_liq)
        x_vap.append(n_vap / nt_vap)
        frac_vap.append(nt_vap / (nt_liq + nt_vap))
        n_fases_prev = (n_liq, n_vap)
    return presiones, np.array(x_liq), np.array(x_vap), np.array(frac_vap)


# ---------------------------------------------------------------------------
# Esterificacion: barrido de T a p fija con UNIFAC (fase liquida unica o
# VLE segun si el sistema esta sub- o sobre-enfriado -- ver nota en
# ejemplo_acetic_etanol.py)
# ---------------------------------------------------------------------------

def barrido_T_esterificacion_VLE(p_atm, T_min, T_max, n_puntos=20):
    """
    Barrido de T a p fija, VLE completo (liquido UNIFAC + vapor ideal)
    para la esterificacion acido acetico/etanol, alimentacion equimolar.
    Si el vapor colapsa (subenfriado), fraccion de vapor ~0.
    """
    feed = np.array([0.5, 0.5, 0.0, 0.0])
    temperaturas = np.linspace(T_min, T_max, n_puntos)
    x_liq, x_vap, frac_vap = [], [], []
    n_liq0, n_vap0 = np.array([0.05, 0.05, 0.10, 0.10]), np.array([0.10, 0.10, 0.25, 0.25])
    lam0_prev = None
    for T in temperaturas:
        g = np.array([0.0, 0.0, 0.0, -np.log(ace.K_eq(T))])
        Psat = ace.Psat_todos(T)
        modelo_liq = {"tipo": "liquido_unifac", "Psat": Psat, "p0": 1.0,
                      "T": T, "chemgroups": ace.CHEMGROUPS}
        r_lag, _, _ = ace.resolver_vle(modelo_liq, feed, T, g, Psat,
                                        n_liq0=n_liq0, n_vap0=n_vap0,
                                        lam0_prev=lam0_prev)
        n_liq, n_vap = r_lag["n_fases"]
        lam0_prev = r_lag["lambda"]
        nt_liq, nt_vap = np.sum(n_liq), np.sum(n_vap)
        x_liq.append(n_liq / nt_liq)
        x_vap.append(n_vap / nt_vap)
        frac_vap.append(nt_vap / (nt_liq + nt_vap))
        # usamos la solucion actual como estimacion inicial del siguiente
        # punto del barrido (continuacion), mas robusto que reiniciar
        n_liq0, n_vap0 = n_liq, n_vap
    return temperaturas, np.array(x_liq), np.array(x_vap), np.array(frac_vap)
