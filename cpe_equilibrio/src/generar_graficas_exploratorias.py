"""
generar_graficas_exploratorias.py
====================================

Generacion EXTENSIVA de graficas termodinamicas a partir de los
solvers ya validados (resolver_lagrange, resolver_rand_modificado) y
de calculos clasicos de punto de burbuja/rocio y equilibrio liquido-
liquido. A pedido explicito del usuario, estas graficas son
EXPLORATORIAS -- "quiero ver que arroja el modelo" -- y NO se someten
a la suite de validacion cuantitativa (pruebas_validacion.py). No se
modifica ningun archivo ya validado.

Sistemas cubiertos:
  A. VLE binario no reactivo: etanol-agua (UNIFAC)          -> 3 figuras
  B. LLE binario (solucion regular con UCST ilustrativo)     -> 1 figura
  C. CPE reactivo: sintesis de MTBE                          -> 4 figuras
  D. CPE reactivo: esterificacion acido acetico/etanol       -> 2 figuras
  E. Combustion/oxidacion (potenciales de elemento, Gibbs)   -> 4 figuras

Total: 14 figuras, guardadas en docs/figuras_exploratorias/.

Ejecutar con:  python generar_graficas_exploratorias.py
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import diagramas_binarios as db
import diagramas_reactivos as dr
import combustion_gibbs as cg
import ejemplo_mtbe as mtbe
from estilo_graficas import aplicar_estilo_profesional

aplicar_estilo_profesional()

DIR_FIGURAS = os.path.join(os.path.dirname(__file__), "..", "docs", "figuras_exploratorias")
os.makedirs(DIR_FIGURAS, exist_ok=True)
DPI = 300


def _guardar(fig, nombre):
    ruta = os.path.join(DIR_FIGURAS, nombre)
    fig.savefig(ruta, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  guardado: {ruta}")


# ===========================================================================
# A. VLE binario no reactivo: etanol(1) - agua(2), UNIFAC
# ===========================================================================

def fig_A1_Txy_etanol_agua():
    x1 = np.concatenate([[0.001], np.linspace(0.02, 0.98, 35), [0.999]])
    T_burb, y1 = [], []
    for x in x1:
        T = db.bubble_T_etanol_agua(x, 1.0)
        T_burb.append(T)
        y1.append(db.y_desde_bubble(x, T, 1.0))
    T_burb, y1 = np.array(T_burb), np.array(y1)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(x1, T_burb, "-", color="#1f77b4", label="líquido (burbuja), x$_1$")
    ax.plot(y1, T_burb, "-", color="#d62728", label="vapor (rocío), y$_1$")
    i_az = np.argmin(T_burb)
    ax.plot(x1[i_az], T_burb[i_az], "k*", markersize=12,
            label=f"azeótropo ≈ {x1[i_az]:.2f} ({T_burb[i_az]:.1f} K)")
    ax.set_xlabel("Fracción molar de etanol")
    ax.set_ylabel("Temperatura (K)")
    ax.set_title("Diagrama T-x-y: etanol(1)-agua(2) a 1 atm (UNIFAC)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _guardar(fig, "A1_Txy_etanol_agua.png")


def fig_A2_Pxy_etanol_agua():
    T_fijo = 350.0
    x1 = np.linspace(0.001, 0.999, 40)
    P_burb = np.array([db.bubble_P_etanol_agua(x, T_fijo) for x in x1])
    y1 = np.array([
        x * (gammas := db.gammas_etanol_agua(x, T_fijo))[0] * db.psat_etanol(T_fijo) / P_burb[i]
        for i, x in enumerate(x1)
    ])

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(x1, P_burb, "-", color="#1f77b4", label="líquido (burbuja), x$_1$")
    ax.plot(y1, P_burb, "-", color="#d62728", label="vapor (rocío), y$_1$")
    ax.set_xlabel("Fracción molar de etanol")
    ax.set_ylabel("Presión (atm)")
    ax.set_title(f"Diagrama P-x-y: etanol(1)-agua(2) a T={T_fijo:.0f} K (UNIFAC)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _guardar(fig, "A2_Pxy_etanol_agua.png")


def fig_A3_xy_etanol_agua():
    x1 = np.linspace(0.001, 0.999, 40)
    y1 = []
    for x in x1:
        T = db.bubble_T_etanol_agua(x, 1.0)
        y1.append(db.y_desde_bubble(x, T, 1.0))
    y1 = np.array(y1)

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.plot(x1, y1, "-", color="#1f77b4", linewidth=2, label="equilibrio y$_1$ vs x$_1$")
    ax.plot([0, 1], [0, 1], "k--", linewidth=0.8, label="diagonal y=x")
    i_az = np.argmin(np.abs(y1 - x1))
    ax.plot(x1[i_az], y1[i_az], "r*", markersize=12, label="cruce con diagonal (azeótropo)")
    ax.set_xlabel("x$_1$ (líquido, etanol)")
    ax.set_ylabel("y$_1$ (vapor, etanol)")
    ax.set_title("Diagrama x-y: etanol(1)-agua(2) a 1 atm (UNIFAC)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _guardar(fig, "A3_xy_etanol_agua.png")


# ===========================================================================
# B. LLE binario (solucion regular, UCST ilustrativo)
# ===========================================================================

def fig_B1_LLE_binodal():
    Tc = db.T_critica_LLE()
    temperaturas = np.linspace(230.0, Tc - 0.5, 40)
    x_pobre, x_rica = [], []
    for T in temperaturas:
        resultado = db.binodal_LLE(T)
        x_pobre.append(resultado[0])
        x_rica.append(resultado[1])

    fig, ax = plt.subplots(figsize=(6, 5.5))
    ax.plot(x_pobre, temperaturas, "-", color="#1f77b4")
    ax.plot(x_rica, temperaturas, "-", color="#1f77b4")
    ax.fill_betweenx(temperaturas, x_pobre, x_rica, color="#1f77b4", alpha=0.15,
                      label="región de 2 fases líquidas (LLE)")
    ax.plot(0.5, Tc, "r*", markersize=14, label=f"punto crítico (UCST={Tc:.1f} K)")
    ax.set_xlabel("Fracción molar del componente 1")
    ax.set_ylabel("Temperatura (K)")
    ax.set_title("Domo de equilibrio líquido-líquido (solución regular,\n"
                  f"$\\Omega$={db.OMEGA_LLE:.0f} J/mol, ilustrativo)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    _guardar(fig, "B1_LLE_binodal.png")


# ===========================================================================
# C. CPE reactivo: sintesis de MTBE
# ===========================================================================

def fig_C1_Txy_mtbe():
    T, xl, xv, fv = dr.barrido_T_mtbe(0.80, 295.0, 345.0, n_puntos=45)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    colores = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for i, comp in enumerate(mtbe.COMPONENTES):
        liq_mask = fv < 0.999
        vap_mask = fv > 0.001
        ax.plot(T[liq_mask], xl[liq_mask, i], "-", color=colores[i],
                label=f"{comp} (líq.)")
        ax.plot(T[vap_mask], xv[vap_mask, i], "--", color=colores[i],
                label=f"{comp} (vap.)")
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar")
    ax.set_title("T-x-y con reacción: síntesis de MTBE a p = 0.80 bar")
    ax.legend(fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    _guardar(fig, "C1_Txy_mtbe.png")
    return T, xl, xv, fv


def fig_C2_conversion_mtbe(T, xl, xv, fv):
    # Isobuteno remanente en cada fase por separado (NO una mezcla
    # ponderada por fv: en la ventana angosta de coexistencia, fv es
    # muy sensible a T y una mezcla ponderada produce una curva en
    # diente de sierra que no refleja nada fisico, solo la sensibilidad
    # numerica del punto de corte liquido/vapor).
    liq_mask = fv < 0.999
    vap_mask = fv > 0.001
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(T[liq_mask], xl[liq_mask, 0], "o-", color="#1f77b4", markersize=4,
            label="isobuteno en líquido")
    ax.plot(T[vap_mask], xv[vap_mask, 0], "s-", color="#d62728", markersize=4,
            label="isobuteno en vapor")
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar de isobuteno")
    ax.set_title("Isobuteno remanente por fase vs. T\n(síntesis de MTBE, p = 0.80 bar)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _guardar(fig, "C2_isobuteno_vs_T_mtbe.png")


def fig_C3_ternario_mtbe(T, xl, xv, fv):
    fig, ax = plt.subplots(figsize=(6.5, 6))
    # Triangulo
    vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    ax.plot(vertices[:, 0], vertices[:, 1], "k-", linewidth=1)
    for frac, nombre in [(1, "isobuteno"), (0, "metanol")]:
        pass
    ax.text(-0.05, -0.03, "isobuteno", ha="right")
    ax.text(1.05, -0.03, "metanol", ha="left")
    ax.text(0.5, np.sqrt(3) / 2 + 0.02, "MTBE", ha="center")

    liq_mask = fv < 0.999
    vap_mask = fv > 0.001
    xL, yL = dr.proyeccion_ternaria(xl[liq_mask, 0], xl[liq_mask, 1], xl[liq_mask, 2])
    xV, yV = dr.proyeccion_ternaria(xv[vap_mask, 0], xv[vap_mask, 1], xv[vap_mask, 2])
    ax.plot(xL, yL, "o-", color="#1f77b4", markersize=3, label="líquido")
    ax.plot(xV, yV, "s-", color="#d62728", markersize=3, label="vapor")
    ax.set_title("Diagrama ternario: trayectoria de composición\n"
                  "(síntesis de MTBE, p = 0.80 bar, T: 295-345 K)")
    ax.legend()
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "C3_ternario_mtbe.png")


def fig_C4_fraccion_fase_vs_p_mtbe():
    p, xl, xv, fv = dr.barrido_p_mtbe(320.92, 0.3, 1.3, n_puntos=35)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(p, fv, "o-", color="#9467bd")
    ax.set_xlabel("Presión (bar)")
    ax.set_ylabel("Fracción molar de vapor")
    ax.set_title("Fracción de fase vapor vs. presión\n"
                  "(síntesis de MTBE, T = 320.92 K)")
    ax.grid(True, alpha=0.3)
    _guardar(fig, "C4_fraccion_vapor_vs_P_mtbe.png")


# ===========================================================================
# D. CPE reactivo: esterificacion acido acetico/etanol
# ===========================================================================

def fig_D1_fraccion_fase_vs_T_esterificacion():
    T, xl, xv, fv = dr.barrido_T_esterificacion_VLE(1.0, 345.0, 375.0, n_puntos=20)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.plot(T, fv, "o-", color="#9467bd")
    ax.set_xlabel("Temperatura (K)")
    ax.set_ylabel("Fracción molar de vapor")
    ax.set_title("Fracción de fase vapor vs. T (esterificación\n"
                  "ácido acético/etanol, p = 1 atm, UNIFAC)")
    ax.grid(True, alpha=0.3)
    _guardar(fig, "D1_fraccion_vapor_vs_T_esterificacion.png")
    return T, xl, xv, fv


def fig_D2_especies_vs_T_esterificacion(T, xl, xv, fv):
    # Igual que en fig_C2: solo se grafica cada fase donde realmente
    # existe (fv entre 0 y 1 estrictos); fuera de ese rango la fase
    # esta colapsada en el piso numerico y su "composicion" no es
    # fisicamente significativa.
    liq_mask = fv < 0.999
    vap_mask = fv > 0.001
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    colores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for i, comp in enumerate(ace_componentes()):
        ax1.plot(T[liq_mask], xl[liq_mask, i], "-", color=colores[i], label=comp)
        ax2.plot(T[vap_mask], xv[vap_mask, i], "-", color=colores[i], label=comp)
    ax1.set_title("Fase líquida")
    ax2.set_title("Fase vapor")
    for ax in (ax1, ax2):
        ax.set_xlabel("Temperatura (K)")
        ax.grid(True, alpha=0.3)
    ax1.set_ylabel("Fracción molar")
    ax1.legend(fontsize=8)
    fig.suptitle("Composición vs. T: esterificación ácido acético/etanol\n"
                 "(p = 1 atm, UNIFAC)", y=1.02)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    _guardar(fig, "D2_especies_vs_T_esterificacion.png")


def ace_componentes():
    import ejemplo_acetic_etanol as ace
    return ace.COMPONENTES


# ===========================================================================
# E. Combustion / oxidacion (potenciales de elemento)
# ===========================================================================

# NOTA: las figuras de combustion/oxidacion (antes E1-E4 en este
# archivo) se movieron a generar_perfiles_combustion.py, que cubre un
# conjunto mucho mas extenso de perfiles de concentracion de
# combustion (ver ese archivo y docs/figuras_combustion/).


# ===========================================================================
if __name__ == "__main__":
    print("Generando graficas exploratorias en", os.path.abspath(DIR_FIGURAS))

    print("\n[A] VLE binario etanol-agua (UNIFAC)...")
    fig_A1_Txy_etanol_agua()
    fig_A2_Pxy_etanol_agua()
    fig_A3_xy_etanol_agua()

    print("\n[B] LLE binario (solucion regular)...")
    fig_B1_LLE_binodal()

    print("\n[C] CPE reactivo: MTBE...")
    T, xl, xv, fv = fig_C1_Txy_mtbe()
    fig_C2_conversion_mtbe(T, xl, xv, fv)
    fig_C3_ternario_mtbe(T, xl, xv, fv)
    fig_C4_fraccion_fase_vs_p_mtbe()

    print("\n[D] CPE reactivo: esterificacion...")
    T2, xl2, xv2, fv2 = fig_D1_fraccion_fase_vs_T_esterificacion()
    fig_D2_especies_vs_T_esterificacion(T2, xl2, xv2, fv2)

    print("\nListo: 10 figuras generadas (A-D). Para combustion, ver")
    print("generar_perfiles_combustion.py")
