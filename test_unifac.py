from thermo.unifac import UFIP, UFSG, UNIFAC

GE = UNIFAC.from_subgroups(
    chemgroups=[{1:2, 2:4}, {1:1, 2:1, 18:1}],
    T=60 + 273.15,
    xs=[0.5, 0.5],
    version=0,
    interaction_data=UFIP,
    subgroups=UFSG
)

print("gammas:", GE.gammas())
print("GE, dGE_dT, d2GE_dT2:", GE.GE(), GE.dGE_dT(), GE.d2GE_dT2())
print("HE, SE, dHE_dT, dSE_dT:", GE.HE(), GE.SE(), GE.dHE_dT(), GE.dSE_dT())
