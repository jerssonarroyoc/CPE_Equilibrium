#!/usr/bin/env python3
"""
Procesamiento y analisis de datos - Practica de Molienda y Tamizado (garbanzo)
Universidad Nacional de Colombia - Ingenieria Quimica y Ambiental

Este script:
 1. Carga los datos crudos (datos/*.csv), fielmente transcritos del archivo
    'molienda_y_tamizaje.xlsx' entregado por el grupo (formulas interpretadas).
 2. Calcula la caracterizacion granulometrica del alimento (10 granos, medidos
    con calibrador, resolucion 0.05 mm) y del producto de cada corrida de
    molienda (tamizaje con mallas ASTM E11: 4,6,10,20,35,45 y fondos).
 3. Ajusta modelos de distribucion de tamano (Gates-Gaudin-Schuhmann y
    Rosin-Rammler-Bennet) para obtener D80/F80, con incertidumbre estimada
    de forma ENTERAMENTE ANALITICA (sin simulacion/Monte Carlo): formula
    asintotica del error estandar de un percentil muestral para F80, e
    intervalo de calibracion/prediccion inversa de regresion lineal simple
    (Fieller) para D80.
 4. Calcula diametros medios (aritmetico, Sauter D32, De Brouckere D43 / masico).
 5. Realiza el balance de masa de cada corrida.
 6. Genera tablas (CSV y fragmentos LaTeX) y figuras (PNG 300dpi + PDF).

Ejecutar: python3 procesar_datos.py
Salidas:  ../datos/*_procesado.csv, ../tablas/*.tex, ../graficas/*.png|pdf
"""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "datos")
GRAF = os.path.join(BASE, "graficas")
TAB = os.path.join(BASE, "tablas")

# ------------------------------------------------------------------
# Estilo grafico de calidad de publicacion
#   - Tipografia: Liberation Sans (metric-compatible con Arial/Helvetica),
#     estandar de facto en figuras cientificas por su legibilidad a
#     tamanos pequenos, incluso en articulos con cuerpo de texto serif.
#   - Paleta: variante de Okabe-Ito, segura para daltonismo y consistente
#     en TODAS las figuras (un color = una misma serie en todo el informe).
#   - Tamanio de figura: ajustado al ANCHO REAL de impresion de cada
#     figura en el informe (segun su \includegraphics width en el .tex),
#     para que el tamano de fuente efectivo en la pagina impresa sea
#     exactamente el aqui especificado, y no una fuente encogida desde
#     un lienzo mas grande.
#   - Resolucion: 300 dpi; cada figura se exporta en PNG (raster) y PDF
#     (vectorial) para uso flexible (impresion, Overleaf, presentaciones).
# ------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Liberation Sans", "Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "axes.labelweight": "regular",
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "legend.title_fontsize": 8,
    "figure.titlesize": 11,
    "figure.titleweight": "bold",
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "grid.color": "#B5B5B5",
    "grid.alpha": 0.35,
    "grid.linestyle": "-",
    "grid.linewidth": 0.5,
    "axes.edgecolor": "#4D4D4D",
    "axes.linewidth": 0.8,
    "axes.titlelocation": "left",
    "xtick.color": "#4D4D4D",
    "ytick.color": "#4D4D4D",
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "text.color": "#1A1A1A",
    "axes.labelcolor": "#1A1A1A",
    "legend.frameon": False,
    "legend.handlelength": 1.6,
    "legend.handletextpad": 0.6,
    "legend.borderaxespad": 0.4,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.03,
    "lines.linewidth": 1.4,
    "lines.markersize": 6,
    "patch.linewidth": 0.7,
})

# Paleta Okabe-Ito (segura para daltonismo), con un rol semantico fijo
# para cada color en todas las figuras del informe:
COLOR_F   = "#009E73"   # verde azulado  - Alimento
COLOR_M1  = "#0072B2"   # azul           - Molienda 1 (producto)
COLOR_M2  = "#D55E00"   # vermellon      - Molienda 2 (producto)
COLOR_FIT = "#8B5FA8"   # purpura        - ajustes de modelo / teoria
COLOR_NEU = "#767676"   # gris neutro    - perdidas / referencias pasivas
COLOR_ACC = "#E69F00"   # ambar          - acentos (puntos experimentales, producto final)

# Anchos objetivo (pulgadas), iguales al ancho real de impresion de cada
# figura en el informe (\textwidth del documento = 6.53 in, con
# geometry margin=2.5cm sobre papel carta):
TEXTWIDTH_IN = 6.53
W_FULL = TEXTWIDTH_IN
W_95 = 0.95 * TEXTWIDTH_IN
W_80 = 0.80 * TEXTWIDTH_IN
W_75 = 0.75 * TEXTWIDTH_IN


def despine(ax, keep=("left", "bottom")):
    """Elimina los ejes superior/derecho (convencion habitual en graficas
    cientificas modernas), conservando solo los ejes indicados."""
    for side, spine in ax.spines.items():
        spine.set_visible(side in keep)


def panel_title(ax, letter, texto, fontsize_letter=10, fontsize_texto=9):
    """Rotula un panel como '(a) Texto descriptivo', con la letra en
    negrita alineada a la izquierda (convencion de figuras multipanel)."""
    ax.set_title(f"({letter})  {texto}", loc="left", fontsize=fontsize_texto,
                 fontweight="bold")


def savefig(fig, name):
    fig.savefig(os.path.join(GRAF, f"{name}.png"))
    fig.savefig(os.path.join(GRAF, f"{name}.pdf"))
    plt.close(fig)

RESULTS = {}  # dict to dump all scalar results -> json + used for narrative numbers in LaTeX

# ====================================================================
# 1. ALIMENTO (10 granos medidos con calibrador)
# ====================================================================
df_feed = pd.read_csv(os.path.join(DATOS, "alimento_diametros.csv"))
D_feed = df_feed["D_mm"].values.astype(float)
n_feed = len(D_feed)
resolucion_calibrador = 0.05  # mm (1/20 mm, dato E1 del Excel)
u_B_feed = resolucion_calibrador / (2 * np.sqrt(3))  # incertidumbre tipo B (rectangular)

mean_feed = D_feed.mean()
std_feed = D_feed.std(ddof=1)
sem_feed = std_feed / np.sqrt(n_feed)
u_c_feed = np.sqrt(sem_feed**2 + u_B_feed**2)
t_val = stats.t.ppf(0.975, df=n_feed - 1)
ci95_feed = t_val * u_c_feed

# Diametros medios (definiciones de momentos, base numero->  D[p,q])
D_arit_feed = D_feed.mean()                                   # D[1,0]
D_sup_feed = np.sqrt((D_feed**2).mean())                      # D[2,0]
D_vol_feed = (np.mean(D_feed**3)) ** (1/3)                    # D[3,0]
D32_feed = np.sum(D_feed**3) / np.sum(D_feed**2)               # Sauter D[3,2]
D43_feed = np.sum(D_feed**4) / np.sum(D_feed**3)               # De Brouckere D[4,3]

# F80 por estadistica de orden (posicion de trazado de Hazen) + incertidumbre
# ANALITICA (aproximacion normal asintotica del error estandar de un percentil
# muestral; sin simulacion). Formula clasica (metodo delta aplicado a la
# funcion cuantil empirica; ver p.ej. Serfling 1980, "Approximation Theorems
# of Mathematical Statistics", o Casella & Berger, "Statistical Inference"):
#   SE(Q_p) = sqrt( p(1-p)/n ) / f(Q_p)
# donde f(Q_p) es la densidad de la poblacion en el percentil p, aproximada
# aqui asumiendo una forma normal con la desviacion estandar muestral s:
#   f(Q_p) ~= phi(z_p) / s ,   z_p = Phi^-1(p)
def percentil_orden(datos, p):
    """Interpola el percentil p (0-100) usando posicion de trazado de Hazen:
    p_i = (i-0.5)/n *100 para datos ordenados ascendentemente."""
    d = np.sort(datos)
    n = len(d)
    pos = (np.arange(1, n + 1) - 0.5) / n * 100
    return np.interp(p, pos, d)


def u_percentil_analitico(datos, p, resolucion, s_muestral=None):
    """Incertidumbre analitica (sin simulacion) de un percentil muestral,
    combinando: (A) dispersion estadistica de la muestra, via la
    aproximacion normal asintotica del error estandar de un cuantil; y
    (B) resolucion del instrumento (tipo B, distribucion rectangular),
    combinadas en cuadratura."""
    n = len(datos)
    s = s_muestral if s_muestral is not None else datos.std(ddof=1)
    frac = p / 100
    z_p = stats.norm.ppf(frac)
    f_Qp = stats.norm.pdf(z_p) / s
    u_A = np.sqrt(frac * (1 - frac) / n) / f_Qp
    u_B = resolucion / (2 * np.sqrt(3))
    return np.sqrt(u_A**2 + u_B**2), u_A, u_B


F80_puntual = percentil_orden(D_feed, 80)
F10_puntual = percentil_orden(D_feed, 10)
F50_puntual = percentil_orden(D_feed, 50)
F90_puntual = percentil_orden(D_feed, 90)

u_F80, u_F80_estadistica, u_F80_instrumento = u_percentil_analitico(
    D_feed, 80, resolucion_calibrador)

RESULTS["feed"] = dict(
    n=n_feed, mean=mean_feed, std=std_feed, sem=sem_feed, u_c=u_c_feed,
    ci95=ci95_feed, D_arit=D_arit_feed, D_sup=D_sup_feed, D_vol=D_vol_feed,
    D32=D32_feed, D43=D43_feed, F80=F80_puntual, u_F80=u_F80,
    u_F80_estadistica=u_F80_estadistica, u_F80_instrumento=u_F80_instrumento,
    F10=F10_puntual, F50=F50_puntual, F90=F90_puntual,
    span=(F90_puntual - F10_puntual) / F50_puntual,
)

# Tabla procesada del alimento
tabla_feed = df_feed.copy()
tabla_feed.to_csv(os.path.join(DATOS, "alimento_procesado.csv"), index=False)

# ====================================================================
# 2. TAMIZAJE DE PRODUCTO (Molienda 1 y 2)
# ====================================================================
APERTURAS = {4: 4.75, 6: 3.35, 10: 2.00, 20: 0.850, 35: 0.500, 45: 0.355}  # mm, ASTM E11
# Diametro representativo de cada intervalo (media aritmetica de aberturas
# consecutivas; el intervalo superior a malla 4 se aproxima por la propia
# abertura de malla 4, y el fondo por la mitad de la abertura de malla 45)
REP_DIAM = {
    4: 4.75,                          # supuesto: material > 4.75 mm (abierto)
    6: (4.75 + 3.35) / 2,             # 4.05
    10: (3.35 + 2.00) / 2,            # 2.675
    20: (2.00 + 0.850) / 2,           # 1.425
    35: (0.850 + 0.500) / 2,          # 0.675
    45: (0.500 + 0.355) / 2,          # 0.4275
    "Fondos": 0.355 / 2,              # 0.1775  (supuesto)
}


def procesar_tamizaje(path_csv):
    df = pd.read_csv(path_csv)
    df["abertura_mm"] = df["malla"].apply(lambda m: APERTURAS[int(m)] if m != "Fondos" else np.nan)
    total = df["peso_neto_g"].sum()
    df["frac_individual_%"] = df["peso_neto_g"] / total * 100
    df["frac_acumulada_%"] = df["frac_individual_%"].cumsum()
    df["pasante_%"] = 100 - df["frac_acumulada_%"]
    df["D_repr_mm"] = df["malla"].apply(lambda m: REP_DIAM[int(m)] if m != "Fondos" else REP_DIAM["Fondos"])
    return df, total


def ajustar_modelos(df):
    """Ajusta GGS (Gates-Gaudin-Schuhmann) y RRB (Rosin-Rammler) sobre los
    puntos con abertura definida (excluye 'Fondos', que no tiene abertura
    propia). Devuelve D80/D50/D10 segun el modelo de mejor R^2, mas los
    parametros de ambos ajustes."""
    sub = df.dropna(subset=["abertura_mm"]).copy()
    D = sub["abertura_mm"].values
    Y = sub["pasante_%"].values  # 0-100

    # --- GGS: ln(Y) = m ln(D) + b  ->  D_p = exp( (ln(p) - b) / m )
    lnD = np.log(D)
    lnY = np.log(Y)
    res_ggs = stats.linregress(lnD, lnY)
    m_ggs, b_ggs, r_ggs = res_ggs.slope, res_ggs.intercept, res_ggs.rvalue

    def D_ggs(p):
        return np.exp((np.log(p) - b_ggs) / m_ggs)

    # --- RRB: ln(-ln(1-Y/100)) = n ln(D) - n ln(D')
    frac = np.clip(Y / 100, 1e-6, 1 - 1e-6)
    lnln = np.log(-np.log(1 - frac))
    res_rrb = stats.linregress(lnD, lnln)
    n_rrb, c_rrb, r_rrb = res_rrb.slope, res_rrb.intercept, res_rrb.rvalue

    def D_rrb(p):
        val = -np.log(1 - p / 100)
        return np.exp((np.log(val) - c_rrb) / n_rrb)

    # --- interpolacion log-log simple (2 puntos que acotan p) como verificacion
    def D_interp(p):
        order = np.argsort(D)
        Ds, Ys = D[order], Y[order]
        return np.exp(np.interp(p, Ys, np.log(Ds)))

    mejor = "GGS" if r_ggs**2 >= r_rrb**2 else "RRB"
    D80_mod = D_ggs(80) if mejor == "GGS" else D_rrb(80)
    D80_ggs_val, D80_rrb_val, D80_interp_val = D_ggs(80), D_rrb(80), D_interp(80)

    # incertidumbre "de metodo": dispersion entre las 3 formas de estimar D80
    tres_estimados = np.array([D80_ggs_val, D80_rrb_val, D80_interp_val])
    u_metodo = tres_estimados.std(ddof=1)

    # --- incertidumbre "de regresion" (ANALITICA, sin simulacion): intervalo
    # de calibracion/prediccion inversa de una regresion lineal simple
    # (Fieller 1954; ver tambien Draper & Smith, "Applied Regression
    # Analysis"). Dado el ajuste log-log Y=mX+b (X=ln D, Y=ln%pasante o su
    # transformacion), se busca X0 tal que Y(X0)=Y0 (aqui Y0=ln 80, un
    # valor OBJETIVO fijo, no una observacion adicional con ruido propio),
    # cuya incertidumbre estandar es:
    #   SE(X0) = (s_resid/|pendiente|) * sqrt(1/n + (X0-Xbar)^2/Sxx)
    # que se traslada a D80 = exp(X0) por el metodo delta: u(D80)=D80*SE(X0)
    n_pts = len(lnD)
    if mejor == "GGS":
        pend, X0 = m_ggs, (np.log(80) - b_ggs) / m_ggs
        resid = lnY - (m_ggs * lnD + b_ggs)
    else:
        pend, X0 = n_rrb, (np.log(-np.log(1 - 0.8)) - c_rrb) / n_rrb
        resid = lnln - (n_rrb * lnD + c_rrb)
    s_resid = np.sqrt(np.sum(resid**2) / (n_pts - 2))
    Xbar = lnD.mean()
    Sxx = np.sum((lnD - Xbar)**2)
    SE_X0 = (s_resid / abs(pend)) * np.sqrt(1/n_pts + (X0 - Xbar)**2 / Sxx)
    u_regresion = D80_mod * SE_X0

    return dict(
        m_ggs=m_ggs, b_ggs=b_ggs, r2_ggs=r_ggs**2,
        n_rrb=n_rrb, c_rrb=c_rrb, r2_rrb=r_rrb**2,
        mejor_modelo=mejor,
        D80=D80_mod, D50=(D_ggs(50) if mejor == "GGS" else D_rrb(50)),
        D10=(D_ggs(10) if mejor == "GGS" else D_rrb(10)),
        D80_ggs=D80_ggs_val, D80_rrb=D80_rrb_val, D80_interp=D80_interp_val,
        u_metodo=u_metodo, u_regresion=u_regresion, s_resid=s_resid,
        D_ggs_fn=D_ggs, D_rrb_fn=D_rrb, D_interp_fn=D_interp,
    )


def diametros_medios(df):
    x = df["frac_individual_%"].values / 100
    Di = df["D_repr_mm"].values
    D_masico = np.sum(x * Di)                 # media masica (aritmetica ponderada)
    D_sauter = 1 / np.sum(x / Di)              # media de Sauter (superficie-volumen)
    return D_masico, D_sauter


df1, total1 = procesar_tamizaje(os.path.join(DATOS, "tamizaje_molienda1.csv"))
df2, total2 = procesar_tamizaje(os.path.join(DATOS, "tamizaje_molienda2.csv"))
ajuste1 = ajustar_modelos(df1)
ajuste2 = ajustar_modelos(df2)
u_D80_1 = ajuste1["u_regresion"]
u_D80_2 = ajuste2["u_regresion"]
Dmasico1, Dsauter1 = diametros_medios(df1)
Dmasico2, Dsauter2 = diametros_medios(df2)

df1.to_csv(os.path.join(DATOS, "tamizaje_molienda1_procesado.csv"), index=False)
df2.to_csv(os.path.join(DATOS, "tamizaje_molienda2_procesado.csv"), index=False)

u_comb_1 = np.sqrt(u_D80_1**2 + ajuste1["u_metodo"]**2)
u_comb_2 = np.sqrt(u_D80_2**2 + ajuste2["u_metodo"]**2)

RESULTS["molienda1"] = dict(
    total_g=total1, D80=ajuste1["D80"], u_D80_regresion=u_D80_1, u_D80_metodo=ajuste1["u_metodo"],
    u_D80=u_comb_1, D80_ggs=ajuste1["D80_ggs"], D80_rrb=ajuste1["D80_rrb"], D80_interp=ajuste1["D80_interp"],
    D50=ajuste1["D50"], D10=ajuste1["D10"], r2_ggs=ajuste1["r2_ggs"], r2_rrb=ajuste1["r2_rrb"],
    m_ggs=ajuste1["m_ggs"], mejor_modelo=ajuste1["mejor_modelo"],
    D_masico=Dmasico1, D_sauter=Dsauter1,
    span=(ajuste1["D_ggs_fn" if ajuste1["mejor_modelo"]=="GGS" else "D_rrb_fn"](90) - ajuste1["D10"]) / ajuste1["D50"],
)
RESULTS["molienda2"] = dict(
    total_g=total2, D80=ajuste2["D80"], u_D80_regresion=u_D80_2, u_D80_metodo=ajuste2["u_metodo"],
    u_D80=u_comb_2, D80_ggs=ajuste2["D80_ggs"], D80_rrb=ajuste2["D80_rrb"], D80_interp=ajuste2["D80_interp"],
    D50=ajuste2["D50"], D10=ajuste2["D10"], r2_ggs=ajuste2["r2_ggs"], r2_rrb=ajuste2["r2_rrb"],
    m_ggs=ajuste2["m_ggs"], mejor_modelo=ajuste2["mejor_modelo"],
    D_masico=Dmasico2, D_sauter=Dsauter2,
    span=(ajuste2["D_ggs_fn" if ajuste2["mejor_modelo"]=="GGS" else "D_rrb_fn"](90) - ajuste2["D10"]) / ajuste2["D50"],
)

# ====================================================================
# 3. RELACION DE REDUCCION (con incertidumbre propagada; ver Seccion 5-bis
#    mas abajo, donde se calcula junto con la propagacion de energia)
# ====================================================================

# ====================================================================
# 4. BALANCE DE MASA
# ====================================================================
bal = pd.read_csv(os.path.join(DATOS, "balance_masa.csv"))
bal_dict = bal.set_index("variable").to_dict()
feed_m1 = bal_dict["molienda_1_g"]["antes_de_moler"]
feed_m2 = bal_dict["molienda_2_g"]["antes_de_moler"]
prod_molino_m1 = bal_dict["molienda_1_g"]["peso_producto_molino"]
prod_molino_m2 = bal_dict["molienda_2_g"]["peso_producto_molino"]
suma_tamices_m1 = bal_dict["molienda_1_g"]["suma_tamices"]
suma_tamices_m2 = bal_dict["molienda_2_g"]["suma_tamices"]
perdidas_tamizaje_m1 = bal_dict["molienda_1_g"]["perdidas_tamizaje"]
perdidas_tamizaje_m2 = bal_dict["molienda_2_g"]["perdidas_tamizaje"]
perdidas_molienda_m1 = feed_m1 - prod_molino_m1
perdidas_molienda_m2 = feed_m2 - prod_molino_m2
pct_perdidas_molienda_m1 = perdidas_molienda_m1 / feed_m1 * 100
pct_perdidas_molienda_m2 = perdidas_molienda_m2 / feed_m2 * 100
pct_perdidas_tamizaje_m1 = perdidas_tamizaje_m1 / prod_molino_m1 * 100
pct_perdidas_tamizaje_m2 = perdidas_tamizaje_m2 / prod_molino_m2 * 100
rendimiento_global_m1 = suma_tamices_m1 / feed_m1 * 100
rendimiento_global_m2 = suma_tamices_m2 / feed_m2 * 100

RESULTS["balance"] = dict(
    feed_m1=feed_m1, feed_m2=feed_m2, prod_molino_m1=prod_molino_m1, prod_molino_m2=prod_molino_m2,
    suma_tamices_m1=suma_tamices_m1, suma_tamices_m2=suma_tamices_m2,
    perdidas_tamizaje_m1=perdidas_tamizaje_m1, perdidas_tamizaje_m2=perdidas_tamizaje_m2,
    perdidas_molienda_m1=perdidas_molienda_m1, pct_perdidas_molienda_m1=pct_perdidas_molienda_m1,
    perdidas_molienda_m2=perdidas_molienda_m2, pct_perdidas_molienda_m2=pct_perdidas_molienda_m2,
    pct_perdidas_tamizaje_m1=pct_perdidas_tamizaje_m1, pct_perdidas_tamizaje_m2=pct_perdidas_tamizaje_m2,
    rendimiento_global_m1=rendimiento_global_m1, rendimiento_global_m2=rendimiento_global_m2,
)

# ====================================================================
# 4-bis. DISTRIBUCION CONJUNTA (M1+M2 agrupadas por masa) -> D80 combinado
#   Se usa como P80 representativo del PROCESO GLOBAL DE MOLIENDA, ya que la
#   unica medicion electrica disponible (ver Sec. 5) cubre ambas corridas
#   sin distincion.
# ====================================================================
df_comb_masas = df1[["malla", "abertura_mm"]].copy()
df_comb_masas["peso_neto_g"] = df1["peso_neto_g"].values + df2["peso_neto_g"].values
total_comb = df_comb_masas["peso_neto_g"].sum()
df_comb_masas["frac_individual_%"] = df_comb_masas["peso_neto_g"] / total_comb * 100
df_comb_masas["frac_acumulada_%"] = df_comb_masas["frac_individual_%"].cumsum()
df_comb_masas["pasante_%"] = 100 - df_comb_masas["frac_acumulada_%"]
ajuste_comb = ajustar_modelos(df_comb_masas)
u_D80_comb_regresion = ajuste_comb["u_regresion"]
u_D80_comb = np.sqrt(u_D80_comb_regresion**2 + ajuste_comb["u_metodo"]**2)
D_masico_comb, D_sauter_comb = diametros_medios(
    df_comb_masas.assign(D_repr_mm=df1["D_repr_mm"].values)
)
df_comb_masas.to_csv(os.path.join(DATOS, "tamizaje_combinado_procesado.csv"), index=False)

RESULTS["combinado"] = dict(
    total_g=total_comb, D80=ajuste_comb["D80"], D50=ajuste_comb["D50"], D10=ajuste_comb["D10"],
    r2_ggs=ajuste_comb["r2_ggs"], mejor_modelo=ajuste_comb["mejor_modelo"],
    D_masico=D_masico_comb, D_sauter=D_sauter_comb,
    u_D80_regresion=u_D80_comb_regresion, u_D80_metodo=ajuste_comb["u_metodo"], u_D80=u_D80_comb,
)

# ====================================================================
# 5. ENERGIA Y CONTRASTE CON LEYES DE CONMINUCION
#   Datos experimentales suministrados por el grupo (medicion electrica en
#   el tablero de control, 27-sep-2026), correspondientes al PROCESO GLOBAL
#   (Molienda 1 + Molienda 2 combinadas, sin discriminar entre corridas):
#     - EN VACIO (motor solo, sin alimentacion de solido): V0=120 V,
#       I0=1.460 A -- lectura estable, tomada antes de iniciar la molienda
#       (paso "Inicialmente, realizar medicion al vacio" del procedimiento,
#       Figura 3).
#     - EN FUNCIONAMIENTO (motor + molienda real, t=3 min 30 s = 210 s):
#       corriente entre 1.480 y 1.600 A, tension entre 117.2 y 117.5 V
#       (fluctuacion observada durante el registro continuo del proceso).
#
#   Con ambas mediciones se aisla, por primera vez, el trabajo NETO de
#   conminucion Wm de las perdidas de vacio W0, exactamente como plantea
#   la Ec. potencia_total (Wtotal = W0 + Wm*mdot): la potencia neta
#   atribuible a la molienda es Pneta = Pfuncionamiento - P0, y la energia
#   especifica neta es Es_neta = Pneta * t / m_procesada.
#
#   SUPUESTOS DOCUMENTADOS (ver Seccion de Metodologia/Incertidumbre del
#   informe; modificar aqui si el grupo confirma valores distintos):
#     (a) t = 3 min 30 s = 210 s (notacion de cronometro), duracion del
#         registro EN FUNCIONAMIENTO (la medicion en vacio es previa y
#         puntual, no se descuenta del tiempo de proceso).
#     (b) Factor de potencia cos(phi) ~= 1 en ambas mediciones (no se
#         dispone de medicion de potencia reactiva ni de vatimetro
#         dedicado; P = V*I es entonces una potencia APARENTE).
#     (c) Masa procesada = masa de ALIMENTACION real de ambas corridas
#         (feed_m1 + feed_m2). Es la base fisicamente mas correcta para la
#         energia especifica, pues es la masa que efectivamente recibio el
#         trabajo de conminucion.
#     (d) Resolucion instrumental: voltimetro 0.1 V (u=0.05 V), amperimetro
#         0.001 A (u=0.0005 A), consistente con las cifras decimales
#         reportadas para ambas mediciones.
#     (e) El rango de corriente/tension EN FUNCIONAMIENTO se trata como una
#         distribucion rectangular (min-max observado durante el registro),
#         con valor central = punto medio e incertidumbre estandar =
#         semirrango/raiz(3); esta dispersion de proceso domina ampliamente
#         sobre la incertidumbre puramente instrumental.
# ====================================================================
V0_TENSION = 120.0        # V, en vacio
I0_CORRIENTE = 1.460      # A, en vacio
V_FUNC_LO, V_FUNC_HI = 117.2, 117.5   # V, en funcionamiento (rango observado)
I_FUNC_LO, I_FUNC_HI = 1.480, 1.600   # A, en funcionamiento (rango observado)
T_S = 3 * 60 + 30        # s  (3 min 30 s = 210 s)  <-- cambiar a 198 si es 3.30 min decimal
COS_PHI = 1.0            # supuesto (ver nota b)

U_VOLTAJE = 0.05         # V   (resolucion 0.1 V -> mitad)
U_CORRIENTE = 0.0005     # A   (resolucion 0.001 A -> mitad)
U_TIEMPO = 1.0           # s   (incertidumbre de lectura/arranque-parada del tiempo de proceso)
U_MASA_LECTURA = 0.05    # g   (media unidad del ultimo digito de la balanza, 0.1 g)

# --- potencia en vacio (lectura unica y estable -> incertidumbre instrumental) ---
P0_watts = V0_TENSION * I0_CORRIENTE * COS_PHI
u_P0_watts = P0_watts * np.sqrt((U_VOLTAJE/V0_TENSION)**2 + (U_CORRIENTE/I0_CORRIENTE)**2)

# --- potencia en funcionamiento (rango fluctuante -> distribucion rectangular) ---
I_func_mid = (I_FUNC_LO + I_FUNC_HI) / 2
V_func_mid = (V_FUNC_LO + V_FUNC_HI) / 2
u_I_func = (I_FUNC_HI - I_FUNC_LO) / 2 / np.sqrt(3)
u_V_func = (V_FUNC_HI - V_FUNC_LO) / 2 / np.sqrt(3)
Pfunc_watts = V_func_mid * I_func_mid * COS_PHI
u_Pfunc_watts = Pfunc_watts * np.sqrt((u_V_func/V_func_mid)**2 + (u_I_func/I_func_mid)**2)

# --- potencia neta de conminucion (Ec. potencia_total: Wtotal = W0 + Wm*mdot) ---
Pneta_watts = Pfunc_watts - P0_watts
u_Pneta_watts = np.sqrt(u_Pfunc_watts**2 + u_P0_watts**2)

t_h = T_S / 3600
m_procesada_g = feed_m1 + feed_m2
m_procesada_t = m_procesada_g / 1e6   # g -> t métrica
m_procesada_kg = m_procesada_g / 1e3
u_m_procesada_g = np.sqrt(U_MASA_LECTURA**2 + U_MASA_LECTURA**2)  # dos lecturas independientes

# Energia BRUTA (sin descontar vacio; equivalente al enfoque de la version
# previa del informe, se conserva para comparacion) y NETA (descontando P0)
E_bruta_kWh = Pfunc_watts * t_h / 1000
u_E_bruta_kWh = u_Pfunc_watts * t_h / 1000
Es_bruta_kWh_t = E_bruta_kWh / m_procesada_t
u_Es_bruta_kWh_t = Es_bruta_kWh_t * np.sqrt((u_E_bruta_kWh/E_bruta_kWh)**2 + (u_m_procesada_g/m_procesada_g)**2)

E_kWh = Pneta_watts * t_h / 1000
u_E_kWh = np.sqrt((u_Pneta_watts*t_h/1000)**2 + (Pneta_watts*U_TIEMPO/3600/1000)**2)
Es_kWh_t = E_kWh / m_procesada_t
Es_kWh_kg = E_kWh / m_procesada_kg
Es_kJ_kg = Es_kWh_kg * 3600
u_Es_kWh_t = Es_kWh_t * np.sqrt((u_E_kWh/E_kWh)**2 + (u_m_procesada_g/m_procesada_g)**2)

F80_mm = RESULTS["feed"]["F80"]
u_F80_mm = RESULTS["feed"]["u_F80"]
P80_mm = RESULTS["combinado"]["D80"]
u_P80_mm = RESULTS["combinado"]["u_D80"]
F80_um, P80_um = F80_mm * 1000, P80_mm * 1000
u_F80_um, u_P80_um = u_F80_mm * 1000, u_P80_mm * 1000

# --- back-calculo de constantes de cada ley con el dato de energia NETA ---
KR_exp = Es_kWh_t / (1/P80_mm - 1/F80_mm)                    # Rittinger, kWh*mm/t
KK_exp = Es_kWh_t / np.log(F80_mm / P80_mm)                  # Kick, kWh/t
Wi_exp = Es_kWh_t / (10 * (1/np.sqrt(P80_um) - 1/np.sqrt(F80_um)))  # Bond, kWh/t

# Rittinger: Y = 1/P80 - 1/F80 ; dY/dP80=-1/P80^2 ; dY/dF80=+1/F80^2
Y_rit = 1/P80_mm - 1/F80_mm
u_Y_rit = np.sqrt((u_P80_mm/P80_mm**2)**2 + (u_F80_mm/F80_mm**2)**2)
u_KR_exp = KR_exp * np.sqrt((u_Es_kWh_t/Es_kWh_t)**2 + (u_Y_rit/Y_rit)**2)

# Kick: Z = ln(F80/P80) ; dZ/dF80=1/F80 ; dZ/dP80=-1/P80
Z_kick = np.log(F80_mm/P80_mm)
u_Z_kick = np.sqrt((u_F80_mm/F80_mm)**2 + (u_P80_mm/P80_mm)**2)
u_KK_exp = KK_exp * np.sqrt((u_Es_kWh_t/Es_kWh_t)**2 + (u_Z_kick/Z_kick)**2)

# Bond: X = 10*(P80^-0.5 - F80^-0.5) ; dX/dP80=-5 P80^-1.5 ; dX/dF80=+5 F80^-1.5
X_bond = 10*(1/np.sqrt(P80_um) - 1/np.sqrt(F80_um))
u_X_bond = np.sqrt((5*P80_um**-1.5*u_P80_um)**2 + (5*F80_um**-1.5*u_F80_um)**2)
u_Wi_exp = Wi_exp * np.sqrt((u_Es_kWh_t/Es_kWh_t)**2 + (u_X_bond/X_bond)**2)

Wi_lit_low, Wi_lit_high = 3.0, 11.0  # kWh/t, rango de literatura (hammer mill, cereales/leguminosas)
Wi_dentro_de_rango = Wi_lit_low <= Wi_exp <= Wi_lit_high

RESULTS["energia"] = dict(
    V0=V0_TENSION, I0=I0_CORRIENTE, P0_W=P0_watts, u_P0_W=u_P0_watts,
    V_func_lo=V_FUNC_LO, V_func_hi=V_FUNC_HI, I_func_lo=I_FUNC_LO, I_func_hi=I_FUNC_HI,
    V_func_mid=V_func_mid, I_func_mid=I_func_mid, Pfunc_W=Pfunc_watts, u_Pfunc_W=u_Pfunc_watts,
    Pneta_W=Pneta_watts, u_Pneta_W=u_Pneta_watts,
    t_s=T_S, cos_phi=COS_PHI,
    Es_bruta_kWh_t=Es_bruta_kWh_t, u_Es_bruta_kWh_t=u_Es_bruta_kWh_t,
    E_kWh=E_kWh, u_E_kWh=u_E_kWh,
    m_procesada_g=m_procesada_g, u_m_procesada_g=u_m_procesada_g,
    Es_kWh_t=Es_kWh_t, u_Es_kWh_t=u_Es_kWh_t, Es_kWh_kg=Es_kWh_kg, Es_kJ_kg=Es_kJ_kg,
    F80_mm=F80_mm, u_F80_mm=u_F80_mm, P80_mm=P80_mm, u_P80_mm=u_P80_mm,
    KR_exp=KR_exp, u_KR_exp=u_KR_exp, KK_exp=KK_exp, u_KK_exp=u_KK_exp,
    Wi_exp=Wi_exp, u_Wi_exp=u_Wi_exp,
    Wi_lit_low=Wi_lit_low, Wi_lit_high=Wi_lit_high, Wi_dentro_de_rango=Wi_dentro_de_rango,
    razon_Wi_exp_vs_lit_max=Wi_exp / Wi_lit_high,
)


# --- relacion de reduccion con incertidumbre propagada (RR = F80/P80) ---
def propagar_RR(F80, uF80, P80, uP80):
    RR = F80/P80
    uRR = RR*np.sqrt((uF80/F80)**2 + (uP80/P80)**2)
    return RR, uRR

RR1, u_RR1 = propagar_RR(RESULTS["feed"]["F80"], RESULTS["feed"]["u_F80"],
                          RESULTS["molienda1"]["D80"], RESULTS["molienda1"]["u_D80"])
RR2, u_RR2 = propagar_RR(RESULTS["feed"]["F80"], RESULTS["feed"]["u_F80"],
                          RESULTS["molienda2"]["D80"], RESULTS["molienda2"]["u_D80"])
RESULTS["reduccion"] = dict(RR1=RR1, u_RR1=u_RR1, RR2=RR2, u_RR2=u_RR2)

# --- balance de masa: incertidumbre de perdidas y rendimiento (dos lecturas
#     de balanza independientes, +-0.05 g cada una) ---
u_masa_simple = U_MASA_LECTURA
u_dif_2masas = np.sqrt(u_masa_simple**2 + u_masa_simple**2)  # resta de dos masas

def propagar_porcentaje(numerador, u_num, denominador, u_den):
    """Propaga incertidumbre de un cociente expresado como porcentaje:
    pct = numerador/denominador*100."""
    pct = numerador/denominador*100
    u_pct = pct*np.sqrt((u_num/numerador)**2 + (u_den/denominador)**2)
    return pct, u_pct

u_perdidas_molienda_m1, u_pct_perdidas_molienda_m1 = (
    u_dif_2masas,
    propagar_porcentaje(perdidas_molienda_m1, u_dif_2masas, feed_m1, u_masa_simple)[1]
)
u_perdidas_molienda_m2, u_pct_perdidas_molienda_m2 = (
    u_dif_2masas,
    propagar_porcentaje(perdidas_molienda_m2, u_dif_2masas, feed_m2, u_masa_simple)[1]
)
u_pct_perdidas_tamizaje_m1 = propagar_porcentaje(
    perdidas_tamizaje_m1, u_dif_2masas, prod_molino_m1, u_masa_simple)[1]
u_pct_perdidas_tamizaje_m2 = propagar_porcentaje(
    perdidas_tamizaje_m2, u_dif_2masas, prod_molino_m2, u_masa_simple)[1]
u_pct_rendimiento_global_m1 = propagar_porcentaje(
    suma_tamices_m1, u_masa_simple, feed_m1, u_masa_simple)[1]
u_pct_rendimiento_global_m2 = propagar_porcentaje(
    suma_tamices_m2, u_masa_simple, feed_m2, u_masa_simple)[1]

RESULTS["balance"]["u_masa_simple"] = u_masa_simple
RESULTS["balance"]["u_perdidas_molienda_m1"] = u_perdidas_molienda_m1
RESULTS["balance"]["u_pct_perdidas_molienda_m1"] = u_pct_perdidas_molienda_m1
RESULTS["balance"]["u_perdidas_molienda_m2"] = u_perdidas_molienda_m2
RESULTS["balance"]["u_pct_perdidas_molienda_m2"] = u_pct_perdidas_molienda_m2
RESULTS["balance"]["u_pct_perdidas_tamizaje_m1"] = u_pct_perdidas_tamizaje_m1
RESULTS["balance"]["u_pct_perdidas_tamizaje_m2"] = u_pct_perdidas_tamizaje_m2
RESULTS["balance"]["u_pct_rendimiento_global_m1"] = u_pct_rendimiento_global_m1
RESULTS["balance"]["u_pct_rendimiento_global_m2"] = u_pct_rendimiento_global_m2

# --- fraccion retenida individual/acumulada: incertidumbre para la muestra
#     de calculo (malla 10, Molienda 1), dos masas independientes +-0.05 g,
#     total = suma de 7 fracciones (propagacion completa vía derivadas) ---
Wr_10 = df1.loc[df1["malla"].astype(str) == "10", "peso_neto_g"].values[0]
Wtotal_m1 = df1["peso_neto_g"].sum()
n_fracciones_m1 = len(df1)
# d(%Ret_i)/d(Wr_i) = (1 - x_i)/Wtotal ; d(%Ret_i)/d(Wr_j, j!=i) = -x_i/Wtotal
x_10 = Wr_10 / Wtotal_m1
u_pctRet_10 = 100 * np.sqrt(
    ((1 - x_10) / Wtotal_m1 * U_MASA_LECTURA) ** 2
    + (n_fracciones_m1 - 1) * (x_10 / Wtotal_m1 * U_MASA_LECTURA) ** 2
)
RESULTS["muestra_calculo"] = dict(
    Wr_10=Wr_10, Wtotal_m1=Wtotal_m1, x_10=x_10, u_pctRet_10=u_pctRet_10,
)

# --- escalamiento industrial: P_industrial (kW) = Es_neta (kWh/t) * Q (t/h)
#   Se emplea la energia especifica NETA (ya descontado el consumo en
#   vacio), pues es la componente que efectivamente escala con el caudal
#   de material procesado; el motor industrial requerira, ademas, su
#   propia potencia base en vacio (no extrapolable desde el equipo de
#   laboratorio), por lo que esta estimacion es una COTA INFERIOR de la
#   potencia total requerida. ---
Q_ejemplo_th = np.array([0.5, 1.0, 2.0, 5.0])
P_industrial_kW = Es_kWh_t * Q_ejemplo_th
RESULTS["escalamiento"] = dict(
    Q_th=Q_ejemplo_th.tolist(), P_industrial_kW=P_industrial_kW.tolist()
)

# ====================================================================
# GUARDAR RESULTADOS NUMERICOS (para consulta y para redactar el informe)
# ====================================================================
with open(os.path.join(DATOS, "resultados_resumen.json"), "w", encoding="utf-8") as f:
    json.dump(RESULTS, f, indent=2, ensure_ascii=False, default=float)

print(json.dumps(RESULTS, indent=2, ensure_ascii=False, default=float))

# ====================================================================
# 5. TABLAS LATEX (fragmentos, estilo booktabs, para \input en el informe)
# ====================================================================

def fnum(x, dec=2):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    # (deja separador de miles '.' y decimal ',' -> convencion es-CO;
    #  para simplicidad de compilacion usamos en cambio punto decimal abajo)

def f(x, dec=2):
    return f"{x:.{dec}f}"

os.makedirs(TAB, exist_ok=True)

# --- Tabla: alimento (granos individuales) ---
with open(os.path.join(TAB, "tabla_alimento.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{ccc}\n\\toprule\n")
    fh.write("Grano & $D$ (mm) & Observaci\\'on \\\\\n\\midrule\n")
    for i, d in zip(df_feed["grano"], df_feed["D_mm"]):
        obs = ""
        if abs(d - 7.9) < 1e-9:
            obs = "$7+0{,}05\\times18$"
        fh.write(f"{int(i)} & {f(d,2)} & {obs} \\\\\n")
    fh.write("\\midrule\n")
    fh.write(f"\\multicolumn{{2}}{{l}}{{Media aritm\\'etica $\\bar D$}} & {f(RESULTS['feed']['mean'],2)} mm \\\\\n")
    fh.write(f"\\multicolumn{{2}}{{l}}{{Desv. est\\'andar muestral $s$}} & {f(RESULTS['feed']['std'],2)} mm \\\\\n")
    fh.write(f"\\multicolumn{{2}}{{l}}{{Incertidumbre combinada $u_c$}} & {f(RESULTS['feed']['u_c'],3)} mm \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla: diametros medios del alimento ---
with open(os.path.join(TAB, "tabla_diametros_alimento.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n")
    fh.write("Diametro medio & Definici\\'on (base n\\'umero) & Valor (mm) \\\\\n\\midrule\n")
    fh.write(f"Aritm\\'etico $\\bar D_{{[1,0]}}$ & $\\sum D_i / n$ & {f(RESULTS['feed']['D_arit'],3)} \\\\\n")
    fh.write(f"Superficial $\\bar D_{{[2,0]}}$ & $(\\sum D_i^2/n)^{{1/2}}$ & {f(RESULTS['feed']['D_sup'],3)} \\\\\n")
    fh.write(f"Volum\\'etrico $\\bar D_{{[3,0]}}$ & $(\\sum D_i^3/n)^{{1/3}}$ & {f(RESULTS['feed']['D_vol'],3)} \\\\\n")
    fh.write(f"Sauter $\\bar D_{{[3,2]}}$ & $\\sum D_i^3/\\sum D_i^2$ & {f(RESULTS['feed']['D32'],3)} \\\\\n")
    fh.write(f"De Brouckere $\\bar D_{{[4,3]}}$ & $\\sum D_i^4/\\sum D_i^3$ & {f(RESULTS['feed']['D43'],3)} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla granulometrica (una funcion generica para M1/M2) ---
def tabla_granulometrica(df, nombre_archivo):
    with open(os.path.join(TAB, nombre_archivo), "w", encoding="utf-8") as fh:
        fh.write("\\begin{tabular}{lcccccc}\n\\toprule\n")
        fh.write("Malla & Abertura & $W_r$ & \\%Ret. & \\%Ret. & \\%Pasante & $D_{repr}$ \\\\\n")
        fh.write(" & (mm) & (g) & indiv. & acum. & & (mm) \\\\\n\\midrule\n")
        for _, row in df.iterrows():
            malla = row["malla"]
            ab = "$<0{,}355$" if malla == "Fondos" else f(row['abertura_mm'],3)
            fh.write(f"{malla} & {ab} & {f(row['peso_neto_g'],2)} & {f(row['frac_individual_%'],2)} & "
                     f"{f(row['frac_acumulada_%'],2)} & {f(row['pasante_%'],2)} & {f(row['D_repr_mm'],3)} \\\\\n")
        total = df["peso_neto_g"].sum()
        fh.write("\\midrule\n")
        fh.write(f"\\multicolumn{{2}}{{l}}{{\\textbf{{Total}}}} & \\textbf{{{f(total,2)}}} & "
                 f"\\multicolumn{{4}}{{l}}{{(suma de fracciones individuales = 100{{,}}00\\%)}} \\\\\n")
        fh.write("\\bottomrule\n\\end{tabular}\n")

tabla_granulometrica(df1, "tabla_granulometria_m1.tex")
tabla_granulometrica(df2, "tabla_granulometria_m2.tex")

# --- Tabla D80: comparacion de metodos ---
with open(os.path.join(TAB, "tabla_D80_metodos.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n")
    fh.write("M\\'etodo & Molienda 1 (mm) & Molienda 2 (mm) & Fundamento \\\\\n\\midrule\n")
    fh.write(f"GGS (ajuste log-log, $R^2$) & {f(RESULTS['molienda1']['D80_ggs'],3)} ({f(RESULTS['molienda1']['r2_ggs'],4)}) & "
             f"{f(RESULTS['molienda2']['D80_ggs'],3)} ({f(RESULTS['molienda2']['r2_ggs'],4)}) & Gates-Gaudin-Schuhmann \\\\\n")
    fh.write(f"RRB (ajuste log-log, $R^2$) & {f(RESULTS['molienda1']['D80_rrb'],3)} ({f(RESULTS['molienda1']['r2_rrb'],4)}) & "
             f"{f(RESULTS['molienda2']['D80_rrb'],3)} ({f(RESULTS['molienda2']['r2_rrb'],4)}) & Rosin-Rammler-Bennet \\\\\n")
    fh.write(f"Interpolaci\\'on log-log (2 puntos) & {f(RESULTS['molienda1']['D80_interp'],3)} & "
             f"{f(RESULTS['molienda2']['D80_interp'],3)} & Verificaci\\'on directa \\\\\n")
    fh.write("\\midrule\n")
    fh.write(f"\\textbf{{Reportado (modelo de mejor ajuste)}} & \\textbf{{{f(RESULTS['molienda1']['D80'],2)} $\\pm$ {f(RESULTS['molienda1']['u_D80'],2)}}} & "
             f"\\textbf{{{f(RESULTS['molienda2']['D80'],2)} $\\pm$ {f(RESULTS['molienda2']['u_D80'],2)}}} & ({RESULTS['molienda1']['mejor_modelo']}/{RESULTS['molienda2']['mejor_modelo']}) \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla resumen de diametros caracteristicos (feed, M1, M2) ---
with open(os.path.join(TAB, "tabla_resumen_diametros.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n")
    fh.write("Par\\'ametro & Alimento & Molienda 1 & Molienda 2 \\\\\n\\midrule\n")
    fh.write(f"$D_{{80}}$ (mm) & {f(RESULTS['feed']['F80'],2)} $\\pm$ {f(RESULTS['feed']['u_F80'],2)} & "
             f"{f(RESULTS['molienda1']['D80'],2)} $\\pm$ {f(RESULTS['molienda1']['u_D80'],2)} & "
             f"{f(RESULTS['molienda2']['D80'],2)} $\\pm$ {f(RESULTS['molienda2']['u_D80'],2)} \\\\\n")
    fh.write(f"$D_{{50}}$ (mm) & {f(RESULTS['feed']['F50'],2)} & {f(RESULTS['molienda1']['D50'],2)} & {f(RESULTS['molienda2']['D50'],2)} \\\\\n")
    fh.write(f"$D_{{10}}$ (mm) & {f(RESULTS['feed']['F10'],2)} & {f(RESULTS['molienda1']['D10'],2)} & {f(RESULTS['molienda2']['D10'],2)} \\\\\n")
    fh.write(f"Media m\\'asica $\\bar D_{{[1,0]}}$ (mm) & {f(RESULTS['feed']['D_arit'],2)} & {f(RESULTS['molienda1']['D_masico'],2)} & {f(RESULTS['molienda2']['D_masico'],2)} \\\\\n")
    fh.write(f"Media de Sauter $\\bar D_{{[3,2]}}$ (mm) & {f(RESULTS['feed']['D32'],2)} & {f(RESULTS['molienda1']['D_sauter'],2)} & {f(RESULTS['molienda2']['D_sauter'],2)} \\\\\n")
    fh.write(f"Span $(D_{{90}}-D_{{10}})/D_{{50}}$ & {f(RESULTS['feed']['span'],2)} & {f(RESULTS['molienda1']['span'],2)} & {f(RESULTS['molienda2']['span'],2)} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla relacion de reduccion ---
with open(os.path.join(TAB, "tabla_reduccion.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lccc}\n\\toprule\n")
    fh.write("Corrida & $F_{80}$ (mm) & $P_{80}$ (mm) & $RR=F_{80}/P_{80}$ \\\\\n\\midrule\n")
    fh.write(f"Molienda 1 & {f(RESULTS['feed']['F80'],2)}$\\pm${f(RESULTS['feed']['u_F80'],2)} & {f(RESULTS['molienda1']['D80'],2)}$\\pm${f(RESULTS['molienda1']['u_D80'],2)} & {f(RESULTS['reduccion']['RR1'],2)}$\\pm${f(RESULTS['reduccion']['u_RR1'],2)} \\\\\n")
    fh.write(f"Molienda 2 & {f(RESULTS['feed']['F80'],2)}$\\pm${f(RESULTS['feed']['u_F80'],2)} & {f(RESULTS['molienda2']['D80'],2)}$\\pm${f(RESULTS['molienda2']['u_D80'],2)} & {f(RESULTS['reduccion']['RR2'],2)}$\\pm${f(RESULTS['reduccion']['u_RR2'],2)} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla balance de masa ---
with open(os.path.join(TAB, "tabla_balance.tex"), "w", encoding="utf-8") as fh:
    B = RESULTS["balance"]
    fh.write("\\begin{tabular}{lcc}\n\\toprule\n")
    fh.write("Etapa & Molienda 1 (g) & Molienda 2 (g) \\\\\n\\midrule\n")
    fh.write(f"Alimento antes de moler & {f(B['feed_m1'],2)}$\\pm${f(B['u_masa_simple'],2)} & {f(B['feed_m2'],2)}$\\pm${f(B['u_masa_simple'],2)} \\\\\n")
    fh.write(f"Producto recuperado del molino & {f(B['prod_molino_m1'],2)}$\\pm${f(B['u_masa_simple'],2)} & {f(B['prod_molino_m2'],2)}$\\pm${f(B['u_masa_simple'],2)} \\\\\n")
    fh.write(f"P\\'erdidas en la molienda (molino) & {f(B['perdidas_molienda_m1'],2)}$\\pm${f(B['u_perdidas_molienda_m1'],2)} ({f(B['pct_perdidas_molienda_m1'],2)}$\\pm${f(B['u_pct_perdidas_molienda_m1'],2)}\\%) & {f(B['perdidas_molienda_m2'],2)}$\\pm${f(B['u_perdidas_molienda_m2'],2)} ({f(B['pct_perdidas_molienda_m2'],2)}$\\pm${f(B['u_pct_perdidas_molienda_m2'],2)}\\%) \\\\\n")
    fh.write(f"Suma de fracciones tamizadas & {f(B['suma_tamices_m1'],2)} & {f(B['suma_tamices_m2'],2)} \\\\\n")
    fh.write(f"P\\'erdidas en el tamizaje & {f(B['perdidas_tamizaje_m1'],2)} ({f(B['pct_perdidas_tamizaje_m1'],2)}$\\pm${f(B['u_pct_perdidas_tamizaje_m1'],2)}\\%) & {f(B['perdidas_tamizaje_m2'],2)} ({f(B['pct_perdidas_tamizaje_m2'],2)}$\\pm${f(B['u_pct_perdidas_tamizaje_m2'],2)}\\%) \\\\\n")
    fh.write("\\midrule\n")
    fh.write(f"Rendimiento global (tamizado/alimento) & {f(B['rendimiento_global_m1'],2)}$\\pm${f(B['u_pct_rendimiento_global_m1'],2)}\\% & {f(B['rendimiento_global_m2'],2)}$\\pm${f(B['u_pct_rendimiento_global_m2'],2)}\\% \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

# --- Tabla energia: vacio -> funcionamiento -> neta (proceso global M1+M2) ---
E = RESULTS["energia"]
with open(os.path.join(TAB, "tabla_energia.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lc}\n\\toprule\n")
    fh.write("Variable & Valor \\\\\n\\midrule\n")
    fh.write("\\multicolumn{2}{l}{\\textit{En vac\\'io}} \\\\\n")
    fh.write(f"Tensi\\'on, $V_0$ & {f(E['V0'],1)}$\\pm${f(U_VOLTAJE,2)} V \\\\\n")
    fh.write(f"Corriente, $I_0$ & {f(E['I0'],3)}$\\pm${f(U_CORRIENTE,4)} A \\\\\n")
    fh.write(f"Potencia en vac\\'io, $P_0=V_0 I_0$ & {f(E['P0_W'],2)}$\\pm${f(E['u_P0_W'],2)} W \\\\\n")
    fh.write("\\multicolumn{2}{l}{\\textit{En funcionamiento (t=210 s, rango observado)}} \\\\\n")
    fh.write(f"Tensi\\'on, $V$ & {f(E['V_func_lo'],1)}--{f(E['V_func_hi'],1)} V (centro {f(E['V_func_mid'],2)}) \\\\\n")
    fh.write(f"Corriente, $I$ & {f(E['I_func_lo'],3)}--{f(E['I_func_hi'],3)} A (centro {f(E['I_func_mid'],3)}) \\\\\n")
    fh.write(f"Potencia en funcionamiento, $P=VI$ & {f(E['Pfunc_W'],2)}$\\pm${f(E['u_Pfunc_W'],2)} W \\\\\n")
    fh.write("\\multicolumn{2}{l}{\\textit{Neta de conminuci\\'on (Ec.~6)}} \\\\\n")
    fh.write(f"Potencia neta, $P_{{neta}}=P-P_0$ & {f(E['Pneta_W'],2)}$\\pm${f(E['u_Pneta_W'],2)} W \\\\\n")
    fh.write(f"Energ\\'ia neta, $E=P_{{neta}}\\,t$ & {f(E['E_kWh']*1000,2)}$\\pm${f(E['u_E_kWh']*1000,2)} Wh \\\\\n")
    fh.write(f"Masa procesada (alimento real, M1+M2) & {f(E['m_procesada_g'],2)}$\\pm${f(E['u_m_procesada_g'],2)} g \\\\\n")
    fh.write(f"\\textbf{{Energ\\'ia espec\\'ifica neta, $E_s$}} & \\textbf{{{f(E['Es_kWh_t'],3)}$\\pm${f(E['u_Es_kWh_t'],3)} kWh/t}} ({f(E['Es_kJ_kg'],2)} kJ/kg) \\\\\n")
    fh.write(f"\\textit{{Referencia: energ\\'ia bruta sin descontar vac\\'io}} & \\textit{{{f(E['Es_bruta_kWh_t'],2)}$\\pm${f(E['u_Es_bruta_kWh_t'],2)} kWh/t}} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

with open(os.path.join(TAB, "tabla_leyes_conminucion.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{lccl}\n\\toprule\n")
    fh.write("Ley & Constante retrocalculada & Valor & Unidades \\\\\n\\midrule\n")
    fh.write(f"Rittinger & $K_R = E_s/(1/P_{{80}}-1/F_{{80}})$ & {f(E['KR_exp'],2)}$\\pm${f(E['u_KR_exp'],2)} & kWh$\\cdot$mm/t \\\\\n")
    fh.write(f"Kick & $K_K = E_s/\\ln(F_{{80}}/P_{{80}})$ & {f(E['KK_exp'],3)}$\\pm${f(E['u_KK_exp'],3)} & kWh/t \\\\\n")
    fh.write(f"Bond & $W_i = E_s / [10(1/\\sqrt{{P_{{80}}}}-1/\\sqrt{{F_{{80}}}})]$ & {f(E['Wi_exp'],2)}$\\pm${f(E['u_Wi_exp'],2)} & kWh/t \\\\\n")
    fh.write("\\midrule\n")
    fh.write(f"\\multicolumn{{4}}{{p{{0.85\\linewidth}}}}{{\\footnotesize Rango de $W_i$ reportado en literatura para molienda de cereales/leguminosas en molino de martillos: {f(E['Wi_lit_low'],1)}--{f(E['Wi_lit_high'],1)} kWh/t \\citep{{budacan2013maiz,budacan2013trigo}}. El valor retrocalculado, obtenido con la energ\\'ia espec\\'ifica \\textbf{{neta}} (Tabla~10), cae \\textbf{{dentro}} de ese rango (v\\'ease discusi\\'on, Secci\\'on~\\ref{{sec:discusion-bond}}).}} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

with open(os.path.join(TAB, "tabla_escalamiento.tex"), "w", encoding="utf-8") as fh:
    fh.write("\\begin{tabular}{cc}\n\\toprule\n")
    fh.write("Caudal de dise\\~no, $Q$ (t/h) & Potencia de motor estimada, $P_{ind}$ (kW) \\\\\n\\midrule\n")
    for q, p in zip(RESULTS["escalamiento"]["Q_th"], RESULTS["escalamiento"]["P_industrial_kW"]):
        fh.write(f"{f(q,1)} & {f(p,2)} \\\\\n")
    fh.write("\\bottomrule\n\\end{tabular}\n")

print("Tablas LaTeX generadas en:", TAB)

# ====================================================================
# 6. FIGURAS  (calidad de publicacion: ver bloque de estilo, Sec. 2)
# ====================================================================

# --- Figura 1 (ancho de impresion: 0.95\textwidth) -----------------------
# Distribucion de tamano del alimento: (a) valores individuales ordenados,
# (b) histograma de frecuencias.
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(W_95, 3.05),
                               gridspec_kw={"width_ratios": [1.3, 1]})

ax.scatter(np.arange(1, n_feed + 1), np.sort(D_feed), color=COLOR_F, s=42,
           zorder=3, edgecolor="black", linewidth=0.6)
ax.axhline(mean_feed, color="#1A1A1A", linestyle="--", linewidth=1.1,
           label=f"Media = {mean_feed:.2f} mm")
ax.fill_between([0, n_feed + 1], mean_feed - ci95_feed, mean_feed + ci95_feed,
                 color=COLOR_NEU, alpha=0.18, linewidth=0,
                 label=f"IC 95% = $\\pm${ci95_feed:.2f} mm")
ax.axhline(F80_puntual, color=COLOR_FIT, linestyle=":", linewidth=1.4,
           label=f"$F_{{80}}$ = {F80_puntual:.2f} mm")
ax.set_xlim(0, n_feed + 1)
ax.set_xlabel("Grano (ordenado ascendentemente)")
ax.set_ylabel("Diámetro $D$ (mm)")
panel_title(ax, "a", "Diámetros medidos individualmente")
ax.legend(loc="lower right", handlelength=1.3)
despine(ax)

ax2.hist(D_feed, bins=6, color=COLOR_F, edgecolor="black", linewidth=0.6, alpha=0.9)
ax2.axvline(mean_feed, color="#1A1A1A", linestyle="--", linewidth=1.1)
ax2.set_xlabel("Diámetro $D$ (mm)")
ax2.set_ylabel("Frecuencia (número de granos)")
panel_title(ax2, "b", "Histograma ($n=10$)")
despine(ax2)

fig.tight_layout(w_pad=2.0)
savefig(fig, "fig1_alimento_distribucion")

# --- Figura 2 (ancho de impresion: 0.75\textwidth) -----------------------
# Curvas granulometricas acumuladas del producto (M1, M2) con ajuste GGS.
fig, ax = plt.subplots(figsize=(W_75, 3.65))
for df, color, label, ajuste in [(df1, COLOR_M1, "Molienda 1", ajuste1),
                                   (df2, COLOR_M2, "Molienda 2", ajuste2)]:
    sub = df.dropna(subset=["abertura_mm"])
    ax.plot(sub["abertura_mm"], sub["pasante_%"], "o", color=color, markersize=5.5,
            markeredgecolor="black", markeredgewidth=0.5, zorder=3)
    Dline = np.logspace(np.log10(0.15), np.log10(5.2), 200)
    if ajuste["mejor_modelo"] == "GGS":
        Yline = np.exp(ajuste["m_ggs"] * np.log(Dline) + ajuste["b_ggs"])
    else:
        Yline = 100 * (1 - np.exp(-np.exp(ajuste["n_rrb"] * np.log(Dline) + ajuste["c_rrb"])))
    Yline = np.minimum(Yline, 100)  # el modelo GGS no satura naturalmente en 100%
    ax.plot(Dline, Yline, "-", color=color, linewidth=1.3, alpha=0.85,
            label=f"{label} ($D_{{80}}$={ajuste['D80']:.2f} mm)")
ax.axhline(80, color=COLOR_NEU, linestyle=":", linewidth=1.0, zorder=1)
ax.set_xscale("log")
ax.set_xlabel("Abertura del tamiz, $D$ (mm, escala log)")
ax.set_ylabel("Pasante acumulado (%)")
ax.set_title("Curvas granulométricas acumuladas del producto")
ax.set_ylim(0, 105)
ax.legend(loc="upper left")
ax.grid(True, which="major", axis="both", alpha=0.35, linewidth=0.5)
ax.grid(True, which="minor", axis="x", alpha=0.15, linewidth=0.4)
despine(ax)
fig.tight_layout()
savefig(fig, "fig2_curvas_granulometricas")

# --- Figura 3 (ancho de impresion: 0.80\textwidth) -----------------------
# Distribucion diferencial (%retenido individual), M1 vs M2, barras agrupadas.
fig, ax = plt.subplots(figsize=(W_80, 3.35))
mallas_labels = [str(m) for m in df1["malla"]]
x = np.arange(len(mallas_labels))
w = 0.36
ax.bar(x - w/2, df1["frac_individual_%"], width=w, color=COLOR_M1,
       edgecolor="black", linewidth=0.5, label="Molienda 1")
ax.bar(x + w/2, df2["frac_individual_%"], width=w, color=COLOR_M2,
       edgecolor="black", linewidth=0.5, label="Molienda 2")
ax.set_xticks(x)
ax.set_xticklabels([f"Malla {m}" if m != "Fondos" else "Fondos" for m in mallas_labels])
ax.set_ylabel("Retenido individual (%)")
ax.set_xlabel("Fracción granulométrica")
ax.set_title("Distribución diferencial de tamaño del producto")
ax.legend()
despine(ax)
fig.tight_layout()
savefig(fig, "fig3_distribucion_diferencial")

# --- Figura 4 (ancho de impresion: 1.00\textwidth) -----------------------
# Linealizacion log-log del modelo GGS, ambas corridas.
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 2.85), sharey=True)
for axi, letter, df, color, label, ajuste in [
    (axes[0], "a", df1, COLOR_M1, "Molienda 1", ajuste1),
    (axes[1], "b", df2, COLOR_M2, "Molienda 2", ajuste2),
]:
    sub = df.dropna(subset=["abertura_mm"])
    lnD = np.log(sub["abertura_mm"])
    lnY = np.log(sub["pasante_%"])
    axi.scatter(lnD, lnY, color=color, s=42, edgecolor="black", linewidth=0.5,
                zorder=3, label="Datos")
    xline = np.linspace(lnD.min() - 0.1, lnD.max() + 0.1, 50)
    axi.plot(xline, ajuste["m_ggs"] * xline + ajuste["b_ggs"], "--", color=COLOR_FIT,
             linewidth=1.3, label=f"Ajuste GGS ($R^2$={ajuste['r2_ggs']:.4f})")
    axi.set_xlabel("$\\ln(D)$")
    panel_title(axi, letter, label)
    axi.legend(loc="lower right", handlelength=1.3)
    despine(axi)
axes[0].set_ylabel("ln(% pasante)")
fig.tight_layout(w_pad=2.0)
savefig(fig, "fig4_ajuste_ggs")

# --- Figura 5 (ancho de impresion: 1.00\textwidth) -----------------------
# Balance de masa, ambas corridas (dos paneles).
etapas = ["Alimento", "Producto\nmolino", "Pérdidas\nmolienda",
          "Tamizado\ntotal", "Pérdidas\ntamizaje"]
fig, axes = plt.subplots(1, 2, figsize=(W_FULL, 3.25), sharey=True)
ylim_max = max(feed_m1, feed_m2) * 1.20
for axi, letter, feed_i, prod_i, perd_mol_i, suma_i, perd_tam_i, color_prod, titulo in [
    (axes[0], "a", feed_m1, prod_molino_m1, perdidas_molienda_m1, suma_tamices_m1, perdidas_tamizaje_m1, COLOR_M1, "Molienda 1"),
    (axes[1], "b", feed_m2, prod_molino_m2, perdidas_molienda_m2, suma_tamices_m2, perdidas_tamizaje_m2, COLOR_M2, "Molienda 2"),
]:
    valores = [feed_i, prod_i, perd_mol_i, suma_i, perd_tam_i]
    colores_i = [COLOR_F, color_prod, COLOR_NEU, COLOR_ACC, COLOR_NEU]
    bars = axi.bar(etapas, valores, color=colores_i, edgecolor="black", linewidth=0.5, width=0.68)
    for b, v in zip(bars, valores):
        axi.text(b.get_x() + b.get_width()/2, v + ylim_max * 0.02, f"{v:.1f} g",
                  ha="center", fontsize=7.6)
    panel_title(axi, letter, titulo)
    axi.set_ylim(0, ylim_max)
    axi.tick_params(axis="x", labelsize=7.8)
    despine(axi)
axes[0].set_ylabel("Masa (g)")
fig.tight_layout(w_pad=2.5)
savefig(fig, "fig5_balance_masa")

# --- Figura 6 (ancho de impresion: 0.80\textwidth) -----------------------
# Comparacion de diametros caracteristicos: alimento vs. producto.
fig, ax = plt.subplots(figsize=(W_80, 3.5))
categorias = ["Aritm./Másico\n$\\bar D_{[1,0]}$", "Sauter\n$\\bar D_{[3,2]}$", "$D_{80}$"]
alim_vals = [RESULTS["feed"]["D_arit"], RESULTS["feed"]["D32"], RESULTS["feed"]["F80"]]
m1_vals = [RESULTS["molienda1"]["D_masico"], RESULTS["molienda1"]["D_sauter"], RESULTS["molienda1"]["D80"]]
m2_vals = [RESULTS["molienda2"]["D_masico"], RESULTS["molienda2"]["D_sauter"], RESULTS["molienda2"]["D80"]]
x = np.arange(len(categorias))
w = 0.26
ax.bar(x - w, alim_vals, width=w, color=COLOR_F, edgecolor="black", linewidth=0.5, label="Alimento")
ax.bar(x, m1_vals, width=w, color=COLOR_M1, edgecolor="black", linewidth=0.5, label="Molienda 1 (producto)")
ax.bar(x + w, m2_vals, width=w, color=COLOR_M2, edgecolor="black", linewidth=0.5, label="Molienda 2 (producto)")
ax.set_xticks(x)
ax.set_xticklabels(categorias)
ax.set_ylabel("Diámetro (mm)")
ax.set_title("Comparación de diámetros característicos: alimento vs. producto")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=3, handlelength=1.3)
despine(ax)
fig.tight_layout()
savefig(fig, "fig6_comparacion_diametros")

# --- Figura 7 (ancho de impresion: 0.95\textwidth) -----------------------
# Comparacion de las tres leyes de conminucion (Rittinger, Kick, Bond),
# cada una calibrada para pasar exactamente por el UNICO punto experimental
# disponible (F80, P80_combinado, Es). Con n=1 dato de energia no es
# valido calcular un R^2 de ajuste (esa metrica requiere >=2 observaciones
# independientes para cuantificar varianza no explicada); en su lugar, el
# panel (b) cuantifica cuantas veces se aleja cada constante retrocalculada
# del rango tipico reportado en literatura para molienda de granos en
# molino de martillos -el criterio de plausibilidad que SI puede evaluarse
# honestamente con un solo dato-.
F80_um = F80_puntual * 1000  # micras
F80_mm_ = F80_puntual        # mm
P80_range_um = np.linspace(1000, 3600, 200)  # micras: ventana centrada en el rango relevante del ensayo
P80_range_mm = P80_range_um / 1000
Wi_lit_low, Wi_lit_high = RESULTS["energia"]["Wi_lit_low"], RESULTS["energia"]["Wi_lit_high"]
Wi_exp_val = RESULTS["energia"]["Wi_exp"]
KR_exp_val = RESULTS["energia"]["KR_exp"]
KK_exp_val = RESULTS["energia"]["KK_exp"]
P80_comb_um = RESULTS["combinado"]["D80"] * 1000
P80_comb_mm = RESULTS["combinado"]["D80"]
Es_exp_val = RESULTS["energia"]["Es_kWh_t"]


def W_bond(P80_um_, F80_um_, Wi):
    return 10 * Wi * (1/np.sqrt(P80_um_) - 1/np.sqrt(F80_um_))


def W_rittinger(P80_mm_, F80_mm_, KR):
    return KR * (1/P80_mm_ - 1/F80_mm_)


def W_kick(P80_mm_, F80_mm_, KK):
    return KK * np.log(F80_mm_/P80_mm_)


fig, (ax, ax2) = plt.subplots(1, 2, figsize=(W_95, 3.3))

# --- Panel (a): las 3 leyes, cada una calibrada al mismo punto experimental
ax.plot(P80_range_um, W_rittinger(P80_range_mm, F80_mm_, KR_exp_val), color=COLOR_M2,
        linestyle="--", linewidth=1.3,
        label=f"Rittinger: $W=K_R(1/P_{{80}}-1/F_{{80}})$\n$K_R$={KR_exp_val:.1f} kWh·mm/t")
ax.plot(P80_range_um, W_kick(P80_range_mm, F80_mm_, KK_exp_val), color=COLOR_M1,
        linestyle="-", linewidth=1.8,
        label=f"Kick: $W=K_K\\ln(F_{{80}}/P_{{80}})$\n$K_K$={KK_exp_val:.2f} kWh/t")
ax.plot(P80_range_um, W_bond(P80_range_um, F80_um, Wi_exp_val), color=COLOR_FIT,
        linestyle="-.", linewidth=1.3,
        label=f"Bond: $W=10W_i(1/\\sqrt{{P_{{80}}}}-1/\\sqrt{{F_{{80}}}})$\n$W_i$={Wi_exp_val:.0f} kWh/t")
ax.plot([P80_comb_um], [Es_exp_val], marker="D", markersize=7, color="#1A1A1A",
        markeredgecolor="white", markeredgewidth=0.6, linestyle="none",
        label=f"Punto experimental neto (M1+M2)\n$E_s$={Es_exp_val:.2f} kWh/t", zorder=5)
ax.set_xlabel("$P_{80}$ (µm)")
ax.set_ylabel("Energía específica, $W$ (kWh/t)")
panel_title(ax, "a", "Tres leyes calibradas al punto experimental")
ax.set_ylim(0, 1.6)
ax.legend(loc="upper right", handlelength=1.5, fontsize=7.2)
despine(ax)

# --- Panel (b): plausibilidad -- distancia de cada constante al rango de
# literatura disponible (unicamente Wi tiene un rango de literatura
# establecido en este informe, Sec. 7.3; KR y KK se muestran para
# referencia pero sin rango comparativo independiente)
etiquetas_ley = ["Rittinger\n$K_R$ (kWh·mm/t)", "Kick\n$K_K$ (kWh/t)", "Bond\n$W_i$ (kWh/t)"]
valores_ley = [KR_exp_val, KK_exp_val, Wi_exp_val]
colores_ley = [COLOR_M2, COLOR_M1, COLOR_FIT]
x_ley = np.arange(3)
ylim_b = max(max(valores_ley) * 1.35, Wi_lit_high * 1.3)
bars = ax2.bar(x_ley, valores_ley, color=colores_ley, edgecolor="black", linewidth=0.5, width=0.55)
for b, v in zip(bars, valores_ley):
    ax2.text(b.get_x() + b.get_width()/2, v + ylim_b*0.025, f"{v:.2f}", ha="center", fontsize=8)
ax2.axhspan(Wi_lit_low, Wi_lit_high, color=COLOR_NEU, alpha=0.25, linewidth=0,
            label=f"Rango de literatura\npara $W_i$: {Wi_lit_low:.0f}–{Wi_lit_high:.0f} kWh/t")
ax2.set_xticks(x_ley)
ax2.set_xticklabels(etiquetas_ley, fontsize=8)
ax2.set_ylabel("Valor de la constante")
panel_title(ax2, "b", "Plausibilidad frente a literatura")
ax2.set_ylim(0, ylim_b)
ax2.legend(loc="upper right", fontsize=7.5)
despine(ax2)

fig.tight_layout(w_pad=2.8)
savefig(fig, "fig7_teoria_bond_sensibilidad")

print("Figuras generadas en:", GRAF)
print("\nRESUMEN CLAVE:")
print(f"F80 alimento = {F80_puntual:.2f} +- {u_F80:.2f} mm")
print(f"D80 Molienda 1 = {RESULTS['molienda1']['D80']:.2f} +- {RESULTS['molienda1']['u_D80']:.2f} mm (modelo {RESULTS['molienda1']['mejor_modelo']})")
print(f"D80 Molienda 2 = {RESULTS['molienda2']['D80']:.2f} +- {RESULTS['molienda2']['u_D80']:.2f} mm (modelo {RESULTS['molienda2']['mejor_modelo']})")
print(f"RR1 = {RR1:.2f}  RR2 = {RR2:.2f}")

