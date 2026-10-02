"""
ejemplo_mtbe.py
=================

Caso de prueba: sintesis de MTBE (seccion 4.1.5, pag. 63-67 de la
tesis de Tsanas), resuelto a T = 320.92 K y p = 1 atm, con alimentacion
isobuteno:metanol = 1:1.1 (sin n-butano inerte), usando tanto el
"successive substitution algorithm" como el "combined algorithm".

Reaccion (Ec. 4.27 de la tesis):
    isobuteno (C4H8) + metanol (CH4O)  <->  MTBE (C5H12O)

Matriz de formula (version sin n-butano inerte, reducida de la Ec. 4.28
de la tesis, que si incluye el inerte). Se verifico que A*N=0 con esta
reduccion:
    A = [[1, 0, 1],      (elemento 1: "unidad isobuteno")
         [0, 1, 1]]      (elemento 2: "unidad metanol")
    componentes: [isobuteno, metanol, MTBE]
    N = [-1, -1, 1]   (coeficientes estequiometricos)
    NE = NC - NR = 3 - 1 = 2  (coincide con el NE=3 de la tesis cuando
    se incluyen los 4 componentes con n-butano; aqui NC=3 sin inerte).

=====================================================================
ADVERTENCIA SOBRE LOS DATOS NUMERICOS (leer antes de interpretar
resultados cuantitativos)
=====================================================================
Ni equilibrio.md ni el PDF de la tesis contienen los parametros de
Wilson, los coeficientes de Antoine ni la correlacion K_eq(T) que
Tsanas tomo de Ung and Doherty (1995e) para este sistema -- esos datos
viven en un paper externo que no esta disponible en esta sesion. Por
lo tanto este ejemplo NO reproduce numericamente la Tabla 4.13 ni las
Figuras 4.9-4.11 de la tesis. En su lugar:

  1. Se modela la fase liquida como SOLUCION IDEAL (gamma_i = 1) en vez
     de con el modelo de Wilson real del estudio. El modulo Wilson
     (termodinamica.gamma_wilson) esta implementado y probado de forma
     independiente (ver pruebas_validacion.py); basta con cambiar el
     "modelo_liquido" de este archivo a tipo "liquido_wilson" con una
     matriz Lambda real si se consiguen los parametros de Ung and
     Doherty (1995e).
  2. Las presiones de vapor se estiman con Clausius-Clapeyron
     simplificado (ver psat_clausius_clapeyron), calibrado unicamente
     con el punto de ebullicion normal de cada compuesto (dato de
     manual, muy bien establecido) y una entalpia de vaporizacion
     tipica aproximada -- NO son coeficientes de Antoine ajustados de
     una fuente verificada para este trabajo.
  3. La constante de equilibrio K_eq(320.92 K) se fija en un valor
     ILUSTRATIVO (ver KEQ_ILUSTRATIVO mas abajo), elegido solo para dar
     una conversion razonable de isobuteno, NO el valor real reportado
     por Ung and Doherty (1995e).

La validacion de la Fase 3 (ver el bloque principal al final de este
archivo) se apoya, por lo tanto, en:
  (a) el acuerdo mutuo entre los dos algoritmos del paper (SSA vs.
      combinado) sobre este MISMO problema -- si ambos coinciden,
      confirma que las Ec. 3.46 y 3.68 estan implementadas de forma
      consistente entre si;
  (b) una verificacion independiente por minimizacion directa de
      Gibbs con scipy.optimize (metodo totalmente distinto al de la
      tesis), que no depende de ninguna de las ecuaciones 3.14-3.70;
  (c) el chequeo fenomenologico cualitativo que la tesis SI reporta en
      prosa (pag. 64): la reaccion no puede alcanzar MTBE puro en
      ninguna fase, y con exceso de metanol el isobuteno (reactivo
      limitante) se consume casi en su totalidad.
"""

import numpy as np
from scipy.optimize import minimize

from algoritmos import successive_substitution_algorithm, combined_algorithm
from termodinamica import gibbs_reducida, ln_Gamma_fase


# ---------------------------------------------------------------------------
# 1. Definicion del sistema (estequiometria verificada: A @ N = 0)
# ---------------------------------------------------------------------------

COMPONENTES = ["isobuteno", "metanol", "MTBE"]
A = np.array([
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 1.0],
])
N = np.array([-1.0, -1.0, 1.0])
assert np.allclose(A @ N, 0.0), "La matriz de formula no es consistente con N"

T = 320.92  # K (punto citado en la tesis, pag. 65, como el del azeotropo)
P0 = 1.01325  # bar, presion de referencia (1 atm)
P = 1.01325  # bar, presion del sistema (1 atm)

# Alimentacion: isobuteno:metanol = 1:1.1, sin MTBE, base 1+1.1=2.1 mol.
n_feed = np.array([1.0, 1.1, 0.0])
b = A @ n_feed


# ---------------------------------------------------------------------------
# 2. Propiedades termodinamicas (ver advertencia en el docstring)
# ---------------------------------------------------------------------------

# Puntos de ebullicion normales (dato de manual, bien establecido) y
# entalpias de vaporizacion TIPICAS aproximadas (valores de referencia
# generales de literatura, no ajustados especificamente a este trabajo).
TB = {"isobuteno": 266.25, "metanol": 337.85, "MTBE": 328.35}       # K
DHVAP = {"isobuteno": 22200.0, "metanol": 35300.0, "MTBE": 31900.0}  # J/mol
R_GAS = 8.314  # J/(mol K)


def psat_clausius_clapeyron(T, componente):
    """
    Presion de vapor aproximada por Clausius-Clapeyron con entalpia de
    vaporizacion constante, calibrada para que Psat(Tb) = 1 atm:

        ln(Psat/p0) = -(DHvap/R) * (1/T - 1/Tb)

    Esto NO sustituye una correlacion de Antoine ajustada a datos
    experimentales; es una aproximacion de orden cero suficiente para
    dar presiones de vapor con la tendencia correcta en el rango de
    interes (ver advertencia al inicio del archivo).
    """
    Tb = TB[componente]
    dH = DHVAP[componente]
    return P0 * np.exp(-(dH / R_GAS) * (1.0 / T - 1.0 / Tb))


Psat_T = np.array([psat_clausius_clapeyron(T, c) for c in COMPONENTES])

# Constante de equilibrio ILUSTRATIVA a 320.92 K (ver advertencia).
KEQ_ILUSTRATIVO = 50.0

# Gauge de referencia: g_isobuteno = g_metanol = 0, g_MTBE = -ln(Keq),
# de forma que sum_i nu_i * g_i = g_MTBE = -ln(Keq) (ver termodinamica.py).
g = np.array([0.0, 0.0, -np.log(KEQ_ILUSTRATIVO)])

modelo_vapor = {"tipo": "vapor_ideal", "p": P, "p0": P0}
modelo_liquido = {"tipo": "liquido_ideal", "Psat": Psat_T, "p0": P0}


# ---------------------------------------------------------------------------
# 3. Verificacion independiente: minimizacion directa de Gibbs (scipy)
# ---------------------------------------------------------------------------

def verificar_con_scipy(n_fases_inicial, modelos_fase, g, A, b):
    """
    Resuelve el MISMO problema de equilibrio quimico y de fases
    minimizando G/(RT) directamente con scipy.optimize.minimize
    (SLSQP), sujeta a la restriccion de balance de elementos
    A @ (n_1 + n_2 + ... ) = b y n_ik >= 0.

    Esto NO usa ninguna de las ecuaciones de Tsanas (3.14-3.70): es un
    metodo de optimizacion generico e independiente, usado solo para
    confirmar que la solucion de los algoritmos no-estequiometricos es
    efectivamente un minimo de Gibbs.

    Retorna
    -------
    n_fases_opt : list[ndarray]
    G_RT_opt : float
    """
    NP = len(n_fases_inicial)
    nc = len(g)
    x0 = np.concatenate(n_fases_inicial)

    def _desempacar(n_flat):
        return [n_flat[k * nc:(k + 1) * nc] for k in range(NP)]

    def objetivo(n_flat):
        n_fases = _desempacar(n_flat)
        ln_Gamma_fases = []
        for n_k, modelo in zip(n_fases, modelos_fase):
            n_t_k = max(np.sum(n_k), 1e-12)
            x_k = n_k / n_t_k
            ln_Gamma_fases.append(ln_Gamma_fase(
                modelo["tipo"], x_k, p=modelo.get("p"), p0=modelo.get("p0"),
                Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
            ))
        return gibbs_reducida(n_fases, g, ln_Gamma_fases)

    def restriccion_balance(n_flat):
        n_fases = _desempacar(n_flat)
        return A @ sum(n_fases) - b

    restricciones = {"type": "eq", "fun": restriccion_balance}
    limites = [(1e-10, None)] * len(x0)

    resultado = minimize(
        objetivo, x0, method="SLSQP", bounds=limites,
        constraints=[restricciones], options={"maxiter": 500, "ftol": 1e-12},
    )
    n_fases_opt = _desempacar(resultado.x)
    return n_fases_opt, resultado.fun, resultado.success


# ---------------------------------------------------------------------------
# 4. Ejecucion de los dos algoritmos y comparacion
# ---------------------------------------------------------------------------

def _reporte_fase(nombre, n_k, componentes):
    n_t = np.sum(n_k)
    x = n_k / n_t
    print(f"  {nombre}: n_t = {n_t:.6f} mol")
    for comp, xi in zip(componentes, x):
        print(f"      x_{comp:10s} = {xi:.6f}")


def ejecutar_caso(p_sistema, etiqueta):
    """
    Resuelve el caso MTBE a la presion p_sistema (bar) con ambos
    algoritmos, los compara entre si y contra una minimizacion directa
    de Gibbs con scipy (metodo independiente de las Ec. 3.14-3.70).
    """
    modelo_vapor_caso = {"tipo": "vapor_ideal", "p": p_sistema, "p0": P0}

    print("=" * 70)
    print(f"{etiqueta}  (T = {T:.2f} K, p = {p_sistema:.5f} bar)")
    print("Alimentacion: isobuteno=%.2f mol, metanol=%.2f mol" % (n_feed[0], n_feed[1]))
    print("K_eq ilustrativo = %.2f (ver advertencia en el docstring)" % KEQ_ILUSTRATIVO)
    print("=" * 70)

    resultado_ssa = successive_substitution_algorithm(
        A, b, n_t_fase_inicial=np.sum(n_feed), modelo_fase_inicial=modelo_liquido,
        g=g, modelos_trial_candidatos=[modelo_vapor_caso, modelo_liquido],
    )
    print("\n--- Successive substitution algorithm ---")
    print(f"Estable: {resultado_ssa['estable']}  |  "
          f"Fases finales: {len(resultado_ssa['n_fases'])}  |  "
          f"Iteraciones externas por fase: {resultado_ssa['historial_fases']}")
    for k, n_k in enumerate(resultado_ssa["n_fases"]):
        _reporte_fase(f"Fase {k+1}", n_k, COMPONENTES)

    resultado_ca = combined_algorithm(
        A, b, n_t_fase_inicial=np.sum(n_feed), modelo_fase_inicial=modelo_liquido,
        g=g, modelos_trial_candidatos=[modelo_vapor_caso, modelo_liquido],
    )
    print("\n--- Combined algorithm ---")
    print(f"Estable: {resultado_ca['estable']}  |  "
          f"Fases finales: {len(resultado_ca['n_fases'])}  |  "
          f"Metodo final: {resultado_ca['metodo_final']}  |  "
          f"Iteraciones externas por fase: {resultado_ca['historial_fases']}")
    for k, n_k in enumerate(resultado_ca["n_fases"]):
        _reporte_fase(f"Fase {k+1}", n_k, COMPONENTES)

    print("\n--- Comparacion SSA vs. combinado (deben coincidir) ---")
    if len(resultado_ssa["n_fases"]) == len(resultado_ca["n_fases"]):
        for k, (n_ssa, n_ca) in enumerate(zip(resultado_ssa["n_fases"], resultado_ca["n_fases"])):
            diferencia = np.max(np.abs(n_ssa - n_ca))
            print(f"  Fase {k+1}: max|n_SSA - n_CA| = {diferencia:.3e} mol")
    else:
        print("  Los dos algoritmos convergieron a un numero distinto de fases.")

    print("\n--- Verificacion independiente (minimizacion directa de Gibbs, scipy) ---")
    n_fases_scipy, G_RT_scipy, exito = verificar_con_scipy(
        resultado_ca["n_fases"], resultado_ca["modelos_fase"], g, A, b,
    )
    print(f"  scipy.optimize exito: {exito}  |  G/RT = {G_RT_scipy:.8f}")
    for k, n_k in enumerate(n_fases_scipy):
        _reporte_fase(f"Fase {k+1} (scipy)", n_k, COMPONENTES)

    ln_Gamma_ca = [
        ln_Gamma_fase(m["tipo"], n_k / np.sum(n_k), p=m.get("p"), p0=m.get("p0"),
                      Psat=m.get("Psat"), Lambda=m.get("Lambda"))
        for m, n_k in zip(resultado_ca["modelos_fase"], resultado_ca["n_fases"])
    ]
    G_RT_ca = gibbs_reducida(resultado_ca["n_fases"], g, ln_Gamma_ca)
    print(f"  G/RT (combined_algorithm) = {G_RT_ca:.8f}  |  "
          f"diferencia con scipy = {abs(G_RT_ca - G_RT_scipy):.3e}")

    print("\n--- Chequeo cualitativo contra la narrativa de la tesis (pag. 64) ---")
    print("  La tesis indica que el MTBE puro no puede alcanzarse en ninguna fase")
    print("  (debido al equilibrio quimico) y que el isobuteno, al ser el reactivo")
    print("  limitante con exceso de metanol, se consume casi en su totalidad.")
    for k, n_k in enumerate(resultado_ca["n_fases"]):
        x = n_k / np.sum(n_k)
        print(f"  Fase {k+1}: x_MTBE = {x[2]:.4f} (< 1, consistente), "
              f"x_isobuteno = {x[0]:.6f} (resto sin convertir)")
    print()
    return resultado_ssa, resultado_ca


if __name__ == "__main__":
    # Caso 1: p = 1 atm (igual que la tesis). Con nuestras propiedades
    # ilustrativas, el liquido resulta subenfriado (su presion de burbuja
    # estimada es menor a 1 atm) y la solucion de equilibrio es monofasica
    # (solo liquido) -- un resultado fisicamente correcto para ESTOS datos,
    # aunque no reproduce el VLE bifasico que Tsanas reporta con los datos
    # reales de Ung and Doherty (1995e).
    ejecutar_caso(P, "CASO 1: p = 1 atm (igual que la tesis)")

    # Caso 2: p = 0.80 bar. Con esta presion mas baja (dentro de la region
    # de dos fases implicada por nuestras propiedades ilustrativas) se
    # obtiene un verdadero equilibrio liquido-vapor con reaccion, que
    # ejercita la logica completa de deteccion de inestabilidad y adicion
    # de fase (seccion 3.1.3 / Figura 3.1).
    ejecutar_caso(0.80, "CASO 2: p = 0.80 bar (VLE bifasico genuino)")
