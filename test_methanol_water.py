from thermo.unifac import UFIP, UFSG, UNIFAC

# Metanol: CH3OH → grupos UNIFAC:
#   CH3 (grupo 1): 1 vez
#   OH (grupo 5, alcohol): 1 vez
# Agua: H2O → grupo UNIFAC:
#   H2O (grupo 7): 1 vez

# Verifica los números de grupo en thermo.unifac.UFSG si estos no funcionan.
chemgroups = [
    {1: 1, 5: 1},   # metanol
    {7: 1},         # agua
]

GE = UNIFAC.from_subgroups(
    chemgroups=chemgroups,
    T=298.15,          # 25 °C
    xs=[0.5, 0.5],
    version=0,
    interaction_data=UFIP,
    subgroups=UFSG
)

print("Metanol/agua 50/50 a 25°C:")
print("gammas:", GE.gammas())
print("GE (J/mol):", GE.GE())
print("HE (J/mol):", GE.HE())
print("SE (J/mol/K):", GE.SE())
