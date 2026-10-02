"""
ejemplo_acetic_etanol.py
==========================

Caso de prueba: esterificacion de acido acetico + etanol -> acetato de
etilo + agua (seccion 4.1.3 de la tesis de Tsanas, Tabla 4.4):

    CH3COOH(l) + C2H5OH(l)  <->  CH3COOC2H5(l) + H2O(l)

Dos escenarios, ambos con datos COMPLETAMENTE trazables (ningun valor
ilustrativo):

  1. Fase liquida unica a 373.15 K (100 C), replicando EXACTAMENTE el
     Example 14.8 de Smith, Van Ness & Abbott, "Introduction to Chemical
     Engineering Thermodynamics", 8th ed. -- sin VLE, tal como lo
     plantea el libro.
  2. VLE completo a 355 K, 1 atm, alimentacion equimolar 0.5/0.5 (igual
     que la Tabla 4.4 de la tesis), con los 4 componentes en equilibrio
     liquido-vapor.

En ambos casos se resuelve con el modelo de solucion IDEAL (gamma_i=1,
la propia simplificacion del libro) y con UNIFAC (predictivo, grupos
oficiales DDBST via `thermo`).

=====================================================================
FUENTES DE DATOS (todas citadas; ver tambien docs/referencias.bib)
=====================================================================

K_eq(T): Smith, Van Ness & Abbott, Example 14.8. K(298.15 K) = 6.5266
y dH_rxn(298.15 K) = -3640 J/mol, obtenidos de las entalpias y energias
de Gibbs de formacion de los 4 compuestos (Tabla C.4 del libro + los
valores de acetato de etilo dados en el enunciado del ejemplo). K(T) se
extrapola con la ecuacion de van't Hoff (dH_rxn constante), tal como lo
hace el propio libro para obtener K(373.15 K)=4.8586. Para 355 K
calculamos K(355 K)=5.1589 con la MISMA ecuacion y los MISMOS datos.

Antoine:
  - Acido acetico, etanol, agua: Smith & Van Ness, Tabla B.2.
    Forma: ln(Psat[kPa]) = A - B/(T[C] + C)
  - Acetato de etilo: NIST Chemistry WebBook, SRD 69
    (https://webbook.nist.gov/cgi/cbook.cgi?ID=C141786&Mask=4).
    Forma: log10(Psat[bar]) = A - B/(T[K] + C)
    Rango valido: 288.73-348.98 K. A 355 K esto es una EXTRAPOLACION de
    ~6 K, verificada explicitamente (ver verificar_antoine_acetato_etilo):
    Psat(348.98 K)=0.960 atm (<1, correcto: bp real=350.2K>348.98K),
    Psat(350.2 K)=0.9996 atm (~1, es el punto de ebullicion normal),
    Psat(355 K)=1.168 atm (>1, correcto y de magnitud razonable).

  NOTA: se descarto la tabla de Antoine de Tosun (Apendice C, de Reid/
  Prausnitz/Sherwood) para acetato de etilo porque se detecto que sus
  filas estan desalineadas en la extraccion del PDF (verificado con
  n-hexano y benceno de la MISMA tabla: su formula da 80-790 bar en vez
  de ~1 atm en sus propios puntos de ebullicion reales).

UNIFAC: grupos de cada componente tomados de la asignacion OFICIAL de
DDBST (thermo.unifac.DDBST_UNIFAC_assignments, indexada por InChIKey),
NO fragmentados a mano:
    acido acetico:     CH3 + COOH
    etanol:            CH3 + CH2 + OH
    agua:              H2O
    acetato de etilo:  CH3 + CH2 + CH3COO

=====================================================================
NOTA METODOLOGICA IMPORTANTE
=====================================================================
Todos los calculos de este archivo usan resolver_lagrange() y
resolver_rand_modificado() DIRECTAMENTE (no successive_substitution_
algorithm() ni combined_algorithm() de algoritmos.py). Con UNIFAC, el
analisis de estabilidad (estabilidad.py) detecta una posible separacion
liquido-liquido en este sistema, lo que dispara el camino de adicion
automatica de fases -- un gap de robustez YA CONOCIDO y explicitamente
fuera de alcance para este proyecto (ver pruebas_validacion.py). Fijar
el numero de fases de antemano (1 fase para el Example 14.8, 2 fases
para el VLE) evita ese camino fragil sin tocarlo, y es ademas lo
fisicamente correcto: ambos casos ya se sabe de antemano cuantas fases
tienen (el libro y la tesis lo plantean asi).
"""

import numpy as np
from scipy.optimize import minimize

from inicializacion import minimizar_Q
from lagrange_multipliers import resolver_lagrange
from modified_rand import resolver_rand_modificado
from termodinamica import ln_Gamma_fase, gibbs_reducida


# ---------------------------------------------------------------------------
# 1. Sistema (estequiometria verificada: A @ N = 0)
# ---------------------------------------------------------------------------

COMPONENTES = ["acido acetico", "etanol", "agua", "acetato de etilo"]
A = np.array([
    [1.0, 0.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [1.0, 0.0, 1.0, 0.0],
])
N = np.array([-1.0, -1.0, 1.0, 1.0])
assert np.allclose(A @ N, 0.0), "La matriz de formula no es consistente con N"

# Grupos UNIFAC oficiales (DDBST, ver docstring del modulo)
CHEMGROUPS = [
    {1: 1, 42: 1},        # acido acetico: CH3 + COOH
    {1: 1, 2: 1, 14: 1},  # etanol: CH3 + CH2 + OH
    {16: 1},              # agua: H2O
    {1: 1, 2: 1, 21: 1},  # acetato de etilo: CH3 + CH2 + CH3COO
]

R_GAS = 8.314  # J/(mol K)
K_298 = 6.5266          # Smith, Van Ness & Abbott, Example 14.8
DH_RXN_298 = -3640.0    # J/mol, idem


def K_eq(T):
    """
    K_eq(T) via van't Hoff (dH_rxn constante), con los MISMOS datos del
    Example 14.8 de Smith, Van Ness & Abbott (K_298, dH_rxn,298). A
    373.15 K reproduce exactamente el K_373=4.8586 del libro.
    """
    return K_298 * np.exp(-DH_RXN_298 / R_GAS * (1.0 / T - 1.0 / 298.15))


def psat_SVN_kPa(T_K, Ac, Bc, Cc):
    """Antoine de Smith & Van Ness, Tabla B.2: ln(Psat[kPa])=A-B/(t[C]+C)."""
    return np.exp(Ac - Bc / ((T_K - 273.15) + Cc))


def psat_NIST_bar(T_K, Ac, Bc, Cc):
    """Antoine de NIST WebBook: log10(Psat[bar])=A-B/(T[K]+C)."""
    return 10 ** (Ac - Bc / (T_K + Cc))


def Psat_todos(T_K):
    """Presiones de vapor de los 4 componentes a T_K, en atm."""
    return np.array([
        psat_SVN_kPa(T_K, 15.0717, 3580.80, 224.650) / 101.325,    # acido acetico
        psat_SVN_kPa(T_K, 16.8958, 3795.17, 230.918) / 101.325,    # etanol
        psat_SVN_kPa(T_K, 16.3872, 3885.70, 230.170) / 101.325,    # agua
        psat_NIST_bar(T_K, 4.22809, 1245.702, -55.189) / 1.01325,  # acetato de etilo
    ])


def verificar_antoine_acetato_etilo():
    """
    Verifica la extrapolacion del Antoine NIST de acetato de etilo
    (rango valido 288.73-348.98 K) a 355 K, contra su punto de
    ebullicion normal real (350.2 K). Ver docstring del modulo.
    """
    p_348 = psat_NIST_bar(348.98, 4.22809, 1245.702, -55.189) / 1.01325
    p_bp = psat_NIST_bar(350.2, 4.22809, 1245.702, -55.189) / 1.01325
    p_355 = psat_NIST_bar(355.0, 4.22809, 1245.702, -55.189) / 1.01325
    return {"p_limite_rango_348.98K": p_348, "p_bp_real_350.2K": p_bp, "p_355K": p_355}


# ---------------------------------------------------------------------------
# 2. Resolucion de una fase liquida unica (Example 14.8)
# ---------------------------------------------------------------------------

def resolver_fase_unica(modelo, feed, T, g, con_scipy=True):
    """
    Resuelve el equilibrio de reaccion en una sola fase liquida con los
    tres metodos (Lagrange, RAND, scipy), fijando de antemano que hay
    una sola fase (ver nota metodologica del docstring del modulo).

    Retorna
    -------
    n_lag, n_rand, n_scipy : ndarray, shape (4,)
    info_lag, info_rand : dict (incluyen "historial_error")
    """
    b = A @ feed
    x0 = feed / np.sum(feed)
    ln_Gamma0 = [ln_Gamma_fase(
        modelo["tipo"], x0, p=modelo.get("p"), p0=modelo.get("p0"),
        Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
        T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
    )]
    lam0, n0, _ = minimizar_Q(A, b, [float(np.sum(feed))], g, ln_Gamma0)

    r_lag = resolver_lagrange(A, b, lam0, n0, g, [modelo])
    r_rand = resolver_rand_modificado(A, b, lam0, n0, g, [modelo])

    if not con_scipy:
        return r_lag["n_fases"][0], r_rand["n_fases"][0], None, r_lag, r_rand

    def G_de(n_flat):
        x_k = n_flat / np.sum(n_flat)
        ln_Gamma_k = ln_Gamma_fase(
            modelo["tipo"], x_k, p=modelo.get("p"), p0=modelo.get("p0"),
            Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
            T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
        )
        return gibbs_reducida([n_flat], g, [ln_Gamma_k])

    res_scipy = minimize(
        G_de, r_lag["n_fases"][0], method="SLSQP", bounds=[(1e-10, None)] * 4,
        constraints=[{"type": "eq", "fun": lambda nf: A @ nf - b}],
        options={"maxiter": 1000, "ftol": 1e-15},
    )
    return (r_lag["n_fases"][0], r_rand["n_fases"][0], res_scipy.x,
            r_lag, r_rand)


# ---------------------------------------------------------------------------
# 3. Resolucion de VLE completo (2 fases: liquido + vapor ideal)
# ---------------------------------------------------------------------------

def resolver_vle(modelo_liquido, feed, T, g, Psat,
                  n_liq0=None, n_vap0=None, lam0_prev=None):
    """
    Resuelve el equilibrio liquido-vapor con reaccion (2 fases, fijadas
    de antemano -- ver nota metodologica del docstring del modulo).

    Si se provee lam0_prev (lambda convergido de un punto anterior de
    un barrido de T o p), se usa directamente como estimacion inicial
    en vez de recalcular lambda desde cero con minimizar_Q. Esto es un
    metodo de continuacion que produce barridos mucho mas suaves,
    especialmente cerca de la ventana de transicion liquido-vapor
    (ver diagramas_reactivos.barrido_T_esterificacion_VLE).

    Retorna
    -------
    (n_liq, n_vap) para Lagrange, RAND y scipy; mas info_lag, info_rand.
    """
    b = A @ feed
    modelo_vapor = {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}

    if n_liq0 is None:
        n_liq0 = np.array([0.05, 0.05, 0.10, 0.10])
    if n_vap0 is None:
        n_vap0 = np.array([0.10, 0.10, 0.25, 0.25])

    n_t_fases = [np.sum(n_liq0), np.sum(n_vap0)]
    ln_Gamma0 = [
        ln_Gamma_fase(modelo_liquido["tipo"], n_liq0 / np.sum(n_liq0),
                       Psat=Psat, p0=1.0, T=modelo_liquido.get("T"),
                       chemgroups=modelo_liquido.get("chemgroups")),
        ln_Gamma_fase(modelo_vapor["tipo"], n_vap0 / np.sum(n_vap0), p=1.0, p0=1.0),
    ]
    if lam0_prev is not None:
        lam0, n0 = lam0_prev, [n_liq0, n_vap0]
    else:
        lam0, n0, _ = minimizar_Q(A, b, n_t_fases, g, ln_Gamma0)

    r_lag = resolver_lagrange(A, b, lam0, n0, g, [modelo_liquido, modelo_vapor])
    r_rand = resolver_rand_modificado(A, b, lam0, n0, g, [modelo_liquido, modelo_vapor])

    def G_de(nflat):
        nf = [nflat[:4], nflat[4:]]
        ln_Gamma_fases = []
        for n_k, m in zip(nf, [modelo_liquido, modelo_vapor]):
            x_k = n_k / np.sum(n_k)
            ln_Gamma_fases.append(ln_Gamma_fase(
                m["tipo"], x_k, p=m.get("p"), p0=m.get("p0"), Psat=m.get("Psat"),
                T=m.get("T"), chemgroups=m.get("chemgroups")))
        return gibbs_reducida(nf, g, ln_Gamma_fases)

    x0_scipy = np.concatenate(r_lag["n_fases"])
    res = minimize(
        G_de, x0_scipy, method="SLSQP", bounds=[(1e-10, None)] * 8,
        constraints=[{"type": "eq", "fun": lambda nf: A @ (nf[:4] + nf[4:]) - b}],
        options={"maxiter": 2000, "ftol": 1e-15},
    )
    n_scipy = [res.x[:4], res.x[4:]]
    return r_lag, r_rand, n_scipy


# ---------------------------------------------------------------------------
# 4. Reporte
# ---------------------------------------------------------------------------

def _reporte_fase(nombre, n_k):
    n_t = np.sum(n_k)
    x = n_k / n_t
    print(f"  {nombre}: n_t = {n_t:.6f} mol")
    for comp, xi in zip(COMPONENTES, x):
        print(f"      x_{comp:18s} = {xi:.6f}")


if __name__ == "__main__":
    print("=" * 70)
    print("Esterificacion acido acetico + etanol -> acetato de etilo + agua")
    print("=" * 70)

    # --- Verificacion del Antoine extrapolado de acetato de etilo ---
    chequeo = verificar_antoine_acetato_etilo()
    print("\nVerificacion Antoine NIST (acetato de etilo), extrapolacion a 355 K:")
    for k, v in chequeo.items():
        print(f"  {k} = {v:.4f} atm")

    # --- Caso 1: fase liquida unica, 373.15 K (Example 14.8) ---
    print("\n" + "-" * 70)
    print("CASO 1: fase liquida unica, T = 373.15 K (Example 14.8, S&VN)")
    print("-" * 70)
    T1 = 373.15
    feed1 = np.array([1.0, 1.0, 0.0, 0.0])
    g1 = np.array([0.0, 0.0, 0.0, -np.log(K_eq(T1))])

    modelo_ideal = {"tipo": "liquido_ideal", "Psat": np.ones(4), "p0": 1.0}
    n_lag, n_rand, n_scipy, info_lag, info_rand = resolver_fase_unica(modelo_ideal, feed1, T1, g1)
    print(f"\n[Ideal] e = {n_lag[3]:.6f} (libro: 0.6879), "
          f"x_EtAc = {n_lag[3]/np.sum(n_lag):.6f} (libro: 0.344)")
    _reporte_fase("Liquido (ideal)", n_lag)

    modelo_unifac = {"tipo": "liquido_unifac", "Psat": np.ones(4), "p0": 1.0,
                      "T": T1, "chemgroups": CHEMGROUPS}
    n_lag_uf, n_rand_uf, n_scipy_uf, info_lag_uf, info_rand_uf = resolver_fase_unica(
        modelo_unifac, feed1, T1, g1)
    print(f"\n[UNIFAC] x_EtAc = {n_lag_uf[3]/np.sum(n_lag_uf):.6f} (experimental: 0.33)")
    _reporte_fase("Liquido (UNIFAC)", n_lag_uf)

    # --- Caso 2: VLE completo, 355 K, feed equimolar (Tabla 4.4 tesis) ---
    print("\n" + "-" * 70)
    print("CASO 2: VLE completo, T = 355 K, p = 1 atm, feed equimolar 0.5/0.5")
    print("-" * 70)
    T2 = 355.0
    feed2 = np.array([0.5, 0.5, 0.0, 0.0])
    g2 = np.array([0.0, 0.0, 0.0, -np.log(K_eq(T2))])
    Psat2 = Psat_todos(T2)
    print(f"\nPsat a {T2} K (atm): " + ", ".join(
        f"{c}={p:.4f}" for c, p in zip(COMPONENTES, Psat2)))

    modelo_liq_ideal_vle = {"tipo": "liquido_ideal", "Psat": Psat2, "p0": 1.0}
    r_lag_id, r_rand_id, n_scipy_id = resolver_vle(modelo_liq_ideal_vle, feed2, T2, g2, Psat2)
    nt_liq_id = np.sum(r_lag_id["n_fases"][0])
    nt_vap_id = np.sum(r_lag_id["n_fases"][1])
    print(f"\n[Liquido ideal] fraccion liquido = {nt_liq_id/(nt_liq_id+nt_vap_id):.4f}, "
          f"fraccion vapor = {nt_vap_id/(nt_liq_id+nt_vap_id):.4f}  "
          "(sistema subenfriado, sin VLE real -- igual que ejemplo_mtbe.py)")

    modelo_liq_unifac_vle = {"tipo": "liquido_unifac", "Psat": Psat2, "p0": 1.0,
                              "T": T2, "chemgroups": CHEMGROUPS}
    r_lag_uf2, r_rand_uf2, n_scipy_uf2 = resolver_vle(modelo_liq_unifac_vle, feed2, T2, g2, Psat2)
    n_liq_uf2, n_vap_uf2 = r_lag_uf2["n_fases"]
    nt_liq_uf2, nt_vap_uf2 = np.sum(n_liq_uf2), np.sum(n_vap_uf2)
    print(f"\n[UNIFAC] fraccion liquido = {nt_liq_uf2/(nt_liq_uf2+nt_vap_uf2):.4f}, "
          f"fraccion vapor = {nt_vap_uf2/(nt_liq_uf2+nt_vap_uf2):.4f}")
    _reporte_fase("Liquido (UNIFAC, VLE)", n_liq_uf2)
    _reporte_fase("Vapor (UNIFAC, VLE)", n_vap_uf2)

    print("\nComparacion cualitativa con Tabla 4.4 de la tesis (355 K, feed 0.5/0.5):")
    print("  Tesis (UNIQUAC+Xiao et al. 1989): vapor=0.882, liquido=0.118")
    print(f"  Este trabajo (UNIFAC):            vapor={nt_vap_uf2/(nt_liq_uf2+nt_vap_uf2):.3f}, "
          f"liquido={nt_liq_uf2/(nt_liq_uf2+nt_vap_uf2):.3f}")
    print("  (misma tendencia cualitativa, magnitud distinta -- modelos gamma distintos)")
