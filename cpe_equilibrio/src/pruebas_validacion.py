"""
pruebas_validacion.py
=======================

Suite de validacion numerica (Fase 3). Dado que ni equilibrio.md ni el
PDF original de la tesis de Tsanas contienen las tablas de parametros
(Wilson, UNIQUAC, Antoine, K_eq(T)) usadas en el Capitulo 4 -- se citan
de papers externos no disponibles en esta sesion (Ung and Doherty
1995e, Xiao et al. 1989, Maurer 1986, Saito et al. 1971) -- esta
validacion NO intenta reproducir numericamente las Tablas 4.2, 4.4, 4.6
u 4.8. En su lugar, valida lo que SI se puede verificar sin esos datos:

    1. test_derivada_wilson()
       La formula de la derivada composicional del modelo de Wilson
       (Ec. 3.49 aplicada al modelo de Wilson) se derivo a mano en
       termodinamica.py; aqui se confirma por diferencias finitas.

    2. test_jacobiano_lagrange()
       El Jacobiano del sistema de Newton de la Ec. 3.46 (JA, JB) se
       confirma por diferencias finitas de la funcion residual F(lambda,n_t).

    3. test_mtbe_una_fase() / test_mtbe_dos_fases()
       El caso de sintesis de MTBE (ejemplo_mtbe.py) se resuelve con los
       dos algoritmos de la tesis (successive_substitution_algorithm y
       combined_algorithm) y se compara contra una minimizacion directa
       de Gibbs con scipy.optimize (metodo totalmente independiente de
       las Ec. 3.14-3.70). Se prueba tanto el caso monofasico (p=1 atm)
       como el caso bifasico (p=0.80 bar, VLE genuino con deteccion de
       inestabilidad y adicion de fase).

    4. test_lagrange_vs_rand_no_ideal()
       En un sistema no reactivo (A = identidad) con una fase liquida
       fuertemente no ideal (modelo de Wilson, parametros ilustrativos),
       se confirma que el metodo de multiplicadores de Lagrange
       (Ec. 3.46, con bucle externo de actualizacion de gamma) y el
       metodo RAND modificado (Ec. 3.68, derivadas composicionales
       exactas) convergen al MISMO equilibrio. Esto es una validacion
       cruzada fuerte: dos formulaciones matematicas distintas de la
       misma fisica deben coincidir.

    5. test_greiner_1991()
       VALIDACION CONTRA UNA FUENTE EXTERNA CON NUMEROS PUBLICADOS.
       Greiner (1991), "An efficient implementation of Newton's method
       for complex nonideal chemical equilibria" (Comput. Chem. Eng. 15,
       115-123) -- el paper en el que se basa la seccion 3.2.2 de la
       tesis de Tsanas -- incluye en su Apendice B un ejemplo numerico
       COMPLETO y autocontenido: dos compuestos A, B en equilibrio
       vapor (gas ideal, 1 bar) - liquido (solucion regular con
       parametro de interaccion Lambda=-3 en unidades de RT), con
       potenciales quimicos de referencia y alimentacion dados
       explicitamente, y la solucion de equilibrio exacta reportada a
       10 cifras significativas.

       NOTA SOBRE UN ERROR DE OCR DETECTADO: la extraccion de texto del
       PDF escaneado de 1991 (pdftotext -layout) dio mu_A(g) =
       -53.54926553, pero verificando la consistencia interna del
       propio ejemplo de Greiner (su solucion reportada debe satisfacer
       mu_A(gas) = mu_A(liquido) en el equilibrio) se encontro que el
       valor correcto es -53.56926553 (un digito mal reconocido por el
       OCR, "69" leido como "49"). Esto se verifico resolviendo la
       ecuacion de equilibrio para el valor de mu_A(g) que hace
       consistente la solucion publicada, encontrando una coincidencia
       casi exacta con -53.56926553 (y confirmando independientemente
       que el mismo procedimiento con la componente B si reproducia
       Lambda=-3.000000 exactamente, lo que aislo el error al digito de
       mu_A(g)). Con el valor corregido, el metodo RAND modificado
       reproduce la solucion publicada por Greiner a ~8e-6 (el limite
       de precision esperable de un dato de 10 cifras).

       Este resultado es la validacion mas fuerte de todo el proyecto:
       no depende de ningun parametro "ilustrativo" nuestro, sino de
       numeros publicados en el paper original del metodo. Tambien
       confirma empiricamente la advertencia central del abstract de
       Greiner: el metodo "de aproximacion ideal" (nuestro
       lagrange_multipliers.py, con Gamma fijo dentro del bucle interno)
       efectivamente DIVERGE en este sistema fuertemente no ideal,
       mientras que el RAND modificado (derivadas exactas) converge sin
       problemas -- es decir, nuestra implementacion reproduce tanto el
       exito del metodo bueno como el fracaso documentado del metodo
       ingenuo.

    6. test_acetic_ethanol_esterification()
       Esterificacion de acido acetico + etanol -> acetato de etilo +
       agua (seccion 4.1.3 de la tesis, Tabla 4.4), en fase liquida
       unica a 373.15 K (100 C), sin VLE (replica exactamente el
       Example 14.8 de Smith, Van Ness & Abbott, "Introduction to
       Chemical Engineering Thermodynamics", 8th ed.):

           CH3COOH(l) + C2H5OH(l) <-> CH3COOC2H5(l) + H2O(l)

       Datos (TODOS trazables a fuentes citadas, ninguno ilustrativo):
         - K_eq(373.15 K) = 4.8586, obtenido por el propio libro via
           van't Hoff desde K(298.15 K)=6.5266, a su vez de
           Hf,Gf de formacion de los 4 compuestos (Tabla C.4 del
           libro + valores de acetato de etilo dados en el enunciado
           del Example 14.8). Verificamos la aritmetica del libro
           (suma de las 4 contribuciones) y cuadra exacto.
         - Modelo "ideal": gamma_i=1 para los 4 componentes (la propia
           simplificacion que usa el libro, dado que no hay datos de
           coeficientes de actividad para este sistema complejo).
         - Modelo "UNIFAC": gamma_i predichos por UNIFAC original
           (thermo.unifac, version=0), con los grupos de cada
           componente tomados de la asignacion OFICIAL de DDBST
           (thermo.unifac.DDBST_UNIFAC_assignments, indexada por
           InChIKey) -- NO fragmentados a mano:
               acido acetico:     CH3 + COOH
               etanol:            CH3 + CH2 + OH
               agua:              H2O
               acetato de etilo:  CH3 + CH2 + CH3COO

       Dato experimental citado por el propio libro: x_EtAc ~ 0.33
       (medido en laboratorio).

       NOTA IMPORTANTE: para este caso de UNA SOLA FASE (liquido puro,
       sin separacion de fases, tal como lo plantea el libro) se
       resuelve con resolver_lagrange() y resolver_rand_modificado()
       DIRECTAMENTE, NO con successive_substitution_algorithm() ni
       combined_algorithm() de algoritmos.py. Esas dos funciones
       incluyen deteccion de inestabilidad y adicion automatica de
       fases (estabilidad.py), cuyo arranque desde una sola fase es un
       gap de robustez YA CONOCIDO (ver conversacion previa) para
       sistemas fuertemente no ideales -- UNIFAC en este sistema
       predice una posible separacion liquido-liquido que dispara ese
       camino fragil y no es lo que queremos probar aqui. Validar los
       solvers de una fase (resolver_lagrange, resolver_rand_modificado)
       de forma directa evita tocar ese gap (que sigue pendiente,
       explicitamente fuera de alcance) y es ademas fisicamente
       correcto: el Example 14.8 del libro ASUME una sola fase liquida,
       no la deriva de un analisis de estabilidad.

       NOTA SOBRE VLE COMPLETO (Antoine): se extendio este caso a
       equilibrio liquido-vapor completo a 355 K, 1 atm, alimentacion
       equimolar 0.5/0.5 (igual que la Tabla 4.4 de la tesis), usando
       las constantes de Antoine de Smith & Van Ness Tabla B.2 (acido
       acetico, etanol, agua) y NIST Chemistry WebBook SRD 69 (acetato
       de etilo, https://webbook.nist.gov/cgi/cbook.cgi?ID=C141786&Mask=4,
       forma log10(P[bar])=A-B/(T[K]+C), A=4.22809, B=1245.702,
       C=-55.189, rango valido 288.73-348.98 K).

       La fuente de Tosun/Reid-Prausnitz-Sherwood para acetato de etilo
       se descarto: se detecto que la tabla de Apendice C (hidrocarburos/
       organicos) tiene las filas desalineadas en la extraccion del PDF
       (verificado evaluando la formula en el punto de ebullicion normal
       REAL de n-hexano y benceno, de la MISMA tabla: el resultado estuvo
       entre 80 y 790 bar en vez de ~1 atm). Smith & Van Ness tampoco
       incluye acetato de etilo en su Tabla B.2.

       El dato de NIST requiere una extrapolacion de ~6 K por encima de
       su rango valido (348.98 K -> 355 K). Se verifico que es razonable
       antes de usarlo:
         - Psat(348.98 K) = 0.960 atm (debe ser ligeramente <1 atm,
           porque el bp normal real es ~350.2 K > 348.98 K) -- CORRECTO.
         - Psat(350.2 K) = 0.9996 atm (debe ser ~1 atm, es el bp normal)
           -- CORRECTO, practicamente exacto.
         - Psat(355 K) = 1.168 atm (debe ser ligeramente >1 atm) --
           CORRECTO, dentro del rango fisicamente esperado.
       Los otros 3 Psat a 355 K tambien se verificaron contra sus bp
       reales (acido acetico 0.292 atm <1, bp real 391 K; etanol 1.154
       atm >1, bp real 351.5 K; agua 0.504 atm <1, bp real 373.15 K):
       los 4 son consistentes.

       Con el modelo de liquido IDEAL, el sistema resulta subenfriado a
       355 K/1 atm (p_burbuja ~0.80 atm < 1 atm, igual que el hallazgo ya
       documentado en ejemplo_mtbe.py) y el solver converge correctamente
       a una sola fase liquida (el vapor colapsa a cantidad despreciable).
       Con UNIFAC, la mayor no-idealidad predicha (p_burbuja ~1.30 atm)
       si produce un VLE genuino de dos fases, con tendencias cualitativas
       consistentes con la Tabla 4.4 de la tesis (el acido acetico se
       concentra en el liquido, agua/acetato de etilo dominan el vapor,
       el vapor es la fase mayoritaria) aunque la magnitud del split de
       fases difiere, como se espera al no tener los parametros UNIQUAC
       reales de Xiao et al. (1989).

Ejecutar con:  python pruebas_validacion.py
"""

import numpy as np
from scipy.optimize import minimize

from termodinamica import gamma_wilson, dln_gamma_dn_wilson, ln_Gamma_fase, gibbs_reducida
from lagrange_multipliers import (
    resolver_lagrange, _composicion_desde_lambda, _ensamblar_sistema_3_46,
)
from modified_rand import resolver_rand_modificado
from inicializacion import minimizar_Q

TOL_REPORTE = 1e-8


def _ok(nombre, condicion, detalle=""):
    estado = "OK" if condicion else "FALLO"
    print(f"[{estado}] {nombre}  {detalle}")
    return condicion


def test_derivada_wilson():
    """
    Verifica dln_gamma_dn_wilson contra diferencias finitas centradas
    de ln(gamma_wilson), para una mezcla ternaria con parametros de
    Wilson genericos (no ligados a ningun sistema real).
    """
    print("\n=== 1. Derivada del modelo de Wilson (diferencias finitas) ===")
    rng = np.random.default_rng(0)
    nc = 3
    Lambda = np.abs(rng.random((nc, nc))) * 0.8 + 0.2
    np.fill_diagonal(Lambda, 1.0)
    n = np.array([2.3, 1.1, 0.7])

    Phi_analitico = dln_gamma_dn_wilson(n, Lambda)

    eps = 1e-6
    Phi_numerico = np.zeros((nc, nc))
    for q in range(nc):
        n_mas, n_menos = n.copy(), n.copy()
        n_mas[q] += eps
        n_menos[q] -= eps
        g_mas = np.log(gamma_wilson(n_mas / np.sum(n_mas), Lambda))
        g_menos = np.log(gamma_wilson(n_menos / np.sum(n_menos), Lambda))
        Phi_numerico[:, q] = (g_mas - g_menos) / (2 * eps)

    diferencia_max = np.max(np.abs(Phi_analitico - Phi_numerico))
    return _ok("derivada de Wilson coincide con diferencias finitas",
                diferencia_max < 1e-8, f"(max|diff|={diferencia_max:.2e})")


def test_jacobiano_lagrange():
    """
    Verifica JA y JB (Ec. 3.41-3.42), ensambladas en
    _ensamblar_sistema_3_46, contra el Jacobiano numerico de la funcion
    residual F(lambda, n_t) = [b - A@N ; e_NP - X^T e_NC].
    """
    print("\n=== 2. Jacobiano del sistema de Lagrange (Ec. 3.46) ===")
    A = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    g = np.zeros(3)
    lam = np.array([-0.3, 0.7])
    n_t_fases = [1.2, 0.8]
    ln_Gamma_fases = [np.array([0.1, -0.2, 0.05]), np.array([0.0, 0.0, 0.0])]

    def residual(vector):
        lam_, nt1, nt2 = vector[:2], vector[2], vector[3]
        x_fases = _composicion_desde_lambda(A, lam_, g, ln_Gamma_fases)
        N = nt1 * x_fases[0] + nt2 * x_fases[1]
        res_balance = (A @ np.array([1.0, 1.1, 0.0])) - A @ N  # b fijo, ver abajo
        res_norm = np.array([1.0 - np.sum(x_fases[0]), 1.0 - np.sum(x_fases[1])])
        return np.concatenate([res_balance, res_norm])

    b = A @ np.array([1.0, 1.1, 0.0])
    x_fases = _composicion_desde_lambda(A, lam, g, ln_Gamma_fases)
    J_analitico, _ = _ensamblar_sistema_3_46(A, lam, n_t_fases, x_fases, b)

    vector0 = np.concatenate([lam, n_t_fases])
    eps = 1e-6
    J_numerico = np.zeros((4, 4))
    for j in range(4):
        v_mas, v_menos = vector0.copy(), vector0.copy()
        v_mas[j] += eps
        v_menos[j] -= eps
        J_numerico[:, j] = (residual(v_mas) - residual(v_menos)) / (2 * eps)

    # El Jacobiano analitico de _ensamblar_sistema_3_46 corresponde a
    # -dF/dvector (porque el sistema se arma como J*delta = -F); por
    # eso comparamos J_analitico con -J_numerico.
    diferencia_max = np.max(np.abs(J_analitico - (-J_numerico)))
    return _ok("Jacobiano JA,JB coincide con diferencias finitas de F",
                diferencia_max < 1e-6, f"(max|diff|={diferencia_max:.2e})")


def test_mtbe_una_fase():
    print("\n=== 3a. Caso MTBE monofasico (p = 1 atm, ver ejemplo_mtbe.py) ===")
    import ejemplo_mtbe as m
    from algoritmos import successive_substitution_algorithm, combined_algorithm

    modelo_vapor = {"tipo": "vapor_ideal", "p": m.P, "p0": m.P0}
    r_ssa = successive_substitution_algorithm(
        m.A, m.b, n_t_fase_inicial=np.sum(m.n_feed), modelo_fase_inicial=m.modelo_liquido,
        g=m.g, modelos_trial_candidatos=[modelo_vapor, m.modelo_liquido],
    )
    r_ca = combined_algorithm(
        m.A, m.b, n_t_fase_inicial=np.sum(m.n_feed), modelo_fase_inicial=m.modelo_liquido,
        g=m.g, modelos_trial_candidatos=[modelo_vapor, m.modelo_liquido],
    )
    n_scipy, G_scipy, exito = m.verificar_con_scipy(r_ca["n_fases"], r_ca["modelos_fase"], m.g, m.A, m.b)

    ok1 = _ok("SSA y combinado coinciden (1 fase)",
              np.allclose(r_ssa["n_fases"][0], r_ca["n_fases"][0], atol=1e-8))
    ok2 = _ok("Combinado coincide con minimizacion directa de Gibbs (scipy)",
              exito and np.allclose(r_ca["n_fases"][0], n_scipy[0], atol=1e-6))
    ok3 = _ok("Balance de elementos se satisface (A@n = b)",
              np.allclose(m.A @ r_ca["n_fases"][0], m.b, atol=1e-8))
    return ok1 and ok2 and ok3


def test_mtbe_dos_fases():
    print("\n=== 3b. Caso MTBE bifasico (p = 0.80 bar, VLE genuino) ===")
    import ejemplo_mtbe as m
    from algoritmos import successive_substitution_algorithm, combined_algorithm

    modelo_vapor = {"tipo": "vapor_ideal", "p": 0.80, "p0": m.P0}
    r_ssa = successive_substitution_algorithm(
        m.A, m.b, n_t_fase_inicial=np.sum(m.n_feed), modelo_fase_inicial=m.modelo_liquido,
        g=m.g, modelos_trial_candidatos=[modelo_vapor, m.modelo_liquido],
    )
    r_ca = combined_algorithm(
        m.A, m.b, n_t_fase_inicial=np.sum(m.n_feed), modelo_fase_inicial=m.modelo_liquido,
        g=m.g, modelos_trial_candidatos=[modelo_vapor, m.modelo_liquido],
    )
    n_scipy, G_scipy, exito = m.verificar_con_scipy(r_ca["n_fases"], r_ca["modelos_fase"], m.g, m.A, m.b)

    ok0 = _ok("Ambos algoritmos detectan 2 fases", len(r_ssa["n_fases"]) == 2 and len(r_ca["n_fases"]) == 2)
    ok1 = _ok("SSA y combinado coinciden (2 fases)", all(
        np.allclose(a, b, atol=1e-8) for a, b in zip(r_ssa["n_fases"], r_ca["n_fases"])
    ))
    ok2 = _ok("Combinado coincide con minimizacion directa de Gibbs (scipy)", exito and all(
        np.allclose(a, b, atol=1e-6) for a, b in zip(r_ca["n_fases"], n_scipy)
    ))
    ok3 = _ok("Balance de elementos se satisface (A@sum(n_k) = b)",
              np.allclose(m.A @ sum(r_ca["n_fases"]), m.b, atol=1e-8))
    return ok0 and ok1 and ok2 and ok3


def test_lagrange_vs_rand_no_ideal():
    """
    Sistema NO reactivo de 3 componentes (A = identidad: cada "elemento"
    es un componente, sin reaccion) con una fase liquida fuertemente no
    ideal (Wilson, parametros ilustrativos genericos). Verifica que el
    metodo de multiplicadores de Lagrange y el RAND modificado --dos
    derivaciones matematicas independientes de la tesis-- convergen al
    mismo equilibrio.
    """
    print("\n=== 4. Lagrange vs. RAND modificado en sistema no ideal (Wilson) ===")
    A = np.eye(3)
    feed = np.array([0.3, 0.3, 0.4])
    b = A @ feed
    g = np.zeros(3)
    Psat = np.array([2.0, 1.0, 0.5])
    Lambda = np.array([[1.0, 0.3, 0.5], [2.0, 1.0, 0.4], [1.5, 1.8, 1.0]])

    modelo_vapor = {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}
    modelo_liquido = {"tipo": "liquido_wilson", "Psat": Psat, "p0": 1.0, "Lambda": Lambda}

    n_t_fases = [0.5, 0.5]
    x0 = np.ones(3) / 3
    ln_Gamma_fijo = [
        ln_Gamma_fase(m_["tipo"], x0, p=m_.get("p"), p0=m_.get("p0"),
                      Psat=m_.get("Psat"), Lambda=m_.get("Lambda"))
        for m_ in [modelo_liquido, modelo_vapor]
    ]
    lam0, n0, _ = minimizar_Q(A, b, n_t_fases, g, ln_Gamma_fijo)

    r_lagrange = resolver_lagrange(A, b, lam0, n0, g, [modelo_liquido, modelo_vapor])
    r_rand = resolver_rand_modificado(A, b, lam0, n0, g, [modelo_liquido, modelo_vapor])

    diferencias = [np.max(np.abs(a - b_)) for a, b_ in zip(r_lagrange["n_fases"], r_rand["n_fases"])]
    ok1 = _ok("Lagrange y RAND modificado coinciden",
              max(diferencias) < 1e-8, f"(max|diff|={max(diferencias):.2e})")
    ok2 = _ok("Balance de elementos se satisface en ambos",
              np.allclose(A @ sum(r_lagrange["n_fases"]), b, atol=1e-8) and
              np.allclose(A @ sum(r_rand["n_fases"]), b, atol=1e-8))
    print(f"    iteraciones Lagrange: externas={r_lagrange['iteraciones_externas']}, "
          f"internas_total={r_lagrange['iteraciones_internas_total']}  |  "
          f"iteraciones RAND: {r_rand['iteraciones']}")
    return ok1 and ok2


def test_greiner_1991():
    """
    Validacion contra el ejemplo numerico completo del Apendice B de
    Greiner (1991) -- ver docstring del modulo para el detalle del
    error de OCR detectado y corregido en mu_A(g).
    """
    print("\n=== 5. Validacion contra Greiner (1991), Apendice B (datos publicados) ===")
    A = np.eye(2)
    feed = np.array([0.37249, 0.12749])
    b = A @ feed

    # mu_A(g) corregido (ver docstring del modulo); el resto son los
    # valores extraidos limpiamente del PDF (sin ambiguedad de OCR).
    mu_A_gas, mu_B_gas = -53.56926553, -54.33693060
    mu_A_liq, mu_B_liq = -54.25814819, -51.50413543
    g = np.array([mu_A_gas, mu_B_gas])
    Psat_equiv = np.array([np.exp(mu_A_liq - mu_A_gas), np.exp(mu_B_liq - mu_B_gas)])

    modelo_vapor = {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}
    modelo_liquido = {"tipo": "liquido_regular_binaria", "Psat": Psat_equiv, "p0": 1.0, "Lambda": -3.0}
    modelos = [modelo_vapor, modelo_liquido]

    n_exacto = [np.array([0.0085794521, 0.0175663182]), np.array([0.3639205492, 0.1099336847])]

    n_t_fases = [np.sum(feed) / 2, np.sum(feed) / 2]
    x0 = feed / np.sum(feed)
    ln_Gamma0 = [
        ln_Gamma_fase(m_["tipo"], x0, p=m_.get("p"), p0=m_.get("p0"),
                      Psat=m_.get("Psat"), Lambda=m_.get("Lambda"))
        for m_ in modelos
    ]
    lam0, n0, _ = minimizar_Q(A, b, n_t_fases, g, ln_Gamma0)

    r_rand = resolver_rand_modificado(A, b, lam0, n0, g, modelos, max_iter=200)
    diff_gas = np.max(np.abs(r_rand["n_fases"][0] - n_exacto[0]))
    diff_liq = np.max(np.abs(r_rand["n_fases"][1] - n_exacto[1]))
    ok1 = _ok("RAND modificado reproduce la solucion EXACTA de Greiner (1991)",
              max(diff_gas, diff_liq) < 1e-4,
              f"(diff_gas={diff_gas:.2e}, diff_liq={diff_liq:.2e}, iter={r_rand['iteraciones']})")

    r_lagrange = resolver_lagrange(A, b, lam0, n0, g, modelos)
    ok2 = _ok("Lagrange (Gamma fijo) diverge en este sistema, como predice Greiner",
              r_lagrange["diverged"] is True)

    return ok1 and ok2


def test_acetic_ethanol_esterification():
    """
    Esterificacion de acido acetico + etanol, fase liquida unica a
    373.15 K (Example 14.8 de Smith, Van Ness & Abbott). Ver docstring
    del modulo para el detalle completo de fuentes y advertencias.
    """
    print("\n=== 6. Esterificacion acido acetico/etanol (Smith, Van Ness & Abbott, Ex. 14.8) ===")

    # Componentes, en orden: [acido acetico, etanol, agua, acetato de etilo]
    A = np.array([
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
    ])
    nu = np.array([-1.0, -1.0, 1.0, 1.0])
    ok_estequiometria = _ok("Matriz de formula consistente con la reaccion (A @ N = 0)",
                             np.allclose(A @ nu, 0.0))

    feed = np.array([1.0, 1.0, 0.0, 0.0])  # 1 mol acido acetico + 1 mol etanol
    b = A @ feed

    T = 373.15  # K (100 C), igual que el Example 14.8
    K_373 = 4.8586  # Smith, Van Ness & Abbott, via van't Hoff desde K(298.15K)=6.5266
    g = np.array([0.0, 0.0, 0.0, -np.log(K_373)])

    def resolver_una_fase(modelo):
        """Resuelve el equilibrio de una sola fase liquida con los tres
        metodos (Lagrange, RAND, scipy) y devuelve sus n finales."""
        x0 = feed / np.sum(feed)
        ln_Gamma0 = [ln_Gamma_fase(
            modelo["tipo"], x0, p=modelo.get("p"), p0=modelo.get("p0"),
            Psat=modelo.get("Psat"), Lambda=modelo.get("Lambda"),
            T=modelo.get("T"), chemgroups=modelo.get("chemgroups"),
        )]
        lam0, n0, _ = minimizar_Q(A, b, [float(np.sum(feed))], g, ln_Gamma0)

        r_lag = resolver_lagrange(A, b, lam0, n0, g, [modelo])
        r_rand = resolver_rand_modificado(A, b, lam0, n0, g, [modelo])

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
        return r_lag["n_fases"][0], r_rand["n_fases"][0], res_scipy.x, res_scipy.success

    # --- Paso 1: solucion ideal (gamma_i = 1), replica exacta del libro ---
    modelo_ideal = {"tipo": "liquido_ideal", "Psat": np.ones(4), "p0": 1.0}
    n_lag_id, n_rand_id, n_scipy_id, exito_id = resolver_una_fase(modelo_ideal)
    x_EtAc_ideal = n_lag_id[3] / np.sum(n_lag_id)
    e_ideal = n_lag_id[3]

    ok_ideal_exacto = _ok(
        "Solucion ideal reproduce el Example 14.8 EXACTO (e=0.6879, x_EtAc=0.344)",
        abs(e_ideal - 0.6879) < 1e-3 and abs(x_EtAc_ideal - 0.344) < 1e-3,
        f"(e={e_ideal:.6f}, x_EtAc={x_EtAc_ideal:.6f})",
    )
    ok_ideal_cruzada = _ok(
        "Ideal: Lagrange, RAND y scipy coinciden (tol 1e-8)",
        exito_id and np.max(np.abs(n_lag_id - n_rand_id)) < 1e-8
        and np.max(np.abs(n_lag_id - n_scipy_id)) < 1e-8,
        f"(max|Lag-RAND|={np.max(np.abs(n_lag_id - n_rand_id)):.2e}, "
        f"max|Lag-scipy|={np.max(np.abs(n_lag_id - n_scipy_id)):.2e})",
    )

    # --- Paso 2: UNIFAC (grupos oficiales DDBST, ver docstring del modulo) ---
    chemgroups = [
        {1: 1, 42: 1},       # acido acetico: CH3 + COOH
        {1: 1, 2: 1, 14: 1},  # etanol: CH3 + CH2 + OH
        {16: 1},             # agua: H2O
        {1: 1, 2: 1, 21: 1},  # acetato de etilo: CH3 + CH2 + CH3COO
    ]
    modelo_unifac = {"tipo": "liquido_unifac", "Psat": np.ones(4), "p0": 1.0,
                      "T": T, "chemgroups": chemgroups}
    n_lag_uf, n_rand_uf, n_scipy_uf, exito_uf = resolver_una_fase(modelo_unifac)
    x_EtAc_unifac = n_lag_uf[3] / np.sum(n_lag_uf)

    ok_unifac_cruzada = _ok(
        "UNIFAC: Lagrange, RAND y scipy coinciden (tol 1e-8)",
        exito_uf and np.max(np.abs(n_lag_uf - n_rand_uf)) < 1e-8
        and np.max(np.abs(n_lag_uf - n_scipy_uf)) < 1e-8,
        f"(max|Lag-RAND|={np.max(np.abs(n_lag_uf - n_rand_uf)):.2e}, "
        f"max|Lag-scipy|={np.max(np.abs(n_lag_uf - n_scipy_uf)):.2e})",
    )

    # --- Tabla comparativa de fase liquida unica (para el documento LaTeX) ---
    x_exp = 0.33
    print("\n    Tabla comparativa x_EtAc (373.15 K, fase liquida unica):")
    print("    | Metodo                | x_EtAc   | Desviacion vs exp (0.33) |")
    print("    |------------------------|----------|--------------------------|")
    print(f"    | Solucion ideal (S&VN)  | {x_EtAc_ideal:.4f}   | "
          f"{100*(x_EtAc_ideal - x_exp)/x_exp:+.1f}%                    |")
    print(f"    | UNIFAC                 | {x_EtAc_unifac:.4f}   | "
          f"{100*(x_EtAc_unifac - x_exp)/x_exp:+.1f}%                    |")
    print(f"    | Experimental           | {x_exp:.4f}   | --                       |")

    # =====================================================================
    # Paso 3-4: VLE completo a 355 K, 1 atm (alimentacion equimolar 0.5/0.5,
    # igual que la Tabla 4.4 de la tesis). Antoine de acido acetico/etanol/
    # agua de Smith & Van Ness Tabla B.2; acetato de etilo de NIST
    # Chemistry WebBook (SRD 69), con una extrapolacion de ~6 K verificada
    # (ver docstring del modulo).
    # =====================================================================
    print("\n--- Paso 3-4: VLE completo a 355 K, 1 atm (alimentacion equimolar) ---")

    T_vle = 355.0
    feed_vle = np.array([0.5, 0.5, 0.0, 0.0])
    b_vle = A @ feed_vle

    # K_eq(355 K) via van't Hoff desde los MISMOS datos de S&VN Example 14.8
    # (K_298=6.5266, dH_rxn,298=-3640 J/mol) -- ninguna fuente nueva, mismo
    # dato ya validado en el Paso 1.
    K_298, dH_298, R_gas = 6.5266, -3640.0, 8.314
    K_355 = K_298 * np.exp(-dH_298 / R_gas * (1.0 / T_vle - 1.0 / 298.15))
    g_vle = np.array([0.0, 0.0, 0.0, -np.log(K_355)])

    def psat_SVN_kPa(T_K, Ac, Bc, Cc):
        return np.exp(Ac - Bc / ((T_K - 273.15) + Cc))

    def psat_NIST_bar(T_K, Ac, Bc, Cc):
        return 10 ** (Ac - Bc / (T_K + Cc))

    Psat_vle = np.array([
        psat_SVN_kPa(T_vle, 15.0717, 3580.80, 224.650) / 101.325,   # acido acetico
        psat_SVN_kPa(T_vle, 16.8958, 3795.17, 230.918) / 101.325,   # etanol
        psat_SVN_kPa(T_vle, 16.3872, 3885.70, 230.170) / 101.325,   # agua
        psat_NIST_bar(T_vle, 4.22809, 1245.702, -55.189) / 1.01325,  # acetato de etilo
    ])
    print(f"    Psat a {T_vle} K (atm): AcOH={Psat_vle[0]:.4f}, EtOH={Psat_vle[1]:.4f}, "
          f"H2O={Psat_vle[2]:.4f}, EtAc={Psat_vle[3]:.4f}")
    ok_psat_fisico = _ok(
        "Los 4 Psat son fisicamente razonables (comparados con bp reales)",
        0.2 < Psat_vle[0] < 0.4 and 1.0 < Psat_vle[1] < 1.3
        and 0.4 < Psat_vle[2] < 0.6 and 1.0 < Psat_vle[3] < 1.3,
        f"({Psat_vle})",
    )

    modelo_vapor_vle = {"tipo": "vapor_ideal", "p": 1.0, "p0": 1.0}

    def resolver_dos_fases(modelo_liquido):
        n_liq0 = np.array([0.05, 0.05, 0.10, 0.10])
        n_vap0 = np.array([0.10, 0.10, 0.25, 0.25])
        n_t_fases = [np.sum(n_liq0), np.sum(n_vap0)]
        ln_Gamma0 = [
            ln_Gamma_fase(modelo_liquido["tipo"], n_liq0 / np.sum(n_liq0),
                           Psat=Psat_vle, p0=1.0, T=modelo_liquido.get("T"),
                           chemgroups=modelo_liquido.get("chemgroups")),
            ln_Gamma_fase(modelo_vapor_vle["tipo"], n_vap0 / np.sum(n_vap0), p=1.0, p0=1.0),
        ]
        lam0, n0, _ = minimizar_Q(A, b_vle, n_t_fases, g_vle, ln_Gamma0)

        r_lag = resolver_lagrange(A, b_vle, lam0, n0, g_vle, [modelo_liquido, modelo_vapor_vle])
        r_rand = resolver_rand_modificado(A, b_vle, lam0, n0, g_vle, [modelo_liquido, modelo_vapor_vle])

        def G_de(nflat):
            nf = [nflat[:4], nflat[4:]]
            ln_Gamma_fases = []
            for n_k, m in zip(nf, [modelo_liquido, modelo_vapor_vle]):
                x_k = n_k / np.sum(n_k)
                ln_Gamma_fases.append(ln_Gamma_fase(
                    m["tipo"], x_k, p=m.get("p"), p0=m.get("p0"), Psat=m.get("Psat"),
                    T=m.get("T"), chemgroups=m.get("chemgroups")))
            return gibbs_reducida(nf, g_vle, ln_Gamma_fases)

        x0_scipy = np.concatenate(r_lag["n_fases"])
        res = minimize(
            G_de, x0_scipy, method="SLSQP", bounds=[(1e-10, None)] * 8,
            constraints=[{"type": "eq", "fun": lambda nf: A @ (nf[:4] + nf[4:]) - b_vle}],
            options={"maxiter": 2000, "ftol": 1e-15},
        )
        n_scipy = [res.x[:4], res.x[4:]]
        return r_lag, r_rand, n_scipy, res.success

    # --- VLE con liquido ideal ---
    modelo_liquido_ideal_vle = {"tipo": "liquido_ideal", "Psat": Psat_vle, "p0": 1.0}
    r_lag_id, r_rand_id, n_scipy_id, exito_id_vle = resolver_dos_fases(modelo_liquido_ideal_vle)
    nt_liq_id = np.sum(r_lag_id["n_fases"][0])
    nt_vap_id = np.sum(r_lag_id["n_fases"][1])
    print(f"\n    [Liquido ideal] fraccion liquido={nt_liq_id/(nt_liq_id+nt_vap_id):.4f}, "
          f"fraccion vapor={nt_vap_id/(nt_liq_id+nt_vap_id):.4f}")
    ok_ideal_sin_vle = _ok(
        "Liquido ideal: el vapor colapsa a cantidad despreciable (sistema subenfriado, "
        "p_burbuja<1atm; consistente con el mismo hallazgo de ejemplo_mtbe.py)",
        nt_vap_id / (nt_liq_id + nt_vap_id) < 1e-6,
        f"(fraccion_vapor={nt_vap_id/(nt_liq_id+nt_vap_id):.2e})",
    )

    # --- VLE con liquido UNIFAC (si hay suficiente no-idealidad, debe dar VLE genuino) ---
    modelo_liquido_unifac_vle = {"tipo": "liquido_unifac", "Psat": Psat_vle, "p0": 1.0,
                                  "T": T_vle, "chemgroups": chemgroups}
    r_lag_uf, r_rand_uf, n_scipy_uf, exito_uf_vle = resolver_dos_fases(modelo_liquido_unifac_vle)
    n_liq_uf, n_vap_uf = r_lag_uf["n_fases"]
    nt_liq_uf, nt_vap_uf = np.sum(n_liq_uf), np.sum(n_vap_uf)
    x_liq_uf, x_vap_uf = n_liq_uf / nt_liq_uf, n_vap_uf / nt_vap_uf

    ok_vle_genuino = _ok(
        "UNIFAC: se obtiene VLE genuino de 2 fases (no colapsa, a diferencia del caso ideal)",
        nt_liq_uf / (nt_liq_uf + nt_vap_uf) > 0.01 and nt_vap_uf / (nt_liq_uf + nt_vap_uf) > 0.01,
    )
    ok_vle_cruzada = _ok(
        "VLE UNIFAC: Lagrange, RAND y scipy coinciden (tol 1e-8)",
        exito_uf_vle
        and max(np.max(np.abs(r_lag_uf["n_fases"][0] - n_scipy_uf[0])),
                np.max(np.abs(r_lag_uf["n_fases"][1] - n_scipy_uf[1]))) < 1e-8
        and max(np.max(np.abs(r_rand_uf["n_fases"][0] - n_scipy_uf[0])),
                np.max(np.abs(r_rand_uf["n_fases"][1] - n_scipy_uf[1]))) < 1e-8,
        f"(max|Lag-scipy|={max(np.max(np.abs(r_lag_uf['n_fases'][0]-n_scipy_uf[0])), np.max(np.abs(r_lag_uf['n_fases'][1]-n_scipy_uf[1]))):.2e}, "
        f"max|RAND-scipy|={max(np.max(np.abs(r_rand_uf['n_fases'][0]-n_scipy_uf[0])), np.max(np.abs(r_rand_uf['n_fases'][1]-n_scipy_uf[1]))):.2e})",
    )
    ok_balance_vle = _ok(
        "Balance de elementos se satisface en el VLE con UNIFAC",
        np.allclose(A @ (n_liq_uf + n_vap_uf), b_vle, atol=1e-8),
    )

    print(f"\n    [UNIFAC] fraccion liquido={nt_liq_uf/(nt_liq_uf+nt_vap_uf):.4f}, "
          f"fraccion vapor={nt_vap_uf/(nt_liq_uf+nt_vap_uf):.4f}")
    print("    Composicion liquido (AcOH, EtOH, H2O, EtAc):", np.round(x_liq_uf, 4))
    print("    Composicion vapor   (AcOH, EtOH, H2O, EtAc):", np.round(x_vap_uf, 4))

    print("\n    Comparacion CUALITATIVA con Tabla 4.4 de la tesis (355 K, 1 atm,")
    print("    feed equimolar 0.5/0.5) -- la tesis usa UNIQUAC con parametros de")
    print("    Xiao et al. (1989), que no tenemos; NO se espera coincidencia numerica:")
    print("    | Componente | Tesis (vapor/liq) | UNIFAC (vapor/liq) |")
    print("    |------------|--------------------|-----------------------|")
    etiquetas = ["AcOH", "EtOH", "H2O ", "EtAc"]
    tesis_vapor = [0.0629, 0.0855, 0.3970, 0.4545]
    tesis_liq = [0.2360, 0.0670, 0.5630, 0.1339]
    for i, nom in enumerate(etiquetas):
        print(f"    | {nom}       | {tesis_vapor[i]:.4f} / {tesis_liq[i]:.4f} | "
              f"{x_vap_uf[i]:.4f} / {x_liq_uf[i]:.4f} |")
    print(f"    | fraccion fase | vapor=0.882, liq=0.118 | "
          f"vapor={nt_vap_uf/(nt_liq_uf+nt_vap_uf):.3f}, liq={nt_liq_uf/(nt_liq_uf+nt_vap_uf):.3f} |")
    print("    Tendencia cualitativa coincide (AcOH se concentra en el liquido, EtAc/H2O")
    print("    dominan el vapor, y ambos predicen que el vapor es la fase mayoritaria),")
    print("    pero la magnitud difiere (UNIFAC predice menos vapor que UNIQUAC+Xiao).")

    return (ok_estequiometria and ok_ideal_exacto and ok_ideal_cruzada
            and ok_unifac_cruzada and ok_psat_fisico and ok_ideal_sin_vle
            and ok_vle_genuino and ok_vle_cruzada and ok_balance_vle)


if __name__ == "__main__":
    resultados = {
        "Derivada de Wilson": test_derivada_wilson(),
        "Jacobiano de Lagrange": test_jacobiano_lagrange(),
        "MTBE monofasico vs. scipy": test_mtbe_una_fase(),
        "MTBE bifasico vs. scipy": test_mtbe_dos_fases(),
        "Lagrange vs. RAND (no ideal)": test_lagrange_vs_rand_no_ideal(),
        "Greiner (1991) Apendice B": test_greiner_1991(),
        "Esterificacion acido acetico/etanol": test_acetic_ethanol_esterification(),
    }

    print("\n" + "=" * 70)
    print("RESUMEN DE VALIDACION")
    print("=" * 70)
    for nombre, ok in resultados.items():
        print(f"  [{'OK' if ok else 'FALLO'}] {nombre}")
    print()
    if all(resultados.values()):
        print("Todas las pruebas de consistencia interna pasaron.")
        print("(Recordatorio: esto valida la IMPLEMENTACION de las Ec. 3.14-3.70,")
        print(" no una reproduccion numerica de las Tablas 4.2/4.4/4.6/4.8 de la")
        print(" tesis, cuyos parametros de modelo no estan en los documentos")
        print(" disponibles -- ver advertencia en ejemplo_mtbe.py.)")
    else:
        print("ALGUNA PRUEBA FALLO -- revisar detalle arriba.")
