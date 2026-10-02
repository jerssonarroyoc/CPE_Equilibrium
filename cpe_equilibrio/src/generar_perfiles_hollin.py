"""
generar_perfiles_hollin.py
=============================

Perfiles de concentracion de un sistema de combustion Vapor-Solido
(CH4/aire rico, con formacion de hollin/carbono solido grafito) y,
donde el barrido lo permite, Vapor-Solido-Liquido (condensacion de
agua), usando combustion_gibbs.resolver_hollin()/barrido_hollin()
(Sistema G de ese archivo): el NUMERO de fases presentes en cada punto
lo decide el analisis de estabilidad de Michelsen (estabilidad.py), NO
un supuesto fijo -- ver docstring de combustion_gibbs.py para el
detalle del tipo de fase "condensado_puro" (termodinamica.py) y de la
verificacion de balance de materia usada para descartar puntos no
confiables.

EXPLORATORIO (misma advertencia de alcance que el resto del modulo de
combustion): datos termoquimicos aproximados, dCp=0, no para diseno.

LIMITACION ENCONTRADA AL EXPLORAR ESTE SISTEMA (documentada aqui en vez
de ocultada): la fase liquida "H2O(l)" SI esta implementada (mismo
mecanismo que "C(s)", ver termodinamica.py), pero no se logro demostrar
su aparicion con este codigo: requiere T por debajo de la temperatura
critica del agua (~647 K), y la inicializacion de
inicializacion.minimizar_Q (archivo ya validado, no modificado aqui)
sobredesborda (overflow) para especies de combustion de esta magnitud
de |dGf| por debajo de ~650-700 K. Estas dos restricciones (una fisica,
una numerica) dejan la condensacion de agua fuera del rango que este
barrido puede mostrar de forma confiable sin mas trabajo de robustez
numerica en un archivo que esta fuera de alcance modificar. El sistema
mostrado aqui es por tanto Vapor-Solido (V-S): vapor + hollin.

Ejecutar con:  python generar_perfiles_hollin.py
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import combustion_gibbs as cg
from estilo_graficas import aplicar_estilo_profesional, PALETA

aplicar_estilo_profesional()

DIR_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "docs", "figuras_combustion")
os.makedirs(DIR_FIGURAS, exist_ok=True)
DPI = 300


def _guardar(fig, nombre):
    ruta = os.path.join(DIR_FIGURAS, nombre)
    fig.savefig(ruta, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  guardado: {ruta}")


def _barrido_hollin_con_gaps(valores, feed_fn, T_fn=None, p_fn=None):
    """
    Envoltura de cg.barrido_hollin() que ademas marca con NaN los
    puntos donde el balance de materia no fue confiable (ver
    combustion_gibbs.resolver_hollin, "balance_ok"), para que el punto
    aparezca como un hueco en la grafica en vez de un numero erroneo.
    """
    NC = len(cg.ESPECIES_HOLLIN)
    x_vapor = np.full((len(valores), NC), np.nan)
    n_C_solido = np.full(len(valores), np.nan)
    n_H2O_liquido = np.full(len(valores), np.nan)

    for j, val in enumerate(valores):
        # feed_fn ya retorna b = [C,H,O,N] directamente (igual que
        # combustion_gibbs.feed_llama/feed_hollin), no una composicion
        # en espacio de especies.
        b = feed_fn(val)
        T = T_fn(val) if T_fn is not None else val
        p = p_fn(val) if p_fn is not None else 1.0
        r = cg.resolver_hollin(cg.A_HOLLIN, b, cg.ESPECIES_HOLLIN, T, p=p)
        if not r["balance_ok"]:
            continue
        n_vapor = r["n_fases"][0]
        x_vapor[j] = n_vapor / np.sum(n_vapor)
        n_C_solido[j] = cg._moles_fase_condensada(r, cg.IDX_C_SOLIDO)
        n_H2O_liquido[j] = cg._moles_fase_condensada(r, cg.IDX_H2O_LIQUIDO)

    return x_vapor, n_C_solido, n_H2O_liquido


# ===========================================================================
# 1. Hollin (C solido) vs T, a phi=4.0 fijo (mezcla muy rica, pobre en
#    oxigeno): reaccion de Boudouard (C + CO2 <-> 2 CO) consume el
#    carbono solido al subir T.
# ===========================================================================

def fig_hollin_vs_T():
    phi_fijo = 4.0
    temperaturas = np.linspace(700, 2600, 25)
    x_vapor, n_C, n_H2O_l = _barrido_hollin_con_gaps(
        temperaturas, lambda T: cg.feed_hollin(phi=phi_fijo), T_fn=lambda T: T,
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True,
                                     gridspec_kw={"height_ratios": [1.3, 1]})

    for especie, color in zip(["CO2", "H2O", "CO", "H2", "N2"], PALETA):
        i = cg.ESPECIES_HOLLIN.index(especie)
        ax1.plot(temperaturas, x_vapor[:, i], "o-", color=color, markersize=3, label=especie)
    ax1.set_ylabel("Fracción molar (fase vapor)")
    ax1.set_title(f"CH$_4$/aire muy rico ($\\phi$={phi_fijo:.1f}) vs. T: perfil de la fase vapor")
    ax1.legend(ncol=2, fontsize=8.5)

    ax2.plot(temperaturas, n_C, "o-", color="#444444", markersize=4)
    ax2.set_yscale("log")
    ax2.set_xlabel("Temperatura (K)")
    ax2.set_ylabel("Moles de C(s) (hollín)")
    ax2.set_title("Carbono sólido en equilibrio: disminuye al subir T\n"
                   "(Boudouard, C + CO$_2$ ⇌ 2 CO, favorecida hacia la derecha a alta T)")
    ax2.text(0.02, 0.05,
             "Rango T limitado a 700-2600 K: por debajo de ~700 K la\n"
             "inicialización de minimizar_Q() (archivo ya validado, no\n"
             "modificado) sobredesborda para especies de combustión de\n"
             "esta magnitud de ΔGf — ver docstring de este script.",
             transform=ax2.transAxes, fontsize=7, style="italic",
             verticalalignment="bottom",
             bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="#cccccc"))

    fig.tight_layout()
    _guardar(fig, "11_hollin_vs_T.png")


# ===========================================================================
# 2. Hollin (C solido) vs phi, a T=1200 K fija: umbral de aparicion del
#    hollin (transición Vapor -> Vapor+Sólido) al enriquecer la mezcla.
# ===========================================================================

def fig_hollin_vs_phi():
    T_fijo = 1200.0
    phis = np.linspace(0.8, 4.3, 24)
    x_vapor, n_C, n_H2O_l = _barrido_hollin_con_gaps(
        phis, lambda phi: cg.feed_hollin(phi=phi), p_fn=lambda phi: 1.0,
        T_fn=lambda phi: T_fijo,
    )

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8), sharex=True,
                                     gridspec_kw={"height_ratios": [1.3, 1]})

    for especie, color in zip(["CO2", "H2O", "CO", "H2", "N2"], PALETA):
        i = cg.ESPECIES_HOLLIN.index(especie)
        ax1.plot(phis, x_vapor[:, i], "o-", color=color, markersize=3, label=especie)
    ax1.axvline(1.0, color="gray", linestyle=":", linewidth=1)
    ax1.set_ylabel("Fracción molar (fase vapor)")
    ax1.set_title(f"CH$_4$/aire vs. $\\phi$ (T={T_fijo:.0f} K): perfil de la fase vapor")
    ax1.legend(ncol=2, fontsize=8.5)

    ax2.plot(phis, n_C, "o-", color="#444444", markersize=4)
    umbral = phis[np.nanargmax(n_C > 0)] if np.any(n_C > 0) else None
    if umbral is not None:
        ax2.axvline(umbral, color="#d62728", linestyle="--", linewidth=1.2)
        ax2.text(umbral + 0.05, ax2.get_ylim()[1] * 0.9 if ax2.get_ylim()[1] > 0 else 0.05,
                 f"umbral ≈ {umbral:.2f}", fontsize=8.5, color="#d62728")
    ax2.set_xlabel("Razón de equivalencia $\\phi$")
    ax2.set_ylabel("Moles de C(s) (hollín)")
    ax2.set_title("Transición Vapor → Vapor+Sólido: el hollín aparece\n"
                   "solo cuando ya no alcanza el O$_2$ ni para CO completo")

    fig.tight_layout()
    _guardar(fig, "12_hollin_vs_phi.png")


# ===========================================================================
if __name__ == "__main__":
    print("Generando perfiles de hollin (V-S) en", os.path.abspath(DIR_FIGURAS))
    print("\n[1/2] Hollín vs T (phi=4.0 fijo)...")
    fig_hollin_vs_T()
    print("[2/2] Hollín vs phi (T=1200 K fijo)...")
    fig_hollin_vs_phi()
