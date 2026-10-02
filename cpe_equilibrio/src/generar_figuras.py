"""
generar_figuras.py
====================

Genera las 6 figuras obligatorias del documento LaTeX (docs/figuras/),
TODAS a partir de ejecuciones reales de los solvers ya validados en
pruebas_validacion.py -- ninguna figura usa datos inventados o
dibujados a mano.

Sistemas usados:
  - MTBE (ejemplo_mtbe.py), caso bifasico p=0.80 bar: figuras 1, 2, 3, 5
  - MTBE, analisis de estabilidad liquido (p=1.01325 bar) vs. vapor
    trial: figura 4 (TPD)
  - Esterificacion acido acetico/etanol (ejemplo_acetic_etanol.py):
    figura 6 (conversion vs T)

Ejecutar con:  python generar_figuras.py
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import ejemplo_mtbe as mtbe
import ejemplo_acetic_etanol as ace
from inicializacion import minimizar_Q
from lagrange_multipliers import resolver_lagrange
from modified_rand import resolver_rand_modificado
from estabilidad import tpd, analizar_estabilidad
from termodinamica import ln_Gamma_fase, gibbs_reducida
from scipy.optimize import minimize
from estilo_graficas import aplicar_estilo_profesional

aplicar_estilo_profesional()

DIR_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "docs", "figuras")
os.makedirs(DIR_FIGURAS, exist_ok=True)
DPI = 300


def _guardar(fig, nombre):
    ruta = os.path.join(DIR_FIGURAS, nombre)
    fig.savefig(ruta, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  guardado: {ruta}")


# ---------------------------------------------------------------------------
# Preparacion comun: caso MTBE bifasico (p = 0.80 bar), ver ejemplo_mtbe.py
# ---------------------------------------------------------------------------

def _resolver_mtbe_bifasico():
    # Construimos directamente el sistema de 2 fases (liquido + vapor),
    # para evitar pasar por el analisis de estabilidad (no es necesario:
    # ya sabemos por ejemplo_mtbe.py que a 0.80 bar el sistema es
    # bifasico). La minimizacion de Q se hace YA con 2 fases (no con 1),
    # para que el lambda inicial sea consistente con el sistema que
    # realmente se va a resolver.
    modelo_vapor_080 = {"tipo": "vapor_ideal", "p": 0.80, "p0": mtbe.P0}
    modelos = [mtbe.modelo_liquido, modelo_vapor_080]

    n_t_liq0, n_t_vap0 = 0.9 * np.sum(mtbe.n_feed), 0.1 * np.sum(mtbe.n_feed)
    x0 = mtbe.n_feed / np.sum(mtbe.n_feed)
    # x0 tiene MTBE=0 (no hay en el feed); usamos una composicion inicial
    # con los 3 componentes presentes para evitar log(0) en la Ec. 3.34.
    x0_trial = np.array([0.3, 0.3, 0.4])
    ln_Gamma0 = [
        ln_Gamma_fase(mtbe.modelo_liquido["tipo"], x0_trial,
                       Psat=mtbe.modelo_liquido["Psat"], p0=mtbe.P0),
        ln_Gamma_fase(modelo_vapor_080["tipo"], x0_trial, p=0.80, p0=mtbe.P0),
    ]
    lam0, n_fases0, _ = minimizar_Q(mtbe.A, mtbe.b, [n_t_liq0, n_t_vap0], mtbe.g, ln_Gamma0)

    r_lag = resolver_lagrange(mtbe.A, mtbe.b, lam0, n_fases0, mtbe.g, modelos)
    r_rand = resolver_rand_modificado(mtbe.A, mtbe.b, lam0, n_fases0, mtbe.g, modelos)

    def G_de(nflat):
        nf = [nflat[:3], nflat[3:]]
        ln_Gamma_fases = []
        for n_k, m in zip(nf, modelos):
            x_k = n_k / np.sum(n_k)
            ln_Gamma_fases.append(ln_Gamma_fase(
                m["tipo"], x_k, p=m.get("p"), p0=m.get("p0"), Psat=m.get("Psat")))
        return gibbs_reducida(nf, mtbe.g, ln_Gamma_fases)

    x0_scipy = np.concatenate(r_lag["n_fases"])
    res = minimize(G_de, x0_scipy, method="SLSQP", bounds=[(1e-10, None)] * 6,
                   constraints=[{"type": "eq",
                                 "fun": lambda nf: mtbe.A @ (nf[:3] + nf[3:]) - mtbe.b}],
                   options={"maxiter": 1000, "ftol": 1e-15})
    n_scipy = [res.x[:3], res.x[3:]]
    return r_lag, r_rand, n_scipy


def figura_convergencia_ssa(r_lag):
    """Figura 1: error vs iteracion (log) del metodo de Lagrange (SSA)."""
    hist = r_lag["historial_error"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(range(1, len(hist) + 1), hist, "o-", color="#1f77b4")
    ax.set_xlabel("Iteracion de Newton")
    ax.set_ylabel("Error (Ec. 3.77), escala log")
    ax.set_title("Convergencia del metodo de multiplicadores de Lagrange\n"
                  "(sintesis de MTBE, VLE bifasico, p = 0.80 bar)")
    ax.grid(True, which="both", alpha=0.3)
    _guardar(fig, "convergencia_ssa.png")


def figura_convergencia_rand(r_rand):
    """Figura 2: error vs iteracion (log) del RAND modificado."""
    hist = r_rand["historial_error"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(range(1, len(hist) + 1), hist, "s-", color="#d62728")
    ax.set_xlabel("Iteracion de Newton")
    ax.set_ylabel("Error (Ec. 3.78), escala log")
    ax.set_title("Convergencia del metodo RAND modificado\n"
                  "(sintesis de MTBE, VLE bifasico, p = 0.80 bar)")
    ax.grid(True, which="both", alpha=0.3)
    _guardar(fig, "convergencia_rand.png")


def figura_gibbs_descenso(r_rand):
    """Figura 3: G/RT vs iteracion del RAND modificado (debe decrecer)."""
    hist = r_rand["G_RT_historial"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(range(len(hist)), hist, "D-", color="#2ca02c")
    ax.set_xlabel("Iteracion")
    ax.set_ylabel("G / (RT)")
    ax.set_title("Descenso monotonico de la energia de Gibbs reducida\n"
                  "(metodo RAND modificado, sintesis de MTBE)")
    ax.grid(True, alpha=0.3)
    _guardar(fig, "gibbs_descenso.png")


def figura_estabilidad_tpd():
    """
    Figura 4: funcion tpd(w) vs composicion de la fase de prueba (vapor),
    para la fase liquida de MTBE YA REACCIONADA (converge con
    resolver_lagrange en una sola fase) a p = 1.01325 bar (caso
    monofasico, estable) y p = 0.80 bar (caso bifasico, inestable antes
    de anadir la fase vapor) -- ver ejemplo_mtbe.py. Se usa la
    composicion reaccionada (no el feed, que tiene MTBE=0 exacto y
    causaria log(0) en la Ec. 3.27).
    """
    modelo_liq = mtbe.modelo_liquido

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for p_sistema, color, estilo in [(1.01325, "#1f77b4", "estable"),
                                      (0.80, "#d62728", "inestable")]:
        modelo_vap = {"tipo": "vapor_ideal", "p": p_sistema, "p0": mtbe.P0}

        # Composicion liquida de referencia: la fase unica convergida
        # (con reaccion), no el feed.
        ln_Gamma0 = [ln_Gamma_fase(modelo_liq["tipo"], np.array([0.3, 0.3, 0.4]),
                                     Psat=modelo_liq["Psat"], p0=mtbe.P0)]
        lam0, n0, _ = minimizar_Q(mtbe.A, mtbe.b, [np.sum(mtbe.n_feed)], mtbe.g, ln_Gamma0)
        r_liq = resolver_lagrange(mtbe.A, mtbe.b, lam0, n0, mtbe.g, [modelo_liq])
        z = r_liq["x_fases"][0]

        # En vez de un barrido 1D arbitrario (que puede no pasar cerca
        # del minimo real de tpd en el simplex 3D), usamos el propio
        # analisis de estabilidad para encontrar la composicion de
        # prueba w* que efectivamente minimiza tpd, y barremos una
        # linea recta entre z y w* (garantiza pasar por el minimo real).
        estable, mejor = analizar_estabilidad(z, modelo_liq, [modelo_vap])
        w_estrella = mejor["w"]

        parametro_t = np.linspace(0.02, 1.3, 60)
        valores_tpd = []
        for t in parametro_t:
            w = (1 - t) * z + t * w_estrella
            w = np.clip(w, 1e-12, None)
            w = w / np.sum(w)
            valores_tpd.append(tpd(w, z, modelo_vap, modelo_liq))
        ax.plot(parametro_t, valores_tpd, "-", color=color,
                 label=f"p = {p_sistema:.2f} bar ({estilo}, "
                       f"tm$_{{min}}$={mejor['tm']:.3f})")

    ax.axhline(0.0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(1.0, color="gray", linewidth=0.6, linestyle=":")
    ax.set_xlabel("Parametro t a lo largo de z -> w*  (t=1: composicion optima w*)")
    ax.set_ylabel("tpd(w)  (Ec. 3.27)")
    ax.set_title("Analisis de estabilidad de Michelsen\n"
                  "(fase liquida de MTBE probada contra vapor de prueba)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    _guardar(fig, "estabilidad_tpd.png")


def figura_comparacion_solvers(r_lag, r_rand, n_scipy):
    """
    Figura 5: barras comparando Lagrange (SSA) vs RAND vs scipy --
    diferencia absoluta en fracciones molares respecto a scipy
    (minimizacion directa de Gibbs, metodo independiente).
    """
    etiquetas = []
    diff_lag = []
    diff_rand = []
    nombres_fase = ["liquido", "vapor"]
    for k, nombre_fase in enumerate(nombres_fase):
        x_lag = r_lag["n_fases"][k] / np.sum(r_lag["n_fases"][k])
        x_rand = r_rand["n_fases"][k] / np.sum(r_rand["n_fases"][k])
        x_scipy = n_scipy[k] / np.sum(n_scipy[k])
        for comp, xl, xr, xs in zip(mtbe.COMPONENTES, x_lag, x_rand, x_scipy):
            etiquetas.append(f"{comp}\n({nombre_fase})")
            diff_lag.append(abs(xl - xs))
            diff_rand.append(abs(xr - xs))

    x_pos = np.arange(len(etiquetas))
    ancho = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x_pos - ancho / 2, diff_lag, ancho, label="|Lagrange (SSA) - scipy|", color="#1f77b4")
    ax.bar(x_pos + ancho / 2, diff_rand, ancho, label="|RAND - scipy|", color="#d62728")
    ax.set_yscale("log")
    ax.set_ylabel("Diferencia absoluta en fraccion molar (escala log)")
    ax.set_title("Consistencia cruzada: Lagrange vs. RAND vs. minimizacion\n"
                  "directa de Gibbs (scipy) -- sintesis de MTBE, VLE bifasico")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(etiquetas, fontsize=8)
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    _guardar(fig, "comparacion_solvers.png")


def figura_conversion_acetic_etanol():
    """
    Figura 6: conversion de equilibrio (x_EtAc) vs temperatura, fase
    liquida unica, para los modelos ideal y UNIFAC -- ver
    ejemplo_acetic_etanol.py.
    """
    temperaturas = np.linspace(340.0, 385.0, 10)
    feed = np.array([1.0, 1.0, 0.0, 0.0])

    x_EtAc_ideal = []
    x_EtAc_unifac = []
    for T in temperaturas:
        g = np.array([0.0, 0.0, 0.0, -np.log(ace.K_eq(T))])

        modelo_ideal = {"tipo": "liquido_ideal", "Psat": np.ones(4), "p0": 1.0}
        n_lag_id, _, _, _, _ = ace.resolver_fase_unica(modelo_ideal, feed, T, g, con_scipy=False)
        x_EtAc_ideal.append(n_lag_id[3] / np.sum(n_lag_id))

        modelo_uf = {"tipo": "liquido_unifac", "Psat": np.ones(4), "p0": 1.0,
                      "T": T, "chemgroups": ace.CHEMGROUPS}
        n_lag_uf, _, _, _, _ = ace.resolver_fase_unica(modelo_uf, feed, T, g, con_scipy=False)
        x_EtAc_unifac.append(n_lag_uf[3] / np.sum(n_lag_uf))

        print(f"    T={T:.1f} K: x_EtAc(ideal)={x_EtAc_ideal[-1]:.4f}, "
              f"x_EtAc(UNIFAC)={x_EtAc_unifac[-1]:.4f}")

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(temperaturas, x_EtAc_ideal, "o-", color="#1f77b4", label="Solucion ideal (S&VN)")
    ax.plot(temperaturas, x_EtAc_unifac, "s-", color="#ff7f0e", label="UNIFAC")
    ax.axhline(0.33, color="green", linestyle="--", linewidth=1,
               label="Experimental a 373.15 K (0.33)")
    ax.axvline(373.15, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("x_(acetato de etilo) en el equilibrio")
    ax.set_title("Conversion de equilibrio vs. temperatura\n"
                  "(esterificacion acido acetico + etanol, fase liquida unica)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _guardar(fig, "acetic_etanol_conversion.png")


if __name__ == "__main__":
    print("Generando figuras en", os.path.abspath(DIR_FIGURAS))

    print("\n[1/6, 2/6, 3/6, 5/6] Resolviendo caso MTBE bifasico (p=0.80 bar)...")
    r_lag, r_rand, n_scipy = _resolver_mtbe_bifasico()
    figura_convergencia_ssa(r_lag)
    figura_convergencia_rand(r_rand)
    figura_gibbs_descenso(r_rand)
    figura_comparacion_solvers(r_lag, r_rand, n_scipy)

    print("\n[4/6] Analisis de estabilidad (TPD)...")
    figura_estabilidad_tpd()

    print("\n[6/6] Barrido de temperatura, esterificacion acido acetico/etanol...")
    figura_conversion_acetic_etanol()

    print("\nListo.")
