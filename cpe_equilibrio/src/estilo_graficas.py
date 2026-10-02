"""
estilo_graficas.py
====================

Estilo visual consistente para todas las figuras del proyecto
(diagramas de validacion y diagramas exploratorios), orientado a
publicacion cientifica: tipografia legible, paleta de colores
cualitativa consistente, rejilla discreta, sin bordes superiores/
derechos, resolucion de 300 dpi en el archivo final.

Uso: llamar aplicar_estilo_profesional() una vez al inicio de cada
script de generacion de figuras, antes de crear cualquier Figure.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

# Paleta cualitativa consistente (Tableau 10, orden fijo para que el
# mismo componente/especie use siempre el mismo color entre figuras).
PALETA = ["#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#9467bd",
          "#8c564b", "#17becf", "#e377c2", "#7f7f7f", "#bcbd22"]


def aplicar_estilo_profesional():
    mpl.rcParams.update({
        # Tipografia
        "font.size": 11,
        "font.family": "sans-serif",
        "axes.titlesize": 12.5,
        "axes.titleweight": "bold",
        "axes.labelsize": 11.5,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 9.5,
        "figure.titlesize": 13.5,
        "figure.titleweight": "bold",

        # Ejes y rejilla (estilo "journal", sin marco superior/derecho)
        "axes.edgecolor": "#444444",
        "axes.linewidth": 0.9,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#d0d0d0",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=PALETA),

        # Lineas y marcadores
        "lines.linewidth": 2.0,
        "lines.markersize": 5,

        # Leyenda
        "legend.frameon": True,
        "legend.framealpha": 0.92,
        "legend.edgecolor": "#cccccc",
        "legend.fancybox": False,

        # Resolucion
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })
