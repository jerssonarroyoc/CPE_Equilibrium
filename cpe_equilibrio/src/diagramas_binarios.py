"""
diagramas_binarios.py
=======================

Diagramas clasicos de equilibrio de fases para sistemas BINARIOS NO
reactivos: T-x-y, P-x-y, x-y (VLE) y el domo de equilibrio liquido-
liquido (LLE, diagrama T vs x).

IMPORTANTE (alcance de este modulo, a pedido explicito del usuario):
estas graficas son EXPLORATORIAS -- "quiero ver que arroja el modelo",
sin requisito de validacion cuantitativa contra datos experimentales.
Se reusan los modelos termodinamicos YA VALIDADOS (UNIFAC con grupos
oficiales DDBST, Antoine de Smith & Van Ness) en termodinamica.py y
ejemplo_acetic_etanol.py, pero las rutinas de calculo de este archivo
(bubble-point, dew-point, binodal LLE) son nuevas y no pasan por la
suite de pruebas_validacion.py.

No se usa el aparato completo de minimizacion de Gibbs no-estequio-
metrica (Lagrange/RAND) para estos binarios NO reactivos -- seria
innecesario, ya que sin reaccion el problema se reduce al calculo
estandar de punto de burbuja/rocio (isofugacidad componente a
componente). El aparato de Gibbs si se usa en diagramas_reactivos.py
y combustion_gibbs.py, donde hay reaccion quimica de por medio.
"""

import numpy as np
from scipy.optimize import brentq

from termodinamica import gamma_unifac, gamma_regular_binaria
from ejemplo_acetic_etanol import psat_SVN_kPa


# ---------------------------------------------------------------------------
# Sistema 1: etanol(1) - agua(2), UNIFAC (grupos oficiales DDBST)
# ---------------------------------------------------------------------------

ETANOL_AGUA_CHEMGROUPS = [
    {1: 1, 2: 1, 14: 1},  # etanol: CH3 + CH2 + OH
    {16: 1},              # agua: H2O
]


def psat_etanol(T_K):
    """Antoine de Smith & Van Ness Tabla B.2 (ya validado)."""
    return psat_SVN_kPa(T_K, 16.8958, 3795.17, 230.918) / 101.325  # atm


def psat_agua(T_K):
    return psat_SVN_kPa(T_K, 16.3872, 3885.70, 230.170) / 101.325  # atm


def gammas_etanol_agua(x1, T_K):
    """Coeficientes de actividad UNIFAC para [etanol, agua] a x1, T."""
    x = np.array([x1, 1.0 - x1])
    return gamma_unifac(x, T_K, ETANOL_AGUA_CHEMGROUPS)


def bubble_T_etanol_agua(x1, p_atm, T_guess=350.0):
    """
    Temperatura de burbuja a composicion liquida x1 y presion p_atm:
    resuelve sum_i(x_i * gamma_i * Psat_i(T)) = p.
    """
    def residual(T):
        g1, g2 = gammas_etanol_agua(x1, T)
        return x1 * g1 * psat_etanol(T) + (1 - x1) * g2 * psat_agua(T) - p_atm
    return brentq(residual, 280.0, 420.0, xtol=1e-6)


def y_desde_bubble(x1, T_K, p_atm):
    """Composicion de vapor en el punto de burbuja (y_i = x_i*gamma_i*Psat_i/p)."""
    g1, g2 = gammas_etanol_agua(x1, T_K)
    y1 = x1 * g1 * psat_etanol(T_K) / p_atm
    return y1


def bubble_P_etanol_agua(x1, T_K):
    """Presion de burbuja a composicion liquida x1 y temperatura T_K."""
    g1, g2 = gammas_etanol_agua(x1, T_K)
    return x1 * g1 * psat_etanol(T_K) + (1 - x1) * g2 * psat_agua(T_K)


# ---------------------------------------------------------------------------
# Sistema 2: binario LLE con solucion regular dependiente de T
# ---------------------------------------------------------------------------
#
# Modelo de solucion regular con parametro de interaccion inversamente
# proporcional a T (forma estandar de una solucion regular real:
# Lambda(T) = Omega / (R T), con Omega una energia de intercambio
# constante). Esto da una temperatura critica superior de solucion
# (UCST) exacta: T_c = Omega / (2R). Se elige Omega = 6000 J/mol de
# forma ILUSTRATIVA (no ajustada a ningun sistema real), dando
# T_c ~ 361 K, un domo de LLE comodo de visualizar.
# ---------------------------------------------------------------------------

OMEGA_LLE = 6000.0  # J/mol, ilustrativo
R_GAS = 8.314


def lambda_regular(T_K):
    return OMEGA_LLE / (R_GAS * T_K)


def T_critica_LLE():
    return OMEGA_LLE / (2 * R_GAS)


def binodal_LLE(T_K):
    """
    Composiciones x', x'' de las dos fases liquidas en equilibrio a T_K,
    para la solucion regular simetrica (resolviendo gamma1*x1 = gamma1'*x1'
    y gamma2*x2 = gamma2'*x2' simultaneamente). Para una solucion regular
    SIMETRICA (ln g1 = Lambda*x2^2, ln g2 = Lambda*x1^2), la solucion es
    simetrica respecto a x=0.5: basta resolver x*exp(Lambda*(1-x)^2) =
    (1-x)*exp(Lambda*x^2).

    Retorna (x_pobre, x_rica) o None si T >= T_critica (una sola fase).
    """
    Lam = lambda_regular(T_K)
    if T_K >= T_critica_LLE():
        return None

    def residual(x1):
        # igualdad de actividad del componente 1 en las dos fases,
        # con x1' = x1 (fase pobre) y x1'' = 1 - x1 (fase rica, por simetria)
        return (x1 * np.exp(Lam * (1 - x1) ** 2)
                - (1 - x1) * np.exp(Lam * x1 ** 2))

    x_pobre = brentq(residual, 1e-6, 0.5 - 1e-6, xtol=1e-8)
    return x_pobre, 1 - x_pobre
