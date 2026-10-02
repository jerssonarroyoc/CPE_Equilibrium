# cpe_equilibrio

Implementación y validación numérica de los métodos no estequiométricos
de la tesis doctoral de Christos Tsanas (DTU, 2018), *"Simultaneous
Chemical and Phase Equilibrium Calculations with Non-Stoichiometric
Method"*: el método de multiplicadores de Lagrange (Ec. 3.46) y el
método RAND modificado (Ec. 3.68).

## Documentación completa

Ver [`docs/documentacion.pdf`](docs/documentacion.pdf) (o compilar
desde [`docs/documentacion.tex`](docs/documentacion.tex)) para el
reporte técnico completo: fundamentos teóricos, métodos numéricos,
arquitectura del código, modelos termodinámicos, validación numérica y
figuras.

## Estructura

```
cpe_equilibrio/
├── src/                        # código fuente
│   ├── termodinamica.py        # Antoine, Wilson, UNIFAC, solucion regular, Gibbs
│   ├── inicializacion.py       # minimizacion de la funcion Q (Ec. 3.71-3.75)
│   ├── lagrange_multipliers.py # metodo de multiplicadores de Lagrange (Ec. 3.46)
│   ├── modified_rand.py        # metodo RAND modificado (Ec. 3.68)
│   ├── estabilidad.py          # analisis de estabilidad de Michelsen (Ec. 3.26-3.29)
│   ├── algoritmos.py           # algoritmos completos (Fig. 3.1 de la tesis)
│   ├── ejemplo_mtbe.py         # caso de prueba: sintesis de MTBE
│   ├── ejemplo_acetic_etanol.py# caso de prueba: esterificacion acido acetico/etanol
│   ├── pruebas_validacion.py   # suite de validacion numerica completa
│   └── generar_figuras.py      # genera docs/figuras/ a partir de ejecuciones reales
├── docs/
│   ├── documentacion.tex
│   ├── documentacion.pdf
│   ├── referencias.bib
│   └── figuras/
└── README.md
```

## Ejecutar

Cada módulo de `src/` corre independientemente:

```bash
cd src/
python pruebas_validacion.py   # suite de validacion completa (7 casos)
python ejemplo_mtbe.py         # caso MTBE (monofasico y VLE bifasico)
python ejemplo_acetic_etanol.py# caso esterificacion (ideal, UNIFAC, VLE)
python generar_figuras.py      # regenera las figuras de docs/figuras/
```

Dependencias: `numpy`, `scipy`, `thermo`, `matplotlib`.

## Validación numérica — resumen

| Validación | Resultado |
|---|---|
| Greiner (1991), Apéndice B | RAND modificado reproduce el valor publicado, diff ~8e-6 |
| Smith, Van Ness & Abbott, Example 14.8 | reproducción exacta (e=0.6879, x=0.344) |
| UNIFAC vs. experimental | reportado sin manipular (ver documentación) |
| SSA = RAND = scipy (minimización directa de Gibbs) | tolerancia 1e-8 en todos los casos |
| Antoine vs. puntos de ebullición reales | los 4 verificados explícitamente |

7/7 pruebas de `pruebas_validacion.py` pasan.

## Limitaciones conocidas (ver documentación completa, Sección 10.2)

- Ninguna de las Tablas 4.2/4.4/4.6/4.8 de la tesis se reproduce
  numéricamente: sus parámetros (Wilson, UNIQUAC, Antoine, K_eq)
  provienen de papers externos no disponibles para este trabajo.
- El arranque automático del análisis de estabilidad desde una sola
  fase no es robusto para sistemas fuertemente no ideales (p. ej.
  UNIFAC en el sistema de esterificación). Gap de robustez conocido,
  no resuelto, explícitamente fuera de alcance.
- No se implementaron ecuaciones de estado reales (todas las fases
  vapor son gas ideal).
- Sistema G de `combustion_gibbs.py` (combustión CH4/aire con hollín,
  `generar_perfiles_hollin.py`): la fase líquida "H2O(l)" está
  implementada (mismo mecanismo de fase condensada pura usado para el
  carbono sólido), pero no se logró demostrar su aparición. Requiere
  T por debajo de la temperatura crítica del agua (~647 K), y por
  debajo de ~700 K la inicialización de `inicializacion.minimizar_Q`
  (archivo ya validado, no modificado) sobredesborda (overflow) para
  especies de combustión de esta magnitud de ΔGf. Estas dos
  restricciones —una física, una numérica— dejan la condensación de
  agua fuera del rango que ese barrido puede mostrar de forma
  confiable sin más trabajo de robustez numérica, explícitamente fuera
  de alcance. Lo que sí se demuestra de forma confiable es la
  transición Vapor→Vapor+Sólido (aparición de carbono sólido/hollín).
