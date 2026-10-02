Downloaded from orbit.dtu.dk on: Mar 17, 2024
Simultaneous Chemical and Phase Equilibrium Calculations with Non-Stoichiometric
Method
Tsanas, Christos
Publication date:
2018
Document Version
Publisher's PDF, also known as Version of record
Link back to DTU Orbit
Citation (APA):
Tsanas, C. (2018). Simultaneous Chemical and Phase Equilibrium Calculations with Non-Stoichiometric Method.
Technical University of Denmark.
General rights
Copyright and moral rights for the publications made accessible in the public portal are retained by the authors and/or other copyright
owners and it is a condition of accessing publications that users recognise and abide by the legal requirements associated with these rights.
 Users may download and print one copy of any publication from the public portal for the purpose of private study or research.
 You may not further distribute the material or use it for any profit-making activity or commercial gain
 You may freely distribute the URL identifying the publication in the public portal
If you believe that this document breaches copyright please contact us providing details, and we will remove access to the work immediately
and investigate your claim.

|       | Simultaneous       |             | Chemical     |         | and |
| ----- | ------------------ | ----------- | ------------ | ------- | --- |
| Phase |                    | Equilibrium | Calculations |         |     |
| with  | Non-Stoichiometric |             |              | Methods |     |
Christos Tsanas
Ph.D. Thesis
January 2018

1

|            | Simultaneous       |            | Chemical     | and Phase |
| ---------- | ------------------ | ---------- | ------------ | --------- |
|            | Equilibrium        |            | Calculations | with      |
|            | Non-Stoichiometric |            |              | Methods   |
| Christos   | Tsanas             |            |              |           |
| Associate  | Professor          | Wei Yan    |              |           |
| Professor  | Erling             | H. Stenby  |              |           |
| Center     | for Energy         | Resources  | Engineering  |           |
| Department | of                 | Chemistry  |              |           |
| Technical  | University         | of Denmark |              |           |
| Kongens    | Lyngby,            | Denmark    |              |           |
| January    | 2018               |            |              |           |

| Science must | begin with | myths, and | with the criticism | of myths |
| ------------ | ---------- | ---------- | ------------------ | -------- |
— Karl R. Popper

Preface
Thisthesis issubmitted inpartialfulfillmentofthe requirementsfor thePh.D. degreeatthe
Technical University of Denmark, DTU. The research was carried out from December 2014
to January 2018 in the Department of Chemistry, DTU, under the supervision of Associate
Professor Wei Yan (main supervisor) and Professor Erling H. Stenby (co-supervisor). The
Ph.D. program was supported by the scholarship provided by DTU Chemistry and the
research on dimethyl ether phase equilibrium modeling was supported by the Danish
Hydrocarbon Research and Technology Centre (DHRTC).
January 2018
Christos Tsanas

Acknowledgments
First and foremost, I would like to express my utmost gratitude to my supervisors, Dr.
Wei Yan and Prof. Erling H. Stenby, for their trust and guidance throughout this project.
This work would not have been possible without their optimism and reassurance, but
most importantly this academic adventure would not have been as enjoyable. I am also
thankful to Prof. Michael L. Michelsen for his comments and suggestions. He was not
directly involved in the supervision of this project, and this is why I appreciate immensely
his help in the beginning of this study.
I am grateful to my colleges in CERE for the countless casual discussions that would
suddenly escalate to detailed model comparisons and ruthless criticism of algorithms.
I greatly appreciate the help of Anders Schlaikjer with the danish translation of the
abstract.
I shared the same office with amazing people in DTU Chemistry. It was a complete
pleasure to work with Farhad, Diego and Duncan. The things I learned and the inspiration
I got from them are invaluable.
Last but certainly not least, I would like to thank my family and friends, the unsung
heroes during my Ph.D. years in Denmark. This new chapter in my life did not come
without difficulties, but their encouragement made everything much easier.

Abstract
Simultaneous chemical and phase equilibrium (CPE) calculations constitute a major class
of challenging equilibrium problems, with applications in diverse scientific disciplines and
engineering fields, such as the chemical industry, oil and gas production, and geochem-
istry. Robustness and efficiency of computational procedures are essential for demanding
simulations of industrial processes, such as reactive distillation, heterogeneous organic
synthesis, and fuel synthesis from renewable feedstocks. Most association equations of state,
such as the popular SAFT family models, are essentially special cases of physical models
incorporating chemical (association) equilibrium. Solution and further improvement of
these association models can benefit from the advance in CPE calculations.
Over 70 years of research on CPE computation have resulted in a long list of algorithms
with many variants but there seems to be no clear consensus on the most adequate
methods. The deterministic algorithms can be roughly divided into stoichiometric and non-
stoichiometric methods. The stoichiometric methods are more intuitive but less efficient
for systems with many reactions. They are usually implemented with inefficient nested
loops, whereas quadratic formulation can involve quite a cumbersome implementation
for multiple phases. The non-stoichiometric methods are less common but suitable to
systems with many reactions. However, most applications of non-stoichiometric methods
are for ideal single-phase mixtures to slightly non-ideal two-phase systems and the reported
algorithms are mostly non-quadratic for non-ideal systems.
The primary aim of this work is to develop a general and systematic non-stoichiometric
approach which can determine the equilibrium state of multicomponent multiphase systems
with multiple reactions at specified temperature and pressure. Two methods based on
Gibbs energy minimization under material balance constraints are derived and presented in
their extended form for non-ideal multiphase reaction systems. Both can be classified under
the same category of using the Lagrange multipliers (and the phase molar amounts) as
variables. Fordistinction, theyarecalledtheLagrangemultipliersmethodandthemodified

RAND method, respectively. In the Lagrange multipliers method, successive substitution
is employed to solve a modified set of equations originating from the Lagrangian conditions
at the minimum. Convergence is quadratic for ideal systems (ideal gas/ideal solution)
and linear for non-ideal systems. In the modified RAND method, one of the Lagrangian
conditions is linearized around the current estimate of mole numbers. Composition
derivatives of fugacity or activity coefficients are utilized to achieve quadratic convergence.
The methods can be combined to form a robust and efficient approach: the Lagrange
multipliers method is used for the first iterations of successive substitution and the
modified RAND method for the second-order convergence. The resulting algorithm is
called the combined algorithm in this thesis. For comparison, a successive substitution
based algorithm using only the first-order Lagrange multipliers method is also investigated
in this study. Both algorithms incorporate a reliable initialization procedure, where initial
estimates are provided by the minimization of a convex function, and stability analysis to
introduce additional phases when needed. The combined algorithm, as the recommended
approach for CPE problems, has several advantages including a smaller system of equations
(fewer variables), less sensitivity to initial estimates, the same treatment for all components
and all phases, and the ability to monitor the decrease in Gibbs energy in the modified
RAND steps to guide convergence.
The algorithms were applied to vapor-liquid (VLE), liquid-liquid (LLE) and vapor-liquid-
liquid (VLLE) equilibrium of ideal as well as non-ideal systems that are commonly tested
in the literature, including acid/alcohol esterifications, alkene/alcohol etherefications,
hydration, hydrogenation and isomer separation. Additionally, predictions were made for
the more complex transesterification of two individual triglycerides with methanol, which
entails five chemical reactions and can result in one-, two- or even three-phase equilibrium.
Finally, CPE calculations were attempted for electrolyte systems. The electroneutrality
equation is satisfied by the material balance constraints, therefore there is no need to
change the working equations of the algorithms. The equilibrium solution was obtained for
aqueous mixtures of electrolytes in contact with a vapor and a solid phase. Consideration
of the solid phase did not affect the convergence of the initialization procedure or the
CPE calculations. This makes the algorithms potentially applicable to more complicated
geological systems with an electrolyte aqueous phase and multiple solids. From the simple
one-reaction ideal systems to the highly non-ideal electrolyte mixtures with speciation
reactions and solids, both algorithms could converge without problems to the equilibrium
solution. The CPU time and the reasonable number of iterations, allowed us to conclude
that the methods presented are efficient and robust for the equilibrium determination of
reaction systems.
The thesis also involves a small study on the dimethyl ether (DME) phase equilibrium
modeling. DME is a slightly polar compound able to dissolve in both water/brine and
hydrocarbon phases. It has been considered as a novel solvent in enhanced oil recovery,
and more specifically in DME enhanced waterflood (DEW) process. DME is dissolved
in water/brine and injected into the reservoir. It partitions preferably into the oil phase

to improve the mobility of the oil by swelling it and reducing its viscosity. DME itself is
first-contact miscible with the oil. Accurate phase equilibrium modeling is necessary in
DEW simulations. Parameters for CPA and PR/SRK EoS with Huron-Vidal mixing rules
areregressedfromexperimentaldataofDMEbinarysystemswithwater, hydrocarbonsand
inert gases. With satisfactory phase equilibrium modeling, predictions are made focusing
on the K-value of DME between oil and aqueous phases in DME/water/oil mixtures (oil
modeled as a mixture of methane, n-butane and n-decane). Different oil compositions
appear to slightly affect the partitioning of DME, which could possibly simplify simulations
of the DEW process. Finally, sensitivity of the K-value is investigated with respect
to temperature, pressure and salinity of the aqueous phase. K-values increase with
temperature and salinity but slightly decrease with pressure. Dependence on temperature
is larger, while high salinity in the aqueous phase favors markedly the DME partitioning
into the oil phase.

Resum´e p˚a dansk
Samtidig beregning af kemisk ligevægt og fase ligevægt (CPE) udgør en betragtelig klasse
af udfordrende ligevægts problemer, med applikationer i et bredt spektre af videnskabelige
discipliner og ingeniør felter som fx den kemiske industri, olie og gas produktion, og
geokemi. Robusthed og effektivitet af de beregningsmæssige processor er essentielle for
krævende simulationer af industrielle processor, som fx reaktiv destillation, heterogen
organisk syntese og brændstof syntese fra bæredygtige r˚amaterialer. De fleste associations
tilstandsligningersomdepopulærereSAFTmodellereregentligsærligetilfældehvorfysiske
modeller inkorporer kemisk (association) ligevægt. Løsning af og yderlige forbedring af
disse associations modeller kan drage fordel fra fremskridt i CPE beregninger.
Over 70 ˚ars forskning i CPE beregninger har resulteret i en lang liste af algoritmer
med mange varianter, men der synes ikke at være en klar konsensus mod de mest
passende metoder. De deterministiske algoritmer kan groft fordels i støkiometriske og ikke
støkiometriske metoder. De støkiometriske metoder er mere intuitive men ogs˚a mindre
effektive i systemer med mange reaktioner. De er som regel implementeret med ineffek-
tive nestede løkker, hvorimod kvadratisk formulering kan involvere en meget besværlig
implementering for flere faser. De ikke støkiometriske metoder er mindre almindelige, men
passende for systemer med mange reaktioner. De fleste applikationer af ikke støkiometriske
metoder er dog for ideelle enkelt fase blandinger op til en smule ikke ideelle 2-fase sys-
temer og de rapporterede algoritmer er hovedsageligt ikke kvadratiske for ikke ideelle
systemer.
Det primære m˚al med dette arbejde er at udvikle en generel systematisk ikke støkiometrisk
tilgang som kan bestemme ligevægts tilstanden af multikomponent multifase systemer
med flere reaktioner ved specificeret temperatur og tryk. To metoder baseret p˚a Gibbs
energi minimering under forudsætning af materialer balance begrænsninger er udledt og
præsenteret i deres udvidet form for ikke ideelle multifase reaktions systemer. Begge kan
blive klassificeret under den samme kategori ved at bruge Lagrange multiplikatorer (og fase

molar mængder) som variable. For at skelne er de kaldet; Lagrange multiplikator metoden
og modificeret RAND metoden. I Lagrange multiplikator metoden bruges successiv substi-
tution til at løse et modificeret set ligninger der stammer fra Lagrange betingelser ved
minimum. Dette konvergerer kvadratisk for ideelle systemer (ideal gas/ideelle opløsninger)
og lineært for ikke ideelle systemer. I den modificeret RAND metode er en af Lagrange
betingelserne lineariseret omkring det nuværende estimat af mol mængde. De sammensæt-
nings aflede af fugacitet or aktivitets koefficient er udnyttet til at opn˚a den kvadratiske
konvergering. De to metoder kan kombineres til at forme en robust og effektive tilgang;
Lagrange multiplikator metoden er brugt til de første iterationer af successiv substitution
og den modificerede RAND metoder er brugt for anden grads konvergeringen. Resultatet
er en algoritme kaldet den kombinerede algoritme i denne afhandling. En successiv substi-
tions baseret algoritme der kun burger første ordens Lagrange multiplikatorer metoden
er ogs˚a undersøgt i dette studie for at kunne blive brugt som sammenligning. Begge
algoritmer inkorporer en troværdig initierings procedure, hvor indledende værdier er fundet
ved minimering af en konveks funktion, og stabilitets analyse til at introducere yderligere
faser n˚ar nødvendigt. Den kombinerede algoritme, som den anbefalede tilgang til CPE
problemer, har flere fordele inklusive et mindre system af ligninger (færre variable), den
er mindre sensitiv to initiale værdier, har samme behandling af alle komponenter og alle
faser og har muligheden for at overv˚age faldet i Gibbs energi per skidt i den modificerede
RAND for at guide mod konvergering.
Algoritmerne er anvendt p˚a gas-væske, væske-væske og gas-væske-væske ligevægte i
ideelle s˚avel som ikke ideelle systemer der er regelmæssigt testet i litteraturen, inklusive
syre/alkohol esterficeringer, alkene/alkohol etherficeringer, hydrering, hydrogenering, og
isomer separation. Forudsigelser er derudover lavet for mere komplekse transesterficeringer
af 2 individuelle triglycerider med metanol, en proces der har 5 kemiske reaktioner og
kan resultere i 1, 2 eller 3 fasers ligevægt. Slutteligt har CPE beregninger været forsøgt
anvendt p˚a elektrolyt systemer. Elektroneutralitets ligningen er opfyldt ved masse balance
begrænsninger, og derfor er der ingen ændring i arbejdes ligningerne i algoritmerne.
Ligevægts opløsningen er fundet ved vandig blanding af elektrolytter i kontakt med en gas
og en fast fase. At tage den faste fase i betragtning har ikke nogen effekt p˚a konvergeringen
af den initiale procedure eller CPE beregningerne. Dette gør potentiellet algoritmerne
anvendelige p˚a mere komplekse geologiske systemer med en vandig elektrolyt fase og indtil
flere faste faser. Begge algoritmer kan konvergere, s˚avel det simpelt 1 reaktions ideelle
system til det meget ikke ideelle elektrolyt system med speciations reaktioner og faste
faser, uden problemer med ligevægts opløsningen. CPU beregningstiden og et passende
antal iterationer, tillader os at konkludere at de præsenterede metoder er effektive og
robuste for ligevægts fastsættelse i reaktions systemer.
Afhandlingen indeholder ogs˚a et mindre studie om modellering af dimethyl ethers (DME)
fase ligevægt. DME er et mildt polært stof der er kan opløses i s˚avel vand/brine og
carbonhydrid faser. Det har været betragtet som et nyt solvent i udvidet olieudvinding
(EOR) og mere specifikt i DME forbedret waterflood (DEW) processer. DME er opløst i

vand/brine og bliver pumpet ned i reservoiret. Her skilles det helst ind i olie fasen for at
forbedre mobiliteten af olien ved at f˚a det til at hæve op og derved reducere viskositeten.
DME er første kontakts opløseligt i olien. Præcis fase ligevægt modellering er nødvendig i
DEW simulationer. Parametre fra CPA og PR/SRK tilstandsligninger med Huron-Vidal
blandings regler er estimeret til eksperimentelle data for binære DME systemer med
vand, carbonhydrider og inerte gaser. Med tilfredsstillende faseligevægts modellering
er forudsigelser af K-værdien for DME mellem olie og vand faserne i DME/vand/olie
blandinger (olie modelleret som en blanding af metan, n-butan og n-dekan) beregnet.
Forskellige olie sammensætninger synes at have en mindre effekt p˚a fordeling af DME,
hvilket potentielt kunne forsimple simuleringen af DEW processen. Til slut er sensitiviteten
af K-værdien undersøgt i forhold til temperatur, tryk og saltindhold i vand fasen. K-
værdierne stiger med temperatur og saltindhold men falder svagt med tryk. Afhængighed
af temperatur er større, mens højt saltindhold i vandfasen kraftigt favoriserer DME i olie
fasen.

Contents
| List of figures |     |     |     |     | iii |
| --------------- | --- | --- | --- | --- | --- |
| List of tables  |     |     |     |     | ix  |
| 1 Introduction  |     |     |     |     | 1   |
1.1 Literature review . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1
1.2 Scope of this work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
| 2 General | thermodynamic | definitions |     |     | 11  |
| --------- | ------------- | ----------- | --- | --- | --- |
2.1 System and state functions . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
2.2 Equilibrium . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
2.2.1 Phase equilibrium . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
2.2.2 Chemical equilibrium . . . . . . . . . . . . . . . . . . . . . . . . . . 18
2.2.3 Types of reference states . . . . . . . . . . . . . . . . . . . . . . . . 21
| 3 Calculation | of chemical | and phase | equilibrium |     | 27  |
| ------------- | ----------- | --------- | ----------- | --- | --- |
3.1 Gibbs energy minimization . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
3.1.1 Stoichiometric formulation . . . . . . . . . . . . . . . . . . . . . . . 28
3.1.2 Non-stoichiometric formulation . . . . . . . . . . . . . . . . . . . . 29
3.1.3 Stability analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
3.2 Non-stoichiometric methods for CPE calculations . . . . . . . . . . . . . . 34
3.2.1 Lagrange multipliers method . . . . . . . . . . . . . . . . . . . . . . 34
3.2.2 The modified RAND method . . . . . . . . . . . . . . . . . . . . . 37
3.2.3 Initialization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
3.3 Non-stoichiometric algorithms for multiphase chemical equilibrium . . . . . 43
3.4 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46
| 4 Application | of CPE algorithms |     | to reaction | systems | 49  |
| ------------- | ----------------- | --- | ----------- | ------- | --- |
4.1 CPE calculations for systems in the literature . . . . . . . . . . . . . . . . 49

| ii  |     |     |     |     | Contents |     |
| --- | --- | --- | --- | --- | -------- | --- |
4.1.1 Formaldehyde/water mixture . . . . . . . . . . . . . . . . . . . . . 51
4.1.2 Xylene separation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53
4.1.3 Esterification of acetic acid with ethanol . . . . . . . . . . . . . . . 58
4.1.4 Esterification of acetic acid with 1-butanol . . . . . . . . . . . . . . 60
4.1.5 MTBE synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63
4.1.6 TAME synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . . 66
4.1.7 Propene hydration . . . . . . . . . . . . . . . . . . . . . . . . . . . 70
4.1.8 Cyclohexane synthesis . . . . . . . . . . . . . . . . . . . . . . . . . 73
4.1.9 Methanol synthesis . . . . . . . . . . . . . . . . . . . . . . . . . . . 75
4.2 Transesterification of fatty acid triglycerides with methanol . . . . . . . . . 77
4.3 Speed and convergence . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
4.4 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92
| 5 Calculation | of CPE | in electrolyte | systems |     |     | 97  |
| ------------- | ------ | -------------- | ------- | --- | --- | --- |
5.1 Electroneutrality in CPE calculations . . . . . . . . . . . . . . . . . . . . . 98
5.2 Infinite dilution reference state . . . . . . . . . . . . . . . . . . . . . . . . . 100
5.3 Non-stoichiometric algorithms in electrolyte mixtures . . . . . . . . . . . . 105
5.3.1 Water/ammonia/carbon dioxide mixture . . . . . . . . . . . . . . . 105
5.3.2 Carbon dioxide in aqueous solutions . . . . . . . . . . . . . . . . . . 109
5.4 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 116
| 6 Phase | equilibrium | modeling | for DME | enhanced | waterflood | 119 |
| ------- | ----------- | -------- | ------- | -------- | ---------- | --- |
6.1 EoS models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
6.2 Regression for DME binary systems . . . . . . . . . . . . . . . . . . . . . . 124
6.3 Predictions of DME partitioning between water and oil . . . . . . . . . . . 136
6.4 Effect of salinity on DME partitioning . . . . . . . . . . . . . . . . . . . . 143
6.5 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 146
| 7 Conclusions | and | future work |     |     |     | 149 |
| ------------- | --- | ----------- | --- | --- | --- | --- |
7.1 Chemical and phase equilibrium calculations . . . . . . . . . . . . . . . . . 149
7.2 DME phase equilibrium modeling . . . . . . . . . . . . . . . . . . . . . . . 151
| Appendices |     |     |     |     |     | 153 |
| ---------- | --- | --- | --- | --- | --- | --- |
A Matrix-vector operations . . . . . . . . . . . . . . . . . . . . . . . . . . . . 153
B Degrees of freedom analysis . . . . . . . . . . . . . . . . . . . . . . . . . . 155
C Reference state chemical potentials . . . . . . . . . . . . . . . . . . . . . . 157
D Determination of the formula matrix . . . . . . . . . . . . . . . . . . . . . 159
E Initialization of calculations . . . . . . . . . . . . . . . . . . . . . . . . . . 163
| Bibliography |     |     |     |     |     | 165 |
| ------------ | --- | --- | --- | --- | --- | --- |
| Glossaries   |     |     |     |     |     | 179 |
| Index        |     |     |     |     |     | 189 |

List of figures
3.1 Main steps of the algorithms in this work: (a) successive substitution and (b)
successive substitution combined with the modified RAND. . . . . . . . . . . . 45
4.1 Equilibrium T-y-x diagrams in formaldehyde/water mixture at 1 atm: (a)
formaldehyde, (b) water, (c) methylene glycol, (d) oxydimethanol [vapor ( ),
liquid ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52
4.2 Equilibrium in formaldehyde/water mixture at 1 atm: (a) T-Y-X diagram of
formaldehyde [vapor ( ), liquid ( )], (b) Y-X diagram of formaldehyde
and water [formaldehyde ( ), water ( )]. . . . . . . . . . . . . . . . . . . . 53
4.3 Equilibrium in xylene separation at 44 mmHg and 86 mmHg: (a, b) phase frac-
tions [vapor ( ), liquid ( )], (c, d, e, f) mole fractions [di-tert-butylbenzene
( ), m-xylene ( ), tert-butyl-m-xylene ( ), tert-butylbenzene ( ), ben-
zene ( ), p-xylene ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55
4.4 Ternary diagrams of elements in m-xylene alkylation without p-xylene at 350 K:
(a) 44 mmHg, (b) 86 mmHg [binodal curve ( ), tie lines ( ), VLE region
( ), vapor region ( ), liquid region ( ), infeasible region ( ), DTTB
(di-tert-butylbenzene), TBB (tert-butylbenzene), TBMX (tert-butyl-m-xylene)]. 57
4.5 Equilibrium in acetic acid/ethanol esterification for an equimolar feed of reac-
tants at 1 atm: (a) phase fractions [vapor ( ), liquid ( )] and (b, c) mole
fractions [acetic acid ( ), ethanol ( ), water ( ), ethyl acetate ( )]. . 59
4.6 Ternary diagram of elements in acetic acid/ethanol esterification at 355 K and
1 atm [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region
( ), liquid region ( ), infeasible region ( ), HAc (acetic acid), EtOAc
(ethyl acetate)]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 60
4.7 Equilibrium in acetic acid/1-butanol esterification for an equimolar feed of
reactants at 1 atm: (a) phase fractions [vapor ( ), liquid ( )], (b, c) mole
fractions [acetic acid ( ), 1-butanol ( ), water ( ), butyl acetate ( )]. 62

iv List of figures
4.8 Ternary diagram of elements in acetic acid/1-butanol esterification at 298.15 K
and 1 atm [binodal curve ( ), tie lines ( ), LLE region ( ), liquid region
( ), infeasible region ( ), HAc (acetic acid), BuOAc (butyl acetate)]. . . . 63
4.9 Equilibrium in MTBE synthesis at 1 atm: (a) T-y-x diagram for MTBE, (b)
T-Y-X diagram for isobutene [vapor ( ), liquid ( )], (c) Y-X diagram for
isobutene and methanol [isobutene ( ), methanol ( )]. . . . . . . . . . . . 65
4.10 Effect of inert feed mole numbers in MTBE synthesis at 300 K and 1 atm: (a)
phase fractions and mole fractions of (b) isobutene, (c) methanol, (d) n-butane,
(e) MTBE [vapor ( ), liquid ( ), overall ( )]. . . . . . . . . . . . . . . . 67
4.11 Ternary diagrams of elements in MTBE synthesis at 1 atm: (a) 280 K, (b) 320
K [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region ( ),
liquid region ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 68
4.12 Equilibrium in the two- and one-reaction TAME synthesis for a stoichiometric
ratio of reactants and methanol/n-pentane ratio equal to 2:1 at 1.52 bar: (a)
phase fractions [vapor ( ), liquid ( )], (b, c) mole fractions [2-methyl-
1-butene ( ), 2-methyl-2-butene ( ), methanol ( ), TAME ( ), n-
pentane ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 71
4.13 Ternary diagram of elements in the two-reaction TAME synthesis at 335 K and
1.52 bar [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region
( ), liquid region ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 72
4.14 Equilibrium in propene hydration for an equimolar feed of reactants at 1 bar
with temperature independent and dependent chemical equilibrium constant:
(a, b) phase fractions [vapor ( ), liquid ( )], (c, d, e, f) mole fractions
[propene ( ), water ( ), 2-propanol ( )]. . . . . . . . . . . . . . . . . . . 74
4.15 EquilibriuminPPOFAGtransesterificationwithmethanolandPPOFAG/methanol
ratio equal to 1:3 at 1 atm: (a) phase fractions [vapor ( ), ester-rich liq-
uid ( ), glycerol-rich liquid ( )], (b, c, d) mole fractions [methanol ( ),
PPOFAG ( ), PPFADIG ( ), POFADIG ( ), PFAMONOG ( ), OFA-
MONOG ( ), glycerol ( ), PFAME ( ), OFAME ( )]. . . . . . . . . . 81
4.16 EquilibriuminOLLFAGtransesterificationwithmethanolandOLLFAG/methanol
ratio equal to 1:3 at 1 atm: (a) phase fractions [vapor ( ), ester-rich liq-
uid ( ), glycerol-rich liquid ( )], (b, c, d) mole fractions [methanol ( ),
OLLFAG ( ), LLFADIG ( ), LOFADIG ( ), LFAMONOG ( ), OFA-
MONOG ( ), glycerol ( ), LFAME ( ), OFAME ( )]. . . . . . . . . . 82
4.17 Convergence in acetic acid/ethanol esterification for an equimolar feed of
reactants at 355 K and 1 atm: (a) successive substitution algorithm, (b)
combined algorithm, (c) inner loop (Newton) iterations per outer loop non-
ideality updates [Q-function minimization ( ), V ( ), VL ( )]. . . . . . . . 85
4.18 Convergence in acetic acid/1-butanol esterification for an equimolar feed of
reactants at 370 K and 1 atm: (a) successive substitution algorithm, (b)
combined algorithm, (c) inner loop (Newton) iterations per outer loop non-
ideality updates [Q-function minimization ( ), L ( ), VL ( )]. . . . . . 87

List of figures v
4.19 Convergence in MTBE synthesis for isobutene/methanol ratio equal to 1:1.1
without inert at 320.92 K and 1 atm: (a) successive substitution algorithm,
(b) combined algorithm, (c) inner loop (Newton) iterations per outer loop
non-ideality updates [Q-function minimization ( ), L ( ), VL ( )]. . . . 88
4.20 Convergence in the two-reaction TAME synthesis for a stoichiometric ratio of
reactants and methanol/n-pentane ratio equal to 2:1 at 330 K and 1.52 bar: (a)
successive substitution algorithm, (b) combined algorithm, (c) inner loop (New-
ton) iterations per outer loop non-ideality updates [Q-function minimization
( ), L ( ), VL ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 89
4.21 Convergence in propene hydration for an equimolar feed of reactants at 345 K
and 1 bar: (a) successive substitution algorithm, (b) combined algorithm, (c)
inner loop (Newton) iterations per outer loop non-ideality updates [Q-function
minimization ( ), L ( ), VL ( )]. . . . . . . . . . . . . . . . . . . . . . 90
4.22 Convergenceincyclohexanesynthesisforbenzene/hydrogenratioequalto1:3.05
at 500 K and 30 atm: (a) successive substitution algorithm, (b) combined
algorithm,(c)innerloop(Newton)iterationsperouterloopnon-idealityupdates
[Q-function minimization ( ), V ( ), VL ( )]. . . . . . . . . . . . . . . . 91
4.23 Convergence in methanol synthesis in the presence of n-octadecane at 473.15 K
and101.3bar: (a)successivesubstitutionalgorithm,(b)combinedalgorithm,(c)
inner loop (Newton) iterations per outer loop non-ideality updates [Q-function
minimization ( ), V ( ), VL ( ), VLL ( )]. . . . . . . . . . . . . . . . 93
4.24 ConvergenceinPPOFAGtransesterificationwithmethanolforPPOFAG/methanol
ratio equal to 1:3 at 450 K and 1 atm: (a) successive substitution algorithm,
(b) combined algorithm, (c) inner loop (Newton) iterations per outer loop
non-ideality updates [Q-function minimization ( ), L ( ), LL ( ), VLL
( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 94
4.25 ConvergenceinOLLFAGtransesterificationwithmethanolforOLLFAG/methanol
ratio equal to 1:3 at at 500 K and 1 atm: (a) successive substitution algorithm,
(b) combined algorithm, (c) inner loop (Newton) iterations per outer loop
non-ideality updates [Q-function minimization ( ), L ( ), LL ( ), VLL
( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 95
5.1 Convergence in the H O/NH /CO system at 373 K and 10 atm: (a) succes-
2 3 2
sive substitution algorithm, (b) combined algorithm, (c) inner loop (Newton)
iterations per outer loop non-ideality updates [Q-function minimization ( ),
VL ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107
5.2 CO solubility in water [experimental data at 285.15 K ( ), 291.15 K ( ), 298.15
2
K ( ), 304.19 K ( ), 308.15 K ( ), 313.15 K ( ), 374.15 K ( ), 393.15 K ( ), sum
of all CO related species ( ), CO ( )]. . . . . . . . . . . . . . . . . . 114
2 2(aq)
5.3 CO solubility in: (a, b) 10.1% CaCl , (c, d) 20.2% CaCl [experimental
2 2(aq) 2(aq)
data at 348.65 K ( ), 349.15 K ( ), 374.15 K ( ), 394.15 K ( ), sum of all CO
2
related species ( ), CO ( )]. . . . . . . . . . . . . . . . . . . . . . . . 115
2(aq)

vi List of figures
5.4 CO solubility in 10.1% CaCl in the presence of CaCO [experimental
2 2(aq) 3(s)
data at 393.15 K ( ), sum of all CO related species ( ), CO ( )]. . . 116
2 2(aq)
6.1 Dimethyl ether molecular structure. . . . . . . . . . . . . . . . . . . . . . . . . 120
6.2 DME/water modeling with CPA and SRK-HV: (a, b) regressed k , β for
ij cross
CPA, (c, d) regressed k , β , (cid:15) for CPA and C , C , α for SRK-HV, (d,
ij cross cross ij ji ij
e) regressed k = f(T) for CPA and C ,C = f(T) for SRK-HV [experimental
ij ij ji
data at 323.15 K ( ), 348.15 K ( ), 373.26 K ( ), 394.21 K ( ), calculations
with CPA ( ), calculations with SRK-HV ( )]. . . . . . . . . . . . . . . . 127
6.3 DME/methane modeling with CPA and SRK: (a) p-y-x diagram, (b) K-values
[experimental data at 282.9 K ( ), 313.3 K ( ), 343.8 K ( ), calculations with
CPA ( ), calculations with SRK ( )]. . . . . . . . . . . . . . . . . . . . . 128
6.4 DME/propane modeling with CPA and SRK: (a, b) p-y-x diagram, (c) K-values
[experimental data at 273.15 K ( ), 298.15 K ( ), 313.10 ( ), 323.15 K ( ),
313.39 K ( ), calculations with CPA ( ), calculations with SRK ( )]. . . . 129
6.5 DME/n-butane modeling with CPA and SRK: (a, b) p-y-x diagram [experi-
mental data at 282.96 K ( ), 297.86 K ( ), 312.98 K ( ), 328.01 K ( ), 343.07
K ( ), 353.65 K ( )], (c, d) p-y-x diagram [experimental data at 372.87 K ( ),
387.22 K ( ), 402.71 K ( ), 405.16 K ( ), 414.50 K ( )] [calculations with CPA
( ), calculations with SRK ( )]. . . . . . . . . . . . . . . . . . . . . . . . . 130
6.6 DME/n-butane modeling with CPA and SRK: (a, b) K-values [experimental
data at 282.96 K ( ), 297.86 K ( ), 312.98 K ( ), 328.01 K ( ), 343.07 K ( ),
353.65 K ( )], (c, d) K-values [experimental data at 372.87 K ( ), 387.22 K
( ), 402.71 K ( ), 405.16 K ( ), 414.50 K ( )] [calculations with CPA ( ),
calculations with SRK ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
6.7 DME/hydrocarbon modeling with CPA and SRK for: (a) n-pentane, (b) n-
decane, (c) n-dodecane [experimental data at x = 0.392 ( ), x = 0.679
DME DME
( ), 323.15 K ( ), calculations with CPA ( ), calculations with SRK ( )]. . 132
6.8 DME/carbon dioxide modeling with CPA and SRK: (a) p-y-x diagram, (b)
K-values [experimental data at 298.15 K ( ), 308.65 K ( ), 320.15 K ( ),
calculations with CPA ( ), calculations with SRK ( )]. . . . . . . . . . . . 133
6.9 DME/nitrogen modeling with CPA and SRK: (a) p-y-x diagram, (b) K-values
[experimental data at 298.15 K ( ), 308.15 K ( ), 318.15 K ( ), calculations
with CPA ( ), calculations with SRK ( )]. . . . . . . . . . . . . . . . . . 133
6.10 Ternary diagram of DME/water at 323.15 and 100 bar with: (a) methane, (b)
propane [binodal curves for LLE ( ), VLE (DME-rich liquid) ( ), VLE
(water-rich liquid) ( ), tie lines ( ), LLE region ( ), VLE (DME-rich
liquid) region ( ), VLE (water-rich liquid) region ( ), VLLE region ( )]. 137
6.11 Ternary diagram of DME/water at 323.15 and 100 bar with: (a) n-butane, (b)
n-pentane [binodal curve ( ), tie lines ( ), LLE region ( )]. . . . . . . . 138
6.12 Ternary diagram of DME/water at 323.15 and 100 bar with: (a) n-decane, (b)
n-dodecane [binodal curve ( ), tie lines ( ), LLE region ( )]. . . . . . . 139

List of figures vii
6.13 Comparison of LLE binodal curves in DME/water/HC ternaries at 323.15 K
and 100 bar [methane ( ), propane ( ), n-butane ( ), n-pentane ( ),
n-decane ( ), n-dodecane ( )]. . . . . . . . . . . . . . . . . . . . . . . . . 140
6.14 K-values of DME partitioning between oil and aqueous phase at 323.15 and
100 bar for different oil composition with DME mole fraction in the feed: (a)
z = 0.1 , (b) z = 0.3. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 141
DME DME
6.15 K-values of DME partitioning between oil and aqueous phase at 323.15 and
100 bar for different oil composition with DME mole fraction in the feed: (a)
z = 0.5, (b) z = 0.7. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
DME DME
6.16 K-values of DME partitioning between oil (30% methane, 30% n-butane, 40%
n-decane) and aqueous phase at: (a) 100 bar [323.15 K ( ), 348.15 K ( ),
373.26 K ( ), 394.21 K ( )], (b) 323.15 K [50 bar ( ), 100 bar ( ), 150
bar ( ), 200 bar ( ), 250 bar ( )]. . . . . . . . . . . . . . . . . . . . . . 143
6.17 Brine vapor pressure modeling with CPA for different w : (a) p-T diagram
NaCl
[experimental data for 2.84% ( ), 5.52% ( ), 10.00% ( ), 12.75% ( ), 15.00%
( ), 18.95% ( )], (b) p-T diagram [experimental data for 5.00% ( ), 8.06% ( ),
10.46% ( ), 14.92% ( ), 16.98% ( ), 20.00% ( )] [calculations with CPA ( )]. 145
6.18 Correlation of CPA c parameter for different NaCl mass fractions [regressed
1
c ( ), polynomial n = 2 trend line ( ), AARD: average absolute relative
1
deviation of the fitting]. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 145
6.19 DME/brine modeling with CPA: (a) 10% w/w NaCl, (b) 323 K [experimental
data 303 K ( ), 353 ( ), 3% w/w NaCl ( ), 10% w/w NaCl ( ), 17% w/w NaCl
( )] [calculations with CPA ( )]. . . . . . . . . . . . . . . . . . . . . . . . . . 146
6.20 Correlation of CPA k for the pseudo-binary DME/brine at 323 K for different
ij
NaCl mass fractions [regressed k ( ), linear trend line ( ), AARD: average
ij
absolute relative deviation of the fitting]. . . . . . . . . . . . . . . . . . . . . . 146
6.21 K-values of DME partitioning between oil (30% methane, 30% n-butane, 40%
n-decane) and aqueous phase at 323 K and 100 bar for different w [3%
NaCl
( ), 6% ( ), 10% ( ), 13% ( ), 17% ( )]. . . . . . . . . . . . . . . . 147

List of tables
2.1 Thermodynamic equilibrium conditions for closed systems. . . . . . . . . . . . 16
4.1 Component and element numbering for the systems examined. . . . . . . . . . 50
4.2 Equilibrium mole fractions in xylene separation at 44 mmHg (bubble point). . 54
4.3 Equilibrium mole fractions in xylene separation at 86 mmHg (bubble point). . 56
4.4 Equilibrium mole fractions, phase amounts and phase fractions in acetic
acid/ethanol esterification at 355 K and 1 atm. . . . . . . . . . . . . . . . . . 58
4.5 Transformed tie line slopes R in acetic acid/1-butanol esterification at 298.15
2
K and 1 atm. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
4.6 Transformed tie line slopes R and R in TAME synthesis for the single-reaction
2 3
system at 335 K and 1.52 bar. . . . . . . . . . . . . . . . . . . . . . . . . . . . 70
4.7 Transformed compositions Y and X in propene hydration at 353.15 K. . . . . 73
1 1
4.8 Equilibrium mole fractions, phase amounts and phase fractions in cyclohexane
synthesis at 500 K and 30 atm. . . . . . . . . . . . . . . . . . . . . . . . . . . 75
4.9 Equilibrium mole fractions, phase amounts and phase fractions in methanol
synthesis at 473.15 K and 300 bar. . . . . . . . . . . . . . . . . . . . . . . . . 76
4.10 Equilibrium mole fractions, phase amounts and phase fractions in methanol
synthesis at 473.15 K and 101.3 bar. . . . . . . . . . . . . . . . . . . . . . . . 76
4.11 Component and element numbering for the PPOFAG (R C H O) and
1 16 31
≡
OLLFAG transesterification (R C H O) systems (for both mixtures R
1 18 33 2
≡ ≡
C H O). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
18 31
4.12 Compounds in triglyceride esterification. . . . . . . . . . . . . . . . . . . . . . 80
4.13 CPU time to obtain the equilibrium solution of the systems examined (SSA: suc-
cessivesubstitutionalgorithm,CA:combinedalgorithm,processor: IntelRCoreTM
(cid:13)
i7-5500U CPU@ 2.40 GHz). . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
5.1 Component and element numbering for the H O/NH /CO system. . . . . . . 106
2 3 2

x List of tables
5.2 Equilibrium partial pressures in the vapor phase, molalities in the liquid phase,
phase amounts and phase fractions of the H O/NH /CO system at 373 K and
2 3 2
10 atm. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 108
5.3 Component and element numbering for H O/CO /CaCl /CaCO system. . . . 113
2 2 2 3
6.1 Experimental data of DME binaries used in the regressions. . . . . . . . . . . 124
6.2 Pure component parameters for CPA. . . . . . . . . . . . . . . . . . . . . . . . 125
6.3 Regressed parameters for DME/water using CPA (non-regressed parameters in
parentheses). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
6.4 Regressed parameters for DME/water using PR and SRK with HV mixing
rules (non-regressed parameters in parentheses). . . . . . . . . . . . . . . . . . 126
6.5 Regressed parameters for DME/HC, DME/CO and DME/N using CPA, PR
2 2
and SRK. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 128
6.6 Average absolute relative deviations for DME binaries considering different
models and regression strategies (LLE-1: water-rich liquid, LLE-2: DME-rich
liquid). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
6.7 Regressed values of CPA c parameter at different NaCl concentrations. . . . . 144
1
6.8 Regressed k for the pseudo-binary system DME/brine (VLE AARD 3.71%,
ij
LLE AARD 2.19%). . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 145

| C H A | P T | E R |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
1
Introduction
| 1.1 | Literature |     |     | review |     |     |     |     |
| --- | ---------- | --- | --- | ------ | --- | --- | --- | --- |
Calculation of simultaneous chemical and phase equilibrium (CPE) is essential in the
chemical and petroleum industry. Fast and reliable algorithms are necessary in process
simulations that combine phase separation and transformation of compounds into valuable
| products. | CPE | calculations |     | are useful |     | in: |     |     |
| --------- | --- | ------------ | --- | ---------- | --- | --- | --- | --- |
reactive distillation (Saito et al., 1971; Barbosa and Doherty, 1988; Ung and Doherty,
•
1995a,b,c,d,e). Reactions allow us to bypass restrictions of purely physical processes,
such as infeasibility of separation due to azeotropes or close-boiling components (e.g.
isomers).
reactive extraction (Kanth et al., 2014; Pal et al., 2015; Shah et al., 2016). Reacting
•
| components |     | tend | to have | higher | partition |     | coefficients. |     |
| ---------- | --- | ---- | ------- | ------ | --------- | --- | ------------- | --- |
heterogeneousorganicsynthesis(Toikkaetal.,2012). Reactantscanimpedetheprogress
•
of the reaction if they separate into different phases. On the other hand, partitioning
| of products |     | can | shift equilibrium |     | to  | favorable | yields. |     |
| ----------- | --- | --- | ----------------- | --- | --- | --------- | ------- | --- |
biodiesel production (Kiss et al., 2006; Anikeev et al., 2012; Osorio-Viana et al., 2013).
•
A mixture of fatty acid esters is mainly produced by transesterification of triglycerides.
weak electrolytes/geochemical systems (Gautam and Seider, 1979c; Venkatraman et al.,
•
2015; Leal et al., 2016a). Speciation of electrolytes takes place in an aqueous phase,
| which | is  | potentially | at  | equilibrium |     | with vapor | and solid | phases. |
| ----- | --- | ----------- | --- | ----------- | --- | ---------- | --------- | ------- |
reactor design (Solsvik et al., 2016). Gibbs energy minimization is combined with
•
| current       | feasibility |              | and | design | models | to improve | them.   |       |
| ------------- | ----------- | ------------ | --- | ------ | ------ | ---------- | ------- | ----- |
| metallurgical |             | applications |     | (Rao,  | 1983;  | Sander     | et al., | 1986) |
•
reactive crystallization (Jim´enez and Costa-L´opez, 2002; Jaime-Leal et al., 2012)
•

| 2   |     |     |     |     |     |     | Chapter | 1. Introduction |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------- |
air pollution control equipment (Sanderson and Chien, 1973; P´erez Cisneros et al.,
•
1997)
Various algorithms and solution strategies were published and applied to a range of
ideal/non-ideal single- or multiphase systems. Some common reaction mixtures reported
| in literature | include: |     |     |     |     |     |     |     |
| ------------- | -------- | --- | --- | --- | --- | --- | --- | --- |
esterification of acetic acid/ethanol (Castillo and Grossmann, 1981; Barbosa and
•
Doherty, 1988; Xiao et al., 1989; Castier et al., 1989; McDonald and Floudas, 1995,
| 1997; P´erez | Cisneros | et al., | 1997) |     |     |     |     |     |
| ------------ | -------- | ------- | ----- | --- | --- | --- | --- | --- |
esterification of acetic acid/1-butanol (Suzuki et al., 1970; Grob and Hasse, 2005;
•
Bonilla-Petriciolet et al., 2006; Mandagaran and Campanella, 2009)
MTBE (methyl-tert-butyl ether) synthesis (Ung and Doherty, 1995e; Seider and
•
| Widagdo, | 1996; | Fateen et | al., 2012; | Moodley | et al., | 2015) |     |     |
| -------- | ----- | --------- | ---------- | ------- | ------- | ----- | --- | --- |
TAME (tert-amyl methyl ether) synthesis (Chen et al., 2002; Bonilla-Petriciolet et al.,
•
| 2008a, | 2011; Elnabawy | et  | al., 2014) |     |     |     |     |     |
| ------ | -------------- | --- | ---------- | --- | --- | --- | --- | --- |
methanol synthesis (Chang et al., 1986; Castier et al., 1989; Gupta et al., 1991; Stateva
•
and Wakeham, 1997; Phoenix and Heidemann, 1998; Avami and Saboohi, 2011)
propene hydration (Castier et al., 1989; Stateva and Wakeham, 1997; Bonilla-Petriciolet
•
| et al., | 2012) |     |     |     |     |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
transesterification of fatty acids (Schuchardt et al., 1998; Darnoko and Cheryan, 2000;
•
| Omota | et al., 2001, | 2003; | Kiss et | al., 2006; | Chong | et al., | 2014) |     |
| ----- | ------------- | ----- | ------- | ---------- | ----- | ------- | ----- | --- |
benzene hydrogenation (George et al., 1976; Castillo and Grossmann, 1981; Burgos-
•
| Solo´rzano | et al., | 2004) |     |     |     |     |     |     |
| ---------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
xylene separation (Ung and Doherty, 1995a,c,e; P´erez Cisneros et al., 1997)
•
reactionsinaqueoussolutionofformaldehyde(UngandDoherty,1995a,e;P´erezCisneros
•
| et al., | 1997; Avami | and Saboohi, |     | 2011) |     |     |     |     |
| ------- | ----------- | ------------ | --- | ----- | --- | --- | --- | --- |
blast furnace problem (Madeley and Toguri, 1973; Cavallotti et al., 1980; Castillo and
•
| Grossmann, | 1981) |     |     |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
steam cracking of ethane (Castillo and Grossmann, 1981; Gautam and Wareck, 1986;
•
| Lantagne | et al., | 1988) |     |     |     |     |     |     |
| -------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
geological reactions with solid calcite/dolomite/quartz (Leal et al., 2016a,b)
•
CPE applications are not limited to these lists. Although there are cases where a process is
subject to kinetic limitations and the equilibrium solution has little to no weight in decision
making (e.g. optimization of process parameters), CPE can still provide a thermodynamic
| limit as reference | to  | judge the | overall | efficiency | of the | process. |     |     |
| ------------------ | --- | --------- | ------- | ---------- | ------ | -------- | --- | --- |
This work uses terminology that appears in Smith and Missen (1982), who published

Chapter 1. Introduction 3
a systematic categorization and review of CPE procedures. Two main categories exist,
solution of equilibrium algebraic equations and Gibbs energy minimization. Minimization
problems are further divided into stoichiometric and non-stoichiometric. The former use
reaction extents as independent variables and the later material balance constraints, which
are incorporated in the Lagrangian of the Gibbs energy. Later publications usually follow
this convention when they refer to CPE calculation methods.
Solution of equilibrium equations
One of the oldest algorithms for CPE calculations was published by Brinkley (1946, 1947),
using a nested-loop scheme to solve the equilibrium equations. Activity coefficients are
kept constant in the inner loop (secondary iterations) and updated in the outer loop
(primary iterations). A “representative phase” and a basis of reference components are
selected for the calculations. Different basis components and representative phases affect
the speed of convergence. According to Brinkley (1946) determination of an optimum basis
is possible but can be too inconvenient for practical application. Nevertheless, a number of
publications have addressed the issue of the basis optimization (Prigogine and Defay, 1947;
Schott, 1964; Cruise, 1964). Usually it consists of the most abundant components.
Stoichiometric algorithms
Ma and Shipman (1972) presented a two-step method for ideal multiphase mixtures ap-
proximating major components in the beginning (high truncation error) and subsequently
solving for the exact equilibrium solution, where minor components re-enter calculations.
Sanderson and Chien (1973) developed a procedure transforming the Gibbs energy mini-
mization into an unconstrained minimization using a penalty function. The solution is
based on the Rachford-Rice equation using values of chemical equilibrium constants in
nested-loop calculations. Marquardt’s method was chosen to solve the non-linear equations.
Phase equilibrium is solved in the inner loop, updating the reaction extents in the outer
loop. Sanderson and Chien (1973) made a distinction between the two solution approaches
for the chemical and phase equilibrium problem. According to them, solution of algebraic
equations should be advantageous in data correlation and simulations whereas Gibbs
energy minimization in larger systems or for predictions. Xiao et al. (1989) studied VLE
of reaction systems with a K-value based method. They proposed an improvement of
the S-C algorithm (Sanderson and Chien, 1973), called the KZ algorithm. Still with a
nested-loop procedure, chemical equilibrium is solved in the inner loop and phase equilib-
rium in the outer loop with a modified Marquardt method (S-C algorithm loops switched).
For improved efficiency, variables are also scaled by the total amount of components at
equilibrium. Stateva and Wakeham (1997) presented a modified KZ algorithm (Xiao et al.,
1989) partitioning the system into linear and non-linear equations. In the inner loop
chemical equilibrium is solved, whereas in the outer loop phase equilibrium equations with
constant K-values are converged. In general, their three-step method involves initialization,
stability analysis with phase split/flash and final convergence to the equilibrium solution.

4 Chapter 1. Introduction
Castier et al. (1989) derived the only stoichiometric second-order method to our knowledge.
Initial steps involve accelerated direct substitution with the General Dominant Eigenvalue
Method (GDEM) (Crowe and Nishio, 1975). Rachford-Rice equations are solved in the
inner loop and reaction extents and K-values are updated in the outer loop. The efficient
Murry’s minimization is employed for final convergence. Yield factors are introduced to
account for the separation of the components between the phases. Components need to be
divided into primary or secondary and revision of their mole numbers is necessary when
they attain negative values.
Non-stoichiometric algorithms
The non-stoichiometric formulation was extensively explained by Zeleznik and Gordon
(1968). Perturbation calculations were used to initialize computations for challenging
systems, accounting for non-ideality. Elimination of the Lagrange multipliers reduces the
minimization to a “chemical equilibrium constant” method. Sensitivity with respect to
initial conditions was also mentioned. The potentially large difference of thermodynamic
derivatives between reaction and non-reaction systems was addressed but it is kinetics
that decides which derivatives should be used. The overall strategy for CPE problems was
considered by the authors as “an interplay between thermodynamic fundamentals and
numerical analysis”. George et al. (1976) used exponential functions instead of penalty
functions to eliminate the constraints for two- or three-phase equilibrium with Powell’s
method (Powell, 1971) with independent treatment of trace components. Castillo and
Grossmann (1981) presented a non-stoichiometric method with a phase elimination proce-
dure using steepest descent coupled with optimum step sizes. A non-linear programming
algorithmalloweddirecttreatmentofthenon-negativityconstraintsofmolenumbers. They
took provision in the neighborhood of zero compositions, since the gradient is unbound
and convergence is impeded. They presented results for both reaction and non-reaction
mixtures. There was no need for a feasible starting point, linear independence of the
constraints and fugacity analytical derivatives, the latter being especially useful for complex
thermodynamic models. Phases with zero mole numbers were not eliminated in the event
that they were needed later. Harvie et al. (1987) identified automatically orthogonal
reaction paths needed in the poorly conditioned chemical equilibrium problems, as they
are more stable in calculations. Gibbs energy was minimized with Newton’s method
and phases were removed when the Hessian was singular. Instability could occur when
assuming more phases than the Gibbs phase rule allows or when concentrations approach
zero. They noted the need for second-order derivatives to increase efficiency in the phase
removal procedure. Different specifications from isothermal and isobaric chemical and
phase equilibrium are mentioned in Gautam and Wareck (1986). In their formulation,
equations for an electrolyte phase were also included. They started calculations with one
phase or more and used the phase splitting algorithm of Gautam and Seider (1979b).
Although the authors believed that the method “is robust enough”, they admit that
there was not extensive testing concerning the phase-splitting algorithm. Uchida (1987)
used logarithms of mole fractions as variables to speed up the convergence. Initialization

Chapter 1. Introduction 5
was provided by the Simplex method and components were separated into primary and
secondary based on their abundance. Instead of trying all the possible phase combinations,
they introduced imaginary components to decide which phases of the ones initially assumed
actuallyexistatequilibrium. SaimandSubramaniam(1988)appliedthenon-stoichiometric
formulation to systems with solvents at supercritical conditions solving the equations of the
Lagrangian at the minimum. Lantagne et al. (1988) showed a second-order Newton’s and
quasi-Newton method based on the penalty function formulation, allowing the existence
of electrolyte phases. The efficiency of the algorithm strongly depends on the choice of the
penalty parameter. The authors compared their procedure with a sequential quadratic
programming (SQP) method for reaction and non-reaction systems. Their algorithm
showed similar performance to the SQP procedure, with the additional advantage that it
is able to deal with low concentrations. Michelsen (1989) stressed that away from critical
conditions, CPE calculations can approach the efficiency of second-order methods coupled
with an acceleration method. To overcome problems associated with trace components,
Michelsen (1989) defined the dual problem. Linear programming was used to initialize
calculations. In the same work, an augmented Lagrangian using penalty functions was
also applied and resulted in more stable iterations.
Lucia and Xu (1990) applied a general SQP algorithm in VLE with trust region as a
stabilization method. The Hessian matrix was approximated and the quadratic problem
was solved by two methods, a linear programming based method and the active set
method. In their work, their formulations involved Gibbs energy minimization and entropy
maximization. Hildebrandt and Glasser (1994) developed a geometric algorithm that
constructstheboundaryoftheconvexhulloftheGibbsenergy. Thisprovidesanalternative
way to find equilibrium number of phases and compositions. P´erez Cisneros et al. (1997)
presented two procedures for chemical and phase equilibrium calculations: the chemical
model using elements in the mass balance equation and the ideal solution approach with
two-loops (inner loop calculation for constant fugacity coefficients, outer loop updating the
non-ideality). They also stressed that the reader should take caution with the sensitivity
of the equilibrium solution on the model parameters. Phoenix and Heidemann (1998)
developed two first-order methods, a stoichiometric with reaction extents and phase
amounts as iteration variables and a non-stoichiometric with Lagrange multipliers and
phase amounts. The usual scheme was considered, where fugacity coefficients are constant
in the inner loop and updated in the outer loop. Stability analysis and damping coefficients
to control the non-stoichiometric convergence were also used. Lee et al. (1999) employed
direct search optimization to minimize the Gibbs energy, that can converge even when the
phases assumed in the beginning were more than the equilibrium phases. Wasylkiewicz
and Ung (2000) using transformed variables form Ung and Doherty (1995d) developed
a procedure that can systematically track all the stationary points of the tangent plane
distance function. Transformed mole fractions for reaction systems introduced by Ung and
Doherty (1995a,b,c,d,e), were widely used in different algorithms in the literature. Their
workwasbasedonthestudyofBarbosaandDoherty(1988)intheVLEofsystemswithone

6 Chapter 1. Introduction
reaction. The authors addressed the issue of reactive azeotropes and the conditions under
they are likely to appear. They showed that mole fractions in the vapor and liquid phase
are not necessarily equal at a reactive azeotrope and ideal systems can also exhibit such
behavior. Jalali-Farahani and Seader (2000) and Jalali et al. (2008) determined equilibrium
with the homotopy-continuation method. Homotopy function provides a smooth transition
to the solution by gradually introducing non-linearities and the continuation method is
capable of finding all the roots of a function. Koukkari and Pajarre (2007) illustrated
how kinetic constraints can be incorporated in a non-stoichiometric method, implying
however that the dependence of the reaction extents on time is known. Rossi et al. (2011)
studied a number of systems with models that behave as pseudo-convex functions, covering
both PT and PH flash with non-linear programming, pointing out that the assumption of
convexity might limit applicability. Avami and Saboohi (2011) worked on the simultaneous
solution of equilibrium and stability analysis, relaxing the constraint of the known phases
number before the calculations. Their method is referred to as an extended τ method.
Variables τ are called phase characteristic variables and are linked to the existence of a
phase at equilibrium. The authors suggest that this method could be used in reactive
distillation simulations. Leal et al. (2016a,b) combined the Gibbs energy minimization
with geochemical reactions, electrolytes and solid precipitation. They start with the
maximum number of phases allowed, removing those that do not exist at equilibrium.
Their observation is that the electroneutrality equation is not an additional constraint,
but is forced by the formula matrix of the system.
The RAND method
White et al. (1958) presented a non-stoichiometric method, the original RAND method,
named after the company where the authors were working. It is a Gibbs energy mini-
mization approach that does not distinguish between the components during calculations
(primary/secondary). Linear programming was used for initialization with a safeguard for
zero concentrations. The method was proposed for ideal gas reaction phases. A similar
method was developed by Huff et al. (1951), known as the NASA method. Their key
difference is that during RAND iterations, the material balance is satisfied in contrast to
NASA iterations. Boynton (1960) extended calculations to multiple ideal phases, with the
assumption that all condensed phases were known beforehand. The author mentioned the
possibility of application to non-ideal systems with an outer loop updating the activity
coefficients. Gautam and Seider (1979a,b,c) and White and Seider (1981) in a series of
four research papers, covered different topics pertinent to equilibrium calculations. They
mentioned solid existence criteria and referred to the procedures presented in Sanderson
and Chien (1973) (S-C algorithm), White et al. (1958) (RAND algorithm), Huff et al.
(1951) (NASA algorithm) and George et al. (1976) (Powell’s method). They found that
quadratic programming and the RAND algorithm are faster than Powell’s method. They
combined the RAND algorithm with a phase-splitting procedure that allows even poor
guesses for trial phases. Furthermore, they accounted for dissociation reactions by in-
cluding additional terms for electrolytes in the Gibbs energy expression. Finally, they

Chapter 1. Introduction 7
discussed characteristic of stoichiometric and non-stoichiometric methods, presenting an
extension of the RAND algorithm for multiphase systems. There is no direct mention of
how they used the RAND method to account for non-ideality. In their final paper (White
and Seider, 1981) they refer to the extended RAND as the “augmented” RAND, that can
be applied to systems with reactions, electrolytes and solid components. Michelsen (1989)
commented on the difficulty of the RAND method to determine small concentrations (trace
components). Greiner (1988a,b,c) presented an extensive analysis of the Gibbs energy
minimization. The analysis was based on the elemental abundance approach. The author
showed with rigorous mathematical proofs how the non-ideal non-convex problem can be
formulated as an equivalent “convexified” problem, avoiding metastable points as final
solutions. Moreover, he demonstrated how the formulation can be transformed into a
generalized linear program to approximate the solution without the need of second-order
derivatives. However, this approach achieved linear converge rate. Generalization of the
RAND algorithm to non-ideal multiphase systems with quadratic convergence rate is
attributed to Greiner (1991), but a similar formulation appears in Michelsen and Mollerup
(2007) with different derivation. Vonˇka and Leitner (1995) showed calculations with the
RAND method in non-ideal systems by performing RAND steps under the ideal system
approximation (constant fugacity or activity coefficients) and then updated the non-ideality
part using the new compositions. New initial estimates were created in the case of a
singular matrix. In general implementations based on the ideal system approximation
are not expected to be fast and there is no guarantee that the Gibbs energy decreases
between outer-loop iterations. Recently Paterson et al. (2017) presented two RAND-based
formulations: modified RAND with TP based thermodynamics and vol-RAND with TV
based thermodynamics. Nevertheless, their study is primarily focused on multiphase
equilibrium calculations without reactions.
Global optimization methods
Floudas and Visweswaran (1990) provided an extensive study with mathematical proofs on
global optimization of non-linear programming. Their treatment involved the solution of a
number of subproblems with partitioning and transformation of variables (GOP algorithm).
McDonald and Floudas (1995, 1997) developed GLOPEQ, guaranteed to convergence
to the global minimum combining two procedures: minimization of Gibbs energy and
minimization of the tangent plane distance. Gupta et al. (1991) presented an alternative
treatmentforstabilityanalysiswithamultiphasereactionequilibriumalgorithm. Algebraic
equations of equilibrium and stability are solved in a nested-loop. In the inner loop fugacity
coefficients are kept constant while phase fractions, stability variables and reaction extents
are converged. In the outer loop mole fractions are updated and an acceleration factor is
calculated based on the dominant eigenvalue method. Incipient phases, phase removal and
reintroduction of phases were not a problem. Burgos-Solo´rzano et al. (2004) developed a
validation tool to provide a guarantee of convergence to the Gibbs energy global minimum.
Due to the additional computation time it requires, the authors suggest its use at the end
of a simulation.

8 Chapter 1. Introduction
A large part of the literature is devoted to deterministic methods. In recent decades, a
number of stochastic methods has been utilized for equilibrium calculations. Stochastic
methods require only evaluation of the objective function. Bonilla-Petriciolet and Segovia-
Hern´andez (2010), and Bonilla-Petriciolet et al. (2008b, 2011, 2012) worked largely on
stochastic methods in Gibbs energy minimization for reacting systems. They proposed
algorithms for two-phase equilibrium (VLE and LLE) using different algorithms such
as swarm optimization and its modifications, genetic algorithms, differential evolution
with tabu list, simulated annealing and harmony search. A local optimization method
is used during final convergence to improve efficiency. Fateen et al. (2012) compared
three global optimization algorithms (CMA-ES, SCE, Firefly). Elnabawy et al. (2014)
presented different variations of the Charged System Search method, inspired by the
Coulombic forces between charged particles. Both works mention the possibility of a local
optimization method for final convergence to improve global success rate, an indication
of the successful convergence to the minimum with different initial estimates. Moodley
et al. (2015) presented modifications of the Krill Herd optimization on CPE and stability
analysis. The method simulates the herding behavior of the krill crustacean and requires a
smaller number of function evaluations than other stochastic methods. Yet, the stochastic
approach is in general computationally expensive and more efficient methods exist for CPE.
Stability analysis coupled with a local minimization method is the conventional way to
check if we have converged to the Gibbs energy global minimum. Even strictly formulated
deterministic global minimization can be too time consuming (Floudas and Visweswaran,
1990; McDonald and Floudas, 1995, 1997). Bonilla-Petriciolet and Segovia-Hern´andez
(2010), and Bonilla-Petriciolet et al. (2008b, 2011, 2012) provide a more comprehensive
listing of various stochastic methods.
1.2 Scope of this work
In our work, we introduce the non-stoichiometric Lagrange multipliers and modified
RAND methods to integrate them in algorithms for equilibrium calculations of non-ideal
multicomponent multiphase systems with multiple reactions. These methods are extensions
of the Lagrange multipliers method for ideal systems mentioned in Michelsen (1989) and
the ideal RAND for a single vapor phase mentioned in White et al. (1958). The successive
substitution algorithm utilizes only the first-order Lagrange multipliers method and results
in linear convergence rate for non-ideal systems. In the combined algorithm, after a few
steps of successive substitution, the second-order modified RAND method is chosen for
final convergence. The use of fugacity or activity coefficient composition derivatives and
the Gibbs energy monitoring during modified RAND steps enhances the efficiency and
robustness of the combined algorithm, which is the recommended general, quick and
reliable approach for CPE calculations. Initialization and stability analysis are included
in both algorithms, which start with the assumption of a single phase and additional
phases are considered whenever needed. The algorithms were extensively applied to
multiphase equilibrium of reaction systems that appear in the literature (VLE, LLE, VLLE

Chapter 1. Introduction 9
of one/two-reaction mixtures). Furthermore, calculations for more complex systems are
shown, such as in the transesterification of fatty acid triglycerides with methanol (five
reactions and up to three phases) as well as highly non-ideal electrolyte speciation in an
aqueous phase at equilibrium with a vapor and/or a pure solid phase.
Asecondaryprojectisalsoincludedinthisthesis. Dimethylether(DME)phaseequilibrium
was modeled with CPA EoS and PR/SRK EoS with Huron-Vidal mixing rules, intended
for the DME enhanced waterflood (DEW) process. Experimental data of DME binary
systems with water, hydrocarbons, carbon dioxide and nitrogen were used in parameter
regression. Predictions for the partitioning between aqueous and oil phases as well as
K-value sensitivity with respect to temperature, pressure, oil composition and salinity of
the aqueous phase are presented.
A brief outline of the remaining chapters in this thesis is given below, where the most
important elements are described.
Chapter 2 Thermodynamic principles and terms relevant to this work are explained.
Starting with the definition of the Gibbs energy, conditions that characterize
phase and chemical equilibrium are described. This chapter serves as a
reference for the equations that will be used throughout the thesis and can
be viewed as an introduction to the analysis of CPE calculation.
Chapter 3 Stoichiometric and non-stoichiometric Gibbs energy minimization methods
for CPE are analyzed. The emphasis is on non-stoichiometric methods
and more specifically on the Lagrange multipliers and the modified RAND
method. At the end of the chapter both methods are integrated in complete
algorithms with initialization and stability analysis, intended for multiphase
CPE calculations.
Chapter 4 The algorithms developed in Chapter 3 are applied to the most common sys-
tems in the literature and calculations are compared with published results.
Moreover, predictions are made for the complex ester mixture resulting
from the transesterification of two fatty acid triglycerides with methanol.
Finally, the speed of calculations as CPU time and the convergence rate
with iteration plots are shown.
Chapter 5 Chemical and phase equilibrium in electrolyte systems is investigated. The
basic equations for electrolyte analysis are presented. Systems containing
water,ammonia,carbondioxide,calciumchlorideandcalciumcarbonatecan
lead to the equilibrium of vapor, liquid and pure solid phases. Calculations
are made without changes in the working equations developed for non-
electrolyte mixtures.
Chapter 6 Dimethyl ether binary systems are modeled with CPA EoS and PR/SRK

| 10  | Chapter | 1. Introduction |
| --- | ------- | --------------- |
EoS with Huron-Vidal mixing rules. Parameters for different regression
strategies are shown. Predictions based on the regressed parameters are
made, especially for the change of the DME K-value between the aqueous
and the oil phase with temperature, pressure, oil composition and salinity.

C H A P T E R
2
General thermodynamic
definitions
The purpose of the following sections is to clarify necessary thermodynamic terms and
notions relevant to the algorithm development and application in succeeding chapters.
The Gibbs energy of a closed system is defined and basic equations of phase and chemical
equilibrium are presented. Finally, the ideal gas and the pure component reference state
are explained, two different reference states that will be used in calculations of reaction
systems.
2.1 System and state functions
Fundamental concepts in thermodynamics are the system, material entities it contains
and the interactions between these entities. Some of the following terms might not adhere
to the classical definitions of chemistry or physical chemistry but are based on their use in
thermodynamics and engineering practices:
system: arbitrarily defined part of the universe regardless of form or size (McNaught
•
and Wilkinson, 1997). The remaining part of the universe is called the surroundings.
Systems can be further divided into:
isolated: cannot exchange either matter or energy with the surroundings, e.g. a
◦
mixture inside a thermally insulated closed container.
closed: can only exchange energy with the surroundings, e.g. a reaction mixture in
◦
a closed flask that is cooling over an ice bath.
open: can exchange matter and energy with the surroundings, e.g. a semi-batch
◦
reactor with a constant feed flow of reactants with heating.
components: entities of a material system with identical chemical structure. For
•
example, different components are H O, CH OH, o-xylene and p-xylene. This term is
2 3
not used with the formal physical chemistry definition mentioned in McNaught and

| 12        |         |     |     |     | Chapter | 2. General thermodynamic | definitions |
| --------- | ------- | --- | --- | --- | ------- | ------------------------ | ----------- |
| Wilkinson | (1997). |     |     |     |         |                          |             |
elements: entities of a mixture whose amount or concentration can be varied inde-
•
pendently. They represent the minimum number of independent entities necessary to
define compositions in all the phases of a system. Their number may vary with external
conditions, since additional chemical equilibria will reduce their number (Rao, 1985).
This definition corresponds to the formal physical chemistry definition of the term
| “component” | (McNaught |     | and | Wilkinson, | 1997). |     |     |
| ----------- | --------- | --- | --- | ---------- | ------ | --- | --- |
phase: an entity of a material system which is uniform in chemical composition
•
and physical state (McNaught and Wilkinson, 1997). Phases are regions in space
characterized by the same values of properties, such as density, refractive index and
component composition. They are separated by distinct boundaries called interfaces.
reaction: a process that results in the interconversion of chemical species (McNaught
•
and Wilkinson, 1997). Chemical reactions may be elementary or step-wise, involving a
| single or | at least | two | consecutive | steps, | respectively. |     |     |
| --------- | -------- | --- | ----------- | ------ | ------------- | --- | --- |
The state of a system is formally described by state functions, also known as thermo-
dynamic potentials (Michelsen and Mollerup, 2007). State functions have the following
features:
| they have | exact | differentials |     |     |     |     |     |
| --------- | ----- | ------------- | --- | --- | --- | --- | --- |
•
| they are | zero or | first order | homogeneous |     | functions |     |     |
| -------- | ------- | ----------- | ----------- | --- | --------- | --- | --- |
•
| a unique | value | of the | function | corresponds | to a | specific state |     |
| -------- | ----- | ------ | -------- | ----------- | ---- | -------------- | --- |
•
the change of the function value between two states A and B does not depend on the
•
path of the transition from A to B but only on the individual states
Along with their derivatives, state functions can provide complete characterization of
the system state. A state function postulated by the first law of thermodynamics is the
| internal energy, | U:  |     |     |     |              |     |       |
| ---------------- | --- | --- | --- | --- | ------------ | --- | ----- |
|                  |     |     |     | U = | f(S,V,n,...) |     | (2.1) |
where:
| S entropy   |     |           |     |        |     |     |     |
| ----------- | --- | --------- | --- | ------ | --- | --- | --- |
| V volume    |     |           |     |        |     |     |     |
| n component |     | abundance |     | matrix |     |     |     |
The entries of matrix n are n , the mole numbers of component i in phase k. It is implied
ik
that the internal energy depends on additional variables, such as the surface area or the
total charge. We assume that the systems are not affected by external fields, the total
charge is zero and that multiple phases contribute additively to the total value of the
function:

| Chapter | 2. General |     | thermodynamic |     | definitions |     |     |     |     | 13  |
| ------- | ---------- | --- | ------------- | --- | ----------- | --- | --- | --- | --- | --- |
NP
X
|     |     |     |     |     | U = | U (S | ,V  | ,n ) |     | (2.2) |
| --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | ----- |
|     |     |     |     |     |     | k    | k k | k    |     |       |
i=1
where:
| U   | internal | energy | of  | phase | k   |     |     |     |     |     |
| --- | -------- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
k
| S   | entropy | of  | phase | k   |     |     |     |     |     |     |
| --- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
k
| V   | volume | of  | phase | k   |     |     |     |     |     |     |
| --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
k
| n   | component |     | abundance | vector |     | in phase | k   |     |     |     |
| --- | --------- | --- | --------- | ------ | --- | -------- | --- | --- | --- | --- |
k
| N   | number | of  | phases |     |     |     |     |     |     |     |
| --- | ------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
P
Eq. 2.2 is not applicable for systems of phases thinly dispersed in another phase (e.g.
colloid systems), because surface energy contributions must be also included. In this work
the internal energy is a function of entropy, volume and mole numbers:
|                  |     |        |          |          | U    | = f(S,V,n) |     |       |     | (2.3) |
| ---------------- | --- | ------ | -------- | -------- | ---- | ---------- | --- | ----- | --- | ----- |
| The differential |     | of the | internal | energy   | (Eq. | 2.3)       | is: |       |     |       |
|                  |     |        |          |          |      |            | NP  | NC    |     |       |
|                  |     |        |          |          |      |            | X   | X     |     |       |
|                  |     |        |          | dU = TdS |      | pdV        | +   | µ dn  |     | (2.4) |
|                  |     |        |          |          |      |            |     | ik ik |     |       |
−
k=1i=1
| with the | following | definitions: |     |     |     |     |     |     |     |       |
| -------- | --------- | ------------ | --- | --- | --- | --- | --- | --- | --- | ----- |
|          |           | !            |     |     | !   |     |     |   ! |     |       |
|          |           | ∂U           |     |     | ∂U  |     |     | ∂U  |     |       |
|          |           |              | =   | T   |     | =   | p   |     | = µ | (2.5) |
ik
|     |     | ∂S  |     |     | ∂V  |     | −   | ∂n       |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
|     |     |     | V,n |     |     | S,n |     | ik S,V,n |     |     |
(j6=i)k
where:
| T   | temperature |           |     |              |     |      |       |     |     |     |
| --- | ----------- | --------- | --- | ------------ | --- | ---- | ----- | --- | --- | --- |
| p   | pressure    |           |     |              |     |      |       |     |     |     |
| µ   | chemical    | potential |     | of component |     | i in | phase | k   |     |     |
ik
| N   | number | of  | components |     |     |     |     |     |     |     |
| --- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
C
| From Euler’s | theorem |     | for | homogeneous |     | functions: |     |     |     |     |
| ------------ | ------- | --- | --- | ----------- | --- | ---------- | --- | --- | --- | --- |
NP NC
X X
|     |     |     |     | U = | TS  | pV + |     | µ n   |     | (2.6) |
| --- | --- | --- | --- | --- | --- | ---- | --- | ----- | --- | ----- |
|     |     |     |     |     |     |      |     | ik ik |     |       |
−
k=1i=1
Different state functions can be defined by applying Legendre transformations to the
| internal energy: |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 14  |     |     |     |     |     | Chapter | 2.  | General |     | thermodynamic |     | definitions |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------- | --- | ------------- | --- | ----------- | --- |
|     |     |     |     |     |     |         |     |         | !   |               |     |             |     |
∂U
|     |     |     | FU[x | ,(∂U/∂x |     | ) ]  | = U | x   |     |     |     |     | (2.7) |
| --- | --- | --- | ---- | ------- | --- | ---- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     |      | j6=i    | i   | x    |     | i   |     |     |     |     |       |
|     |     |     | i    |         |     | j6=i | −   |     | ∂x  |     |     |     |       |
i
|     |     |     |     |     |     |     |     |     |     | x j6=i |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
where:
Ff Legendre transformation of function f(x) with respect to variable x
i
i
In terms of function f(x), variables x are called natural variables, whereas x and
i
(∂f/∂x ) are called conjugate variables. Legendre transformation creates a new function
| i x |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j6=i
Ff
with natural variables all x , and (∂f/∂x ) in place of x . Intensive variables of
| i   |     |     |     | j6=i |     |     | i x j6=i |     |     | i   |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
state functions do not depend on the size or amount of matter in the system. When such
| a dependency | exists, |     | the variables |     | are called | extensive. |     |     |     |     |     |     |     |
| ------------ | ------- | --- | ------------- | --- | ---------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Three of the most useful state functions derived from internal energy are:
| Enthalpy | (Legendre |     | transformation |     | of  | U with | respect |     | to V) |     |     |     |     |
| -------- | --------- | --- | -------------- | --- | --- | ------ | ------- | --- | ----- | --- | --- | --- | --- |
•
|     |     |     |     |     |     | !   |     |     |     | NP  | NC  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂U
X X
|     | H(S,p,n) |     | =   | U V |     | =   | U +pV | =   | TS  | +      | µ n |     | (2.8) |
| --- | -------- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ | --- | --- | ----- |
|     |          |     |     | −   | ∂V  |     |       |     |     |        | ik  | ik  |       |
|     |          |     |     |     |     | S,n |       |     |     | k=1i=1 |     |     |       |
Enthalpy is the internal energy of a system plus the work exerted on the surroundings
by the system, to attain final volume V and pressure p. Mathematical treatment of
open systems with mass flow or closed systems under constant entropy and pressure is
| usually | based | on enthalpy |     | analysis. |     |     |     |     |     |     |     |     |     |
| ------- | ----- | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Helmholtz energy (Legendre transformation of U with respect to S)
•
|     |          |     |     |     | !   |     |     |      |     |        |     |     |       |
| --- | -------- | --- | --- | --- | --- | --- | --- | ---- | --- | ------ | --- | --- | ----- |
|     |          |     |     |     | ∂U  |     |     |      |     | NP     | NC  |     |       |
|     |          |     |     |     |     |     |     |      |     | X      | X   |     |       |
|     | A(T,V,n) |     | =   | U S |     | =   | U   | TS = | pV  | +      | µ n |     | (2.9) |
|     |          |     |     |     | ∂S  |     |     |      |     |        | ik  | ik  |       |
|     |          |     |     | −   |     |     | −   |      | −   |        |     |     |       |
|     |          |     |     |     |     | V,n |     |      |     | k=1i=1 |     |     |       |
Helmholtz energy represents the maximum reversible work that can be performed by a
| closed | system | at constant |     | temperature |     | and | volume. |     |     |     |     |     |     |
| ------ | ------ | ----------- | --- | ----------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
Gibbs (free) energy (Legendre transformation of U with respect to S and V):
•
|     |     |          |     |     |     | ∂U ! |     |   ∂U | !   |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- |
|     |     | G(T,p,n) |     | = U | S   |      | V   |      |     | =   |     |     |     |
|     |     |          |     | −   |     | ∂S   | −   | ∂V   |     |     |     |     |     |
|     |     |          |     |     |     | V,n  |     |      | S,n |     |     |     |     |
(2.10)
|     |     |     |     |     |     |     |     |     | NP  | NC  |       |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     |     |     |     |     |     |     |     | X   | X   |       |     |     |
|     |     |     |     | = U | TS  | +pV | = H | TS  | =   | µ   | n     |     |     |
|     |     |     |     | −   |     |     |     | −   |     |     | ik ik |     |     |
k=1i=1
Gibbs energy represents the maximum reversible work that can be performed by a closed
system at constant temperature and pressure. These are frequently the conditions
of physical and chemical processes, therefore the Gibbs energy is usually selected for
thermodynamic analysis. The total differential of the Gibbs energy is:

| Chapter | 2. General |     | thermodynamic |     |     | definitions |     |     |     |     |     | 15     |
| ------- | ---------- | --- | ------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | ------ |
|         |            |     | !             |     |     | !           |     |     |     | !   |     |        |
|         |            |     | ∂G            |     |     | ∂G          |     | NP  | NC  | ∂G  |     |        |
|         |            |     |               |     |     |             |     | X   | X   |     |     |        |
|         | dG         | =   |               | dT  | +   |             | dp+ |     |     |     | dn  | (2.11) |
|         |            |     | ∂T            |     |     | ∂p          |     |     |     | ∂n  | ik  |        |
ik
|     |     |     |     | p,n |     |     | T,n | k=1i=1 |     | T,p,n |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | ----- | --- | --- |
(j6=i)k
| Taking | the | total | differential |     | of  | Eq. | 2.10 results |     | in: |     |     |     |
| ------ | --- | ----- | ------------ | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
NP NC
X X
|     |     |     |     | dG  | =   | SdT | +Vdp+ |     |     | µ dn  |     | (2.12) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- | --- | ------ |
|     |     |     |     |     |     |     |       |     |     | ik ik |     |        |
−
k=1i=1
Therefore:
|     |     |     | !   |     |     |     | !   |     |     | !   |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     | ∂G  |     |     |     | ∂G  |     |     |     | ∂G  |     |        |
|     |     |     |     | =   | S   |     |     | = V |     |     | = µ | (2.13) |
ik
|     |     | ∂T  |     | −   |     | ∂p  |     |     |     | ∂n       |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
|     |     |     | p,n |     |     |     | T,n |     |     | ik T,p,n |     |     |
(j6=i)k
| Additional |     | derivatives |     | of the | Gibbs |          | energy | are: |     |     |     |        |
| ---------- | --- | ----------- | --- | ------ | ----- | -------- | ------ | ---- | --- | --- | --- | ------ |
|            |     |             |     |        |       | " ∂(G/T) |        | #    | H   |     |     |        |
|            |     |             |     |        |       |          |        | =    |     |     |     | (2.14) |
|            |     |             |     |        |       |          | ∂T     |      | −T2 |     |     |        |
p,n
and
|     |     |     |     |     |     | "      |     | #   |     |     |     |        |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | ∂(G/T) |     |     | V   |     |     |        |
|     |     |     |     |     |     |        |     |     | =   |     |     | (2.15) |
|     |     |     |     |     |     |        | ∂p  |     | T   |     |     |        |
T,n
| 2.2 | Equilibrium |     |     |     |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Equilibrium in thermodynamics refers to a state of balance between the driving forces of
change in the system, so that no macroscopic change is observed. It is an internal state
of a system insensitive to small temporary perturbations. Thermodynamic analysis of
processes is not concerned about how fast we reach equilibrium, but the feasible limits of
| the process. | Two | types |     | of equilibrium |     |     | on which | we  | focus | are: |     |     |
| ------------ | --- | ----- | --- | -------------- | --- | --- | -------- | --- | ----- | ---- | --- | --- |
phase equilibrium: balance between the transfer of components between different
•
phases (e.g. in a vapor-liquid system, the rate of evaporation is equal to the rate of
condensation)
chemical equilibrium: balance between the transformation of reactants to products and
•
| vice | versa | (rates | of forward |     | and | backward |     | reaction | are | equal) |     |     |
| ---- | ----- | ------ | ---------- | --- | --- | -------- | --- | -------- | --- | ------ | --- | --- |

| 16    |       |     |             |     |     |     | Chapter | 2. General | thermodynamic | definitions |
| ----- | ----- | --- | ----------- | --- | --- | --- | ------- | ---------- | ------------- | ----------- |
| 2.2.1 | Phase |     | equilibrium |     |     |     |         |            |               |             |
We assume a system consisting of N phases in contact that allow exchange of components.
P
From the second law of thermodynamics, when the system attains conditions of thermo-
dynamic equilibrium, entropy has its maximum value. It follows that for two arbitrary
| phases | k and         | q:  |              |              |     |     |     |     |     |     |
| ------ | ------------- | --- | ------------ | ------------ | --- | --- | --- | --- | --- | --- |
| T =    | T (thermal    |     | equilibrium) |              |     |     |     |     |     |     |
| • k    | q             |     |              |              |     |     |     |     |     |     |
| p =    | p (mechanical |     |              | equilibrium) |     |     |     |     |     |     |
| k      | q             |     |              |              |     |     |     |     |     |     |
•
| µ    | = µ , | for i | = 1,...,N |     | (diffusive | equilibrium) |     |     |     |     |
| ---- | ----- | ----- | --------- | --- | ---------- | ------------ | --- | --- | --- | --- |
| • ik | iq    |       |           | C   |            |              |     |     |     |     |
where:
| T   | temperature |     |     | of phase | k   |     |     |     |     |     |
| --- | ----------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
k
| p   | pressure |     | of phase | k   |     |     |     |     |     |     |
| --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
k
Entropy maximization is not the only criterion for thermodynamic equilibrium. Differ-
ent conditions in terms of equivalent thermodynamic potentials are shown in Table 2.1
| (Michelsen | and | Mollerup, |     | 2007). |     |     |     |     |     |     |
| ---------- | --- | --------- | --- | ------ | --- | --- | --- | --- | --- | --- |
Table 2.1: Thermodynamic equilibrium conditions for closed systems.
|     |     |     | Natural |      | variables |      | State | function | Extremum |     |
| --- | --- | --- | ------- | ---- | --------- | ---- | ----- | -------- | -------- | --- |
|     |     |     | U,      | V, n | or H,     | p, n |       | S        | max      |     |
|     |     |     |         | S,   | V, n      |      |       | U        | min      |     |
|     |     |     |         | S,   | p, n      |      |       | H        | min      |     |
|     |     |     |         | T,   | V, n      |      |       | A        | min      |     |
|     |     |     |         | T,   | p, n      |      |       | G        | min      |     |
Chemical potentials are particularly important in equilibrium determination. The differen-
tial of the chemical potential of an ideal gas in phase k at constant temperature is given
by:
dp
|     |     |     |     |     | dµ  | =   | v dp | = RT |     | (2.16) |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | --- | ------ |
|     |     |     |     |     |     | ik  | ik   | p    |     |        |
where:
| v   | molar | volume |     | of component |     | i   | in phase | k   |     |     |
| --- | ----- | ------ | --- | ------------ | --- | --- | -------- | --- | --- | --- |
ik
| R             | gas | constant |     |           |     |             |     |     |     |     |
| ------------- | --- | -------- | --- | --------- | --- | ----------- | --- | --- | --- | --- |
| For non-ideal |     | phases,  | we  | introduce |     | fugacities: |     |     |     |     |
ˆ
df
|     |     |     |     |     |     |     | ¯    | ik   |     |        |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | --- | ------ |
|     |     |     |     |     | dµ  | =   | V dp | = RT |     | (2.17) |
|     |     |     |     |     |     | ik  | ik   | ˆ    |     |        |
f
ik

| Chapter | 2.  | General | thermodynamic |     | definitions |     |     |     | 17  |
| ------- | --- | ------- | ------------- | --- | ----------- | --- | --- | --- | --- |
After integration:
ˆ
f
|     |     |     |     |     | µ = | µ◦ +RT | ln  | ik  | (2.18) |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | ------ |
ik
|     |     |     |     |     |     | ik  |     | f◦  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ik
where:
¯
| V   | partial | molar | volume | of  | component |     | i in phase | k   |     |
| --- | ------- | ----- | ------ | --- | --------- | --- | ---------- | --- | --- |
ik
µ◦ reference state chemical potential of component i in phase k
ik
| f ˆ | fugacity | of  | component |     | i in phase | k   |     |     |     |
| --- | -------- | --- | --------- | --- | ---------- | --- | --- | --- | --- |
ik
f◦
|     | reference | state | fugacity |     | of component |     | i in | phase k |     |
| --- | --------- | ----- | -------- | --- | ------------ | --- | ---- | ------- | --- |
ik
Diffusiveequilibriumisnotuniquelyexpressedintermsofchemicalpotentials. Theequality
of chemical potentials at equilibrium results in the fugacity equality in two arbitrary phases
k and q:
|     |     |     |     |     |     | ˆ   | ˆ   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | f = | f   |     |     |
|     |     |     |     |     |     | ik  | iq  |     |     |
(2.19)
i = 1,...,N
C
However, the changes of chemical potentials are not independent in a particular phase.
The Gibbs-Duhem equation shows the dependence between different chemical potentials
in the same phase. If we use Eq. 2.10 and 2.12 for an arbitrary phase k, we have:
NC
X
|     |     |     |     |     | G   | =   | µ n   |     | (2.20) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | ------ |
|     |     |     |     |     | k   |     | ik ik |     |        |
i=1
NC
X
|     |     |     |     | dG = | S dT | +V  | dp+ | µ dn  | (2.21) |
| --- | --- | --- | --- | ---- | ---- | --- | --- | ----- | ------ |
|     |     |     |     | k    | k    |     | k   | ik ik |        |
−
i=1
where:
| G   | Gibbs | energy | of  | phase | k   |     |     |     |     |
| --- | ----- | ------ | --- | ----- | --- | --- | --- | --- | --- |
k
| By differentiating |     | Eq. | 2.20, | and | subtracting | Eq. | 2.21, | we get: |     |
| ------------------ | --- | --- | ----- | --- | ----------- | --- | ----- | ------- | --- |
NC
X
|     |     |     |     |     | n dµ  | =   | S dT | +V dp |        |
| --- | --- | --- | --- | --- | ----- | --- | ---- | ----- | ------ |
|     |     |     |     |     | ik ik |     | k    | k     |        |
|     |     |     |     |     |       | −   |      |       | (2.22) |
i=1
k = 1,...,N
P
| At constant |     | temperature | and | pressure: |     |     |     |     |     |
| ----------- | --- | ----------- | --- | --------- | --- | --- | --- | --- | --- |

| 18  |     |     |     |     | Chapter |     | 2. General |     | thermodynamic | definitions |
| --- | --- | --- | --- | --- | ------- | --- | ---------- | --- | ------------- | ----------- |
NC
X
|     |     |     |     |     | n   | dµ = | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
ik ik
(2.23)
i=1
|     |     |     |     |     | k = 1,...,N |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
P
It must be underlined, that the above expressions for the Gibbs-Duhem equation are not
general. In fact, their application is valid only in systems where the internal energy is
given by Eq. 2.3. Nevertheless, this is a reasonable assumption for the purpose of this
work.
| 2.2.2 | Chemical |     | equilibrium |     |     |     |     |     |     |     |
| ----- | -------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Studying chemical equilibrium involves identifying the reactions between the components
of a mixture. There are different ways to write the formula of a chemical reaction but a
| systematic | way      | to represent |     | it is: |        |     |     |     |     |        |
| ---------- | -------- | ------------ | --- | ------ | ------ | --- | --- | --- | --- | ------ |
|            |          |              |     | A      |        | A   |     |     |     |        |
|            |          |              |     | ν      | +...+ν |     | =   | 0   |     | (2.24) |
|            |          |              |     | 1 1    |        | NC  | NC  |     |     |        |
| or, for    | multiple | reactions:   |     |        |        |     |     |     |     |        |
NC
|     |     |     |     |     | X   | A   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | ν   | =   | 0   |     |     |     |
ir i
(2.25)
i=1
|     |     |     |     |     | r = 1,...,N |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
R
where:
| A   | component |     | i in a chemical |     | reaction |     |     |     |     |     |
| --- | --------- | --- | --------------- | --- | -------- | --- | --- | --- | --- | --- |
i
| ν   | stoichiometric |     | coefficient | of  | component |     | i in reaction |     | r   |     |
| --- | -------------- | --- | ----------- | --- | --------- | --- | ------------- | --- | --- | --- |
ir
| N   | number | of  | independent | chemical |     | reactions |     |     |     |     |
| --- | ------ | --- | ----------- | -------- | --- | --------- | --- | --- | --- | --- |
R
Stoichiometric coefficients indicate the number of molecules that take part in a reaction.
| Values | of the stoichiometric |     |     | coefficients | follow | this | convention: |     |     |     |
| ------ | --------------------- | --- | --- | ------------ | ------ | ---- | ----------- | --- | --- | --- |

|     |     |     |  < | 0 i is a | reactant | in          | reaction | r           |     |        |
| --- | --- | --- | ------- | -------- | -------- | ----------- | -------- | ----------- | --- | ------ |
|     |     |     | ν =     | 0 i does | not      | participate |          | in reaction | r   | (2.26) |
ir
>
|     |     |     |     | 0 i is a | product | in reaction |     | r   |     |     |
| --- | --- | --- | --- | -------- | ------- | ----------- | --- | --- | --- | --- |
Stoichiometric coefficients can be combined in the stoichiometric matrix N, which is a
compact way to document all the reactions between the components. It is also common to
| refer to | the total | stoichiometric |     | coefficient |     | of reaction | r   | as: |     |     |
| -------- | --------- | -------------- | --- | ----------- | --- | ----------- | --- | --- | --- | --- |

| Chapter | 2. General thermodynamic |     | definitions |     | 19  |
| ------- | ------------------------ | --- | ----------- | --- | --- |
NC
X
|     |     |     | ν   | = ν | (2.27) |
| --- | --- | --- | --- | --- | ------ |
|     |     |     | t,r | ir  |        |
i=1
When ν = 0, there is no change in the total mole numbers due to reaction r. In other
t,r
words, reactants and products have each the same number of molecules. An essential
quantity in reaction analysis is the reaction extent. These are defined to demonstrate the
degree of progression of each transformation from reactants to products. For multiple
| reactions | in a single phase: |     |     |     |     |
| --------- | ------------------ | --- | --- | --- | --- |
NR
X
|     |     |     | dn = | ν dξ | (2.28) |
| --- | --- | --- | ---- | ---- | ------ |
|     |     |     | i    | ir r |        |
r=1
where:
| ξ   | extent of reaction | r   |     |     |     |
| --- | ------------------ | --- | --- | --- | --- |
r
Despite that an arbitrary component i appears in the definition of Eq. 2.28, the reaction
extent does not depend on the component used in its calculation. Positive values imply
that the reaction proceeds from reactants to products and negative values from products to
reactants. The following example clarifies the essence of the reaction extent. Components
| A, B and | C react according | to the | scheme: |                |        |
| -------- | ----------------- | ------ | ------- | -------------- | ------ |
|          |                   |        | ν A+ν   | B (cid:10) ν C | (2.29) |
|          |                   |        | A       | B C            |        |
If the extent of the above reaction is ξ, then ν ξ moles of A reacted with ν ξ moles of B
A B
C.
to produce ν C ξ moles of For multiple phases, Eq. 2.28 becomes:
|     |     |     |          |       |        |
| --- | --- | --- | --------- | ------ | ------ |
|     |     |     | NP        | NR     |        |
|     |     |     | X         | X      |        |
|     |     |     | d  n ik | = ν dξ | (2.30) |
ir r
|     |     |     | k=1 | r=1 |     |
| --- | --- | --- | --- | --- | --- |
and:
|     |     |     | NP  | NR      |        |
| --- | --- | --- | --- | ------- | ------ |
|     |     |     | X   | X       |        |
|     |     |     | n = | n + ν ξ | (2.31) |
ik F,i ir r
|                      |       |     | k=1 | r=1 |     |
| -------------------- | ----- | --- | --- | --- | --- |
| or, in matrix-vector | form: |     |     |     |     |
NP
X
|     |     |     | n   | = n +Nξ | (2.32) |
| --- | --- | --- | --- | ------- | ------ |
|     |     |     | k   | F       |        |
k=1
where:

| 20          |     |     |           |        | Chapter  |     | 2. General | thermodynamic |     | definitions |
| ----------- | --- | --- | --------- | ------ | -------- | --- | ---------- | ------------- | --- | ----------- |
| n component |     |     | abundance | vector | in phase |     | k          |               |     |             |
k
| n component |     |     | abundance | vector | in the | feed |     |     |     |     |
| ----------- | --- | --- | --------- | ------ | ------ | ---- | --- | --- | --- | --- |
F
| N stoichiometric |         |             | matrix |           |      |          |     |     |     |     |
| ---------------- | ------- | ----------- | ------ | --------- | ---- | -------- | --- | --- | --- | --- |
| ξ vector         |         | of reaction |        | extents   |      |          |     |     |     |     |
| n mole           | numbers |             | of     | component | i in | the feed |     |     |     |     |
F,i
The degree to which reactions progress is governed by the chemical equilibrium constants.
For reaction r in phase k, the chemical equilibrium constant is defined as:
|     |     |     |     |      |       |      |      |        |  νir |        |
| --- | --- | --- | --- | ---- | ----- | ---- | ---- | ------ | ------ | ------ |
|     |     |     |     | ∆ G◦ | !     |   PN | ν    | µ◦ ! N | f ˆ    |        |
|     |     |     |     | r    |       |      | C ir | YC     | ik     |        |
|     | Keq | =   | exp | rk   | = exp |      | i= 1 | ik =   |        | (2.33) |
|     |     | rk  |     |      |       |      |      |        |  f◦  |        |
|     |     |     | −   | RT   |       | −    | RT   |        |        |        |
|     |     |     |     |      |       |      |      | i=1    | ik     |        |
where:
Keq thermodynamic equilibrium constant of reaction r in phase k
rk
| ∆ G◦ reference |     | state | Gibbs | energy | of reaction |     | r in | phase k |     |     |
| -------------- | --- | ----- | ----- | ------ | ----------- | --- | ---- | ------- | --- | --- |
r
rk
Since the Gibbs energy is a state function, formation or combustion Gibbs energies of
components can be used to calculate the Gibbs energy of reaction:
|     |     |     |     |      | NC   |      | NC  |         |     |        |
| --- | --- | --- | --- | ---- | ---- | ---- | --- | ------- | --- | ------ |
|     |     |     |     |      | X    |      | X   |         |     |        |
|     |     |     | ∆   | G◦ = | ν ∆  | G◦ = |     | ν ∆ G◦  |     | (2.34) |
|     |     |     |     | r rk | ir f | ik   |     | ir c ik |     |        |
−
|     |     |     |     |     | i=1 |     | i=1 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
where:
G◦
∆ reference state Gibbs energy of formation of component i in phase k
f ik
∆ G◦ reference state Gibbs energy of combustion of component i in phase k
c ik
The chemical equilibrium constant is a function of the same independent variables as the
standard state chemical potentials. Therefore, reference state quantities in Eq. 2.33 and
2.34 must correspond to the same temperature and pressure. Derivatives of the chemical
equilibrium constant with respect to T and p, combining Eq. 2.33, 2.14 and 2.15, are given
| by the following |     | relations: |     |     |     |     |     |     |     |     |
| ---------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
  ∂lnKeq!
∆ H◦
|     |     |     |     |     | rk  | =   | r rk |     |     | (2.35) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ------ |
|     |     |     |     |     | ∂T  |     | RT2  |     |     |        |
p
with
|     |     |     |     |     | ∂∆ H ◦ | NC  |        |     |     |        |
| --- | --- | --- | --- | --- | ------ | --- | ------ | --- | --- | ------ |
|     |     |     |     |     | r r k  | X   | C◦     |     |     |        |
|     |     |     |     |     |        | =   | ν      |     |     | (2.36) |
|     |     |     |     |     | ∂T     |     | ir p,i |     |     |        |
i=1
and

| Chapter | 2. General |     | thermodynamic |     | definitions |      |      |     | 21     |
| ------- | ---------- | --- | ------------- | --- | ----------- | ---- | ---- | --- | ------ |
|         |            |     |               |     | ∂lnKeq!     |      |      |     |        |
|         |            |     |               |     |             |      | ∆ V◦ |     |        |
|         |            |     |               |     |             | rk = | r rk |     | (2.37) |
|         |            |     |               |     | ∂p          |      | − RT |     |        |
T
where:
| ∆ H◦ | reference | state | enthalpy |     | of reaction | r in | phase k |     |     |
| ---- | --------- | ----- | -------- | --- | ----------- | ---- | ------- | --- | --- |
r rk
| ∆ V◦ | reference | state | volume | change |     | of reaction | r in phase | k   |     |
| ---- | --------- | ----- | ------ | ------ | --- | ----------- | ---------- | --- | --- |
r rk
C◦
reference state heat capacity at constant pressure of component i
p,i
When the enthalpies of reactions or heat capacities are not known, we can use formation
or combustion enthalpies at the same temperature and pressure:
|     |     |     |     |      | NC  |        | NC    |     |        |
| --- | --- | --- | --- | ---- | --- | ------ | ----- | --- | ------ |
|     |     |     | ∆   | H◦ = | X ν | ∆ H◦ = | X ν ∆ | H◦  | (2.38) |
|     |     |     | r   |      | ir  | f      | ir    | c   |        |
|     |     |     |     | rk   |     | ik     | −     | ik  |        |
|     |     |     |     |      | i=1 |        | i=1   |     |        |
Phase equilibrium analysis utilizes the K-values of components. These are essentially
distribution coefficients of a component between phase k and a reference phase q:
x
|     |     |     |     |     |     | K = ik |     |     | (2.39) |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | ------ |
ik
x
iq
| 2.2.3 | Types | of  | reference |     | states |     |     |     |     |
| ----- | ----- | --- | --------- | --- | ------ | --- | --- | --- | --- |
To calculate the absolute value of the chemical potential in Eq. 2.18, the reference state
must be decided. Convenience of calculations is often the criterion to choose between
chemical potential expressions with different reference states. It is important to be
consistent with the use of reference states in Eq. 2.18. Two of the most widely used are
| the ideal | gas and   | the | pure component |     | reference |     | state. |     |     |
| --------- | --------- | --- | -------------- | --- | --------- | --- | ------ | --- | --- |
| Ideal gas | reference |     | state:         |     |           |     |        |     |     |
•
|     |     |     |     |     |     | f◦ p∗ |     |     |        |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     |     |     |     |     | =     |     |     | (2.40) |
ik
and
|     |     |     |     |     | µ◦  | = µ∗(T,p∗) |     |     | (2.41) |
| --- | --- | --- | --- | --- | --- | ---------- | --- | --- | ------ |
|     |     |     |     |     |     | ik i       |     |     |        |
where:
| p∗  | ideal | gas | reference | pressure  |     |              |     |     |     |
| --- | ----- | --- | --------- | --------- | --- | ------------ | --- | --- | --- |
| µ∗  | ideal | gas | chemical  | potential |     | of component | i   |     |     |
i
Reference temperature is equal to the system temperature. Reference pressure is usually
selected as p∗ = 1 atm or p∗ = 1 bar. Originally, it was supposed to refer to unit

| 22  |     |     |     |     | Chapter |     | 2.  | General thermodynamic | definitions |
| --- | --- | --- | --- | --- | ------- | --- | --- | --------------------- | ----------- |
fugacity, but at low pressures fugacity and pressure do not differ much. The ideal gas
chemical potential depends only on temperature. We select this reference state when a
phase is described by an equation of state that provides us with fugacity coefficients,
| defined | as: |     |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ˆ
f
|     |     |     |     |     | φ ˆ |     | ik  |     | (2.42) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik
|     |     |     |     |     |     | ≡ x | p   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ik
where:
| φ ˆ | fugacity | coefficient |     | of component |     | i   | in phase | k   |     |
| --- | -------- | ----------- | --- | ------------ | --- | --- | -------- | --- | --- |
ik
| Fugacities     | are        | calculated | from: |        |          |     |       |       |        |
| -------------- | ---------- | ---------- | ----- | ------ | -------- | --- | ----- | ----- | ------ |
|                |            |            |       |        | f ˆ      | = x | φ ˆ p |       | (2.43) |
|                |            |            |       |        | ik       | ik  | ik    |       |        |
| and chemical   | potentials |            | from: |        |          |     |       |       |        |
|                |            |            |       |        |          |     | x     | φ ˆ p |        |
|                |            |            |       |        |          |     | ik    | ik    |        |
|                |            |            |       | µ      | = µ∗ +RT |     | ln    |       | (2.44) |
|                |            |            |       | ik     | i        |     |       | p∗    |        |
| Pure component |            | reference  |       | state: |          |     |       |       |        |
•
|     |     |     |     |     | f◦ = | f (T,p) |     |     | (2.45) |
| --- | --- | --- | --- | --- | ---- | ------- | --- | --- | ------ |
ik
ik
and
|     |     |     |     |     | µ◦ = | µpure(T,p) |     |     | (2.46) |
| --- | --- | --- | --- | --- | ---- | ---------- | --- | --- | ------ |
|     |     |     |     |     | ik   | ik         |     |     |        |
where:
| f   | fugacity | of  | pure component |     | i in | phase | k   |     |     |
| --- | -------- | --- | -------------- | --- | ---- | ----- | --- | --- | --- |
ik
µpure
|     | chemical | potential |     | of pure | component |     | i in | phase k |     |
| --- | -------- | --------- | --- | ------- | --------- | --- | ---- | ------- | --- |
ik
Reference temperature and pressure are equal to the system temperature and pressure.
Reference state chemical potential and pure component fugacity depend on T and p.
We select the pure component reference state when a phase is described by an activity
coefficient model that provides us with the symmetric activity coefficients, defined as:
f ˆ
ik
|     |     |     |     |     | γ   |     |     |     | (2.47) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik
|     |     |     |     |     |     | ≡ x | f   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | ik  | ik  |     |     |
where:

| Chapter | 2. General |     | thermodynamic |     |             | definitions |              |     |            |     | 23  |
| ------- | ---------- | --- | ------------- | --- | ----------- | ----------- | ------------ | --- | ---------- | --- | --- |
| γ       | symmetric  |     | activity      |     | coefficient |             | of component |     | i in phase | k   |     |
ik
| Fugacities   | are | calculated |     | from: |     |       |          |       |     |     |        |
| ------------ | --- | ---------- | --- | ----- | --- | ----- | -------- | ----- | --- | --- | ------ |
|              |     |            |     |       |     | f ˆ   | = x γ f  |       |     |     | (2.48) |
|              |     |            |     |       |     | ik    | ik ik ik |       |     |     |        |
| and chemical |     | potentials |     | from: |     |       |          |       |     |     |        |
|              |     |            |     |       | µ = | µpure | +RT ln(x | γ     | )   |     | (2.49) |
|              |     |            |     |       | ik  | ik    |          | ik ik |     |     |        |
Activity coefficient models usually describe non-ideal liquid phases. The fugacity of the
| liquid | pure component |     |     | i is expressed |     | as: |          |     |     |     |        |
| ------ | -------------- | --- | --- | -------------- | --- | --- | -------- | --- | --- | --- | ------ |
|        |                |     |     |                |     | f   | = psφsPe |     |     |     | (2.50) |
|        |                |     |     |                |     | il  | i i      | i   |     |     |        |
where the Poynting effect (Poynting correction) of component i is calculated as:
|     |     |     |     |     |   Z | p v | !      | " v | (p  | ps) # |        |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | ----- | ------ |
|     |     |     |     |     |     | il  |        |     | il  |       |        |
|     |     |     | Pe  | =   | exp |     | dp exp |     | −   | i     | (2.51) |
i
|     |     |     |     |     |     | ps RT | ≈   |     | RT  |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
i
where:
| ps  | vapor | pressure |     | of component |     |     | i   |     |     |     |     |
| --- | ----- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
i
φs
|     | saturation |     | fugacity |     | coefficient |     | of component |     | i   |     |     |
| --- | ---------- | --- | -------- | --- | ----------- | --- | ------------ | --- | --- | --- | --- |
i
| v   | molar | volume |     | of component |     | i   | in the liquid | phase |     |     |     |
| --- | ----- | ------ | --- | ------------ | --- | --- | ------------- | ----- | --- | --- | --- |
il
The pure component reference state introduces the activity, which shows the deviation of
the fugacity from the pure component fugacity. Activity is defined from the expression:
ˆ
f
ik
|     |     |     |     |     |     | α   |     |     |     |     | (2.52) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik f
|     |     |     |     |     |     |     | ≡ ik |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
where:
| α   | activity |     | of component |     | i   | in phase | k   |     |     |     |     |
| --- | -------- | --- | ------------ | --- | --- | -------- | --- | --- | --- | --- | --- |
ik
Therefore, an alternative equation for the chemical potential calculation is:
µpure
|     |     |     |     |     | µ   | =   | +RT | lnα |     |     | (2.53) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | ik  |     | ik  | ik  |     |     |        |
When we account for non-ideality through fugacity coefficients for vapor and liquid phases,

| 24  |     |     |     |     |     | Chapter | 2. General | thermodynamic |     | definitions |
| --- | --- | --- | --- | --- | --- | ------- | ---------- | ------------- | --- | ----------- |
we follow the φ-φ approach, whereas when an activity coefficient model is used for the
liquid phases, we follow the γ-φ approach. In case there is a need to change between these
| two reference | states | we  | can use | the | following |     | equation: |     |     |     |
| ------------- | ------ | --- | ------- | --- | --------- | --- | --------- | --- | --- | --- |
p∗
|     |     |     |     | µ∗  | µpure  | =   | RT ln |     |     | (2.54) |
| --- | --- | --- | --- | --- | ------ | --- | ----- | --- | --- | ------ |
|     |     |     |     |     | i − ik |     | f     |     |     |        |
ik
Whenusinganactivitycoefficientmodel,anequivalentfugacitycoefficientcanbecalculated
by:
|     |     |     |     |     |     | γ   | f     |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     |     |     |     | φ ˆ | =   | ik ik |     |     | (2.55) |
ik
p
As a result, derivatives of fugacity and activity coefficients are equal when they refer to
| the same phase: |     |     |     |      |     |     |      |     |     |        |
| --------------- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | ------ |
|                 |     |     |     |      |     |     |    |     |     |        |
|                 |     |     |     |      | !   |     | ˆ    |     |     |        |
|                 |     |     |     | ∂lnγ |     |     | ∂lnφ |     |     |        |
|                 |     |     |     |      | ik  | =   | ik   |     |     |        |
|                 |     |     |     |      |     |     |    |     |     |        |
|                 |     |     |     | ∂n   |     |     | ∂n   |     |     | (2.56) |
|                 |     |     |     |      | qk  | T,p | qk   |     |     |        |
T,p
|     |     |     | i,q | =   | 1,...,N |     | k = 1,...,N |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | ----------- | --- | --- | --- |
|     |     |     |     |     |         | C   |             | P   |     |     |
We define the symmetric matrix of mole number derivatives of fugacity coefficients:
|     |     |     |     |     |     |    |    |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ˆ
∂lnφ
|     |     |     |     | Φ   | =   |     | ik  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | iqk |    |    |     |     |     |
∂n
|     |     |     |     |     |     |     | qk  |     |     | (2.57) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
T,p
|     |     |     |     |     | k   | = 1,...,N |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
P
where
|     |     |     |     |     | Φ   | =   | Φ   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | iqk | qik |     |     |     |
(2.58)
|     |     |     | i,q | =   | 1,...,N |     | k = 1,...,N |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | ----------- | --- | --- | --- |
|     |     |     |     |     |         | C   |             | P   |     |     |
The Gibbs-Duhem equation (Eq. 2.23) can also be expressed in terms of the fugacity
coefficients:
|     |     |     |     |             |     |     |            |         |     |        |
| --- | --- | --- | --- | ----------- | --- | ---- | ----------- | ------- | --- | ------ |
|     | NC  |     | !   |             | NC  |      | ˆ           | NC      |     |        |
|     |     |     | ∂µ  |             |     | ∂lnφ |             |         |     |        |
|     | X   | n   | ik  | =           | X n |      | ik          | = X n Φ | = 0 |        |
|     |     | ik  |     |             |     | ik  |            | ik iqk  |     |        |
|     |     |     | ∂n  |             |     |      | ∂n          |         |     |        |
|     | i=1 |     | qk  |             | i=1 |      | qk          | i=1     |     | (2.59) |
|     |     |     |     | T,p         |     |      | T,p         |         |     |        |
|     |     |     |     | q = 1,...,N |     |      | k = 1,...,N |         |     |        |
|     |     |     |     |             |     | C    |             | P       |     |        |
or

| Chapter | 2. General thermodynamic |     |     | definitions |     | 25  |
| ------- | ------------------------ | --- | --- | ----------- | --- | --- |
|         |                          |     |     | Φ n         | = 0 |     |
k k
(2.60)
|     |     |     |     | k = 1,...,N |     |     |
| --- | --- | --- | --- | ----------- | --- | --- |
P
The selection of the reference state has an effect on the dependence of the chemical
equilibrium constant on T and p (Eq. 2.33). The ideal gas reference state renders the
chemical equilibrium constant only temperature dependent. However, even if the pure
component reference state is chosen and the resulting chemical equilibrium constant
becomes pressure dependent, pressure effect is usually assumed minor at lower pressures
| (Eq. 2.37, | ∆ V◦ 0). |     |     |     |     |     |
| ---------- | -------- | --- | --- | --- | --- | --- |
r rk
≈
Finally, ideal behavior of vapor and liquid phases refers to composition independent
fugacity or activity coefficients. More specifically, fugacity coefficients for ideal gases and
activity coefficients for ideal liquids are equal to 1. Ideal vapor fugacity and chemical
| potential | is given by: |     |     |     |     |     |
| --------- | ------------ | --- | --- | --- | --- | --- |
ˆ
|     |     |     |     | f = x | p = p | (2.61) |
| --- | --- | --- | --- | ----- | ----- | ------ |
|     |     |     |     | ik    | ik i  |        |
and
x p
|     |     |     |     | µ∗    | ik  |        |
| --- | --- | --- | --- | ----- | --- | ------ |
|     |     |     | µ   | = +RT | ln  | (2.62) |
|     |     |     | ik  | i     | p∗  |        |
where:
| p   | partial pressure | of component |     | i   |     |     |
| --- | ---------------- | ------------ | --- | --- | --- | --- |
i
| For ideal | liquid we have: |     |     |     |     |     |
| --------- | --------------- | --- | --- | --- | --- | --- |
ˆ
|     |     |     |     | f = | x f   | (2.63) |
| --- | --- | --- | --- | --- | ----- | ------ |
|     |     |     |     | ik  | ik ik |        |
and
|     |     |     | µ   | = µpure | +RT lnx | (2.64) |
| --- | --- | --- | --- | ------- | ------- | ------ |
|     |     |     | ik  |         | ik      |        |
ik
| At low pressures | in liquid | phases: |     |     |     |        |
| ---------------- | --------- | ------- | --- | --- | --- | ------ |
|                  |           |         |     | f   | ps  | (2.65) |
ik
≈ i
Therefore, the K-value (Eq. 2.39) of an ideal vapor-liquid system at low pressures is
| (Raoult’s | law): |     |     |     |     |     |
| --------- | ----- | --- | --- | --- | --- | --- |

| 26  |     |     |     | Chapter | 2. General thermodynamic | definitions |
| --- | --- | --- | --- | ------- | ------------------------ | ----------- |
|     |     |     |     | x ps    |                          |             |
iv
|     |     |     | K = | =   | i   | (2.66) |
| --- | --- | --- | --- | --- | --- | ------ |
i
|     |     |     |     | x   | p   |     |
| --- | --- | --- | --- | --- | --- | --- |
il
A generalized K-value correlation of T , p and ω is the Wilson K-factor expression:
c c
|     |     |     | p   | (cid:20)  | (cid:18)T (cid:19)(cid:21) |        |
| --- | --- | --- | --- | --------- | -------------------------- | ------ |
|     |     |     | c,i |           | c,i                        |        |
|     |     | K = | exp | 5.373(1+ω | )                          | (2.67) |
|     |     | W,i | p   |           | i T                        |        |
where:
| T critical | temperature | of component |     | i   |     |     |
| ---------- | ----------- | ------------ | --- | --- | --- | --- |
c,i
| p critical | pressure | of component | i   |     |     |     |
| ---------- | -------- | ------------ | --- | --- | --- | --- |
c,i
| ω acentric | factor | of component | i   |     |     |     |
| ---------- | ------ | ------------ | --- | --- | --- | --- |
i
The Wilson K-factors do not yield accurate results for polar components. They are usually
preferred to initialize a non-ideal multicomponent flash procedure.

C H A P T E R
3
Calculation of chemical
and phase equilibrium
Thefirstattemptstocalculatesimultaneouschemicalandphaseequilibriumwereconcerned
with the solution of the algebraic equations valid at equilibrium. These are the relations
that hold at the minimum of the Gibbs energy at constant temperature and pressure.
For instance, in the early work of Brinkley (1946, 1947) the material balance is solved,
ensuring that the sum of mole fractions in each phase is 1 and chemical potentials are
equal. However, convergence of such an approach is not guaranteed because monitoring
the Gibbs energy between iterations is not feasible.
An alternative route to the CPE solution is the direct minimization of the total Gibbs
energy of a closed system at specified temperature and pressure. In contrast to solving
algebraic equations, minimizing the Gibbs energy could allow monitoring of its value. It
is possible then to conclude if the current iteration produced an acceptable direction,
namely a descent direction pointing to the minimum. In the following sections stoichio-
metric and non-stoichiometric minimization methods are explained, with the focus on the
non-stoichiometric approach. Finally, two non-stoichiometric calculation procedures are
proposed, which are integrated in full algorithms with initialization of computations and
stability analysis to confirm that the global minimum of the Gibbs energy is found.
3.1 Gibbs energy minimization
According to Smith and Missen (1982), minimization methods in chemical and phase
equilibrium are divided into stoichiometric and non-stoichiometric based on the way the
minimization is formulated. A common constraint of both formulations is that mole
numbers cannot be negative. In general, algorithms do not account for this constraint
explicitly in the derivation of the working equations and employ different checks that
attempt to satisfy it internally.

| 28                   |     |     |     | Chapter     | 3.  | Calculation | of  | chemical | and phase | equilibrium |     |
| -------------------- | --- | --- | --- | ----------- | --- | ----------- | --- | -------- | --------- | ----------- | --- |
| 3.1.1 Stoichiometric |     |     |     | formulation |     |             |     |          |           |             |     |
In stoichiometric methods, mole numbers are expressed as functions of the reaction extents,
defined in Eq. 2.30. The Gibbs energy is then minimized with respect to the reaction
extents:
minG(T,p,ξ)
|     |     |      | ξ   |     |     |         |     |         |     |     | (3.1) |
| --- | --- | ---- | --- | --- | --- | ------- | --- | ------- | --- | --- | ----- |
|     |     | s.t. | n   | 0,  | i = | 1,...,N | k = | 1,...,N |     |     |       |
|     |     |      | ik  |     |     | C       |     |         | P   |     |       |
≥
| At the minimum, |     | the equilibrium |     | conditions |     | are: |     |      |     |     |       |
| --------------- | --- | --------------- | --- | ---------- | --- | ---- | --- | ---- | --- | --- | ----- |
|                 |     |                 |     | NP NC      |     | NC   | ∂PN |      |     |     |       |
|                 |     | ∂G              |     | X X        | ∂G  | ∂n X |     | P    | n   |     |       |
|                 |     |                 | =   |            |     | ik = | µ   | k= 1 | ik  |     | (3.2) |
ik
|     |     | ∂ξ  |     |        | ∂n  | ∂ξ    |     | ∂ξ  |     |     |     |
| --- | --- | --- | --- | ------ | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     | r   | k=1i=1 | ik  | r i=1 |     | r   |     |     |     |
or
NC
X
|     |     |     |     |     | ν   | µ = 0 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
ir ik
(3.3)
i=1
|     |     |     |     |     | k = | 1,...,N |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
P
Disregarding the non-negativity constraints, the above problem is essentially an uncon-
strained minimization. The conventional approach involves nested loop calculations,
solving phase equilibrium in the inner loop and updating the reaction extents in the outer
loop. The work of Sanderson and Chien (1973) applies such a successive substitution-based
method on reaction systems. This independent treatment of the two phenomena allows
chemical equilibrium to be coupled with an existing reliable multiphase flash code. Never-
theless, in spite of their simple implementation, nested loop schemes are not expected to
| be very efficient. |     |     |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The only second-order stoichiometric method we could find in the literature for non-ideal
mixtureswaspresentedbyCastieretal.(1989). Theauthorsappliedsuccessivesubstitution
with acceleration as initialization, and the second-order calculations were used for final
convergence. Castier et al. (1989) account simultaneously for reactions through the extents
| and for phase | separation |     | through | the | yield | factors: |     |     |     |     |     |
| ------------- | ---------- | --- | ------- | --- | ----- | -------- | --- | --- | --- | --- | --- |
n
ik
θ =
|     |     |     |     |     | ik  | PNC n |     |     |     |     |       |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | ----- |
|     |     |     |     |     |     | qk    |     |     |     |     | (3.4) |
q=1
|     |     |     |     | i = 1,...,N |     | k = | 1,...,N |     |     |     |     |
| --- | --- | --- | --- | ----------- | --- | --- | ------- | --- | --- | --- | --- |
|     |     |     |     |             | C   |     |         | P   |     |     |     |
Stoichiometric formulation is advantageous when the number of independent chemical
reactions is small (Michelsen and Mollerup, 2007). On the other hand, the main limitations

| Chapter | 3. Calculation |     | of chemical |     | and phase | equilibrium |     |     | 29  |
| ------- | -------------- | --- | ----------- | --- | --------- | ----------- | --- | --- | --- |
are initialization problems and susceptibility to round-off errors. To overcome round-off
errors, an “optimum” basis of components can be selected, the primary components, which
are the most abundant in the system (Michelsen and Mollerup, 2007). The rest of the
components are called secondary and their mole numbers can be expressed as a function
of the primary components. It is possible that primary components are the same at every
iteration. If at the current estimate a previously secondary component becomes more
abundant than a primary, the former should be included in the basis at the expense of the
later. Various publications have studied how to select the proper basis (Brinkley, 1946,
| 1947; Prigogine | and                | Defay, | 1947; | Schott, | 1964).      |     |     |     |     |
| --------------- | ------------------ | ------ | ----- | ------- | ----------- | --- | --- | --- | --- |
| 3.1.2           | Non-stoichiometric |        |       |         | formulation |     |     |     |     |
Components are not independent in reaction systems. Reactions dictate the relations
between different components. At the same time, it is implied that the later are being
produced or depleted. As a result, the material balance cannot be expressed in terms of
component mole numbers. A new basis must be selected consisting of the independent
entities, called elements. Elements usually represent building blocks of components and
they can be single chemical elements or even groups of atoms. Isomers, although sharing
the same chemical composition, must be “composed” by separate elements. Provided
that there are no additional stoichiometric constraints and we choose a set of linearly
| independent | reactions |     | (Appendix | B): |     |     |     |     |       |
| ----------- | --------- | --- | --------- | --- | --- | --- | --- | --- | ----- |
|             |           |     |           | N   | = N | N   |     |     | (3.5) |
|             |           |     |           |     | E   | C   | R   |     |       |
−
where:
| N   | number | of elements |     |     |     |     |     |     |     |
| --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
E
Non-stoichiometric methods do not take into account the reactions in a direct way. The
Gibbs energy is minimized under material balance constraints, which are expressed in
| terms of | elements: |     |             |     |       |     |            |     |     |
| -------- | --------- | --- | ----------- | --- | ----- | --- | ---------- | --- | --- |
|          |           |     |             |     |       | NP  | NC         |     |     |
|          |           |     |             |     |       | X   | X          |     |     |
|          |           |     | minG(T,p,n) |     | = min |     | n µ (T,p,n | )   |     |
|          |           |     |             |     |       |     | ik ik      | k   |     |
|          |           |     | n           |     |       | n   |            |     |     |
ik k=1i=1
|     |     |      | NP  | NC  |      |       |         |     | (3.6) |
| --- | --- | ---- | --- | --- | ---- | ----- | ------- | --- | ----- |
|     |     |      | X   | X   |      |       |         |     |       |
|     |     | s.t. |     | A n | = b  | , j = | 1,...,N |     |       |
|     |     |      |     | ji  | ik j |       | E       |     |       |
k=1i=1
|     |     |     | n   | 0, i | = 1,...,N |     | k = 1,...,N |     |     |
| --- | --- | --- | --- | ---- | --------- | --- | ----------- | --- | --- |
|     |     |     | ik  |      |           | C   |             | P   |     |
≥
where:
A number of elements j in the chemical formula of component i
ji
| b   | total mole | numbers |     | of element | j   |     |     |     |     |
| --- | ---------- | ------- | --- | ---------- | --- | --- | --- | --- | --- |
j
More conveniently, the material balance in matrix-vector form is:

| 30  |     |     |     | Chapter | 3.  | Calculation | of chemical | and phase | equilibrium |     |
| --- | --- | --- | --- | ------- | --- | ----------- | ----------- | --------- | ----------- | --- |
NP
X
|     |     |     |     |     | A   | n = b |     |     |     | (3.7) |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- |
k
k=1
where:
| A   | formula | matrix    |     |        |     |     |     |     |     |     |
| --- | ------- | --------- | --- | ------ | --- | --- | --- | --- | --- | --- |
| b   | element | abundance |     | vector |     |     |     |     |     |     |
Thematerialbalanceconstraintmustbevalidatalltimesandisindependentofthereaction
progress. It must be satisfied by the feed, unstable intermediate phase configurations or
the equilibrium solution. The element abundance vector is constant and can be calculated
by the feed:
|     |     |     |     |     | NC  |         | NC   |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ---- | --- | --- | --- |
|     |     |     |     |     | X   |         | X    |     |     |     |
|     |     |     |     | b = | A n | = n     | A z  |     |     |     |
|     |     |     |     | j   | ji  | F,i t,F | ji i |     |     |     |
(3.8)
|     |     |     |     |     | i=1 |         | i=1 |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
|     |     |     |     |     | j = | 1,...,N |     |     |     |     |
E
or
|     |     |     |     |     | b = An | = n   | Az  |     |     | (3.9) |
| --- | --- | --- | --- | --- | ------ | ----- | --- | --- | --- | ----- |
|     |     |     |     |     |        | F t,F |     |     |     |       |
where:
| n   | component | abundance |     | vector | in  | the feed |     |     |     |     |
| --- | --------- | --------- | --- | ------ | --- | -------- | --- | --- | --- | --- |
F
| z   | vector of  | mole    | fractions | in     | the feed |     |     |     |     |     |
| --- | ---------- | ------- | --------- | ------ | -------- | --- | --- | --- | --- | --- |
| n   | total mole | numbers |           | in the | feed     |     |     |     |     |     |
t,F
| z   | mole fraction | of  | component |     | i in | the feed |     |     |     |     |
| --- | ------------- | --- | --------- | --- | ---- | -------- | --- | --- | --- | --- |
i
It might be preferable to present the distribution of elements in different phases instead of
| components.     | The  | following | quantities |     | are | defined: |     |     |     |        |
| --------------- | ---- | --------- | ---------- | --- | --- | -------- | --- | --- | --- | ------ |
|                 |      |           |            |     | B   | = An     |     |     |     | (3.10) |
|                 |      |           |            |     |     | k k      |     |     |     |        |
| or collectively | in a | matrix:   |            |     |     |          |     |     |     |        |
|                 |      |           |            |     | B   | = An     |     |     |     | (3.11) |
Similar to component mole fractions, we have the element mole fractions:

| Chapter | 3. Calculation |     | of  | chemical | and | phase equilibrium |     |     |     | 31  |
| ------- | -------------- | --- | --- | -------- | --- | ----------------- | --- | --- | --- | --- |
B
jk
|     |     |     |     |     | xel | =   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
jk PN
|     |     |     |     |     |     | E   | B   |     |     | (3.12) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
q= 1 qk
k = 1,...,N
P
where:
| B   | element | abundance |     | vector | in  | phase k |     |     |     |     |
| --- | ------- | --------- | --- | ------ | --- | ------- | --- | --- | --- | --- |
k
| B   | element | abundance    |     | matrix     |     |            |     |     |     |     |
| --- | ------- | ------------ | --- | ---------- | --- | ---------- | --- | --- | --- | --- |
| B   | total   | mole numbers |     | of element |     | j in phase | k   |     |     |     |
jk
| xel | mole | fraction | of  | element | j in | phase k |     |     |     |     |
| --- | ---- | -------- | --- | ------- | ---- | ------- | --- | --- | --- | --- |
jk
When working with non-stoichiometric methods, we define the Lagrangian of the function
to eliminate the constraints. For convenience, we decided to minimize the reduced Gibbs
energyG/(RT),sinceitsharesitsminimizerwiththeGibbsenergyatconstanttemperature.
| The Lagrangian |     | is given | by: |       |     |      |     |     |      |        |
| -------------- | --- | -------- | --- | ----- | --- | ---- | --- | --- | ---- | ------ |
|                |     |          |     |       |     |      |    |     |     |        |
|                |     |          |     | NP NC | n µ | NE   | NP  | NC  |      |        |
|                |     | L(n,λ)   |     | X X   | ik  | ik X | X   | X   |      |        |
|                |     |          |     | =     |     | λ    | j  | A n | b j | (3.13) |
ji ik
|     |     |     |     |        | RT  | −   |        |     | −   |     |
| --- | --- | --- | --- | ------ | --- | --- | ------ | --- | --- | --- |
|     |     |     |     | k=1i=1 |     | j=1 | k=1i=1 |     |     |     |
where:
| λ   | vector   | of Lagrange |     | multipliers |         |     |     |     |     |     |
| --- | -------- | ----------- | --- | ----------- | ------- | --- | --- | --- | --- | --- |
| λ   | Lagrange | multiplier  |     | of          | element | j   |     |     |     |     |
j
The equilibrium solution is a stationary point of the Lagrangian. Derivatives with respect
| to mole | numbers | and | Lagrange | multipliers |         | must | satisfy:  |     |     |        |
| ------- | ------- | --- | -------- | ----------- | ------- | ---- | --------- | --- | --- | ------ |
|         |         |     |          | ∂L          | µ       | NE   |           |     |     |        |
|         |         |     |          |             |         | ik X |           |     |     |        |
|         |         |     |          |             | =       |      | A λ =     | 0   |     |        |
|         |         |     |          |             |         |      | ji j      |     |     |        |
|         |         |     |          | ∂n          | RT      | −    |           |     |     | (3.14) |
|         |         |     |          |             | ik      | j=1  |           |     |     |        |
|         |         |     |          | i =         | 1,...,N | k    | = 1,...,N |     |     |        |
|         |         |     |          |             |         | C    |           | P   |     |        |
and
|     |     |     |     | ∂L  | NP  | NC  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
X X
|     |     |     |     |     | =      | A   | n +b | = 0 |     |        |
| --- | --- | --- | --- | --- | ------ | --- | ---- | --- | --- | ------ |
|     |     |     |     |     |        | ji  | ik   | j   |     |        |
|     |     |     |     | ∂λ  | −      |     |      |     |     | (3.15) |
|     |     |     |     | j   | k=1i=1 |     |      |     |     |        |
j = 1,...,N
E
The optimization theory concludes that Lagrange multipliers indicate how sensitive the
| solution | is to | the constraints. |     | From | Eq. | 3.14 we | get: |     |     |     |
| -------- | ----- | ---------------- | --- | ---- | --- | ------- | ---- | --- | --- | --- |

| 32  |     |     |     | Chapter | 3.    | Calculation |     | of chemical | and phase | equilibrium |     |
| --- | --- | --- | --- | ------- | ----- | ----------- | --- | ----------- | --------- | ----------- | --- |
|     |     | G   |     | NP NC   | n µ   | NP          | NC  | NE          |           |             |     |
|     |     |     | min | X X     | ik ik | X           | X   | X           |           |             |     |
|     |     |     | =   |         |       | =           | n   | A λ         | =         |             |     |
|     |     | RT  |     |         | RT    |             | ik  | ji          | j         |             |     |
|     |     |     |     | k=1i=1  |       | k=1i=1      |     | j=1         |           |             |     |
(3.16)
|     |     |     |     | NE  | NP NC  |       | NE  |           |     |     |     |
| --- | --- | --- | --- | --- | ------ | ----- | --- | --------- | --- | --- | --- |
|     |     |     | =   | X λ | X X    | A n   | = X | b λ = bTλ |     |     |     |
|     |     |     |     | j   |        | ji ik |     | j j       |     |     |     |
|     |     |     |     | j=1 | k=1i=1 |       | j=1 |           |     |     |     |
and
|     |     |     |     |     |     | !   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂ G
|     |     |     |     |     | min |     | =   | λ   |     |     | (3.17) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
j
|     |     |     |     | ∂b  | RT  |       |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     |     |     | j   | T,p,b |     |     |     |     |     |
q6=j
From the perspective of Eq. 3.16, Eq. 3.14 shows that the Lagrange multipliers represent
the reduced chemical potentials of the elements at equilibrium (Michelsen and Mollerup,
2007). Eq. 3.15 is simply the constraint of the minimization. It should be stressed and
clarified that the reduced Gibbs energy is minimized, not the Lagrangian. The minimum
of the reduced Gibbs energy corresponds to a saddle point of the Lagrangian.
Stoichiometric and non-stoichiometric methods perform the same minimization in different
ways. The link they share is established between the characteristic matrices of each method:
the stoichiometric matrix N for stoichiometric methods and the formula matrix A for
non-stoichiometric methods. Multiplying Eq. 2.32 with A from the left, we have:
NP
X
|     |     |     |     | A   | n = | An  | +ANξ |     |     |     | (3.18) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ |
|     |     |     |     |     | k   | F   |      |     |     |     |        |
k=1
| Using Eq. | 3.7 and | 3.9, we | get: |     |     |     |     |     |     |     |        |
| --------- | ------- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- | ------ |
|           |         |         |      |     | ANξ | =   | 0   |     |     |     | (3.19) |
Assuming that at least one of the reactions progresses to some extent, there is at least one
| non-zero | ξ . Therefore, |     | for Eq. | 3.19 | to be | valid | for any | ξ:  |     |     |     |
| -------- | -------------- | --- | ------- | ---- | ----- | ----- | ------- | --- | --- | --- | --- |
q
|     |     |     |     |     | AN  | = 0 |     |     |     |     | (3.20) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
Eq. 3.20 shows that we need to know only one of the matrices A or N to calculate the
other. If the elements are selected, there can be found a consistent set of independent
chemical reactions and vice versa (Appendix D). A similar comment can be found in
Smith and Missen (1982). The solution of Eq. 3.20 for one of the two matrices is not
unique.

| Chapter | 3.        | Calculation | of       | chemical | and | phase | equilibrium |     |     | 33  |
| ------- | --------- | ----------- | -------- | -------- | --- | ----- | ----------- | --- | --- | --- |
| 3.1.3   | Stability |             | analysis |          |     |       |             |     |     |     |
For a fixed number of phases, it might be possible to find the minimum Gibbs energy of
the system. Nevertheless, a different number of phases could result in lower Gibbs energy.
In other words, we might have determined a local minimum if the number of phases is
allowed to change (formation or disappearance of phases). Only the global minimum of
the Gibbs energy is the actual equilibrium solution. Stability analysis investigates whether
additional phases should be considered to further decrease the Gibbs energy. If this is the
case, our current phase set is unstable. The method used in this work was presented by
Michelsen (1982) and later in Michelsen and Mollerup (2007). We check the stability of a
feed phase with composition z and total mole numbers n . Its Gibbs energy is:
t
NC
|     |     |     |     |     | G   | = n | X z µ | (z) |     | (3.21) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     |     |     |     | f   |     | t i   | i   |     |        |
i=1
The feed phase is separated into two phases. The Gibbs energy of the new phase with
| composition |     | w and infinitesimal |     |     | total | mole | numbers | (cid:15) is: |     |     |
| ----------- | --- | ------------------- | --- | --- | ----- | ---- | ------- | ------------ | --- | --- |
NC
X
|     |     |     |     |     | G((cid:15)) | = (cid:15) | w µ | (w) |     | (3.22) |
| --- | --- | --- | --- | --- | ----------- | ---------- | --- | --- | --- | ------ |
|     |     |     |     |     |             |            | i   | i   |     |        |
i=1
| The total | change | of the | Gibbs | energy |       | for this | process               | is: |     |        |
| --------- | ------ | ------ | ----- | ------ | ----- | -------- | --------------------- | --- | --- | ------ |
|           |        |        |       | ∆G     | = G(n |          | (cid:15))+G((cid:15)) | G   |     | (3.23) |
|           |        |        |       |        |       | t        |                       | f   |     |        |
|           |        |        |       |        |       | −        |                       | −   |     |        |
The first term can be approximated with the Taylor expansion around the feed:
|     |     |     |     |     |     | NC  |   ! |     | NC  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂G
|     |     |     |             |     |            | X   |      |     | X                |        |
| --- | --- | --- | ----------- | --- | ---------- | --- | ---- | --- | ---------------- | ------ |
|     |     | G(n | (cid:15)) = | G(n | ) (cid:15) | w   |      | = G | (cid:15) w µ (z) | (3.24) |
|     |     | t   | −           |     | t −        |     | i ∂n | f   | − i i            |        |
i
|          |     |               |     |     |     | i=1 |     | nt  | i=1 |     |
| -------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Finally, | Eq. | 3.23 becomes: |     |     |     |     |     |     |     |     |
NC
X
|     |     |     |     | ∆G  | = (cid:15) | w   | [µ (w) | µ (z)] |     | (3.25) |
| --- | --- | --- | --- | --- | ---------- | --- | ------ | ------ | --- | ------ |
|     |     |     |     |     |            |     | i i    | − i    |     |        |
i=1
For a spontaneous phase split, ∆G must be negative. Two equivalent functions can be
| defined, | the | tangent | plane | distance | function: |     |     |     |     |     |
| -------- | --- | ------- | ----- | -------- | --------- | --- | --- | --- | --- | --- |
NC
X
|     |     |     |     | TPD(w) |     | =   | w [µ (w) | µ (z)] |     | (3.26) |
| --- | --- | --- | --- | ------ | --- | --- | -------- | ------ | --- | ------ |
|     |     |     |     |        |     |     | i i      | i      |     |        |
−
i=1

| 34      |         |         |     | Chapter |          | 3. Calculation |     |     | of chemical | and | phase | equilibrium |     |
| ------- | ------- | ------- | --- | ------- | -------- | -------------- | --- | --- | ----------- | --- | ----- | ----------- | --- |
| and the | reduced | tangent |     | plane   | distance | function:      |     |     |             |     |       |             |     |
NC
|     |        |     | TPD(w) |     |     | h       |      |     |     |         |       | i   |        |
| --- | ------ | --- | ------ | --- | --- | ------- | ---- | --- | --- | ------- | ----- | --- | ------ |
|     | tpd(w) |     | =      |     | =   | X w lnw | +lnφ | ˆ   | (w) | lnz lnφ | ˆ (z) |     | (3.27) |
|     |        |     |        |     |     | i       | i    |     | i   | i       | i     |     |        |
|     |        |     |        | RT  |     |         |      |     | −   | −       |       |     |        |
i=1
The function used in Michelsen (1982) is a modified tangent plane distance function with
| mole numbers |     | W as | variables: |     |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
i
NC
|     |     |       |      | X   | h   |          | ˆ   |     |     | ˆ       |     | i   |        |
| --- | --- | ----- | ---- | --- | --- | -------- | --- | --- | --- | ------- | --- | --- | ------ |
|     |     | tm(W) | = 1+ |     | W   | lnW +lnφ |     | (W) | lnz | lnφ (z) | 1   |     | (3.28) |
|     |     |       |      |     | i   | i        | i   |     |     | i i     |     |     |        |
|     |     |       |      |     |     |          |     |     | −   | −       | −   |     |        |
i=1
Negative values of tm indicate an unstable feed phase. Although instability can be
identified by finding the minima of the above function (Michelsen, 1982; Michelsen and
Mollerup, 2007), there is no need to fully converge to a minimum. If a negative tm is
found during the search, the phase split will occur. Mole fractions of the trial phase can
| be then | found | as: |     |     |     |     |     |     |     |     |     |     |     |
| ------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
W
|     |     |     |     |     |     | w = |     | i   |     |     |     |     | (3.29) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
i
|     |     |     |     |     |     |     | PNC | W   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | q=1 | q   |     |     |     |     |     |
In case of a multiphase system, stability is essentially the same as for a two-phase system.
| Any phase | can | be  | used to | test | the overall | stability, |     | since: |     |     |     |     |     |
| --------- | --- | --- | ------- | ---- | ----------- | ---------- | --- | ------ | --- | --- | --- | --- | --- |
|           |     |     |         |      |             | µ          | = µ |        |     |     |     |     |     |
|           |     |     |         |      |             | ik         | iq  |        |     |     |     |     |     |
(3.30)
|     |     |     |     |     | i = | 1,...,N |     | k   | = q |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
C
∀ 6
However, initialization of this minimization for multiphase calculations requires special
care (Michelsen, 1982; Michelsen and Mollerup, 2007). Suitable initial estimates must be
| chosen | to ensure          | that | no  | minimum |     | is overlooked. |     |     |     |     |     |     |     |
| ------ | ------------------ | ---- | --- | ------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
| 3.2    | Non-stoichiometric |      |     |         |     | methods        |     |     | for | CPE |     |     |     |
calculations
| 3.2.1 | Lagrange |     | multipliers |     |     | method |     |     |     |     |     |     |     |
| ----- | -------- | --- | ----------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
†
Eq. 3.14 and 3.15 define a system of N N +N equations for N N unknown mole
|     |     |     |     |     |     | C   | P   | E   |     |     | C P |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
numbers n and N unknown Lagrange multipliers λ . In practice reaction mixtures
|     | ik  |     | E   |     |     |     |     |     | j   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
involve many components and consequently the dimensions of the system can be large.
| † Appears | in  | Tsanas | et al. | (2017b) |     |     |     |     |     |     |     |     |     |
| --------- | --- | ------ | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| Chapter | 3.  | Calculation |     | of chemical | and | phase | equilibrium |     | 35  |
| ------- | --- | ----------- | --- | ----------- | --- | ----- | ----------- | --- | --- |
Instead of solving directly the Lagrangian conditions for all n and λ , we introduce mole
ik j
| fractions | and | phase | amounts: |     |     |     |     |     |        |
| --------- | --- | ----- | -------- | --- | --- | --- | --- | --- | ------ |
|           |     |       |          |     | n   | = x | n   |     | (3.31) |
|           |     |       |          |     | ik  | ik  | t,k |     |        |
where:
| x   | mole | fraction | of  | component | i in | phase | k   |     |     |
| --- | ---- | -------- | --- | --------- | ---- | ----- | --- | --- | --- |
ik
| n   | amount | of  | phase | k   |     |     |     |     |     |
| --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
t,k
| Substitution |     | of Eq. | 3.31 | in Eq. 3.15, | gives: |     |       |       |        |
| ------------ | --- | ------ | ---- | ------------ | ------ | --- | ----- | ----- | ------ |
|              |     |        |      |              | NP     | NC  |       |       |        |
|              |     |        |      | FA           | X      | X   |       |       |        |
|              |     |        |      | =            | n      | A   | x     | b = 0 |        |
|              |     |        |      | j            | t,k    |     | ji ik | j     |        |
|              |     |        |      |              |        |     | −     |       | (3.32) |
|              |     |        |      |              | k=1    | i=1 |       |       |        |
j = 1,...,N
E
| Mole fractions |     | in each | phase | must | also satisfy: |     |     |     |     |
| -------------- | --- | ------- | ----- | ---- | ------------- | --- | --- | --- | --- |
NC
|     |     |     |     |     | FB  | X   |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | =   | x   | 1 = | 0   |        |
|     |     |     |     |     | k   | ik  |     |     |        |
|     |     |     |     |     |     |     | −   |     | (3.33) |
i=1
k = 1,...,N
P
Mole fractions appearing in 3.32 and 3.33 can be further expressed as functions of the
| Lagrange | multipliers. |               | From | Eq. 3.14: |          |          |     |       |        |
| -------- | ------------ | ------------- | ---- | --------- | -------- | -------- | --- | ----- | ------ |
|          |              |               |      |           | NE       |          | µ◦  | ˆ     |        |
|          |              |               |      |           | X        |          |     | φ p   |        |
|          |              |               |      | lnx       | = A      | λ        | ik  | ln ik | (3.34) |
|          |              |               |      | ik        |          | ji j     |     |       |        |
|          |              |               |      |           |          | −        | RT  | − f◦  |        |
|          |              |               |      |           | j=1      |          |     | ik    |        |
| For the  | ideal        | gas reference |      | state,    | Eq. 3.34 | becomes: |     |       |        |
|          |              |               |      |           | NE       |          |     | ˆ     |        |
|          |              |               |      |           |          |          | µ∗  | φ p   |        |
|          |              |               |      | lnx       | = X A    | λ        | i   | ln ik | (3.35) |
|          |              |               |      | ik        |          | ji j     |     |       |        |
|          |              |               |      |           |          | −        | RT  | − p∗  |        |
j=1
| and for | the | pure component |     | reference | state: |        |        |      |        |
| ------- | --- | -------------- | --- | --------- | ------ | ------ | ------ | ---- | ------ |
|         |     |                |     |           | NE     |        | µp ure |      |        |
|         |     |                |     |           | X      |        | ik     |      |        |
|         |     |                |     | lnx       | = A    | λ      |        | lnγ  | (3.36) |
|         |     |                |     | ik        |        | ji j − | RT     | − ik |        |
j=1
The working equations of the Lagrange multipliers method are given by Eq. 3.32 and 3.33.
Independent variables are and n , which are roots of function F at equilibrium:
|     |     |     |     | λ   | t   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

| 36  |     | Chapter |     | 3. Calculation | of chemical | and phase | equilibrium |
| --- | --- | ------- | --- | -------------- | ----------- | --------- | ----------- |
|     |     |         |     |               |            |           |             |
FA
|     |     |     | F(λ,n | ) = |     |     | (3.37) |
| --- | --- | --- | ----- | --- | --- | --- | ------ |
|     |     |     |       | t  |    |     |        |
FB
where:
| n phase | amount | vector |     |     |     |     |     |
| ------- | ------ | ------ | --- | --- | --- | --- | --- |
t
The system of equations is solved with Newton’s method. Derivatives of x with respect
ik
to the independent variables are required to find the Jacobian of F. Whenever we use the
Jacobian in calculations, we assume that the fugacity or activity coefficients are constant
(ideal system approximation). As a result, differentiation of Eq. 3.34 gives:
∂x
ik
= A x
|     |     |     | ∂λ  | qi        | ik  |     |        |
| --- | --- | --- | --- | --------- | --- | --- | ------ |
|     |     |     |     | q         |     |     | (3.38) |
|     |     |     | q   | = 1,...,N |     |     |        |
E
and
∂x
ik
= 0
∂n
|     |     |     |     | t,q       |     |     | (3.39) |
| --- | --- | --- | --- | --------- | --- | --- | ------ |
|     |     |     | q   | = 1,...,N |     |     |        |
P
| The Jacobian | matrix | of function | F has | the form: |     |     |        |
| ------------ | ------ | ----------- | ----- | --------- | --- | --- | ------ |
|              |        |             |       |          |    |     |        |
|              |        |             |       | JA        | JB  |     |        |
|              |        |             | J(λ,n | ) =      |    |     | (3.40) |
|              |        |             |       | t JC      | JD  |     |        |
where:
|     |     |     | ∂F A | NP  | NC  |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- |
X X
|     |     | JA  | = j       | = n     | A A x     |     |        |
| --- | --- | --- | --------- | ------- | --------- | --- | ------ |
|     |     | jq  |           | t,k     | ji qi ik  |     |        |
|     |     |     | ∂λ        |         |           |     | (3.41) |
|     |     |     | q         | k=1     | i=1       |     |        |
|     |     | j   | = 1,...,N | q       | = 1,...,N |     |        |
|     |     |     |           | E       | E         |     |        |
|     |     |     |           | ∂F A NC |           |     |        |
j X
|     |     |     | JB = | =   | A x   |     |        |
| --- | --- | --- | ---- | --- | ----- | --- | ------ |
|     |     |     | jq   |     | ji iq |     |        |
|     |     |     |      | ∂n  |       |     | (3.42) |
t,q i=1
|     |     | j   | = 1,...,N | q    | = 1,...,N |     |        |
| --- | --- | --- | --------- | ---- | --------- | --- | ------ |
|     |     |     |           | E    | P         |     |        |
|     |     |     | ∂F        | B NC |           |     |        |
|     |     | JC  |           | k X  | JB        |     |        |
|     |     |     | =         | = A  | x =       |     |        |
|     |     |     | kq ∂λ     |      | qi ik qk  |     |        |
|     |     |     |           | q    |           |     | (3.43) |
i=1
|     |     | k   | = 1,...,N | q   | = 1,...,N |     |     |
| --- | --- | --- | --------- | --- | --------- | --- | --- |
|     |     |     |           | P   | E         |     |     |

| Chapter | 3. Calculation | of  | chemical | and | phase | equilibrium |     |     |     | 37  |
| ------- | -------------- | --- | -------- | --- | ----- | ----------- | --- | --- | --- | --- |
∂FB
|     |     |     |     | JD  | = k | = 0 |     |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     | kq  | ∂n  |     |     |     |     | (3.44) |
t,q
|     |     |     | k = | 1,...,N |     | q = 1,...,N |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | ----------- | --- | --- | --- | --- |
|     |     |     |     |         | P   |             | P   |     |     |     |
Finally, the system of equations in the Lagrange multipliers method is:
 
∆λ
|     |     |     |     | J   | =   | F   |     |     |     | (3.45) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
 
|     |     |     |     |     | ∆n  | −   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t
or
|     |      | (cid:16) |       | (cid:17) |     |    |     |     |    |        |
| --- | ----- | -------- | ----- | -------- | ----- | --- | ---- | --- | --- | ------ |
|     |       | PNP      |       | AT       |       |     | APNP |     |     |        |
|     | Adiag |          | n     |          | Ax ∆λ |     |      |     | n b |        |
|     |       |          | k=1 k |          |       | =   |      | k=1 | k   | (3.46) |
|     |      |          |       |          |     |    |     |     | −  |        |
|     |       | (Ax)T    |       |          | 0 ∆n  |     | −    | xTe | e   |        |
|     |       |          |       |          |       | t   |      | NC  | NP  |        |
−
where:
| e   | vector of ones | with | dimensions |     | X 1 |     |     |     |     |     |
| --- | -------------- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
X
×
The Lagrange multipliers method is based on the work of Michelsen (1989). If the system is
ideal, the solution of Eq. 3.46 is the equilibrium solution. Conversely, when we are dealing
with non-ideal systems, a nested loop procedure is required: the solution of Eq. 3.46 in
the inner loop must be used to update the values of the fugacity or activity coefficients in
the outer loop, continuing until the update is smaller than a tolerance.
| 3.2.2 | The modified |     | RAND |     | method |     |     |     |     |     |
| ----- | ------------ | --- | ---- | --- | ------ | --- | --- | --- | --- | --- |
†
The RAND method was originally proposed by White et al. (1958) only for single-phase
ideal gases, with N + 1 working equations. Boynton (1960) calculated multiphase
E
ideal system equilibrium with N +N equations and suggested extension to non-ideal
|     |     |     | E   | P   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
calculations using the ideal system approximation: a nested loop scheme with constant
fugacity or activity coefficients in the inner loop and non-ideality updates in the outer loop.
Smith and Missen (1982) showed calculations for ideal multiphase systems, mentioning the
RAND method in the algorithm group “BNR” (Brinkley-NASA-RAND). They discussed
application in non-ideal mixtures and provided N linearized equilibrium equations for
C
a single phase, but did not comment on how the equations should be solved. For the
multiphase case, this strategy would result in N N +N equations.
|     |     |     |     |     |     | C P | E   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Different authors applied the RAND method to non-ideal mixtures with the ideal system
approximation (Gautam and Seider, 1979a,b,c; White and Seider, 1981; Vonˇka and Leitner,
1995) but this approach does not exhibit quadratic convergence. A second-order non-ideal
RAND formulation for multiple phases was published by Greiner (1991) with N +N
E P
| † Appears | in Tsanas | et al. | (2017a) |     |     |     |     |     |     |     |
| --------- | --------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |

| 38  |     |     |     | Chapter |     | 3. Calculation |     |     | of chemical | and phase | equilibrium |     |
| --- | --- | --- | --- | ------- | --- | -------------- | --- | --- | ----------- | --------- | ----------- | --- |
equations, but no calculations for reaction systems were included in his work. Michelsen
and Mollerup (2007) presented in brief a modified formulation, preserving the same number
of equations as in Greiner (1991). Paterson et al. (2017) showed RAND based formulations
for TP and TV thermodynamics, titled modified and vol-RAND respectively, intended
for phase equilibrium calculations. In this work the modified RAND is presented based
on the extension of the original RAND to the general case of non-ideal multiple phases.
The modified RAND method is faster and more reliable than implementations based on
the ideal system approximation. Eq. 3.14 can be linearized around the estimate of mole
numbers:
|     |     |     | µ   | NC  | ∂ (cid:18)µ | (cid:19) |     |           | NE   |     |     |        |
| --- | --- | --- | --- | --- | ----------- | -------- | --- | --------- | ---- | --- | --- | ------ |
|     |     |     | ik  | X   |             | ik       |     |           | X    |     |     |        |
|     |     |     | +   |     |             |          | ∆n  |           | λ A  | = 0 |     |        |
|     |     |     |     |     |             |          |     | qk        | j ji |     |     |        |
|     |     |     | RT  | ∂n  |             | RT       |     | −         |      |     |     | (3.47) |
|     |     |     |     | q=1 | qk          |          | T,p |           | j=1  |     |     |        |
|     |     |     |     | i = | 1,...,N     |          | k   | = 1,...,N |      |     |     |        |
|     |     |     |     |     |             | C        |     |           | P    |     |     |        |
Mole number derivatives of the chemical potentials are calculated as:
|     |     |     |     |           |          |      |     |    |     |     |     |        |
| --- | --- | --- | --- | --------- | -------- | ---- | --- | --- | ---- | --- | --- | ------ |
|     |     |     |     | (cid:18)µ | (cid:19) |      |     |     | ˆ    |     |     |        |
|     |     |     | ∂   |           |          | δ    | 1   |     | ∂lnφ |     |     |        |
|     |     |     |     | ik        |          | = iq |     | +   | ik   |     |     | (3.48) |
|     |     |     |     |           |          |      |     |    |     |     |     |        |
|     |     |     | ∂n  | RT        |          | n    | − n |     | ∂n   |     |     |        |
|     |     |     | qk  |           | T,p      | ik   | t,k |     | qk   |     |     |        |
T,p
where:
| δ   | Kronecker |     | delta |     |     |     |     |     |     |     |     |     |
| --- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ij
If an activity coefficient model is used for a liquid phase, derivatives of the activity
coefficients are equivalent, as shown in Eq. 2.56. Corrections to the mole numbers ∆n
ik
must be isolated. According to the Gibbs-Duhem equation, the matrix of the mole number
derivatives of the chemical potentials in a specific phase is singular and therefore not
| invertible | (Eq. | 2.59 | and 2.60). | We  | define | the  | following: |     |       |     |     |        |
| ---------- | ---- | ---- | ---------- | --- | ------ | ---- | ---------- | --- | ----- | --- | --- | ------ |
|            |      |      |            |     |        |     | ˆ         |     |       |     |     |        |
|            |      |      |            |     | δ      | ∂lnφ |            |     | δ     |     |     |        |
|            |      |      |            |     | iq     |      | ik         |     | iq    |     |     |        |
|            |      |      | M          | =   | +      |     |           | =   | +Φ    |     |     | (3.49) |
|            |      |      |            | iqk | n      | ∂n   |            |     | n iqk |     |     |        |
|            |      |      |            |     | ik     |      | qk         |     | ik    |     |     |        |
T,p
and
|     |     |     |     |     | PNC | ∆n  | ∆n  |     | ∆n   |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ------ |
|     |     |     |     |     | i=1 | ik  |     | t,k | t,k  |     |     |        |
|     |     |     |     | s = |     |     | =   | =   |      |     |     | (3.50) |
|     |     |     |     | k   | n   |     | n   |     | eT n |     |     |        |
|     |     |     |     |     |     | t,k |     | t,k | k    |     |     |        |
NC
| The matrix-vector |     | form | of  | Eq. 3.47 | for | different |     | phases | is: |     |     |     |
| ----------------- | --- | ---- | --- | -------- | --- | --------- | --- | ------ | --- | --- | --- | --- |
µ
|     |     |     |     | k   |     |     |      | ATλ |     |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
|     |     |     |     | +M  | ∆n  |     | s e  |     | = 0 |     |     |        |
|     |     |     |     | RT  | k   | k   | k NC |     |     |     |     |        |
|     |     |     |     |     |     | −   |      | −   |     |     |     | (3.51) |
k = 1,...,N
P

| Chapter | 3. Calculation |     | of  | chemical | and | phase | equilibrium |     |     | 39  |
| ------- | -------------- | --- | --- | -------- | --- | ----- | ----------- | --- | --- | --- |
where:
| µ   | vector | of chemical |     | potentials |     | in phase | k   |     |     |     |
| --- | ------ | ----------- | --- | ---------- | --- | -------- | --- | --- | --- | --- |
k
| s   | correction | for | the | amount | of  | phase | k   |     |     |     |
| --- | ---------- | --- | --- | ------ | --- | ----- | --- | --- | --- | --- |
k
| Corrections | to  | the component |     | abundance |      | vectors |     | are given | by:        |        |
| ----------- | --- | ------------- | --- | --------- | ---- | ------- | --- | --------- | ---------- | ------ |
|             |     |               |     |           |      |         |     | (cid:18)  | µ (cid:19) |        |
|             |     |               |     | M−1e      |      | +M−1    |     | ATλ       | k          |        |
|             |     |               | ∆n  | =         |      | s       |     |           |            |        |
|             |     |               |     | k         | k NC | k       | k   |           | RT         |        |
|             |     |               |     |           |      |         |     |           | −          | (3.52) |
k = 1,...,N
P
| From the | definition | of  | matrix | M   | (Eq. | 3.49), | we have: |     |     |     |
| -------- | ---------- | --- | ------ | --- | ---- | ------ | -------- | --- | --- | --- |
k
|     |     |     |     |     | M n | = e | +Φ  | n   |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | k   | k   | NC  | k k |     | (3.53) |
k = 1,...,N
P
| From Eq. | 2.59, | Eq. 3.53 | becomes: |     |     |     |     |     |     |     |
| -------- | ----- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
|          |       |          |          |     | M   | n   | = e |     |     |     |
|          |       |          |          |     |     | k k | NC  |     |     |     |
(3.54)
k = 1,...,N
P
| and by | inverting | matrix | M   | :   |     |     |     |     |     |     |
| ------ | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
k
M−1e
|     |     |     |     |     | n   | =   |      |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
|     |     |     |     |     |     | k   | k NC |     |     |     |
(3.55)
k = 1,...,N
P
| Substituting |     | Eq. 3.55 | in Eq. | 3.52: |     |     |          |     |          |     |
| ------------ | --- | -------- | ------ | ----- | --- | --- | -------- | --- | -------- | --- |
|              |     |          |        |       |     |     | (cid:18) |     | (cid:19) |     |
µ
|     |     |     |     | ∆n = | n s | +M−1 | ATλ |     | k   |        |
| --- | --- | --- | --- | ---- | --- | ---- | --- | --- | --- | ------ |
|     |     |     |     | k    | k k |      | k   |     |     |        |
|     |     |     |     |      |     |      |     | −   | RT  | (3.56) |
k = 1,...,N
P
Linearizing Eq. 3.7 around the estimate of mole numbers, we obtain:
NP
X
|     |     |     |     |     | A   | (n +∆n |     | ) = b |     | (3.57) |
| --- | --- | --- | --- | --- | --- | ------ | --- | ----- | --- | ------ |
|     |     |     |     |     |     | k      | k   |       |     |        |
k=1
or
|     |     |     |     |     | NP  |      |     | NP  |     |        |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ |
|     |     |     |     |     | X   |      |     | X   |     |        |
|     |     |     |     |     | A   | ∆n = | b   | B   |     | (3.58) |
|     |     |     |     |     |     | k    | −   |     | k   |        |
|     |     |     |     |     | k=1 |      |     | k=1 |     |        |

| 40  |     |     |     | Chapter |     | 3. Calculation |     | of  | chemical | and phase | equilibrium |     |
| --- | --- | --- | --- | ------- | --- | -------------- | --- | --- | -------- | --------- | ----------- | --- |
We define:
NP
|     |     |     |     |     | ∆b  | b   | X B |     |     |     |     | (3.59) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
k
|     |     |     |     |     |     | ≡ − |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
k=1
If the mole numbers satisfy the material balance, ∆b is equal to zero. There are two
| conditions | the | correction |     | vectors | ∆n  | must meet: |     |     |     |     |     |     |
| ---------- | --- | ---------- | --- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
k
NP
X
|     |     |     |     |     | A   | ∆n  | = ∆b |     |     |     |     | (3.60) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
k
k=1
and
|     |     |     |     |     | eT  | ∆n = | ∆n  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | NC  | k    |     | t,k |     |     |     |     |
(3.61)
|     |     |     |     |     | k   | = 1,...,N |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
P
| Substitution |     | of Eq. | 3.56 in | Eq. | 3.60 results | in: |     |     |     |     |     |     |
| ------------ | --- | ------ | ------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
|              |     |        | NP      |     | NP           |     |     | NP  |     |     |     |     |
µ
|     |     |     | A X n | s +A | X M−1ATλ |     | A   | X M−1 | k   | = ∆b |     | (3.62) |
| --- | --- | --- | ----- | ---- | -------- | --- | --- | ----- | --- | ---- | --- | ------ |
k k
|     |     |     |     |     |     | k   | −   |     | k RT |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
|     |     |     | k=1 |     | k=1 |     |     | k=1 |      |     |     |     |
or
|     |     |     |    |       |      |     |     |     |     |     |     |        |
| --- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     | NP  |       |       |     |     | NP  | µ   |     |     |        |
|     |     |     | X   |       |       |     |     | X   | k   |     |     |        |
|     |     |     | A   | M−1AT | λ+Bs |     | = A | M−1 |     | +∆b |     | (3.63) |
|     |     |     |    |       | k     |     |     | k   |     |     |     |        |
RT
|     |     |     | k=1 |     |     |     |     | k=1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
where:
| s            | phase | amount | correction |     | vector       |           |     |            |      |     |     |        |
| ------------ | ----- | ------ | ---------- | --- | ------------ | --------- | --- | ---------- | ---- | --- | --- | ------ |
| Substitution |       | of Eq. | 3.56 in    | Eq. | 3.61 results | in:       |     |            |      |     |     |        |
|              |       |        |            |     |              | (cid:18)  |     | µ (cid:19) |      |     |     |        |
|              |       |        | eT         | n s | +eT M−1      | ATλ       |     | k          | = ∆n |     |     |        |
|              |       |        |            | k   | k            |           |     |            |      | t,k |     |        |
|              |       |        | NC         |     | NC           | k         | −   | RT         |      |     |     | (3.64) |
|              |       |        |            |     | k            | = 1,...,N |     |            |      |     |     |        |
P
Matrix M is symmetric (Eq. 2.58), therefore, when we take the transpose of Eq.
k
3.55:
|     |     |     |     |     | nT  | = eT      | M−1 |     |     |     |     |        |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | k NC      | k   |     |     |     |     | (3.65) |
|     |     |     |     |     | k   | = 1,...,N |     |     |     |     |     |        |
P

| Chapter | 3. Calculation | of chemical | and | phase | equilibrium |     |     | 41  |
| ------- | -------------- | ----------- | --- | ----- | ----------- | --- | --- | --- |
Combining Eq. 3.50 with 3.65 and substituting them in Eq. 3.64 gives:
|     |     |     | (cid:18) |     | µ (cid:19) |     |     |     |
| --- | --- | --- | -------- | --- | ---------- | --- | --- | --- |
|     |     |     | nT       | ATλ | k =        | 0   |     |     |
|     |     |     | k        | −   | RT         |     |     |     |
(3.66)
|     |     |     |     | k = 1,...,N |     |     |     |     |
| --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
P
or
nTµ
|     |     |     | BTλ |     | k k |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
=
|     |     |     |     | k           | RT  |     |     | (3.67) |
| --- | --- | --- | --- | ----------- | --- | --- | --- | ------ |
|     |     |     |     | k = 1,...,N |     |     |     |        |
P
Finally, the modified RAND method for non-ideal multiphase mixtures requires solving
| the system | of Eq. | 3.63 and Eq. | 3.67: |     |      |         |     |        |
| ---------- | ------ | ------------ | ----- | --- | ---- | ------- | --- | ------ |
|            |       |              |     |   |      |         |    |        |
|            | APNP   | M−1AT        |       |     | APNP | M−1(µ   |     |        |
|            |        |              | B     | λ   |      | /RT)+∆b |     |        |
|            |        | k=1 k        |       | =   | k=1  | k k     |     | (3.68) |
|            |       |              |     |   |      |         |    |        |
|            |        | BT           | 0     | s   |      | d       |     |        |
where:
nTµ
|     |     |     |     | d = | k k |     |     | (3.69) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ |
k
RT
Monitoring of the Gibbs energy is the major advantage of the RAND method (original
and modified). Mole numbers satisfy the material balance at every iteration, if the initial
estimate satisfies it. In this case, the value of the Gibbs energy can be calculated and
compared with previous values, to ensure the descent to a minimum. At every iteration,
λ and s are determined from Eq. 3.68 to calculate corrections to the mole numbers from
Eq. 3.56. The mole numbers at iteration q are then updated as:
|     |     |     | n(q+1) | = n(q)      | +α∆n(q) |     |     |        |
| --- | --- | --- | ------ | ----------- | ------- | --- | --- | ------ |
|     |     |     | k      | k           |         | k   |     | (3.70) |
|     |     |     |        | k = 1,...,N |         |     |     |        |
P
using parameter α to control the step when the Gibbs energy increases or corrections
lead to negative mole numbers. In Eq. 3.68, ∆b can be omitted if the initial estimate
of n satisfies the material balance. However, in our implementation we preserve it in the
general form defined by Eq. 3.59, in order to mitigate the effect of round-off errors and
cover the cases where the initial estimates do not meet the constraint.

| 42    |                |     | Chapter |     | 3. Calculation |     | of  | chemical | and phase | equilibrium |     |
| ----- | -------------- | --- | ------- | --- | -------------- | --- | --- | -------- | --------- | ----------- | --- |
| 3.2.3 | Initialization |     |         |     |                |     |     |          |           |             |     |
To obtain initial estimates for CPE calculations, we usually need to solve a linear pro-
gramming problem (Michelsen and Mollerup, 2007). This involves the determination of
non-zero mole numbers for N components, allowing the estimation of λ and n . The
|     |     |     | E   |     |     |     |     |     |     |     | t   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
main disadvantages associated with this method are degenerate cases, poor estimation of
small concentrations and a solution with fewer than N present components. In the last
E
case, there is not enough information to estimate λ (Michelsen and Mollerup, 2007).
A different approach can be followed to avoid the linear programming problem. First, we
guess the values of the phase amounts. Based on the minimum and maximum reaction
extents, total mole numbers of a phase will be between a minimum and a maximum
number. In the special case where all reactions do not change the number of molecules,
the estimate will be equal to the total mole numbers in the feed. In this way, we can
find reasonable starting values for the phase amounts. When the n is decided, it is kept
t
| constant | and the | following | function | is   | defined: |     |     |     |     |     |        |
| -------- | ------- | --------- | -------- | ---- | -------- | --- | --- | --- | --- | --- | ------ |
|          |         |           |          |      |         |     |    |     |     |     |        |
|          |         |           |          | NP   | NC       |     |     | NE  |     |     |        |
|          |         |           |          | X    | X        |     |     | X   |     |     |        |
|          |         |           | Q(λ)     | = n  |          | x   | 1   | λ b |     |     | (3.71) |
|          |         |           |          | t,k |          | ik  |    | j   | j   |     |        |
|          |         |           |          |      |          | −   | −   |     |     |     |        |
|          |         |           |          | k=1  | i=1      |     |     | j=1 |     |     |        |
TheunconstrainedminimizationoffunctionQcanprovideinitialestimatesfortheLagrange
| multipliers. | To find | the | minimizer, | we   | need | to solve: |     |     |     |     |        |
| ------------ | ------- | --- | ---------- | ---- | ---- | --------- | --- | --- | --- | --- | ------ |
|              |         |     |            | 2Q∆λ |      | =         | Q   |     |     |     | (3.72) |
|              |         |     |            | ∇    |      | −∇        |     |     |     |     |        |
Assuming composition independent fugacity or activity coefficients, and comparing Eq.
| 3.72 with | Eq. 3.32 | and | 3.41: |      |     |      |     |     |     |     |        |
| --------- | -------- | --- | ----- | ---- | --- | ---- | --- | --- | --- | --- | ------ |
|           |          |     |       | JA∆λ |     | = FA |     |     |     |     | (3.73) |
−
or
|     |     |      |    |    |      |     |    |     |    |     |        |
| --- | --- | ----- | --- | --- | ----- | --- | --- | --- | --- | --- | ------ |
|     |     |       |     | NP  |       |     |     | NP  |     |     |        |
|     |     |       |     | X   |       |     |     | X   |     |     |        |
|     |     | Adiag |     | n   | AT ∆λ | =   | A   | n   | b   |     | (3.74) |
|     |     |      |    | k  |      |     |    | k   |    |     |        |
|     |     |       |     |     |       | −   |     |     | −   |     |        |
|     |     |       |     | k=1 |       |     |     | k=1 |     |     |        |
The entries of the diagonal matrix are the total mole numbers of each component, which
are all positive. Since the diagonal matrix is positive definite and A has full rank, matrix
JA is also positive definite. This means that Q is a strongly convex function and it has a
unique minimizer. During the minimization, parameter α controls the step at iteration q
| in case | of an increase | in  | the value | of function |     | Q:  |     |     |     |     |     |
| ------- | -------------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |

| Chapter | 3. Calculation | of chemical | and    | phase equilibrium |     | 43     |
| ------- | -------------- | ----------- | ------ | ----------------- | --- | ------ |
|         |                |             | λ(q+1) | = λ(q) +α∆λ(q)    |     | (3.75) |
The minimizer λ corresponds to the equilibrium of a hypothetical mixture of ideal phases,
with the initially assumed phase amounts. Consequently, when the guess of the phase
amounts is exactly equal to their actual equilibrium values and the phases are ideal, Q
function minimization converges to the final solution of Eq. 3.46.
| 3.3 | Non-stoichiometric |             |     | algorithms | for multiphase |     |
| --- | ------------------ | ----------- | --- | ---------- | -------------- | --- |
|     | chemical           | equilibrium |     |            |                |     |
In sections 3.2.1 and 3.2.2 we presented two numerical methods for CPE calculations of
ideal and non-ideal systems. Each method represents the core of a different algorithm we
tested for the multiphase chemical equilibrium of multicomponent systems, when multiple
reactions take place. The first algorithm is entirely based on the Lagrange multipliers
method (successive substitution algorithm). The second algorithm uses successive substi-
tution for the first steps and then switches to the modified RAND for rapid convergence
(combined algorithm). The most essential steps of both algorithms are explained below
| and are also | presented    | in Figure | 3.1. |     |     |     |
| ------------ | ------------ | --------- | ---- | --- | --- | --- |
| Successive   | substitution | algorithm |      |     |     |     |
•
1. Set temperature, pressure, specify the feed composition, assume that only a single
phase exists and guess the phase amount. It is more straightforward to guess
the mole numbers of the single phase, based on how much reactions can progress.
Although systematic generalization for a multiphase system is not addressed here,
initial estimates of phase amounts were found less critical for convergence (Appendix
E).
2. Minimize function Q mentioned in section 3.2.3 with respect to λ for the n guessed
t
in step 1. Update mole fractions from Eq. 3.34 as x = f(λ) at each iteration until
convergence. Assume ideal vapor (ideal gas) or ideal solution (ideal liquid): set for
|     |     | ˆ   |     |     | ˆ   |     |
| --- | --- | --- | --- | --- | --- | --- |
the vapor phase all φ = 1 and for the liquid phase φ = K . Find the K-values
|     |     | ik  |     |     | ik ik |     |
| --- | --- | --- | --- | --- | ----- | --- |
from Eq. 2.67 when an EoS is used or from Eq. 2.66 when an activity coefficient
model is used. When converged, calculate mole numbers as n = f(λ,n ).
t
3. Use as initial estimates the n guessed in step 1 and the at the minimum of
|     |     |     | t   |     | λ   |     |
| --- | --- | --- | --- | --- | --- | --- |
ˆ
function Q in step 2. Calculate fugacity or activity coefficients as φ = f(n ) or
ik k
γ = f(n ) and keep them constant. Solve the full system of Eq. 3.46, updating
| ik  | k   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
mole fractions from Eq. 3.34 as x = f(λ) at each iteration until convergence. When
converged, calculate mole numbers as n = f(λ,n ). This step constitutes the inner
t
loop.

| 44  |       |            |        |            | Chapter  |     | 3. Calculation |     |     | of chemical | and phase | equilibrium |     |
| --- | ----- | ---------- | ------ | ---------- | -------- | --- | -------------- | --- | --- | ----------- | --------- | ----------- | --- |
| 4.  | Check | if all     | phases | are        | ideal:   |     |                |     |     |             |           |             |     |
|     | If    | all phases |        | are ideal, | proceed. |     |                |     |     |             |           |             |     |
◦
If at least one phase is non-ideal, update fugacity or activity coefficients with the
◦
solution of the inner loop and go to step 3. Repeat until convergence. This step
|     | constitutes |            | the | outer | loop. |            |     |     |     |     |     |     |     |
| --- | ----------- | ---------- | --- | ----- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| 5.  | Check       | if current |     | phase | set   | is stable: |     |     |     |     |     |     |     |
If the phase set is stable, the equilibrium solution has been found.
◦
If the phase set is unstable, add one phase and go to step 3. Re-initialization
◦
is not required. Stability analysis provides reasonable estimates for the mole
fractions of the new phase. The amount of the new phase is set to zero and the
|          | λ   | used is   | the | one | from | the previously |     | converged |     | phase | set. |     |     |
| -------- | --- | --------- | --- | --- | ---- | -------------- | --- | --------- | --- | ----- | ---- | --- | --- |
| Combined |     | algorithm |     |     |      |                |     |           |     |       |      |     |     |
•
1. Set conditions, assume a single phase and guess the phase amount.
| 2.  | Miminize | function |     | Q   | for λ | initial | estimates. |     |     |     |     |     |     |
| --- | -------- | -------- | --- | --- | ----- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
3. Repeat steps 3 and 4 of the successive substitution algorithm for up to three
|     | outer-loop |           | iterations. |          |     |       |             |     |          |     |     |     |     |
| --- | ---------- | --------- | ----------- | -------- | --- | ----- | ----------- | --- | -------- | --- | --- | --- | --- |
|     | If         | converged |             | at three | or  | fewer | iterations, |     | proceed. |     |     |     |     |
◦
If not converged at three iterations, change to the modified RAND method
◦
solving the system of Eq. 3.68 until convergence. Fugacity or activity coefficients
|     | are   | updated    |     | as φ ˆ | = f(n | ) or       | γ = | f(n | ) at | every iteration. |     |     |     |
| --- | ----- | ---------- | --- | ------ | ----- | ---------- | --- | --- | ---- | ---------------- | --- | --- | --- |
|     |       |            |     | ik     |       | k          | ik  |     | k    |                  |     |     |     |
| 4.  | Check | if current |     | phase  | set   | is stable: |     |     |      |                  |     |     |     |
If the phase set is stable, the equilibrium solution has been found.
◦
|     | If  | the phase | set | is  | unstable, | add | one | phase | and | go to | step 3. |     |     |
| --- | --- | --------- | --- | --- | --------- | --- | --- | ----- | --- | ----- | ------- | --- | --- |
◦
Convergence is assumed when the error is less than 10−10. The error in the Q-function
| minimization |     | is defined |     | at iteration |     | q as: |     |     |     |     |     |     |     |
| ------------ | --- | ---------- | --- | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
v
u
NE
|     |     |     |     |     |          |     | u X | h λ(q) | λ(q−1) | i2  |     |     |        |
| --- | --- | --- | --- | --- | -------- | --- | --- | ------ | ------ | --- | --- | --- | ------ |
|     |     |     |     |     | error(q) | =   | u   |        |        |     |     |     | (3.76) |
|     |     |     |     |     |          |     | t   | j      | j      |     |     |     |        |
−
j=1
| For successive |     | substitution |     |     | (inner/outer |     | loop): |     |     |     |     |     |     |
| -------------- | --- | ------------ | --- | --- | ------------ | --- | ------ | --- | --- | --- | --- | --- | --- |

| Chapter |     | 3. Calculation |                       | of             | chemical | and | phase | equilibrium |         |     |     |                        | 45  |
| ------- | --- | -------------- | --------------------- | -------------- | -------- | --- | ----- | ----------- | ------- | --- | --- | ---------------------- | --- |
|         |     |                | SetT,p,nF,NP=1        |                |          |     |       |             |         |     |     | SetT,p,nF,NP=1         |     |
|         |     |                |                       | andguessnt     |          |     |       |             |         |     |     | andguessnt             |     |
|         |     |                | Findλinitialestimates |                |          |     |       |             |         |     |     | Findλinitialestimates  |     |
|         |     |                |                       | fromthentguess |          |     |       |             |         |     |     | fromthentguess         |     |
|         |     |                |                       | Solveequations |          |     |       |             |         |     |     | Successivesubstitution |     |
|         |     |                | withNewton’smethod    |                |          |     |       |             |         |     |     | forupto3iterations     |     |
|         |     |                | yes                   | Al l p         | h a ses  | no  |       |             |         |     | yes |                        |     |
| NP=NP+1 |     |                |                       |                |          |     |       | Updateγorφˆ | NP=NP+1 |     |     | Converged?             |     |
|         |     |                |                       | i d e          | a l?     |     |       |             |         |     |     |                        |     |
no
|     | no  |         |     |     | yes |            |     | no  |     | no  |         |     |      |
| --- | --- | ------- | --- | --- | --- | ---------- | --- | --- | --- | --- | ------- | --- | ---- |
|     |     | Stable? |     |     |     | Converged? |     |     |     |     | Stable? |     | RAND |
yes
yes
|     |     | Getλ,ntandxk |     |     |     |     |     |     |     |     | Getλ,ntandxk |     |     |
| --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- |
|     |     |              |     | (a) |     |     |     |     |     |     | (b)          |     |     |
Figure 3.1: Main steps of the algorithms in this work: (a) successive substitution and (b)
|     |     |     | successive | substitution |     | combined |     | with | the | modified | RAND. |     |     |
| --- | --- | --- | ---------- | ------------ | --- | -------- | --- | ---- | --- | -------- | ----- | --- | --- |
v
u
|     |     |              |          |      | u NE    | h    |        | i2  | NP h   |        | i2  |     |        |
| --- | --- | ------------ | -------- | ---- | ------- | ---- | ------ | --- | ------ | ------ | --- | --- | ------ |
|     |     |              | error(q) |      | u X     | λ(q) | λ(q−1) |     | X n(q) | n(q−1) |     |     |        |
|     |     |              |          |      | =       |      |        | +   |        |        |     |     | (3.77) |
|     |     |              |          |      | t       | j    | − j    |     |        | t,k −  | t,k |     |        |
|     |     |              |          |      | j=1     |      |        |     | k=1    |        |     |     |        |
| and | for | the modified |          | RAND | method: |      |        |     |        |        |     |     |        |
v
|     |     |     |     |     |          | u   | NP NC |        |        |     |     |     |        |
| --- | --- | --- | --- | --- | -------- | --- | ----- | ------ | ------ | --- | --- | --- | ------ |
|     |     |     |     |     |          | u   | X X   | h n(q) | n(q−1) | i2  |     |     |        |
|     |     |     |     |     | error(q) | = t |       |        |        |     |     |     | (3.78) |
|     |     |     |     |     |          |     |       | ik     | ik     |     |     |     |        |
−
k=1i=1
The unknown variables in the algorithms (Eq. 3.46 and 3.68) are N +N . The original
|     |     |     |     |     |     |     |     |     |     |     | E P |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
working equations of the Lagrangian (Eq. 3.14 and 3.15) require a total of N N +N
|     |     |     |     |     |     |     |     |     |     |     |     | C   | P E |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
variables, whereas the Lagrange multipliers method and the modified RAND method
use (N 1)N fewer variables. In multiphase multicomponent mixtures this difference
|     | C   |     | P   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
| becomes |     | more | prominent. |     |     |     |     |     |     |     |     |     |     |
| ------- | --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The successive substitution algorithm is expected to be slower as it utilizes a first-order
method that does not take advantage of fugacity or activity composition derivatives. An
accelerated technique could be employed, such as the the General Dominant Eigenvalue
Method(GDEM)(CroweandNishio,1975). Althoughaccelerationcanreducecomputation
time, calculation could become unstable. To validate if an accelerated step should be
accepted, the value of the Gibbs energy must be decreasing. Checking the value of
G = f(λ,n ) is not possible because the constraints are not satisfied at every iteration.
t
| Instead, |     | the material |     | balance | is a | working | equation. |     |     |     |     |     |     |
| -------- | --- | ------------ | --- | ------- | ---- | ------- | --------- | --- | --- | --- | --- | --- | --- |

46 Chapter 3. Calculation of chemical and phase equilibrium
The Q function minimization initializes calculations for both algorithms with the ideal
system approximation and a single phase. This minimization could be also achieved under
different assumptions. A multiphase mixture can be chosen (N > 1) and fugacity/activity
P
coefficients can be calculated for an ideal mixture. Alternatively, the system can be
considered non-ideal and fugacity/activity coefficients can be calculated for the current
composition estimate and kept constant. The Hessian of function Q is always positive
definite, thus the minimization is a safe procedure.
The algorithms presented in Figure 3.1 are intended to provide a general solution, without
prior knowledge of the phase number or the distribution of components in the different
phases. Our trials showed that the algorithms can also converge if the initial assumption
is N > 1, saving calculation time for more than one phase at equilibrium. However, the
P
focus of this work was to determine the equilibrium solution by sequentially adding phases
after the previous phase set has converged.
Finally, the CPE solvers and the thermodynamic routines are coded in FORTRAN
with the IntelR Parallel Studio XE 2015 compiler. In this implementation, we used
(cid:13)
functions provided by the IntelR MKL libraries (LAPACK). Function DSYTRF is required
(cid:13)
tofactorizeasymmetricmatrix(LDLdecomposition),DSYTRStosolvethelinearsystemand
DSYTRI to invert a symmetric matrix. Similar performance is expected by other Cholesky
decomposition routines. Furthermore, EoS or activity coefficient models are included in a
modular way, to effectively make the algorithms “fugacity-expression” independent. The
input of a fugacity routine is temperature, pressure and component mole numbers of a
phase to calculate fugacity coefficients. This can be done directly from an EoS after solving
for volume, or from an activity coefficient model using Eq. 2.55.
3.4 Conclusions
Gibbs energy minimization methods in CPE are classified as stoichiometric and non-
stoichiometric. Stoichiometric methods with reaction extents as independent variables
are associated with certain disadvantages, such as the selection of primary/secondary
components to avoid round-off errors and challenging initialization. For this reason, we
selected non-stoichiometric methods for CPE calculation in our work. The Lagrange
multipliers method and the modified RAND method were derived and presented in their
generalformfornon-idealmultiphasesystems. Lagrangemultipliersandphaseamountsare
theindependentvariablesforbothmethods, atotalof(N 1)N fewervariablescompared
C P
−
with the conventional method based on the Lagrangian conditions at equilibrium.
The Lagrange multipliers method for non-ideal systems is a first-order nested-loop method.
Although the inner loop is a second-order procedure, inner-loop calculations are performed
under constant fugacity or activity coefficients with outer-loop non-ideality updates. For
ideal gas/ideal solution phases, no outer-loop updates are required and the procedure
shows quadratic convergence. Logarithms of mole fractions are expressed as a function

Chapter 3. Calculation of chemical and phase equilibrium 47
of Lagrange multipliers, therefore the actual mole fractions are always expected to be
positive.
The modified RAND is a second-order method for both ideal and non-ideal systems. The
material balance is not a working equation as in the Lagrange multipliers method. Instead,
it is satisfied at every iteration, allowing monitoring of the Gibbs energy and enhancing
the robustness of the method. Corrections for trace components might lead to negative
mole numbers, but this can be overcome with the control of the Newton step. Compared
with different nested (first-order) RAND implementations published in the literature, the
modified RAND method can be used for multiphase reaction systems, while preserving its
quadratic convergence rate even for non-ideal systems.
Initialization is required for the numerical methods presented in this section. Values
for phase amounts must be assumed based on the mole number changes caused by the
reactions. At constant phase amounts, a convex function Q is defined and minimized
under the ideal system approximation. The minimizer represents the initial estimates for
the Lagrange multipliers. With a positive definite Hessian, the minimization of function
Q is always a safe procedure and control of the Newton step is only needed when its
value is increasing due to overstepping. This minimization results in the equilibrium of a
hypothetical ideal gas/ideal solution system with the initially assumed phase amounts.
If the phase amount guesses coincide with the actual equilibrium phase amounts and
the systems are ideal, the CPE solution can be obtained from this minimization. It was
found that the convergence of the Lagrange multipliers method or the modified RAND
method are not particularly influenced by initial estimates of the phase amounts during
this step.
Finally, CPEmethods, initializationandstabilityanalysisarecoupledinnon-stoichiometric
algorithms. The first algorithm uses only the Lagrange multipliers method (successive
substitution algorithm). The second algorithm combines the Lagrange multipliers method
for the first few iterations with the much faster modified RAND method that accelerates
convergence (combined algorithm). The algorithms are intended for calculations where
no information about the equilibrium phases is available. Therefore, initialization is
performed in the beginning assuming one phase and when the single phase converges,
stability analysis investigates if a second phase should be considered. Stability analysis
provides a good estimate of the new phase composition and there is no need to re-initialize
with the new phase set. In the same fashion, new phases are added and converged until
the current phase set is stable, which means that the Gibbs energy global minimum has
been found. More than one phase can be initially assumed to save computation time
but this work is focused on presenting and applying a more general approach by starting
calculations with one phase.

| C H A P T | E R |     |     |     |     |
| --------- | --- | --- | --- | --- | --- |
4
|     |     |            |     | Application | of CPE  |
| --- | --- | ---------- | --- | ----------- | ------- |
|     |     | algorithms |     | to reaction | systems |
The most common reaction systems in the literature are tested with the successive
substitution and the combined algorithm. Calculations in this work are compared with
published results of two- and three-phase mixtures where one or two reactions can take
place. Then, the algorithms are applied to a more complex five-reaction system, which
is the basis of the biodiesel synthesis: transesterification of fatty acid triglycerides with
methanol. For this purpose we used two different starting triglycerides that lead to two
separate mixtures of esters. Finally, speed of calculations and convergence behavior is
presented for all the systems in this chapter to evaluate the efficiency of the proposed
algorithms.
| 4.1 CPE | calculations |     | for systems | in the |     |
| ------- | ------------ | --- | ----------- | ------ | --- |
literature
†
For convenience, components and elements are numbered in each mixture. Table 4.1
illustrates the identity of components and the chemical composition of elements in the
systems included in this work. Apart from the calculations of component mole fractions, a
useful measure to quantify phase distribution is the mole fraction of phase k:
n
t,k
β = (4.1)
|     |     |     | k PNP | n   |     |
| --- | --- | --- | ----- | --- | --- |
t,q
q=1
Calculations concern VLE, LLE and VLLE systems. All equations where developed using
“x ” as the mole fraction of component i in phase k. Nevertheless, to avoid using double
ik
subscripts (e.g. x component 3 in the 1st phase), we refer to mole fractions of component
31
i in vapor phase as “y ”, in the first liquid phase as “x ” and in the second liquid phase as
|           | i            |               |     | i   |     |
| --------- | ------------ | ------------- | --- | --- | --- |
| † Appears | in Tsanas et | al. (2017a,b) |     |     |     |

50 Chapter 4. Application of CPE algorithms to reaction systems
“x0”.
i
Table 4.1: Component and element numbering for the systems examined.
| System |     |     | 1   | 2   |     | 3   | 4 5 | 6 7 |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Formaldehyde/ Component formaldehyde water methyleneglycol oxydimethanol
| water | Element | CH2O |     | H2O |     |     |     |     |
| ----- | ------- | ---- | --- | --- | --- | --- | --- | --- |
Xylene Component di-tert-butylbenzene m-xylene tert-butyl-m-xylene tert-butylbenzene benzene p-xylene
| separation | Element | C6H6 |     | C4H8 |     | C8H10 | C8H10 |     |
| ---------- | ------- | ---- | --- | ---- | --- | ----- | ----- | --- |
Aceticacid/ethanol Component aceticacid ethanol water ethylacetate
| esterification | Element | C2H2O |     | C2H6O |     | H2O |     |     |
| -------------- | ------- | ----- | --- | ----- | --- | --- | --- | --- |
Aceticacid/1-butanol Component aceticacid 1-butanol water butylacetate
| esterification | Element   | C2H2O     |     | C4H10O   |     | H2O      |      |     |
| -------------- | --------- | --------- | --- | -------- | --- | -------- | ---- | --- |
| MTBE           | Component | isobutene |     | methanol |     | n-butane | MTBE |     |
| synthesis      | Element   | C4H8      |     | CH4O     |     | C4H10    |      |     |
TAMEsynthesis Component 2-methyl-1-butene 2-methyl-2-butene methanol TAME n-pentane
| 1reaction   | Element   | C2.5H5  |     | C2.5H5   |             | CH4O  | C5H12 |     |
| ----------- | --------- | ------- | --- | -------- | ----------- | ----- | ----- | --- |
| 2reactions  | Element   | C5H10   |     | CH4O     |             | C5H12 |       |     |
| Propene     | Component | propene |     | water    | 2-propanol  |       |       |     |
| hydration   | Element   | C3H6    |     | H2O      |             |       |       |     |
| Cyclohexane | Component | benzene |     | hydrogen | cyclohexane |       |       |     |
| synthesis   | Element   | C6H6    |     | H2       |             |       |       |     |
Methanol Component carbonmonoxide carbondioxide hydrogen water methanol methane octadecane
| synthesis | Element | CO  |     | O   |     | H2  | CH4 C18H38 |     |
| --------- | ------- | --- | --- | --- | --- | --- | ---------- | --- |
For the analysis of reaction systems, Ung and Doherty (1995b,d) introduced a set of N
E
transformedcompositionvariablesbasedonasetofN referencecomponents. Transformed
R
| mole fractions | X defined | as: |     |     |     |     |     |     |
| -------------- | --------- | --- | --- | --- | --- | --- | --- | --- |
i
|     |     |     |     | x   | ν V−1x |     |     |       |
| --- | --- | --- | --- | --- | ------ | --- | --- | ----- |
|     |     |     |     | i   | i      | ref |     | (4.2) |
|     |     |     |     | X = | −      |     |     |       |
|     |     |     |     | i 1 | νTV−1x |     |     |       |
t ref
−
where:
| ν   | vector of all | stoichiometric |     | coefficients |     | for component | i   |     |
| --- | ------------- | -------------- | --- | ------------ | --- | ------------- | --- | --- |
i
| ν   | vector of total | stoichiometric |     | coefficients |     |     |     |     |
| --- | --------------- | -------------- | --- | ------------ | --- | --- | --- | --- |
t
V stoichiometric matrix of reference components in Ung and Doherty (1995b,d)
x reference component mole fractions in Ung and Doherty (1995b,d)
ref
| A property | of the transformed |     | mole | fractions | is: |     |     |     |
| ---------- | ------------------ | --- | ---- | --------- | --- | --- | --- | --- |
NE
X
|     |     |     |     |     | X = 1 |     |     | (4.3) |
| --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
i
i=1
When mole fractions of different phases are selected, such as y or x0, we can calculate
i i
transformed Y or X0 respectively. In phase equilibrium of non-reaction systems, azeotropes
i
i
| are identified | when: |     |     |     |     |     |     |       |
| -------------- | ----- | --- | --- | --- | --- | --- | --- | ----- |
|                |       |     |     | y   | = x |     |     | (4.4) |
Ung and Doherty (1995b,d) have proven that this is not necessarily true for reaction

Chapter 4. Application of CPE algorithms to reaction systems 51
systems. However, the use of transformed compositions can preserve this equality at the
reactive azeotrope:
|     |     |     |     | Y = | X   |     |     |     | (4.5) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
Derivation and implications of transformed variables can be found in Ung and Doherty
(1995b,d). In some publications, only equilibrium transformed mole fractions are available
for comparison.
| 4.1.1 Formaldehyde/water |     |     |     | mixture |     |     |     |     |     |
| ------------------------ | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
Maurer (1986) presented a number of reactions occurring in aqueous solutions of formalde-
hyde:
(cid:10)
|     |     | CH  | O+H | O   | CH  | O   |     |     | (4.6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     | 2   | 2   |     | 4 2 |     |     |       |
(cid:10)
| HO-(CH | O)  | -H+CH |     | O   | HO-(CH |     | O) -H+H | O   | (4.7) |
| ------ | --- | ----- | --- | --- | ------ | --- | ------- | --- | ----- |
|        | 2   | n−1   |     | 4 2 |        | 2   | n       | 2   |       |
|        |     |       |     | n   | 2      |     |         |     |       |
≥
We base our calculations on the approach of Ung and Doherty (1995e), who studied the
reaction system for n = 2:
|     |     | CH  | O+H | O          | (cid:10) CH | O   |     |     | (4.8) |
| --- | --- | --- | --- | ---------- | ----------- | --- | --- | --- | ----- |
|     |     |     | 2   | 2          |             | 4 2 |     |     |       |
|     |     | 2CH | O   | (cid:10) C | H O +H      | O   |     |     | (4.9) |
|     |     |     | 4 2 | 2          | 6 3         | 2   |     |     |       |
where formaldehyde reacts with water to produce methylene glycol and two molecules
of methylene glycol produce oxydimethanol and water. The number of elements is
N = N N = 4 2 = 2. The formula matrix and stoichiometric matrix of the system
E C R
− −
are given by:
|     |    |     |    |     |     |     |     | T  |        |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ |
|     | 1   | 0 1 | 2   |     | 1    | 1   | 1 0 |     |        |
| A   | =  |     |    | N   | = − | −   |     |    | (4.10) |
|     | 0   | 1 1 | 1   |     | 0    | 1   | 2 1 |     |        |
−
Vapor phase is ideal gas and liquid phase is ideal solution (Ung and Doherty, 1995e).
Chemical equilibrium constants and vapor pressures were taken from Maurer (1986).
Oxydimethanol is considered non-volatile and its vapor concentration is zero, as for all
oligomers in the original study from Maurer (1986). Equilibrium T-y-x diagrams at 1 atm

52 Chapter 4. Application of CPE algorithms to reaction systems
| 380 |     |     | 380 |     |     |
| --- | --- | --- | --- | --- | --- |
360
360
340
| )K(         |     | )K(         | 340 |     |     |
| ----------- | --- | ----------- | --- | --- | --- |
| erutarepmeT |     | erutarepmeT |     |     |     |
| 320         |     |             | 320 |     |     |
| 300         |     |             | 300 |     |     |
| 280         |     |             | 280 |     |     |
| 260         |     |             | 260 |     |     |
240
240
| 0 0.2 | 0.4 0.6 | 0.8 1 | 0 0.2 | 0.4 0.6 | 0.8 1 |
| ----- | ------- | ----- | ----- | ------- | ----- |
Formaldehydemolefraction
Watermolefraction
|                 | (a)          |             |                           | (b)     |       |
| --------------- | ------------ | ----------- | ------------------------- | ------- | ----- |
| 380             |              |             | 380                       |         |       |
| 360             |              |             | 360                       |         |       |
| )K( 340         |              | )K(         | 340                       |         |       |
| erutarepmeT     |              | erutarepmeT |                           |         |       |
| 320             |              |             | 320                       |         |       |
| 300             |              |             | 300                       |         |       |
| 280             |              |             | 280                       |         |       |
| 260             |              |             | 260                       |         |       |
| 240             |              |             | 240                       |         |       |
| 0 0.2           | 0.4 0.6      | 0.8 1       | 0 0.2                     | 0.4 0.6 | 0.8 1 |
| Methyleneglycol | molefraction |             | Oxydimethanolmolefraction |         |       |
|                 | (c)          |             |                           | (d)     |       |
Figure 4.1: Equilibrium T-y-x diagrams in formaldehyde/water mixture at 1 atm: (a)
formaldehyde, (b) water, (c) methylene glycol, (d) oxydimethanol [vapor ( ), liquid
|     |     | ( )]. |     |     |     |
| --- | --- | ----- | --- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 53
for all components are presented in Figure 4.1, matching the results published by Ung and
| Doherty | (1995e). |     |     |     |     |     |     |
| ------- | -------- | --- | --- | --- | --- | --- | --- |
Reaction system components do not always cover the full mole fraction range [0,1] (Ung
and Doherty, 1995e). For instance, Eq. 4.9 shows that methylene glycol cannot be pure,
since it reacts with other methylene glycol molecules to produce oxydimethanol. Methylene
glycol is relatively non-volatile with maximum concentration in the vapor phase less than
0.1% mol at 315.98 K. Maximum mole fractions in the liquid phase are 0.24 at 304.07
K for methylene glycol and 0.60 at 285.02 K for oxydimethanol. Equilibrium diagrams
at 1 atm are presented in Figure 4.2 using transformed compositions. For this system,
| transformed | compositions |     | are calculated | by: |         |     |        |
| ----------- | ------------ | --- | -------------- | --- | ------- | --- | ------ |
|             |              |     | x +x +2x       |     | x +x    | +x  |        |
|             |              |     | 1 3            | 4   | 2 3     | 4   |        |
|             |              | X   | =              | X   | =       |     | (4.11) |
|             |              |     | 1              |     | 2       |     |        |
|             |              |     | 1+x +2x        |     | 1+x +2x |     |        |
|             |              |     | 3              | 4   | 3       | 4   |        |
using methylene glycol and oxydimethanol as reference components. At the current
| pressure, | no reactive | azeotrope | is identified. |     |     |     |     |
| --------- | ----------- | --------- | -------------- | --- | --- | --- | --- |
| 380       |             |           |                |     | 1   |     |     |
360
0.8
340
)K(
0.6
erutarepmeT
320
Y
| 300 |     |     |     |     | 0.4 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
280
0.2
260
| 240 |     |     |         |     | 0     |         |       |
| --- | --- | --- | ------- | --- | ----- | ------- | ----- |
| 0   | 0.2 | 0.4 | 0.6 0.8 | 1   | 0 0.2 | 0.4 0.6 | 0.8 1 |
|     |     | Y   | , X     |     |       | X       |       |
1 1
|     |     | (a) |     |     |     | (b) |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
Figure 4.2: Equilibrium in formaldehyde/water mixture at 1 atm: (a) T-Y-X diagram of
formaldehyde [vapor ( ), liquid ( )], (b) Y-X diagram of formaldehyde and water
|       |        |            | [formaldehyde | ( ), | water ( )]. |     |     |
| ----- | ------ | ---------- | ------------- | ---- | ----------- | --- | --- |
| 4.1.2 | Xylene | separation |               |      |             |     |     |
Separating a mixture of isomers is not usually achieved by simple distillation, because
boilingpointsaretooclosefordistillationtobeadvantageous. Saitoetal.(1971)attempted
to separate m- and p-xylene in a reactive distillation column, seeing that the former
| participates | in the | following | reactions: |     |     |     |     |
| ------------ | ------ | --------- | ---------- | --- | --- | --- | --- |

54 Chapter 4. Application of CPE algorithms to reaction systems
|     |     |     |     | C H +m-C | H (cid:10)      | C H +C   | H   |     | (4.12) |
| --- | --- | --- | --- | -------- | --------------- | -------- | --- | --- | ------ |
|     |     |     |     | 14 22    | 8 10            | 12 18 10 | 14  |     |        |
|     |     |     |     | C H      | +m-C H (cid:10) | C H +C   | H   |     | (4.13) |
|     |     |     |     | 10 14    | 8 10            | 12 18 6  | 6   |     |        |
where di-tert-butylbenzene reacts with m-xylene to give tert-butyl-m-xylene and tert-
butylbenzene,whiletert-butylbenzenereactswithm-xylenetoproducetert-butyl-m-xylene
and benzene (p-xylene is an inert). The number of elements is N = N N = 6 2 = 4.
|     |     |     |     |     |     |     | E   | C R |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     | −   | −   |
The formula matrix and stoichiometric matrix of the system are given by:
|     |     |     |     |       |      |       |     |     |        |
| --- | --- | --- | ---- | ----- | ----- | ----- | --- | --- | ------ |
|     |     |     | 1    | 0 0 1 | 1 0   |       |     |     |        |
|     |     |     |      |       |       |      |     | T  |        |
|     |     |     |     |       |      |       |     |     |        |
|     |     |     | 2   | 0 1 1 | 0 0  | 1 1 1 | 1   | 0 0 |        |
|     |     | A   | =   |       |  N = |       |     |     | (4.14) |
|     |     |     |      |       |       | − −  |     |    |        |
|     |     |     |  0 | 1 1 0 | 0 0  | 0 1 1 | 1   | 1 0 |        |

|     |     |     |    |       |    | −   | −   |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     | 0   | 0 0 0 | 0 1 |     |     |     |     |
Vapor phase is ideal gas and liquid phase is ideal solution (Ung and Doherty, 1995e).
Chemical equilibrium constants and vapor pressures were taken from Saito et al. (1971).
The authors determined experimentally mole fractions in the main alkylation columun of
m-xylene at 44 mmHg, and in a second recovery column of m-xylene and alkylating reagent
at 86 mmHg. We compared bubble point calculations with the experimental data at the
first plate/condenser stage of the columns in Saito et al. (1971). Results are presented
in Tables 4.2 and 4.3. Benzene concentrations deviate the most at both pressures, while
overall deviations are larger at the higher pressure. At the lower pressure there is higher
| overestimation |     |     | of the | bubble point. |     |     |     |     |     |
| -------------- | --- | --- | ------ | ------------- | --- | --- | --- | --- | --- |
Table 4.2: Equilibrium mole fractions in xylene separation at 44 mmHg (bubble point).
Component Feed Our work: 336.54 K Saito et al. (1971): 331.15 K
|     |                      |          |     |      | Vapor Liquid |      |     | Vapor |     |
| --- | -------------------- | -------- | --- | ---- | ------------ | ---- | --- | ----- | --- |
|     | di-tert-butylbenzene |          |     | 0.29 | 0.01         | 0.29 |     | 0.02  |     |
|     |                      | m-xylene |     | 0.08 | 0.10         | 0.08 |     | 0.14  |     |
|     | tert-butyl-m-xylene  |          |     | 0.07 | 0.01         | 0.07 |     | 0.01  |     |
|     | tert-butylbenzene    |          |     | 0.19 | 0.08         | 0.19 |     | 0.11  |     |
|     |                      | benzene  |     | 0.03 | 0.34         | 0.03 |     | 0.22  |     |
|     |                      | p-xylene |     | 0.34 | 0.47         | 0.34 |     | 0.50  |     |
Figure 4.3 shows the temperature range of the two-phase system using the same feed
compositions as in Tables 4.2 and 4.3. Most mole fractions curves exhibit monotonic
behavior. Although xylene isomer compositions might have maxima in the two different
pressures and phases, p-xylene shows the clearest maximum at 347.52 K and 44 mmHg
| with | a vapor | phase | mole | fraction | of 0.557 (Figure | 4.3c). |     |     |     |
| ---- | ------- | ----- | ---- | -------- | ---------------- | ------ | --- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 55
|                            | 44 mmHg        |         |                         |         | 86 mmHg        |         |         |
| -------------------------- | -------------- | ------- | ----------------------- | ------- | -------------- | ------- | ------- |
| 1                          |                |         |                         | 1       |                |         |         |
| 0.8                        |                |         |                         | 0.8     |                |         |         |
| noitcarfesahP              |                |         | noitcarfesahP           |         |                |         |         |
| 0.6                        |                |         |                         | 0.6     |                |         |         |
| 0.4                        |                |         |                         | 0.4     |                |         |         |
| 0.2                        |                |         |                         | 0.2     |                |         |         |
| 0                          |                |         |                         | 0       |                |         |         |
| 330 340                    | 350 360        | 370 380 | 390                     | 320 330 | 340 350        | 360 370 | 380 390 |
|                            | Temperature    | (K)     |                         |         | Temperature(K) |         |         |
|                            | (a)            |         |                         |         | (b)            |         |         |
| 1                          |                |         |                         | 1       |                |         |         |
| noitcarfelomesahpropaV 0.8 |                |         | noitcarfelomesahpropaV  | 0.8     |                |         |         |
| 0.6                        |                |         |                         | 0.6     |                |         |         |
| 0.4                        |                |         |                         | 0.4     |                |         |         |
| 0.2                        |                |         |                         | 0.2     |                |         |         |
| 0                          |                |         |                         | 0       |                |         |         |
| 330 340                    | 350 360        | 370 380 | 390                     | 320 330 | 340 350        | 360 370 | 380 390 |
|                            | Temperature(K) |         |                         |         | Temperature(K) |         |         |
|                            | (c)            |         |                         |         | (d)            |         |         |
| 1                          |                |         |                         | 1       |                |         |         |
| noitcarfelomesahpdiuqiL    |                |         | noitcarfelomesahpdiuqiL |         |                |         |         |
| 0.8                        |                |         |                         | 0.8     |                |         |         |
| 0.6                        |                |         |                         | 0.6     |                |         |         |
| 0.4                        |                |         |                         | 0.4     |                |         |         |
| 0.2                        |                |         |                         | 0.2     |                |         |         |
| 0                          |                |         |                         | 0       |                |         |         |
| 330 340                    | 350 360        | 370 380 | 390                     | 320 330 | 340 350        | 360 370 | 380 390 |
|                            | Temperature(K) |         |                         |         | Temperature(K) |         |         |
|                            | (e)            |         |                         |         | (f)            |         |         |
Figure 4.3: Equilibrium in xylene separation at 44 mmHg and 86 mmHg: (a, b) phase
fractions [vapor ( ), liquid ( )], (c, d, e, f) mole fractions [di-tert-butylbenzene ( ),
m-xylene ( ), tert-butyl-m-xylene ( ), tert-butylbenzene ( ), benzene ( ),
|     |     |     | p-xylene ( | )]. |     |     |     |
| --- | --- | --- | ---------- | --- | --- | --- | --- |

56 Chapter 4. Application of CPE algorithms to reaction systems
Table 4.3: Equilibrium mole fractions in xylene separation at 86 mmHg (bubble point).
Component Feed Our work: 324.40 K Saito et al. (1971): 323.15 K
|     |                      |          |      | Vapor | Liquid |     | Vapor |     |
| --- | -------------------- | -------- | ---- | ----- | ------ | --- | ----- | --- |
|     | di-tert-butylbenzene |          | 0.09 | 0.00  | 0.07   |     | 0.00  |     |
|     |                      | m-xylene | 0.35 | 0.13  | 0.34   |     | 0.29  |     |
|     | tert-butyl-m-xylene  |          | 0.04 | 0.00  | 0.05   |     | 0.00  |     |
|     | tert-butylbenzene    |          | 0.21 | 0.03  | 0.24   |     | 0.05  |     |
|     |                      | benzene  | 0.25 | 0.82  | 0.24   |     | 0.59  |     |
|     |                      | p-xylene | 0.06 | 0.02  | 0.06   |     | 0.07  |     |
When the inert p-xylene is not included in the calculations, the number of elements reduces
to three. It is possible to depict phase behavior of this reaction system in a ternary
diagram, where the coordinates correspond to the element mole fractions (Eq. 3.12).
Figure 4.4 shows the VLE region at 350 K for 44 and 86 mmHg. As expected, the vapor
| phase | region | is larger | at the lower | pressure. |     |     |     |     |
| ----- | ------ | --------- | ------------ | --------- | --- | --- | --- | --- |
A ternary diagram expressed in element mole fractions might not allow us to see the actual
component distribution in the phases. Nevertheless, a ternary diagram can reveal if a
phase split will take place, based on the element mole fractions in a feed we want to test.
To determine the component mole fractions, we need to solve the CPE problem for the
corresponding element abundance vector of the specific phase. The components that do
not appear as vertices of the triangle refer to combinations of the elements and are defined,
| according |     | to the formula | matrix, | by:    |       |       |       |        |
| --------- | --- | -------------- | ------- | ------ | ----- | ----- | ----- | ------ |
|           |     | DTBB:          | 2b =    | b TBB: | b = b | TBMX: | b = b | (4.15) |
|           |     |                | 1       | 2      | 2 3   |       | 1 2   |        |
These points represent pure di-tert-butylbenzene, tert-butylbenzene and tert-butyl-m-
xylene respectively. In this ternary diagram, there is a region that corresponds to infeasible
mole fractions of the elements (non-physical mixture). Such a region exists because element
2 can be used only as part of a component – there is no component in the physical mixture
with chemical composition C H . Elements 1 and 3 can exist as pure, because their
|     |     |     | 4   | 8   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
chemical composition corresponds to benzene and m-xylene. In other words, pure element
1 or 3 is a system of pure benzene and m-xylene respectively. Concentration of elements 1
and 3 must be high enough to be combined with element 2 and deplete it completely when
“building” the components in the system. The constraint on the elements that defines the
| infeasible |     | region, according | to the | formula | matrix, is: |     |     |        |
| ---------- | --- | ----------------- | ------ | ------- | ----------- | --- | --- | ------ |
|            |     |                   |        | b       | 2b +b       |     |     | (4.16) |
|            |     |                   |        | 2       | 1 3         |     |     |        |
≥

Chapter 4. Application of CPE algorithms to reaction systems 57
0
1
0.2
0.8
0.4 B
H8 0.6 e
n
C4 z e
B n
B e
T
0.6
0.4
B
B
T
D
0.8
0.2
1
0
TBMX
0 0.2 0.4 0.6 0.8 1
m-Xylene
(a)
0
1
0.2
0.8
0.4 B
H8 0.6 e
n
C4 z e
B n
B e
T
0.6
0.4
B
B
T
D
0.8
0.2
1
0
TBMX
0 0.2 0.4 0.6 0.8 1
m-Xylene
(b)
Figure 4.4: Ternary diagrams of elements in m-xylene alkylation without p-xylene at 350
K: (a) 44 mmHg, (b) 86 mmHg [binodal curve ( ), tie lines ( ), VLE region ( ),
vapor region ( ), liquid region ( ), infeasible region ( ), DTTB
(di-tert-butylbenzene), TBB (tert-butylbenzene), TBMX (tert-butyl-m-xylene)].

58 Chapter 4. Application of CPE algorithms to reaction systems
| 4.1.3 | Esterification |     |     |     | of acetic |     | acid | with | ethanol |     |     |     |
| ----- | -------------- | --- | --- | --- | --------- | --- | ---- | ---- | ------- | --- | --- | --- |
A benchmark system for chemical and phase equilibrium algorithms is the acetic acid and
| ethanol | esterification, |     |     | producing | water  | and | ethyl      | acetate: |     |     |     |        |
| ------- | --------------- | --- | --- | --------- | ------ | --- | ---------- | -------- | --- | --- | --- | ------ |
|         |                 |     |     | C         | H O +C | H   | O (cid:10) | H O+C    | H   | O   |     | (4.17) |
|         |                 |     |     |           | 2 4 2  | 2   | 6          | 2        | 4   | 8 2 |     |        |
The number of elements is N = N N = 4 1 = 3. The formula matrix and
|                |     |        |     |      | E      | C   | R     |     |     |     |     |        |
| -------------- | --- | ------ | --- | ---- | ------ | --- | ----- | --- | --- | --- | --- | ------ |
|                |     |        |     |      |        |     | −     |     | −   |     |     |        |
| stoichiometric |     | matrix | of  | the  | system | are | given | by: |     |     |     |        |
|                |     |        |     |     |        |    |       |     |     |     |     |        |
|                |     |        |     |      | 1 0 0  | 1   |       |     |     |     |     |        |
|                |     |        |     |     |        |    |       | h   |     | iT  |     |        |
|                |     |        | A   | = 0 | 1 0    | 1  | N     | =   | 1 1 | 1 1 |     | (4.18) |
|                |     |        |     |     |        |    |       | −   | −   |     |     |        |
|                |     |        |     |      | 1 0 1  | 0   |       |     |     |     |     |        |
Vapor phase is considered ideal gas and liquid phase is described by the UNIQUAC activity
coefficient model (Abrams and Prausnitz, 1975). The chemical equilibrium constant, vapor
pressures and parameters for the UNIQUAC model were taken from Xiao et al. (1989).
Castier et al. (1989) studied this system considering the competitive conversion of ethanol
to diethylether and the acetic acid dimerization in the vapor phase. The latter was not
modeled by a reaction in Castier et al. (1989) but implicitly accounted for by the value of
the fugacity coefficient (Nothnagel et al., 1973; Hayden and O’Connell, 1975). Xiao et al.
(1989) and Stateva and Wakeham (1997) made similar calculations and the comparisons
with this work are presented in Table 4.4. Larger deviations with Stateva and Wakeham
(1997) are due to different chemical equilibrium constants. The behavior of the two-phase
system at 1 atm is also shown in Figure 4.5 for an equimolar feed of the reactants.
Table 4.4: Equilibrium mole fractions, phase amounts and phase fractions in acetic
|     |     |     | acid/ethanol |     | esterification |     |     | at 355 | K and | 1 atm. |     |     |
| --- | --- | --- | ------------ | --- | -------------- | --- | --- | ------ | ----- | ------ | --- | --- |
Component Feed Our work Stateva and Wakeham (1997) Xiao et al. (1989)
|     |               |     |     | Vapor  | Liquid |     |     | Vapor  | Liquid |     | Vapor  | Liquid |
| --- | ------------- | --- | --- | ------ | ------ | --- | --- | ------ | ------ | --- | ------ | ------ |
|     | acetic acid   |     | 0.5 | 0.0629 | 0.2360 |     |     | 0.0554 | 0.2243 |     | 0.0624 | 0.2376 |
|     | ethanol       |     | 0.5 | 0.0855 | 0.0670 |     |     | 0.1029 | 0.0675 |     | 0.0862 | 0.0686 |
|     | water         |     | 0   | 0.3970 | 0.5630 |     |     | 0.3604 | 0.5537 |     | 0.3963 | 0.5565 |
|     | ethyl acetate |     | 0   | 0.4545 | 0.1339 |     |     | 0.4813 | 0.1545 |     | 0.4551 | 0.1373 |
|     | n t (mol)     |     | 20  | 17.636 | 2.364  |     |     | –      |        | –   | –      | –      |
|     | β             |     |     | 0.882  | 0.118  |     |     | 0.767  | 0.233  |     | 0.877  | 0.123  |
The number of elements is equal to three. Figure 4.6 shows the VLE region of the system
at 355 K and 1 atm in terms of element mole fractions. The components that do not
appear as vertices of the triangle are acetic acid and ethyl acetate respectively:

Chapter 4. Application of CPE algorithms to reaction systems 59
1
0.8
noitcarfesahP
0.6
0.4
0.2
0
|     |     | 346 348 | 350 352 | 354 356 | 358 |     |     |
| --- | --- | ------- | ------- | ------- | --- | --- | --- |
Temperature(K)
(a)
| 1   |     |     |     | 1   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
noitcarfelomesahpdiuqiL
| noitcarfelomesahpropaV 0.8 |                |         |     | 0.8     |                |         |     |
| -------------------------- | -------------- | ------- | --- | ------- | -------------- | ------- | --- |
| 0.6                        |                |         |     | 0.6     |                |         |     |
| 0.4                        |                |         |     | 0.4     |                |         |     |
| 0.2                        |                |         |     | 0.2     |                |         |     |
| 0                          |                |         |     | 0       |                |         |     |
| 346 348                    | 350 352        | 354 356 | 358 | 346 348 | 350 352        | 354 356 | 358 |
|                            | Temperature(K) |         |     |         | Temperature(K) |         |     |
|                            | (b)            |         |     |         | (c)            |         |     |
Figure 4.5: Equilibrium in acetic acid/ethanol esterification for an equimolar feed of
reactants at 1 atm: (a) phase fractions [vapor ( ), liquid ( )] and (b, c) mole
fractions [acetic acid ( ), ethanol ( ), water ( ), ethyl acetate ( )].

60 Chapter 4. Application of CPE algorithms to reaction systems
|     |     |     |     | HAc: | b = | b   | EtOAc: | b   | = b | (4.19) |
| --- | --- | --- | --- | ---- | --- | --- | ------ | --- | --- | ------ |
|     |     |     |     |      | 1   | 3   |        | 1   | 2   |        |
0
1
0.2
0.8
0.4
|     |     |     | ol  |     |     |     |     |     | 0.6 C |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     | n   |     |     |     |     |     | 2H    |     |
a
h
|     |     |     | t   | c   |     |     |     |     | 2O  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | E   | A   |     |     |     |     | H   |     |
|     |     |     |     | O   |     |     |     |     | A   |     |
|     |     |     |     | E t |     |     |     |     | c   |     |
0.6
0.4
0.8
0.2
1
0
|     |     |     | 0.2 |     | 0.4 |     | 0.6 |     | 0.8 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0 1
Water
Figure 4.6: Ternary diagram of elements in acetic acid/ethanol esterification at 355 K and
1 atm [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region ( ), liquid
region ( ), infeasible region ( ), HAc (acetic acid), EtOAc (ethyl acetate)].
Element 1 represents part of a component molecule, therefore it cannot exist pure in the
| system and | there | is an | infeasible |     | region | defined | by:  |     |     |        |
| ---------- | ----- | ----- | ---------- | --- | ------ | ------- | ---- | --- | --- | ------ |
|            |       |       |            |     |        | b       | b +b |     |     | (4.20) |
|            |       |       |            |     |        | 1       | 2 3  |     |     |        |
≥
| 4.1.4 | Esterification |     |     | of  | acetic | acid | with |     | 1-butanol |     |
| ----- | -------------- | --- | --- | --- | ------ | ---- | ---- | --- | --------- | --- |
A different esterification was studied by Wasylkiewicz and Ung (2000), the LLE of acetic
| acid and | 1-butanol | reaction |     | to water | and | butyl | acetate:   |     |        |        |
| -------- | --------- | -------- | --- | -------- | --- | ----- | ---------- | --- | ------ | ------ |
|          |           |          | C   | H O      | +C  | H O   | (cid:10) H | O+C | H O    | (4.21) |
|          |           |          | 2   | 4 2      |     | 4 10  | 2          |     | 6 12 2 |        |
The number of elements is N = N N = 4 1 = 3. The formula matrix and
|                |        |     |        | E      |     | C     | R   |     |     |     |
| -------------- | ------ | --- | ------ | ------ | --- | ----- | --- | --- | --- | --- |
|                |        |     |        |        |     | −     |     | −   |     |     |
| stoichiometric | matrix |     | of the | system | are | given | by: |     |     |     |

Chapter 4. Application of CPE algorithms to reaction systems 61
|     |     |     |     |       |     |     |     |     |     |     |        |
| --- | --- | --- | --- | ------ | --- | ---- | --- | --- | --- | --- | ------ |
|     |     |     |     | 1      | 0 0 | 1    |     |     |     |     |        |
|     |     |     |     |        |     |      | h   |     |     | iT  |        |
|     |     |     | A   | =  0 | 1 0 | 1  | N = | 1   | 1 1 | 1   | (4.22) |
|     |     |     |     |       |     |     |     | −   | −   |     |        |
|     |     |     |     | 1      | 0 1 | 0    |     |     |     |     |        |
Vapor phase is considered ideal gas and liquid phases is described by the UNIQUAC
activity coefficient model (Abrams and Prausnitz, 1975). The chemical equilibrium
constant was taken from Wasylkiewicz and Ung (2000), vapor pressures and parameters
for the UNIQUAC model from Okasinski and Doherty (2000). Calculations for the LLE
of the quaternary mixture are compared with Bonilla-Petriciolet et al. (2008a) in Table
4.5. Transformed mole fractions were calculated by Eq. 4.2, taking butyl acetate as the
| reference | component: |     |     |     |     |     |     |        |     |     |        |
| --------- | ---------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | ------ |
|           |            |     |     | X   | = x | +x  | X   | = x +x |     |     | (4.23) |
|           |            |     |     |     | 1 1 | 4   | 2   | 2      | 4   |     |        |
The first liquid phase is the organic liquid phase and calculation of the aqueous (water-rich)
|     |     |     |     |     |     | X0  | X0  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
liquid phase transformed mole fractions and is similar. Bonilla-Petriciolet et al.
|         |      |         |        |        |             |     | 1         | 2   |     |     |     |
| ------- | ---- | ------- | ------ | ------ | ----------- | --- | --------- | --- | --- | --- | --- |
| (2008a) | also | defined | slopes | of the | transformed |     | tie lines | as: |     |     |     |
X X0
j
|     |     |     |     |     | R   | =   | −   | j   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j
|     |     |     |     |     |     |     | X X0 |     |     |     | (4.24) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ |
|     |     |     |     |     |     |     | 1    | 1   |     |     |        |
−
|     |     |     |     |     |     | j = 2,...,N |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
E
Table 4.5: Transformed tie line slopes R in acetic acid/1-butanol esterification at 298.15
2
|     |        |       |          |           |         | K and | 1 atm.              |     |         |                |     |
| --- | ------ | ----- | -------- | --------- | ------- | ----- | ------------------- | --- | ------- | -------------- | --- |
|     |        | Feed  | vector   |           | Our     | work  | Bonilla-Petriciolet |     |         | et al. (2008a) |     |
|     |        | [0.01 | 0.4 0.59 | 0]T       | 46.1875 |       |                     |     | 46.0948 |                |     |
|     |        | [0.1  | 0.2 0.7  | 0]T       | 2.6801  |       |                     |     | 2.6796  |                |     |
|     |        | [0.15 | 0.5 0.35 | 0]T       | 3.7591  |       |                     |     | 3.7574  |                |     |
|     |        | [0.2  | 0.3 0.5  | 0]T       | 1.8917  |       |                     |     | 1.8920  |                |     |
|     |        | [0.3  | 0.3 0.4  | 0]T       | 1.3425  |       |                     |     | 1.3410  |                |     |
|     |        | [0.3  | 0.4 0.3  | 0]T       | 1.6227  |       |                     |     | 1.6227  |                |     |
|     | [0.397 | 0.294 |          | 0.309 0]T | 1.0689  |       |                     |     | 1.0649  |                |     |
|     | [0.394 | 0.274 |          | 0.332 0]T | 1.0368  |       |                     |     | 1.0323  |                |     |
0]T
|     |     | [0.3 0.15 | 0.55     |     | 0.9759 |     |     |     | 0.9692 |     |     |
| --- | --- | --------- | -------- | --- | ------ | --- | --- | --- | ------ | --- | --- |
|     |     | [0.27     | 0.1 0.63 | 0]T | 0.9257 |     |     |     | 0.9176 |     |     |
Moreover, calculations for the VLE of the system were made at 1 atm for an equimolar
amount of reactants. The phase and mole fractions are presented in Figure 4.7.

62 Chapter 4. Application of CPE algorithms to reaction systems
1
0.8
noitcarfesahP
0.6
0.4
0.2
0
|     |     | 368 370 | 372 374 | 376 378 | 380 |     |     |
| --- | --- | ------- | ------- | ------- | --- | --- | --- |
Temperature(K)
(a)
| 1   |     |     |     | 1   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
noitcarfelomesahpdiuqiL
| noitcarfelomesahpropaV 0.8 |                |         |     | 0.8     |                |         |     |
| -------------------------- | -------------- | ------- | --- | ------- | -------------- | ------- | --- |
| 0.6                        |                |         |     | 0.6     |                |         |     |
| 0.4                        |                |         |     | 0.4     |                |         |     |
| 0.2                        |                |         |     | 0.2     |                |         |     |
| 0                          |                |         |     | 0       |                |         |     |
| 368 370                    | 372 374        | 376 378 | 380 | 368 370 | 372 374        | 376 378 | 380 |
|                            | Temperature(K) |         |     |         | Temperature(K) |         |     |
|                            | (b)            |         |     |         | (c)            |         |     |
Figure 4.7: Equilibrium in acetic acid/1-butanol esterification for an equimolar feed of
reactants at 1 atm: (a) phase fractions [vapor ( ), liquid ( )], (b, c) mole fractions
[acetic acid ( ), 1-butanol ( ), water ( ), butyl acetate ( )].

Chapter 4. Application of CPE algorithms to reaction systems 63
The number of elements is equal to three. Figure 4.8 shows the LLE region of the system
at 298.15 K and 1 atm in terms of element mole fractions. The components that do not
appear as vertices of the triangle are acetic acid and butyl acetate respectively:
|     |     |     | HAc: b | = b | BuOAc: | b = b |     | (4.25) |
| --- | --- | --- | ------ | --- | ------ | ----- | --- | ------ |
|     |     |     | 1      | 3   |        | 1 2   |     |        |
0
1
0.2
0.8
ol
|     |     |     | 0.4 |     |     | C   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | n   |     |     |     | 0.6 |     |     |
|     |     | a   |     |     |     | 2H  |     |     |
u t
|     |     | B   | c   |     |     | 2O  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | A   |     |     | H   |     |     |
|     |     | 1 - | O   |     |     | A   |     |     |
|     |     |     | u   |     |     | c   |     |     |
B
0.6
0.4
0.8
0.2
1
0
|     | 0   | 0.2 |     | 0.4 | 0.6 | 0.8 | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Water
Figure 4.8: Ternary diagram of elements in acetic acid/1-butanol esterification at 298.15
K and 1 atm [binodal curve ( ), tie lines ( ), LLE region ( ), liquid region ( ),
infeasible region ( ), HAc (acetic acid), BuOAc (butyl acetate)].
Element 1 represents part of a component molecule, therefore it cannot exist pure in the
| system and | there is | an infeasible | region | defined | by:  |     |     |        |
| ---------- | -------- | ------------- | ------ | ------- | ---- | --- | --- | ------ |
|            |          |               |        | b       | b +b |     |     | (4.26) |
|            |          |               |        | 1       | 2 3  |     |     |        |
≥
| 4.1.5 | MTBE | synthesis |     |     |     |     |     |     |
| ----- | ---- | --------- | --- | --- | --- | --- | --- | --- |
Methyl-tert-butylether(MTBE)issynthesizedfromamixtureofisobuteneandmethanol:
|     |     |     | C H | +CH | O (cid:10) C | H O  |     | (4.27) |
| --- | --- | --- | --- | --- | ------------ | ---- | --- | ------ |
|     |     |     | 4   | 8 4 |              | 5 12 |     |        |
Ung and Doherty (1995e) examined the VLE of the mixture in the presence of n-butane
as inert. The number of elements is N = N N = 4 1 = 3. The formula matrix and
|     |     |     |     | E   | C R |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | −   | −   |     |     |

64 Chapter 4. Application of CPE algorithms to reaction systems
| stoichiometric | matrix | of  | the system | are given | by: |     |     |     |        |
| -------------- | ------ | --- | ---------- | --------- | --- | --- | --- | --- | ------ |
|                |        |     |           |          |     |     |     |     |        |
|                |        |     | 1 0        | 0 1       |     |     |     |     |        |
|                |        |     |           |          |     | h   |     | iT  |        |
|                |        | A = | 0 1       | 0 1      | N   | = 1 | 1 0 | 1   | (4.28) |
|                |        |     |           |          |     | −   | −   |     |        |
|                |        |     | 0 0        | 1 0       |     |     |     |     |        |
Vapor phase is considered ideal gas and liquid phase is described by the Wilson activity
coefficient model (Wilson, 1964). The chemical equilibrium constant, vapor pressurs and
parameters for the Wilson model were taken from Ung and Doherty (1995e). Calculations
without n-butane are shown in Figure 4.9. The equilibrium diagram of MTBE at 1 atm is
presented in Figure 4.9a. Due to the reaction in Eq. 4.27, pure MTBE cannot be achieved
in any of the phases. Maximum mole fraction in the vapor phase is 0.70 at 320.56 K and in
the liquid phase 0.93 at 317.70 K. Figures 4.9b and 4.9c show transformed mole fractions
at equilibrium using MTBE as a reference component, calculated by:
|     |     |     |     | x +x |     | x   | +x  |     |        |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
|     |     |     | X = | 1    | 4 X | =   | 2 4 |     | (4.29) |
|     |     |     | 1   |      |     | 2   |     |     |        |
|     |     |     |     | 1+x  |     | 1+x |     |     |        |
|     |     |     |     | 4    |     |     | 4   |     |        |
According to Ung and Doherty (1995e), an “intermediate-boiling inflection azeotrope” or
a “pseudo-reactive azeotrope” is identified. This charecterization comes from the fact that
the plot Y = f(X ) approaches the diagonal Y = X (Eq. 4.5). We observed this point
| 1            |     | 1   |     |     |     | 1 1 |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| at 320.92 K. |     |     |     |     |     |     |     |     |     |
Different mole numbers of n-butane were included in the feed to study the effect of the
inert at 300 K and 1 atm. Isobutene and methanol were kept constant in the feed at 1 mol
each. Figure 4.10 illustrates the phase fractions and the mole fractions of the components
in each phase. An overall mole fraction is included in Figures 4.10b to 4.10e, calculated
as:
NP
X
|     |     |     |     | x¯ = | β   | x    |     |     |     |
| --- | --- | --- | --- | ---- | --- | ---- | --- | --- | --- |
|     |     |     |     | i    |     | k ik |     |     |     |
(4.30)
k=1
i = 1,...,N
C
The overall mole fraction represents the average concentration of a component in the
N -phase mixture. Vapor pressure for n-butane was taken from NIST Chemistry WebBook
P
(2016) and parameters for the Wilson model from Ung and Doherty (1995e). Results are
shown in Figure 4.10. The inert is a volatile component, therefore a vapor phase is expected
to appear as its concentration in the feed increases (approximately after adding 0.36 mol
of n-butane). After n-butane is abundant enough, we obtain 100% vapor. Increasing the
concentration of the inert causes the reaction (Eq. 4.27) to shift to the left, decreasing
the yield according to Le Chatelier’s principle. This leads to the increase of isobutene

Chapter 4. Application of CPE algorithms to reaction systems 65
340
320
)K(
erutarepmeT
300
280
260
|     |     | 0 0.2 | 0.4 0.6 | 0.8 1 |     |
| --- | --- | ----- | ------- | ----- | --- |
MTBEmole fraction
(a)
1
340
0.8
320
)K(
| erutarepmeT |     |     | 0.6 |     |     |
| ----------- | --- | --- | --- | --- | --- |
| 300         |     |     | Y   |     |     |
0.4
280
0.2
| 260   |     |         | 0   |             |       |
| ----- | --- | ------- | --- | ----------- | ----- |
| 0 0.2 | 0.4 | 0.6 0.8 | 1 0 | 0.2 0.4 0.6 | 0.8 1 |
Y 1 , X 1 X
(b) (c)
Figure 4.9: Equilibrium in MTBE synthesis at 1 atm: (a) T-y-x diagram for MTBE, (b)
T-Y-X diagram for isobutene [vapor ( ), liquid ( )], (c) Y-X diagram for isobutene
|     | and methanol | [isobutene | ( ), methanol | ( )]. |     |
| --- | ------------ | ---------- | ------------- | ----- | --- |

66 Chapter 4. Application of CPE algorithms to reaction systems
and methanol mole numbers. However, the addition of the inert dilutes the remaining
components of the mixture. As a result, the single-phase mole fractions of all components
except for the inert decrease, with MTBE exhibiting the faster decrease. In Figures 4.10b,
4.10c and 4.10e it is evident that in the two-phase region the shift due to backward reaction
is more prominent than the dilution of the reactants, with their overall mole fractions
slightly increasing. In any case, the overall mole fraction of MTBE is expected to decreases
continuously.
The number of elements is equal to three. Figure 4.11 shows the VLE region of the system
at 1 atm for at 280 and 320 K and in terms of element mole fractions. At the higher
temperature, the single liquid region shrinks appreciably compared to the one at the
lower temperature. The component that does not appear as a vertice of the triangle is
MTBE:
|     |     |     |     | MTBE: |     | b = b |     |     |     | (4.31) |
| --- | --- | --- | --- | ----- | --- | ----- | --- | --- | --- | ------ |
1 2
All the elements can exist as pure, therefore there are no infeasible regions.
| 4.1.6 TAME |     | synthesis |     |     |     |     |     |     |     |     |
| ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Bonilla-Petriciolet et al. (2008a) modeled the synthesis of tert-amyl methyl ether (TAME)
from a mixture of 2-methyl-1-butene, 2-methyl-2-butene and methanol:
|     |     | 2-CH -1-C | H +2-CH |     | -2-C | H +2CH | O (cid:10) | 2C H | O   | (4.32) |
| --- | --- | --------- | ------- | --- | ---- | ------ | ---------- | ---- | --- | ------ |
|     |     | 3         | 4 7     | 3   | 4    | 7      | 4          | 6    | 14  |        |
in the presence of inert n-pentane. The number of elements is N = N N = 5 1 = 4.
|     |     |     |     |     |     |     |     | E   | C R |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     | −   | −   |
The formula matrix and stoichiometric matrix of the system are given by:
|     |     |     |     |     |     |     |     |     |     |        |
| --- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- | ------ |
|     |     | 2    | 0 0 | 1 0  |     |     |     |     |     |        |
|     |     |     |     |     |     |     |     |     |     |        |
|     |     | 0   | 2 0 | 1 0 |     | h   |     |     | iT  |        |
|     |     |     |     |     |     |     |     |     |     |        |
|     |     | A =  |     |      | N   | = 1 | 1   | 2 2 | 0   | (4.33) |
|     |     |  0 | 0 1 | 1 0 |     | −   | − − |     |     |        |

|     |     |    |     |    |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 0   | 0 0 | 0 1 |     |     |     |     |     |     |
Vapor phase is considered ideal and liquid phase is described by the Wilson activity
coefficient model (Wilson, 1964). The chemical equilibrium constant was taken from
Bonilla-Petriciolet et al. (2008a), vapor pressures and parameters for the Wilson model
were taken from Chen et al. (2002). Transformed compositions using TAME as the
| reference component |     | are | found by: |     |     |       |     |     |     |        |
| ------------------- | --- | --- | --------- | --- | --- | ----- | --- | --- | --- | ------ |
|                     |     | x   | +0.5x     |     | x   | +0.5x |     | x   | +x  |        |
|                     | X   | = 1 | 4         | X   | = 2 |       | 4 X | = 3 | 4   | (4.34) |
|                     |     | 1   |           | 2   |     |       | 3   |     |     |        |
|                     |     | 1+x |           |     |     | 1+x   |     | 1+x |     |        |
|                     |     |     | 4         |     |     | 4     |     |     | 4   |        |

Chapter 4. Application of CPE algorithms to reaction systems 67
1
0.8
noitcarf
0.6
esahP
0.4
0.2
0
|     |     | 0 0.5 | 1 1.5         | 2 2.5 | 3   |     |     |
| --- | --- | ----- | ------------- | ----- | --- | --- | --- |
|     |     |       | Feed n-butane | (mol) |     |     |     |
(a)
| 0.10                  |                   |       |                      | 0.10  |                   |       |     |
| --------------------- | ----------------- | ----- | -------------------- | ----- | ----------------- | ----- | --- |
| 0.08                  |                   |       |                      | 0.08  |                   |       |     |
| noitcarfelomenetubosI |                   |       | noitcarfelomlonahteM |       |                   |       |     |
| 0.06                  |                   |       |                      | 0.06  |                   |       |     |
| 0.04                  |                   |       |                      | 0.04  |                   |       |     |
| 0.02                  |                   |       |                      | 0.02  |                   |       |     |
| 0                     |                   |       |                      | 0     |                   |       |     |
| 0 0.5                 | 1 1.5             | 2 2.5 | 3                    | 0 0.5 | 1 1.5             | 2 2.5 | 3   |
|                       | Feedn-butane(mol) |       |                      |       | Feedn-butane(mol) |       |     |
|                       | (b)               |       |                      |       | (c)               |       |     |
| 1                     |                   |       |                      | 1     |                   |       |     |
| 0.8                   |                   |       |                      | 0.8   |                   |       |     |
noitcarf
noitcarf
| 0.6 |     |     |     | 0.6 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
elom
elom
| enatuB-n 0.4 |     |     |     | 0.4 |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- |
EBTM
| 0.2   |               |       |     | 0.2   |               |       |     |
| ----- | ------------- | ----- | --- | ----- | ------------- | ----- | --- |
| 0     |               |       |     | 0     |               |       |     |
| 0 0.5 | 1 1.5         | 2 2.5 | 3   | 0 0.5 | 1 1.5         | 2 2.5 | 3   |
|       | Feed n-butane | (mol) |     |       | Feed n-butane | (mol) |     |
|       | (d)           |       |     |       | (e)           |       |     |
Figure 4.10: Effect of inert feed mole numbers in MTBE synthesis at 300 K and 1 atm:
(a) phase fractions and mole fractions of (b) isobutene, (c) methanol, (d) n-butane, (e)
|     | MTBE | [vapor ( | ), liquid | ( ), overall | ( )]. |     |     |
| --- | ---- | -------- | --------- | ------------ | ----- | --- | --- |

68 Chapter 4. Application of CPE algorithms to reaction systems
0
1
0.2
0.8
| ol    |     |     | I     |     |
| ----- | --- | --- | ----- | --- |
| n 0.4 |     |     | s o   |     |
| a     |     |     | 0.6 b |     |
| h     |     |     | u     |     |
| t     |     |     | t     |     |
| e E   |     |     | e     |     |
| M B   |     |     | n     |     |
T e
M
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Butane
(a)
0
1
0.2
0.8
| ol    |     |     | I   |     |
| ----- | --- | --- | --- | --- |
| n 0.4 |     |     | s o |     |
0.6 b
| h a |     |     | u   |     |
| --- | --- | --- | --- | --- |
| t   |     |     | t   |     |
| e E |     |     | e   |     |
| M B |     |     | n   |     |
T e
M
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Butane
(b)
Figure 4.11: Ternary diagrams of elements in MTBE synthesis at 1 atm: (a) 280 K, (b)
320 K [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region ( ), liquid
|     | region | ( )]. |     |     |
| --- | ------ | ----- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 69
| Transformed | tie lines | slopes | are | calculated | by: |     |     |     |     |     |
| ----------- | --------- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
|             |           |        |     |            | Y   | X   |     |     |     |     |
j j
|     |     |     |     | R   | =   | −   |     |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     | j   | Y   | X   |     |     |     |        |
|     |     |     |     |     | 1   | 1   |     |     |     | (4.35) |
−
j = 2,...,N
E
VLE results are compared with Bonilla-Petriciolet et al. (2008a) in Table 4.6. Chen et al.
(2002) studied the kinetics in reactive distillation of TAME. In their analysis, two reactions
| take place | in the column: |     |      |        |     |            |     |     |     |        |
| ---------- | -------------- | --- | ---- | ------ | --- | ---------- | --- | --- | --- | ------ |
|            |                |     | 2-CH | -1-C H | +CH | O (cid:10) | C   | H O |     | (4.36) |
|            |                |     |      | 3 4    | 7   | 4          | 6   | 14  |     |        |
|            |                |     | 2-CH | -2-C H | +CH | O (cid:10) | C   | H O |     | (4.37) |
|            |                |     |      | 3 4    | 7   | 4          | 6   | 14  |     |        |
With the new reaction set, the number of elements is now N = N N = 5 2 = 3.
|     |     |     |     |     |     |     |     | E   | C R |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     | −   | −   |
The formula matrix and stoichiometric matrix of the new system are given by:
|     |     |     |     |     |     |      |     |     |     |        |
| --- | --- | ---- | --- | ---- | --- | ---- | --- | --- | --- | ------ |
|     |     | 1    | 1 0 | 1 0  |     |     |     |     | T  |        |
|     |     |      |     |      |     |      | 1 0 | 1 1 | 0   |        |
|     |     |     |     |     |     |      |     |     |     |        |
|     | A   | = 0 | 0 1 | 1 0 | N   | = − |     | −   |     | (4.38) |

|     |     |    |     |    |     | 0   |     | 1 1 1 | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     | 0   | 0 0 | 0 1 |     |     | −   | −     |     |     |
|     |     |     |     |     |     |     |     |       | Keq | Keq |
The chemical equilibrium constants of reactions in Eq. 4.36 and 4.37 are and
1 2
respectively. Bonilla-Petricioletetal.(2008a)combinedthesereactionsintoasinglereaction
given by Eq. 4.32. The chemical equilibrium constant of the resulting reaction must be
|     |     |     |     |     |     |     |     |     | Keq | KeqKeq. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
the product of the chemical equilibrium constants of the two reactions =
|     |     |     |     |     |     |     |     |     | comb | 1 2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
Instead, Bonilla-Petriciolet et al. (2008a) disregarded the second chemical equilibrium
constant and reported Keq = Keq. In this work we calculated the correct chemical
|     |     |     | comb | 1   |     |     |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
equilibrium constant of the combined reaction and compared one- and two-reaction mixture
VLE. A stoichiometric ratio of reactants and methanol/n-pentane ratio 2:1 was selected at
1.52 bar (Figure 4.12). According to Eq. 4.32, 2-methyl-1-butene and 2-methyl-2-butene
are equivalent as reactants. In the single-phase regions, their concentrations are expected
to be equal. Because they are isomers, their physical properties differ slightly and in the
two-phase region their concentrations are not supposed to be very different (Figures 4.12b,
4.12d and 4.12f). Conversely, if we follow the two-reaction modeling of the system and
| subtract Eq. | 4.37 from | 4.36, | we   | obtain: |            |      |      |     |     |        |
| ------------ | --------- | ----- | ---- | ------- | ---------- | ---- | ---- | --- | --- | ------ |
|              |           |       | 2-CH | -1-C    | H (cid:10) | 2-CH | -2-C | H   |     | (4.39) |
|              |           |       |      | 3 4     | 7          |      | 3    | 4 7 |     |        |
Calculations are the same if Eq. 4.39 would replaced one of Eq. 4.36 or 4.37. Eq. 4.39
shows that one of the two isomer forms is more dominant and mole fractions are expected

70 Chapter 4. Application of CPE algorithms to reaction systems
to be different (Figures 4.12a, 4.12c and 4.12e). Finally, the chemical equilibrium constant
of the combined reaction is larger, and we can expect higher concentrations of the heavier
product (TAME) which will result in a heavier system, and therefore the vapor phase will
| appear |     | at higher | temperatures |     | than | the | two-reaction | system. |     |     |     |     |
| ------ | --- | --------- | ------------ | --- | ---- | --- | ------------ | ------- | --- | --- | --- | --- |
Table 4.6: Transformed tie line slopes R and R in TAME synthesis for the
|     |       |      |          |                 |         |        | 2      | 3                   |         |      |                |     |
| --- | ----- | ---- | -------- | --------------- | ------- | ------ | ------ | ------------------- | ------- | ---- | -------------- | --- |
|     |       |      |          | single-reaction |         | system | at 335 | K and               | 1.52    | bar. |                |     |
|     |       | Feed | vector   |                 |         | Our    | work   | Bonilla-Petriciolet |         |      | et al. (2008a) |     |
|     |       |      |          |                 |         | R      | R      |                     |         | R    | R              |     |
|     |       |      |          |                 |         | 2      | 3      |                     |         | 2    | 3              |     |
|     | [0.3  | 0.15 | 0.55     | 0 0]T           | -0.2083 |        | –      |                     | -0.2072 |      | –              |     |
|     | [0.32 |      | 0.2 0.48 | 0 0]T           | -0.2813 |        | –      |                     | -0.2800 |      | –              |     |
0]T
|     | [0.354 | 0.183 | 0.463 | 0     | -0.2869 |        | –   |     | -0.2856 |        | –   |     |
| --- | ------ | ----- | ----- | ----- | ------- | ------ | --- | --- | ------- | ------ | --- | --- |
|     | [0.2   | 0.07  | 0.73  | 0 0]T | -0.0079 |        | –   |     | -0.0076 |        | –   |     |
|     | [0.15  | 0.02  | 0.83  | 0 0]T |         | 0.0063 | –   |     |         | 0.0064 | –   |     |
0]T
|     | [0.27  |      | 0.3 0.43  | 0        |           | 0.8050 | –        |     |           | 0.8089 | –        |     |
| --- | ------ | ---- | --------- | -------- | --------- | ------ | -------- | --- | --------- | ------ | -------- | --- |
|     | [0.2   | 0.35 | 0.45      | 0 0]T    | -3.6530   |        | –        |     | -3.6767   |        | –        |     |
|     | [0.1   | 0.35 | 0.55      | 0 0]T    | -8.4680   |        | –        |     | -8.5301   |        | –        |     |
|     | [0.05  |      | 0.3 0.65  | 0 0]T    | -157.8824 |        | –        |     | -162.6184 |        | –        |     |
|     | [0.025 |      | 0.3 0.675 | 0 0]T    | 334.3359  |        | –        |     | 327.5080  |        | –        |     |
|     | [0.15  | 0.02 | 0.8       | 0 0.03]T |           | 0.0098 | -1.2428  |     |           | 0.0099 | -1.2428  |     |
|     | [0.1   | 0.1  | 0.6       | 0 0.2]T  |           | 0.9404 | -5.8388  |     |           | 0.9406 | -5.8340  |     |
|     | [0.05  | 0.05 | 0.85      | 0 0.05]T |           | 0.8065 | -6.2504  |     |           | 0.8069 | -6.2438  |     |
|     | [0.1   | 0.15 | 0.7       | 0 0.05]T |           | 6.0678 | -13.5463 |     |           | 6.0243 | -13.4445 |     |
|     | [0.15  | 0.15 | 0.6       | 0 0.1]T  |           | 0.8456 | -4.0466  |     |           | 0.8465 | -4.0396  |     |
|     | [0.07  | 0.17 | 0.64      | 0 0.12]T |           | 7.9465 | -18.0942 |     |           | 7.9130 | -18.0152 |     |
The number of elements in the two-reaction mixture is equal to three. Figure 4.13 shows
the VLE region of the system at 335 K and 1.52 bar in terms of element mole fractions.
The component that does not appear as a vertice of the triangle is TAME:
|     |     |     |     |     |     | TAME: | b = | b   |     |     |     | (4.40) |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     |       | 1   | 2   |     |     |     |        |
All the elements can exist as pure, therefore there are no infeasible regions.
| 4.1.7 |     | Propene |     | hydration |     |     |     |     |     |     |     |     |
| ----- | --- | ------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Castier et al. (1989), and Stateva and Wakeham (1997) examined the synthesis of 2-
| propanol |     | by  | propene | hydration: |     |        |              |     |     |     |     |        |
| -------- | --- | --- | ------- | ---------- | --- | ------ | ------------ | --- | --- | --- | --- | ------ |
|          |     |     |         |            |     | C H +H | O (cid:10) C | H O |     |     |     | (4.41) |
|          |     |     |         |            |     | 3 6    | 2            | 3 8 |     |     |     |        |

Chapter 4. Application of CPE algorithms to reaction systems 71
N = 2 N = 1
R R
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
noitcarfesahP
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
(a)
noitcarfesahP
(b)
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
noitcarfelomesahpropaV
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
(c)
noitcarfelomesahpropaV
(d)
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
noitcarfelomesahpdiuqiL
1
0.8
0.6
0.4
0.2
0
328 329 330 331 332 333 334 335 336
Temperature(K)
(e)
noitcarfelomesahpdiuqiL
(f)
Figure 4.12: Equilibrium in the two- and one-reaction TAME synthesis for a
stoichiometric ratio of reactants and methanol/n-pentane ratio equal to 2:1 at 1.52 bar:
(a) phase fractions [vapor ( ), liquid ( )], (b, c) mole fractions [2-methyl-1-butene
( ), 2-methyl-2-butene ( ), methanol ( ), TAME ( ), n-pentane ( )].

72 Chapter 4. Application of CPE algorithms to reaction systems
0
1
0.2
0.8
ol
0.4
|     |     | n   |     |     | 0.6 C |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     | a   |     |     | 5H    |     |     |
h
|     |     | t   |     |     | 1   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     | M   | e E |     |     | 0   |     |     |
M
A
T
0.6
0.4
0.8
0.2
1
0
|     | 0   | 0.2 | 0.4 | 0.6 | 0.8 | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
n-Pentane
Figure 4.13: Ternary diagram of elements in the two-reaction TAME synthesis at 335 K
and 1.52 bar [binodal curve ( ), tie lines ( ), VLE region ( ), vapor region ( ),
|     |     |     | liquid | region ( )]. |     |     |     |
| --- | --- | --- | ------ | ------------ | --- | --- | --- |
in the presence of n-nonane as inert. The resulting equilibrium could lead to vapor-liquid
and vapor-liquid-liquid mixtures, depending on the concentration of n-nonane in the feed.
Bonilla-Petriciolet et al. (2008a) tested the same system without the inert and this is the
approach we followed as well. The number of elements is N = N N = 3 1 = 2.
|     |     |     |     |     | E   | C R |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | −   | −   |
The formula matrix and stoichiometric matrix of the system are given by:
|     |     |    |    |       |     |     |        |
| --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     | 1   | 0 1 | h     | iT  |     |        |
|     |     | A = |     | N = 1 | 1 1 |     | (4.42) |
|     |     |    |    |       |     |     |        |
|     |     | 0   | 1 1 | −     | −   |     |        |
Vapor and liquid phases are described by the Soave-Redlich-Kwong equation of state
(Soave, 1972) with all the binary interaction parameters k set to zero (Bonilla-Petriciolet
ij
et al., 2008a). The chemical equilibrium constant was taken from Bonilla-Petriciolet
et al. (2008a), and was considered temperature independent. Calculations are compared
with Bonilla-Petriciolet et al. (2008a) in Table 4.7, using transformed compositions with
| 2-propanol | as a reference | component: |     |      |     |     |     |
| ---------- | -------------- | ---------- | --- | ---- | --- | --- | --- |
|            |                |            |     | x +x |     |     |     |
1 3
|     |     |     | X   | =   |     |     | (4.43) |
| --- | --- | --- | --- | --- | --- | --- | ------ |
1
1+x
3
If the chemical equilibrium constant is not temperature independent, we need to use

Chapter 4. Application of CPE algorithms to reaction systems 73
Table 4.7: Transformed compositions Y and X in propene hydration at 353.15 K.
1 1
|     | Pressure | (bar)  | Our work | Bonilla-Petriciolet | et al. (2008a) |     |
| --- | -------- | ------ | -------- | ------------------- | -------------- | --- |
|     |          |        | Y X      | Y                   | X              |     |
|     |          |        | 1 1      | 1                   | 1              |     |
|     | 1        | 0.3817 | 0.0002   | 0.3745              | 0.0002         |     |
|     | 10       | 0.9158 | 0.5673   | 0.9149              | 0.5663         |     |
|     | 30       | 0.9802 | 0.8648   | 0.9800              | 0.8649         |     |
equations Eq. 2.35 and 2.36 to determine its change with temperature. As a first
approximation, we can assume that the non-zero enthalpy of reaction is temperature
independent. Integrating Eq. 2.35 from a reference temperature T to T:
0
|     |     |          |           | H◦ (cid:18) | 1(cid:19) |        |
| --- | --- | -------- | --------- | ----------- | --------- | ------ |
|     |     |          |           | ∆ 1         |           |        |
|     |     | lnKeq(T) | = lnKeq(T | )+ r        |           | (4.44) |
0
|     |     |     |     | R T − | T   |     |
| --- | --- | --- | --- | ----- | --- | --- |
0
To calculate the enthalpy of reaction from Eq. 2.38, enthalpies of formation were taken
from NIST Chemistry WebBook (2017). The reference temperature was selected as the
temperature Bonilla-Petriciolet et al. (2008a) performed their calculations and the value
lnKeq(T
of ) is known (T = 353.15 K). In Figure 4.14 the VLE of an equimolar feed
|     | 0   | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
of reactants at 1 bar is presented using a temperature independent and temperature
dependent chemical equilibrium constant. The reaction is exothermic (∆ H◦ < 0), which
r
results in an increase of the chemical equilibrium constant when the temperature decreases.
The two-phase system exists in temperatures lower than T . Therefore, when the chemical
0
equilibrium constant is temperature independent (Figures 4.14a, 4.14c and 4.14e), its
value is lower than the temperature dependent chemical equilibrium constant (Figures
4.14b, 4.14d and 4.14f). When the effect of temperature is taken into account, the reaction
progresses further and there is more product in the system. The product is 2-propanol and
Keq
it is heavier than propene. It is expected that the higher allows the liquid phase to
exist at higher temperatures (or the vapor phase to start appearing at higher temperatures).
However, results do not seem to be very different in Figure 4.14. In the case reactions are
H◦
nearly athermic (∆ 0), they have a very weak dependence on temperature and the
|     |     | r ≈ |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
assumption of a temperature independent chemical equilibrium constant is reasonable. Of
course, when such dependency is more prominent, we need to account for it through the
| use of enthalpies | of          | reaction for | more reliable | calculations. |     |     |
| ----------------- | ----------- | ------------ | ------------- | ------------- | --- | --- |
| 4.1.8             | Cyclohexane | synthesis    |               |               |     |     |
George et al. (1976) examined the synthesis of cyclohexane by benzene hydrogenation at
high temperature:
|     |     |     | C H +3H | (cid:10) C H |     | (4.45) |
| --- | --- | --- | ------- | ------------ | --- | ------ |
|     |     |     | 6 6     | 2 6 12       |     |        |

74 Chapter 4. Application of CPE algorithms to reaction systems
|     | Keq = f(T) |     |     |     | Keq = f(T) |     |     |
| --- | ---------- | --- | --- | --- | ---------- | --- | --- |
6
| 1                       |                |         |                         | 1       |                |         |     |
| ----------------------- | -------------- | ------- | ----------------------- | ------- | -------------- | ------- | --- |
| 0.8                     |                |         |                         | 0.8     |                |         |     |
| noitcarfesahP           |                |         | noitcarfesahP           |         |                |         |     |
| 0.6                     |                |         |                         | 0.6     |                |         |     |
| 0.4                     |                |         |                         | 0.4     |                |         |     |
| 0.2                     |                |         |                         | 0.2     |                |         |     |
| 0                       |                |         |                         | 0       |                |         |     |
| 330 333                 | 336 339        | 342 345 | 348                     | 330 333 | 336 339        | 342 345 | 348 |
|                         | Temperature(K) |         |                         |         | Temperature(K) |         |     |
|                         | (a)            |         |                         |         | (b)            |         |     |
| 1                       |                |         |                         | 1       |                |         |     |
| noitcarfelomesahpropaV  |                |         | noitcarfelomesahpropaV  |         |                |         |     |
| 0.8                     |                |         |                         | 0.8     |                |         |     |
| 0.6                     |                |         |                         | 0.6     |                |         |     |
| 0.4                     |                |         |                         | 0.4     |                |         |     |
| 0.2                     |                |         |                         | 0.2     |                |         |     |
| 0                       |                |         |                         | 0       |                |         |     |
| 330 333                 | 336 339        | 342 345 | 348                     | 330 333 | 336 339        | 342 345 | 348 |
|                         | Temperature(K) |         |                         |         | Temperature(K) |         |     |
|                         | (c)            |         |                         |         | (d)            |         |     |
| 1                       |                |         |                         | 1       |                |         |     |
| noitcarfelomesahpdiuqiL |                |         | noitcarfelomesahpdiuqiL |         |                |         |     |
| 0.8                     |                |         |                         | 0.8     |                |         |     |
| 0.6                     |                |         |                         | 0.6     |                |         |     |
| 0.4                     |                |         |                         | 0.4     |                |         |     |
| 0.2                     |                |         |                         | 0.2     |                |         |     |
| 0                       |                |         |                         | 0       |                |         |     |
| 330 333                 | 336 339        | 342 345 | 348                     | 330 333 | 336 339        | 342 345 | 348 |
|                         | Temperature(K) |         |                         |         | Temperature(K) |         |     |
|                         | (e)            |         |                         |         | (f)            |         |     |
Figure 4.14: Equilibrium in propene hydration for an equimolar feed of reactants at 1 bar
with temperature independent and dependent chemical equilibrium constant: (a, b) phase
fractions [vapor ( ), liquid ( )], (c, d, e, f) mole fractions [propene ( ), water ( ),
|     |     | 2-propanol |     | ( )]. |     |     |     |
| --- | --- | ---------- | --- | ----- | --- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 75
The number of elements is N = N N = 3 1 = 2. The formula matrix and
|                |     |        |        |        | E   | C −   | R   | −   |     |     |        |
| -------------- | --- | ------ | ------ | ------ | --- | ----- | --- | --- | --- | --- | ------ |
| stoichiometric |     | matrix | of the | system | are | given | by: |     |     |     |        |
|                |     |        |        |       |     |      |     |     |     |     |        |
|                |     |        |        |        | 1 0 | 1     |     |     |     |     |        |
|                |     |        |        |        |     |       |     | h   | iT  |     |        |
|                |     |        | A      | =      |     |       | N = | 1   | 3 1 |     | (4.46) |
|                |     |        |        |       |     |      |     |     |     |     |        |
|                |     |        |        |        | 0 1 | 3     |     | −   | −   |     |        |
Phase behavior is described by the Peng-Robinson equation of state (Peng and Robinson,
1976) with all binary interaction parameters k set to zero, similar to Burgos-Sol´orzano
ij
et al. (2004). Gibbs energy of formation was taken from George et al. (1976). Calculations
are shown in Table 4.8. Small differences with Burgos-Sol´orzano et al. (2004) are due to
different chemical equilibrium constants. George et al. (1976) assumed that the system
obeystheLewisfugacityrule, whichdoesnotfullyaccountfornon-idealityofintermolecular
| forces | and | therefore | predicted |     | larger vapor |     | phase | fraction. |     |     |     |
| ------ | --- | --------- | --------- | --- | ------------ | --- | ----- | --------- | --- | --- | --- |
Table 4.8: Equilibrium mole fractions, phase amounts and phase fractions in cyclohexane
|     |     |     |     | synthesis |     | at 500 | K and | 30  | atm. |     |     |
| --- | --- | --- | --- | --------- | --- | ------ | ----- | --- | ---- | --- | --- |
Component Feed Our work Burgos-Sol´orzano et al. (2004) George et al. (1976)
|     |     |     | Vapor |     | Liquid |     | Vapor |     | Liquid | Vapor | Liquid |
| --- | --- | --- | ----- | --- | ------ | --- | ----- | --- | ------ | ----- | ------ |
benzene 0.247 4.45 10−6 5.43 10−6 4.00 10−6 4.92 10−6 3.64 10−4 3.87 10−4
|             |           |          | ×         |     | ×      |     | ×     |     | ×      | ×     | ×      |
| ----------- | --------- | -------- | --------- | --- | ------ | --- | ----- | --- | ------ | ----- | ------ |
|             | hydrogen  | 0.753    | 0.238     |     | 0.0204 |     | 0.249 |     | 0.0147 | 0.076 | 0.0023 |
| cyclohexane |           | 0        | 0.762     |     | 0.980  |     | 0.751 |     | 0.985  | 0.923 | 0.997  |
|             | n t (mol) | 4.05     | 0.132     |     | 0.918  |     | 0.148 |     | 0.902  | 0.660 | 0.391  |
|             | β         |          | 0.125     |     | 0.875  |     | 0.141 |     | 0.859  | 0.628 | 0.372  |
| 4.1.9       |           | Methanol | synthesis |     |        |     |       |     |        |       |        |
Methanol synthesis is usually modeled in the literature (Castier et al., 1989; Stateva and
Wakeham, 1997; Phoenix and Heidemann, 1998) by the following reactions:
|     |     |     |     |     | CO+2H |     | (cid:10) CH   | O   |     |     | (4.47) |
| --- | --- | --- | --- | --- | ----- | --- | ------------- | --- | --- | --- | ------ |
|     |     |     |     |     |       |     | 2             | 4   |     |     |        |
|     |     |     |     |     | CO +H |     | (cid:10) CO+H |     | O   |     | (4.48) |
|     |     |     |     |     | 2     | 2   |               |     | 2   |     |        |
from a mixture of carbon monoxide, carbon dioxide, hydrogen and water with methane
and n-octadecane as inerts. The number of elements is N = N N = 7 2 = 5. The
|     |     |     |     |     |     |     |     |     | E C | R   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     | −   | −   |     |
formula matrix and stoichiometric matrix of the system are given by:

76 Chapter 4. Application of CPE algorithms to reaction systems
|     |     |     |     |     |     |     |     |     |         |     |        |
| --- | --- | ---- | --- | --- | ---- | --- | --- | --- | ------- | --- | ------ |
|     |     | 1    | 1 0 | 0 1 | 0 0  |     |     |     |         |     |        |
|     |     |     |     |     |     |     |     |     |         |     |        |
|     |     | 0   | 1 0 | 1 0 | 0 0 |     |     |    |         | T  |        |
|     |     |     |     |     |     |     |     | 1 0 | 2 0 1   | 0 0 |        |
|     |     |     |     |     |     |     |     |     |         |     |        |
|     | A   | = 0 | 0 1 | 1 2 | 0 0 |     | N = | −  | −       |    | (4.49) |
|     |     |     |     |     |     |     |     | 1   | 1 1 1 0 | 0 0 |        |
|     |     |  0  | 0 0 | 0 0 | 1 0 |     |     | −   | −       |     |        |
|     |     |     |     |     |     |     |     |     |         |     |        |
|     |     |     |     |     |     |     |     |     |         |     |        |
|     |     | 0    | 0 0 | 0 0 | 0 1  |     |     |     |         |     |        |
Phase behavior is described by the Soave-Redlich-Kwong equation of state (Soave, 1972)
with binary interaction parameters k from Castier et al. (1989). Reference state (ideal
ij
gas) chemical potentials at 473.15 K and 1 bar were taken from Phoenix and Heidemann
(1998). In Tables 4.9 and 4.10 VLE and VLLE results are presented for two different feeds.
Results from Stateva and Wakeham (1997), and Castier et al. (1989) are also included for
comparison. The heavy hydrocarbon n-octadecane leads to the separation of the liquid
phases and the conditions permit the presence of a vapor phase. Larger deviations are
observed with the calculations from Stateva and Wakeham (1997), while both authors use
| different | values | for | the | chemical | equilibrium |     | constants. |     |     |     |     |
| --------- | ------ | --- | --- | -------- | ----------- | --- | ---------- | --- | --- | --- | --- |
Table 4.9: Equilibrium mole fractions, phase amounts and phase fractions in methanol
|     |     |     |     | synthesis |     | at 473.15 |     | K and | 300 bar. |     |     |
| --- | --- | --- | --- | --------- | --- | --------- | --- | ----- | -------- | --- | --- |
Component Feed Our work Stateva and Wakeham (1997) Castier et al. (1989)
|     |     |     |     | Vapor | Liquid |     |     | Vapor | Liquid | Vapor | Liquid |
| --- | --- | --- | --- | ----- | ------ | --- | --- | ----- | ------ | ----- | ------ |
carbon monoxide 0.15 6.27 10−5 1.09 10−5 1.33 10−5 traces 6.51 10−5 1.08 10−5
|     |     |     |     | ×   |     | ×   |     | ×   |     | ×   | ×   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
carbon dioxide 0.08 0.0006 0.0003 traces traces 0.0005 0.0002
|     | hydrogen     |     | 0.74 | 0.6597 |     | 0.0970 |     | 0.6493 | 0.0948 | 0.6589 | 0.0962 |
| --- | ------------ | --- | ---- | ------ | --- | ------ | --- | ------ | ------ | ------ | ------ |
|     | water        |     | 0    | 0.0471 |     | 0.2432 |     | 0.0464 | 0.2488 | 0.0473 | 0.2436 |
|     | methanol     |     | 0    | 0.2045 |     | 0.6349 |     | 0.2120 | 0.6371 | 0.2053 | 0.6354 |
|     | methane      |     | 0.3  | 0.0880 |     | 0.0246 |     | 0.0923 | 0.0193 | 0.0878 | 0.0246 |
|     | n-octadecane |     | 0    | 0      |     | 0      |     | 0      | 0      | 0      | 0      |
|     | n (mol)      |     | 100  | 26.346 |     | 27.702 |     | –      | –      | 26.421 | 27.622 |
t
|     | β   |     |     | 0.4875 |     | 0.5125 |     | 0.4968 | 0.5032 | 0.4889 | 0.5111 |
| --- | --- | --- | --- | ------ | --- | ------ | --- | ------ | ------ | ------ | ------ |
Table 4.10: Equilibrium mole fractions, phase amounts and phase fractions in methanol
|     |     |     |     | synthesis |     | at 473.15 |     | K and 101.3 | bar. |     |     |
| --- | --- | --- | --- | --------- | --- | --------- | --- | ----------- | ---- | --- | --- |
Component Feed Ourwork StatevaandWakeham(1997) Castieretal.(1989)
Vapor Liquid(aq) Liquid(org) Vapor Liquid(aq) Liquid(org) Vapor Liquid(aq) Liquid(org)
carbonmonoxide 0.1071 0.0010 7.00 10−6 0.0002 5.63 10−8 1.27 10−10 4.80 10−9 0.0011 6.82 10−6 0.0002
|     |     |     |     | ×   |     |     | ×   | ×   | ×   | ×   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
carbondioxide 0.0571 0.0548 0.0025 0.0271 7.27 10−12 2.96 10−6 3.18 10−12 0.0534 0.0024 0.0270
|     |     |     |     |     |     |     | ×   | ×   | ×   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
hydrogen 0.5286 0.5741 0.0059 0.1091 0.5328 0.0071 0.0600 0.5731 0.0058 0.1159
water 0.2143 0.1718 0.7715 0.1104 0.1635 0.7047 0.0070 0.1722 0.7709 0.1116
methanol 0 0.1426 0.2197 0.2767 0.2274 0.2870 0.1418 0.1441 0.2205 0.2753
methane 0.0214 0.0544 0.0004 0.0182 0.0752 0.0011 0.0210 0.0546 0.0004 0.0192
n-octadecane 0.0715 0.0014 1.18 10−14 0.4582 0.0010 2.70 10−6 0.7702 0.0015 1.31 10−15 0.4507
|     |         |     |        | ×      |        |     |     | ×   |     | ×             |        |
| --- | ------- | --- | ------ | ------ | ------ | --- | --- | --- | --- | ------------- | ------ |
|     | nt(mol) | 140 | 47.702 | 31.285 | 21.673 |     | –   | –   | –   | 46.917 31.508 | 22.030 |
β 0.4739 0.3108 0.2153 0.4843 0.3780 0.1377 0.4670 0.3136 0.2193

Chapter 4. Application of CPE algorithms to reaction systems 77
4.2 Transesterification of fatty acid triglycerides
with methanol
Biodiesel is a liquid mixture of fatty acid esters, which are alkyl monoesters of long
alkyl-chain (fatty) acids (Perdomo et al., 2013; Wu et al., 2016). It is not as toxic
as traditional diesel, biodegrades faster, has a higher cetane number and flash point,
and is practically free from sulfur components, that can lead to hazardous emissions
from combustion. Furthermore, biodiesel is produced from renewable sources and is
an alternative to conventional fossil fuels (Perdomo et al., 2013; Anikeev, 2014; Yancy-
Caballero and Guirardello, 2015; Wu et al., 2016). Esters in biodiesel can be also applied
in polymerizations as substrates (da Roza et al., 2012).
Biodiesel production can be achieved through a number of processes: esterification,
transesterification, blending, cracking, microemulsification, and pyrolysis (Yancy-Caballero
and Guirardello, 2015). Transesterification of vegetable oils and animal fats with different
alcohols at low pressures is usually the preferred method for biodiesel synthesis (Voll
et al., 2011) and homogeneous catalyzed transesterification is mainly employed. Acidic or
basic (NaOH, KOH, CH ONa) catalysts are used, while non-catalytic synthesis is also
3
reported with sub- and supercritical alcohols (Anikeev, 2014; Voll et al., 2011). Two
liquid phases are expected at equilibrium, a fatty acid methyl-ester and a glycerol rich
phase (Yancy-Caballero and Guirardello, 2015). Due to its low cost and availability,
methanol is the alcohol selected for the reaction. Equilibrium is shifted toward favorable
equilibrium yields using an excess of the alcohol (Likozar and Levec, 2014; Perdomo
et al., 2013; Wu et al., 2016; Yancy-Caballero and Guirardello, 2015, 2013). Glycerol is a
by-product of transesterification that is separated after equilibrium has been established
(Yancy-Caballero and Guirardello, 2013) and can find different applications (Perdomo
et al., 2013; Liu et al., 2016). Soybean, algal, canola, sunflower, cotton, palm, and coconut
oil are used in the reactions (Likozar and Levec, 2014; Yancy-Caballero and Guirardello,
2015). Interest has shifted toward non-edible oils such as linseed, castor, Karanja, neem,
rubber, jatropha and cashew oil (Mathiarasi and Partha, 2016). Second generation biofuels
involve the transesterification with oils from hazardous waste (Perdomo et al., 2013). As
far as the synthesis is concerned, water in the system can lead to reduced yields due to
two phenomena: acceleration of ester hydrolysis to fatty acids reacting with the basic
catalyst to produce even more water, and shift of the hydroxide/alkoxide equilibrium to
hydroxide, reducing the concentration of the true catalyst, which is the methoxide ions
(Wu et al., 2016). Finally, saponification can take place between glycerin and the basic
catalyst (Wu et al., 2016).
Anikeev et al. (2012) and Anikeev (2014) examined the successive transesterifications of a
triglyceride with methanol, according to the following reaction scheme:

78 Chapter 4. Application of CPE algorithms to reaction systems
|     | H C | OR  |     |     |     |     | H C | OR  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 2   |     | 1   |     |     |     | 2   | 1   |     |     |     |
(4.50)
|     | HC  | OR  | +   | CH  | OH  |     | HC  | OR + | R   | O CH |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     |     | 1   | 3   |     |     |     | 1    | 2   | 3    |     |
|     | H C | OR  |     |     |     |     | H C | OH   |     |      |     |
|     | 2   |     | 2   |     |     |     | 2   |      |     |      |     |
|     | H C | OR  |     |     |     |     | H C | OR   |     |      |     |
|     | 2   |     | 1   |     |     |     | 2   | 1    |     |      |     |
(4.51)
|     | HC  | OR  | +   | CH  | OH  |     | HC  | OH + | R   | O CH |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     |     | 1   | 3   |     |     |     |      | 1   | 3    |     |
|     | H C | OR  |     |     |     |     | H C | OR   |     |      |     |
|     | 2   |     | 2   |     |     |     | 2   | 2    |     |      |     |
|     | H C | OR  |     |     |     |     | H C | OR   |     |      |     |
|     | 2   |     | 1   |     |     |     | 2   | 1    |     |      |     |
(4.52)
|     | HC  | OR  | +   | CH  | OH  |     | HC  | OH + | R   | O CH |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- |
|     |     |     | 1   | 3   |     |     |     |      | 1   | 3    |     |
|     | H C | OH  |     |     |     |     | H C | OH   |     |      |     |
|     | 2   |     |     |     |     |     | 2   |      |     |      |     |
|     | H C | OR  |     |     |     |     | H C | OH   |     |      |     |
|     | 2   |     | 1   |     |     |     | 2   |      |     |      |     |
(4.53)
|     | HC  | OH  | +   | CH  | OH  |     | HC  | OH + | R   | O CH |        |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | ------ |
|     |     |     |     | 3   |     |     |     |      | 1   | 3    |        |
|     | H C | OR  |     |     |     |     | H C | OR   |     |      |        |
|     | 2   |     | 2   |     |     |     | 2   | 2    |     |      |        |
|     | H C | OR  |     |     |     |     | H C | OH   |     |      |        |
|     | 2   |     | 1   |     |     |     | 2   |      |     |      |        |
|     | HC  | OH  | +   | CH  | OH  |     | HC  | OH + | R O | CH   | (4.54) |
|     |     |     |     | 3   |     |     |     |      | 1   | 3    |        |
|     | H C | OH  |     |     |     |     | H C | OH   |     |      |        |
|     | 2   |     |     |     |     |     | 2   |      |     |      |        |
At each step the group OR or OR is substituted by a OH, until glycerol is obtained.
|     |     |     | 1   |     | 2   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | −   |     | −   |     |     |     | −   |     |     |     |
The authors showed calculations for a single vapor phase and two starting components:
palmitic-palmitic-oleic and oleic-linoleic-linoleic triglycerides. Both compounds share the
same R group but differ in their R group. The chemical compositions of all components
| 2   |     |     |     | 1   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and elements for the two transesterification systems is presented in Table 4.11. The number
of elements is N = N N = 9 5 = 4. The formula matrix and stoichiometric matrix
|               | E         | C   | R   |     |     |     |     |        |     |     |     |
| ------------- | --------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
|               |           |     | −   | −   |     |     |     |        |     |     |     |
| of the system | are given |     | by: |     |     |     |     |        |     |     |     |
|               |           |     |     |    |     |     |     |       |     |     |     |
|               |           |     |     | 1   | 3 3 | 3   | 3 3 | 3 1 1  |     |     |     |
|               |           |     |     |    |     |     |     |       |     |     |     |
|               |           |     |     | 3  | 2 3 | 3   | 4 4 | 5 2 2 |     |     |     |
|               |           |     | A   | =  |     |     |     |       |     |     |     |
|               |           |     |     |    |     |     |     | 0     |     |     |     |
|               |           |     |     | 0  | 2 2 | 1   | 1 0 | 0 1    |     |     |     |

|     |     |     |     |    |     |     |     |      |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |     | 0   | 1 0 | 1   | 0 1 | 0 0 1 |     |     |     |
(4.55)
|     |     |     |    |     |     |     |     |       | T  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |     | 1 1 | 1   | 0   | 0   | 0 0 0 | 1   |     |     |
|     |     |     | −  | −   |     |     |     |       |    |     |     |
|     |     |     |     | 1 1 | 0   | 1   | 0   | 0 0 1 | 0  |     |     |

|     |     |     | −  | −   |     |     |     |       |    |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |    |     |     |     |     |       |    |     |     |
|     |     | N   | =  | 1 0 | 1   | 0   | 1   | 0 0 1 | 0  |     |     |
|     |     |     | −  |     |     |     |     |       |    |     |     |
−
|     |     |     |    | 1 0 | 0   | 1   | 0   | 1 0 1 | 0  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     |     |    |     |     |     |     |       |    |     |     |
|     |     |     | −  |     |     | −   |     |       |    |     |     |
|     |     |     |     | 1 0 | 0   | 0   | 1   | 0 1 1 | 0   |     |     |
|     |     |     |     | −   |     |     | −   |       |     |     |     |

Chapter 4. Application of CPE algorithms to reaction systems 79
Table 4.11: Component and element numbering for the PPOFAG (R C H O) and
1 16 31
≡
OLLFAG transesterification (R C H O) systems (for both mixtures R C H O).
1 18 33 2 18 31
≡ ≡
|     |     | Component |      | Element |
| --- | --- | --------- | ---- | ------- |
|     |     | 1         | CH O | CHO     |
4
|     |     | 2 C H | O (R ) R  | H   |
| --- | --- | ----- | --------- | --- |
|     |     | 3     | 5 3 1 2 2 |     |
|     |     | 3 C   | H O (R )  | R   |
|     |     |       | 3 6 3 1 2 | 1   |
|     |     | 4 C   | H O R R   | R   |
|     |     |       | 3 6 3 1 2 | 2   |
|     |     | 5     | C H O R   |     |
3 7 3 1
|     |     | 6   | C H O R |     |
| --- | --- | --- | ------- | --- |
3 7 3 2
|     |     | 7   | C H O |     |
| --- | --- | --- | ----- | --- |
3 8 3
|     |     | 8   | CH OR |     |
| --- | --- | --- | ----- | --- |
3 1
|     |     | 9   | CH OR |     |
| --- | --- | --- | ----- | --- |
3 2
The compounds that exist in both mixtures are shown in Table 4.12. Phase behavior is
described by the Peng-Robinson equation of state (Peng and Robinson, 1976) with all
binary interaction parameters k set to zero. Critical constants and acentric factors were
ij
predicted by Anikeev (2014) and chemical equilibrium constants were taken from the same
authors. Figures 4.15 and 4.16 show phase and mole fractions at equilibrium for both
| systems | at 1 atm and | triglyceride/methanol | ratio | equal to 1:3. |
| ------- | ------------ | --------------------- | ----- | ------------- |
For the temperature window selected, both systems can mostly exist as a two- or three-
phase mixture. At lower temperatures, we begin with LLE of an ester-rich phase (CH OR ,
3 1
CH OR ) and a glycerol-rich phase. At higher temperatures, a vapor phase can appear.
3 2
After the vapor phase appears, increasing the temperature decreases more rapidly the
amount of the glycerol-rich liquid phase, which eventually leads to VLE. For the PPOFAG
transesterification, at higher temperatures both liquid phases disappear and it can exist
| as a single-vapor | phase. |                 |     |     |
| ----------------- | ------ | --------------- | --- | --- |
| 4.3               | Speed  | and convergence |     |     |
†
Computational efficiency of algorithms in the literature is usually reported as CPU time
and/or number of iterations. Total CPU time for each system at specified conditions
is presented for both algorithms in Table 4.13. This reflects the time needed by each
algorithm to determine the equilibrium solution including initialization, solving for simul-
taneous chemical and phase equilibrium, and finally, stability analysis. The successive
substitution algorithm is entirely a first-order method, whereas the combined algorithm
uses a second-order method for final convergence. Nevertheless, the latter requires calcula-
tion of derivatives and inversion of matrices, which could make the method not as fast as
expected. In other words, absolute CPU time is not proportional to the number of the
iterations. Although the speed is an indication of the efficiency of the algorithm, results in
| † Appears | in Tsanas | et al. (2017a,b) |     |     |
| --------- | --------- | ---------------- | --- | --- |

80 Chapter 4. Application of CPE algorithms to reaction systems
| Table 4.12: | Compounds | in triglyceride | esterification. |     |
| ----------- | --------- | --------------- | --------------- | --- |
Abbreviation
| Compound |          |               | Chemical | formula |
| -------- | -------- | ------------- | -------- | ------- |
|          | (Anikeev | et al., 2012) |          |         |
|          |          |               | H C OOC  | H       |
|          |          |               | 2        | 16 31   |
Palmitic-palmitic-oleic
|     |     | PPOFAG | HC OOC | H   |
| --- | --- | ------ | ------ | --- |
16 31
fatty acid glyceride
|     |     |     | H C OOC | H     |
| --- | --- | --- | ------- | ----- |
|     |     |     | 2       | 18 33 |
|     |     |     | H C OOC | H     |
|     |     |     | 2       | 18 31 |
Oleic-linoleic-linoleic
|     |     | OLLFAG | HC OOC | H   |
| --- | --- | ------ | ------ | --- |
18 31
fatty acid glyceride
|                   |       |          | H C OOC | H     |
| ----------------- | ----- | -------- | ------- | ----- |
|                   |       |          | 2       | 18 33 |
|                   |       |          | H C OOC | H     |
|                   |       |          | 2       | 16 31 |
| Palmitic-palmitic | fatty |          |         |       |
|                   |       |          | HC OOC  | H     |
|                   |       | PPDFADIG |         | 16 31 |
acid di-glyceride
|     |     |     | H C OH |     |
| --- | --- | --- | ------ | --- |
2
|                   |       |          | H 2 C OOC | 18 H 31 |
| ----------------- | ----- | -------- | --------- | ------- |
| Linoleic-linoleic | fatty |          |           |         |
|                   |       | LLDFADIG | HC OOC    | H       |
18 31
acid di-glyceride
|     |     |     | H C OH |     |
| --- | --- | --- | ------ | --- |
2
|                |            |          | H C OOC | H     |
| -------------- | ---------- | -------- | ------- | ----- |
|                |            |          | 2       | 16 31 |
| Palmitic-oleic | fatty acid |          |         |       |
|                |            | PODFADIG | HC OH   |       |
di-glyceride
|                      |      |     | H C OOC | H     |
| -------------------- | ---- | --- | ------- | ----- |
|                      |      |     | 2       | 18 33 |
|                      |      |     | H C OOC | H     |
|                      |      |     | 2       | 18 31 |
| Linoleic-oleic fatty | acid |     |         |       |
|                      |      |     | HC OH   |       |
LOFADIG
di-glyceride
|                |      |          | H C OOC | H     |
| -------------- | ---- | -------- | ------- | ----- |
|                |      |          | 2       | 18 33 |
|                |      |          | H C OOC | H     |
|                |      |          | 2       | 16 31 |
| Palmitic fatty | acid |          |         |       |
|                |      | PFAMONOG | HC OH   |       |
mono-glyceride
|     |     |     | H C OH |     |
| --- | --- | --- | ------ | --- |
2
|                |      |          | H C OOC | H     |
| -------------- | ---- | -------- | ------- | ----- |
|                |      |          | 2       | 18 31 |
| Linoleic fatty | acid |          |         |       |
|                |      | LFAMONOG | HC OH   |       |
mono-glyceride
|     |     |     | H C OH |     |
| --- | --- | --- | ------ | --- |
2
|     |     |     | H C OH |     |
| --- | --- | --- | ------ | --- |
2
| Oleic fatty | acid |     |       |     |
| ----------- | ---- | --- | ----- | --- |
|             |      |     | HC OH |     |
OFAMONOG
mono-glyceride
|     |     |     | H C OOC | H     |
| --- | --- | --- | ------- | ----- |
|     |     |     | 2       | 18 33 |
|     |     |     | H C     | OH    |
2
| Glycerol       |      | –     | HC       | OH  |
| -------------- | ---- | ----- | -------- | --- |
|                |      |       | H 2 C    | OH  |
| Palmitic fatty | acid |       |          |     |
|                |      | PFAME | C H OOCH |     |
|                |      |       | 16 31    | 3   |
methyl ester
| Linoleic fatty | acid |       |          |     |
| -------------- | ---- | ----- | -------- | --- |
|                |      | LFAME | C H OOCH |     |
|                |      |       | 18 31    | 3   |
methyl ester
| Oleic fatty acid | methyl |       |          |     |
| ---------------- | ------ | ----- | -------- | --- |
|                  |        | OFAME | C H OOCH |     |
|                  |        |       | 18 33    | 3   |
ester

Chapter 4. Application of CPE algorithms to reaction systems 81
1
1
| 0.8 |     |     | noitcarfelomesahpropaV 0.8 |     |
| --- | --- | --- | -------------------------- | --- |
noitcarfesahP
| 0.6 |     |     | 0.6 |     |
| --- | --- | --- | --- | --- |
| 0.4 |     |     | 0.4 |     |
| 0.2 |     |     | 0.2 |     |
| 0   |     |     | 0   |     |
300 350 400 450 500 550 600 650 300 350 400 450 500 550 600 650
|     | Temperature(K) |     |     | Temperature(K) |
| --- | -------------- | --- | --- | -------------- |
(a) (b)
noitcarfelomesahpdiuqilhcir-lorecylG
| noitcarfelomesahpdiuqilhcir-retsE 1 |     |     | 1   |     |
| ----------------------------------- | --- | --- | --- | --- |
| 0.8                                 |     |     | 0.8 |     |
| 0.6                                 |     |     | 0.6 |     |
| 0.4                                 |     |     | 0.4 |     |
| 0.2                                 |     |     | 0.2 |     |
| 0                                   |     |     | 0   |     |
300 350 400 450 500 550 600 650 300 350 400 450 500 550 600 650
|     | Temperature(K) |     |     | Temperature(K) |
| --- | -------------- | --- | --- | -------------- |
(c) (d)
Figure 4.15: Equilibrium in PPOFAG transesterification with methanol and
PPOFAG/methanol ratio equal to 1:3 at 1 atm: (a) phase fractions [vapor ( ),
ester-rich liquid ( ), glycerol-rich liquid ( )], (b, c, d) mole fractions [methanol ( ),
| PPOFAG | ( ), PPFADIG  | ( ), POFADIG | ( ), PFAMONOG | ( ), OFAMONOG |
| ------ | ------------- | ------------ | ------------- | ------------- |
|        | ( ), glycerol | ( ), PFAME   | ( ), OFAME    | ( )].         |

82 Chapter 4. Application of CPE algorithms to reaction systems
1
1
| 0.8 |     |     | noitcarfelomesahpropaV 0.8 |     |
| --- | --- | --- | -------------------------- | --- |
noitcarfesahP
| 0.6 |     |     | 0.6 |     |
| --- | --- | --- | --- | --- |
| 0.4 |     |     | 0.4 |     |
| 0.2 |     |     | 0.2 |     |
| 0   |     |     | 0   |     |
300 350 400 450 500 550 600 650 300 350 400 450 500 550 600 650
|     | Temperature(K) |     |     | Temperature(K) |
| --- | -------------- | --- | --- | -------------- |
(a) (b)
noitcarfelomesahpdiuqilhcir-lorecylG
| noitcarfelomesahpdiuqilhcir-retsE 1 |     |     | 1   |     |
| ----------------------------------- | --- | --- | --- | --- |
| 0.8                                 |     |     | 0.8 |     |
| 0.6                                 |     |     | 0.6 |     |
| 0.4                                 |     |     | 0.4 |     |
| 0.2                                 |     |     | 0.2 |     |
| 0                                   |     |     | 0   |     |
300 350 400 450 500 550 600 650 300 350 400 450 500 550 600 650
|     | Temperature(K) |     |     | Temperature(K) |
| --- | -------------- | --- | --- | -------------- |
(c) (d)
Figure 4.16: Equilibrium in OLLFAG transesterification with methanol and
OLLFAG/methanol ratio equal to 1:3 at 1 atm: (a) phase fractions [vapor ( ),
ester-rich liquid ( ), glycerol-rich liquid ( )], (b, c, d) mole fractions [methanol ( ),
| OLLFAG | ( ), LLFADIG  | ( ), LOFADIG | ( ), LFAMONOG | ( ), OFAMONOG |
| ------ | ------------- | ------------ | ------------- | ------------- |
|        | ( ), glycerol | ( ), LFAME   | ( ), OFAME    | ( )].         |

Chapter 4. Application of CPE algorithms to reaction systems 83
Table 4.13 are not universally conclusive. CPU time depends on the thermodynamic model
selected. Simple models are expected to provide faster equilibrium results. Especially
for ideal systems, the outer loop (non-ideality update) in the successive substitution
algorithm is not required because components have composition independent fugacity
or activity coefficients. It should not be overlooked that CPU time depends also on the
implementation of the method that has to do with the efficiency of matrix manipulation
(e.g. inversion, solution of linear systems, etc.). Finally, CPU time can differ due to the
| hardware, |     | computer | language and | compilers. |     |     |     |     |     |
| --------- | --- | -------- | ------------ | ---------- | --- | --- | --- | --- | --- |
Table 4.13: CPU time to obtain the equilibrium solution of the systems examined (SSA:
successive substitution algorithm, CA: combined algorithm, processor: IntelRCoreTM
(cid:13)
|     |     |        | i7-5500U |     | CPU@  | 2.40 GHz). |     |          |         |
| --- | --- | ------ | -------- | --- | ----- | ---------- | --- | -------- | ------- |
|     |     | System |          |     | T (K) | p          | N   | SSA (ms) | CA (ms) |
P
|     |      | Formaldehyde/water    |              |     | 310    | 1 atm    | 2   | 1.28 | –    |
| --- | ---- | --------------------- | ------------ | --- | ------ | -------- | --- | ---- | ---- |
|     |      | Xylene                | separation   |     | 350    | 0.05 atm | 2   | 1.31 | –    |
|     |      | Acetic                | acid/ethanol |     | 355    | 1 atm    | 2   | 1.72 | 1.46 |
|     |      | Acetic acid/1-butanol |              |     | 370    | 1 atm    | 2   | 1.62 | 1.48 |
|     |      | MTBE                  | synthesis    |     | 320.92 | 1 atm    | 2   | 1.87 | 1.30 |
|     | TAME | synthesis             | (N =         | 2)  | 330    | 1.52 bar | 2   | 1.60 | 1.37 |
R
|     | Propene | hydration | [Keq = f(T)] |     | 345 | 1 bar | 2   | 1.45 | 1.47 |
| --- | ------- | --------- | ------------ | --- | --- | ----- | --- | ---- | ---- |
6
|     |     | Cyclohexane | synthesis |     | 500    | 30 atm    | 2   | 1.48 | 1.30 |
| --- | --- | ----------- | --------- | --- | ------ | --------- | --- | ---- | ---- |
|     |     | Methanol    | synthesis |     | 473.15 | 101.3 bar | 3   | 3.08 | 2.23 |
|     |     | PPOFAG      |           |     | 500    | 1 atm     | 3   | 3.07 | 3.25 |
|     |     | OLLFAG      |           |     | 450    | 1 atm     | 3   | 2.82 | 3.06 |
Apart from the CPU time, we also present the number of iterations of each solution
procedure in both algorithms (Figures 4.17 to 4.25): Q-function minimization, main
calculation for each phase set, and the number of inner-loop (Newton) iterations per outer
loop non-ideality update when the Lagrange multipliers method is employed. Stability
analysis iterations are not shown. Minimization of Q-function follows the same trend in
both algorithms, since this is a common initialization routine. Change of the error at
each iteration reveals the convergence rate type of each algorithm. Successive substitution
figures show linear convergence rate and require more iterations to reach the Gibbs energy
minimum. In the figures of the combined algorithm, after three iterations of successive
substitution, it is evident that the error reduces quadratically, as a result of accelerated
calculations by the modified RAND method. Direct comparison of the algorithms shows
in general a decrease in the iteration number when the combined algorithm is used. The
difference can be small for some examples, such as propene hydration, and for others it
ranges from two to even five times fewer iterations. The number of inner loop iterations
in the successive substitution algorithm is decreasing the closer we approach to the final
solution. However, the iteration number is sensible for the Lagrange multipliers method,
taking into account that a linearly convergent method is expected to be slower. The

84 Chapter 4. Application of CPE algorithms to reaction systems
number of iterations is also not conclusive about the efficiency of the calculations or the
speed. Single iteration cost is not the same for the different algorithms. The number of
iterations depends on initial estimates and the convergence criterion tolerance. Whenever
a comparison with the literature can be made, the factors that affect CPU time or number
of iterations must be considered.
Formaldehyde/water mixture and xylene separation
•
Both systems are ideal and there is no need of an outer loop to update fugacity or
activity coefficients. Successive substitution algorithm attains quadratic convergence
rate and the combined algorithm does not require to switch calculations to the modified
RAND. No convergence behavior is presented.
Esterification of acetic acid with ethanol
•
The initial assumption is a single vapor phase, which does not require the nested-loop
procedure to converge. Vapor phase is ideal and the total mole numbers do not change
due to the reaction. These are the conditions under which the Q-function minimization
can yield the equilibrium solution of the single-phase assumption (section 3.2.3). For
this reason, only the convergence behavior of the two-phase system appears in Figure
4.17.
Xiao et al. (1989) studied the application of two stoichiometric algorithms, the S-C
(Sanderson and Chien, 1973) and the KZ algorithm. The S-C algorithm follows the
conventional stoichiometric approach using nested loops. In the inner loop the phase
equilibrium problem is solved based on the Rachford-Rice equation and successive
substitution. In the outer loop, the reaction extents are updated. The KZ algorithm
is proposed by the authors as an improvement of the S-C algorithm. In this new
formulation, the loops of the S-C algorithm are switched. The algorithms mentioned in
Xiao et al. (1989) should be comparable with the successive substitution algorithm in
this work, since all three are based on a nested-loop procedure. To fully converge to the
solution, the successive substitutuion algorithm needed 44 outer loop iterations (106
Newton iterations), the combined algorithm 3 (12 Newton iterations and 4 modified
RAND iterations), the S-C algorithm 10 (42 Newton iterations) and the KZ algorithm
9 (23 Newton iterations). The reason why our successive substitution algorithm needs
almost three times as many iterations as the slower S-C algorithm is probably because
Xiao et al. (1989) used a very lose convergence criterion. They calculated the K-factors
of VLE as K = y /x and the procedure stopped when PNC(Knew/K 1)2 < 10−6.
i i i i=1 i i −
In our method, convergence was assumed after tighter criteria, when the error given
by Eq. 3.77 is less than 10−10. The combined algorithm is superior with a total of 12
inner loop iterations and only 4 additional RAND iterations to fully converge. Finally,
in Xiao et al. (1989) the initial assumption is a two-phase mixture, in contrast with our
approach, where we assume a single phase and later test if an additional phase must be
considered.

Chapter 4. Application of CPE algorithms to reaction systems 85
| 4       |            |       |         | 4     |            |      |
| ------- | ---------- | ----- | ------- | ----- | ---------- | ---- |
| 0       |            |       |         | 0     |            |      |
| )rorre( |            |       | )rorre( |       |            |      |
| 4       |            |       |         | 4     |            |      |
| −       |            |       |         | −     |            |      |
| 01      |            |       | 01      |       |            |      |
| gol 8   |            |       | gol     | 8     |            |      |
| −       |            |       |         | −     |            |      |
| 12      |            |       |         | 12    |            |      |
| −       |            |       |         | −     |            |      |
| 16      |            |       |         | 16    |            |      |
| − 0 8   | 16 24      | 32 40 | 48      | − 0 2 | 4 6        | 8 10 |
|         | Iterations |       |         |       | Iterations |      |
|         | (a)        |       |         |       | (b)        |      |
6
5
snoitareti
4
|     | pool | 3   |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- |
rennI
2
1
0
|     |     | 0 6 12 | 18 24          | 30 36 42 | 48  |     |
| --- | --- | ------ | -------------- | -------- | --- | --- |
|     |     | Outer  | loop iteration | index    |     |     |
(c)
Figure 4.17: Convergence in acetic acid/ethanol esterification for an equimolar feed of
reactants at 355 K and 1 atm: (a) successive substitution algorithm, (b) combined
algorithm, (c) inner loop (Newton) iterations per outer loop non-ideality updates
|     | [Q-function | minimization | (   | ), V ( ), VL | ( )]. |     |
| --- | ----------- | ------------ | --- | ------------ | ----- | --- |

86 Chapter 4. Application of CPE algorithms to reaction systems
Castier et al. (1989) presented a second-order stoichiometric method. The authors
initialize calculations with direct substitution aided by the General Dominant Eigen-
value Method (GDEM) (Crowe and Nishio, 1975) for accelerated calculations. Final
convergence is achieved with Murray’s minimization. It is suggested in their method
to use 5 direct substitution iterations followed by 1 GDEM step for the single-phase
chemical equilibrium, 2 GDEM steps for two-phase systems and 3 GDEM steps for
three-phase systems. They also mention which criteria must be met to skip GDEM
and enter Murray’s minimization. The Murray steps are very efficient and are used
only for final convergence. The authors performed their calculations at slightly higher
temperature than the one in this work (358.15 K). When the vapor phase was considered
ideal, a single vapor phase exists at equilibrium with 3 Murray iterations. Conversely,
when an EoS that accounts for the acid dimerization is used, the inital assumption of a
vapor phase needed 3 Murray iterations and the final vapor-liquid mixture needed 2
Murray iterations.
Esterification of acetic acid with 1-butanol
•
Bonilla-Petriciolet et al. (2008a) applied simulated annealing to determine the equilib-
rium of two-phase reaction systems. Their algorithm belongs to stochastic optimization
methods formulated as a stoichiometric problem. Their procedure involves solving for
CPE at specific conditions, using different feeds and initial estimates. At the end they
report total number of function evaluations and success rate, showing the percentage of
the initial estimates that will actually lead to the equilibrium solution. For this system,
they mention total time of 40 s compared to our 1.62 ms with successive substitution
and 1.48 with the combined algorithm. Moreover, the authors report 0% and 3% success
rate for two feed compositions they chose to demostrate the algorithm performance,
while our algorithms did not face problems with the same feeds.
MTBE synthesis
•
Castier et al. (1989) tested the system under different conditions from this work.
Calculations were made for the temperature window of the two-phase system at 5.07
bar with 1-butene as inert instead of n-butane. Initialization in our work needed 9
iterations. The successive substitution algorithm required for the single-phase reaction
9 outer loop iterations (25 Newton iterations) and for the two-phase system 30 (73
Newton iterations). With the combined algorithm L and VL phase sets needed 3
outer loop iterations (13 and 14 Newton iterations) and additionally 3 and 4 modified
RAND iterations respectively. Castier et al. (1989) reported 2 Murray iterations for the
single-phase convergence and 1 Murray iteration for the two-phase system. No further
information was given for the initialization iterations.
TAME synthesis
•
Bonilla-Petriciolet et al. (2008a) reported total time of 85 s compared with our 1.60
ms with successive substitution and 1.37 with the combined algorithm. For all the

Chapter 4. Application of CPE algorithms to reaction systems 87
3
3
| 0         |     |     |     |     | 0         |     |     |     |
| --------- | --- | --- | --- | --- | --------- | --- | --- | --- |
| 3         |     |     |     |     | 3         |     |     |     |
| )rorre( − |     |     |     |     | )rorre( − |     |     |     |
6
6
| 01 − |     |     |     |     | 01 − |     |     |     |
| ---- | --- | --- | --- | --- | ---- | --- | --- | --- |
gol
gol
| 9   |     |     |     |     | 9   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
−
| 12  |            |       |     |     | 12  |     |            |     |
| --- | ---------- | ----- | --- | --- | --- | --- | ---------- | --- |
| −   |            |       |     |     | −   |     |            |     |
| 15  |            |       |     |     | 15  |     |            |     |
| −   |            |       |     |     | − 0 | 1 2 | 3 4 5 6 7  | 8   |
| 0 5 | 10 15      | 20 25 | 30  | 35  |     |     |            |     |
|     | Iterations |       |     |     |     |     | Iterations |     |
|     | (a)        |       |     |     |     |     | (b)        |     |
7
6
snoitareti
5
4
pool
3
rennI
2
1
0
|     |     | 0   | 5 10  | 15             | 20 25 | 30 35 |     |     |
| --- | --- | --- | ----- | -------------- | ----- | ----- | --- | --- |
|     |     |     | Outer | loop iteration | index |       |     |     |
(c)
Figure 4.18: Convergence in acetic acid/1-butanol esterification for an equimolar feed of
reactants at 370 K and 1 atm: (a) successive substitution algorithm, (b) combined
algorithm, (c) inner loop (Newton) iterations per outer loop non-ideality updates
|     | [Q-function | minimization |     | (   | ), L ( | ), VL ( | )]. |     |
| --- | ----------- | ------------ | --- | --- | ------ | ------- | --- | --- |

88 Chapter 4. Application of CPE algorithms to reaction systems
| 3         |            |          |         | 3     |            |      |     |
| --------- | ---------- | -------- | ------- | ----- | ---------- | ---- | --- |
| 0         |            |          |         | 0     |            |      |     |
| 3         |            |          |         | 3     |            |      |     |
| )rorre( − |            |          | )rorre( | −     |            |      |     |
| 6         |            |          |         | 6     |            |      |     |
| 01 −      |            |          | 01      | −     |            |      |     |
| gol       |            |          | gol     |       |            |      |     |
| 9         |            |          |         | 9     |            |      |     |
| −         |            |          |         | −     |            |      |     |
| 12        |            |          |         | 12    |            |      |     |
| −         |            |          |         | −     |            |      |     |
| 15        |            |          |         | 15    |            |      |     |
| − 0 4     | 8 12 16    | 20 24 28 | 32      | − 0 2 | 4 6        | 8 10 | 12  |
|           | Iterations |          |         |       | Iterations |      |     |
|           | (a)        |          |         |       | (b)        |      |     |
7
6
snoitareti
5
4
pool
3
rennI
2
1
0
|     |     | 0 4   | 8 12 16        | 20 24 28 | 32  |     |     |
| --- | --- | ----- | -------------- | -------- | --- | --- | --- |
|     |     | Outer | loop iteration | index    |     |     |     |
(c)
Figure 4.19: Convergence in MTBE synthesis for isobutene/methanol ratio equal to 1:1.1
without inert at 320.92 K and 1 atm: (a) successive substitution algorithm, (b) combined
algorithm, (c) inner loop (Newton) iterations per outer loop non-ideality updates
|     | [Q-function | minimization | (   | ), L ( ), | VL ( )]. |     |     |
| --- | ----------- | ------------ | --- | --------- | -------- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 89
feeds selected, the authors had 100% success rate at finding the equilibrium solution. It
must be mentioned that our calculations refer to the two-reaction system as presented
in Chen et al. (2002) instead of the single-reaction system in Bonilla-Petriciolet et al.
(2008a).
| 4   |     |     |     | 4   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
0
0
| 4   |     |     |         | 4   |     |     |
| --- | --- | --- | ------- | --- | --- | --- |
|     |     |     | )rorre( | −   |     |     |
)rorre( −
| 8     |            |       |     | 8     |            |       |
| ----- | ---------- | ----- | --- | ----- | ---------- | ----- |
| −     |            |       |     | −     |            |       |
| 01    |            |       | 01  |       |            |       |
| gol   |            |       | gol |       |            |       |
| 12    |            |       |     | 12    |            |       |
| −     |            |       |     | −     |            |       |
| 16    |            |       |     | 16    |            |       |
| −     |            |       |     | −     |            |       |
| 20    |            |       |     | 20    |            |       |
| − 0 3 | 6 9        | 12 15 | 18  | − 0 1 | 2 3 4 5    | 6 7 8 |
|       | Iterations |       |     |       | Iterations |       |
|       | (a)        |       |     |       | (b)        |       |
7
6
snoitareti
5
4
pool
3
rennI
2
1
0
|     |     | 0 3   | 6 9            | 12 15 | 18  |     |
| --- | --- | ----- | -------------- | ----- | --- | --- |
|     |     | Outer | loop iteration | index |     |     |
(c)
Figure 4.20: Convergence in the two-reaction TAME synthesis for a stoichiometric ratio of
reactants and methanol/n-pentane ratio equal to 2:1 at 330 K and 1.52 bar: (a) successive
substitution algorithm, (b) combined algorithm, (c) inner loop (Newton) iterations per
outer loop non-ideality updates [Q-function minimization ( ), L ( ), VL ( )].
| Propene hydration |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- |
•
Bonilla-Petriciolet et al. (2008a) reported total time of 30 s compared with our 1.45
ms with successive substitution and 1.47 with the combined algorithm. The lowest
success rate they reported was 41%. This is an example of a system where the combined
algorithm is not decisively faster than the successive substitution algorithm.
| Cyclohexane | synthesis |     |     |     |     |     |
| ----------- | --------- | --- | --- | --- | --- | --- |
•

90 Chapter 4. Application of CPE algorithms to reaction systems
| 3         |            |     |         | 3     |            |      |
| --------- | ---------- | --- | ------- | ----- | ---------- | ---- |
| 0         |            |     |         | 0     |            |      |
| 3         |            |     |         | 3     |            |      |
| )rorre( − |            |     | )rorre( | −     |            |      |
| 6         |            |     |         | 6     |            |      |
| 01 −      |            |     | 01      | −     |            |      |
| gol       |            |     | gol     |       |            |      |
| 9         |            |     |         | 9     |            |      |
| −         |            |     |         | −     |            |      |
| 12        |            |     |         | 12    |            |      |
| −         |            |     |         | −     |            |      |
| 15        |            |     |         | 15    |            |      |
| − 0       | 2 4        | 6 8 | 10      | − 0 2 | 4 6        | 8 10 |
|           | Iterations |     |         |       | Iterations |      |
|           | (a)        |     |         |       | (b)        |      |
8
snoitareti 6
pool 4
rennI
2
0
|     |     | 0 2   | 4              | 6 8   | 10  |     |
| --- | --- | ----- | -------------- | ----- | --- | --- |
|     |     | Outer | loop iteration | index |     |     |
(c)
Figure 4.21: Convergence in propene hydration for an equimolar feed of reactants at 345
K and 1 bar: (a) successive substitution algorithm, (b) combined algorithm, (c) inner loop
(Newton) iterations per outer loop non-ideality updates [Q-function minimization ( ), L
|     |     | (   | ), VL ( | )]. |     |     |
| --- | --- | --- | ------- | --- | --- | --- |

Chapter 4. Application of CPE algorithms to reaction systems 91
Burgos-Sol´orzano et al. (2004) study the minimization of the Gibbs energy using a
validation tool, which guarantees determining the global minimum. The only time they
reported is 120 ms for the validation tool calculations [Sun Blade 1000 Model 1600
(600 MHz) workstation]. In our work we spent 1.48 ms with the successive substitution
and 1.30 ms with the combined algorithm for the complete calculations (initialization,
convergence of single phase, stability analysis, convergence of two-phase system and
| final stability | analysis). |     |     |     |     |     |
| --------------- | ---------- | --- | --- | --- | --- | --- |
| 3               |            |     |     | 3   |     |     |
0
0
| 3   |     |     |         | 3   |     |     |
| --- | --- | --- | ------- | --- | --- | --- |
|     |     |     | )rorre( | −   |     |     |
)rorre( −
| 6   |            |       |     | 6       |            |       |
| --- | ---------- | ----- | --- | ------- | ---------- | ----- |
| −   |            |       |     | −       |            |       |
| 01  |            |       | 01  |         |            |       |
| gol |            |       | gol |         |            |       |
| 9   |            |       |     | 9       |            |       |
| −   |            |       |     | −       |            |       |
| 12  |            |       |     | 12      |            |       |
| −   |            |       |     | −       |            |       |
| 15  |            |       |     | 15      |            |       |
| − 0 | 4 8        | 12 16 | 20  | − 0 1 2 | 3 4 5      | 6 7 8 |
|     | Iterations |       |     |         | Iterations |       |
|     | (a)        |       |     |         | (b)        |       |
10
8
snoitareti
6
pool
4
rennI
2
0
|     |     | 0 4   | 8              | 12 16 | 20  |     |
| --- | --- | ----- | -------------- | ----- | --- | --- |
|     |     | Outer | loop iteration | index |     |     |
(c)
Figure 4.22: Convergence in cyclohexane synthesis for benzene/hydrogen ratio equal to
1:3.05 at 500 K and 30 atm: (a) successive substitution algorithm, (b) combined
algorithm, (c) inner loop (Newton) iterations per outer loop non-ideality updates
|     | [Q-function | minimization | ( ), | V ( ), VL | ( )]. |     |
| --- | ----------- | ------------ | ---- | --------- | ----- | --- |

92 Chapter 4. Application of CPE algorithms to reaction systems
Methanol synthesis
•
Castier et al. (1989) reported iteration numbers for the three-phase synthesis. Initial-
ization of L, VL and VLL required 5 iterations with 1 GDEM step, 10 iterations with
2 GDEM steps, and 12 iterations with 2 GDEM steps respectively (the third GDEM
step was not needed for the three-phase convergence). For the full convergence of L,
VL and VLL, the Murray iterations were 3, 4 and 1 respectively. In this work, 10
iterations were required for initialization. For the CPE calculations with the successive
substitution algorithm, we had 54 outer loop iterations (149 Newton iterations) for V,
27 outer loop iterations (78 Newton iterations) for VL and 22 outer loop iterations (60
Newton iterations) for VLL. With the combined algorithm, all phases required 3 outer
loop iterations (with 19 Newton iterations for V, 18 for VL and 16 for VLL) and 4, 5
and 4 modified RAND additional iterations for V, VL and VLL respectively.
PPOFAG and OLLFAG transesterification with methanol
•
For the two transesterification systems mentioned in Anikeev (2014) there were no
pertinent data to compare. The only equilibrium results shown in Anikeev (2014) are
for a single-vapor phase. What is worth mentioning here is that a relatively large
number of iterations correspond to the first outer loop iteration (Figures 4.24c and
4.25c, 11 and 18 respectively). This happens because Q-function was minimized with
the assumption of a single vapor phase. When this vapor phase was brought in the
nested-loop procedure, at some point, the compositions of the phase matched better
to a liquid phase. The phase was changed to liquid and the calculations continued.
Subsequent calculations (LL and VLL) appear to be fast for both algorithms.
4.4 Conclusions
The non-stoichiometric algorithms introduced in Chapter 3 were first applied to systems
studied in the literature. Calculations were made for the VLE, LLE or VLLE of three- to
seven-component systems with one or two reactions. The same general algorithms were
used for all the cases without exceptions and there was no issue excluding components
from different phases (e.g. non-volatile oxydimethanol in the formaldehyde/water mixture).
Comparison with the published results show that the algorithms can be successfully used
for CPE calculations. Moreover, the algorithms could perform well for more complex
mixtures, such as in the transesterification of two different triglyceride with methanol,
involving nine components, five reactions and up to three phases.
Apart from CPE calculations at specified temperature, pressure and feed composition, it
was also possible to examine the effect of various factors that could affect equilibrium: the
presence of inert in MTBE synthesis, temperature dependence in the chemical equilibrium
constant in propene hydration, and combination of a two-reaction synthesis into a single
reaction in TAME synthesis. Although no published calculations were available for

Chapter 4. Application of CPE algorithms to reaction systems 93
| 4       |            |       | 4       |            |      |     |
| ------- | ---------- | ----- | ------- | ---------- | ---- | --- |
| 0       |            |       | 0       |            |      |     |
| )rorre( |            |       | )rorre( |            |      |     |
| 4       |            |       | 4       |            |      |     |
| −       |            |       | −       |            |      |     |
| 01      |            |       | 01      |            |      |     |
| gol 8   |            |       | gol 8   |            |      |     |
| −       |            |       | −       |            |      |     |
| 12      |            |       | 12      |            |      |     |
| −       |            |       | −       |            |      |     |
| 16      |            |       | 16      |            |      |     |
| −       |            |       | −       |            |      |     |
| 0 8 16  | 24 32 40   | 48 56 | 0       | 2 4 6      | 8 10 | 12  |
|         | Iterations |       |         | Iterations |      |     |
|         | (a)        |       |         | (b)        |      |     |
10
8
snoitareti
6
pool
4
rennI
2
0
|     | 0   | 8 16 24              | 32 40 | 48 56 |     |     |
| --- | --- | -------------------- | ----- | ----- | --- | --- |
|     |     | Outer loop iteration | index |       |     |     |
(c)
Figure 4.23: Convergence in methanol synthesis in the presence of n-octadecane at 473.15
K and 101.3 bar: (a) successive substitution algorithm, (b) combined algorithm, (c) inner
loop (Newton) iterations per outer loop non-ideality updates [Q-function minimization
|     | ( ), V | ( ), VL ( | ), VLL ( | )]. |     |     |
| --- | ------ | --------- | -------- | --- | --- | --- |

94 Chapter 4. Application of CPE algorithms to reaction systems
| 4       |            |         | 4   |            |      |
| ------- | ---------- | ------- | --- | ---------- | ---- |
| 0       |            |         | 0   |            |      |
| )rorre( |            | )rorre( |     |            |      |
| 4       |            |         | 4   |            |      |
| −       |            |         | −   |            |      |
| 01      |            | 01      |     |            |      |
| gol 8   |            | gol     | 8   |            |      |
| −       |            |         | −   |            |      |
| 12      |            |         | 12  |            |      |
| −       |            |         | −   |            |      |
| 16      |            |         | 16  |            |      |
| −       |            |         | −   |            |      |
| 0 3     | 6 9        | 12 15   | 0 2 | 4 6        | 8 10 |
|         | Iterations |         |     | Iterations |      |
|         | (a)        |         |     | (b)        |      |
12
10
snoitareti
8
pool 6
rennI
4
2
0
|     | 0   | 3 6                  | 9 12  | 15  |     |
| --- | --- | -------------------- | ----- | --- | --- |
|     |     | Outer loop iteration | index |     |     |
(c)
Figure 4.24: Convergence in PPOFAG transesterification with methanol for
PPOFAG/methanol ratio equal to 1:3 at 450 K and 1 atm: (a) successive substitution
algorithm, (b) combined algorithm, (c) inner loop (Newton) iterations per outer loop
non-ideality updates [Q-function minimization ( ), L ( ), LL ( ), VLL ( )].

Chapter 4. Application of CPE algorithms to reaction systems 95
| 4       |            |      |         | 4   |            |      |     |
| ------- | ---------- | ---- | ------- | --- | ---------- | ---- | --- |
| 0       |            |      |         | 0   |            |      |     |
| )rorre( |            |      | )rorre( |     |            |      |     |
| 4       |            |      |         | 4   |            |      |     |
| −       |            |      |         | −   |            |      |     |
| 01      |            |      | 01      |     |            |      |     |
| gol 8   |            |      | gol     | 8   |            |      |     |
| −       |            |      |         | −   |            |      |     |
| 12      |            |      |         | 12  |            |      |     |
| −       |            |      |         | −   |            |      |     |
| 16      |            |      |         | 16  |            |      |     |
| −       |            |      |         | −   |            |      |     |
| 0 2     | 4 6        | 8 10 | 12      | 0 2 | 4 6        | 8 10 | 12  |
|         | Iterations |      |         |     | Iterations |      |     |
|         | (a)        |      |         |     | (b)        |      |     |
20
16
snoitareti
12
pool
8
rennI
4
0
|     |     | 0 2   | 4 6            | 8 10  | 12  |     |     |
| --- | --- | ----- | -------------- | ----- | --- | --- | --- |
|     |     | Outer | loop iteration | index |     |     |     |
(c)
Figure 4.25: Convergence in OLLFAG transesterification with methanol for
OLLFAG/methanol ratio equal to 1:3 at at 500 K and 1 atm: (a) successive substitution
algorithm, (b) combined algorithm, (c) inner loop (Newton) iterations per outer loop
non-ideality updates [Q-function minimization ( ), L ( ), LL ( ), VLL ( )].

96 Chapter 4. Application of CPE algorithms to reaction systems
comparisons, these factors affected the equilibrium of the mixtures as expected.
Minimization of function Q provided initial estimates of good quality for the Lagrange mul-
tipliers method and we never encountered cases of divergence or oscillations. Furthermore,
stability analysis could always identify a good estimate of the new phase without the need
of re-initialization with function Q. Actually, it was observed that re-initialization with
the new phase might lead to worse estimates because during the Q-function minimization,
unlike in stability analysis, fugacity or activity coefficients are not utilized.
Speedandconvergencebehaviorwereinvestigatedforthetwonon-stoichiometricalgorithms.
The combined algorithm converged to the solution with fewer iterations than the first-order
successive substitution algorithm. Each outer loop iteration of the Lagrange multipliers
method involved on average 2-4 inner loop (Newton) iterations, which reduced to 1-2
close to the solution. In the combined algorithm, successive substitution refines the initial
estimates from the Q-function minimization and full convergence needs only 2-5 additional
modifiedRANDsteps. TakingintoaccountthattheLagrangemultipliersmethodhaslinear
and the modified RAND method quadratic convergence, both require a reasonable number
of iterations and they are much faster than reported CPU times in different publications.
There have been cases where the algorithms in this work exhibited comparable CPU times
but in general the combined algorithm appears to be more efficient, while the Gibbs energy
monitoring during modified RAND steps is improving the robustness of calculations. Due
to the modified RAND method, we propose the combined algorithm as an efficient and
reliable approach for equilibrium calculations in multiphase reaction systems.
Finally, calculations were not compared with experimental data for the systems of this
chapter. The focus of the study was the structure and performance of the algorithms,
without concluding which model is more suitable to describe a reaction system. The use
of better models will result in more accurate calculations/predictions. However, it should
be mentioned that more complex models are computationally expensive and this could be
reflected in increased CPU times.

| C H A | P T E R |     |     |     |     |
| ----- | ------- | --- | --- | --- | --- |
5
Calculation of CPE
in electrolyte systems
Various models have been used to describe electrolyte behavior in solutions. One of the
first successful attempts to theoretically formulate non-ideality in an electrolyte solution is
attributed to Debye and Hu¨ckel (1923). Usually, when we refer to “Debye-Hu¨ckel” activity
coefficients, we need to clarify how many parameters are included in the equation. There
can be up to three ion independent parameters that depend on temperature and solvent
properties. The limiting Debye-Hu¨ckel law has one parameter and extended Debye-Hu¨ckel
equations utilize the two additional parameters. However, its use is limited to low values
| of ionic | strength. | Ionic strength | in phase | k is defined | as: |
| -------- | --------- | -------------- | -------- | ------------ | --- |
1 NC
X z2m
|     |     |     | I = |     | (5.1) |
| --- | --- | --- | --- | --- | ----- |
|     |     |     | k   | 2 i | ik    |
i=1
where:
| I   | ionic strength | in phase | k   |     |     |
| --- | -------------- | -------- | --- | --- | --- |
k
| z   | charge of | component | i   |     |     |
| --- | --------- | --------- | --- | --- | --- |
i
| m   | molality | of component | i in phase | k   |     |
| --- | -------- | ------------ | ---------- | --- | --- |
ik
At higher electrolyte concentrations more complicated models are applicable, such as the
Pitzer’s model. It was originally proposed by Pitzer (1973) and it is worth mentioning one
of its extended variants presented in Felmy and Weare (1986). Felmy and Weare (1986)
show a number of different contributing terms to the activity coefficient: a Debye-Hu¨ckel
based term and binary as well as ternary interactions between cations, anions and neutral
solutes. Binary and ternary interaction parameters are regressed based on experimental
data. Less complex Pitzer based equations might omit the ternary interaction parameters
and include their own analysis predicting interaction parameters when experimental data
| are scarce | (Edwards | et al., | 1978). |     |     |
| ---------- | -------- | ------- | ------ | --- | --- |
A number of equilibrium calculation methods based on the law of mass action have

| 98  |     |     |     |     | Chapter |     | 5. Calculation |     | of CPE | in electrolyte | systems |
| --- | --- | --- | --- | --- | ------- | --- | -------------- | --- | ------ | -------------- | ------- |
been published, such as PHREEQC (Parkhurst and Appelo, 2013), used also in reactive
transport processes. A more detailed list of similar methods is mentioned in Leal et al.
(2016b). The authors followed the approach of Gibbs energy minimization to calculate
geological system equilibrium and integrated their method in Reaktoro (C++ and Python
framework combining chemical equilibrium and/or kinetics for chemically reactive process
modeling, reaktoro.org). Moreover, Thomsen (1997) employed reaction extents in a
second-order single phase procedure using the chemical equilibrium constants of the
reactions. Finally, Xiao et al. (1989) developed the first-order KZ algorithm and applied it
to the VLE of water/ammonia/carbon dioxide and Gautam and Seider (1979c) used the
original single phase ideal RAND in an aqueous solution of sulfur dioxide with the ideal
system approximation.
The non-stoichiometric algorithms developed in this work are applied to multiphase
chemicalequilibriuminvolvingelectrolytereactions. Electroneutralitymustbeincorporated
in the working equations due to electrolytes in the system. In general, cases of interest
include weak electrolytes, ion speciation and reactions with minerals. CPE calculation
in electrolyte systems is useful for geochemistry modeling such as underground carbon
| dioxide | sequestration.    |     |     |     |     |        |     |              |     |     |     |
| ------- | ----------------- | --- | --- | --- | --- | ------ | --- | ------------ | --- | --- | --- |
| 5.1     | Electroneutrality |     |     |     |     | in CPE |     | calculations |     |     |     |
Dissociation of an electrolyte can be viewed as a chemical reaction. In the general case we
have a mixture of N electrolytes that dissociate according to the reactions:
R
|     |     |     |     | X     | Y     | (cid:10) y | X (xr)+ | +x  | Y (yr)− |     |     |
| --- | --- | --- | --- | ----- | ----- | ---------- | ------- | --- | ------- | --- | --- |
|     |     |     |     | r(yr) | r(xr) | r          | r       | r   | r       |     |     |
(5.2)
|     |     |     |     |     |     | r = 1,...,N |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
R
where:
X(xr)+
|        | cation | with | charge | +x  | in                | dissociation | reaction |     | r   |     |     |
| ------ | ------ | ---- | ------ | --- | ----------------- | ------------ | -------- | --- | --- | --- | --- |
| r      |        |      |        |     | r                 |              |          |     |     |     |     |
| Y(yr)− | anion  | with | charge |     | y in dissociation |              | reaction |     | r   |     |     |
| r      |        |      |        |     | r                 |              |          |     |     |     |     |
−
|     |     |     |     |     |     | X(xr)+ | Y(yr)− |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | ------ | --- | --- | --- | --- |
For convenience, we assume that ions and are unique for each dissociation r.
|     |     |     |     |     |     | r   |     | r   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The number of elements is N = N N = 3N N = 2N . If the elements are chosen
|     |     |     |     | E   | C   | R   | R   | R   | R   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | −   |     | −   |     |     |     |     |
as the ions, the formula matrix and stoichiometric matrix of the hypothetical system are
given by:

| Chapter | 5. Calculation |     | of    | CPE   | in    | electrolyte |         | systems |         |     |     |           | 99  |
| ------- | -------------- | --- | ----- | ----- | ----- | ----------- | ------- | ------- | ------- | --- | --- | --------- | --- |
|         |                |     | X     | Y     |       |             | X (xr)+ |         | Y (yr)− |     |     |           |     |
|         |                |     |       | r(yr) | r(xr) |             | r       |         | r       |     |     |           |     |
|         |                |     | ··. · |       |       | ··. ·       |         |         |         | ··. | ·   |           |     |
|         |                |    | .     | . .   |       | .           |         | . .     | . .     | .   |    | . .       |     |
|         |                |     | .     | .     |       | .           |         | .       | .       | .   |     | .         |     |
|         |                |    |       |       |       |             |         |         |         |     |    |           |     |
|         |                |     | . .   |       |       |             |         |         |         | . . |     |           |     |
|         |                |    | .     | y     |       |             | 1       |         | 0       | .   |  X | ( x r ) + |     |
|         | A              | =  |       |       | r     |             |         |         |         |     |    | r         |     |
|         |                |    |       |       |       | ···         |         |         |         |     |    |           |     |
|         |                |    | . .   |       |       |             |         |         |         | . . |    |           |     |
|         |                |    | .     | x     |       |             | 0       |         | 1       | .   |  Y | ( yr ) −  |     |
|         |                |     |       |       | r     |             |         |         |         |     |     | r         |     |
|         |                |    |       |       |       | ··. ·       |         |         |         |     |    |           |     |
|         |                |    | . .   | . .   |       | .           |         | . .     | . .     | . . |    | . .       |     |
|         |                |     | .     | .     |       | .           |         | .       | .       | .   |     | .         |     |
(5.3)
|     |     |      | X   | Y     |       |      | X (xr)+ |     | Y (yr)− |      |            |     |     |
| --- | --- | ---- | --- | ----- | ----- | ---- | ------- | --- | ------- | ---- | ---------- | --- | --- |
|     |     |      |     | r(yr) | r(xr) |      | r       |     | r       |      |            |     |     |
|     |     | ··.· |     |       |       | ··.· |         |     |         | ··.· |            |     |     |
|     |     |     | .   | . .   |       | .    | . .     |     | . .     | .    |           | . . |     |
|     |     |      | .   | .     |       | .    | .       |     | .       | .    |            | .   |     |
|     | NT  |     | .   |       |       |      |         |     |         | .    |           |     |     |
|     |     | =   | . . | 1     |       |      | y       |     | x       | . .  |  reaction | r   |     |
|     |     |     |     |       |       |      | r       |     | r       |      |           |     |     |
|     |     |      |     | −.    |       | ··.· |         |     |         |      |            |     |     |
|     |     |     | .   |       |       |      | .       |     | .       | .    |           | .   |     |
|     |     |      | . . | . .   |       | . .  | . .     |     | . .     | . .  |            | . . |     |
An additional equation that is supposed to be satisfied in such systems is the electroneu-
trality equation. We start with N uncharged electrolytes with net charge equal to zero,
R
which should not change after all dissociation equilibria have been established. In other
| words, at | equilibrium: |     |     |     |       |     |     |          |     |       |     |     |       |
| --------- | ------------ | --- | --- | --- | ----- | --- | --- | -------- | --- | ----- | --- | --- | ----- |
|           |              |     | NR  |     |       |     | NR  |          |     |       |     |     |       |
|           |              |     | X   | (n  | )(+x  | )+  | X   | (n       | )(  | y ) = | 0   |     | (5.4) |
|           |              |     |     |     |       | r   |     |          |     | r     |     |     |       |
|           |              |     |     | Xr  | (xr)+ |     |     | Yr (yr)− | −   |       |     |     |       |
|           |              |     | r=1 |     |       |     | r=1 |          |     |       |     |     |       |
The material balance in non-stoichiometric methods is given by Eq. 3.7:
NP
|     |     |     |     |     |     | A X | n   | = b |     |     |     |     | (5.5) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
k
k=1
Eq. 5.4 could be included as an additional row in the matrix and vector of the material
| balance constraints |     |     | as (Appendix |     | B): |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                     |     |     |              |     |    |    |     |    |    |     |     |     |     |
|                     |     |     |              |     |     | A   | NP  |     | b   |     |     |     |     |
X
|     |     |     |     |     |     |     | n   | =   |     |     |     |     | (5.6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     |     |     |    |    | k   |    |    |     |     |     |       |
|     |     |     |     |     |     | A   |     |     | 0   |     |     |     |       |
el k=1
where:
|     |     |     |      |     |       |       |     | (xr)+ |     | (yr)− |      |     |       |
| --- | --- | --- | ---- | --- | ----- | ----- | --- | ----- | --- | ----- | ---- | --- | ----- |
|     |     |     |      | X   |       | Y     |     | X     |     | Y     |      |     |       |
|     |     |     | h··· |     | r(yr) | r(xr) | ··· | r     |     | r     | ···i |     |       |
|     |     | A   | =    |     |       |       |     |       |     |       |      |     | (5.7) |
|     |     | el  |      |     | 0     |       |     | x     |     | y     |      |     |       |
|     |     |     |      |     |       |       |     |       | r   | r     |      |     |       |
|     |     |     | ···  |     |       |       | ··· |       |     | −     | ···  |     |       |
However, this row can be obtained as a linear combination of the rows that already exist

| 100 |     |     | Chapter | 5. Calculation |     | of CPE | in electrolyte | systems |
| --- | --- | --- | ------- | -------------- | --- | ------ | -------------- | ------- |
(xr)+
in the formula matrix of Eq. 5.3. If we multiply the rows of X with x , the rows of
|     |     |     |     |     |     | r   | r   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Y (yr)+ with y and then add all the rows, we will get Eq. 5.4. Therefore, this framework
| r   | r   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
already takes into account the electroneutrality equation. Reaching equilibrium does not
only mean that the material balance is satisfied. It also implies that the change of the
component mole numbers follows the way the reactions are written. The formula matrix
“hides” reaction information because it is not independent of the stoichiometric matrix
(Eq. 3.20). In fact, since the reactions are balanced out and there is no production or
consumption of charge (e.g. as in redox half reactions), if the net charge in the feed is
zero, the net charge at equilibrium will be also zero. A similar analysis can be made when
the different dissociating electrolytes X Y share common ions.
|     |     |     |     | r(yr) r(xr) |     |     |     |     |
| --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
The way electroneutrality is satisfied by the the formula matrix in Eq. 5.6 does not prevent
individual phases from being charged. It only ensures that the net charge of all the phases
at equilibrium will be zero. Eq. 5.4 should be satisfied for every phase where charged
particles appear. The main assumption is that charged components are excluded from
all phases except for the solvent phase (in this work the aqueous phase). In this case,
PNP
the entries of the vector n for charged components are actually their total mole
k=1 k
numbers in the only phase they appear. The models in this work do not account for this
inherently. Instead, charged particles are artificially excluded from non-solvent phases to
guarantee that phase electroneutrality coincides with overall electroneutrality in Eq. 5.6.
The reason why Eq. 5.6 was presented with the sum of mole numbers of all the phases,
was to keep the material balance in the form used for the non-electrolyte systems of the
previous chapter.
| 5.2 Infinite | dilution |     | reference |     | state |     |     |     |
| ------------ | -------- | --- | --------- | --- | ----- | --- | --- | --- |
In the expression of liquid phase chemical potential, pure component reference state
is usually selected if a component can be condensed at the system temperature. This
is particularly favorable if the behavior of the component does not deviate much from
Raoult’s law. On the other hand, when the component is non-condensable at the system
temperature or it is not described adequately by the pure component limiting law, the
infinite dilution (Henry’s law based) reference state is often preferred:
f◦
|     |     |     | =   | H (T,p,n | )     |     |     | (5.8) |
| --- | --- | --- | --- | -------- | ----- | --- | --- | ----- |
|     |     |     | ik  | ik       | sol,k |     |     |       |
and
µ◦
|     |     |     |     | = µ˜ (T,p,n | )     |     |     | (5.9) |
| --- | --- | --- | --- | ----------- | ----- | --- | --- | ----- |
|     |     |     | ik  | ik          | sol,k |     |     |       |
where:
| H Henry’s | constant | of component |     | i in phase | k   |     |     |     |
| --------- | -------- | ------------ | --- | ---------- | --- | --- | --- | --- |
ik

| Chapter | 5. Calculation |      | of CPE  | in  | electrolyte |     | systems |     |     |     | 101 |
| ------- | -------------- | ---- | ------- | --- | ----------- | --- | ------- | --- | --- | --- | --- |
| n       | solvent        | mole | numbers | in  | phase       | k   |         |     |     |     |     |
sol,k
µ˜ infinite dilution chemical potential of component i in phase k
ik
The dependence of Henry’s constant on pressure is usually expressed as:
|     |     |     |      |     | ¯∞    | !   |     | " ¯∞(p |      | ps # |        |
| --- | --- | --- | ---- | --- | ----- | --- | --- | ------ | ---- | ---- | ------ |
|     |     |     |      |     | Z p V |     |     | V      |      | )    |        |
|     |     | H   | = Hs | exp | ik    | dp  | Hs  | exp    | ik − | sol  | (5.10) |
|     |     | ik  | ik   |     |       |     | ik  |        |      |      |        |
|     |     |     |      |     | ps RT |     | ≈   |        | RT   |      |        |
sol
where:
Hs
|     | saturation |     | Henry’s | constant | of  | component |     | i in phase | k   |     |     |
| --- | ---------- | --- | ------- | -------- | --- | --------- | --- | ---------- | --- | --- | --- |
ik
¯∞
V infinite dilution partial molar volume of component i in phase k
ik
| ps  | solvent | vapor | pressure |     |     |     |     |     |     |     |     |
| --- | ------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
sol
In such mixtures the treatment is different for solvents and solutes. Solvents follow the
pure component reference state and solutes the infinite dilution reference state. Henry’s
constants for specific solvents can be found in the literature. Nevertheless, it is difficult to
predict the overall Henry’s constant in the case of mixed solvents only from pure solvent
Henry’s constants (Michelsen and Mollerup, 2007). For this reason it is preferable to
consider one component as the solvent and the rest as the solutes. Similar to the symmetric
activity coefficient defined by Eq. 2.47 in the pure component reference state, using the
infinite dilution reference state we define the asymmetric activity coefficient:
f ˆ
ik
|     |     |     |     |     | γ˜  |     |     |     |     |     | (5.11) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik
|     |     |     |     |     |     | ≡ x | H   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ik ik
where:
| γ˜  | asymmetric |     | activity | coefficient |     | of component |     | i in | phase | k   |     |
| --- | ---------- | --- | -------- | ----------- | --- | ------------ | --- | ---- | ----- | --- | --- |
ik
| Therefore, | fugacity | and | chemical |     | potential | expressions |     | become: |     |     |     |
| ---------- | -------- | --- | -------- | --- | --------- | ----------- | --- | ------- | --- | --- | --- |
ˆ
|     |     |     |     |     | f   | = x | γ˜ H  |     |     |     | (5.12) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ------ |
|     |     |     |     |     | ik  | ik  | ik ik |     |     |     |        |
and
|           |     |      |            | µ   | = µ˜ | +RT      | ln(x  | γ˜ )  |     |     | (5.13) |
| --------- | --- | ---- | ---------- | --- | ---- | -------- | ----- | ----- | --- | --- | ------ |
|           |     |      |            |     | ik   | ik       |       | ik ik |     |     |        |
| Comparing | Eq. | 2.48 | with 5.12, | we  | can  | conclude | that: |       |     |     |        |
H
ik
|     |     |     |     |     | γ   | = γ˜ |     |     |     |     | (5.14) |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | ik   | ik  |     |     |     |        |
f
ik
As the mole fraction of component i approaches 0, the asymmetric activity coefficient

| 102 |     |     |     |     | Chapter | 5.  | Calculation |     | of CPE | in electrolyte | systems |
| --- | --- | --- | --- | --- | ------- | --- | ----------- | --- | ------ | -------------- | ------- |
γ˜ approaches 1 according to the definition of Eq. 5.11. However, the infinite dilution
ik
activity coefficient of component i under the symmetric convention is usually not 1 but
given by:
|     |     |     |     |       |     |         |     | !   |     |     |        |
| --- | --- | --- | --- | ----- | --- | ------- | --- | --- | --- | --- | ------ |
|     |     |     |     |       |     |         |     | H   | H   |     |        |
|     |     |     | γ∞  |       |     |         |     | ik  |     | ik  |        |
|     |     |     |     | = lim | γ   | = lim   | γ˜  |     | =   |     | (5.15) |
|     |     |     | ik  |       | ik  |         | ik  | f   | f   |     |        |
|     |     |     |     | x ik  | →0  | x ik →0 |     | ik  | ik  |     |        |
where:
γ∞ symmetric infinite dilution activity coefficient of component i in phase k
ik
| As a result, | from | Eq. | 5.14: |     |     |     |     |     |     |     |     |
| ------------ | ---- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
γ
ik
|     |     |     |     |     |     | γ˜ = |     |     |     |     | (5.16) |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | ik   | γ∞  |     |     |     |        |
ik
| Comparing | Eq. | 2.49 | with 5.13, | using | Eq.  | 5.15:     |      |     |     |     |        |
| --------- | --- | ---- | ---------- | ----- | ---- | --------- | ---- | --- | --- | --- | ------ |
|           |     |      |            |       | µ˜ = | µpure +RT | lnγ∞ |     |     |     | (5.17) |
ik
|     |     |     |     |     |     | ik  |     | ik  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
When we have more than one solvent, the infinity dilution activity coefficient depends on
the composition of these solvents. In the electrolyte systems presented in the following
| section, | we assume | that | only | water | is  | the solvent. | Therefore: |     |     |     |     |
| -------- | --------- | ---- | ---- | ----- | --- | ------------ | ---------- | --- | --- | --- | --- |
  ∂lnγ∞!
|     |     |     |     |     |     | ik  | =   | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂n
|     |     |     |     |     |     | qk          | T,p |     |     |     | (5.18) |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | q = 1,...,N |     |     |     |     |        |
C
Two further variations of the infinite dilution reference state can be found in the litera-
ture:
| Unit | molality | reference |     | state |     |     |     |     |     |     |     |
| ---- | -------- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
•
| Molality | is  | a different | measure |     | of concentration |     | defined |     | as: |     |     |
| -------- | --- | ----------- | ------- | --- | ---------------- | --- | ------- | --- | --- | --- | --- |
n
|     |     |     |     |     | m   | =   | ik  |     |     |     | (5.19) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik
n M
|     |     |     |     |     |     |     | sol,k sol,k |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
and it shows the mole numbers of a solute dissolved per kg of solvent. We can express
| mole | fractions | as functions |     | of   | molality: |       |             |     |     |             |        |
| ---- | --------- | ------------ | --- | ---- | --------- | ----- | ----------- | --- | --- | ----------- | ------ |
|      |           |              | n   |      | n         | n     | M           |     |     |             |        |
|      |           | x            | =   | ik = |           | ik    | sol,k sol,k | =   | m x | M           | (5.20) |
|      |           |              | ik  |      |           |       |             |     | ik  | sol,k sol,k |        |
|      |           |              | n   |      | n M       |       | n           |     |     |             |        |
|      |           |              |     | t,k  | sol,k     | sol,k | t,k         |     |     |             |        |

| Chapter | 5. Calculation | of  | CPE in | electrolyte |     | systems |     | 103 |
| ------- | -------------- | --- | ------ | ----------- | --- | ------- | --- | --- |
where:
| M   | solvent | molar | mass in phase |     | k   |     |     |     |
| --- | ------- | ----- | ------------- | --- | --- | --- | --- | --- |
sol,k
| x   | solvent | mole fraction | in  | phase | k   |     |     |     |
| --- | ------- | ------------- | --- | ----- | --- | --- | --- | --- |
sol,k
| Using | Eq. 5.13: |     |     |     |     |     |     |     |
| ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
m (γ˜ x )
|     |     | µ = [µ˜ | +RT | ln(M | m◦)]+RT | ln ik | ik sol,k | (5.21) |
| --- | --- | ------- | --- | ---- | ------- | ----- | -------- | ------ |
|     |     | ik      | ik  |      | sol,k   |       |          |        |
m◦
We define:
|     |     |     | µ˜m | = µ˜ | +RT | ln(M m◦) |     | (5.22) |
| --- | --- | --- | --- | ---- | --- | -------- | --- | ------ |
|     |     |     | ik  | ik   |     | sol,k    |     |        |
and
|     |     |     |     | γ˜m | = x   | γ˜  |     | (5.23) |
| --- | --- | --- | --- | --- | ----- | --- | --- | ------ |
|     |     |     |     | ik  | sol,k | ik  |     |        |
where:
µ˜m chemical potential of component i in phase k at unit molality
ik
γ˜m asymmetric molality activity coefficient of component i in phase k
ik
| m◦      | unit         | molality  |          |       |     |          |     |        |
| ------- | ------------ | --------- | -------- | ----- | --- | -------- | --- | ------ |
| Finally | the chemical | potential | becomes: |       |     |          |     |        |
|         |              |           |          |       |     | m γ˜m    |     |        |
|         |              |           | µ        | = µ˜m | +RT | ln ik ik |     | (5.24) |
ik
|     |     |     |     | ik  |     | m◦  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
This expression is useful when the activities of solutes are expressed as:
γ˜m
m
|     |     |     |     | α   | =   | ik ik |     | (5.25) |
| --- | --- | --- | --- | --- | --- | ----- | --- | ------ |
ik
m◦
| Unit molarity |     | reference | state |     |     |     |     |     |
| ------------- | --- | --------- | ----- | --- | --- | --- | --- | --- |
•
| Molarity | is formally | defined | as: |     |     |     |     |     |
| -------- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
n
ik
|     |     |     |     |     | c = |     |     | (5.26) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | ik  | V   |     |        |
k
and shows how many moles are dissolved per unit volume of solution. Instead of the
S.I. unit, the unit “M” is more common, defined as mol/L. Mole fractions are found as:

| 104 |     |     |     |     | Chapter | 5.  | Calculation |      | of CPE | in electrolyte |     | systems |
| --- | --- | --- | --- | --- | ------- | --- | ----------- | ---- | ------ | -------------- | --- | ------- |
|     |     |     |     |     | n       |     | n V         | c    |        |                |     |         |
|     |     |     |     |     |         | ik  | ik          | k ik |        |                |     |         |
|     |     |     |     |     | x =     | =   |             | =    |        |                |     | (5.27)  |
ik
|     |     |     |     |     | n   |     | V n   | c   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | t,k | k t,k | t,k |     |     |     |     |
where:
| c   | molarity |     | of component |     | i in | phase | k   |     |     |     |     |     |
| --- | -------- | --- | ------------ | --- | ---- | ----- | --- | --- | --- | --- | --- | --- |
ik
| c   | total | molarity |     | in phase | k   |     |     |     |     |     |     |     |
| --- | ----- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
t,k
| Molality | and | molarity |     | are related | through: |     |     |     |     |     |     |     |
| -------- | --- | -------- | --- | ----------- | -------- | --- | --- | --- | --- | --- | --- | --- |
c
|     |     |     |     |     | m = |     | ik  |     |     |     |     | (5.28) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ik
|     |     |     |     |     |     | ρ   | PNC | c M  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     |     |     |     |     |     | k   | i=1 | ik i |     |     |     |     |
−
i6=sol
where:
| M   | molar | mass | of  | component |     | i   |     |     |     |     |     |     |
| --- | ----- | ---- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
i
| c   | solvent |     | molarity | in  | phase k |     |     |     |     |     |     |     |
| --- | ------- | --- | -------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
sol,k
| ρ   | density |     | of phase | k   |     |     |     |     |     |     |     |     |
| --- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
k
| Using | Eq. 5.13: |     |     |     |       |     |     |      |          |        |     |        |
| ----- | --------- | --- | --- | --- | ----- | --- | --- | ---- | -------- | ------ | --- | ------ |
|       |           |     |     |     |       |     |     |     |          |        |    |        |
|       |           |     | "   |     |       | #   |     |      |          |        |     |        |
|       |           |     |     |     | c◦M   |     |     | c    | γ˜ x     | ρ      |     |        |
|       |           |     |     |     | sol,k |     |     |  ik | ik sol,k | sol,k  |    |        |
|       |           | µ = | µ˜  | +RT | ln    | +RT | ln |      |          |        |    | (5.29) |
|       |           | ik  | ik  |     | ρ     |     |     | c◦  | PNC      |        |     |        |
|       |           |     |     |     | sol,k |     |     | ρ    |          | c      | M  |        |
|       |           |     |     |     |       |     |     |      | k        | i=1 ik | i   |        |
|       |           |     |     |     |       |     |     |      | − i6=sol |        |     |        |
We define:
c◦M
|     |     |     |     |     | µ˜c  |     |     | sol,k |     |     |     |        |
| --- | --- | --- | --- | --- | ---- | --- | --- | ----- | --- | --- | --- | ------ |
|     |     |     |     |     | = µ˜ | +RT | ln  |       |     |     |     | (5.30) |
|     |     |     |     |     | ik   | ik  |     | ρ     |     |     |     |        |
sol,k
and
x ρ
|     |     |     |     |     | γ˜c = | sol,k | sol,k | γ˜  |     |     |     | (5.31) |
| --- | --- | --- | --- | --- | ----- | ----- | ----- | --- | --- | --- | --- | ------ |
ik
|     |     |     |     |     | ik ρ | PNC | c   | M    |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | --- |
|     |     |     |     |     |      | k   | i=1 | ik i |     |     |     |     |
−
i6=sol
| Chemical | potentials |     | become: |     |     |     |     |     |     |     |     |     |
| -------- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
c γ˜c
ik
|     |     |     |     |     | µ = | µ˜c +RT | ln  | ik  |     |     |     | (5.32) |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | ik  | ik      |     | c◦  |     |     |     |        |
where:
µ˜c
|     | chemical |     | potential |     | of component |     | i in phase | k at | unit | molarity |     |     |
| --- | -------- | --- | --------- | --- | ------------ | --- | ---------- | ---- | ---- | -------- | --- | --- |
ik
γ˜c asymmetric molarity activity coefficient of component i in phase k
ik
| ρ   | pure | solvent | density |     | in phase | k   |     |     |     |     |     |     |
| --- | ---- | ------- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
sol,k

| Chapter | 5. Calculation | of  | CPE | in electrolyte |     | systems |     | 105 |
| ------- | -------------- | --- | --- | -------------- | --- | ------- | --- | --- |
c◦
unit molarity
This expression is useful when the activities of solutes are expressed as:
γ˜c
c
|     |     |     |     |     | α   | = ik ik |     | (5.33) |
| --- | --- | --- | --- | --- | --- | ------- | --- | ------ |
ik
c◦
In general the unit molality m◦ and molarity c◦ do not always appear in relationships in
the literature. The only reason they are introduced here is to maintain dimensionless all
the arguments of the logarithms while preserving the general expressions for the molality
| and molarity | chemical           | potentials |     | (Eq. | 5.24       | and 5.32). |                |     |
| ------------ | ------------------ | ---------- | --- | ---- | ---------- | ---------- | -------------- | --- |
| 5.3          | Non-stoichiometric |            |     |      | algorithms |            | in electrolyte |     |
mixtures
| 5.3.1 | Water/ammonia/carbon |     |     |     |     | dioxide | mixture |     |
| ----- | -------------------- | --- | --- | --- | --- | ------- | ------- | --- |
Xiao et al. (1989) included calculations in their work for the VLE of the mixture
H O/NH /CO in the presence of methane and ethane as inerts. Ammonia and car-
| 2   | 3 2 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
bon dioxide dissolve in water and react according to the schemes:
|     |     |     |     |      |          | (cid:10) NH+ +OH− |     |        |
| --- | --- | --- | --- | ---- | -------- | ----------------- | --- | ------ |
|     |     |     | NH  | +H   | O        |                   |     | (5.34) |
|     |     |     |     | 3    | 2        | 4                 |     |        |
|     |     |     |     |      |          | (cid:10) HCO−     | +H+ |        |
|     |     |     | CO  | +H   | O        |                   |     | (5.35) |
|     |     |     |     | 2    | 2        | 3                 |     |        |
|     |     |     |     | HCO− | (cid:10) | CO2− +H+          |     |        |
(5.36)
|     |     |     |     |     | 3    | 3        |     |        |
| --- | --- | --- | --- | --- | ---- | -------- | --- | ------ |
|     |     |     |     | H+  | +OH− | (cid:10) |     |        |
|     |     |     |     |     |      | H        | O   | (5.37) |
2
|     |     |     | NH +HCO− |     | (cid:10) | NH COO− | +H O | (5.38) |
| --- | --- | --- | -------- | --- | -------- | ------- | ---- | ------ |
|     |     |     | 3        |     |          | 2       | 2    |        |
3
The chemical compositions of all components and elements for the electrolyte system is
presented in Table 5.1. The number of elements is N = N N = 11 5 = 6. The
E C R
− −
formula matrix and stoichiometric matrix of the system are given by:

| 106 |     |     |      | Chapter |     | 5.  | Calculation |       | of CPE | in electrolyte | systems |
| --- | --- | --- | ---- | ------- | --- | --- | ----------- | ----- | ------ | -------------- | ------- |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     |      | 2 1     | 0 0 | 0 1 | 2           | 1 1 0 | 0      |                |         |
|     |     |     | 1   | 0       | 0 0 | 0 0 | 0           | 1 1 1 | 0     |                |         |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     | 0   | 1       | 0 0 | 0 0 | 1           | 0 0 0 | 1     |                |         |
|     |     | A   | =   |         |     |     |             |       |       |                |         |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     | 0   | 0       | 1 0 | 0 0 | 0           | 0 1 1 | 1     |                |         |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     |  0 | 0       | 0 1 | 0 0 | 0           | 0 0 0 | 0    |                |         |
|     |     |     |     |         |     |     |             |       |       |                |         |
|     |     |     |      | 0 0     | 0 0 | 1 0 | 0           | 0 0 0 | 0      |                |         |
(5.39)
|     |     |    |     |     |     |     |     |     |     | T  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 1   | 1 0 | 0   | 0 0 | 1   | 1   | 0 0 | 0   |     |
|     |     | −  | −   |     |     |     |     |     |     |     |     |

|     |     |    | 1 0 |     | 1 0 | 0 1 | 0   | 0   | 1 0 | 0  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | −  |     |     |     |     |     |     |     |    |     |
|     |     |    |     | −   |     |     |     |     |     |    |     |
|     | N   | =   | 0 0 | 0   | 0   | 0 1 | 0   | 0   | 1 1 | 0  |     |

|     |     |    |     |     |     |     |     | −   |     |    |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |    | 1 0 | 0   | 0   | 0   | 1 0 | 1   | 0 0 | 0  |     |
|     |     |    |     |     |     |     |     |     |     |    |     |
|     |     |    |     |     |     | −   |     | −   |     |    |     |
|     |     |     | 1   | 1 0 | 0   | 0 0 | 0   | 0   | 1 0 | 1   |     |
|     |     |     | −   |     |     |     |     | −   |     |     |     |
Vapor phase is described by the Soave-Redlich-Kwong equation of state (Soave, 1972)
with all binary interaction parameters k set to zero and liquid phase by the activity
ij
coefficientmodelpresentedinEdwardsetal.(1978)usingnumericalcompositionderivatives.
Chemical equilibrium constants and Henry’s constants were taken from Edwards et al.
(1978), water density and vapor pressure from Dortmund Data Bank (2017), and water
dielectric constant from P´atek et al. (2009). Charged components are considered non-
volatile and the inert hydrocarbons non-soluble in the aqueous phase (Xiao et al., 1989).
Results are compared with Xiao et al. (1989) in Table 5.2 and convergence behavior
is shown in Figure 5.1. Calculations required 2.32 ms with the successive substitution
algorithm and 2.31 ms with the combined algorithm. Similar CPU times show that the
fewer iterations required by the combined algorithm cost more, possibly because of the
matrix inversion and calculations of numerical derivatives (central difference).
Table 5.1: Component and element numbering for the H O/NH /CO system.
|     |     |     |     |     |           |     |         |     | 2   | 3 2 |     |
| --- | --- | --- | --- | --- | --------- | --- | ------- | --- | --- | --- | --- |
|     |     |     |     |     | Component |     | Element |     |     |     |     |
|     |     |     |     | 1   | H         | O   |         | H+  |     |     |     |
2
O2−
|     |     |     |     | 2   | NH  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3
NH−
|     |     |     |     | 3   | CO  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | 2   |     | 2   |     |     |     |
|     |     |     |     | 4   | CH  |     |     | CO  |     |     |     |
|     |     |     |     |     |     | 4   |     | 2   |     |     |     |
|     |     |     |     | 5   | C H |     |     | CH  |     |     |     |
|     |     |     |     |     | 2   | 6   |     | 4   |     |     |     |
H+
|     |     |     |     | 6   |     |     | C   | H   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     | 2 6 |     |     |     |
|     |     |     |     | 7   | NH+ |     |     |     |     |     |     |
4
|     |     |     |     | 8   | OH− |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
HCO−
9
3
|     |     |     |     | 10  | CO2− |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
3
|     |     |     |     | 11  | NH COO− |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
2
Xiao et al. (1989) used a different equation of state for the vapor phase suitable for

| Chapter   | 5. Calculation | of CPE     | in electrolyte | systems   |            | 107   |
| --------- | -------------- | ---------- | -------------- | --------- | ---------- | ----- |
| 3         |                |            |                | 3         |            |       |
| 0         |                |            |                | 0         |            |       |
| 3         |                |            |                | 3         |            |       |
| )rorre( − |                |            |                | )rorre( − |            |       |
| 6         |                |            |                | 6         |            |       |
| −         |                |            |                | −         |            |       |
| 01        |                |            |                | 01        |            |       |
| gol       |                |            |                | gol       |            |       |
| 9         |                |            |                | 9         |            |       |
| −         |                |            |                | −         |            |       |
| 12        |                |            |                | 12        |            |       |
| −         |                |            |                | −         |            |       |
| 15        |                |            |                | 15        |            |       |
| − 0       | 5 10           | 15 20      | 25 30          | − 0       | 3 6 9      | 12 15 |
|           |                | Iterations |                |           | Iterations |       |
|           | (a)            |            |                |           | (b)        |       |
8
snoitareti 6
4
pool
rennI
2
0
|     |     | 0   | 5 10       | 15 20 25        | 30  |     |
| --- | --- | --- | ---------- | --------------- | --- | --- |
|     |     |     | Outer loop | iteration index |     |     |
(c)
Figure 5.1: Convergence in the H O/NH /CO system at 373 K and 10 atm: (a)
|     |     |     | 2   | 3 2 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
successive substitution algorithm, (b) combined algorithm, (c) inner loop (Newton)
iterations per outer loop non-ideality updates [Q-function minimization ( ), VL ( )].

| 108 |     |     | Chapter | 5. Calculation | of CPE | in electrolyte | systems |
| --- | --- | --- | ------- | -------------- | ------ | -------------- | ------- |
Table 5.2: Equilibrium partial pressures in the vapor phase, molalities in the liquid phase,
phase amounts and phase fractions of the H O/NH /CO system at 373 K and 10 atm.
|     |     |     |     | 2 3 | 2   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
Component Feed Our work Our work (++, interact) Xiao et al. (1989)
−−
|       |        | p (atm) | m (mol/kg) | p (atm) | m (mol/kg) | p (atm) | m (mol/kg) |
| ----- | ------ | ------- | ---------- | ------- | ---------- | ------- | ---------- |
|       |        | i       | i          | i       | i          | i       | i          |
| H 2 O | 0.8473 | 0.9173  | 55.5084    | 0.9304  | 55.5084    | 0.9462  | 55.5550    |
| NH    | 0.0458 | 0.2556  | 0.8322     | 0.1881  | 0.5926     | 0.1543  | 0.6151     |
3
| CO  | 0.0458 | 2.1333 | 0.0243 | 1.5385 | 0.0178 | 1.8080 | 0.0183 |
| --- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
2
| CH  | 0.0305 | 3.3469 | 0   | 3.6714 | 0   | 3.5457 | 0   |
| --- | ------ | ------ | --- | ------ | --- | ------ | --- |
4
| C 2 H 6 | 0.0305 | 3.3469 | 0         | 3.6714 | 0         | 3.5457 | 0         |
| ------- | ------ | ------ | --------- | ------ | --------- | ------ | --------- |
| H+      | 0      | 0      | 3.25 10−8 | 0      | 1.65 10−8 | 0      | 5.34 10−8 |
|         |        |        | ×         |        | ×         |        | ×         |
| NH+     | 0      | 0      | 1.8242    | 0      | 2.3301    | 0      | 2.2256    |
4
| OH− | 0   | 0   | 3.78 10−5 | 0   | 2.63 10−5 | 0   | 4.61 10−5 |
| --- | --- | --- | --------- | --- | --------- | --- | --------- |
|     |     |     | ×         |     | ×         |     | ×         |
HCO−
|     | 0   | 0   | 1.4090 | 0   | 2.0517 | 0   | 1.6712 |
| --- | --- | --- | ------ | --- | ------ | --- | ------ |
3
| CO2− | 0   | 0   | 0.0599 | 0   | 0.0822 | 0   | 0.1780 |
| ---- | --- | --- | ------ | --- | ------ | --- | ------ |
3
| NH COO− | 0   | 0   | 0.2954 | 0   | 0.1139 | 0   | 0.1984 |
| ------- | --- | --- | ------ | --- | ------ | --- | ------ |
2
| n (mol) | 65.5084 | 5.9756 | 57.8310 | 5.4474 | 57.9161 | –   | –   |
| ------- | ------- | ------ | ------- | ------ | ------- | --- | --- |
t
| β   |     | 0.0937 | 0.9063 | 0.0860 | 0.9140 | –   | –   |
| --- | --- | ------ | ------ | ------ | ------ | --- | --- |
polar compounds, but this does not fully explain the deviations compared with our
calculations. Details about parameters and model implementation (Edwards et al., 1978)
are not provided by Xiao et al. (1989). For instance, same types of charges do not interact
according to Edwards et al. (1978) and their binary interaction parameters must be set
to zero. If we allow such interactions, the equilibrium solution seems to be closer to the
one presented by Xiao et al. (1989) (Table 5.2). We did not try to investigate further
if the interpretation of binary interaction parameter rules in Edwards et al. (1978) was
correct or not in the work of Xiao et al. (1989). The main purpose of this section is to
show that the algorithms can be applied to electrolyte systems without modifications of
the working equations. Furthermore, Figure 5.1 illustrates that the non-stoichiometric
algorithms of this work exhibit the same convergence rate as for non-electrolyte mixtures:
linear convergence with the successive substitution algorithm and quadratic during the
final iterations of the combined algorithm where the modified RAND method is used.
Possible modifications are concerned with the change of the infinite dilution reference
state of solutes (mole fraction or molality based) to the pure component reference state.
The first step is to transition from the unit molality to the infinite dilution reference state
with Eq. 5.22 and 5.23, since we use mole fractions in the equations instead of molalities.
Additionally, derivatives of the chemical potential are required in the modified RAND
method. For component i in phase k, where we use the infinite dilution reference state,
| we have (Eq. | 5.15 | and 5.17): |     |     |     |     |     |
| ------------ | ---- | ---------- | --- | --- | --- | --- | --- |

| Chapter | 5. Calculation |     | of CPE | in  | electrolyte |           | systems |          |     | 109    |
| ------- | -------------- | --- | ------ | --- | ----------- | --------- | ------- | -------- | --- | ------ |
|         |                |     |        | !   |             |           | !       |   ∂lnγ∞! |     |        |
|         |                |     | ∂lnγ˜  |     |             | ∂lnγ      |         |          |     |        |
|         |                |     | ik     |     | =           |           | ik      |          | ik  |        |
|         |                |     | ∂n     |     |             | ∂n        |         | −        | ∂n  |        |
|         |                |     | qk     |     |             | qk        |         |          | qk  | (5.40) |
|         |                |     |        | T,p |             |           | T,p     |          | T,p |        |
|         |                |     |        |     | q           | = 1,...,N |         |          |     |        |
C
and
|     |     |     |     |     |     | !   |   ∂lnγ∞! |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
1 ∂µ˜
|     |     |     |     |     | ik  | =         |     | ik  |     |        |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | ------ |
|     |     |     |     | RT  | ∂n  |           |     | ∂n  |     |        |
|     |     |     |     |     | qk  | T,p       |     | qk  | T,p | (5.41) |
|     |     |     |     |     | q   | = 1,...,N |     |     |     |        |
C
| Using Eq. | 5.18, we | get: |     |       |     |           |      |     |     |        |
| --------- | -------- | ---- | --- | ----- | --- | --------- | ---- | --- | --- | ------ |
|           |          |      |     |       | !   |           |      | !   |     |        |
|           |          |      |     | ∂lnγ˜ |     |           | ∂lnγ |     |     |        |
|           |          |      |     |       | ik  | =         |      | ik  |     |        |
|           |          |      |     | ∂n    |     |           | ∂n   |     |     | (5.42) |
|           |          |      |     |       | qk  | T,p       |      | qk  | T,p |        |
|           |          |      |     |       | q   | = 1,...,N |      |     |     |        |
C
and
|     |     |     |     |     |   ∂µ˜ | !   |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
ik
= 0
|     |     |     |     |     | ∂n  |     |     |     |     | (5.43) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
qk T,p
|     |     |     |     |     | q   | = 1,...,N |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
C
| 5.3.2 | Carbon | dioxide |     | in  | aqueous |     | solutions |     |     |     |
| ----- | ------ | ------- | --- | --- | ------- | --- | --------- | --- | --- | --- |
Carbon dioxide dissolves in water but is not an inert in an aqueous solution. It is
usually assumed that the following reactions take place when carbon dioxide interacts
with water:
|     |     |     |     |      |     | (cid:10)    | H+ +HCO− |     |     |        |
| --- | --- | --- | --- | ---- | --- | ----------- | -------- | --- | --- | ------ |
|     |     |     |     | CO   | +H  | O           |          |     |     | (5.44) |
|     |     |     |     | 2    |     | 2           |          |     | 3   |        |
|     |     |     |     | HCO− |     | (cid:10) H+ | +CO2−    |     |     |        |
(5.45)
|          |          |            |     |            | 3   |     |     | 3   |     |     |
| -------- | -------- | ---------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
| Eq. 5.44 | could be | split into | two | reactions: |     |     |     |     |     |     |
(cid:10)
|     |     |     |     | CO  | +H  | O           | H     | CO  |     | (5.46) |
| --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | --- | ------ |
|     |     |     |     |     | 2   | 2           |       | 2 3 |     |        |
|     |     |     |     |     |     | (cid:10) H+ | +HCO− |     |     |        |
|     |     |     |     | H   | CO  |             |       |     |     | (5.47) |
|     |     |     |     |     | 2 3 |             |       | 3   |     |        |

110 Chapter 5. Calculation of CPE in electrolyte systems
Most studies [e.g. Leal et al. (2016a,b)] disregard the carbonic acid in the solution and use
Eq. 5.44 and 5.45 to model the dissolution of carbon dioxide in water. We examined these
two cases separately: a set of reactions that exclude the carbonic acid using Eq. 5.44 and
5.45, and a different set that accounts for the carbonic acid with Eq. 5.46, 5.47 and 5.45.
Apart from water, calculations are also made for an aqueous solution of calcium chloride
with or without solid calcium carbonate.
In the calculations, vapor phase is described by the Peng-Robinson equation of state
(Peng and Robinson, 1976) with all binary interaction parameters k set to zero, except
ij
between water and carbon dioxide that is equal to 0.189 (Mohebbinia et al., 2013). Liquid
phase is described by Pitzer’s activity coefficient model (Pitzer, 1973) with the extended
version presented in Felmy and Weare (1986) and parameters from the Pitzer database
of PHREEQC (Parkhurst and Appelo, 2013) using numerical composition derivatives.
Reference state chemical potentials were taken from Venkatraman et al. (2015), except for
carbon dioxide that was taken from Duan and Sun (2003). Water density was obtained
from Dortmund Data Bank (2017) and water dielectric constant from Pa´tek et al. (2009).
All solutes except carbon dioxide are considered non-volatile. Only calcium carbonate is
allowed to exist in the solid phase. Results are compared with experimental solubilites of
carbon dioxide in water (Wiebe and Gaddy, 1940; Prutton and Savage, 1945) and calcium
chloride solutions (Prutton and Savage, 1945).
In Duan and Sun (2003), the reduced unit molality reference state chemical potential of
carbon dioxide is modeled. The analysis of the authors reveals that this value is actually
the Henry’s constant of carbon dioxide. Henry’s constant can be found at lower pressures
from the equation:
y p
H =
CO2
(5.48)
CO2
x
CO2
Experimental determination of x does not refer only to molecular carbon dioxide
CO2
dissolved in water. Solubility is the sum of all carbon dioxide related species: carbon
dioxide, carbonic acid, bicarbonate and carbonate ions. Bicarbonate and carbonate ions
are not produced in large amounts due to the small chemical equilibrium constants. In this
case, x is expected to be close to the aqueous molecular carbon dioxide. In contrast,
CO2
carbon dioxide to carbonic acid reaction has a chemical equilibrium constant close to 1.
Dissolved molecular carbon dioxide is expected to be almost as much as carbonic acid
at equilibrium. With a rough approximation, ignoring the bicarbonate and carbonate
ions, the Henry’s constant that is calculated for the actual carbon dioxide in water should
be multiplied with a factor of 2, to account for carbonic acid. Before calculating the
equilibrium of the electrolyte system in the presence of carbonic acid, we attempted to
find a scaling factor of the Henry’s constant. This factor was determined by the following
procedure:

| Chapter |     | 5. Calculation |     | of      | CPE | in electrolyte |     | systems |     |     |     | 111 |
| ------- | --- | -------------- | --- | ------- | --- | -------------- | --- | ------- | --- | --- | --- | --- |
|         |     |                |     | Hscaled |     | 2HDS           |     | HDS     |     |     |     |     |
1. Assume initially = , where is calculated from the correlation in
|     |      |     |             | CO2 |     | CO2 |     | CO2 |     |     |     |     |
| --- | ---- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | Duan | and | Sun (2003). |     |     |     |     |     |     |     |     |     |
Hscaled
| 2.  | Solve | CPE          | with | H       | =      |         |       |          |      |        |     |        |
| --- | ----- | ------------ | ---- | ------- | ------ | ------- | ----- | -------- | ---- | ------ | --- | ------ |
|     |       |              |      | CO2     | CO2    |         |       |          |      |        |     |        |
| 3.  | From  | the solution |      | update  | scaled | Henry’s |       | constant | as:  |        |     |        |
|     |       |              |      |         |        | x +x    |       | +x       | HCO− | +x CO2 | −   |        |
|     |       |              |      | Hscaled |        | CO2     | H2CO3 |          |      |        | HDS |        |
|     |       |              |      |         | =      |         |       |          | 3    | 3      |     | (5.49) |
|     |       |              |      | CO2     |        |         |       | x        |      |        | CO2 |        |
CO2
|     | If  | Hscaled | has | converged,     |     | accept | the scaling | factor |     |     |     |     |
| --- | --- | ------- | --- | -------------- | --- | ------ | ----------- | ------ | --- | --- | --- | --- |
|     | •   | CO2     |     |                |     |        |             |        |     |     |     |     |
|     | If  | Hscaled | has | not converged, |     | go     | to step     | 2      |     |     |     |     |
CO2
•
We found that an average value of this factor is 2.01 in the range 280-400 K and 5-15 atm.
Whenever the carbonic acid was included in the calculations, the scaled Henry’s constant
was used for carbon dioxide. Results for both approaches (with and without carbonic acid)
| are | presented. |     | It is | also assumed |     | that: |     |      |     |     |     |        |
| --- | ---------- | --- | ----- | ------------ | --- | ----- | --- | ---- | --- | --- | --- | ------ |
|     |            |     |       |              |     | V ¯∞  | =   | v +V | ¯∞  |     |     | (5.50) |
H2O
|     |     |     |     |     |     | H2CO3 |     |     | CO2 |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
Otherwise, based on the data from Venkatraman et al. (2015), only the reference state
chemical potential of water and carbon dioxide will be pressure dependent and the chemical
equilibrium constant at higher pressures will favor unreasonably the production of H CO .
2 3
The reactions in the complete system of carbon dioxide, water, calcium chloride and
| calcium | carbonate |          |     | acid are: |     |     |     |     |     |     |     |     |
| ------- | --------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
|         | Without   | carbonic |     | acid      |     |     |     |     |     |     |     |     |
•
|     |     |     |     |     |     |     | (cid:10) | H+ +OH− |     |     |     |        |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | --- | --- | --- | ------ |
|     |     |     |     |     |     | H   | O        |         |     |     |     | (5.51) |
2
|     |     |     |     |     |     |       |          | (cid:10) H+ | +HCO− |     |     |        |
| --- | --- | --- | --- | --- | --- | ----- | -------- | ----------- | ----- | --- | --- | ------ |
|     |     |     |     |     |     | CO +H | O        |             |       |     |     | (5.52) |
|     |     |     |     |     |     | 2     | 2        |             |       | 3   |     |        |
|     |     |     |     |     |     | HCO−  | (cid:10) | H+ +CO2−    |       |     |     |        |
(5.53)
|     |     |     |     |     |     |      | 3        |            | 3   |     |     |        |
| --- | --- | --- | --- | --- | --- | ---- | -------- | ---------- | --- | --- | --- | ------ |
|     |     |     |     |     |     | CaCl | (cid:10) | Ca2+ +2Cl− |     |     |     | (5.54) |
2
|     |     |     |     |     |     | CaCO | (cid:10) | Ca2+ +CO2− |     |     |     | (5.55) |
| --- | --- | --- | --- | --- | --- | ---- | -------- | ---------- | --- | --- | --- | ------ |
3
3
The number of elements is N = N N = 10 5 = 5. The formula matrix and
|     |                |     |        |     |     | E      | C         | R   |     |     |     |     |
| --- | -------------- | --- | ------ | --- | --- | ------ | --------- | --- | --- | --- | --- | --- |
|     |                |     |        |     |     |        | −         |     | −   |     |     |     |
|     | stoichiometric |     | matrix | of  | the | system | are given | by: |     |     |     |     |

| 112 |     |     |     | Chapter |     | 5. Calculation |     | of  | CPE | in electrolyte | systems |
| --- | --- | --- | --- | ------- | --- | -------------- | --- | --- | --- | -------------- | ------- |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     | 2 0     | 0   | 0 1            | 0 1 | 0 1 | 0   |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     | 0 0    | 1   | 1 0            | 1 0 | 0 0 | 0  |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     | A = | 1 0    | 0   | 1 0            | 0 1 | 0 1 | 1  |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     | 0 0    | 2   | 0 0            | 0 0 | 1 0 | 0  |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     |        |     |                |     |     |    |                |         |
|     |     |     |     | 0 1     | 0   | 1 0            | 0 0 | 0 1 | 1   |                |         |
(5.56)
|     |     |     |    |     |     |     |     |     |     | T  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 1   | 0   | 0   | 0 1 | 0 1 | 0   | 0   | 0   |     |
−

|     |     |     |  1 | 1   | 0   | 0 1 | 0 0 | 0   | 1   | 0  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | −  | −   |     |     |     |     |     |    |     |
|     |     |     |    |     |     |     |     |     |     |    |     |
|     |     | N = |  0 | 0   | 0   | 0 1 | 0 0 | 0   | 1   | 1  |     |
|     |     |     |    |     |     |     |     |     | −   |    |     |
|     |     |     |  0 | 0   | 1   | 0 0 | 1 0 | 2   | 0   | 0  |     |
|     |     |     |    |     |     |     |     |     |     |    |     |
|     |     |     |    |     | −   |     |     |     |     |    |     |
|     |     |     | 0   | 0   | 0   | 1 0 | 1 0 | 0   | 0   | 1   |     |
−
| With carbonic | acid |     |     |     |     |     |     |     |     |     |     |
| ------------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
•
|     |     |     |     | H   | O (cid:10) | H+ +OH− |     |     |     |     | (5.57) |
| --- | --- | --- | --- | --- | ---------- | ------- | --- | --- | --- | --- | ------ |
2
|     |     |     |     | CO   | +H       | O (cid:10) | H CO  |     |     |     | (5.58) |
| --- | --- | --- | --- | ---- | -------- | ---------- | ----- | --- | --- | --- | ------ |
|     |     |     |     |      | 2        | 2          | 2     | 3   |     |     |        |
|     |     |     |     | H CO | (cid:10) | H+         | +HCO− |     |     |     | (5.59) |
|     |     |     |     | 2    | 3        |            |       | 3   |     |     |        |
|     |     |     |     | HCO− | (cid:10) | H+         | +CO2− |     |     |     | (5.60) |
|     |     |     |     |      | 3        |            | 3     |     |     |     |        |
|     |     |     |     | CaCl | (cid:10) | Ca2+       | +2Cl− |     |     |     | (5.61) |
2
(cid:10)
|     |     |     |     | CaCO |     | Ca2+ | +CO2− |     |     |     | (5.62) |
| --- | --- | --- | --- | ---- | --- | ---- | ----- | --- | --- | --- | ------ |
|     |     |     |     |      | 3   |      |       | 3   |     |     |        |
The number of elements is N = N N = 11 6 = 5. The formula matrix and
|                |        |     |             | E   | C   | R     |     |     |     |     |     |
| -------------- | ------ | --- | ----------- | --- | --- | ----- | --- | --- | --- | --- | --- |
|                |        |     |             |     | −   |       | −   |     |     |     |     |
| stoichiometric | matrix | of  | the systems |     | are | given | by: |     |     |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        |     |             | 2 0 | 2 0 | 0 1   | 0 1 | 0 1 | 0   |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        |     | 0          | 0   | 0 1 | 1 0   | 1 0 | 0 0 | 0  |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        | A   | = 1        | 0   | 1 0 | 1 0   | 0 1 | 0 1 | 1  |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        |     | 0          |     |     |       |     |     | 0  |     |     |
|                |        |     |            | 0   | 0 2 | 0 0   | 0 0 | 1 0 |    |     |     |
|                |        |     |            |     |     |       |     |     |    |     |     |
|                |        |     |             | 0 1 | 1 0 | 1 0   | 0 0 | 0 1 | 1   |     |     |
(5.63)
|     |     |    |     |     |     |     |     |     |     | T  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 1 0 | 0   | 0   | 0   | 1 0 | 1 0 | 0   | 0   |     |
−
|     |     |    |     |     |     |     |     |     |     | 0  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 1   | 1 1 | 0   | 0   | 0 0 | 0 0 | 0   |     |     |
|     |     |    |     |     |     |     |     |     |     |    |     |
|     |     | −  | −   |     |     |     |     |     |     |    |     |
|     |     |    | 0 0 |     | 1 0 | 0   | 1 0 | 0 0 | 1   | 0  |     |
|     |     |    |     |     |     |     |     |     |     |    |     |
|     | N   | =  |     | −   |     |     |     |     |     |    |     |
|     |     |    | 0 0 | 0   | 0   | 0   | 1 0 | 0 0 | 1   | 1  |     |
|     |     |    |     |     |     |     |     |     | −   |    |     |
|     |     |    |     |     |     |     |     |     |     |    |     |
|     |     |    | 0 0 | 0   | 1   | 0   | 0 1 | 0 2 | 0   | 0  |     |
|     |     |    |     |     |     |     |     |     |     |    |     |
−
|     |     |     | 0 0 | 0   | 0   | 1   | 0 1 | 0 0 | 0   | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
−
The components and elements of the complete system are presented in Table 5.3.

| Chapter | 5. Calculation |     | of  | CPE | in electrolyte | systems |     |     | 113 |
| ------- | -------------- | --- | --- | --- | -------------- | ------- | --- | --- | --- |
Table 5.3: Component and element numbering for H O/CO /CaCl /CaCO system.
|     |     |           |     |         |     |      | 2 2       | 2 3     |     |
| --- | --- | --------- | --- | ------- | --- | ---- | --------- | ------- | --- |
|     |     | Component |     | Without |     | H CO | With H CO | Element |     |
|     |     |           |     |         |     | 2 3  | 2 3       |         |     |
|     |     |           | 1   |         | H   | O    | H O       | H+      |     |
|     |     |           |     |         |     | 2    | 2         |         |     |
Ca2+
|     |     |     | 2   |     | CO   |     | CO   |     |     |
| --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- |
|     |     |     |     |     |      | 2   | 2    |     |     |
|     |     |     | 3   |     | CaCl |     | H CO | O2− |     |
|     |     |     |     |     |      | 2   | 2 3  |     |     |
|     |     |     | 4   |     | CaCO |     | CaCl | Cl− |     |
|     |     |     |     |     |      | 3   | 2    |     |     |
H+
|     |     |     | 5   |     |      |     | CaCO | CO  |     |
| --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- |
|     |     |     |     |     |      |     | 3    | 2   |     |
|     |     |     | 6   |     | Ca2+ |     | H+   |     |     |
|     |     |     | 7   |     | OH−  |     | Ca2+ |     |     |
|     |     |     |     |     | Cl−  |     | OH−  |     |     |
8
|     |     |     | 9   |     | HCO− |     | Cl− |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
3
|     |     |     | 10  |     | CO2− |     | HCO− |     |     |
| --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- |
|     |     |     |     |     |      | 3   | 3    |     |     |
CO2−
11
3
| Carbon | dioxide | in  | water |     |     |     |     |     |     |
| ------ | ------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Carbon dioxide solubility in pure water is calculated without calcium chloride or calcium
carbonate in the solution. Their corresponding rows and columns are decoupled from
the formula and stoichiometric matrices. Figure 5.2 shows the solubility as a function of
| pressure | at different | temperatures. |     |     |     |     |     |     |     |
| -------- | ------------ | ------------- | --- | --- | --- | --- | --- | --- | --- |
Both approaches can capture adequately the experimental data at different temperatures
over a large pressure range. In Figures 5.2a and 5.2c, concentrations of the bicarbonate
and carbonate ions are so low, that the molecular aqueous carbon dioxide is almost as
high as the total solubility. We see a different picture in Figures 5.2b and 5.2d where
the carbonic acid is included in the calculations. Dissolved molecular carbon dioxide is
approximately as abundant as the carbonic acid and the scaled Henry’s constant must
| account | for this | to ultimately |         | yield    | correct | solubilities. |          |     |     |
| ------- | -------- | ------------- | ------- | -------- | ------- | ------------- | -------- | --- | --- |
| Carbon  | dioxide  | in            | aqueous | solution |         | of calcium    | chloride |     |     |
The electrolyte system is more complex and non-ideal when calcium chloride is dissolved
in water. There is no calcium carbonate in the solution and its corresponding rows
and columns are decoupled from the formula and stoichiometric matrices. Experimental
solubility of carbon dioxide in the solution is lower at higher salinity. Calculations are
| shown with | experimental |     | data | in  | Figure | 5.3. |     |     |     |
| ---------- | ------------ | --- | ---- | --- | ------ | ---- | --- | --- | --- |
The calculated curves at different temperatures are more distinguishable in comparison
with the experimental data but they change as expected, i.e. higher temperatures result in
lower solubilities. The reason for the larger deviations compared to pure water solubility, is
the lack of a ternary interaction parameter involving calcium and chloride ions with carbon
dioxide [Pitzer database of PHREEQC (Parkhurst and Appelo, 2013) for Pitzer’s model in

| 114                      |      |         |               |       |     | Chapter | 5. Calculation           |      | of   | CPE           | in electrolyte |     | systems |
| ------------------------ | ---- | ------- | ------------- | ----- | --- | ------- | ------------------------ | ---- | ---- | ------------- | -------------- | --- | ------- |
|                          |      | without | H2CO          | 3(aq) |     |         |                          |      | with | H2CO          | 3(aq)          |     |         |
|                          | 2.5  |         |               |       |     |         |                          | 2.5  |      |               |                |     |         |
| ])O                      |      |         |               |       |     |         | ])O                      |      |      |               |                |     |         |
| 2                        | 2.0  |         |               |       |     |         | 2                        | 2.0  |      |               |                |     |         |
| Hgk(/lom[ytilibulos      |      |         |               |       |     |         | Hgk(/lom[ytilibulos      |      |      |               |                |     |         |
|                          | 1.5  |         |               |       |     |         |                          | 1.5  |      |               |                |     |         |
|                          | 1.0  |         |               |       |     |         |                          | 1.0  |      |               |                |     |         |
|                          | 0.5  |         |               |       |     |         |                          | 0.5  |      |               |                |     |         |
| OC 2                     |      |         |               |       |     |         | OC 2                     |      |      |               |                |     |         |
|                          | 0    |         |               |       |     |         |                          | 0    |      |               |                |     |         |
|                          | 0    | 100     | 200 300       | 400   |     | 500 600 |                          | 0    | 100  | 200           | 300 400        | 500 | 600     |
|                          |      |         | Pressure(atm) |       |     |         |                          |      |      | Pressure(atm) |                |     |         |
|                          |      |         | (a)           |       |     |         |                          |      |      | (b)           |                |     |         |
|                          | 0.04 |         |               |       |     |         |                          | 0.04 |      |               |                |     |         |
| )noitcarfelom(ytilibulos |      |         |               |       |     |         | )noitcarfelom(ytilibulos |      |      |               |                |     |         |
|                          | 0.03 |         |               |       |     |         |                          | 0.03 |      |               |                |     |         |
|                          | 0.02 |         |               |       |     |         |                          | 0.02 |      |               |                |     |         |
|                          | 0.01 |         |               |       |     |         |                          | 0.01 |      |               |                |     |         |
| 2                        |      |         |               |       |     |         | 2                        |      |      |               |                |     |         |
| OC                       |      |         |               |       |     |         | OC                       |      |      |               |                |     |         |
|                          | 0    |         |               |       |     |         |                          | 0    |      |               |                |     |         |
|                          | 0    | 200     | 400           | 600   | 800 | 1000    |                          | 0    | 200  | 400           | 600            | 800 | 1000    |
|                          |      |         | Pressure(atm) |       |     |         |                          |      |      | Pressure(atm) |                |     |         |
|                          |      |         | (c)           |       |     |         |                          |      |      | (d)           |                |     |         |
Figure 5.2: CO solubility in water [experimental data at 285.15 K ( ), 291.15 K ( ),
2
298.15 K ( ), 304.19 K ( ), 308.15 K ( ), 313.15 K ( ), 374.15 K ( ), 393.15 K ( ), sum of
|     |     |     | all | CO  | related | species | (   | ), CO | (     | )]. |     |     |     |
| --- | --- | --- | --- | --- | ------- | ------- | --- | ----- | ----- | --- | --- | --- | --- |
|     |     |     |     | 2   |         |         |     |       | 2(aq) |     |     |     |     |

| Chapter                  | 5.  | Calculation   | of CPE | in electrolyte | systems                  |       |               |     | 115  |
| ------------------------ | --- | ------------- | ------ | -------------- | ------------------------ | ----- | ------------- | --- | ---- |
|                          |     | without       | H2CO   |                |                          | with  | H2CO          |     |      |
|                          |     |               | 3(aq)  |                |                          |       | 3(aq)         |     |      |
| 0.025                    |     |               |        |                |                          | 0.025 |               |     |      |
| )noitcarfelom(ytilibulos |     |               |        |                | )noitcarfelom(ytilibulos |       |               |     |      |
| 0.020                    |     |               |        |                |                          | 0.020 |               |     |      |
| 0.015                    |     |               |        |                |                          | 0.015 |               |     |      |
| 0.010                    |     |               |        |                |                          | 0.010 |               |     |      |
| 0.005                    |     |               |        |                |                          | 0.005 |               |     |      |
| OC 2                     |     |               |        |                | OC 2                     |       |               |     |      |
|                          | 0   |               |        |                |                          | 0     |               |     |      |
|                          | 0   | 200 400       | 600    | 800            | 1000                     | 0 200 | 400 600       | 800 | 1000 |
|                          |     | Pressure(atm) |        |                |                          |       | Pressure(atm) |     |      |
|                          |     | (a)           |        |                |                          |       | (b)           |     |      |
| 0.018                    |     |               |        |                |                          | 0.018 |               |     |      |
| )noitcarfelom(ytilibulos |     |               |        |                | )noitcarfelom(ytilibulos |       |               |     |      |
| 0.015                    |     |               |        |                |                          | 0.015 |               |     |      |
| 0.012                    |     |               |        |                |                          | 0.012 |               |     |      |
| 0.009                    |     |               |        |                |                          | 0.009 |               |     |      |
| 0.006                    |     |               |        |                |                          | 0.006 |               |     |      |
| 2 0.003                  |     |               |        |                | 2                        | 0.003 |               |     |      |
| OC                       |     |               |        |                | OC                       |       |               |     |      |
|                          | 0   |               |        |                |                          | 0     |               |     |      |
|                          | 0   | 200 400       | 600    | 800            | 1000                     | 0 200 | 400 600       | 800 | 1000 |
|                          |     | Pressure(atm) |        |                |                          |       | Pressure(atm) |     |      |
|                          |     | (c)           |        |                |                          |       | (d)           |     |      |
Figure 5.3: CO solubility in: (a, b) 10.1% CaCl , (c, d) 20.2% CaCl [experimental
|     |     | 2   |     |     | 2(aq) |     | 2(aq) |     |     |
| --- | --- | --- | --- | --- | ----- | --- | ----- | --- | --- |
data at 348.65 K ( ), 349.15 K ( ), 374.15 K ( ), 394.15 K ( ), sum of all CO related
2
|     |     |     |     | species ( | ), CO | ( )]. |     |     |     |
| --- | --- | --- | --- | --------- | ----- | ----- | --- | --- | --- |
2(aq)

| 116 |     |     | Chapter | 5. Calculation | of  | CPE in electrolyte | systems |
| --- | --- | --- | ------- | -------------- | --- | ------------------ | ------- |
Felmy and Weare (1986)]. However, we conclude that the algorithms can produce results
even when the system is highly non-ideal. Of course, better models or more available
relevant parameters will shift the calculated curves closer to the experimental data.
Carbon dioxide in aqueous solution of calcium chloride with calcium
carbonate
Finally, calculations are made in the presence of both calcium chloride and calcium
carbonate in the solution. The latter is a solute but can also form a pure solid phase.
| Comparison               |     | with experimental | data is | shown in Figures         | 5.4.  |               |          |
| ------------------------ | --- | ----------------- | ------- | ------------------------ | ----- | ------------- | -------- |
|                          |     | without H2CO      |         |                          | with  | H2CO          |          |
|                          |     | 3(aq)             |         |                          |       | 3(aq)         |          |
| 0.025                    |     |                   |         | 0.025                    |       |               |          |
| )noitcarfelom(ytilibulos |     |                   |         | )noitcarfelom(ytilibulos |       |               |          |
| 0.020                    |     |                   |         | 0.020                    |       |               |          |
| 0.015                    |     |                   |         | 0.015                    |       |               |          |
| 0.010                    |     |                   |         | 0.010                    |       |               |          |
| 0.005                    |     |                   |         | 0.005                    |       |               |          |
| OC 2                     |     |                   |         | OC 2                     |       |               |          |
|                          | 0   |                   |         |                          | 0     |               |          |
|                          | 0   | 200 400 600       | 800     | 1000                     | 0 200 | 400 600       | 800 1000 |
|                          |     | Pressure(atm)     |         |                          |       | Pressure(atm) |          |
|                          |     | (a)               |         |                          |       | (b)           |          |
Figure 5.4: CO solubility in 10.1% CaCl in the presence of CaCO [experimental
|     |     | 2   |     | 2(aq) |     | 3(s) |     |
| --- | --- | --- | --- | ----- | --- | ---- | --- |
data at 393.15 K ( ), sum of all CO related species ( ), CO ( )].
|     |     |     |     | 2   |     | 2(aq) |     |
| --- | --- | --- | --- | --- | --- | ----- | --- |
Experimental data with or without calcium carbonate at equilibrium do not seem to be
easily distinguishable (Figures 5.3a and 5.3b). The solid does not appear in the system
from precipitation, but it is included in the feed. Calculations predict only a small amount
of the solid dissolving in the the aqueous phase (0.01%-0.02%) and as a result it does not
affect much the overall equilibrium. The main capability of the algorithms highlighted
here is that with both the Lagrange multipliers method and the modified RAND we
can handle pure solids in contact with highly non-ideal electrolyte aqueous phases at
equilibrium.
| 5.4 | Conclusions |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- |
The successive substitution and the combined algorithm were successfully applied to
single-solvent (aqueous) electrolyte systems. Electroneutrality is already satisfied by the
formula matrix in the material balance. It should be mentioned that the working equations
have been derived for mole fractions and a mole fraction based reference state needs to
be selected. Therefore, the main difficulty associated with these systems is to transform

Chapter 5. Calculation of CPE in electrolyte systems 117
the molality or molarity reference state to the infinite dilution reference state. This task
is not performed by the non-stoichiometric methods presented in this work but by the
fugacity or activity coefficient routine. As a result the working equations of both the
Lagrange multipliers and the modified RAND method remain unchanged in electrolyte
systems.
Calculations in the VLE of an ammonia/carbon dioxide aqueous solution in the presence
of inerts revealed that CPU time and convergence behavior are similar to calculations for
non-electrolyte systems. Furthermore, we investigated the solubility of carbon dioxide in
pure water and highly non-ideal aqueous solutions of calcium chloride in the presence of
solid calcium carbonate. Comparisons were made with experimental data to validate as a
first step the correct qualitative description of the systems. The most accurate calculations
were observed for aqueous solution of carbon dioxide at various temperatures. The models
used for the electrolytes in the aqueous phase are not necessarily the most suitable because
not all interaction parameters between the solutes were available. Improved calculations
can be made when more relevant parameters are known or a more consistent electrolyte
EoS model is used.
Finally, the most important finding of this chapter is that both algorithms were able to
solve the CPE of electrolyte systems and consideration of a solid phase did not cause
any problems in convergence (initialization or the actual CPE calculations). Even more
complex areas of application could include geochemical systems with an aqueous phase of
various charged and uncharged solutes at equilibrium with multiple solid phases, such as
the systems appearing in Leal et al. (2016a,b).

C H A P T E R
6
Phase equilibrium modeling
for DME enhanced waterflood
Waterflooding is a secondary oil recovery method. Water/brine injected into a reservoir
displaces the oil by maintaining the reservoir pressure at a sufficient level for oil production.
However, primaryandsecondaryoilrecoveryaccountsforabout35%ofthetotaloilamount,
while further recovery with conventional methods proves to be too expensive (Lake, 1989).
Toextractmoreoilfromareservoir,enhancedoilrecoverymethodsareemployed. OneEOR
method is solvent enhanced waterflood, which involves phase equilibrium and component
exchange with the reservoir oil, such as extraction, dissolution, etc. In the case of complete
miscibility of the solvent with the oil, the process has high ultimate displacement efficiency
due to the absence of residual phases (Lake, 1989). Dimethyl ether (DME) has been
recently proposed as a novel solvent in the DME enhanced waterflood (DEW) process
developed by Shell (Chernetsky et al., 2015), intended for mature and new wells (Groot
et al., 2016).
DME or methoxymethane, a colorless gas at room temperature, is the simplest ether. The
molecular structure of DME is shown in Figure 6.1. It is synthesized from synthesis gas
(syngas), natural gas, coal or biomass: methanol is first produced and is subsequently
dehydrated to DME (Arteconi et al., 2009; Park et al., 2007). It can be used as a propellant
gas, fuel additive, pesticide, hydrogen source for fuel cells, for household cooking and
heating, etc. (Wu et al., 2003, 2004; Park et al., 2007; Meng et al., 2012; Ratnakar
et al., 2016a, 2017). DME is not a cryogenic liquid, which makes it easy to store (Park
et al., 2007). It is a high performance refrigerant that operates at moderate pressures,
being potentially a green refrigerant (ozone depletion potential equal to 0) (Meng et al.,
2012).
It has similar physical properties to liquefied petroleum gases (propane, butane) and as a
result is has been proposed as an alternative to LPG. DME exhibits excellent properties as
a diesel fuel and has been viewed as a fossil fuel alternative because of the lower emissions
of SO and NO (Arteconi et al., 2009; Meng et al., 2012; Tallon and Fenton, 2010). Use
x x

120 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
H H
O
C C
H H
H H
Figure 6.1: Dimethyl ether molecular structure.
in extraction is advantageous due to its higher vapor pressure compared to other liquid
organic solvents, because of the easier removal from the final product. DME in air is
flammable, making it ideal as a fuel, but requires provision when applied as a solvent
in extraction (Tallon and Fenton, 2010). Finally, DME is non-toxic, non-corrosive and
non-carcinogenic (Chahardowli et al., 2016; Ratnakar et al., 2016a, 2017).
DME is a slightly polar compound (dipole moment 1.3 D), soluble in both polar and
non-polar solvents (Wu et al., 2003, 2004; Dahlhoff and Pfennig, 2000; Arteconi et al.,
2009). This the reason why it was considered as a solvent in enhanced waterflood. Details
of the DEW process are included in te Riele et al. (2016). Alkindi et al. (2016) mention
that DME enhanced waterflood is advantageous compared with steam injection due to
the miscible flow without density differences that could cause negative gravity effects.
DME can be dissolved in water/brine and it is first-contact miscible with the oil. When it
partitions into the oil phase, it swells the oil reducing its viscosity and therefore increasing
its mobility. The solvent is then recovered and reused by chase water flooding (Groot et al.,
2016). Water/brine plays the role of the DME carrier during the injection (Chernetsky
et al., 2015; Ratnakar et al., 2016a). DME is imported or synthesized on site (te Riele
et al., 2016).
A complex EOR process, the DEW process, involves partitioning of DME between the
hydrocarbon and water/brine phases. Compared with classical waterflooding, because of
DME,hydrocarbonscanbedissolvedtoalargerextentintheaqueousphaseandmorewater
can be dissolved in the hydrocarbon phase. In order to combine the DEW process with
reservoir simulation, adequate phase equilibrium modeling is needed to capture the major
characteristics of the DME/water(brine)/hydrocarbon phase behavior. In particular, the
most important property to describe is the partitioning of DME between the hydrocarbon
and aqueous phases (K-value). In addition to phase equilibrium, other physical properties
of DME-containing oils and aqueous phases, such as densities and viscosities, are important,
but they are not covered in this study. In this chapter, we present the modeling of DME
binary systems with different compounds relevant to the DEW process, influenced by
the work of Ratnakar et al. (2016b,a, 2017). Predictions are made initially for ternary
mixtures of DME/water/hydrocarbons and then for DME/water/model oil, examining the
effect of oil composition, temperature, pressure and salinity on the K-values of DME.

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 121
| 6.1 EoS |     | models |     |     |     |     |     |     |     |     |     |     |
| ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The models selected for the phase equilibrium modeling are the Cubic-Plus-Association
equation of state and cubic equations of state with Huron-Vidal mixing rules.
| Cubic-Plus-Association |     |     |     | equation | of  | state (CPA |     | EoS) |     |     |     |     |
| ---------------------- | --- | --- | --- | -------- | --- | ---------- | --- | ---- | --- | --- | --- | --- |
•
CPA is an EoS developed to account for the association of compounds such as water,
alcohols, organic acids etc. (Kontogeorgis et al., 1996). Association can take place be-
tween the same types of molecules (self-association) or different types (cross association
or solvation). The equation combines the Soave-Redlich-Kwong EoS (Soave, 1972) with
the association term of Huang and Radosz (1990). The original form of CPA is:
|       |          |      |     |         |            |     |           |      |        | !        |        |       |
| ----- | -------- | ---- | --- | ------- | ---------- | --- | --------- | ---- | ------ | -------- | ------ | ----- |
|       |          |      | RT  |         | a(T)       | RT  |           |      | 1      | 1 ∂X     |        |       |
|       |          |      |     |         |            |     | X         |      |        |          | Ai     |       |
|       |          |      | p = |         |            |     |           |      |        |          |        | (6.1) |
|       |          |      | v   | b       | v(v        | +b) | v2        | X    |        | 2 ∂(1/v) |        |       |
|       |          |      |     | −       |            | −   |           |      | Ai −   |          |        |       |
|       |          |      |     | −       |            |     | Ai        |      |        |          |        |       |
| which | can also | take | the | form    | (Michelsen | and | Hendriks, |      | 2001): |          |        |       |
|       |          |      |     |         |            |     |           |      | !      |          |        |       |
|       |          | RT   |     | a(T)    |            | 1RT | 1         | ∂lng |        |          |        |       |
|       |          |      |     |         |            |     |           |      | X      | X        |        |       |
|       | p        | =    |     |         |            |     | 1+        |      |        | x        | (1 X ) | (6.2) |
|       |          | v    | b   | v(v +b) |            | 2 v | v∂(1/v)   |      |        | i        | Ai     |       |
|       |          |      | −   |         | −          |     |           |      |        |          | −      |       |
|       |          | −    |     |         |            |     |           |      |        | i Ai     |        |       |
with
1
|     |     |     |       | X   | =        |     |              |     |       |       |     | (6.3) |
| --- | --- | --- | ----- | --- | -------- | --- | ------------ | --- | ----- | ----- | --- | ----- |
|     |     |     |       | Ai  | 1+(1/v)P |     |              | P   |       |       |     |       |
|     |     |     |       |     |          |     | x            | X   | ∆AiBj |       |     |       |
|     |     |     |       |     |          |     | j j          | Bj  | Bj    |       |     |       |
|     |     |     |       |     |          | "   | (cid:15)AiBj | !   | #     |       |     |       |
|     |     |     | ∆AiBj |     | = g(v)   | exp |              |     | 1 b   | βAiBj |     | (6.4) |
ij
|     |     |     |     |     |     |        | RT  | −   |     |     |     |       |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | ----- |
|     |     |     |     |     |     |        | 2   | η   |     |     |     |       |
|     |     |     |     |     |     | g(v) = | −   |     |     |     |     | (6.5) |
|     |     |     |     |     |     |        | 2(1 | η)3 |     |     |     |       |
−
and
b
|     |     |     |     |     |     | η = |     |     |     |     |     | (6.6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
4v
where:
| v   | molar    | volume    |           |     |     |     |     |     |     |     |     |     |
| --- | -------- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| a   | energy   | parameter |           |     |     |     |     |     |     |     |     |     |
| b   | covolume |           | parameter |     |     |     |     |     |     |     |     |     |
∆AiBj
|     | association |     | strength |     | between | sites | A   | and | B   |     |     |     |
| --- | ----------- | --- | -------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
|     |             |     |          |     |         |       | i   |     | j   |     |     |     |

122 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
| X   | mole | fraction | of  | component |     | i   | not bonded | at  | site A |     |
| --- | ---- | -------- | --- | --------- | --- | --- | ---------- | --- | ------ | --- |
Ai
| g(v) | radial | distribution |     | function |     |     |     |     |     |     |
| ---- | ------ | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- |
(cid:15)AiBj association energy of interaction between sites A and B
i j
βAiBj
parameter in the association term of CPA between sites A and B
i j
| b   | covolume |     | parameter |     | of components |     |     | i and j |     |     |
| --- | -------- | --- | --------- | --- | ------------- | --- | --- | ------- | --- | --- |
ij
| The radial | distribution |     | function |     | is  | approximated |     | as: |     |     |
| ---------- | ------------ | --- | -------- | --- | --- | ------------ | --- | --- | --- | --- |
1
|     |     |     |     |     |     | g(v) |     |      |     | (6.7) |
| --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | ----- |
|     |     |     |     |     |     |      | ≈ 1 | 1.9η |     |       |
−
| For pure | components, |     | the | energy | parameter |       | is       | calculated | by:       |       |
| -------- | ----------- | --- | --- | ------ | --------- | ----- | -------- | ---------- | --------- | ----- |
|          |             |     |     |        |           | "     |          |            | #         |       |
|          |             |     |     |        |           |       | (cid:18) | q          | (cid:19)2 |       |
|          |             |     |     | a(T)   | =         | a 1+c |          | 1 T        |           | (6.8) |
|          |             |     |     |        |           | 0     | 1        | r          |           |       |
−
Combining rules of a involve the use of a binary interaction parameter:
|     |     |     |     |     | a   | = √a | a (1 | k ) |     | (6.9) |
| --- | --- | --- | --- | --- | --- | ---- | ---- | --- | --- | ----- |
|     |     |     |     |     |     | ij   | i j  | ij  |     |       |
−
No interaction parameters are involved in the combining rules of b:
b +b
|     |     |     |     |     |     |     | i   | j   |     |        |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | b   | =   |     |     | (6.10) |
ij
2
where:
| a   | energy | parameter |     | of  | components |     | i and | j   |     |     |
| --- | ------ | --------- | --- | --- | ---------- | --- | ----- | --- | --- | --- |
ij
| a   | energy | parameter |     | of  | component |     | i   |     |     |     |
| --- | ------ | --------- | --- | --- | --------- | --- | --- | --- | --- | --- |
i
| k   | binary | interaction |     | parameter |     |     | between | component | i and j |     |
| --- | ------ | ----------- | --- | --------- | --- | --- | ------- | --------- | ------- | --- |
ij
| b   | covolume |     | parameter |     | of component |     | i   |     |     |     |
| --- | -------- | --- | --------- | --- | ------------ | --- | --- | --- | --- | --- |
i
| b   | covolume |     | parameter |     | of components |     |     | i and j |     |     |
| --- | -------- | --- | --------- | --- | ------------- | --- | --- | ------- | --- | --- |
ij
In this work, water is the only self-associating compound, hydrocarbons or inert gases
in the oil are non-associating and DME is solvating in water. For DME/water the
modified CR-1 rules are followed for cross association (Folas et al., 2006):
|     |     |     |     |     |     | β     | = β       |     |     | (6.11) |
| --- | --- | --- | --- | --- | --- | ----- | --------- | --- | --- | ------ |
|     |     |     |     |     |     | cross | regressed |     |     |        |
and
(cid:15)
water
|     |     |     |     |     |     | (cid:15) | =   |     |     | (6.12) |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | ------ |
|     |     |     |     |     |     | cross    |     | 2   |     |        |

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 123
| Classical mixing | rules | are | used | for a | and b: |     |     |     |     |
| ---------------- | ----- | --- | ---- | ----- | ------ | --- | --- | --- | --- |
XX
|     |     |     |     | a = |     | x x | a   |     | (6.13) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     |     | i j | ij  |     |        |
|     |     |     |     |     | i j |     |     |     |        |
and
X
|     |     |     |     |     | b = | x b |     |     | (6.14) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
i i
i
Cubic equation of state with Huron-Vidal mixing rules (CEoS-HV)
•
Cubic equations of state are widely used due to their simplicity. Peng-Robinson (Peng
and Robinson, 1976) and Soave-Redlich-Kwong (Soave, 1972) are expressed with the
same equation:
|     |     |     |     | RT  |         | a(T) |       |     |        |
| --- | --- | --- | --- | --- | ------- | ---- | ----- | --- | ------ |
|     |     |     | p = |     |         |      |       |     | (6.15) |
|     |     |     |     | v b | − (v +δ | b)(v | +δ b) |     |        |
|     |     |     |     |     |         | 1    | 2     |     |        |
−
with
|     |     |       |     |     |     |     |       |     |        |
| --- | --- | ------ | --- | --- | --- | --- | ------ | --- | ------ |
|     |     | 1+√2 |     | PR  |     |     | 1 √2 | PR  |        |
|     | δ   | =      |     |     |     | δ   | = −    |     | (6.16) |
|     | 1   |        |     |     |     | 2   |        |     |        |
|     |     |  1   |     | SRK |     |     |  0   | SRK |        |
and
|     |     |     |     |     | 1   | 1+δ |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
|     |     |     |     | ∆ = |     | ln  |     |     | (6.17) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
|     |     |     |     |     | δ δ | 1+δ |     |     |        |
|     |     |     |     |     | 2 1 |     | 1   |     |        |
−
To apply a CEoS on a mixture with polar components the Huron-Vidal mixing rules
(Huron and Vidal, 1979) are used, based on a modified NRTL excess energy function:
|     |     |     |     | a   | X a  |     | 1 gE,∞ |     |        |
| --- | --- | --- | --- | --- | ---- | --- | ------ | --- | ------ |
|     |     |     |     | =   | i    |     |        |     | (6.18) |
|     |     |     | bRT |     | b RT | −   | ∆ RT   |     |        |
i i
with
|     |     |      |     |     | P     | (cid:16) | Cji (cid:17)          |     |        |
| --- | --- | ---- | --- | --- | ----- | -------- | --------------------- | --- | ------ |
|     |     |      |     |     | x b   | exp      | α C                   |     |        |
|     |     | gE,∞ |     | X   | j j j |          | jiRT                  | ji  |        |
|     |     |      | =   | x   |       |          | −                     |     | (6.19) |
|     |     |      |     | i   | P     |          | (cid:16) Cji (cid:17) |     |        |
|     |     |      |     |     | x     | b exp    | α                     |     |        |
|     |     |      |     | i   | j j   | j        | jiRT                  |     |        |
−

124 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
where:
C HV-NRTL energy interaction parameter between components i and j
ij
α HV-NRTL non-randomness parameter between components i and j
ij
The advantage of the modified NRTL equation is that we can reduce the mixing rules
to the classical van der Waals mixing rules by the following relations (Huron and Vidal,
1979):
a
i
|     |     |     | α   | = 0 | C   | = g | g   | g   | = ∆ |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | ij  |     | ji  | ji  | ii  | ii  |     |     |     |
|     |     |     |     |     |     |     | −   |     | −b  |     |     |
i
|     |     |     |     |     | q   |     |     |     |     |     | (6.20) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
b b
i j
|     |            |     |     | g   | = 2 |        | √g g  | (1      | k ) |     |     |
| --- | ---------- | --- | --- | --- | --- | ------ | ----- | ------- | --- | --- | --- |
|     |            |     |     | ji  | − b | +b     | ii jj | −       | ij  |     |     |
|     |            |     |     |     |     | i j    |       |         |     |     |     |
| 6.2 | Regression |     |     | for | DME | binary |       | systems |     |     |     |
Parameters were regressed for CPA and CEoS-HV using experimental data of binary
systems of DME with different compounds. The binary systems are presented in Table
6.1 and are divided into 2 groups, DME/water and DME/hydrocarbon or inert gas. The
same critical constants were used for both CPA and CEoS-HV. CPA pure component
| parameters | are reported |     | in  | Table | 6.2, where | Γ   | is given | by: |     |     |     |
| ---------- | ------------ | --- | --- | ----- | ---------- | --- | -------- | --- | --- | --- | --- |
a
|     |     |     |     |     |     | Γ = | 0   |     |     |     | (6.21) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
bR
Table 6.1: Experimental data of DME binaries used in the regressions.
|     |     | Binary |     |     |     |     | T range(K) |     | prange(bar) | Points | Type |
| --- | --- | ------ | --- | --- | --- | --- | ---------- | --- | ----------- | ------ | ---- |
p-y-x,p-x-x0
|     | water(PozoandStreett,1984) |     |     |     |     | 323.15 |     | 394.21 | 0.12 346.81 | 74  |     |
| --- | -------------------------- | --- | --- | --- | --- | ------ | --- | ------ | ----------- | --- | --- |
|     |                            |     |     |     |     |        | −   |        | −           |     |     |
methane(Garcia-Sanchezetal.,1987) 282.9 343.8 19.7 123.6 23 p-y-x
|     |     |     |     |     |     |     | −   |     | −   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
propane(Horstmannetal.,2003;GilesandWilson,2000) 273.15 313.39 2.663 13.868 93 p-x,p-y-x
|     |     |     |     |     |     |     | −   |     | −   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n-butane(PozodeFerna´ndezetal.,1992) 282.96 414.5 1.474 48.2 154 p-y-x
|     |     |     |     |     |     |     | −   |     | −   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n-pentane(OutcaltandLemmon,2013) 269.99 380 1.8326 27.502 34 T-p
|     |                          |     |     |     |     |     | −      |     | −              |     |     |
| --- | ------------------------ | --- | --- | --- | --- | --- | ------ | --- | -------------- | --- | --- |
|     | n-decane(Parketal.,2007) |     |     |     |     |     | 323.15 |     | 0.0118 11.4231 | 39  | p-x |
−
|     | n-dodecane(Parketal.,2007) |     |     |     |     |     | 323.15 |     | 0.002 11.4339 | 36  | p-x |
| --- | -------------------------- | --- | --- | --- | --- | --- | ------ | --- | ------------- | --- | --- |
−
|     | CO 2                  | (Laursenetal.,2003) |     |     |     | 298.15 |     | 320.15 | 6 73.2  | 27  | p-y-x |
| --- | --------------------- | ------------------- | --- | --- | --- | ------ | --- | ------ | ------- | --- | ----- |
|     |                       |                     |     |     |     |        | −   |        | −       |     |       |
|     | N (Laursenetal.,2003) |                     |     |     |     | 298.15 |     | 318.15 | 6 103.5 | 34  | p-y-x |
2
|     |     |     |     |     |     |     | −   |     | −   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The objective function to be minimized in the regression is the sum of all deviations
from experimental data: pressure and compositions in VLE, LLE. Deviations ∆X are
i
| calculated | as: |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 125
|     |     |     | Table | 6.2: | Pure | component |     | parameters | for CPA. |     |     |     |
| --- | --- | --- | ----- | ---- | ---- | --------- | --- | ---------- | -------- | --- | --- | --- |
103
|     |     | Component |     |     |     | T c (K) | Γ(K) | b(L/mol) | c 1 | (cid:15)/R (K) | β   | Scheme |
| --- | --- | --------- | --- | --- | --- | ------- | ---- | -------- | --- | -------------- | --- | ------ |
×
DME(TsivintzelisandKontogeorgis,2014) 400.1 2045.568 0.0496 0.72125 0 0 -
water(Kontogeorgisetal.,1999) 647.29 1017.338 0.014515 0.67359 2003.248 69.2 4C
methane(Tsivintzelisetal.,2011) 190.56 959.028 0.0291 0.44718 0 0 -
propane(Yakoumisetal.,1997) 369.83 1896.453 0.057834 0.6307 0 0 -
n-butane(Yakoumisetal.,1997) 425.18 2193.083 0.072081 0.70771 0 0 -
n-pentane(Yakoumisetal.,1997) 469.7 2405.105 0.091008 0.79858 0 0 -
n-decane(Yakoumisetal.,1997) 617.7 3190.542 0.17865 1.13243 0 0 -
n-dodecane(Tsivintzelisetal.,2011) 658 3471.038 0.21624 1.19531 0 0 -
CO (Tsivintzelisetal.,2010) 304.21 1551.222 0.0272 0.7602 0 0 -
2
|     | N   | (Folasetal.,2006) |     |     |     | 126.2 | 634.07 | 0.02605 | 0.49855 | 0   | 0   | -   |
| --- | --- | ----------------- | --- | --- | --- | ----- | ------ | ------- | ------- | --- | --- | --- |
2
|     |     |     |     | (cid:12) | (cid:12)Xexp | Xcalc | (cid:12) |     |     |     |     |     |
| --- | --- | --- | --- | --------- | ------------ | ----- | -------- | --- | --- | --- | --- | --- |
(cid:12)
|     |     |     |     |  | (cid:12) i | − i | (cid:12) | X is | pressure |     |     |     |
| --- | --- | --- | --- | -------- | ---------- | --- | -------- | ---- | -------- | --- | --- | --- |
|     |     |     |     |          | (cid:12)   | exp | (cid:12) |      |          |     |     |     |
X
|     |     |     |     |     | (cid:12) | i   | (cid:12) |     |     |     |     |        |
| --- | --- | --- | --- | --- | -------- | --- | -------- | --- | --- | --- | --- | ------ |
|     |     |     | ∆X  | =   |          |     |          |     |     |     |     | (6.22) |
i
|     |     |     |     |  | (cid:12)    | ex p  | ca lc | (cid:12)      |             |     |     |     |
| --- | --- | --- | --- | -------- | ----------- | ----- | ----- | ------------- | ----------- | --- | --- | --- |
|     |     |     |     |          | (cid:12)    | X     | X     | (cid:12)      |             |     |     |     |
|     |     |     |     |          | (cid:12)    | i −   | i     | (cid:12) X is | composition |     |     |     |
|     |     |     |     |          | (cid:12)min | e xp  |       | exp) (cid:12) |             |     |     |     |
|     |     |     |     |          |             | (X ,1 | X     |               |             |     |     |     |
|     |     |     |     |          | (cid:12)    | i     | i     | (cid:12)      |             |     |     |     |
−
DME/water
DME/water phase equilibrium data exhibit two vapor-liquid and one liquid-liquid region.
Tsivintzelis and Kontogeorgis (2014) presented CPA modeling of this binary at two
temperatures. The reason their parameters are not used in this work is because we
regressed experimental data at four temperatures. A number of different regression
| strategies | was | attempted |     | for | CPA: |     |     |     |     |     |     |     |
| ---------- | --- | --------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
regress two parameters for all temperatures: k and β using Eq. 6.12 to calculate
| •   |     |     |     |     |     |     |     | ij  | cross |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
(cid:15)
cross
| regress |     | three | parameters |     | for all | temperatures: |     | k , β    | and (cid:15) |     |     |     |
| ------- | --- | ----- | ---------- | --- | ------- | ------------- | --- | -------- | ------------ | --- | --- | --- |
|         |     |       |            |     |         |               |     | ij cross | cross        |     |     |     |
•
regress k for each temperature using constant β and Eq. 6.12 to calculate (cid:15)
|     |     | ij  |     |     |     |     |     | cross |     |     |     | cross |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- |
•
| and for | CEoS-HV: |       |            |     |         |               |     |       |       |     |     |     |
| ------- | -------- | ----- | ---------- | --- | ------- | ------------- | --- | ----- | ----- | --- | --- | --- |
| regress |          | three | parameters |     | for all | temperatures: |     | C , C | and α |     |     |     |
|         |          |       |            |     |         |               |     | ij    | ji ij |     |     |     |
•
| regress |     | C and | C   | for each | temperature |     | using | constant | α   |     |     |     |
| ------- | --- | ----- | --- | -------- | ----------- | --- | ----- | -------- | --- | --- | --- | --- |
|         |     | ij    | ji  |          |             |     |       |          | ij  |     |     |     |
•
Tables 6.3 and 6.4 show the parameters for each model and regression strategy. In Figure
6.2 calculations with CPA and SRK-HV are compared with experimental data. In general,
the two VLE branches of the curves are represented well by all models, but temperature
dependent parameters give better results for the LLE curves (Figures 6.2e and 6.2f).
The worst results are obtained when only two temperature independent parameters are
regressed for CPA, especially when predicting solubility of water in the DME-rich phase
| and DME |     | in the | water-rich |     | phase. |     |     |     |     |     |     |     |
| ------- | --- | ------ | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |

126 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
Table 6.3: Regressed parameters for DME/water using CPA (non-regressed parameters in
parentheses).
|     |     |     | T (K)  | k       | β        | (cid:15) /R | (K) |     |
| --- | --- | --- | ------ | ------- | -------- | ----------- | --- | --- |
|     |     |     |        | ij      | cross    | cross       |     |     |
|     |     |     | all    | -0.0967 | 0.3799   | (1001.624)  |     |     |
|     |     |     | all    | -0.1250 | 0.1438   | 1287.500    |     |     |
|     |     |     | 323.15 | -0.1274 | (0.3799) | (1001.624)  |     |     |
|     |     |     | 348.15 | -0.1066 | (0.3799) | (1001.624)  |     |     |
|     |     |     | 373.26 | -0.0937 | (0.3799) | (1001.624)  |     |     |
|     |     |     | 394.21 | -0.0807 | (0.3799) | (1001.624)  |     |     |
Table 6.4: Regressed parameters for DME/water using PR and SRK with HV mixing
|        |         | rules  | (non-regressed |     | parameters | in parentheses). |          |          |
| ------ | ------- | ------ | -------------- | --- | ---------- | ---------------- | -------- | -------- |
| T (K)  |         |        | PR             |     |            |                  | SRK      |          |
|        | C       | /R (K) | C /R           | (K) | α          | C /R (K)         | C /R (K) | α        |
|        | ij      |        | ji             |     | ij         | ij               | ji       | ij       |
| all    | 2104.07 |        | -1916.56       |     | 0.0950     | 2147.48          | -1986.72 | 0.0923   |
| 323.15 | 2293.17 |        | -2047.16       |     | (0.0950)   | 2376.86          | -2147.05 | (0.0923) |
| 348.15 | 2036.05 |        | -1851.43       |     | (0.0950)   | 2136.14          | -1974.91 | (0.0923) |
| 373.26 | 1940.59 |        | -1773.66       |     | (0.0950)   | 2049.42          | -1907.38 | (0.0923) |
| 394.21 | 1511.54 |        | -1295.47       |     | (0.0950)   | 1643.92          | -1479.10 | (0.0923) |

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 127
| 25  |     |     | 300 |     |     |
| --- | --- | --- | --- | --- | --- |
| 20  |     |     | 250 |     |     |
)rab(erusserP
)rab(erusserP 200
15
150
10
100
5
50
| 0     |                 |       | 0     |                 |       |
| ----- | --------------- | ----- | ----- | --------------- | ----- |
| 0 0.2 | 0.4 0.6         | 0.8 1 | 0 0.2 | 0.4 0.6         | 0.8 1 |
|       | DMEmolefraction |       |       | DMEmolefraction |       |
|       | (a)             |       |       | (b)             |       |
25
300
250
20
)rab(erusserP
)rab(erusserP 200
15
150
10
100
5
50
| 0     |         |       | 0     |         |       |
| ----- | ------- | ----- | ----- | ------- | ----- |
| 0 0.2 | 0.4 0.6 | 0.8 1 | 0 0.2 | 0.4 0.6 | 0.8 1 |
DMEmolefraction
DMEmolefraction
|     | (c) |     |     | (d) |     |
| --- | --- | --- | --- | --- | --- |
25
300
| 20            |     |               | 250 |     |     |
| ------------- | --- | ------------- | --- | --- | --- |
| )rab(erusserP |     | )rab(erusserP | 200 |     |     |
15
150
10
100
5
50
| 0     |                 |       | 0     |                 |       |
| ----- | --------------- | ----- | ----- | --------------- | ----- |
| 0 0.2 | 0.4 0.6         | 0.8 1 | 0 0.2 | 0.4 0.6         | 0.8 1 |
|       | DMEmolefraction |       |       | DMEmolefraction |       |
|       | (e)             |       |       | (f)             |       |
Figure 6.2: DME/water modeling with CPA and SRK-HV: (a, b) regressed k , β for
ij cross
CPA, (c, d) regressed k , β , (cid:15) for CPA and C , C , α for SRK-HV, (d, e)
|     | ij  | cross cross | ij ji | ij  |     |
| --- | --- | ----------- | ----- | --- | --- |
regressed k = f(T) for CPA and C ,C = f(T) for SRK-HV [experimental data at
| ij  |     | ij ji |     |     |     |
| --- | --- | ----- | --- | --- | --- |
323.15 K ( ), 348.15 K ( ), 373.26 K ( ), 394.21 K ( ), calculations with CPA ( ),
|     | calculations | with SRK-HV | ( )]. |     |     |
| --- | ------------ | ----------- | ----- | --- | --- |

128 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
| DME/hydrocarbon |     | and | inert | gas |     |     |     |     |
| --------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
For the DME binaries with hydrocarbons (HC) or inert gases, a binary interaction
parameter was was enough to describe adequately the experimental data at different
temperatures. For the CEoS-HV approach, we did not regress the HV parameters C , C
ij ji
and α . Instead, we regressed a temperature independent k using the corresponding EoS.
|     | ij  |     |     |     |     | ij  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Eq. 6.20 can be then used to determine the HV parameters. Performance of the models is
similar (Figures 6.3a to 6.9) except for the higher temperatures in the DME/n-butane
mixture. In Figures 6.5c, 6.5d, 6.6c and 6.6d there are isotherms that correspond to higher
temperatures than pure DME critical temperature (400.1 K). CPA could not describe
properly equilibrium around the critical point. Nevertheless, this is not a problem of the
binary modeling but requires different parametrization for the pure components.
Table 6.5: Regressed parameters for DME/HC, DME/CO and DME/N using CPA, PR
|     |     |     |     |     |     | 2   | 2   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
and SRK.
|     |     | DME   | binary | CPA k  | PR k    | SRK k   |     |     |
| --- | --- | ----- | ------ | ------ | ------- | ------- | --- | --- |
|     |     |       |        | ij     | ij      | ij      |     |     |
|     |     | C1    |        | 0.0194 | 0.0401  | 0.0299  |     |     |
|     |     | C3    |        | 0.0477 | 0.0486  | 0.0490  |     |     |
|     |     | n-C4  |        | 0.0437 | 0.0425  | 0.0455  |     |     |
|     |     | n-C5  |        | 0.0382 | 0.0402  | 0.0404  |     |     |
|     |     | n-C10 |        | 0.0179 | 0.0174  | 0.0194  |     |     |
|     |     | n-C12 |        | 0.0107 | 0.0091  | 0.0117  |     |     |
|     |     | CO    |        | 0.0019 | -0.0066 | -0.0070 |     |     |
2
|     |     | N   |     | 0.0495 | 0.1063 | 0.0968 |     |     |
| --- | --- | --- | --- | ------ | ------ | ------ | --- | --- |
2
100
150
120
10
)rab(erusserP
|     | 90  |     |     |     | eulav-K |     |         |     |
| --- | --- | --- | --- | --- | ------- | --- | ------- | --- |
|     | 60  |     |     |     |         |     | Methane |     |
1
DME
30
0.1
|     | 0     |     |         |     | 1   | 10  | 100 | 1000 |
| --- | ----- | --- | ------- | --- | --- | --- | --- | ---- |
|     | 0 0.2 | 0.4 | 0.6 0.8 | 1   |     |     |     |      |
Pressure(bar)
Methanemolefraction
|     |     | (a) |     |     |     | (b) |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 6.3: DME/methane modeling with CPA and SRK: (a) p-y-x diagram, (b) K-values
[experimental data at 282.9 K ( ), 313.3 K ( ), 343.8 K ( ), calculations with CPA ( ),
|     |     |     | calculations | with | SRK ( | )]. |     |     |
| --- | --- | --- | ------------ | ---- | ----- | --- | --- | --- |

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 129
20
15
10
5
0
0 0.2 0.4 0.6 0.8 1
Propane mole fraction
)rab(
erusserP
(a)
16
14
12
10
8
0 0.2 0.4 0.6 0.8 1
Propane mole fraction
)rab(
erusserP
2.5
2.0
1.5
Propane
1.0
DME
0.5
0
8 10 12 14 16
Pressure (bar)
(b)
eulav-K
(c)
Figure 6.4: DME/propane modeling with CPA and SRK: (a, b) p-y-x diagram, (c)
K-values [experimental data at 273.15 K ( ), 298.15 K ( ), 313.10 ( ), 323.15 K ( ), 313.39
K ( ), calculations with CPA ( ), calculations with SRK ( )].

130 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
| 10  |     |     | 30  |     |     |
| --- | --- | --- | --- | --- | --- |
25
8
| )rab( |     | )rab( | 20  |     |     |
| ----- | --- | ----- | --- | --- | --- |
6
| erusserP |     | erusserP | 15  |     |     |
| -------- | --- | -------- | --- | --- | --- |
4
10
2
5
| 0     |                   |       | 0     |                   |       |
| ----- | ----------------- | ----- | ----- | ----------------- | ----- |
| 0 0.2 | 0.4 0.6           | 0.8 1 | 0 0.2 | 0.4 0.6           | 0.8 1 |
|       | DME mole fraction |       |       | DME mole fraction |       |
|       | (a)               |       |       | (b)               |       |
| 60    |                   |       | 60    |                   |       |
50
50
| )rab( 40    |     | )rab(    |     |     |     |
| ----------- | --- | -------- | --- | --- | --- |
| erusserP 30 |     | erusserP | 40  |     |     |
20
30
10
| 0     |                   |       | 20    |                   |       |
| ----- | ----------------- | ----- | ----- | ----------------- | ----- |
| 0 0.2 | 0.4 0.6           | 0.8 1 | 0 0.2 | 0.4 0.6           | 0.8 1 |
|       | DME mole fraction |       |       | DME mole fraction |       |
|       | (c)               |       |       | (d)               |       |
Figure 6.5: DME/n-butane modeling with CPA and SRK: (a, b) p-y-x diagram
[experimental data at 282.96 K ( ), 297.86 K ( ), 312.98 K ( ), 328.01 K ( ), 343.07 K ( ),
353.65 K ( )], (c, d) p-y-x diagram [experimental data at 372.87 K ( ), 387.22 K ( ),
402.71 K ( ), 405.16 K ( ), 414.50 K ( )] [calculations with CPA ( ), calculations with
|     |     | SRK ( | )]. |     |     |
| --- | --- | ----- | --- | --- | --- |

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 131
4
3.0
2.5
3
2.0
eulav-K
eulav-K
2
1.5
DME
1.0
|     |     |     | DME |     |     | n-Butane |     |
| --- | --- | --- | --- | --- | --- | -------- | --- |
1
n-Butane
0.5
| 0   |          |       |     | 0   |          |       |     |
| --- | -------- | ----- | --- | --- | -------- | ----- | --- |
| 0 2 | 4 6      | 8 10  | 12  | 0 6 | 12 18    | 24 30 | 36  |
|     | Pressure | (bar) |     |     | Pressure | (bar) |     |
|     | (a)      |       |     |     | (b)      |       |     |
2.5
1.75
| 2.0     |     |     |         | 1.50 |     |     |     |
| ------- | --- | --- | ------- | ---- | --- | --- | --- |
| eulav-K |     |     | eulav-K |      |     |     |     |
1.5
1.25
| 1.0 |     |     | DME |     |     |     | DME |
| --- | --- | --- | --- | --- | --- | --- | --- |
1.00
|       |          | n-Butane |     |       |               | n-Butane |     |
| ----- | -------- | -------- | --- | ----- | ------------- | -------- | --- |
| 0.5   |          |          |     | 0.75  |               |          |     |
| 10 20 | 30 40    | 50 60    | 70  |       |               |          |     |
|       |          |          |     | 20 30 | 40            | 50 60    | 70  |
|       | Pressure | (bar)    |     |       | Pressure(bar) |          |     |
|       | (c)      |          |     |       | (d)           |          |     |
Figure 6.6: DME/n-butane modeling with CPA and SRK: (a, b) K-values [experimental
data at 282.96 K ( ), 297.86 K ( ), 312.98 K ( ), 328.01 K ( ), 343.07 K ( ), 353.65 K ( )],
(c, d) K-values [experimental data at 372.87 K ( ), 387.22 K ( ), 402.71 K ( ), 405.16 K
( ), 414.50 K ( )] [calculations with CPA ( ), calculations with SRK ( )].

132 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
30
25
)rab(erusserP
20
15
10
5
0
|     | 250 | 275 300 325 | 350 375 | 400 |     |
| --- | --- | ----------- | ------- | --- | --- |
|     |     | Temperature | (K)     |     |     |
(a)
| 12         |                   |          | 12    |                   |       |
| ---------- | ----------------- | -------- | ----- | ----------------- | ----- |
| 10         |                   |          | 10    |                   |       |
| )rab( 8    |                   | )rab(    | 8     |                   |       |
| erusserP 6 |                   | erusserP | 6     |                   |       |
| 4          |                   |          | 4     |                   |       |
| 2          |                   |          | 2     |                   |       |
| 0          |                   |          | 0     |                   |       |
| 0 0.2      | 0.4 0.6           | 0.8 1    | 0 0.2 | 0.4 0.6           | 0.8 1 |
|            | DME mole fraction |          |       | DME mole fraction |       |
|            | (b)               |          |       | (c)               |       |
Figure 6.7: DME/hydrocarbon modeling with CPA and SRK for: (a) n-pentane, (b)
n-decane, (c) n-dodecane [experimental data at x = 0.392 ( ), x = 0.679 ( ),
DME DME
323.15 K ( ), calculations with CPA ( ), calculations with SRK ( )].

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 133
8
100
| 80  |     |     |     |     | 6   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
)rab(erusserP
| 60  |     |     |     | eulav-K |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --- | --- |
4
40
2
| 20  |     |     |     |     |     |     |     | CO2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
DME
0
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   | 0   | 20 40    | 60    | 80 100 |
| ----- | --- | --- | --- | --- | --- | -------- | ----- | ------ |
|       |     |     |     |     |     | Pressure | (bar) |        |
CO 2 molefraction
|     | (a) |     |     |     |     |     | (b) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 6.8: DME/carbon dioxide modeling with CPA and SRK: (a) p-y-x diagram, (b)
K-values [experimental data at 298.15 K ( ), 308.65 K ( ), 320.15 K ( ), calculations with
|     |     | CPA ( | ), calculations | with | SRK  | ( )]. |     |     |
| --- | --- | ----- | --------------- | ---- | ---- | ----- | --- | --- |
| 600 |     |       |                 |      | 1000 |       |     |     |
500
100
)rab(erusserP 400
eulav-K
| 300 |     |     |     |     | 10  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
200
N2
1
DME
100
0.1
0
| 0 0.2 | 0.4            | 0.6 | 0.8 | 1   | 1   | 10            | 100 | 1000 10000 |
| ----- | -------------- | --- | --- | --- | --- | ------------- | --- | ---------- |
|       | N molefraction |     |     |     |     | Pressure(bar) |     |            |
2
|     | (a) |     |     |     |     |     | (b) |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 6.9: DME/nitrogen modeling with CPA and SRK: (a) p-y-x diagram, (b) K-values
[experimental data at 298.15 K ( ), 308.15 K ( ), 318.15 K ( ), calculations with CPA
|     |     | (   | ), calculations | with | SRK | ( )]. |     |     |
| --- | --- | --- | --------------- | ---- | --- | ----- | --- | --- |

134 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
Table 6.6 shows the deviations for all the binaries and regression approaches. The error
of the calculation is expressed in terms of average absolute relative deviations. Absolute
relative deviation is given by:
(cid:12) (cid:12)Xexp Xcalc (cid:12) (cid:12)
ARD = (cid:12) i − i (cid:12) (6.23)
i (cid:12) Xexp (cid:12)
(cid:12) i (cid:12)
The formula implies that no experimental point is zero. The average absolute relative
deviation is calculated by:
1 N
X
AARD = ARD (6.24)
i
N
i=1
where:
N number of experimental points
The comparisons were made with experimental pressure and the mole fraction of DME in
the vapor phase, the liquid phase of VLE, and the two liquid phases of LLE (whenever
possible). Regression errors are acceptable and the modeling of the systems satisfactory.
Larger deviations appear for DME liquid phase mole fractions in DME/water VLE, because
the values of the mole fractions are small (Eq. 6.23 will result in larger values for the
same absolute deviations). Finally, CPA in DME/n-butane has larger deviations than
the two CEoS. This is a problem of pure component parametrization, that does not allow
CPA to capture the correct behavior around the critical point (Figures 6.5c, 6.5d, 6.6c
and 6.6d).
In general, it seems that CPA and CEoS-HV lead to equilibrium curves with similar
deviations from the experimental data (PR-HV and SRK-HV are judged as a group since
they give very similar results). For the purpose intended, we do not expect predictions
with any of the models to yield much different conclusions. If conditions are not close
to the critical region, CPA can model the binaries more than adequately. At the time
of calculations, a CPA fugacity coefficient routine was more accessible therefore CPA
was chosen to make predictions for the partitioning of DME, namely the K-value. For
DME/water, the temperature dependent k were selected. HV multicomponent mixing
ij
rules would require modifications in the routines to differentiate between water and
hydrocarbons/inert gases. The parameters of the later are not supplied to the routine but
must be calculated from Eq. 6.20.

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 135
Table 6.6: Average absolute relative deviations for DME binaries considering different
models and regression strategies (LLE-1: water-rich liquid, LLE-2: DME-rich liquid).
| System | Model | Regression | parameters | %∆p %∆y    | %∆x  | %∆x   | %∆x   |
| ------ | ----- | ---------- | ---------- | ---------- | ---- | ----- | ----- |
|        |       |            |            |            | VLE  | LLE-1 | LLE-2 |
|        | CPA   | k ,βAiBj   |            | 1.50 26.71 | 2.81 | 6.26  | 4.36  |
ij
|     | CPA | k ,βAiBj,(cid:15)AiBj |     | 0.62 26.46 | 1.80 | 11.99 | 4.94 |
| --- | --- | --------------------- | --- | ---------- | ---- | ----- | ---- |
ij
|     | CPA | k =f(T) |     | 1.45 11.86 | 2.75 | 16.13 | 2.45 |
| --- | --- | ------- | --- | ---------- | ---- | ----- | ---- |
ij
| DME/Water | PR-HV  | C ,C  | ,α    | 3.51 3.65 | 37.61 | 5.63  | 5.97 |
| --------- | ------ | ----- | ----- | --------- | ----- | ----- | ---- |
|           |        | ij ji | ij    |           |       |       |      |
|           | SRK-HV | C ,C  | ,α    | 2.86 3.95 | 32.35 | 7.20  | 5.31 |
|           |        | ij ji | ij    |           |       |       |      |
|           | PR-HV  | C ,C  | =f(T) | 3.87 3.78 | 31.18 | 12.64 | 2.63 |
ij ji
|     | SRK-HV | C ,C | =f(T) | 3.12 4.05 | 30.59 | 10.20 | 2.32 |
| --- | ------ | ---- | ----- | --------- | ----- | ----- | ---- |
ij ji
|        | CPA | k ij |     | 2.99 2.49 |     |     |     |
| ------ | --- | ---- | --- | --------- | --- | --- | --- |
| DME/C1 | PR  | k ij |     | 2.66 2.91 |     |     |     |
|        | SRK | k    |     | 2.62 2.90 |     |     |     |
ij
|     | CPA | k   |     | 0.67 0.82 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
| DME/C3 | PR  | k   |     | 1.11 1.03 |     |     |     |
| ------ | --- | --- | --- | --------- | --- | --- | --- |
ij
|     | SRK | k   |     | 0.58 0.80 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
|     | CPA | k   |     | 1.18 8.18 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
| DME/n-C4 | PR  | k   |     | 1.20 2.59 |     |     |     |
| -------- | --- | --- | --- | --------- | --- | --- | --- |
ij
|     | SRK | k   |     | 0.88 2.69 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
|     | CPA | k   |     | 2.63 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
ij
| DME/n-C5 | PR  | k   |     | 2.61 |     |     |     |
| -------- | --- | --- | --- | ---- | --- | --- | --- |
ij
|     | SRK | k   |     | 2.56 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
ij
|     | CPA | k   |     | 1.35 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
ij
| DME/n-C10 | PR  | k   |     | 1.27 |     |     |     |
| --------- | --- | --- | --- | ---- | --- | --- | --- |
ij
|     | SRK | k   |     | 1.29 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
ij
|           | CPA | k ij |     | 2.39 |     |     |     |
| --------- | --- | ---- | --- | ---- | --- | --- | --- |
| DME/n-C12 | PR  | k ij |     | 2.09 |     |     |     |
|           | SRK | k    |     | 1.78 |     |     |     |
ij
|     | CPA | k   |     | 2.73 1.68 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
| DME/CO | PR  | k   |     | 1.33 0.95 |     |     |     |
| ------ | --- | --- | --- | --------- | --- | --- | --- |
|        | 2   | ij  |     |           |     |     |     |
|        | SRK | k   |     | 1.36 0.94 |     |     |     |
ij
|     | CPA | k   |     | 3.80 2.11 |     |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- |
ij
| DME/N | PR  | k   |     | 4.18 1.93 |     |     |     |
| ----- | --- | --- | --- | --------- | --- | --- | --- |
| 2     |     | ij  |     |           |     |     |     |
|       | SRK | k   |     | 4.10 2.35 |     |     |     |
ij

136 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
6.3 Predictions of DME partitioning between water
and oil
The experimental data of the DME binaries were captured successfully and therefore the
next step is to predict the equilibrium behavior of DME/water/hydrocarbon mixtures.
CEoS-HV could serve the same purpose, but in this work all predictions were made with
CPA. As a first step, ternary mixture behavior will be predicted. In Figures 6.10 to 6.12
ternary mixtures of DME/water/hydrocarbon are shown at the same conditions. Binary
interaction parameters for water/hydrocarbons were taken from Paterson (2017). Methane
is the only hydrocarbon that allows the existence of two VLE and one VLLE region, as it
is the lightest hydrocarbon. The number of degrees of freedom is zero in the VLLE regions
at specified temperature and pressure with unique compositions of the vapor and the two
liquid phases. The LLE curves of all hydrocarbons are presented in the same ternary figure
(Figure 6.13). It appears that the nature of the hydrocarbon does not have a prominent
effect on the overall equilibrium. Even for the DME/water/methane ternary where more
complicated equilibria are observed, LLE boundaries are close to those of the remaining
hydrocarbons. This implies that the K-values of DME between oil and water are not likely
to have a strong dependence on the hydrocarbon concentration in the oil.
To test this hypothesis, we perform the following test. A light, intermediate and heavy
hydrocarbon are chosen to represent the oil. For different hydrocarbon (methane, n-butane
and n-decane) composition and DME concentration in the feed, we calculate the K-values
at equilibrium. The constraint in these calculations is to use as little water as possible in
the feed, which will result in a water-rich incipient phase (phase fraction < 10−5). This
leads to an oil phase with practically the same composition as the feed. The only case
where this is not possible, is when the oil is too light to exist only as a liquid and we have
separation into a vapor phase as well. Binary interaction parameters for methane/n-butane
and methane/n-decane are -0.0005 and 0.0067 respectively, both regressed using databases
developed in the work of Varzandeh (2017).
Figures 6.14 and 6.15 show the DME K-value between the oil and the aqueous phase, as a
function of the oil composition in the feed. Each figure corresponds to constant DME in
the feed. Because of the calculation procedure, the DME concentration is essentially the
DME in the oil phase if there is only LLE (oil-rich liquid and water-rich liquid equilibrium).
Figure 6.14a, 10% of DME in the feed with an incipient water-rich phase results in LLE
when the heavier hydrocarbons dominate. At higher compositions of lighter hydrocarbons,
the oil phase is too light and we have VLLE reducing to VLE at even higher methane
concentrations in the absence of n-decane. Figures 6.14b and 6.15a show that by increasing
DME in the feed, VLE disappears and the VLLE region shrinks. Finally at 70% DME
(Figure 6.15b) in the feed, the only equilibrium that can be established is LLE at the
current conditions regardless of the oil composition.

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 137
0
1
0.2
0.8
0.4
|     | r   |     |     | 0.6 D |     |
| --- | --- | --- | --- | ----- | --- |
t e
|     | a   |     |     | M   |     |
| --- | --- | --- | --- | --- | --- |
|     | W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0   | 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| --- | --- | --- | --- | --- | --- |
Methane
(a)
0
1
0.2
0.8
0.4
|     | r   |     |     | 0.6 D |     |
| --- | --- | --- | --- | ----- | --- |
t e
|     | a   |     |     | M   |     |
| --- | --- | --- | --- | --- | --- |
|     | W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0   | 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| --- | --- | --- | --- | --- | --- |
Propane
(b)
Figure 6.10: Ternary diagram of DME/water at 323.15 and 100 bar with: (a) methane,
(b) propane [binodal curves for LLE ( ), VLE (DME-rich liquid) ( ), VLE
(water-rich liquid) ( ), tie lines ( ), LLE region ( ), VLE (DME-rich liquid) region
| ( ), VLE | (water-rich | liquid) region | (   | ), VLLE region | ( )]. |
| -------- | ----------- | -------------- | --- | -------------- | ----- |

138 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
0
1
0.2
0.8
0.4
| r   |     |     | 0.6 D |     |
| --- | --- | --- | ----- | --- |
e
| a t |     |     | M   |     |
| --- | --- | --- | --- | --- |
| W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Butane
(a)
0
1
0.2
0.8
0.4
| r   |     |     | 0.6 D |     |
| --- | --- | --- | ----- | --- |
e
| a t |     |     | M   |     |
| --- | --- | --- | --- | --- |
| W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Pentane
(b)
Figure 6.11: Ternary diagram of DME/water at 323.15 and 100 bar with: (a) n-butane,
(b) n-pentane [binodal curve ( ), tie lines ( ), LLE region ( )].

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 139
0
1
0.2
0.8
0.4
| r   |     |     | 0.6 D |     |
| --- | --- | --- | ----- | --- |
e
| a t |     |     | M   |     |
| --- | --- | --- | --- | --- |
| W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Decane
(a)
0
1
0.2
0.8
0.4
| r   |     |     | 0.6 D |     |
| --- | --- | --- | ----- | --- |
e
| a t |     |     | M   |     |
| --- | --- | --- | --- | --- |
| W   |     |     | E   |     |
0.6
0.4
0.8
0.2
1
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |
| ----- | --- | --- | --- | --- |
n-Dodecane
(b)
Figure 6.12: Ternary diagram of DME/water at 323.15 and 100 bar with: (a) n-decane,
(b) n-dodecane [binodal curve ( ), tie lines ( ), LLE region ( )].

140 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
0
1
0.2
0.8
0.4
e r 0.6 D
a t M
W E
0.6
0.4
0.8
0.2
1
0
0 0.2 0.4 0.6 0.8 1
HC
Figure 6.13: Comparison of LLE binodal curves in DME/water/HC ternaries at 323.15 K
and 100 bar [methane ( ), propane ( ), n-butane ( ), n-pentane ( ), n-decane
( ), n-dodecane ( )].
The common observation of the ternary diagrams is that the K-value does not change much,
and the higher the DME concentration, the less impactful the nature of the hydrocarbon
is. This conclusion may potentially simplify the design and modeling of core flooding
experiments, because the oil composition, based on the predictions, gives very modest
influence on the DME partitioning.
Temperature and pressure effects are presented in Figure 6.16 for a constant oil composition
(30% methane, 30% n-butane, 40% n-decane). Keeping the aqueous phase incipient, we
increase the DME until we reach 100% DME in the oil phase. This is the ending point
of Figures 6.16a and 6.16b, practically DME and traces of oil in the oil phase. In other
words, it is the limiting K-value of the binary DME/water at the conditions specified.
Increasing the pressure causes a slight decrease in the K-value, but change of temperature
leads to larger differences in the distribution ratio of DME. Higher temperatures favor the
partitioning from water into oil, especially at lower to medium DME mole fractions.
Figure 6.16 reveals a maximum DME mole fraction in the oil phase that does not appear
in the work of Ratnakar et al. (2016b,a, 2017). By increasing the DME mole fraction, the
hydrocarbon mole fractions and the oil/water ratio decrease. After the oil is diluted enough
with DME and water, the oil phase cannot dissolve as much DME as before. It decreases
to ultimately reach the DME mole fraction of the DME/water LLE in the DME-rich

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 141
0
|     | VLE |     | 1   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
12
0.2
|     |         |      | 0.8 |     |     | 10  |
| --- | ------- | ---- | --- | --- | --- | --- |
|     | n e 0.4 |      |     |     | M   | 8   |
|     | a       |      |     | 0.6 |     |     |
|     | t       |      |     |     | e t | DME |
|     | u       |      |     |     | h   |     |
|     | B       | VLLE |     |     | a   |     |
|     | n-      |      |     |     | n   |     |
e
6 K-value
0.6
0.4
4
0.8
0.2
LLE
2
1
0
0
|     | 0.2 | 0.4 | 0.6 | 0.8 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| 0   |     |     |     |     | 1   |     |
n-Decane
(a)
0
1
12
0.2
|     |     |     | 0.8 |     |     | 10  |
| --- | --- | --- | --- | --- | --- | --- |
e
|     | n 0.4 | VLLE |     |     | M   | 8   |
| --- | ----- | ---- | --- | --- | --- | --- |
|     | a     |      |     | 0.6 | e   | DME |
|     | t     |      |     |     | t   |     |
|     | u     |      |     |     | h   |     |
|     | B     |      |     |     | a   |     |
|     | n-    |      |     |     | n   |     |
e
6 K-value
0.6
0.4
4
0.8
|     |     | LLE |     |     | 0.2 |     |
| --- | --- | --- | --- | --- | --- | --- |
2
1
0
0
| 0   | 0.2 | 0.4 | 0.6 | 0.8 | 1   |     |
| --- | --- | --- | --- | --- | --- | --- |
n-Decane
(b)
Figure 6.14: K-values of DME partitioning between oil and aqueous phase at 323.15 and
100 bar for different oil composition with DME mole fraction in the feed: (a) z = 0.1 ,
DME
|     |     | (b) | z = | 0.3. |     |     |
| --- | --- | --- | --- | ---- | --- | --- |
DME

142 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
0
1
12
0.2
|     |     | 0.8 |     |     | 10  |
| --- | --- | --- | --- | --- | --- |
VLLE
| n e 0.4 |     |     | M   |     | 8   |
| ------- | --- | --- | --- | --- | --- |
| a       |     |     | 0.6 |     |     |
| t       |     |     | e t |     | DME |
| u       |     |     | h   |     |     |
| B       |     |     | a   |     |     |
| n-      |     |     | n   |     |     |
e
6 K-value
0.6
0.4
|     | LLE |     |     |     | 4   |
| --- | --- | --- | --- | --- | --- |
0.8
0.2
2
1
0
0
| 0.2 | 0.4 | 0.6 | 0.8 |     |     |
| --- | --- | --- | --- | --- | --- |
| 0   |     |     |     | 1   |     |
n-Decane
(a)
0
1
12
0.2
|     |     | 0.8 |     |     | 10  |
| --- | --- | --- | --- | --- | --- |
e
| n 0.4 |     |     | M     |     | 8   |
| ----- | --- | --- | ----- | --- | --- |
| a     |     |     | 0.6 e |     | DME |
| t     |     |     | t     |     |     |
| u     |     |     | h     |     |     |
| B     |     |     | a     |     |     |
| n-    |     |     | n     |     |     |
e
6 K-value
| 0.6 | LLE |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
0.4
4
0.8
0.2
2
1
0
0
| 0 0.2 | 0.4 | 0.6 | 0.8 | 1   |     |
| ----- | --- | --- | --- | --- | --- |
n-Decane
(b)
Figure 6.15: K-values of DME partitioning between oil and aqueous phase at 323.15 and
100 bar for different oil composition with DME mole fraction in the feed: (a) z = 0.5,
DME
|     | (b) | z = | 0.7. |     |     |
| --- | --- | --- | ---- | --- | --- |
DME

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 143
phase, which is practically a limiting oil phase. This change does not mean that DME
stops preferring partitioning in the oil phase, since K-values are larger than 1. Instead,
the “capacity” of the oil phase for DME is lower. This maximum DME concentration in
the oil phase reduces with increasing temperate and pressure, while temperature still has
| a more obvious | effect.           |        |         |     |                   |           |
| -------------- | ----------------- | ------ | ------- | --- | ----------------- | --------- |
| 20             |                   |        |         | 12  |                   |           |
| 16             |                   |        |         | 10  |                   |           |
| eulav-K        |                   |        | eulav-K |     |                   |           |
| 12             |                   |        |         | 8   |                   |           |
| EMD            |                   |        | EMD     |     |                   |           |
| 8              |                   |        |         | 6   |                   |           |
| 4              |                   |        |         | 4   |                   |           |
| 0              |                   |        |         | 2   |                   |           |
| 0              | 0.2 0.4           | 0.6    | 0.8 1   | 0   | 0.2 0.4           | 0.6 0.8 1 |
|                | DME mole fraction | in oil |         |     | DME mole fraction | in oil    |
|                | (a)               |        |         |     | (b)               |           |
Figure 6.16: K-values of DME partitioning between oil (30% methane, 30% n-butane,
40% n-decane) and aqueous phase at: (a) 100 bar [323.15 K ( ), 348.15 K ( ), 373.26
K ( ), 394.21 K ( )], (b) 323.15 K [50 bar ( ), 100 bar ( ), 150 bar ( ), 200
|            |             | bar | ( ), 250 bar | ( )].        |     |     |
| ---------- | ----------- | --- | ------------ | ------------ | --- | --- |
| 6.4 Effect | of salinity |     | on DME       | partitioning |     |     |
Instead of fresh water usually brine is involved in waterflooding. It is also possible for
brine to be the DME carrier during the injection process. Consequently, it is more relevant
to study the DME partitioning between hydrocarbon and brine phases. Models such
as the Electrolyte CPA EoS (eCPA) proposed by Maribo-Mogensen et al. (2015), can
be applied to mixtures of electrolytes under the unified framework of an equation of
state. However, it requires significant effort to implement a complex model like eCPA
into practical simulations. It is advantageous to choose a simpler model to generate
quick results for analysis, which is more easily used for the purpose of simulation. The
treatment of brine is inspired by the study of Søreide and Whitson (1992). Despite
its theoretical non-rigorousness, the approach can account for the major effects of salt
with a simple procedure, particularly suitable for quick implementation in simulators by
slight modification of the existing models. According to their method, brine is treated as
“pseudo-water”, a special form of water. The method predicts the reduced water vapor
pressure in the presence of salt by modifying the a(T) function. This works well far from
the critical point of water but since the critical constants of the “pseudo-water” are not
changed, larger deviations at higher reduced temperatures are expected.

144 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
Brine is modeled as a pseudo-component with the same critical constants and CPA
parameters as water except for c . This parameter is allowed to be a function of salinity
1
and its value is determined through regression of experimental vapor pressures of brine
solution at different mass fractions of NaCl (Haas Jr., 1976). Results are presented in
Table 6.7 with average absolute relative vapor pressure deviations and Figure 6.17.
Table 6.7: Regressed values of CPA c parameter at different NaCl concentrations.
1
%w c %AARD
NaCl 1
2.84 0.68624 0.90
5.00 0.70752 1.30
5.52 0.71108 1.44
8.06 0.74120 1.93
10.00 0.76080 2.35
10.46 0.77208 2.48
12.75 0.79516 3.02
14.92 0.82260 3.59
15.00 0.82468 3.60
16.98 0.85448 4.15
18.95 0.87204 4.75
20.00 0.88464 5.12
Vaporpressuresaredescribedadequatelybythemodelandasexpectedhighertemperatures
exhibit larger deviations. Change of c cannot capture vapor pressure at the critical
1
temperature. More accurate modeling would require correlations of the critical constants
with salinity. For most reservoir applications, the influence is not supposed to be large,
because it will mainly influence the water content in vapor phase.
Forsalinitiesotherthantheonesregressed, arelationshipbetweenc andw ispresented
1 NaCl
in Figure 6.18. For 0% NaCl, we force the equation to give the c of pure water. With
1
such a correlation, experimental data of DME/brine can be regressed (Ratnakar et al.,
2017). Binary interaction parameters are presented in Table 6.8 and model prediction
with experimental data in Figure 6.19.
Figure 6.20 shows how binary interaction parameters change with NaCl mass fraction at
323 K. A liner equation can be fitted to the data to allow predictions at salinities where
experimental data was not available. The equation k = f(w ) was used to predict the
ij NaCl
sensitivity of the K-value with different NaCl concentrations in the brine (Figure 6.21).
For brine/hydrocarbon, k of water/hydrocarbon were used for simplicity. It is evident
ij
that the salting-out effect at larger salinity forces more DME to migrate to the oil phase,
as the aqueous phase becomes more and more undesirable. Not as obvious as in Figure
6.16, a maximum DME mole fraction in the oil phase is identified. In the case of constant
temperature and pressure, this maximum DME mole fraction is eliminated at high salinity.

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 145
| 100              |                |         |               | 100     |                |         |     |
| ---------------- | -------------- | ------- | ------------- | ------- | -------------- | ------- | --- |
| )rab(erusserP 10 |                |         | )rab(erusserP | 10      |                |         |     |
| 1                |                |         |               | 1       |                |         |     |
| 0.1              |                |         |               | 0.1     |                |         |     |
| 350 375          | 400 425        | 450 475 | 500           | 350 375 | 400 425        | 450 475 | 500 |
|                  | Temperature(K) |         |               |         | Temperature(K) |         |     |
|                  | (a)            |         |               |         | (b)            |         |     |
Figure 6.17: Brine vapor pressure modeling with CPA for different w : (a) p-T
NaCl
diagram [experimental data for 2.84% ( ), 5.52% ( ), 10.00% ( ), 12.75% ( ), 15.00% ( ),
18.95% ( )], (b) p-T diagram [experimental data for 5.00% ( ), 8.06% ( ), 10.46% ( ),
14.92% ( ), 16.98% ( ), 20.00% ( )] [calculations with CPA ( )].
0.95
|     |     | c1=2.03667w | 2 +0.67892wNaCl+0.67359 |     |     |     |     |
| --- | --- | ----------- | ----------------------- | --- | --- | --- | --- |
N aCl
0.90 R2=0.9986
AARD=0.50%
0.85
|     | 1   | 0.80 |     |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- |
c
0.75
0.70
0.65
|     |     | 0 0.04 | 0.08 | 0.12 0.16 | 0.2 |     |     |
| --- | --- | ------ | ---- | --------- | --- | --- | --- |
MassfractionofNaCl
Figure 6.18: Correlation of CPA c parameter for different NaCl mass fractions [regressed
1
c ( ), polynomial n = 2 trend line ( ), AARD: average absolute relative deviation of
1
the fitting].
Table 6.8: Regressed k for the pseudo-binary system DME/brine (VLE AARD 3.71%,
ij
|     |     | LLE   | AARD 2.19%). |         |     |     |     |
| --- | --- | ----- | ------------ | ------- | --- | --- | --- |
|     |     | T (K) | %w           | k       |     |     |     |
|     |     |       | NaCl         | ij      |     |     |     |
|     |     | 303   | 10           | -0.0997 |     |     |     |
|     |     | 353   | 10           | -0.0538 |     |     |     |
|     |     | 323   | 3            | -0.1037 |     |     |     |
|     |     | 323   | 10           | -0.0815 |     |     |     |
|     |     | 323   | 17           | -0.0576 |     |     |     |

146 Chapter 6. Phase equilibrium modeling for DME enhanced waterflood
|               | 120   |                  |     |               | 120 |     |                  |       |
| ------------- | ----- | ---------------- | --- | ------------- | --- | --- | ---------------- | ----- |
|               | 100   |                  |     |               | 100 |     |                  |       |
| )rab(erusserP | 80    |                  |     | )rab(erusserP | 80  |     |                  |       |
|               | 60    |                  |     |               | 60  |     |                  |       |
|               | 40    |                  |     |               | 40  |     |                  |       |
|               | 20    |                  |     |               | 20  |     |                  |       |
|               | 0     |                  |     |               | 0   |     |                  |       |
|               | 0 0.2 | 0.4 0.6          | 0.8 | 1             | 0   | 0.2 | 0.4 0.6          | 0.8 1 |
|               |       | DMEmole fraction |     |               |     |     | DMEmole fraction |       |
|               |       | (a)              |     |               |     |     | (b)              |       |
Figure 6.19: DME/brine modeling with CPA: (a) 10% w/w NaCl, (b) 323 K
[experimental data 303 K ( ), 353 ( ), 3% w/w NaCl ( ), 10% w/w NaCl ( ), 17% w/w
|     |     | NaCl | ( )] [calculations |     | with CPA | (   | )]. |     |
| --- | --- | ---- | ------------------ | --- | -------- | --- | --- | --- |
Following the decreasing K-value curve, mole fractions after some aqueous mass fraction of
NaCl show a monotonically increasing trend. Brine is a pseudo-component and therefore
| the | DME mole fraction | can | be considered | as salt-free. |     |     |     |     |
| --- | ----------------- | --- | ------------- | ------------- | --- | --- | --- | --- |
0.04
−
|     |     |     | kij=0.32929wNaCl− | 0.11386 |     |     |     |     |
| --- | --- | --- | ----------------- | ------- | --- | --- | --- | --- |
R2=0.9995
|     |     |     | 0.06 AARD=0.49% |     |     |     |     |     |
| --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
−
ji 0.08
k
−
0.10
−
0.12
−
|     |     |     | 0 0.04 | 0.08 | 0.12 | 0.16 | 0.2 |     |
| --- | --- | --- | ------ | ---- | ---- | ---- | --- | --- |
MassfractionofNaCl
Figure 6.20: Correlation of CPA k for the pseudo-binary DME/brine at 323 K for
ij
different NaCl mass fractions [regressed k ( ), linear trend line ( ), AARD: average
ij
|     |             | absolute | relative | deviation | of the | fitting]. |     |     |
| --- | ----------- | -------- | -------- | --------- | ------ | --------- | --- | --- |
| 6.5 | Conclusions |          |          |           |        |           |     |     |
The DEW process requires adequate phase equilibrium modeling for mixtures of DME
in water and oil. For this reason parameters for CPA and CEoS-HV (PR and SRK)
were regressed using DME binary systems with water, hydrocarbons and inert gases.
Both models resulted in satisfactory phase equilibrium calculations with relatively small

Chapter 6. Phase equilibrium modeling for DME enhanced waterflood 147
35
30
25
20
15
10
5
0 0.2 0.4 0.6 0.8 1
DME mole fraction in oil
eulav-K
EMD
Figure 6.21: K-values of DME partitioning between oil (30% methane, 30% n-butane,
40% n-decane) and aqueous phase at 323 K and 100 bar for different w [3% ( ), 6%
NaCl
( ), 10% ( ), 13% ( ), 17% ( )].
deviations from experimental data. For DME/water, temperature dependent interaction
parameters provided the best fit, while only one temperature independent parameter was
enough in DME/hydrocarbon and DME/inert gas binaries.
Predictions were made for ternary mixtures of DME/water with various hydrocarbons
at the same temperature and pressure. It was observed that the size of the hydrocarbon
had a minor effect on the overall equilibrium. This was validated by K-value calculations
in DME/water/oil mixtures, where the oil was modeled as a ternary system of methane,
n-butane and n-decane. For different oil compositions, the K-values of DME between
the oil and the aqueous phase changed only slightly. This weak dependence of the DME
partitioning on the oil compositions might simplify core flood experiments and DEW
simulations, allowing simpler “model” oils to be used for quick but acceptable estimation
of the DME partitioning. Temperature, pressure and salinity sensitivity of the K-value
was also investigated. Larger K-values are found at higher temperatures, lower pressures
and higher salinities. K-values are more sensitive to temperature than pressure, whereas
salinity has a profound effect on the DME partitioning, resulting much larger compositions
of DME in the oil phase at high concentrations of NaCl in water.

C H A P T E R
7
Conclusions and future work
7.1 Chemical and phase equilibrium calculations
Conlcusions
Various methods and algorithms have been proposed in the literature for chemical and
phase equilibrium calculations in multicomponent mixtures. The Gibbs energy mini-
mization approach includes stoichiometric methods, which involve reaction extents, and
non-stoichiometric methods, which minimize the Gibbs energy under material balance
constraints. Most implementations of stoichiometric methods are inefficient nested loops
using the ideal system approximation, while multiphase quadratic methods result in a
cumbersome framework. On the other hand, non-stoichiometric methods are advantageous
for multiple reactions but are usually applied to single-phase or slightly non-ideal two-phase
systems. There is still need of a systematic, reliable and straightforward approach to CPE
calculations. In this work two non-stoichiometric methods are presented for non-ideal
multiphase chemical equilibrium calculations: the Lagrange multipliers method and the
modified RAND method. The Lagrangian of the reduced Gibbs energy is defined incorpo-
rating the material balance constraints and equations based on the Lagrangian conditions
at the minimum are solved in both methods.
The Lagrange multipliers method is a nested-loop procedure: in the inner loop the working
equations are solved for constant fugacity/activity coefficients and their values are updated
in the outer loop. As a result, the method can attain quadratic convergence for ideal
systems, where the outer loop is redundant. The modified RAND is a second-order method
that takes advantage of fugacity/activity coefficient composition derivatives to accelerate
calculations. The advantages of the modified RAND method are quadratic convergence for
multiphase non-ideal mixtures, same treatment for all components in all the phases, and
monitoring the value of the Gibbs energy to control convergence. The latter is possible
because the material balance is satisfied at every modified RAND iteration.

150 Chapter 7. Conclusions and future work
Two algorithms are applied to the VLE, LLE and VLLE of reaction systems in this
study: the successive substitution algorithm, which includes calculations only with the
Lagrange multipliers method and the combined algorithm, which uses the modified RAND
method after a few steps of successive substitution. Our initialization could provide good
initial estimates and stability analysis could successfully identify if a phase split should
occur. All calculations converged to the equilibrium solution without issues, even when
components were be excluded from a phase (e.g. non-volatile components). CPU times of
both algorithms showed that they are faster than different methods in the literature and
the number of iterations was acceptable considering their convergence rate and calculation
tolerances set. The recommended approach for CPE calculations is the combined algorithm
as it exhibits clear advantages: efficient second-order convergence with increased robustness
provided by the Gibbs energy monitoring.
Finally, the algorithms were used for calculations in electrolyte mixtures. Equilibrium
involves speciation reactions in a highly non-ideal aqueous phase, a vapor phase of the
volatile solutes and a pure solid phase. The material balance accounts for electoneutrality
indirectly when the electrolytes are confined to the aqueous phase and there are no
additional working equations for electrolyte solutions. If the molality or molarity reference
state, usuallyselectedforsuchsystems, istransformedtotheinfinitedilutionreferencestate
(mole fraction based), the equations of the algorithms do not require any modifications.
It should be stressed that the tested electrolyte systems show similar CPU time and
convergence behavior to non-electrolyte reaction systems.
Future work
The algorithms in this study provide a general approach to multiphase reaction equilibrium
and their application is not limited to specific systems. The efficient combined algorithm
could be useful in simulations of industrial processes such as reactive distillation, reactive
extraction and weak electrolyte equilibrium (e.g. sour water stripping). Simulations
involve a large number of PT flash problems, therefore adjustments are required to further
improve the speed of calculations. If the maximum number of equilibrium phases is
known beforehand, the time used in stability analysis can be reduced. Furthermore, during
successivesubstitutionthehighestnumberofinner-loopiterationsarefoundduringthefirst
few outer-loop non-ideality updates. Excessive computation could be avoided if successive
substitution was used only once before the modified RAND steps. Finally, comparison
of stoichiometric algorithm with the non-stoichiometric algorithms of this work, could
illustrate more clearly the weaknesses and the advantages of both formulations, either for
CPE calculations at constant temperature and pressure or in process simulation.
The Lagrange multipliers method is based on Gibbs energy minimization equations, but it
is not a minimization itself. The material balance belongs to the working equations and
the Gibbs energy decrease cannot be controlled. In this work the successive substitution
algorithm never failed to converge for any of the systems tested. Nevertheless, there is no

Chapter 7. Conclusions and future work 151
mathematical guarantee of convergence, which can cause oscillations in strongly non-ideal
systems. Heidemann and Michelsen (1995) published examples of unstable successive
substitution calculations when solving phase equilibrium with the Rachford-Rice equations
for two-phase systems. A similar analysis could be performed for the current formulation to
conclude when the method cannot be successfully used for CPE calculations and determine
the non-ideality limits that can be tolerated.
Despite the advantages of the modified RAND method, a non-descent direction could be
produced during calculations. In this case, regardless of the step control parameter in
Eq. 3.70, the Gibbs energy cannot decrease. Corrections to the M−1 matrix in phase
equilibrium problems have been proposed by Paterson et al. (2018), suggesting that the
ascent direction issues are likely to be encountered close to critical points. This correction
was not needed in the examples tested in our work, but including it in the algorithm
clearly provides an extra level of robustness. Extension to CPE calculations is easily
achieved by substituting the phase equilibrium formula matrix (identity matrix) with
the corresponding formula matrix of the reaction system. Moreover, the RAND method
(original and modified) can lead to negative mole numbers of trace components. White
et al. (1958) and Smith and Missen (1982) addressed the issue of small concentrations,
using essentially Eq. 3.34 to determine compositions of trace components more accurately.
This was not attempted in this work, but it could be applied in future analysis with a
systematic investigation of the improvement they offer.
Finally, successful calculation of electrolyte equilibrium with the two non-stoichiometric
algorithms allows the study of more complex geochemical systems, pertinent to the research
of geologists and oil reservoir engineers. Geochemical reactions appearing in Leal et al.
(2016a,b) with multiple solutes and calcite/dolomite/quartz solid phases could be an
interesting application of the CPE algorithms proposed in this work. In the current
framework, speciation of electrolytes is a different type of reaction, and the consideration
of a solid is the addition of a pure component phase (remaining components are excluded).
However, the number of electrolyte systems we tested might not be enough to identify
further provisions we should take into account when dealing with a strongly non-ideal
electrolyte aqueous phase or pure solid phases. The suitability of electrolyte models
and analysis of solute behavior should be also carefully investigated. Equilibrium results
appeared to be rather sensitive to different sets of parameters for the same models or
different correlations for the Henry’s constant corresponding to the same component.
7.2 DME phase equilibrium modeling
Conlcusions
AccurateDMEphasemodelingisnecessaryforsimulationsoftheDEWprocess. Parameters
for CPA and CEoS-HV (PR and SRK) were regressed for binary systems of DME with
water, methane, propane, n-butane, n-pentane, n-decane, n-dodecane, carbon dioxide

152 Chapter 7. Conclusions and future work
and nitrogen. Deviations from experimental data revealed that temperature dependent
parameters are needed for adequate description of DME/water (DME modeled as cross
associating with CPA), while only one binary interaction parameter was required for
the remaining binaries. CPA was selected for predictions in multicomponent DME
mixtures with water and hydrocarbons. Calculations for the LLE of ternary systems of
DME/water/hydrocarbon produced similar curves for different hydrocarbons, suggesting
that the hydrocarbon size may not have a strong effect on the DME partitioning.
To examine the extent of this effect, predictions of the DME K-values between oil and
water were made, modeling the oil as a methane/n-butane/n-decane mixture. K-values
seemed to exhibit a stronger dependence on the DME mole fraction in the oil phase rather
than the oil composition. Temperature, pressure and salinity sensitivities of K-value were
also investigated. Temperature has a larger effect on the K-value than pressure, with
higher temperatures and lower pressures resulting in higher concentrations of DME in
the oil phase. For the salinity effect, brine was considered as “pseudo-water”. Salinity
was introduced with CPA in the c parameter. Vapor pressures of brine solutions were
1
regressed to determine a correlation of the form c = f(w ) and then binary interaction
1 NaCl
parameters for CPA were regressed using DME/brine experimental data. K-values were
predicted at different NaCl concentrations in water, showing that high salinity improves
appreciably the partitioning of DME into the oil phase.
Future work
The DME phase equilibrium modeling was aimed to provide a quick and preliminary
analysis with the focus on the K-values of DME between oil and aqueous phases. There
is obviously room for further refinement and improvement. More accurate electrolyte
models, such as eCPA Maribo-Mogensen et al. (2015), can apparently be used. If we want
to select a simpler model for reservoir simulation, the current approach based on Søreide
and Whitson (1992) can also be improved, e.g. by introducing salinity dependent critical
constants of “pseudo-water” and brine/hydrocarbon k . Finally, although we believe the
ij
current analysis has captured the main characteristics of the temperature, pressure and
salinity influences, future work should include calculations for live oils or multicomponent
oils with more realistic composition of hydrocarbons and inerts.

Appendices
| A Matrix-vector |     |     | operations |     |     |     |
| --------------- | --- | --- | ---------- | --- | --- | --- |
Equations in different chapters involve the use of operations between matrices and vectors.
This section presents simple mathematical operations between the quantities in a more
compact way. Vectors are considered to be equivalent to single column matrices. For
| vector v | Rq×1 and  | matrix      | M Rp×q, | we have: |     |     |
| -------- | --------- | ----------- | ------- | -------- | --- | --- |
|          | ∈         |             | ∈       |          |     |     |
| sum      | of vector | components: |         |          |     |     |
•
q
X
|     |     |     |     | v = vTe |     | (A.1) |
| --- | --- | --- | --- | ------- | --- | ----- |
|     |     |     |     | i       | q   |       |
i=1
| vector | of matrix | columns | sum: |     |     |     |
| ------ | --------- | ------- | ---- | --- | --- | --- |
•
|     |     |     |    |    |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Pq M
1j
j=1
|     |     |     |    |      |        |       |
| --- | --- | --- | --- | ----- | ------ | ----- |
|     |     |     |  . |      |        |       |
|     |     |     |    |  q   |        |       |
|     |     |     |    |  X   |        |       |
|     |     |     | .   | =     | M = Me | (A.2) |
|     |     |     |    |      | j q    |       |
|     |     |     |    |      |        |       |
|     |     |     |  . |  j=1 |        |       |
|     |     |     |    |      |        |       |
|     |     |     |    |      |        |       |
Pq
M
|        |           |           | j=1 | pj  |     |     |
| ------ | --------- | --------- | --- | --- | --- | --- |
| vector | of matrix | rows sum: |     |     |     |     |
•
|     |     |     |    |    |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Pp M
i1
i=1
|     |     |     |    |      |          |       |
| --- | --- | --- | --- | ----- | -------- | ----- |
|     |     |     |  . |      |          |       |
|     |     |     |    |  p   |          |       |
|     |     |     |    |  X   |          |       |
|     |     |     | .   | =     | MT = MTe | (A.3) |
|     |     |     |    |      | i p      |       |
|     |     |     |    |      |          |       |
|     |     |     |  . |  i=1 |          |       |
|     |     |     |    |      |          |       |
|     |     |     |    |      |          |       |
Pp
M
|     |     |     | i=1 | iq  |     |     |
| --- | --- | --- | --- | --- | --- | --- |

| 154           |             |     |     | A.  | Matrix-vector | operations |
| ------------- | ----------- | --- | --- | --- | ------------- | ---------- |
| sum of matrix | components: |     |     |     |               |            |
•
|     |     |     | p q |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
XX
|     |     |     | M = | eTMe |     | (A.4) |
| --- | --- | --- | --- | ---- | --- | ----- |
|     |     |     | ij  | p q  |     |       |
i=1j=1
where:
| M column | j of matrix | M   |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- | --- |
j
| MT column | i of matrix | MT (row | i of matrix | M in column | form) |     |
| --------- | ----------- | ------- | ----------- | ----------- | ----- | --- |
i
| e vector | of ones with | dimensions | X 1 |     |     |     |
| -------- | ------------ | ---------- | --- | --- | --- | --- |
| X        |              |            | ×   |     |     |     |

| B. Degrees | of  | freedom | analysis |         |     |          |     |     |     | 155 |
| ---------- | --- | ------- | -------- | ------- | --- | -------- | --- | --- | --- | --- |
| B Degrees  |     |         | of       | freedom |     | analysis |     |     |     |     |
In a general chemical and phase equilibrium problem (Smith and Missen, 1982), the ranks
| of the stoichiometric |     |     | and | formula | matrix  |     | are linked | by:     |     |       |
| --------------------- | --- | --- | --- | ------- | ------- | --- | ---------- | ------- | --- | ----- |
|                       |     |     |     |         | rank(N) |     | N          | rank(A) |     | (B.1) |
C
|     |     |     |     |     |     | ≤   | −   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
To use these matrices in calculations, the equality must be valid. In the case of inequality,
the number of additional stoichiometric constraints to be defined is found by:
|          |      |           |     | N   | = N | rank(A) |     | rank(N) |     | (B.2) |
| -------- | ---- | --------- | --- | --- | --- | ------- | --- | ------- | --- | ----- |
|          |      |           |     |     | S   | C −     |     | −       |     |       |
| and they | have | the form: |     |     |     |         |     |         |     |       |
NP
X
|     |     |     |     |     |     | A   | n = | b   |     | (B.3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     |     |     |     |     | ac  | k   | ac  |     |       |
k=1
where:
| A ,b | additional |     | stoichiometric |     | constraints |     |     |     |     |     |
| ---- | ---------- | --- | -------------- | --- | ----------- | --- | --- | --- | --- | --- |
ac ac
It is easy to incorporate these constraints in a modified formula matrix and element
| abundance  | vector: |     |     |     |     |        |     |       |     |       |
| ---------- | ------- | --- | --- | --- | --- | ------ | --- | ----- | --- | ----- |
|            |         |     |     |     |     |      |     |     |     |       |
|            |         |     |     |     |     | A      |     | b     |     |       |
|            |         |     |     |     | A0  |        | b0  |       |     |       |
|            |         |     |     |     | =   |      |     | =   |     | (B.4) |
|            |         |     |     |     |     | A      |     | b     |     |       |
|            |         |     |     |     |     | ac     |     | ac    |     |       |
| It follows | that:   |     |     |     |     |        |     |       |     |       |
|            |         |     |     |     |     | rank(A | ) = | N     |     | (B.5) |
|            |         |     |     |     |     |        | ac  | S     |     |       |
TheGibbsphaseruleforreactionsystemsandadditionalspecificationsis(Rao,1985):
|     |     |     | F = | (N  | N   | N   | )+(N | N ) | N +2 | (B.6) |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | ----- |
|     |     |     |     | C   | R   | S   |      | V T | P    |       |
|     |     |     |     |     | −   | −   |      | − − |      |       |
where:
| N   | number | of  | additional |     | variables |     |     |     |     |     |
| --- | ------ | --- | ---------- | --- | --------- | --- | --- | --- | --- | --- |
V
| N   | number | of  | additional |     | constraints |     | not included | in A | ,b    |     |
| --- | ------ | --- | ---------- | --- | ----------- | --- | ------------ | ---- | ----- | --- |
| T   |        |     |            |     |             |     |              |      | ac ac |     |
The quantity N = N N N represents the number of the elements in the system
|              |            | E   | C   | R   | S   |              |     |     |     |     |
| ------------ | ---------- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- |
|              |            |     | −   |     | −   |              |     |     |     |     |
| (independent | entities). |     | Eq. | B.6 | can | be rewritten |     | as: |     |     |

| 156 |           |     | B. Degrees | of freedom | analysis |
| --- | --------- | --- | ---------- | ---------- | -------- |
|     | F = N +(N | N ) | N +2       |            | (B.7)    |
|     | E V       | T   | P          |            |          |
− −
When no additional constraints or variables are assumed, the Gibbs phase rule be-
comes:
|     | F = N | N +2 |     |     | (B.8) |
| --- | ----- | ---- | --- | --- | ----- |
E P
−
where:
|     | N = | N N |     |     | (B.9) |
| --- | --- | --- | --- | --- | ----- |
E C R
−
In this work, calculations take place at specified temperature and pressure. Since F 0,
≥
the number of phases cannot be larger than the number of elements (Eq. B.8):
|     | N   | N   |     |     | (B.10) |
| --- | --- | --- | --- | --- | ------ |
P E
≤

| C. Reference | state | chemical |       | potentials |     |            |     |     | 157 |
| ------------ | ----- | -------- | ----- | ---------- | --- | ---------- | --- | --- | --- |
| C Reference  |       |          | state | chemical   |     | potentials |     |     |     |
In a phase equilibrium problem, when the reference states are the same for all components,
referencestatechemicalpotentialscanbeassumedequaltozero. Conversely, determination
of simultaneous chemical and phase equilibrium implies that reference state chemical
| potentials | satisfy the | following |     | equation: |      |     |         |     |       |
| ---------- | ----------- | --------- | --- | --------- | ---- | --- | ------- | --- | ----- |
|            |             |           |     | G◦        | NC   | µ◦  |         |     |       |
|            |             |           |     | ∆         | X ν  |     |         |     |       |
|            |             |           |     | r rk      | = ir | ik  | = lnKeq |     |       |
|            |             |           |     | RT        | RT   |     | −       | rk  | (C.1) |
i=1
|     |     |     |     |     | r = 1,...,N |     |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
R
where the reference state Gibbs energy of the reaction and chemical potentials are at the
same conditions. However, databases for standard state chemical potentials are not always
available. Individual values of µ◦ do not affect the equilibrium solution, as long as they
are consistent with Eq. C.1. Reference state Gibbs energy of formation or combustion can
be found in the literature for individual components and we can set:
|     |     |     | µ◦  | G◦  |             |     | µ◦  | G◦     |       |
| --- | --- | --- | --- | --- | ----------- | --- | --- | ------ | ----- |
|     |     |     |     | = ∆ | or          |     | =   | ∆      |       |
|     |     |     | ik  | f   | ik          |     | ik  | − c ik | (C.2) |
|     |     |     |     |     | i = 1,...,N |     |     |        |       |
C
What is usually reported in the literature is chemical equilibrium constants for specific
reactions. We have N chemical reactions and therefore N equations as Eq. C.1. The
|     |     | R   |     |     |     |     |     | R   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
number of the reference chemical potentials required for the calculations is N . For this
C
reason, when chemical equilibrium constants are given, we must “decompose” them into
fictitious values of µ◦. The first step is to select N reference components and set at the
R
| desired | temperature | and | pressure: |     |     |     |     |     |     |
| ------- | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- |

|     |     |     |     | µˆ , | i reference |     | components |     |     |
| --- | --- | --- | --- | ------ | ----------- | --- | ---------- | --- | --- |
ik
|     |     |     | µ◦ = |     | ∈   |     |     |     | (C.3) |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | ----- |
ik
|     |     |     |     |  0, | i reference |     | components |     |     |
| --- | --- | --- | --- | ----- | ----------- | --- | ---------- | --- | --- |
6∈
| The following | system | is  | solved | for the | non-zero | µˆ  | :   |     |     |
| ------------- | ------ | --- | ------ | ------- | -------- | --- | --- | --- | --- |
k
|     |     |     |     |     |     |    | lnKeq |    |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
1k
|     |     |     |     |       |     |  − |     |    |       |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | ----- |
|     |     |     |     |       |     |    | .   |    |       |
|     |     |     |     | 1     |     |    |     |    |       |
|     |     |     |     | NˆTµˆ | =   |    |     |    | (C.4) |
|     |     |     |     |       |     |    | .   |    |       |
|     |     |     |     | RT    | k   |    |     |    |       |
|     |     |     |     |       |     |    |     |    |       |
.
|     |     |     |     |     |     |    |     |    |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |    |     |    |     |
lnKeq
NRk
−
Nˆ
Matrix is the stoichiometric matrix corresponding only to the reference components.
This matrix must be invertible, therefore the general rule is to choose reference components

| 158 |     |     |     | C. Reference | state chemical | potentials |
| --- | --- | --- | --- | ------------ | -------------- | ---------- |
rank(Nˆ)
that result in = N . There can be cases where this is not true: if we select an inert
R
as a reference component, the corresponding row of the matrix will be all zeros. Another
case when the rank can be less than N is when the reference components participate
R
in all reactions with the same stoichiometric coefficients. If the same reference state is
selected for all phases, then µˆ is common between the different phases. Otherwise, Eq.
k
2.54 must be used appropriately to change reference states for the remaining phases. To
determine the reaction extents at equilibrium we can use the mole numbers of the reference
| components | in the feed | and in phase | k, nˆ and | nˆ : |     |     |
| ---------- | ----------- | ------------ | --------- | ---- | --- | --- |
|            |             |              | F         | k    |     |     |
|            |             |              |          |     |     |     |
NP
Nˆ−1 X
|     |     | ξ   | =   | nˆ nˆ |     | (C.5) |
| --- | --- | --- | --- | ----- | --- | ----- |
|     |     |     |    | k F  |     |       |
−
k=1
In this way, we can calculate reaction extents even for a non-stoichiometric method in
| simultaneous | chemical | and phase | equilibrium | computation. |     |     |
| ------------ | -------- | --------- | ----------- | ------------ | --- | --- |

| D. Determination | of  | the formula | matrix         |        | 159 |
| ---------------- | --- | ----------- | -------------- | ------ | --- |
| D Determination  |     |             | of the formula | matrix |     |
The formula matrix is vital for the material balance in non-stoichiometric methods, because
it is a summary of the elemental composition of each component. Moreover, it includes
reaction information, since the mole numbers must not only lead to constant total mass,
but their change should be also consistent with the chemical reactions. The link between
the formula matrix and the reactions is proven by Eq. 3.20: the choice of elements depends
on the way the reactions are selected and vice versa. In an equation of the form:
|     |     |     | WZ = 0 |     | (D.1) |
| --- | --- | --- | ------ | --- | ----- |
matrix Z is a basis of the null space of W. The solution is not a unique matrix Z. It is
obvious that Z = 0 satisfies the equation. Eq. 3.20 has the same form in a CPE problem,
where it is implied that A = 0 and N = 0. Smith and Missen (1982) presented a method,
|     |     | 6   | 6   |     |     |
| --- | --- | --- | --- | --- | --- |
where they determine N from A in Eq. 3.20. This method produces a number of linearly
| independent | reactions | that will | be satisfied at equilibrium. |     |     |
| ----------- | --------- | --------- | ---------------------------- | --- | --- |
According to Eq. 3.5, when the number of components is fixed, increasing the number of
elements decreases the number of independent chemical reactions. In the literature, we
usually find chemical equilibrium constants for well-defined reactions that were observed
experimentally. Thus, N is already specified by the authors. Determination of A is
therefore more desirable: chemical equilibrium will be established only for the equations
that were observed experimentally. When the number of reactions is small, it might be
easy to select the elements by observation. However, in systems with many reactions and
complex components we need a systematic way of determining the formula matrix. For
| this reason, | we take the | transpose | of Eq. 3.20: |     |     |
| ------------ | ----------- | --------- | ------------ | --- | --- |
NTAT
= 0 (D.2)
The command null( ,’r’) in MATLABR calculates the “rational” basis for the null space
|     | ·   |     | (cid:13) |     |     |
| --- | --- | --- | -------- | --- | --- |
of a matrix obtained from the reduced row echelon form of the matrix. The reduced row
echelon form of matrix A is a relatively simple form of A which also satisfies Eq. 3.20 and
D.2. The command rref( ) calculates the reduced row echelon form of a matrix, which is
·
| unique. | In MATLABR: |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- |
(cid:13)
|     |     |     | n [null(NT,’r’)]T | o   |       |
| --- | --- | --- | ----------------- | --- | ----- |
|     |     | A   | = rref            |     | (D.3) |
In this matrix, each leading 1 in every row is the only non-zero entry in its column.
This form implies that all the elements are selected as components. When an element is

| 160 |     |     |     |     |     | D. Determination | of the formula | matrix |
| --- | --- | --- | --- | --- | --- | ---------------- | -------------- | ------ |
defined as a component, its Lagrange multiplier is equal to the chemical potential of the
| corresponding | component. |     | In the | following | reaction: |     |     |     |
| ------------- | ---------- | --- | ------ | --------- | --------- | --- | --- | --- |
(cid:10)
|     |     |     |     | A+B | D   | C inert |     | (D.4) |
| --- | --- | --- | --- | --- | --- | ------- | --- | ----- |
the number of elements is N = N N = 4 1 = 3 and the stoichiometric matrix is
|          |              |         | E   | C      | R    |                   |     |       |
| -------- | ------------ | ------- | --- | ------ | ---- | ----------------- | --- | ----- |
|          |              |         |     | −      |      | −                 |     |       |
| N = [ 1, | 1,0,1]T. The | formula |     | matrix | A is | found by Eq. D.3: |     |       |
| −        | −            |         |     |        |      |                   |     |       |
|          |              |         |     | A      | B    | C D               |     |       |
|          |              |         |     |       |      |                  |     |       |
|          |              |         |     | 1      | 0    | 0 1 A             |     |       |
|          |              |         | A   | =     |      |                  |     | (D.5) |
|          |              |         |     | 0     | 1    | 0 1 B            |     |       |
|          |              |         |     |       |      |                  |     |       |
|          |              |         |     | 0      | 0    | 1 0 C             |     |       |
Matrix A illustrates what we intuitively understand: elements A and B must be combined
to produce component D. It is crucial to stress that when elements have been defined
as components, the latter share only the chemical composition of the corresponding
components. Unlike elements, system components are chemical substances with certain
physical and chemical properties (boiling point, density, etc.). Elements are artificial
entities we define to facilitate the mathematical formulation of a CPE material balance. In
other words, elements are a mathematical convenience. Furthermore, elements are reaction
invariant entities, which makes the element abundance vector a constant. Only component
| mole numbers | change | throughout |     | the course |     | of reactions. |     |     |
| ------------ | ------ | ---------- | --- | ---------- | --- | ------------- | --- | --- |
Nevertheless, reactions can have multiple products. If reactants and products are chosen
as elements and multiple-product reactions exist, some A might be negative for products
ji
| not selected | as elements. | For | instance, |     | in reaction: |     |     |       |
| ------------ | ------------ | --- | --------- | --- | ------------ | --- | --- | ----- |
|              |              |     |           | A+B | (cid:10)     | C+D |     | (D.6) |
the number of elements must be N = N N = 4 1 = 3. The stoichiometric matrix
|     |     |     |     | E   | C   | R   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | −   | −   |     |     |
is N = [ 1, 1,1,1]T and the formula matrix A is calculated by Eq. D.3:
− −
|     |     |     |     | A   | B   | C D     |     |       |
| --- | --- | --- | --- | --- | --- | ------- | --- | ----- |
|     |     |     |     |  1 | 0   | 0 1  A |     |       |
|     |     |     | A   | =  |     |        |     | (D.7) |
|     |     |     |     | 0  | 1   | 0 1  B |     |       |
|     |     |     |     |    |     |        |     |       |
|     |     |     |     | 0   | 0   | 1 1 C   |     |       |
−
Although elements A and B are combined to produce D, we need to remove the chemical

| D. Determination |     | of  | the formula |     | matrix |     |     |     |     |     | 161 |
| ---------------- | --- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- |
composition of element C from the complex AB to match the exact chemical composition
of component D. This could also lead to b 0. Therefore, we need to broaden the
j
≤
interpretationofvectorb: totalmolenumbersofelementj, asthenetresultofcontributing
to form components and being removed as excess from components. We can calculate
different values of b using Eq. 3.7 for each feed, focusing on element C and components C,
D:
| 1. n = [1 | 1 1 | 0]T |     |     |     |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
F
1]T:
b = [1 1 Initially there is no component D and all of element C is used to form
component C. At an arbitrary reaction extent, x mol of component C and x mol of
component D are produced. Element C contributes x+1 mol to form component C and
x mol are removed from component D as excess. The net result is 1+x x = 1 = b .
− C
| 2. n = [1 | 1 0 | 0]T |     |     |     |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
F
b = [1 1 0]T. Initially, there is no component C or component D. At an arbitrary
reaction extent, x mol of component C and x mol of component D are produced.
Element C contributes x mol to form component C and x mol are removed from
| component | D   | as excess. | The | net | result | is x | x   | = 0 = | b . |     |     |
| --------- | --- | ---------- | --- | --- | ------ | ---- | --- | ----- | --- | --- | --- |
C
−
1]T
| 3. n = [1 | 1 0 |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
F
b = [2 2 1]T. Initially, there is only component D. At an arbitrary reaction extent, x
−
mol of component C and x mol of component D are produced. Element C contributes
x mol to form component C and x+1 mol are removed from component D as excess.
| The net | result | is  | x (x+1) | =   | 1 = | b . |     |     |     |     |     |
| ------- | ------ | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
C
|     |     |     | −   |     | −   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Positive and negative values of the formula matrix can be separated in the matrices A+
| and A−. For | the | matrix | of Eq. | D.7 | we   | have: |      |     |     |     |       |
| ----------- | --- | ------ | ------ | --- | ---- | ----- | ---- | --- | --- | --- | ----- |
|             |     |        |        |     |     |       |     |    |     |    |       |
|             |     |        |        |     | 1    | 0 0   | 1    | 0   | 0 0 | 0   |       |
|             |     |        | A+     | +A− |     |       |     |    |     |    |       |
|             |     | A      | =      |     | = 0 | 1 0   | 1 + | 0  | 0 0 | 0  | (D.8) |
|             |     |        |        |     |     |       |     |    |     |    |       |
|             |     |        |        |     | 0    | 0 1   | 0    | 0   | 0 0 | 1   |       |
−
The mole numbers of element j that actually exist in the system correspond to the positive
|     |     |     |     | PNC | A+PNP |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
values of the formula matrix n . The “artificial” excessive mole numbers
|     |     |     |     | i=1 | ji  | k=1 ik |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
of element j in other element combinations to form components is PNC A−PNP n .
|     |     |     |     |     |     |     |     |     |     | i=1 ji | k=1 ik |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ |
−
Although each of these numbers is not constant, their difference (material balance) is:
|     |     | NC  | NP  |     | NC  | NP  |     | NC  | NP  |     |       |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
|     |     | X   | X   |     | X   | X   |     | X   | X   |     |       |
|     |     |     | A+  | n + | A−  | n   | =   | A   | n   | = b | (D.9) |
|     |     |     | ji  | ik  |     | ji  | ik  | ji  | ik  | j   |       |
|     |     | i=1 | k=1 |     | i=1 | k=1 |     | i=1 | k=1 |     |       |

162 D. Determination of the formula matrix
Unless we desire all elements to be a tangible entity as actual building blocks (strictly
parts of molecules, A 0), there should not be any problem using them with a broader
ji
≥
interpretation in the calculations, allowing negative entries in the formula matrix.

| E. Initialization |                | of  | calculations |     |              |     |     |     |     | 163 |
| ----------------- | -------------- | --- | ------------ | --- | ------------ | --- | --- | --- | --- | --- |
| E                 | Initialization |     |              | of  | calculations |     |     |     |     |     |
Minimization of function Q (section 3.2.3) is a robust procedure to initialize the main
calculations. This is a numerical method, where initialization is required as well. Lagrange
multipliers are the chemical potentials of the elements at equilibrium. A reasonable initial
| estimate | is: |     |     |      |      |     |         |     |     |       |
| -------- | --- | --- | --- | ---- | ---- | --- | ------- | --- | --- | ----- |
|          |     |     |     |      |     |     | b       |     |     |       |
|          |     |     |     |      |  |     | j       |     |     |       |
|          |     |     |     |      | ln   | |   | |       | , b | = 0 |       |
|          |     |     |     |      |      | PN  |         | j   |     |       |
|          |     |     |     | λ(0) | =    |     | E b     |     | 6   |       |
|          |     |     |     |      |      | q = | 1 | q | |     |     |       |
|          |     |     |     |      | j    |     |         |     |     | (E.1) |
0,
|     |     |     |     |     |     |     |     | b   | = 0 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j
j = 1,...,N
E
Absolute values are used for negative entries in vector b. In this case, it is not implied
that an element does not exist when b = 0 (Appendix D). There is also the need of
j
initial estimates for the phase amounts. We follow a simple analysis: mole numbers will
be between a minimum and a maximum number, because reactions tend to decrease or
increase the total mole numbers. If there is no change in the mole numbers, the phase
amount estimate is equal to the feed total mole numbers. There are two directions for
reactions, forward and backward. To calculate the theoretical maximum extents for the
| forward | and | backward | reactions, |     | we have: |     |          |     |     |       |
| ------- | --- | -------- | ---------- | --- | -------- | --- | -------- | --- | --- | ----- |
|         |     |          |            |     | (cid:18) | n   | (cid:19) | n   |     |       |
|         |     |          |            |     |          | F,i |          | F,i |     |       |
|         |     |          |            | ξF  | = min    |     | ,        |     | < 0 | (E.2) |
r
|     |     |     |     |     | i     | − ν       |          | ν   |     |       |
| --- | --- | --- | --- | --- | ----- | --------- | -------- | --- | --- | ----- |
|     |     |     |     |     |       | ir        |          | ir  |     |       |
|     |     |     |     |     |       | (cid:18)n | (cid:19) | n   |     |       |
|     |     |     |     | ξB  | = min | F,i       | ,        | F,i | > 0 | (E.3) |
|     |     |     |     | r   | i     | ν         |          | ν   |     |       |
|     |     |     |     |     |       | ir        |          | ir  |     |       |
where:
| ξF  | maximum |     | extent | of the | forward | reaction |     | r   |     |     |
| --- | ------- | --- | ------ | ------ | ------- | -------- | --- | --- | --- | --- |
r
ξB
|     | maximum |     | extent | of the | backward |     | reaction | r   |     |     |
| --- | ------- | --- | ------ | ------ | -------- | --- | -------- | --- | --- | --- |
r
The total mole numbers for each reaction happening independently are:
|     |     |     |     |     | nF  | = n | +ν    | ξF  |     | (E.4) |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
|     |     |     |     |     |     | t,F | t,r   |     |     |       |
|     |     |     |     |     | t,r |     |       | r   |     |       |
|     |     |     |     |     | nB  |     |       | ξB  |     |       |
|     |     |     |     |     |     | = n | ν     |     |     | (E.5) |
|     |     |     |     |     | t,r | t,F | − t,r | r   |     |       |
where:
nF
|     | phase | amount | estimate |     | for the | full | forward | reaction | r   |     |
| --- | ----- | ------ | -------- | --- | ------- | ---- | ------- | -------- | --- | --- |
t,r
| nB  | phase | amount | estimate |     | for the | full | backward |     | reaction r |     |
| --- | ----- | ------ | -------- | --- | ------- | ---- | -------- | --- | ---------- | --- |
t,r

| 164 |     |     |     | E. Initialization | of calculations |
| --- | --- | --- | --- | ----------------- | --------------- |
To calculate an average value of mole numbers based on forward and backward reactions,
a weighted average can be used, with chemical equilibrium constants as weights:
|     |     |     | PNR Keq | nF     |     |
| --- | --- | --- | ------- | ------ | --- |
|     |     |     | n¯F r=1 | rk t,r |     |
= (E.6)
|     |     |     | t PNR | Keq |     |
| --- | --- | --- | ----- | --- | --- |
r=1 rk
PNR (1/Keq)nB
|     |     |     | r=1 | rk t,r |     |
| --- | --- | --- | --- | ------ | --- |
n¯B = (E.7)
|     |     |     | t PNR (1/Keq) |     |     |
| --- | --- | --- | ------------- | --- | --- |
|     |     |     | r=1           | rk  |     |
to finally obtain the initial estimate of the total mole numbers of the single phase k:
|     |     |     | n¯F      | +n¯B |       |
| --- | --- | --- | -------- | ---- | ----- |
|     |     |     | n(0) = t | t    | (E.8) |
|     |     |     | t,k      | 2    |       |
Rigorous generalization to multiple phases has not been attempted. In case we need to
n¯F n¯B,
start with more than one phases, we can calculate an average number of and
t t
| distributing | it equally | to all phases: |          |      |       |
| ------------ | ---------- | -------------- | -------- | ---- | ----- |
|              |            |                | n¯F      | +n¯B |       |
|              |            |                | n(0) = t | t    |       |
|              |            |                | t,k 2N   |      | (E.9) |
P
k = 1,...,N
P
It has been found that phase amounts initial estimates are not crucial for convergence.

Bibliography
Abrams, D. S. and Prausnitz, J. M. (1975). Statistical thermodynamics of liquid mixtures:
A new expression for the excess gibbs energy of partly or completely miscible systems.
AIChE Journal, 21(1):116–128.
Alkindi, A., Al-Azri, N., Said, D., AlShuaili, K., and Te Riele, P. (2016). Persistence in
EOR - design of a field trial in a carbonate reservoir using solvent-based water-flood
process. Muscat, Oman. SPE EOR Conference at Oil and Gas West Asia, Society of
Petroleum Engineers.
Anikeev, V. (2014). Chapter 1 – synthesis of biodiesel fuel in supercritical lower alco-
hols with and without heterogeneous catalysts (thermodynamics, phase and chemical
equilibriums, experimental studies). Supercritical Fluid Technology for Energy and
Environmental Applications, pages 1–29.
Anikeev, V., Stepanov, D., and Yermakova, A. (2012). Thermodynamics of phase and
chemical equilibrium in the processes of biodiesel fuel synthesis in subcritical and
supercritical methanol. Industrial & Egineering Chemistry Research, 51(13):4783–4796.
Arteconi, A., Di Nicola, G., Santori, G., and Stryjek, R. (2009). Second virial coefficients
for dimethyl ether. Journal of Chemical & Engineering Data, 54(6):1840–1843.
Avami, A. and Saboohi, Y. (2011). A simultaneous method for phase identification and
equilibriumcalculationsinreactivemixtures. Chemical Engineering Research and Design,
89(10):1901–1908.
Barbosa, D. and Doherty, M. F. (1988). The influence of equilibrium chemical reactions
on vapor-liquid phase diagrams. Chemical Engineering Science, 43(3):529–540.
Bonilla-Petriciolet, A., Bravo-S´anchez, U. I., Castillo-Borja, F., Frausto-Hern´andez, S.,
and Segovia-Hern´andez, J. G. (2008a). Gibbs energy minimization using simulated

166 Bibliography
annealing for two-phase equilibrium calculations in reactive systems. Chemical and
| Biochemical | Engineering | Quarterly, | 22(3):285–298. |
| ----------- | ----------- | ---------- | -------------- |
Bonilla-Petriciolet,A.,Iglesias-Silva,G.A.,andHall,K.R.(2008b). Aneffectivecalculation
procedure for two-phase equilibria in multireaction systems. Fluid Phase Equilibria,
269(1–2):48–55.
Bonilla-Petriciolet, A., Moreno-Virgen, M. d. R., and Soto-Bernal, J. J. (2012). Global
Gibbs free energy minimization in reactive systems via harmony search. International
| Journal | of Chemical | Reactor Engineering, | 10(1). |
| ------- | ----------- | -------------------- | ------ |
Bonilla-Petriciolet, A., Rangaiah, G. P., and Segovia-Herna´ndez, J. G. (2011). Constrained
and unconstrained Gibbs free energy minimization in reactive systems using genetic
algorithm and differential evolution with tabu list. Fluid Phase Equilibria, 300(1–2):120–
134.
Bonilla-Petriciolet,A.andSegovia-Herna´ndez,J.G.(2010). Acomparativestudyofparticle
swarm optimization and its variants for phase stability and equilibrium calculations in
multicomponent reactive and non-reactive systems. Fluid Phase Equilibria, 289(2):110–
121.
Bonilla-Petriciolet, A., V´azquez-Rom´an, R., Iglesias-Silva, G. A., and Hall, K. R. (2006).
Performance of stochastic global optimization methods in the calculation of phase stabil-
ity analyses for nonreactive and reactive mixtures. Industrial & Egineering Chemistry
| Research, | 45(13):4764–4772. |     |     |
| --------- | ----------------- | --- | --- |
Boynton, P. F. (1960). Chemical equilibrium in multicomponent polyphase systems. The
| Journal | of Chemical | Physics, 32(6):1880–1881. |     |
| ------- | ----------- | ------------------------- | --- |
Brinkley, Jr, S. R. (1946). Note on the conditions of equilibrium for systems of many
| constituents. | The | Journal of Chemical | Physics, 14(9):563–564. |
| ------------- | --- | ------------------- | ----------------------- |
Brinkley, Jr, S. R. (1947). Calculation of the equilibrium composition of systems of many
| constituents. | The | Journal of Chemical | Physics, 15(2):107–110. |
| ------------- | --- | ------------------- | ----------------------- |
Burgos-Sol´orzano, G. I., Brennecke, J. F., and Stadtherr, M. A. (2004). Validated
computing approach for high-pressure chemical and multiphase equilibrium. Fluid Phase
| Equilibria, | 219(2):245–255. |     |     |
| ----------- | --------------- | --- | --- |
Castier, M., Rasmussen, P., and Fredenslund, A. (1989). Calculation of simultaneous
chemical and phase equilibria in nonideal systems. Chemical Engineering Science,
44(2):237–248.
Castillo, J. and Grossmann, I. E. (1981). Computation of phase and chemical equilibria.
| Computers | & Chemical | Engineering, | 5(2):99–108. |
| --------- | ---------- | ------------ | ------------ |
Cavallotti, P., Celeri, G., Leonardis, B., and Gardini, L. (1980). Calculation of multicom-
ponent multiphase equilibria. Chemical Engineering Science, 35(11):2297–2304.

Bibliography 167
Chahardowli, M., Farajzadeh, R., and Bruining, H. (2016). Experimental investigation of
dimethyl ether/polymer hybrid as an enhanced oil recovery method. Muscat, Oman.
SPE EOR Conference at Oil and Gas West Asia, Society of Petroleum Engineers.
Chang, T., Rousseau, R. W., and Kilpatrick, P. K. (1986). Methanol synthesis reactions:
calculations of equilibrium conversions using equations of state. Industrial & Engineering
Chemistry Process Design and Development, 25(2):477–481.
Chen, F., Huss, R. S., Doherty, M. F., and Malone, M. F. (2002). Multiple steady states
in reactive distillation: kinetic effects. Computers & Chemical Engineering, 26(1):81–93.
Chernetsky, A., Masalmeh, S., Eikmans, D., Boerrigter, P. M., Fadili, A., Parsons, C. A.,
Parker, A., Boersma, D. M., Cui, J., Dindoruk, B., te Riele, P. M., Alkindi, A., and
Azri, N. (2015). A novel enhanced oil recovery technique: Experimental results and
modelling workflow of the DME enhanced waterflood technology. Abu Dhabi, UAE.
Abu Dhabi International Petroleum Exhibition and Conference, Society of Petroleum
Engineers.
Chong, M. F., Chen, J., Oh, P. P., and Chen, Z.-S. (2014). Modeling study of chemical
phase equilibrium of canola oil transesterification in a CSTR. Chemical Engineering
Science, 87:371–380.
Crowe, C. M. and Nishio, M. (1975). Convergence promotion in the simulation of chemical
processes - the general dominant eigenvalue method. AIChE Journal, 21(3):528–533.
Cruise, D. R. (1964). Notes on the rapid computation of chemical equilibria. The Journal
of Physical Chemistry, 68(12):3797–3802.
da Roza, M. B., Nicolau, A., Angeloni, L. M., Sidou, P. N., and Samios, D. (2012).
Thermodynamic and kinetic evaluation of the polymerization process of epoxidized
biodiesel with dicarboxylic anhydride. Molecular Physics, 110(11–12):1375–1381.
Dahlhoff, G. and Pfennig, A. (2000). Vapor-liquid equilibria in quaternary mixtures of
dimethyl ether + n-butane + ethanol + water. Journal of Chemical & Engineering
Data, 45(4):887–892.
Darnoko, D. and Cheryan, M. (2000). Kinetics of palm oil transesterification in a batch
reactor. Journal of the American Oil Chemists’ Society, 77(12):1263–1267.
Debye, P. and Hu¨ckel, E. (1923). Zur theorie der elektrolyte. Physikalische Zeitschrift,
24:179–207.
Dortmund Data Bank (Accessed: 25.08.2017).
Duan, Z. and Sun, R. (2003). An improved model calculating CO solubility in pure
2
water and aqueous NaCl solutions from 273 to 533 K and from 0 to 2000 bar. Chemical
Geology, 193(3):257–271.
Edwards, T. J., Maurer, G., Newman, J., and Prausnitz, J. M. (1978). Vapor-liquid

168 Bibliography
equilibria in multicomponent aqueous solutions of volatile weak electrolytes. AIChE
Journal, 24(6):966–976.
Elnabawy, A. O., Fateen, S.-E. K., and Bonilla-Petriciolet, A. (2014). Phase stability
analysis and phase equilibrium calculations in reactive and nonreactive systems us-
ing charged system search algorithms. Industrial & Egineering Chemistry Research,
53(6):2382–2395.
Fateen, S.-E. K., Bonilla-Petriciolet, A., and Rangaiah, G. P. (2012). Evaluation of
covariance matrix adaptation evolution strategy, shuffled complex evolution and firefly
algorithms for phase stability, phase equilibrium and chemical equilibrium problems.
Chemical Engineering Research and Design, 90(12):2051–2071.
Felmy, A. R. and Weare, J. H. (1986). The prediction of borate mineral equilibria in
natural waters: Application to Searles Lake, California. Geochimica et Cosmochimica
Acta, 50(12):2771–2783.
Floudas, C. A. and Visweswaran, V. (1990). A global optimization algorithm (GOP)
for certain classes of nonconvex NLPs–I. Theory. Computers & Chemical Engineering,
14(12):1397–1417.
Folas, G. K., Kontogeorgis, G. M., Michelsen, M. L., and Stenby, E. H. (2006). Application
of the Cubic-Plus-Association equation of state to mixtures with polar chemicals and
high pressures. Industrial & Engineering Chemistry Research, 45(4):1516–1526.
Garcia-Sanchez, F., Laugier, S., and Richon, D. (1987). Vapor-liquid equilibrium data for
the methane-dimethylether and methane-diethylether systems between 282 and 344 K.
Journal of Chemical & Engineering Data, 32(2):211–215.
Gautam, R. and Seider, W. D. (1979a). Computation of phase and chemical equilibrium:
Part I. Local and constrained minima in Gibbs free energy. AIChE Journal, 25(6):991–
999.
Gautam, R. and Seider, W. D. (1979b). Computation of phase and chemical equilibrium:
Part II. Phase-splitting. AIChE Journal, 25(6):999–1006.
Gautam, R. and Seider, W. D. (1979c). Computation of phase and chemical equilibrium:
Part III. Electrolytic solutions. AIChE Journal, 25(6):1006–1015.
Gautam, R. and Wareck, J. S. (1986). Computation of physical and chemical equilibria–
alternate specifications. Computers & Chemical Engineering, 10(2):143–151.
George, B., Brown, L. P., Farmer, C. H., Buthod, P., and Manning, F. S. (1976). Compu-
tation of multicomponent, multiphase equilibrium. Industrial & Engineering Chemistry
Process Design and Development, 15(3):372–377.
Giles, N. F. and Wilson, G. M. (2000). Phase equilibria on seven binary mixtures. Journal
of Chemical & Engineering Data, 45(2):146–153.

Bibliography 169
Greiner, H. (1988a). The chemical equilibrium problem for a multiphase system formulated
as a convex program. Calphad, 12(2):155–170.
Greiner, H. (1988b). Computing complex chemical equilibria by generalized linear pro-
gramming. Mathematical and Computer Modelling, 10(7):529–550.
Greiner, H. (1988c). The Gibbs energy of a chemical reaction system considered as a
function of its elemental abundancies. Calphad, 12(2):143–154.
Greiner, H. (1991). An efficient implementation of Newton’s method for complex nonideal
chemical equilibria. Computers & Chemical Engineering, 15(2):115–123.
Grob, S. and Hasse, H. (2005). Thermodynamics of phase and chemical equilibrium in
a strongly nonideal esterification system. Journal of Chemical & Engineering Data,
50(1):92–101.
Groot, J. A. W. M., Eikmans, D., Fadili, A., and Romate, J. E. (2016). Field-scale
modelling and sensitivity analysis of DME enhanced waterflooding. Muscat, Oman.
SPE EOR Conference at Oil and Gas West Asia, Society of Petroleum Engineers.
Gupta, A. K., Bishnoi, P. R., and Kalogerakis, N. (1991). A method for the simultaneous
phase equilibria and stability calculations for multiphase reacting and non-reacting
systems. Fluid Phase Equilibria, 63(1–2):65–89.
Haas Jr., J. L. (1976). Physical properties of the coexisting phases and thermochemical
properties of the H O component in boiling NaCl solutions. Geological Survey Bulletin,
2
1421-A.
Harvie, C. E., Greenberg, J. P., and Weare, J. H. (1987). A chemical equilibrium algorithm
for highly non-ideal multiphase systems: Free energy minimization. Geochimica et
Cosmochimica Acta, 51(5):1045–1057.
Hayden, J. G. and O’Connell, J. P. (1975). A generalized method for predicting second
virial coefficients. Industrial & Engineering Chemistry Process Design and Development,
14(3):209–216.
Heidemann, R. A. and Michelsen, M. L. (1995). Instability of successive substitution.
Industrial & Engineering Chemistry Research, 34(3):958–966.
Hildebrandt, D. and Glasser, D. (1994). Predicting phase and chemical equilibrium using
the convex hull of the gibbs free energy. The Chemical Engineering Journal and the
Biochemical Engineering Journal, 54(3):187–197.
Horstmann, S., Birke, G., and Fischer, K. (2003). Vapor-liquid equilibrium and excess
enthalpy data for the binary systems propane + dimethyl ether and propene + dimethyl
ether at temperatures from (298 to 323) K. Journal of Chemical & Engineering Data,
49(1):38–42.

170 Bibliography
Huang, S. H. and Radosz, M. (1990). Equation of state for small, large, polydisperse, and
associating molecules. Industrial & Engineering Chemistry Research, 29(11):2284–2294.
Huff, V. N., Gordon, S., and Morrell, V. E. (1951). General method and thermodynamic
tables for computation of equilibrium composition and temperature of chemical reactions.
National Advisory Committee for Aeronautics, NACA Technical Report 1037:829–885.
Huron, M.-J. and Vidal, J. (1979). New mixing rules in simple equations of state for rep-
resenting vapour-liquid equilibria of strongly non-ideal mixtures. Fluid Phase Equilibria,
3(4):255–271.
Jaime-Leal, J. E., Bonilla-Petriciolet, A., Segovia-Hern´andez, J. G., Hern´andez, S., and
Hern´andez-Escoto, H. (2012). Analysis and prediction of input multiplicity for the
reactive flash separation using reaction-invariant composition variables. Chemical
Engineering Research and Design, 90(11):1856–1870.
Jalali, F., Seader, J. D., and Khaleghi, S. (2008). Global solution approaches in equilibrium
and stability analysis using homotopy continuation in the complex domain. Computers
& Chemical Engineering, 32(10):2333–2345.
Jalali-Farahani, F. and Seader, J. D. (2000). Use of homotopy-continuation method in
stability analysis of multiphase, reacting systems. Computers & Chemical Engineering,
24(8):1997–2008.
Jim´enez, L. and Costa-L´opez, J. (2002). The production of butyl acetate and methanol
via reactive and extractive distillation. II. Process modeling, dynamic simulation, and
control strategy. Industrial & Egineering Chemistry Research, 41(26):6735–6744.
Kanth, M. V. S. R. R., Pushpavanam, S., Narasimhan, S., and Narasimha, M. B. (2014). A
robust and efficient algorithm for computing reactive equilibria in single and multiphase
systems. Industrial & Egineering Chemistry Research, 53(39):15278–15286.
Kiss, A. A., Dimian, A. C., and Rothenberg, G. (2006). Solid acid catalysts for biodiesel
production —towards sustainable energy. Advanced Synthesis & Catalysis, 348(1–2):75–
81.
Kontogeorgis, G. M., Voutsas, E. C., Yakoumis, I. V., and Tassios, D. P. (1996). An
equation of state for associating fluids. Industrial & Engineering Chemistry Research,
35(11):4310–4318.
Kontogeorgis, G. M., Yakoumis, I. V., Meijer, H., Hendriks, E., and Moorwood, T. (1999).
Multicomponent phase equilibrium calculations for water–methanol–alkane mixtures.
Fluid Phase Equilibria, 158-160(Supplement C):201–209.
Koukkari, P. and Pajarre, R. (2007). Combining reaction kinetics to the multi-phase Gibbs
energy calculation. Computer Aided Chemical Engineering, 24:153–158.
Lake, L. W. (1989). Enhanced oil recovery. Prentice-Hall, Inc, Upper Saddle River, NJ.

Bibliography 171
Lantagne, G., Marcos, B., and Cayrol, B. (1988). Computation of complex equilibria by
nonlinear optimization. Computers & Chemical Engineering, 12(6):589–599.
Laursen, T., Rasmussen, P., and Andersen, S. I. (2003). VLE and VLLE measurements of
dimethyl ether containing systems. Journal of Chemical & Engineering Data, 47(2):198–
202.
Leal, A. M. M., Kulik, D. A., and Kosakowski, G. (2016a). Computational methods for
reactive transport modeling: A Gibbs energy minimization approach for multiphase
equilibrium calculations. Advances in Water Resources, 88:231–240.
Leal, A. M. M., Kulik, D. A., and Saar, M. O. (2016b). Enabling Gibbs energy mini-
mization algorithms to use equilibrium constants of reactions in multiphase equilibrium
calculations. Chemical Geology, 437:170–181.
Lee, Y. P., Rangaiaha, G. P., and Luus, R. (1999). Phase and chemical equilibrium calcu-
lations by direct search optimization. Computers & Chemical Engineering, 23(9):1183–
1191.
Likozar, B. and Levec, J. (2014). Transesterification of canola, palm, peanut, soybean and
sunflower oil with methanol, ethanol, isopropanol, butanol and tert-butanol to biodiesel:
Modelling of chemical equilibrium, reaction kinetics and mass transfer based on fatty
acid composition. Applied Energy, 123(Supplement C):108–120.
Liu, J., Daoutidis, P., and Yang, B. (2016). Process design and optimization for ether-
ification of glycerol with isobutene. Chemical Engineering Science, 144(Supplement
C):326–335.
Lucia, A. and Xu, J. (1990). Chemical process optimization using Newton-like methods.
Computers & Chemical Engineering, 14(2):119–138.
Ma, Y. H. and Shipman, C. W. (1972). On the computation of complex equilibria. AIChE
Journal, 18(2):299–304.
Madeley, W. D. and Toguri, J. M. (1973). Computing chemical equilibrium compositions in
multiphase systems. Industrial & Engineering Chemistry Fundamentals, 12(2):261–262.
Mandagaran, B. A. and Campanella, E. A. (2009). Modeling of phase and chemical
equilibrium on the quaternary system acetic acid, n-butanol, water and n-butylacetate.
Chemical Product and Process Modeling, 4(1).
Maribo-Mogensen, B., Thomsen, K., and Kontogeorgis, G. M. (2015). An electrolyte CPA
equation of state for mixed solvent electrolytes. AIChE Journal, 61(9):2933–2950.
Mathiarasi, R. and Partha, N. (2016). Optimization, kinetics and thermodynamic studies
on oil extraction from Daturametel Linn oil seed for biodiesel production. Renewable
Energy, 96(Part A):583–590.

172 Bibliography
Maurer, G. (1986). Vapor-liquid equilibrium of formaldehyde-and water-containing multi-
| component | mixtures. | AIChE | Journal, 32(6):932–948. |     |
| --------- | --------- | ----- | ----------------------- | --- |
McDonald, C. M. and Floudas, C. A. (1995). Global optimization for the phase and
chemical equilibrium problem: Application to the NRTL equation. Computers &
| Chemical | Engineering, | 19(11):1111–1139. |     |     |
| -------- | ------------ | ----------------- | --- | --- |
McDonald, C. M. and Floudas, C. A. (1997). GLOPEQ: A new computational tool for
the phase and chemical equilibrium problem. Computers & Chemical Engineering,
121(1):1–23.
McNaught, A. D. and Wilkinson, A. (1997). IUPAC Compendium of Chemical Terminology.
| Blackwell | Scientific | Publications, | Oxford, second | edition. |
| --------- | ---------- | ------------- | -------------- | -------- |
Meng, X., Zhang, J., Wu, J., and Liu, Z. (2012). Experimental measurement and modeling
of the viscosity of dimethyl ether. Journal of Chemical & Engineering Data, 57(3):988–
993.
Michelsen, M. L. (1982). The isothermal flash problem. Part I. Stability. Fluid Phase
| Equilibria, | 9(1):1–19. |     |     |     |
| ----------- | ---------- | --- | --- | --- |
Michelsen, M. L. (1989). Calculation of multiphase ideal solution chemical equilibrium.
| Fluid | Phase Equilibria, | 53:73–80. |     |     |
| ----- | ----------------- | --------- | --- | --- |
Michelsen, M. L. and Hendriks, E. M. (2001). Physical properties from association models.
| Fluid | Phase Equilibria, | 180(1–2):165–174. |     |     |
| ----- | ----------------- | ----------------- | --- | --- |
Michelsen, M. L. and Mollerup, J. M. (2007). Thermodynamic Models: Fundamentals &
Computational Aspects. Tie-Line Publications, Holte, Denmark, second edition.
Mohebbinia, S., Sepehrnoori, K., and Johns, R. T. (2013). Four-phase equilibrium
calculations of carbon dioxide/hydrocarbon/water systems with a reduced method. SPE
| Journal, | 18(5):943–951. |     |     |     |
| -------- | -------------- | --- | --- | --- |
Moodley, K., Rarey, J., and Ramjugernath, D. (2015). Application of the bio-inspired Krill
Herd optimization technique to phase equilibrium calculations. Computers & Chemical
| Engineering, | 74:75–88. |     |     |     |
| ------------ | --------- | --- | --- | --- |
NIST Chemistry WebBook (Accessed: 19.02.2016). NIST Standard Reference Database
| Number | 69. |     |     |     |
| ------ | --- | --- | --- | --- |
NIST Chemistry WebBook (Accessed: 28.08.2017). NIST Standard Reference Database
| Number | 69. |     |     |     |
| ------ | --- | --- | --- | --- |
Nothnagel, K.-H., Abrams, D. S., and Prausnitz, J. M. (1973). Generalized correlation
for fugacity coefficients in mixtures at moderate pressures. Application of chemical
theory of vapor imperfections. Industrial & Engineering Chemistry Process Design and
| Development, | 12(1):25–35. |     |     |     |
| ------------ | ------------ | --- | --- | --- |

Bibliography 173
Okasinski, M.J.andDoherty, M.F.(2000). Predictionofheterogeneousreactiveazeotropes
in esterification systems. Chemical Engineering Science, 55(22):5263–5271.
Omota, F., Dimian, A. C., and Bliek, A. (2001). Design of reactive distillation process for
fatty acid esterification. Computer Aided Chemical Engineering, 9:463–468.
Omota, F., Dimian, A. C., and Bliek, A. (2003). Fatty acid esterification by reactive
distillation.Part1: equilibrium-baseddesign. ChemicalEngineeringScience,58(14):3159–
3174.
Osorio-Viana, W., Duque-Bernal, M., Quintero-Arias, J. D., Dobrosz-Go´mez, I., Fontalvo,
´
J., and G´omez-Garc´ıa, M. A. (2013). Activity model and consistent thermodynamic
features for acetic acid-isoamyl alcohol-isoamyl acetate-water reactive system. Fluid
Phase Equilibria, 345:68–80.
Outcalt, S. L. and Lemmon, E. W. (2013). Bubble-point measurements of eight binary
mixtures for organic Rankine cycle applications. Journal of Chemical & Engineering
Data, 58(6):1853–1860.
Pal, D., Tripathi, A., Shukla, A., Gupta, K. R., and Keshav, A. (2015). Reactive extraction
of pyruvic acid using tri-n-octylamine diluted in decanol/kerosene: Equilibrium and
effect of temperature. Industrial & Egineering Chemistry Research, 60(3):860–869.
Park, S.-J., Han, K.-J., and Gmehling, J. (2007). Isothermal phase equilibria and excess
molarenthalpiesforbinarysystemswithdimethyletherat323.15K. Journal of Chemical
& Engineering Data, 52(5):1814–1818.
Parkhurst, D. L. and Appelo, C. A. J. (2013). Description of input and examples
for PHREEQC version 3 – A computer program for speciation, batch-reaction, one-
dimensional transport, and inverse geochemical calculations, volume Book 6, Chapter
43. U.S. Geological Survey Techniques and Methods.
P´atek, J., Hruby´, J., Klomfar, J., Souˇakov´a, M., and Harvey, A. H. (2009). Reference
correlations for thermophysical properties of liquid water at 0.1 MPa. Journal of Physical
and Chemical Reference Data, 38(1):21–29.
Paterson, D. (2017). Flash Computation and EoS Modelling for Compositional Thermal
Simulation of Flow in Porous Media. PhD thesis, Technical University of Denmark.
Paterson, D., Michelsen, M. L., Stenby, E. H., and Yan, W. (2017). New formulations
for isothermal multiphase flash. Montgomery, Texas, USA. SPE Reservoir Simulation
Conference, Society of Petroleum Engineers. Submitted under the title “RAND-Based
Formulations for Isothermal Multiphase Flash” to Society of Petroleum Engineers
Journal (accepted).
Paterson, D., Michelsen, M. L., Yan, W., and Stenby, E. H. (2018). Extension of modified
RAND to multiphase flash specifications based on state functions other than (T,P).
Fluid Phase Equilibria, 458(41):288–299.

174 Bibliography
Peng, D.-Y. and Robinson, D. B. (1976). A new two-constant equation of state. Industrial
| & Engineering |     | Chemistry | Fundamentals, |     | 15(1):59–64. |     |
| ------------- | --- | --------- | ------------- | --- | ------------ | --- |
Perdomo, F. A., Mill´an-Malo, B. M., Mendoza-D´ıaz, G., and Gil-Villegas, A. (2013).
Predicting reactive equilibria of biodiesel’s fatty-acid-methyl-esters compounds. Journal
| of Molecular |     | Liquids, | 185(Supplement |     | C):8–12. |     |
| ------------ | --- | -------- | -------------- | --- | -------- | --- |
P´erez Cisneros, E. S., Gani, R., and Michelsen, M. L. (1997). Reactive separation systems–
I. Computation of physical and chemical equilibrium. Chemical Engineering Science,
52(4):527–543.
Phoenix, A. V. and Heidemann, R. A. (1998). A non-ideal multiphase chemical equilibrium
| algorithm. | Fluid | Phase | Equilibria, |     | 150–151:255–265. |     |
| ---------- | ----- | ----- | ----------- | --- | ---------------- | --- |
Pitzer, K. S. (1973). Thermodynamics of electrolytes. I. Theoretical basis and general
| equations. | The | Journal | of Physical |     | Chemistry, | 77(2):268–277. |
| ---------- | --- | ------- | ----------- | --- | ---------- | -------------- |
Powell, M. J. D. (1971). Recent advances in unconstrained optimization. Mathematical
| Programming, |     | 1(1):26–57. |     |     |     |     |
| ------------ | --- | ----------- | --- | --- | --- | --- |
Pozo, M. E. and Streett, W. B. (1984). Fluid phase equilibria for the system dimethyl
ether/water from 50 to 220 ◦C and pressures to 50.9 MPa. Journal of Chemical &
| Engineering |     | Data, | 29(3):324–329. |     |     |     |
| ----------- | --- | ----- | -------------- | --- | --- | --- |
Pozo de Fern´andez, M. E., Calado, J. C. G., Zollweg, J. A., and Streett, W. B. (1992).
Vapor-liquid equilibria in the binary system dimethyl ether + n-butane from 282.9 to
414.5 K at pressures to 4.82 MPa. Fluid Phase Equilibria, 74:289–302.
Prigogine, I. and Defay, R. (1947). On the number of independent constituents and the
| phase rule. | The | Journal | of  | Chemical | Physics, | 15(8):614–615. |
| ----------- | --- | ------- | --- | -------- | -------- | -------------- |
Prutton, C. F. and Savage, R. L. (1945). The solubility of carbon dioxide in calcium
chloride-water solutions at 75, 100, 120◦ and high pressures. Journal of the American
| Chemical | Society, |     | 67(9):1550–1554. |     |     |     |
| -------- | -------- | --- | ---------------- | --- | --- | --- |
Rao, Y. K. (1983). The analysis and calculation of equilibria in complex metallurgical
| systems. | Metallurgical |     | Transactions |     | B, 14(4):701–710. |     |
| -------- | ------------- | --- | ------------ | --- | ----------------- | --- |
Rao, Y. K. (1985). Extended form of the Gibbs phase rule. Chemical Engineering
| Education, | 19(1):46–49. |     |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- | --- |
Ratnakar, R. R., Dindoruk, B., and Wilson, L. (2016a). Experimental investigation
of DME-water-crude oil phase behavior and PVT modeling for the application of
| DME-enhanced |     | waterflooding. |     | Fuel, | 182:188–197. |     |
| ------------ | --- | -------------- | --- | ----- | ------------ | --- |
Ratnakar, R. R., Dindoruk, B., and Wilson, L. (2016b). Use of DME as an EOR agent:
Experimental and modeling study to capture interactions of DME, brine and crudes at
reservoir conditions. Dubai, UAE. SPE Annual Technical Conference and Exhibition,
| Society | of Petroleum |     | Engineers. |     |     |     |
| ------- | ------------ | --- | ---------- | --- | --- | --- |

Bibliography 175
Ratnakar, R. R., Dindoruk, B., and Wilson, L. C. (2017). Phase behavior experiments
and PVT modeling of DME-brine-crude oil mixtures based on Huron-Vidal mixing rules
| for EOR | applications. |     | Fluid | Phase | Equilibria, | 434:49–62. |
| ------- | ------------- | --- | ----- | ----- | ----------- | ---------- |
Rossi, C. C. R. S., Berezuk, M. E., Cardozo-Filho, L., and Guirardello, R. (2011). Simulta-
neous calculation of chemical and phase equilibria using convexity analysis. Computers
| & Chemical | Engineering, |     |     | 35(7):1226–1237. |     |     |
| ---------- | ------------ | --- | --- | ---------------- | --- | --- |
Saim, S. and Subramaniam, B. (1988). Chemical reaction equilibrium at supercritical
| conditions. | Chemical |     | Engineering |     | Science, | 43(8):1837–1847. |
| ----------- | -------- | --- | ----------- | --- | -------- | ---------------- |
Saito, S., Michishita, T., and Maeda, S. (1971). Separation of meta- and para-xylene mix-
ture by distillation accompanied by chemical reactions. Journal of Chemical Engineering
| of Japan, | 4(1):37–43. |     |     |     |     |     |
| --------- | ----------- | --- | --- | --- | --- | --- |
Sander, B.,Rasmussen,P., andFredenslund,A.(1986). Calculationofsolid-liquidequilibria
in aqueous solutions of nitrate salts using an extended UNIQUAC equation. Chemical
| Engineering | Science, |     | 41(5):1197–1202. |     |     |     |
| ----------- | -------- | --- | ---------------- | --- | --- | --- |
Sanderson, R. V. and Chien, H. H. Y. (1973). Simultaneous chemical and phase equilibrium
calculation. Industrial & Engineering Chemistry Process Design and Development,
12(1):81–85.
Schott, G. L. (1964). Computation of restricted equilibria by general methods. The Journal
| of Chemical | Physics, |     | 40(7):2065–2066. |     |     |     |
| ----------- | -------- | --- | ---------------- | --- | --- | --- |
Schuchardt, U., Sercheli, R., and Vargas, R. M. (1998). Transesterification of vegetable
oils: a review. Journal of the Brazilian Chemical Society, 9(3):199–210.
Seider, W. D. and Widagdo, S. (1996). Multiphase equilibria of reactive systems. Fluid
| Phase | Equilibria, | 123(1–2):283–303. |     |     |     |     |
| ----- | ----------- | ----------------- | --- | --- | --- | --- |
Shah, V. H., Pham, V., Larsen, P., Biswas, S., and Frank, T. (2016). Liquid-liquid
extraction for recovering low margin chemicals: Thinking beyond the partition ratio.
| Industrial | &   | Egineering | Chemistry |     | Research, | 55(6):1731–1739. |
| ---------- | --- | ---------- | --------- | --- | --------- | ---------------- |
Smith, W. R. and Missen, R. W. (1982). Chemical Reaction Equilibrium Analysis: Theory
| and Algorithms. |     | Wiley, | New | York, | United | States of America. |
| --------------- | --- | ------ | --- | ----- | ------ | ------------------ |
Soave, G. (1972). Equilibrium constants from a modified Redlich-Kwong equation of state.
| Chemical | Engineering |     | Science, |     | 27(6):1197–1203. |     |
| -------- | ----------- | --- | -------- | --- | ---------------- | --- |
Solsvik, J., Haug-Warberg, T., and Jakobsen, H. A. (2016). Implementation of chemi-
cal reaction equilibrium by Gibbs and Helmholtz energies in tubular reactor models:
Application to the steam-methane reforming process. Chemical Engineering Science,
140:261–278.
Søreide, I. and Whitson, C. H. (1992). Peng-Robinson predictions for hydrocarbons, CO ,
2
N , and H S with pure water and NaCl brine. Fluid Phase Equilibria, 77:217–240.
| 2   | 2   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |

176 Bibliography
Stateva, R. P. and Wakeham, W. A. (1997). Phase equilibrium calculations for chemically
reacting systems. Industrial & Engineering Chemistry Research, 36(12):5474–5482.
Suzuki, I., Komatsu, H., and Hirata, M. (1970). Formulation and prediction of quaternary
vapor-liquid equilibria accompanied by esterification. Journal of Chemical Engineering
| of Japan, | 3(2):152–157. |     |     |
| --------- | ------------- | --- | --- |
Tallon, S. and Fenton, K. (2010). The solubility of water in mixtures of dimethyl ether
| and carbon | dioxide. Fluid | Phase Equilibria, | 298(1):60–66. |
| ---------- | -------------- | ----------------- | ------------- |
te Riele, P., Parsons, C., Boerrigter, P., Plantenberg, J. Suijkerbuijk, B., Burggraaf, J.,
Chernetsky, A., Boersma, D., and Broos, R. (2016). Implementing a water soluble
solvent based enhanced oil recovery technology - aspects of field development planning.
Muscat, Oman. SPE EOR Conference at Oil and Gas West Asia, Society of Petroleum
Engineers.
Thomsen, K. (1997). Aqueous Electrolytes Model Parameters and Process Simulation. PhD
| thesis, | Technical University | of Denmark. |     |
| ------- | -------------------- | ----------- | --- |
Toikka, A. M., Toikka, M. A., and Trofimova, M. A. (2012). Chemical equilibrium in a
heterogeneous fluid phase system: thermodynamic regularities and topology of phase
| diagrams. | Russian Chemical | Bulletin, 61(4):741–751. |     |
| --------- | ---------------- | ------------------------ | --- |
Tsanas, C., Stenby, E. H., and Yan, W. (2017a). Calculation of multiphase chemical
equilibrium by the modified RAND method. Industrial & Engineering Chemistry
| Research, | 56(41):11983–11995. |     |     |
| --------- | ------------------- | --- | --- |
Tsanas, C., Stenby, E. H., and Yan, W. (2017b). Calculation of simultaneous chemical
and phase equilibrium by the method of Lagrange multipliers. Chemical Engineering
| Science, | 174:112–126. |     |     |
| -------- | ------------ | --- | --- |
Tsivintzelis, I. and Kontogeorgis, G. M. (2014). On the predictive capabilities of CPA
for applications in the chemical industry: Multicomponent mixtures containing methyl-
methacrylate, dimethyl-ether or acetic acid. Chemical Engineering Research and Design,
92(12):2947–2969.
Tsivintzelis, I., Kontogeorgis, G. M., Michelsen, M. L., and Stenby, E. H. (2010). Modeling
phase equilibria for acid gas mixtures using the CPA equation of state. I. Mixtures with
| H S. AIChE | Journal, 56(11):2965–2982. |     |     |
| ---------- | -------------------------- | --- | --- |
2
Tsivintzelis, I., Kontogeorgis, G. M., Michelsen, M. L., and Stenby, E. H. (2011). Modeling
phase equilibria for acid gas mixtures using the CPA equation of state. Part II: Binary
| mixtures | with CO . Fluid | Phase Equilibria, | 306(1):38–56. |
| -------- | --------------- | ----------------- | ------------- |
2
Uchida, M. (1987). MPEC2: A code for multi-phase chemical equilibria. Computers &
| Chemistry, | 11(1):19–24. |     |     |
| ---------- | ------------ | --- | --- |
Ung, S. and Doherty, M. F. (1995a). Calculation of residue curve maps for mixtures with

Bibliography 177
multiple equilibrium chemical reactions. Industrial & Engineering Chemistry Research,
34(10):3195–3202.
Ung, S. and Doherty, M. F. (1995b). Necessary and sufficient conditions for reactive
azeotropes in multireaction mixtures. AIChE Journal, 41(11):2383–2392.
Ung, S. and Doherty, M. F. (1995c). Synthesis of reactive distillation systems with
multiple equilibrium chemical reactions. Industrial & Engineering Chemistry Research,
34(8):2555–2565.
Ung, S. and Doherty, M. F. (1995d). Theory of phase equilibria in multireaction systems.
Chemical Engineering Science, 50(20):3201–3216.
Ung, S. and Doherty, M. F. (1995e). Vapor-liquid phase equilibrium in systems with
multiple chemical reactions. Chemical Engineering Science, 50(1):23–48.
Varzandeh, F. (2017). Modeling Study of High Pressure and High Temperature Reservoir
Fluids. PhD thesis, Technical University of Denmark.
Venkatraman, A., Lake, L. W., and Johns, R. T. (2015). Modelling the impact of
geochemical reactions on hydrocarbon phase behavior during CO gas injection for
2
enhanced oil recovery. Fluid Phase Equilibria, 402:56–68.
Voll, F. A. P., da Silva, C., Rossi, C. C. R. S., Guirardello, R., de Castilhos, F., Oliveira,
J. V., and Cardozo-Filho, L. (2011). Thermodynamic analysis of fatty acid esterification
for fatty acid alkyl esters production. Biomass and Bioenergy, 35(2):781–788.
Vonˇka, P. and Leitner, J. (1995). Calculation of chemical equilibria in heterogeneous
multicomponent systems. Calphad, 19(1):25–36.
Wasylkiewicz, S. K. and Ung, S. (2000). Global phase stability analysis for heteroge-
neous reactive mixtures and calculation of reactive liquid-liquid and vapor-liquid-liquid
equilibria. Fluid Phase Equilibria, 175(1–2):253–272.
White,III,C.W.andSeider,W.D.(1981). Computationofphaseandchemicalequilibrium:
Part IV. Approach to chemical equilibrium. AIChE Journal, 27(3):466–471.
White, W. B., Johnson, S. M., and Dantzig, G. B. (1958). Chemical equilibrium in complex
mixtures. The Journal of Chemical Physics, 28(5):751–755.
Wiebe, R. and Gaddy, V. L. (1940). The solubility of carbon dioxide in water at various
temperatures from 12 to 40◦ and at pressures to 500 atmospheres. Critical phenomena.
Journal of the American Chemical Society, 62(4):815–817.
Wilson, G. M. (1964). Vapor-liquid equilibrium. xi. a new expression for the excess free
energy of mixing. Journal of the American Chemical Society, 86(2):127–130.
Wu, J., Liu, Z., Pan, J., and Zhao, X. (2004). Vapor pressure measurements of dimethyl
ether from (233 to 399) K. Journal of Chemical & Engineering Data, 49(1):32–34.

178 Bibliography
Wu, J., Liu, Z., Wang, F., and Ren, C. (2003). Surface tension of dimethyl ether from
(213 to 368) K. Journal of Chemical & Engineering Data, 48(6):1571–1573.
Wu, L., Wei, T., Lin, Z., Zou, Y., Tong, Z., and Sun, J. (2016). Bentonite-enhanced
biodiesel production by NaOH-catalyzed transesterification: Process optimization and
kinetics and thermodynamic analysis. Fuel, 182(Supplement C):920–927.
Xiao, W.-d., Zhu, K.-h., Yuan, W.-k., and Chien, H. H.-y. (1989). An algorithm for
simultaneous chemical and phase equilibrium calculation. AIChE Journal, 35(11):1813–
1820.
Yakoumis, I. V., Kontogeorgis, G. M., Voutsas, E. C., and Tassios, D. P. (1997). Vapor-
liquid equilibria for alcohol/hydrocarbon systems using the CPA equation of state. Fluid
| Phase Equilibria, | 130(1):31–47. |     |
| ----------------- | ------------- | --- |
Yancy-Caballero, D. M. and Guirardello, R. (2013). Thermodynamic simulation of
transesterification reaction by gibbs energy minimization. Fluid Phase Equilibria,
| 341(Supplement | C):12–22. |     |
| -------------- | --------- | --- |
Yancy-Caballero, D. M. and Guirardello, R. (2015). Modeling and parameters fitting of
chemical and phase equilibria in reactive systems for biodiesel production. Biomass and
| Bioenergy, | 81(Supplement | C):544–555. |
| ---------- | ------------- | ----------- |
Zeleznik, F.J.andGordon, S.(1968). Calculationofcomplexchemicalequilibria. Industrial
| & Engineering | Chemistry, | 60(6):27–57. |
| ------------- | ---------- | ------------ |

Glossaries
Abbreviations
| ARD  | absolute               | relative    | deviation         |           |
| ---- | ---------------------- | ----------- | ----------------- | --------- |
| AARD | average                | absolute    | relative          | deviation |
| CEoS | cubic equation         |             | of state          |           |
| CPA  | Cubic-Plus-Association |             |                   |           |
| CPE  | chemical               | and         | phase equilibrium |           |
| DME  | dimethyl               | ether       |                   |           |
| EoS  | equation               | of state    |                   |           |
| HC   | hydrocarbon            |             |                   |           |
| LLE  | liquid-liquid          | equilibrium |                   |           |
| VLE  | vapor-liquid           | equilibrium |                   |           |
| VLLE | vapor-liquid-liquid    |             | equilibrium       |           |
Symbols
| A    | formula    | matrix         |     |             |
| ---- | ---------- | -------------- | --- | ----------- |
| A ,b | additional | stoichiometric |     | constraints |
ac ac
A number of elements j in the chemical formula of component i
ji

180 Glossaries
A
|     | component | i   | in a chemical |     | reaction |     |     |
| --- | --------- | --- | ------------- | --- | -------- | --- | --- |
i
| a   | energy | parameter |     |           |     |     |     |
| --- | ------ | --------- | --- | --------- | --- | --- | --- |
| a   | energy | parameter | of  | component |     | i   |     |
i
| a   | parameter | in  | the energy |     | term | of CPA |     |
| --- | --------- | --- | ---------- | --- | ---- | ------ | --- |
0
| a   | energy | parameter | of  | components |     | i   | and j |
| --- | ------ | --------- | --- | ---------- | --- | --- | ----- |
ij
| B   | element | abundance |     | matrix |          |     |     |
| --- | ------- | --------- | --- | ------ | -------- | --- | --- |
| B   | element | abundance |     | vector | in phase |     | k   |
k
| b   | element    | abundance |     | vector     |     |      |         |
| --- | ---------- | --------- | --- | ---------- | --- | ---- | ------- |
| B   | total mole | numbers   |     | of element |     | j in | phase k |
jk
| b   | total mole | numbers |     | of element |     | j   |     |
| --- | ---------- | ------- | --- | ---------- | --- | --- | --- |
j
| b   | covolume | parameter |     |              |     |     |     |
| --- | -------- | --------- | --- | ------------ | --- | --- | --- |
| b   | covolume | parameter |     | of component |     |     | i   |
i
| b   | covolume | parameter |     | of components |     |     | i and j |
| --- | -------- | --------- | --- | ------------- | --- | --- | ------- |
ij
C◦ reference state heat capacity at constant pressure of component i
p,i
C HV-NRTL energy interaction parameter between components i and j
ij
| c   | molarity | of component |     | i   | in phase | k   |     |
| --- | -------- | ------------ | --- | --- | -------- | --- | --- |
ik
| c   | solvent | molarity | in  | phase | k   |     |     |
| --- | ------- | -------- | --- | ----- | --- | --- | --- |
sol,k
| c   | total molarity |     | in phase | k   |     |     |     |
| --- | -------------- | --- | -------- | --- | --- | --- | --- |
t,k
c◦
unit molarity
| c   | parameter | in  | the energy |     | term | of CPA |     |
| --- | --------- | --- | ---------- | --- | ---- | ------ | --- |
1
| e   | vector | of ones | with | dimensions |     | X   | 1   |
| --- | ------ | ------- | ---- | ---------- | --- | --- | --- |
X
×
F vector of working equations in the successive substitution method
| f ˆ | fugacity | of component |     | i   | in phase | k   |     |
| --- | -------- | ------------ | --- | --- | -------- | --- | --- |
ik
| f   | fugacity | of pure | component |     | i   | in phase | k   |
| --- | -------- | ------- | --------- | --- | --- | -------- | --- |
ik
| f   | fugacity | of pure | liquid | i   |     |     |     |
| --- | -------- | ------- | ------ | --- | --- | --- | --- |
il

Glossaries 181
f◦
|     | reference | state | fugacity | of  | component |     | i in phase | k   |
| --- | --------- | ----- | -------- | --- | --------- | --- | ---------- | --- |
ik
| G   | Gibbs energy |     |          |     |     |     |     |     |
| --- | ------------ | --- | -------- | --- | --- | --- | --- | --- |
| G   | Gibbs energy |     | of phase | k   |     |     |     |     |
k
| g(v) | radial distribution |          | function |           |     |      |         |     |
| ---- | ------------------- | -------- | -------- | --------- | --- | ---- | ------- | --- |
| H    | enthalpy            |          |          |           |     |      |         |     |
| H    | Henry’s             | constant | of       | component |     | i in | phase k |     |
ik
Hs
|     | saturation | Henry’s |     | constant | of  | component | i in | phase k |
| --- | ---------- | ------- | --- | -------- | --- | --------- | ---- | ------- |
ik
| I   | ionic strength |     | in phase | k   |     |     |     |     |
| --- | -------------- | --- | -------- | --- | --- | --- | --- | --- |
k
| J   | Jacobian | of F | in the | Lagrange |     | multiplier | method |     |
| --- | -------- | ---- | ------ | -------- | --- | ---------- | ------ | --- |
Keq
|     | thermodynamic |     | equilibrium |     | constant |     | of reaction | r in phase k |
| --- | ------------- | --- | ----------- | --- | -------- | --- | ----------- | ------------ |
rk
| k   | binary | interaction | parameter |     | between |     | component | i and j |
| --- | ------ | ----------- | --------- | --- | ------- | --- | --------- | ------- |
ij
K K-factor of component i in phase k with respect to a reference phase
ik
L
|     | Lagrangian | function |           |     |     |     |     |     |
| --- | ---------- | -------- | --------- | --- | --- | --- | --- | --- |
| M   | molar mass | of       | component |     | i   |     |     |     |
i
| M   | solvent | molar | mass | in phase | k   |     |     |     |
| --- | ------- | ----- | ---- | -------- | --- | --- | --- | --- |
sol,k
| m   | molality | of component |     | i   | in phase | k   |     |     |
| --- | -------- | ------------ | --- | --- | -------- | --- | --- | --- |
ik
| m◦  | unit molality  |     |        |     |     |     |     |     |
| --- | -------------- | --- | ------ | --- | --- | --- | --- | --- |
| N   | stoichiometric |     | matrix |     |     |     |     |     |
Nˆ
|     | stoichiometric |           | matrix | for    | the assignment |          | of µˆ |     |
| --- | -------------- | --------- | ------ | ------ | -------------- | -------- | ----- | --- |
| n   | component      | abundance |        | matrix |                |          |       |     |
| n   | component      | abundance |        | vector |                | in phase | k     |     |
k
| n   | phase amount |     | vector |     |     |     |     |     |
| --- | ------------ | --- | ------ | --- | --- | --- | --- | --- |
t
| n   | component | abundance |     | vector |     | in the | feed |     |
| --- | --------- | --------- | --- | ------ | --- | ------ | ---- | --- |
F
| N   | number | of experimental |     | points |     |     |     |     |
| --- | ------ | --------------- | --- | ------ | --- | --- | --- | --- |
| N   | number | of components   |     |        |     |     |     |     |
C

182 Glossaries
| N   | number | of elements |     |     |     |     |     |     |     |
| --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
E
| N   | number | of phases |     |     |     |     |     |     |     |
| --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
P
| N   | number | of independent |     |     | chemical | reactions |     |     |     |
| --- | ------ | -------------- | --- | --- | -------- | --------- | --- | --- | --- |
R
| N   | number | of special |     | stoichiometric |     | conditions |     |     |     |
| --- | ------ | ---------- | --- | -------------- | --- | ---------- | --- | --- | --- |
S
| N   | number | of additional |     | constraints |     | not | included | in  | A ,b  |
| --- | ------ | ------------- | --- | ----------- | --- | --- | -------- | --- | ----- |
| T   |        |               |     |             |     |     |          |     | ac ac |
| N   | number | of additional |     | variables   |     |     |          |     |       |
V
| n   | mole numbers |     | of component |     | i   | in phase | k   |     |     |
| --- | ------------ | --- | ------------ | --- | --- | -------- | --- | --- | --- |
ik
| n   | amount | of phase | k   |     |     |     |     |     |     |
| --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
t,k
| n   | mole numbers |     | of component |     | i   | in the | feed |     |     |
| --- | ------------ | --- | ------------ | --- | --- | ------ | ---- | --- | --- |
F,i
| n   | total mole | numbers |     | in the | feed |     |     |     |     |
| --- | ---------- | ------- | --- | ------ | ---- | --- | --- | --- | --- |
t,F
| n   | solvent | mole | numbers | in  | phase | k   |     |     |     |
| --- | ------- | ---- | ------- | --- | ----- | --- | --- | --- | --- |
sol,k
| nB  | phase amount |     | estimate |     | for the | full backward |     | reaction | r   |
| --- | ------------ | --- | -------- | --- | ------- | ------------- | --- | -------- | --- |
t,r
nF
|     | phase amount |     | estimate |     | for the | full forward |     | reaction | r   |
| --- | ------------ | --- | -------- | --- | ------- | ------------ | --- | -------- | --- |
t,r
| OF  | objective | function |           | in the | regressions |     | of DME        | binaries |     |
| --- | --------- | -------- | --------- | ------ | ----------- | --- | ------------- | -------- | --- |
| Pe  | Poynting  | effect   | (Poynting |        | correction) |     | for component |          | i   |
i
| p   | pressure |          |     |     |     |     |     |     |     |
| --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
| p   | pressure | of phase |     | k   |     |     |     |     |     |
k
| p   | partial | pressure | of  | component |     | i   |     |     |     |
| --- | ------- | -------- | --- | --------- | --- | --- | --- | --- | --- |
i
ps
|     | vapor pressure |     | of  | component |     | i   |     |     |     |
| --- | -------------- | --- | --- | --------- | --- | --- | --- | --- | --- |
i
| p   | critical | pressure | of  | component |     | i   |     |     |     |
| --- | -------- | -------- | --- | --------- | --- | --- | --- | --- | --- |
c,i
| ps  | solvent | vapor | pressure |     |     |     |     |     |     |
| --- | ------- | ----- | -------- | --- | --- | --- | --- | --- | --- |
sol
p∗
|     | ideal gas    | reference |     | pressure |               |     |     |     |     |
| --- | ------------ | --------- | --- | -------- | ------------- | --- | --- | --- | --- |
| Q   | function     | minimized |     | during   | intialization |     |     |     |     |
| R   | gas constant |           |     |          |               |     |     |     |     |
R transformed tie line slopes defined in Bonilla-Petriciolet et al. (2008a)
j

Glossaries 183
| s   | phase amount |          | correction |     | vector |     |     |     |
| --- | ------------ | -------- | ---------- | --- | ------ | --- | --- | --- |
| S   | entropy      |          |            |     |        |     |     |     |
| S   | entropy      | of phase |            | k   |        |     |     |     |
k
| s   | correction | for | the | amount | of phase | k   |     |     |
| --- | ---------- | --- | --- | ------ | -------- | --- | --- | --- |
k
| T   | temperature |     |          |     |     |     |     |     |
| --- | ----------- | --- | -------- | --- | --- | --- | --- | --- |
| T   | temperature |     | of phase | k   |     |     |     |     |
k
| T   | critical | temperature |     | of  | component | i   |     |     |
| --- | -------- | ----------- | --- | --- | --------- | --- | --- | --- |
c,i
| T   | reduced | temperature |     |     |     |     |     |     |
| --- | ------- | ----------- | --- | --- | --- | --- | --- | --- |
r
| TPD | tangent  | plane   | distance |       |          |     |     |     |
| --- | -------- | ------- | -------- | ----- | -------- | --- | --- | --- |
| tpd | reduced  | tangent |          | plane | distance |     |     |     |
| tm  | modified | tangent |          | plane | distance |     |     |     |
| U   | internal | energy  |          |       |          |     |     |     |
| U   | internal | energy  | of       | phase | k        |     |     |     |
k
V stoichiometricmatrixofreferencecomponentsinUngandDoherty(1995b,d)
| V   | volume |          |     |     |     |     |     |     |
| --- | ------ | -------- | --- | --- | --- | --- | --- | --- |
| V   | volume | of phase |     | k   |     |     |     |     |
k
| V ¯ | partial | molar | volume | of  | component | i   | in phase | k   |
| --- | ------- | ----- | ------ | --- | --------- | --- | -------- | --- |
ik
¯∞
V infinite dilution partial molar volume of component i in phase k
ik
| v   | molar volume |     |     |           |      |       |     |     |
| --- | ------------ | --- | --- | --------- | ---- | ----- | --- | --- |
| v   | molar volume |     | of  | component | i in | phase | k   |     |
ik
| v   | molar volume |     | of  | component | i in | the | liquid | phase |
| --- | ------------ | --- | --- | --------- | ---- | --- | ------ | ----- |
il
| W   | vector      | of trial | phase | mole    | numbers      |     |     |     |
| --- | ----------- | -------- | ----- | ------- | ------------ | --- | --- | --- |
| w   | vector      | of trial | phase | mole    | fractions    |     |     |     |
| W   | trial phase | mole     |       | numbers | of component |     | i   |     |
i
| w   | trial phase | mole |     | fraction | of component |     | i   |     |
| --- | ----------- | ---- | --- | -------- | ------------ | --- | --- | --- |
i

184 Glossaries
| x   | matrix | of mole | fractions |     |     |     |     |     |     |
| --- | ------ | ------- | --------- | --- | --- | --- | --- | --- | --- |
x reference component mole fractions in Ung and Doherty (1995b,d)
ref
| x   | vector | of mole | fractions |     | in phase | k   |     |     |     |
| --- | ------ | ------- | --------- | --- | -------- | --- | --- | --- | --- |
k
X(xr)+
|     | cation        | with | charge       | +x  | in dissociation |            | reaction | r         |     |
| --- | ------------- | ---- | ------------ | --- | --------------- | ---------- | -------- | --------- | --- |
| r   |               |      |              | r   |                 |            |          |           |     |
| X   | mole fraction |      | of component |     | i               | not bonded |          | at site A |     |
Ai
| x   | mole fraction |     | of component |     | i   | in phase | k   |     |     |
| --- | ------------- | --- | ------------ | --- | --- | -------- | --- | --- | --- |
ik
| x¯  | overall | mole | fraction | of  | component |     | i   |     |     |
| --- | ------- | ---- | -------- | --- | --------- | --- | --- | --- | --- |
i
| xel | mole fraction |     | of element |     | j in | phase | k   |     |     |
| --- | ------------- | --- | ---------- | --- | ---- | ----- | --- | --- | --- |
jk
| x   | solvent | mole | fraction | in  | phase | k   |     |     |     |
| --- | ------- | ---- | -------- | --- | ----- | --- | --- | --- | --- |
sol,k
Y(yr)−
|     | anion         | with    | charge       | y   | in dissociation |        | reaction | r   |     |
| --- | ------------- | ------- | ------------ | --- | --------------- | ------ | -------- | --- | --- |
| r   |               |         |              | − r |                 |        |          |     |     |
| z   | vector        | of mole | fractions    |     | in the          | feed   |          |     |     |
| z   | mole fraction |         | of component |     | i               | in the | feed     |     |     |
i
| z   | charge | of component |     | i   |     |     |     |     |     |
| --- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- |
i
| Greek | letters   |              |           |     |          |     |     |     |     |
| ----- | --------- | ------------ | --------- | --- | -------- | --- | --- | --- | --- |
| α     | step-size | control      | parameter |     |          |     |     |     |     |
| α     | activity  | of component |           | i   | in phase | k   |     |     |     |
ik
α HV-NRTL non-randomness parameter between components i and j
ij
| β   | mole fraction |     | of phase | k   |     |     |     |     |     |
| --- | ------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
k
βAiBj
parameter in the association term of CPA between sites A and B
i j
| β   | cross association |     | β   | parameter |     | of CPA | in  | DME/water |     |
| --- | ----------------- | --- | --- | --------- | --- | ------ | --- | --------- | --- |
cross
| γ   | symmetric |     | activity | coefficient |     | of component |     | i in phase | k   |
| --- | --------- | --- | -------- | ----------- | --- | ------------ | --- | ---------- | --- |
ik
γ∞
symmetric infinite dilution activity coefficient of component i in phase k
ik
| γ˜  | asymmetric |     | activity | coefficient |     | of component |     | i in phase | k   |
| --- | ---------- | --- | -------- | ----------- | --- | ------------ | --- | ---------- | --- |
ik
γ˜m asymmetric molality activity coefficient of component i in phase k
ik
γ˜c
asymmetric molarity activity coefficient of component i in phase k
ik

Glossaries 185
G◦
∆ reference state Gibbs energy of combustion of component i in phase k
c ik
∆ G◦ reference state Gibbs energy of formation of component i in phase k
f
ik
| ∆ G◦ | reference | state | Gibbs | energy |     | of reaction |     | r in | phase | k   |     |
| ---- | --------- | ----- | ----- | ------ | --- | ----------- | --- | ---- | ----- | --- | --- |
r rk
H◦
| ∆   | reference | state | enthalpy |     | of  | reaction | r in | phase | k   |     |     |
| --- | --------- | ----- | -------- | --- | --- | -------- | ---- | ----- | --- | --- | --- |
r rk
| ∆ V◦ | reference | state | volume |     | change | of  | reaction | r   | in phase | k   |     |
| ---- | --------- | ----- | ------ | --- | ------ | --- | -------- | --- | -------- | --- | --- |
r
rk
| ∆AiBj | association  |       | strength     | between |        | sites | A and | B   |     |     |     |
| ----- | ------------ | ----- | ------------ | ------- | ------ | ----- | ----- | --- | --- | --- | --- |
|       |              |       |              |         |        |       | i     |     | j   |     |     |
| δb    | mass balance |       | satisfaction |         | vector |       |       |     |     |     |     |
| δ     | Kronecker    | delta |              |         |        |       |       |     |     |     |     |
ij
(cid:15)AiBj association energy of interaction between sites A and B
|     |     |     |     |     |     |     |     |     | i   |     | j   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:15) cross association (cid:15) parameter of CPA in DME/water
cross
| θ   | yield factor |     | of component |     | i   | in phase | k   |     |     |     |     |
| --- | ------------ | --- | ------------ | --- | --- | -------- | --- | --- | --- | --- | --- |
ik
| λ   | vector   | of Lagrange |     | multipliers |         |     |     |     |     |     |     |
| --- | -------- | ----------- | --- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
| λ   | Lagrange | multiplier  |     | of          | element | j   |     |     |     |     |     |
j
| µ   | vector | of chemical |     | potentials |     | in phase |     | k   |     |     |     |
| --- | ------ | ----------- | --- | ---------- | --- | -------- | --- | --- | --- | --- | --- |
k
| µ   | chemical | potential |     | of component |     |     | i in phase |     | k   |     |     |
| --- | -------- | --------- | --- | ------------ | --- | --- | ---------- | --- | --- | --- | --- |
ik
µ◦
|     | reference | state | chemical |     | potential |     | of component |     | i   | in phase | k   |
| --- | --------- | ----- | -------- | --- | --------- | --- | ------------ | --- | --- | -------- | --- |
ik
| µ∗  | ideal gas | chemical |     | potential |     | of component |     | i   |     |     |     |
| --- | --------- | -------- | --- | --------- | --- | ------------ | --- | --- | --- | --- | --- |
i
µpure
|     | chemical | potential |     | of pure | component |     |     | i in phase |     | k   |     |
| --- | -------- | --------- | --- | ------- | --------- | --- | --- | ---------- | --- | --- | --- |
ik
µ˜ infinite dilution chemical potential of component i in phase k
ik
µ˜m chemical potential of component i in phase k at unit molality
ik
µ˜c chemical potential of component i in phase k at unit molarity
ik
µˆ chemical potential of component i in phase k assigned from a chemical
ik
|     | equilibrium |                   | constant |     |              |     |     |          |     |     |     |
| --- | ----------- | ----------------- | -------- | --- | ------------ | --- | --- | -------- | --- | --- | --- |
| ν   | vector      | of stoichiometric |          |     | coefficients |     | in  | reaction | r   |     |     |
r
| ν   | vector | of all | stoichiometric |     |     | coefficients |     | for component |     | i   |     |
| --- | ------ | ------ | -------------- | --- | --- | ------------ | --- | ------------- | --- | --- | --- |
i

186 Glossaries
| ν   | vector | of total | stoichiometric |     | coefficients |     |     |     |     |
| --- | ------ | -------- | -------------- | --- | ------------ | --- | --- | --- | --- |
t
| ν   | stoichiometric |     | coefficient | of  | component |     | i   | in reaction | r   |
| --- | -------------- | --- | ----------- | --- | --------- | --- | --- | ----------- | --- |
ir
| ν   | total stoiometric |     | coefficient |     | in  | reaction | r   |     |     |
| --- | ----------------- | --- | ----------- | --- | --- | -------- | --- | --- | --- |
t,r
| ξ   | vector | of reaction | extents |     |     |     |     |     |     |
| --- | ------ | ----------- | ------- | --- | --- | --- | --- | --- | --- |
| ξ   | extent | of reaction | r       |     |     |     |     |     |     |
r
| ξB  | maximum | extent | of  | the backward |     | reaction |     | r   |     |
| --- | ------- | ------ | --- | ------------ | --- | -------- | --- | --- | --- |
r
ξF
|     | maximum | extent | of  | the forward |     | reaction |     | r   |     |
| --- | ------- | ------ | --- | ----------- | --- | -------- | --- | --- | --- |
r
| ρ   | density | of phase | k   |     |     |     |     |     |     |
| --- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- |
k
| ρ   | pure solvent |     | density | in phase | k   |     |     |     |     |
| --- | ------------ | --- | ------- | -------- | --- | --- | --- | --- | --- |
sol,k
Φ matrix of fugacity coefficient composition derivatives in phase k
k
| φ ˆ | fugacity | coefficient | of  | component |     | i in | phase | k   |     |
| --- | -------- | ----------- | --- | --------- | --- | ---- | ----- | --- | --- |
ik
| φs  | saturation | fugacity |     | coefficient | of  | component |     | i   |     |
| --- | ---------- | -------- | --- | ----------- | --- | --------- | --- | --- | --- |
i
| ω   | acentric | factor | of component |     | i   |     |     |     |     |
| --- | -------- | ------ | ------------ | --- | --- | --- | --- | --- | --- |
i
Superscripts
| 0   | initial   | value |     |     |     |     |     |     |     |
| --- | --------- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     | reference | state |     |     |     |     |     |     |     |
◦
| calc | calculated   | value |        |           |     |     |     |     |     |
| ---- | ------------ | ----- | ------ | --------- | --- | --- | --- | --- | --- |
| exp  | experimental |       | value  |           |     |     |     |     |     |
| s    | saturation   |       |        |           |     |     |     |     |     |
| T    | transpose    | of    | matrix | or vector |     |     |     |     |     |
Subscripts
| ( ) | state of | matter | indicator | (solid, |     | liquid, | etc.) |     |     |
| --- | -------- | ------ | --------- | ------- | --- | ------- | ----- | --- | --- |
·
| i   | component |     |     |     |     |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| j   | element   |     |     |     |     |     |     |     |     |

Glossaries 187
| k   | phase       |          |     |     |
| --- | ----------- | -------- | --- | --- |
| l   | liquid      | phase    |     |     |
| q   | dummy       | variable |     |     |
| r   | reaction    |          |     |     |
| s   | solid phase |          |     |     |
| sol | solvent     |          |     |     |
| v   | vapor       | phase    |     |     |
Operators
gradient
∇
2
Laplacian
∇
∆ finite difference, correction quantity in iterative calculations
| ∆   | change | of a property | during combustion | reaction |
| --- | ------ | ------------- | ----------------- | -------- |
c
| ∆   | change | of a property | during formation | reaction |
| --- | ------ | ------------- | ---------------- | -------- |
f
| ∆   | change | of a property | during reaction |     |
| --- | ------ | ------------- | --------------- | --- |
r
Ff Legendre transformation of function f(x) with respect to variable x
i i

Index
| chemical   | equilibrium | constant, | 20  | system, 11    |                    |     |
| ---------- | ----------- | --------- | --- | ------------- | ------------------ | --- |
| component, | 11          |           |     |               |                    |     |
|            |             |           |     | tangent plane | distance function, | 33  |
| primary,   | 29          |           |     |               |                    |     |
| secondary, | 29          |           |     |               |                    |     |
variables
|             |                 |     |     | conjugate, | 14  |     |
| ----------- | --------------- | --- | --- | ---------- | --- | --- |
| element,    | 12, 29          |     |     |            |     |     |
|             |                 |     |     | extensive, | 14  |     |
| enthalpy,   | 14              |     |     |            |     |     |
|             |                 |     |     | intensive, | 14  |     |
| Gibbs       | energy, 14      |     |     | natural,   | 14  |     |
| Gibbs-Duhem | equation,       | 17, | 24  |            |     |     |
| Helmholtz   | energy,         | 14  |     |            |     |     |
| Henry’s     | law, 100        |     |     |            |     |     |
| internal    | energy, 12      |     |     |            |     |     |
| K-value,    | 21              |     |     |            |     |     |
| Wilson      | K-factors,      | 26  |     |            |     |     |
| Lagrangian, | 31              |     |     |            |     |     |
| Legandre    | transformation, | 13  |     |            |     |     |
| molality,   | 102             |     |     |            |     |     |
| molarity,   | 103             |     |     |            |     |     |
phase, 12
| Raoult’s        | law, 25    |     |     |     |     |     |
| --------------- | ---------- | --- | --- | --- | --- | --- |
| reaction,       | 12         |     |     |     |     |     |
| reaction        | extent, 19 |     |     |     |     |     |
| reference       | states, 21 |     |     |     |     |     |
| state function, | 12         |     |     |     |     |     |

1

1

| Center      | for Energy   | Resources  | Engineering | (CERE) |
| ----------- | ------------ | ---------- | ----------- | ------ |
| Department  | of Chemistry |            |             |        |
| Kemitorvet, | Building     | 207        |             |        |
| Technical   | University   | of Denmark |             |        |
| DK-2800     | Kgs. Lyngby  |            |             |        |
| +45 45      | 25 24 19     |            |             |        |
www.kemi.dtu.dk
