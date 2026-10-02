"""
generar_perfiles_combustion.py
=================================

Perfiles de concentracion de equilibrio para procesos de combustion y
oxidacion, obtenidos EXCLUSIVAMENTE por minimizacion no estequiometrica
de la energia de Gibbs (potenciales de elemento), exactamente el mismo
formalismo implementado y validado en el resto del proyecto
(resolver_lagrange, Ec. 3.6 y 3.14 de Tsanas 2018) -- ver
combustion_gibbs.py para el detalle de cada sistema y los datos
termoquimicos usados (aproximados, dCp=0, ver advertencia alli).

Diez perfiles, cinco sistemas:
  1-2. Disociacion termica: CO2 y H2O puros                 -> 2 figuras
  3-5. Combustion CH4/aire: vs T, vs phi, vs P               -> 3 figuras
  6.   Combustion H2/aire vs phi                             -> 1 figura
  7.   Combustion C3H8 (propano)/aire vs phi                 -> 1 figura
  8.   Reaccion de desplazamiento agua-gas (water-gas shift) -> 1 figura
  9.   NOx (NO) vs T, familia de curvas a varios phi         -> 1 figura
  10.  Comparacion de NOx entre 3 combustibles vs T          -> 1 figura

Ejecutar con:  python generar_perfiles_combustion.py
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import combustion_gibbs as cg
from estilo_graficas import aplicar_estilo_profesional

aplicar_estilo_profesional()

DIR_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "docs", "figuras_combustion")
os.makedirs(DIR_FIGURAS, exist_ok=True)
DPI = 300


def _guardar(fig, nombre):
    ruta = os.path.join(DIR_FIGURAS, nombre)
    fig.savefig(ruta, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  guardado: {ruta}")


def _barrido_T(A, especies, b_fn, temperaturas, n_t_guess=None):
    """Barrido de T con continuacion (metodo de Newton encadenado)."""
    composiciones = []
    n_prev, lam_prev = None, None
    for T in temperaturas:
        b = b_fn(T) if callable(b_fn) else b_fn
        n, lam = cg.resolver_combustion(A, b, especies, T, n_t_guess=n_t_guess,
                                          n0_prev=n_prev, lam0_prev=lam_prev)
        composiciones.append(n / np.sum(n))
        n_prev, lam_prev = n, lam
    return np.array(composiciones)


def _barrido_phi(A, especies, feed_fn, phis, T_fijo):
    """Barrido de razon de equivalencia con continuacion."""
    composiciones = []
    n_prev, lam_prev = None, None
    for phi in phis:
        b = feed_fn(phi)
        n, lam = cg.resolver_combustion(A, b, especies, T_fijo,
                                          n_t_guess=np.sum(b) / 3,
                                          n0_prev=n_prev, lam0_prev=lam_prev)
        composiciones.append(n / np.sum(n))
        n_prev, lam_prev = n, lam
    return np.array(composiciones)


# ===========================================================================
# 1-2. Disociacion termica: CO2 y H2O puros
# ===========================================================================

def fig_1_disociacion_CO2():
    temperaturas = np.linspace(1200, 3600, 30)
    b = cg.A_CO2 @ cg.feed_CO2(1.0)
    comp = _barrido_T(cg.A_CO2, cg.ESPECIES_CO2, b, temperaturas, n_t_guess=1.0)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for i, especie in enumerate(cg.ESPECIES_CO2):
        ax.plot(temperaturas, comp[:, i], "-", label=especie, linewidth=2)
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar")
    ax.set_title("Disociación de CO$_2$ en equilibrio:\nCO$_2$ ⇌ CO + ½O$_2$ (p = 1 atm)")
    ax.legend()
    _guardar(fig, "01_disociacion_CO2.png")


def fig_2_disociacion_H2O():
    temperaturas = np.linspace(1200, 3600, 30)
    b = cg.A_H2O @ cg.feed_H2O()
    comp = _barrido_T(cg.A_H2O, cg.ESPECIES_H2O, b, temperaturas, n_t_guess=1.5)

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for i, especie in enumerate(cg.ESPECIES_H2O):
        ax.plot(temperaturas, comp[:, i], "-", label=especie, linewidth=2)
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 1)
    ax.set_title("Disociación de H$_2$O en equilibrio:\n2H$_2$ + O$_2$ ⇌ 2H$_2$O + ... (p = 1 atm)")
    ax.legend(ncol=2, fontsize=8)
    _guardar(fig, "02_disociacion_H2O.png")


# ===========================================================================
# 3-5. Combustion CH4/aire
# ===========================================================================

def fig_3_CH4_vs_T():
    temperaturas = np.linspace(1600, 2800, 20)
    b = cg.feed_llama(phi=1.0)
    comp = _barrido_T(cg.A_LLAMA, cg.ESPECIES_LLAMA, b, temperaturas, n_t_guess=np.sum(b) / 3)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    principales = ["CO2", "H2O", "N2"]
    trazas = ["CO", "H2", "O2", "NO", "OH", "H", "O"]
    for especie in principales:
        i = cg.ESPECIES_LLAMA.index(especie)
        ax1.plot(temperaturas, comp[:, i], "-", linewidth=2, label=especie)
    for especie in trazas:
        i = cg.ESPECIES_LLAMA.index(especie)
        ax2.plot(temperaturas, comp[:, i], "-", linewidth=1.5, label=especie)
    ax2.set_yscale("log")
    ax2.set_ylim(1e-7, 0.2)
    for ax in (ax1, ax2):
        ax.set_xlabel("Temperatura (K)")
        ax.legend(fontsize=8)
    ax1.set_ylabel("Fracción molar")
    ax1.set_title("Especies mayoritarias")
    ax2.set_title("Especies traza (incl. NO)")
    fig.suptitle("CH$_4$/aire en equilibrio vs. T ($\\phi$=1, p=1 atm)", y=1.02)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    _guardar(fig, "03_CH4_aire_vs_T.png")


def fig_4_CH4_vs_phi():
    phis = np.linspace(0.5, 1.6, 23)
    T_fijo = 2200.0
    comp = _barrido_phi(cg.A_LLAMA, cg.ESPECIES_LLAMA, cg.feed_llama, phis, T_fijo)

    fig, ax = plt.subplots(figsize=(7, 5))
    for especie in ["CO2", "H2O", "CO", "H2", "O2", "NO"]:
        i = cg.ESPECIES_LLAMA.index(especie)
        ax.plot(phis, comp[:, i], "o-", markersize=3, label=especie)
    ax.axvline(1.0, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Razón de equivalencia $\\phi$ (pobre < 1 < rico)")
    ax.set_ylabel("Fracción molar")
    ax.set_title(f"CH$_4$/aire vs. $\\phi$ (T = {T_fijo:.0f} K, p = 1 atm)")
    ax.legend()
    _guardar(fig, "04_CH4_aire_vs_phi.png")


def fig_5_CH4_vs_P():
    presiones = np.linspace(1.0, 40.0, 20)
    T_fijo, phi_fijo = 2200.0, 1.0
    b = cg.feed_llama(phi=phi_fijo)
    comp = []
    n_prev, lam_prev = None, None
    for p in presiones:
        n, lam = cg.resolver_combustion(cg.A_LLAMA, b, cg.ESPECIES_LLAMA, T_fijo, p=p,
                                          n_t_guess=np.sum(b) / 3,
                                          n0_prev=n_prev, lam0_prev=lam_prev)
        comp.append(n / np.sum(n))
        n_prev, lam_prev = n, lam
    comp = np.array(comp)

    fig, ax = plt.subplots(figsize=(7, 5))
    for especie in ["CO", "H2", "O2", "NO", "OH", "H", "O"]:
        i = cg.ESPECIES_LLAMA.index(especie)
        ax.plot(presiones, comp[:, i], "-", linewidth=2, label=especie)
    ax.set_yscale("log")
    ax.set_xlabel("Presión (atm)")
    ax.set_ylabel("Fracción molar (especies traza)")
    ax.set_title(f"CH$_4$/aire vs. presión (T = {T_fijo:.0f} K, $\\phi$=1):\n"
                  "la disociación se suprime al aumentar P (Le Chatelier)")
    ax.legend(ncol=2, fontsize=8)
    _guardar(fig, "05_CH4_aire_vs_P.png")


# ===========================================================================
# 6. Combustion H2/aire vs phi
# ===========================================================================

def fig_6_H2_vs_phi():
    phis = np.linspace(0.5, 1.6, 23)
    T_fijo = 2200.0
    comp = _barrido_phi(cg.A_H2_AIRE, cg.ESPECIES_H2_AIRE, cg.feed_H2_aire, phis, T_fijo)

    fig, ax = plt.subplots(figsize=(7, 5))
    for especie in cg.ESPECIES_H2_AIRE:
        if especie == "N2":
            continue
        i = cg.ESPECIES_H2_AIRE.index(especie)
        ax.plot(phis, comp[:, i], "o-", markersize=3, label=especie)
    ax.axvline(1.0, color="gray", linestyle=":", linewidth=1)
    ax.set_yscale("log")
    ax.set_xlabel("Razón de equivalencia $\\phi$ (pobre < 1 < rico)")
    ax.set_ylabel("Fracción molar (escala log, excl. N$_2$)")
    ax.set_title(f"H$_2$/aire vs. $\\phi$ (T = {T_fijo:.0f} K, p = 1 atm)\n"
                  "combustible sin carbono: no hay CO/CO$_2$")
    ax.legend(ncol=2, fontsize=8)
    _guardar(fig, "06_H2_aire_vs_phi.png")


# ===========================================================================
# 7. Combustion C3H8 (propano)/aire vs phi
# ===========================================================================

def fig_7_propano_vs_phi():
    phis = np.linspace(0.5, 1.6, 23)
    T_fijo = 2200.0
    comp = _barrido_phi(cg.A_LLAMA, cg.ESPECIES_LLAMA, cg.feed_propano, phis, T_fijo)

    fig, ax = plt.subplots(figsize=(7, 5))
    for especie in ["CO2", "H2O", "CO", "H2", "O2", "NO"]:
        i = cg.ESPECIES_LLAMA.index(especie)
        ax.plot(phis, comp[:, i], "o-", markersize=3, label=especie)
    ax.axvline(1.0, color="gray", linestyle=":", linewidth=1)
    ax.set_xlabel("Razón de equivalencia $\\phi$ (pobre < 1 < rico)")
    ax.set_ylabel("Fracción molar")
    ax.set_title(f"C$_3$H$_8$ (propano)/aire vs. $\\phi$ (T = {T_fijo:.0f} K, p = 1 atm)")
    ax.legend()
    _guardar(fig, "07_propano_aire_vs_phi.png")


# ===========================================================================
# 8. Water-gas shift: CO + H2O <-> CO2 + H2
# ===========================================================================

def fig_8_water_gas_shift():
    temperaturas = np.linspace(400, 1300, 25)
    b = cg.A_WGS @ cg.feed_WGS(1.0, 1.0)
    comp = _barrido_T(cg.A_WGS, cg.ESPECIES_WGS, b, temperaturas, n_t_guess=1.0)

    # Con alimentacion equimolar CO:H2O=1:1 y sin CO2/H2 inicial, la
    # estequiometria 1:1:1:1 de la reaccion impone una simetria EXACTA:
    # CO(T)=H2O(T) y CO2(T)=H2(T) en todo punto. Se usan estilos de
    # linea distintos (no solo color) para que ambas curvas de cada
    # par sean visibles aunque se superpongan perfectamente.
    estilos = {"CO": "-", "H2O": "--", "CO2": "-", "H2": "--"}
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for i, especie in enumerate(cg.ESPECIES_WGS):
        ax.plot(temperaturas, comp[:, i], estilos[especie], linewidth=2.5, label=especie)
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar")
    ax.set_title("Water-gas shift: CO + H$_2$O ⇌ CO$_2$ + H$_2$\n"
                  "(alimentación equimolar CO:H$_2$O = 1:1, p = 1 atm)")
    ax.legend()
    ax.text(0.02, 0.02, "CO≡H$_2$O y CO$_2$≡H$_2$ por simetría exacta\n"
                          "de la alimentación equimolar 1:1",
            transform=ax.transAxes, fontsize=8, style="italic",
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="#cccccc"))
    _guardar(fig, "08_water_gas_shift.png")


# ===========================================================================
# 9. NOx vs T, familia de curvas a varios phi
# ===========================================================================

def fig_9_NOx_familia():
    temperaturas = np.linspace(1600, 2800, 20)
    fig, ax = plt.subplots(figsize=(7, 5))
    i_NO = cg.ESPECIES_LLAMA.index("NO")
    for phi, color in zip([0.8, 0.9, 1.0, 1.1, 1.2],
                            ["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd"]):
        b = cg.feed_llama(phi=phi)
        comp = _barrido_T(cg.A_LLAMA, cg.ESPECIES_LLAMA, b, temperaturas, n_t_guess=np.sum(b) / 3)
        ax.plot(temperaturas, comp[:, i_NO], "-", color=color, linewidth=2, label=f"$\\phi$={phi}")
    ax.set_yscale("log")
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar de NO")
    ax.set_title("NO térmico vs. T a varias razones de equivalencia\n"
                  "(a T fija: más NO cuanto más pobre la mezcla, por mayor O$_2$ libre)")
    ax.legend()
    ax.text(0.02, 0.02,
            "Nota: aquí T se fija externamente (no es la T de llama\n"
            "adiabática real, que sí varía con $\\phi$ y por sí sola\n"
            "favorecería $\\phi$≈1). A T fija domina solo el efecto\n"
            "de disponibilidad de O$_2$, de ahí la tendencia monótona.",
            transform=ax.transAxes, fontsize=7.5, style="italic",
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85, edgecolor="#cccccc"))
    _guardar(fig, "09_NOx_familia_vs_T.png")


# ===========================================================================
# 10. Comparacion de NOx entre 3 combustibles vs T (phi=1)
# ===========================================================================

def fig_10_comparacion_combustibles_NOx():
    temperaturas = np.linspace(1600, 2800, 20)

    b_ch4 = cg.feed_llama(phi=1.0)
    comp_ch4 = _barrido_T(cg.A_LLAMA, cg.ESPECIES_LLAMA, b_ch4, temperaturas, n_t_guess=np.sum(b_ch4) / 3)

    b_c3h8 = cg.feed_propano(phi=1.0)
    comp_c3h8 = _barrido_T(cg.A_LLAMA, cg.ESPECIES_LLAMA, b_c3h8, temperaturas, n_t_guess=np.sum(b_c3h8) / 3)

    comp_h2 = []
    n_prev, lam_prev = None, None
    for T in temperaturas:
        b_h2 = cg.feed_H2_aire(phi=1.0)
        n, lam = cg.resolver_combustion(cg.A_H2_AIRE, b_h2, cg.ESPECIES_H2_AIRE, T,
                                          n_t_guess=np.sum(b_h2) / 3,
                                          n0_prev=n_prev, lam0_prev=lam_prev)
        comp_h2.append(n / np.sum(n))
        n_prev, lam_prev = n, lam
    comp_h2 = np.array(comp_h2)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(temperaturas, comp_ch4[:, cg.ESPECIES_LLAMA.index("NO")], "-", linewidth=2, label="CH$_4$/aire")
    ax.plot(temperaturas, comp_c3h8[:, cg.ESPECIES_LLAMA.index("NO")], "-", linewidth=2, label="C$_3$H$_8$/aire")
    ax.plot(temperaturas, comp_h2[:, cg.ESPECIES_H2_AIRE.index("NO")], "-", linewidth=2, label="H$_2$/aire")
    ax.set_yscale("log")
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar de NO")
    ax.set_title("Comparación de NO térmico entre combustibles\n"
                  "($\\phi$=1, p=1 atm, mismo mecanismo de Zeldovich subyacente)")
    ax.legend()
    _guardar(fig, "10_comparacion_combustibles_NOx.png")


# ===========================================================================
if __name__ == "__main__":
    print("Generando perfiles de combustion en", os.path.abspath(DIR_FIGURAS))
    print("\n[1/10] Disociacion de CO2 vs T...")
    fig_1_disociacion_CO2()
    print("[2/10] Disociacion de H2O vs T...")
    fig_2_disociacion_H2O()
    print("[3/10] CH4/aire vs T (phi=1)...")
    fig_3_CH4_vs_T()
    print("[4/10] CH4/aire vs phi...")
    fig_4_CH4_vs_phi()
    print("[5/10] CH4/aire vs P...")
    fig_5_CH4_vs_P()
    print("[6/10] H2/aire vs phi...")
    fig_6_H2_vs_phi()
    print("[7/10] Propano/aire vs phi...")
    fig_7_propano_vs_phi()
    print("[8/10] Water-gas shift vs T...")
    fig_8_water_gas_shift()
    print("[9/10] Familia NOx vs T (varios phi)...")
    fig_9_NOx_familia()
    print("[10/10] Comparacion de combustibles (NOx)...")
    fig_10_comparacion_combustibles_NOx()
    print("\nListo: 10 perfiles de combustion generados.")
