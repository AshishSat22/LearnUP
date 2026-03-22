"""generate_data.py — Run once to create all sample data for LearnUP."""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

VIDEOS = {
    "Physics": {
        "Electric Charges and Fields": [
            "Introduction to Electric Charges || https://www.youtube.com/watch?v=x1-SibwIPM4",
            "Coulombs Law Explained || https://www.youtube.com/watch?v=rYjo774UpHI",
            "Electric Field Lines || https://www.youtube.com/watch?v=H3Hg_XGHSss",
            "Gauss Law Derivation || https://www.youtube.com/watch?v=MTsCpZqcHSs",
            "Electric Flux Problems || https://www.youtube.com/watch?v=_oqGmFtE3sA",
        ],
        "Electrostatic Potential": [
            "Electric Potential Intro || https://www.youtube.com/watch?v=elJUghWSVh4",
            "Potential due to a Point Charge || https://www.youtube.com/watch?v=1TKEMoAg8AE",
            "Equipotential Surfaces || https://www.youtube.com/watch?v=6nEB-_bP0xI",
            "Capacitors and Capacitance || https://www.youtube.com/watch?v=X4EUwTwZ110",
            "Energy Stored in Capacitor || https://www.youtube.com/watch?v=5hFC9ugTGLs",
        ],
        "Current Electricity": [
            "Ohms Law and Resistance || https://www.youtube.com/watch?v=J4Vq-xHqUo8",
            "Kirchhoffs Laws || https://www.youtube.com/watch?v=mSGrRfACxig",
            "Wheatstone Bridge || https://www.youtube.com/watch?v=47bF13o8pb8",
            "Potentiometer Working || https://www.youtube.com/watch?v=LT2CiukGQ90",
            "Drift Velocity and Current || https://www.youtube.com/watch?v=BvCNgCuCcQA",
        ],
    },
    "Chemistry": {
        "Solutions": [
            "Types of Solutions || https://www.youtube.com/watch?v=4J-oONkFOqg",
            "Raoults Law Explained || https://www.youtube.com/watch?v=bNtqhxFkCLI",
            "Colligative Properties || https://www.youtube.com/watch?v=z9LxdiyxEQg",
            "Osmosis and Osmotic Pressure || https://www.youtube.com/watch?v=8txkf6mmgEg",
            "Van't Hoff Factor || https://www.youtube.com/watch?v=aRFCeXJ1NJo",
        ],
        "Electrochemistry": [
            "Electrochemical Cells || https://www.youtube.com/watch?v=c28nHbJ0grc",
            "Nernst Equation || https://www.youtube.com/watch?v=9JaoP-DRK2Q",
            "Electrolysis and Faradays Laws || https://www.youtube.com/watch?v=_z-S9qnW2JA",
            "Conductance of Electrolytes || https://www.youtube.com/watch?v=h5PEfS5os7Q",
            "Corrosion and Prevention || https://www.youtube.com/watch?v=BgFPHeoQK7g",
        ],
        "Chemical Kinetics": [
            "Rate of Reaction || https://www.youtube.com/watch?v=TMwMPv1xBFg",
            "Order of Reaction || https://www.youtube.com/watch?v=wnaFNt99Bds",
            "Arrhenius Equation || https://www.youtube.com/watch?v=L3jjMkV_eds",
            "Integrated Rate Laws || https://www.youtube.com/watch?v=7qOFtL3VEBc",
            "Half Life of Reactions || https://www.youtube.com/watch?v=RyIoMGPOFKo",
        ],
    },
    "Maths": {
        "Relations and Functions": [
            "Types of Relations || https://www.youtube.com/watch?v=B_9J3Myhu28",
            "Types of Functions || https://www.youtube.com/watch?v=2BF_LPDSvRk",
            "Composition of Functions || https://www.youtube.com/watch?v=hEBEcqo3GlA",
            "Inverse Functions || https://www.youtube.com/watch?v=aC5L97XFQGY",
            "Binary Operations || https://www.youtube.com/watch?v=_oGMmiNzX0Q",
        ],
        "Matrices and Determinants": [
            "Matrix Operations || https://www.youtube.com/watch?v=kqWCwwyeE6k",
            "Determinant of a Matrix || https://www.youtube.com/watch?v=Ip3X9LOh2dk",
            "Inverse of a Matrix || https://www.youtube.com/watch?v=01c12NaUQDw",
            "Cramers Rule || https://www.youtube.com/watch?v=jBsC34PxzoM",
            "Properties of Determinants || https://www.youtube.com/watch?v=mSld9BhpA_E",
        ],
        "Integrals": [
            "Introduction to Integration || https://www.youtube.com/watch?v=rfG8ce4nNh0",
            "Integration by Substitution || https://www.youtube.com/watch?v=b86_BNOQP5Q",
            "Integration by Parts || https://www.youtube.com/watch?v=oSaTGHKlwwA",
            "Partial Fractions Integration || https://www.youtube.com/watch?v=0TAbSp0DLbI",
            "Definite Integrals and Area || https://www.youtube.com/watch?v=SfNvCFSHOXg",
        ],
    },
}

QUESTIONS = {
    "Physics": {
        "Electric Charges and Fields": """SAMPLE & PAST YEAR QUESTIONS — Electric Charges and Fields
================================================================

SECTION A: 1-Mark Questions
1. What is the SI unit of electric charge?
2. State Coulomb's Law.
3. Define electric field intensity.
4. What is an equipotential surface?
5. State Gauss's Law.

SECTION B: 2-Mark Questions
6. Two charges +3μC and -3μC are placed 10 cm apart. Find the electric force between them.
7. Define electric dipole. Write the expression for the torque on a dipole in a uniform electric field.
8. Sketch the electric field lines for two equal and opposite charges placed close together.

SECTION C: 3-Mark Questions
9. Derive the expression for electric field intensity due to an infinitely long straight wire of linear charge density λ using Gauss's Law.
10. Explain the concept of superposition principle for electric forces.
11. A charge of 2μC is placed at the centre of a cube of side 10 cm. Find the electric flux through the cube.

SECTION D: 5-Mark Questions (Previous Year)
12. (CBSE 2023) Derive the expression for the electric field at a point on the axis of an electric dipole.
13. (CBSE 2022) State and prove Gauss's Law. Apply it to find the electric field due to a uniformly charged spherical shell at a point (i) outside the shell and (ii) inside the shell.
14. (CBSE 2021) A parallel plate capacitor has plates of area A separated by distance d. Find the capacitance. What happens if a dielectric slab of dielectric constant K is inserted?

CASE STUDY (CBSE 2023):
15. A point charge of +2μC is placed at the origin. Answer the following:
  (a) Find electric field at (3, 0, 0) m.
  (b) Find potential at (3, 0, 0) m.
  (c) What is the work done in bringing a charge of +1μC from infinity to this point?
""",
        "Electrostatic Potential": """SAMPLE & PAST YEAR QUESTIONS — Electrostatic Potential
================================================================

SECTION A: 1-Mark Questions
1. Define electric potential. What is its SI unit?
2. What is the potential at a point midway between two equal and opposite charges?
3. Define capacitance of a capacitor.
4. What is a polar molecule? Give one example.
5. Define dielectric constant.

SECTION B: 2-Mark Questions
6. Two capacitors of capacitance 2μF and 3μF are connected in series. Find the equivalent capacitance.
7. Derive the relation between electric field and electric potential.
8. What is the energy density of an electric field? Write its expression.

SECTION C: 3-Mark Questions
9. Derive the expression for the potential energy of a system of two charges.
10. Explain polarisation of a dielectric in an external electric field.
11. (CBSE 2022) Three capacitors of 2μF each are connected (i) in series and (ii) in parallel. Compare the equivalent capacitances.

SECTION D: 5-Mark Questions
12. Derive the expression for the energy stored in a capacitor. How does the energy change when a dielectric slab is introduced with the battery connected?
13. (CBSE 2023) Two large parallel plates are maintained at potentials +V and -V. Find (a) electric field between plates (b) potential at a point midway (c) force on a charge q placed at the midpoint.
""",
        "Current Electricity": """SAMPLE & PAST YEAR QUESTIONS — Current Electricity
================================================================

SECTION A: 1-Mark Questions
1. State Ohm's law.
2. Define resistivity. What is its SI unit?
3. What is the condition for a balanced Wheatstone bridge?
4. Define emf of a cell.
5. What is the principle of a potentiometer?

SECTION B: 2-Mark Questions
6. A wire of resistance 10 Ω is stretched to double its length. Find the new resistance.
7. State Kirchhoff's two laws for electric circuits.
8. Explain why the terminal voltage of a battery is less than its emf when current flows.

SECTION C: 3-Mark Questions
9. Derive the expression for the equivalent resistance of three resistors in parallel.
10. Explain the working of a potentiometer to compare emfs of two cells.
11. A battery of emf 12V and internal resistance 2Ω is connected to a 4Ω resistor. Find the terminal voltage and current.

SECTION D: 5-Mark Questions
12. (CBSE 2023) Derive the condition for balance in a Wheatstone bridge. Explain its use to find unknown resistance.
13. (CBSE 2022) Define drift velocity. Derive the expression relating drift velocity, current, and the number density of electrons.
""",
    },
    "Chemistry": {
        "Solutions": """SAMPLE & PAST YEAR QUESTIONS — Solutions
================================================================

SECTION A: 1-Mark Questions
1. Define mole fraction. Write its formula.
2. What is an ideal solution?
3. State Raoult's Law.
4. Define osmotic pressure.
5. What is van't Hoff factor?

SECTION B: 2-Mark Questions
6. Calculate the mole fraction of ethanol in a solution containing 46g of ethanol and 180g of water.
7. Differentiate between molarity and molality.
8. What is elevation of boiling point? State the formula.

SECTION C: 3-Mark Questions
9. A solution of glucose (M=180) contains 18g per litre. Calculate its molarity and osmotic pressure at 27°C.
10. Explain why a raw mango placed in common salt solution becomes shrivelled.
11. State Henry's Law for solubility of gases. Mention two applications.

SECTION D: 5-Mark Questions
12. (CBSE 2023) What are colligative properties? Explain depression in freezing point with derivation.
13. (CBSE 2022) Calculate the boiling point of a solution of 15g of urea (M=60) in 250g of water. Kb(water)=0.52 K·kg/mol.
""",
        "Electrochemistry": """SAMPLE & PAST YEAR QUESTIONS — Electrochemistry
================================================================

SECTION A: 1-Mark Questions
1. What is a galvanic cell?
2. Define standard electrode potential.
3. State Faraday's first law of electrolysis.
4. What is the unit of molar conductivity?
5. Define corrosion.

SECTION B: 2-Mark Questions
6. Calculate the EMF of the cell: Zn|Zn²⁺(1M)||Cu²⁺(1M)|Cu. (E°Zn=-0.76V, E°Cu=+0.34V)
7. Write the Nernst equation and explain each term.
8. Differentiate between electrolytic and galvanic cells.

SECTION C: 3-Mark Questions
9. Explain the working of a hydrogen-oxygen fuel cell with electrode reactions.
10. How much charge is required to deposit 2.7g of Al from Al³⁺ solution? (Molar mass Al=27)
11. Define limiting molar conductivity. Explain Kohlrausch's Law.

SECTION D: 5-Mark Questions
12. (CBSE 2023) State and explain Faraday's laws. Calculate the mass of silver deposited when 2A current flows for 30 minutes. (Atomic mass Ag=108)
13. (CBSE 2022) Write the half-cell reactions and overall reaction for Daniel cell. Calculate its EMF at 25°C when concentrations are 0.1M and 1M.
""",
        "Chemical Kinetics": """SAMPLE & PAST YEAR QUESTIONS — Chemical Kinetics
================================================================

SECTION A: 1-Mark Questions
1. Define order of a reaction.
2. What is the unit of rate constant for a first-order reaction?
3. Define activation energy.
4. What is a catalyst?
5. State the Arrhenius equation.

SECTION B: 2-Mark Questions
6. The half-life of a first-order reaction is 10 minutes. Find the rate constant.
7. What is pseudo-first-order reaction? Give an example.
8. How does temperature affect the rate of a reaction? (Give quantitative relation)

SECTION C: 3-Mark Questions
9. Derive the integrated rate law for a first-order reaction.
10. For the reaction A → B, the rate doubles when concentration of A is doubled. Find the order. Write the rate law.
11. (CBSE 2022) The rate constant of a reaction is 1.54×10⁻³ s⁻¹. Calculate the half-life and time for 75% completion.

SECTION D: 5-Mark Questions
12. (CBSE 2023) What is activation energy? How does a catalyst lower it? Draw the energy profile diagram with and without catalyst.
13. (CBSE 2022) Explain the effect of temperature on rate constant using Arrhenius equation. A reaction has Ea=50 kJ/mol. Find k at 37°C if k=2×10⁻⁴ s⁻¹ at 27°C. (R=8.314 J/mol·K)
""",
    },
    "Maths": {
        "Relations and Functions": """SAMPLE & PAST YEAR QUESTIONS — Relations and Functions
================================================================

SECTION A: 1-Mark Questions
1. Define a reflexive relation.
2. What is a bijective function?
3. If f(x) = 2x+3, find f⁻¹(x).
4. Define an equivalence relation.
5. What is the range of f(x) = sin x?

SECTION B: 2-Mark Questions
6. Show that the relation R on ℤ defined by R = {(a,b): 2 divides (a-b)} is an equivalence relation.
7. Let f: ℝ→ℝ be f(x)=x² and g: ℝ→ℝ be g(x)=x+1. Find fog and gof.
8. Check if f(x) = 3x-5 is one-one and onto.

SECTION C: 3-Mark Questions
9. Prove that f: ℝ→ℝ defined by f(x) = 4x+3 is invertible. Find f⁻¹.
10. Let A = {1,2,3}. Write all equivalence relations on A that contain (1,2).
11. (CBSE 2023) Show that the relation R defined by (a,b)R(c,d) iff a+d=b+c on ℕ×ℕ is an equivalence relation.

SECTION D: 5-Mark Questions
12. (CBSE 2023) Let f: ℕ→ℕ be defined by f(n)=(n+1)/2 if n is odd, n/2 if n is even. Is f one-one? Is f onto?
13. (CBSE 2022) Consider f: {1,2,3}→{a,b,c} given by f(1)=a, f(2)=b, f(3)=c. Show f is bijective and find f⁻¹.
""",
        "Matrices and Determinants": """SAMPLE & PAST YEAR QUESTIONS — Matrices and Determinants
================================================================

SECTION A: 1-Mark Questions
1. If A is a 2×3 matrix and B is 3×4 matrix, what is the order of AB?
2. What is the value of |I₃| (determinant of 3×3 identity matrix)?
3. Define singular matrix.
4. If A is skew-symmetric, what is A^T?
5. What is cofactor expansion?

SECTION B: 2-Mark Questions
6. Find the inverse of [[2,1],[1,1]].
7. Prove that the determinant of a matrix and its transpose are equal.
8. If A = [[1,2],[3,4]], find adj(A).

SECTION C: 3-Mark Questions
9. Using Cramer's Rule, solve: 2x+y=5, x+3y=10.
10. Prove that |AB| = |A|·|B| using a 2×2 example.
11. (CBSE 2023) If A = [[2,-1],[-1,2]], show that A²-4A+3I=0. Hence find A⁻¹.

SECTION D: 5-Mark Questions
12. (CBSE 2023) Using matrix method, solve the system: x+y+z=6, 2x-y+z=3, x+2y-z=2.
13. (CBSE 2022) Find A⁻¹ where A=[[1,1,1],[1,2,-3],[2,-1,3]] and use it to solve the system of equations.
""",
        "Integrals": """SAMPLE & PAST YEAR QUESTIONS — Integrals
================================================================

SECTION A: 1-Mark Questions
1. Evaluate ∫x^n dx.
2. What is ∫sin x dx?
3. Write the formula for integration by parts.
4. Evaluate ∫(1/x) dx.
5. What is the value of ∫₀^(π/2) sin x dx?

SECTION B: 2-Mark Questions
6. Evaluate ∫ x·eˣ dx using integration by parts.
7. Evaluate ∫ dx / (1+x²).
8. Find ∫ (2x+3) / (x²+3x+5) dx.

SECTION C: 3-Mark Questions
9. Evaluate ∫ x·sin x dx using integration by parts.
10. Using partial fractions, evaluate ∫ dx / (x²-1).
11. (CBSE 2023) Evaluate ∫₁³ (x²+x) dx using the definition (limit of sum).

SECTION D: 5-Mark Questions
12. (CBSE 2023) Evaluate ∫₀^π x·sinx / (1+cos²x) dx using properties of definite integrals.
13. (CBSE 2022) Evaluate ∫ (3x+5) / √(x²+4x+3) dx. Also find ∫₀¹ x·eˣ dx.
""",
    },
}

def make_quiz(subject, chapter):
    banks = {
        ("Physics","Electric Charges and Fields"): [
            {"question":"The SI unit of electric charge is:","options":["Coulomb","Ampere","Volt","Joule"],"answer":"Coulomb","difficulty":"Easy"},
            {"question":"Coulomb's law constant k equals:","options":["9×10⁹ Nm²/C²","8.85×10⁻¹²","1.6×10⁻¹⁹","6.67×10⁻¹¹"],"answer":"9×10⁹ Nm²/C²","difficulty":"Easy"},
            {"question":"Electric field lines originate from:","options":["Positive charge","Negative charge","Neutral body","Ground"],"answer":"Positive charge","difficulty":"Easy"},
            {"question":"Gauss's Law relates electric flux to:","options":["Enclosed charge","Total charge","Surface area","Capacitance"],"answer":"Enclosed charge","difficulty":"Medium"},
            {"question":"The electric field inside a conductor in electrostatic equilibrium is:","options":["Zero","Maximum","Negative","Infinite"],"answer":"Zero","difficulty":"Easy"},
            {"question":"Two charges +q and -q separated by distance 2a form a:","options":["Dipole","Capacitor","Resistor","Inductor"],"answer":"Dipole","difficulty":"Easy"},
            {"question":"The unit of electric flux is:","options":["Nm²/C","N/C","Vm","C/m²"],"answer":"Nm²/C","difficulty":"Medium"},
            {"question":"Dielectric constant of vacuum is:","options":["1","0","∞","8.85×10⁻¹²"],"answer":"1","difficulty":"Easy"},
            {"question":"A conductor has charge on its:","options":["Surface","Core","Middle","Uniformly"],"answer":"Surface","difficulty":"Easy"},
            {"question":"Coulomb's law is analogous to:","options":["Newton's law of gravitation","Ohm's law","Faraday's law","Hooke's law"],"answer":"Newton's law of gravitation","difficulty":"Medium"},
            {"question":"The force between two charges is inversely proportional to:","options":["Square of distance","Distance","Cube of distance","Fourth power"],"answer":"Square of distance","difficulty":"Easy"},
            {"question":"Electric field due to infinite sheet of charge density σ is:","options":["σ/2ε₀","σ/ε₀","2σ/ε₀","σ²/ε₀"],"answer":"σ/2ε₀","difficulty":"Hard"},
            {"question":"Electric potential is a:","options":["Scalar","Vector","Tensor","None"],"answer":"Scalar","difficulty":"Easy"},
            {"question":"When charge is tripled and distance halved, force becomes:","options":["36 times","9 times","18 times","4 times"],"answer":"36 times","difficulty":"Hard"},
            {"question":"The work done in moving a charge on an equipotential surface is:","options":["Zero","Maximum","Negative","Positive"],"answer":"Zero","difficulty":"Medium"},
            {"question":"Which material allows charge to flow freely?","options":["Conductor","Insulator","Semiconductor","Dielectric"],"answer":"Conductor","difficulty":"Easy"},
            {"question":"Electric field lines are always perpendicular to:","options":["Equipotential surfaces","Field direction","Current","None"],"answer":"Equipotential surfaces","difficulty":"Medium"},
            {"question":"Permittivity of free space ε₀ value is:","options":["8.85×10⁻¹² C²/Nm²","9×10⁹","1.6×10⁻¹⁹","6.67×10⁻¹¹"],"answer":"8.85×10⁻¹² C²/Nm²","difficulty":"Hard"},
            {"question":"Two equal positive charges repel with force F. If one charge is doubled, force becomes:","options":["2F","4F","F/2","F"],"answer":"2F","difficulty":"Medium"},
            {"question":"Linear charge density has SI unit:","options":["C/m","C/m²","C/m³","C"],"answer":"C/m","difficulty":"Medium"},
        ],
        ("Physics","Electrostatic Potential"): [
            {"question":"SI unit of electric potential is:","options":["Volt","Joule","Coulomb","Tesla"],"answer":"Volt","difficulty":"Easy"},
            {"question":"Capacitance SI unit is:","options":["Farad","Henry","Ohm","Weber"],"answer":"Farad","difficulty":"Easy"},
            {"question":"Energy stored in capacitor is:","options":["½CV²","CV²","½CV","2CV²"],"answer":"½CV²","difficulty":"Medium"},
            {"question":"Capacitors in series have:","options":["Same charge","Same voltage","Same energy","Same field"],"answer":"Same charge","difficulty":"Medium"},
            {"question":"Introducing a dielectric increases capacitance by factor:","options":["K","1/K","K²","√K"],"answer":"K","difficulty":"Medium"},
            {"question":"Potential due to a point charge varies as:","options":["1/r","1/r²","r","r²"],"answer":"1/r","difficulty":"Easy"},
            {"question":"Work done by electric force is W = q(V₁-V₂). If V₁=V₂, work is:","options":["Zero","Maximum","Negative","Infinite"],"answer":"Zero","difficulty":"Easy"},
            {"question":"Parallel plate capacitor with plate area A, separation d: C =","options":["ε₀A/d","ε₀d/A","ε₀Ad","A/d"],"answer":"ε₀A/d","difficulty":"Medium"},
            {"question":"For capacitors in parallel, equivalent capacitance is:","options":["Sum of all","Reciprocal sum","Product","Difference"],"answer":"Sum of all","difficulty":"Easy"},
            {"question":"Polar molecules have:","options":["Permanent dipole moment","No dipole","Zero charge","Equal charges"],"answer":"Permanent dipole moment","difficulty":"Medium"},
            {"question":"The relation E = -dV/dr means E is:","options":["Negative gradient of V","Sum of V","Integral of V","Product of V"],"answer":"Negative gradient of V","difficulty":"Hard"},
            {"question":"If C₁=2μF and C₂=4μF in series, equivalent is:","options":["4/3 μF","6 μF","8 μF","2 μF"],"answer":"4/3 μF","difficulty":"Hard"},
            {"question":"Potential at infinity is taken as:","options":["Zero","Maximum","Minimum","Undefined"],"answer":"Zero","difficulty":"Easy"},
            {"question":"Van de Graaff generator works on principle of:","options":["Charge accumulation on outer surface","Induction","Conduction","All"],"answer":"Charge accumulation on outer surface","difficulty":"Hard"},
            {"question":"Potential energy of a dipole in uniform field E is:","options":["−pEcosθ","pEcosθ","pEsinθ","pE"],"answer":"−pEcosθ","difficulty":"Hard"},
            {"question":"Electric field inside a hollow conductor is:","options":["Zero","Non-zero","Negative","Positive"],"answer":"Zero","difficulty":"Easy"},
            {"question":"Torque on a dipole in uniform field is:","options":["p×E","p·E","E/p","p/E"],"answer":"p×E","difficulty":"Medium"},
            {"question":"When battery is disconnected and dielectric inserted, energy:","options":["Decreases","Increases","Stays same","Doubles"],"answer":"Decreases","difficulty":"Hard"},
            {"question":"Gauss's law in medium with dielectric uses:","options":["ε = ε₀K","ε₀ only","K only","ε₀/K"],"answer":"ε = ε₀K","difficulty":"Hard"},
            {"question":"Two capacitors 3μF and 6μF in parallel; equivalent capacitance:","options":["9 μF","2 μF","4.5 μF","18 μF"],"answer":"9 μF","difficulty":"Easy"},
        ],
        ("Physics","Current Electricity"): [
            {"question":"Ohm's Law states V =","options":["IR","I/R","R/I","I²R"],"answer":"IR","difficulty":"Easy"},
            {"question":"SI unit of resistance is:","options":["Ohm","Siemen","Farad","Henry"],"answer":"Ohm","difficulty":"Easy"},
            {"question":"When wire length is doubled, resistance:","options":["Doubles","Halves","Unchanged","Quadruples"],"answer":"Doubles","difficulty":"Easy"},
            {"question":"Kirchhoff's Current Law is based on:","options":["Conservation of charge","Conservation of energy","Ohm's law","Faraday's law"],"answer":"Conservation of charge","difficulty":"Medium"},
            {"question":"EMF of a cell is 12V, internal resistance 2Ω, external 4Ω. Current:","options":["2A","3A","6A","4A"],"answer":"2A","difficulty":"Medium"},
            {"question":"Resistivity depends on:","options":["Material and temperature","Only length","Only area","Only current"],"answer":"Material and temperature","difficulty":"Medium"},
            {"question":"Wheatstone bridge is balanced when:","options":["P/Q = R/S","P/Q = S/R","P+Q=R+S","PQ=RS"],"answer":"P/Q = R/S","difficulty":"Medium"},
            {"question":"Drift velocity of electrons is of order:","options":["10⁻⁴ m/s","10⁸ m/s","10² m/s","1 m/s"],"answer":"10⁻⁴ m/s","difficulty":"Hard"},
            {"question":"Potentiometer is preferred over voltmeter because it:","options":["Draws no current","Is cheaper","Is faster","Has less resistance"],"answer":"Draws no current","difficulty":"Medium"},
            {"question":"Carbon resistors have colour codes because:","options":["Small size makes printing hard","They are expensive","Standard practice","None"],"answer":"Small size makes printing hard","difficulty":"Easy"},
            {"question":"Terminal voltage (V) of cell: V =","options":["E - Ir","E + Ir","E × Ir","E / Ir"],"answer":"E - Ir","difficulty":"Medium"},
            {"question":"Three 3Ω resistors in parallel give:","options":["1Ω","9Ω","3Ω","6Ω"],"answer":"1Ω","difficulty":"Medium"},
            {"question":"Power dissipated in resistor R carrying current I is:","options":["I²R","IR","IR²","I/R"],"answer":"I²R","difficulty":"Easy"},
            {"question":"Superconductors have resistance:","options":["Zero","Infinite","Very high","0.5Ω"],"answer":"Zero","difficulty":"Easy"},
            {"question":"Temperature coefficient of resistance for metals is:","options":["Positive","Negative","Zero","Variable"],"answer":"Positive","difficulty":"Medium"},
            {"question":"Meter bridge works on principle of:","options":["Wheatstone bridge","Potentiometer","Kirchhoff's law","Ohm's law"],"answer":"Wheatstone bridge","difficulty":"Medium"},
            {"question":"Current density J is related to E by:","options":["J = σE","J = E/σ","J = σ/E","J = σE²"],"answer":"J = σE","difficulty":"Hard"},
            {"question":"Cells in series: total emf is:","options":["Sum of emfs","Average","Product","Minimum"],"answer":"Sum of emfs","difficulty":"Easy"},
            {"question":"Resistance of conductor increases with temperature for:","options":["Metals","Semiconductors","Superconductors","Insulators only"],"answer":"Metals","difficulty":"Medium"},
            {"question":"Galvanometer is converted to ammeter by connecting:","options":["Low resistance in parallel","High resistance in series","Low resistance in series","High resistance in parallel"],"answer":"Low resistance in parallel","difficulty":"Hard"},
        ],
        ("Chemistry","Solutions"): [
            {"question":"Mole fraction of solvent + mole fraction of solute =","options":["1","0","∞","0.5"],"answer":"1","difficulty":"Easy"},
            {"question":"Raoult's Law deals with:","options":["Vapour pressure","Boiling point","Density","Viscosity"],"answer":"Vapour pressure","difficulty":"Easy"},
            {"question":"Colligative properties depend on:","options":["Number of solute particles","Nature of solute","Mass of solute","Volume of solution"],"answer":"Number of solute particles","difficulty":"Medium"},
            {"question":"Osmosis is movement of solvent through:","options":["Semipermeable membrane","Any membrane","Filter paper","Glass"],"answer":"Semipermeable membrane","difficulty":"Easy"},
            {"question":"Van't Hoff factor for NaCl:","options":["2","1","3","0.5"],"answer":"2","difficulty":"Medium"},
            {"question":"Ebullioscopic constant Kb depends on:","options":["Solvent","Solute","Concentration","Volume"],"answer":"Solvent","difficulty":"Medium"},
            {"question":"Molality is defined as:","options":["Moles of solute per kg solvent","Moles per litre","Mass per litre","Moles per mole"],"answer":"Moles of solute per kg solvent","difficulty":"Easy"},
            {"question":"An ideal solution has ΔHmix =","options":["Zero","Positive","Negative","Infinite"],"answer":"Zero","difficulty":"Medium"},
            {"question":"Reverse osmosis is used in:","options":["Water purification","Distillation","Crystallisation","Filtration"],"answer":"Water purification","difficulty":"Easy"},
            {"question":"Henry's Law constant increases with:","options":["Temperature","Pressure","Concentration","None"],"answer":"Temperature","difficulty":"Hard"},
            {"question":"Elevation of boiling point ΔTb is proportional to:","options":["Molality","Molarity","Mole fraction","Normality"],"answer":"Molality","difficulty":"Medium"},
            {"question":"Depression in freezing point is a:","options":["Colligative property","Additive property","Physical property","Chemical property"],"answer":"Colligative property","difficulty":"Easy"},
            {"question":"The unit of osmotic pressure is:","options":["Pascal","Mol/L","g/mol","Kelvin"],"answer":"Pascal","difficulty":"Easy"},
            {"question":"π = CRT gives osmotic pressure where R is:","options":["Gas constant","Resistance","Rate","None"],"answer":"Gas constant","difficulty":"Medium"},
            {"question":"Azeotropes are mixtures that:","options":["Boil at constant temperature","Never boil","Freeze at 0°C","Evaporate slowly"],"answer":"Boil at constant temperature","difficulty":"Hard"},
            {"question":"18g of water contains how many moles?","options":["1","2","0.5","18"],"answer":"1","difficulty":"Easy"},
            {"question":"Which shows maximum boiling point elevation per gram?","options":["Al₂(SO₄)₃","NaCl","Glucose","Urea"],"answer":"Al₂(SO₄)₃","difficulty":"Hard"},
            {"question":"Normality = Molarity × n-factor. For H₂SO₄, n-factor is:","options":["2","1","3","0.5"],"answer":"2","difficulty":"Medium"},
            {"question":"PPM means parts per:","options":["Million","Thousand","Hundred","Billion"],"answer":"Million","difficulty":"Easy"},
            {"question":"Isotonic solutions have:","options":["Same osmotic pressure","Same density","Same concentration","Same temperature"],"answer":"Same osmotic pressure","difficulty":"Medium"},
        ],
        ("Chemistry","Electrochemistry"): [
            {"question":"In galvanic cell, oxidation occurs at:","options":["Anode","Cathode","Both","Neither"],"answer":"Anode","difficulty":"Easy"},
            {"question":"Standard hydrogen electrode has potential:","options":["0 V","1 V","-1 V","0.5 V"],"answer":"0 V","difficulty":"Easy"},
            {"question":"Faraday's constant F =","options":["96500 C/mol","6.022×10²³","8.314","1.6×10⁻¹⁹"],"answer":"96500 C/mol","difficulty":"Medium"},
            {"question":"Nernst equation is used to find:","options":["Cell potential at non-standard conditions","Equilibrium constant only","Rate","Enthalpy"],"answer":"Cell potential at non-standard conditions","difficulty":"Medium"},
            {"question":"Molar conductivity increases with dilution for:","options":["Strong electrolytes","Weak electrolytes","Both","Neither"],"answer":"Weak electrolytes","difficulty":"Hard"},
            {"question":"EMF of Daniel cell at standard conditions:","options":["1.10 V","0.76 V","0.34 V","2.0 V"],"answer":"1.10 V","difficulty":"Medium"},
            {"question":"Electrolysis of water produces H₂ at:","options":["Cathode","Anode","Both electrodes","None"],"answer":"Cathode","difficulty":"Easy"},
            {"question":"Kohlrausch's Law applies at:","options":["Infinite dilution","High concentration","Normal dilution","Standard state"],"answer":"Infinite dilution","difficulty":"Hard"},
            {"question":"Corrosion of iron is essentially:","options":["Electrochemical process","Thermal process","Physical process","Chemical only"],"answer":"Electrochemical process","difficulty":"Medium"},
            {"question":"In electrolytic cell, cations move to:","options":["Cathode","Anode","Both","Neither"],"answer":"Cathode","difficulty":"Easy"},
            {"question":"Fuel cells convert chemical energy to:","options":["Electrical energy","Heat","Mechanical","Light"],"answer":"Electrical energy","difficulty":"Easy"},
            {"question":"ΔG° = -nFE°. When E° is positive, reaction is:","options":["Spontaneous","Non-spontaneous","At equilibrium","Impossible"],"answer":"Spontaneous","difficulty":"Medium"},
            {"question":"Mass deposited in electrolysis ∝","options":["Charge passed","Time only","Current only","Voltage"],"answer":"Charge passed","difficulty":"Medium"},
            {"question":"Salt bridge maintains:","options":["Electrical neutrality","Electron flow","Ion concentration","pH"],"answer":"Electrical neutrality","difficulty":"Medium"},
            {"question":"Specific conductance unit is:","options":["S/m","S·m","S/m²","Ω"],"answer":"S/m","difficulty":"Hard"},
            {"question":"Lead storage battery has emf per cell:","options":["2 V","1.5 V","12 V","6 V"],"answer":"2 V","difficulty":"Medium"},
            {"question":"Nickel-Cadmium cell is:","options":["Rechargeable","Primary","Fuel cell","Electrolytic"],"answer":"Rechargeable","difficulty":"Easy"},
            {"question":"At higher temperature, EMF of galvanic cell generally:","options":["Changes (depends on reaction)","Always increases","Always decreases","Stays same"],"answer":"Changes (depends on reaction)","difficulty":"Hard"},
            {"question":"Reduction potential of Zn²⁺/Zn is:","options":["-0.76 V","+0.76 V","+0.34 V","-0.34 V"],"answer":"-0.76 V","difficulty":"Medium"},
            {"question":"Cathodic protection prevents:","options":["Corrosion","Oxidation","Reduction","Dissolution"],"answer":"Corrosion","difficulty":"Medium"},
        ],
        ("Chemistry","Chemical Kinetics"): [
            {"question":"Rate of reaction is defined as change in concentration per:","options":["Unit time","Unit volume","Unit pressure","Unit mass"],"answer":"Unit time","difficulty":"Easy"},
            {"question":"For zero-order reaction, rate =","options":["k","k[A]","k[A]²","k/[A]"],"answer":"k","difficulty":"Medium"},
            {"question":"Unit of rate constant for first-order reaction:","options":["s⁻¹","mol/L·s","L/mol·s","mol²/L²·s"],"answer":"s⁻¹","difficulty":"Medium"},
            {"question":"Half-life of first-order reaction is:","options":["0.693/k","0.693k","k/0.693","1/k"],"answer":"0.693/k","difficulty":"Medium"},
            {"question":"Activation energy can be determined from:","options":["Arrhenius plot (ln k vs 1/T)","Rate vs concentration","Half-life","Order"],"answer":"Arrhenius plot (ln k vs 1/T)","difficulty":"Hard"},
            {"question":"Catalyst increases rate by:","options":["Lowering activation energy","Providing reactants","Increasing temperature","Increasing pressure"],"answer":"Lowering activation energy","difficulty":"Easy"},
            {"question":"Molecularity of a reaction:","options":["Cannot be zero or fraction","Can be any number","Is same as order","Is always 1"],"answer":"Cannot be zero or fraction","difficulty":"Hard"},
            {"question":"For the reaction 2A → B, if [A] doubles and rate quadruples, order =","options":["2","1","3","0"],"answer":"2","difficulty":"Medium"},
            {"question":"Temperature coefficient (10°C rise) typically doubles:","options":["Rate","Equilibrium constant","Activation energy","Frequency factor"],"answer":"Rate","difficulty":"Easy"},
            {"question":"Rate law is determined by:","options":["Experiment","Stoichiometry only","Balanced equation","Mechanism always"],"answer":"Experiment","difficulty":"Medium"},
            {"question":"A + B → Products. Rate = k[A][B]². Overall order:","options":["3","2","1","0"],"answer":"3","difficulty":"Medium"},
            {"question":"Integrated rate law for first order: [A] =","options":["[A₀]e⁻ᵏᵗ","[A₀]+kt","[A₀]-kt","[A₀]/(1+kt)"],"answer":"[A₀]e⁻ᵏᵗ","difficulty":"Hard"},
            {"question":"Pseudo-first-order reaction example:","options":["Acid hydrolysis of ester","Neutralisation","Combustion","Photosynthesis"],"answer":"Acid hydrolysis of ester","difficulty":"Medium"},
            {"question":"Frequency factor A in Arrhenius equation represents:","options":["Collision frequency with proper orientation","Energy barrier","Temperature","Concentration"],"answer":"Collision frequency with proper orientation","difficulty":"Hard"},
            {"question":"For zero-order reaction, half-life is:","options":["[A₀]/2k","0.693/k","k/[A₀]","1/k"],"answer":"[A₀]/2k","difficulty":"Hard"},
            {"question":"The rate constant k at higher temperature is:","options":["Larger","Smaller","Same","Zero"],"answer":"Larger","difficulty":"Easy"},
            {"question":"Effective collisions are those with:","options":["Energy ≥ Ea and proper orientation","Any energy","High speed only","Low temperature"],"answer":"Energy ≥ Ea and proper orientation","difficulty":"Medium"},
            {"question":"If order = 2 and [A] is halved, rate becomes:","options":["1/4 of original","1/2","Same","Double"],"answer":"1/4 of original","difficulty":"Medium"},
            {"question":"Which graph is linear for first-order reaction?","options":["ln[A] vs t","[A] vs t","[A]² vs t","1/[A] vs t"],"answer":"ln[A] vs t","difficulty":"Hard"},
            {"question":"Rate of reaction can be increased by:","options":["All of the above","Increasing temperature","Adding catalyst","Increasing concentration"],"answer":"All of the above","difficulty":"Easy"},
        ],
        ("Maths","Relations and Functions"): [
            {"question":"A relation R on set A is reflexive if:","options":["(a,a)∈R for all a∈A","(a,b)∈R ⟹ (b,a)∈R","(a,b),(b,c)∈R ⟹ (a,c)∈R","None"],"answer":"(a,a)∈R for all a∈A","difficulty":"Easy"},
            {"question":"A function f: A→B is onto if:","options":["Every element of B has a preimage","f is one-one","f(a)=f(b) ⟹ a=b","Domain equals codomain"],"answer":"Every element of B has a preimage","difficulty":"Easy"},
            {"question":"If f(x)=2x+1, then f⁻¹(x) =","options":["(x-1)/2","(x+1)/2","2x-1","x/2"],"answer":"(x-1)/2","difficulty":"Medium"},
            {"question":"An equivalence relation must be:","options":["Reflexive, symmetric, transitive","Reflexive and symmetric only","Symmetric and transitive only","Reflexive only"],"answer":"Reflexive, symmetric, transitive","difficulty":"Medium"},
            {"question":"fog(x) means:","options":["f(g(x))","g(f(x))","f(x)+g(x)","f(x)×g(x)"],"answer":"f(g(x))","difficulty":"Easy"},
            {"question":"Number of binary operations on a set with n elements:","options":["n^(n²)","n!","n²","2n"],"answer":"n^(n²)","difficulty":"Hard"},
            {"question":"f: ℝ→ℝ, f(x)=x² is:","options":["Neither one-one nor onto","One-one","Onto","Bijective"],"answer":"Neither one-one nor onto","difficulty":"Medium"},
            {"question":"If n(A)=3 and n(B)=2, total functions from A to B:","options":["8","6","9","4"],"answer":"8","difficulty":"Medium"},
            {"question":"Identity function I(x) =","options":["x","x+1","x²","1"],"answer":"x","difficulty":"Easy"},
            {"question":"A function has an inverse if and only if it is:","options":["Bijective","Only injective","Only surjective","Constant"],"answer":"Bijective","difficulty":"Medium"},
            {"question":"If f∘g = I (identity), then g is:","options":["Left inverse of f","Right inverse of f","Same as f","None"],"answer":"Left inverse of f","difficulty":"Hard"},
            {"question":"Relation R = {(1,1),(2,2),(3,3)} on {1,2,3} is:","options":["Equivalence relation","Not reflexive","Not transitive","Only symmetric"],"answer":"Equivalence relation","difficulty":"Medium"},
            {"question":"Empty relation on a nonempty set is:","options":["Symmetric and transitive but not reflexive","Reflexive","Equivalence","None"],"answer":"Symmetric and transitive but not reflexive","difficulty":"Hard"},
            {"question":"Universal relation on set A is:","options":["A×A","Empty set","Identity","None"],"answer":"A×A","difficulty":"Easy"},
            {"question":"If f: A→B and g: B→C both bijective, then g∘f is:","options":["Bijective","Only injective","Only surjective","Not a function"],"answer":"Bijective","difficulty":"Medium"},
            {"question":"Binary operation * on ℤ defined by a*b=a-b is:","options":["Neither commutative nor associative","Commutative","Associative","Both"],"answer":"Neither commutative nor associative","difficulty":"Hard"},
            {"question":"If R is symmetric then:","options":["(a,b)∈R ⟹ (b,a)∈R","(a,a)∈R always","(a,b),(b,c)∈R ⟹ (a,c)∈R","None"],"answer":"(a,b)∈R ⟹ (b,a)∈R","difficulty":"Easy"},
            {"question":"f(x) = |x| from ℝ to ℝ is:","options":["Many-one and into","Bijective","One-one","Onto"],"answer":"Many-one and into","difficulty":"Medium"},
            {"question":"Number of equivalence relations on {1,2} is:","options":["2","1","3","4"],"answer":"2","difficulty":"Hard"},
            {"question":"If f: ℝ→ℝ is f(x)=3x-5, then f is:","options":["Bijective","Only injective","Only surjective","None"],"answer":"Bijective","difficulty":"Medium"},
        ],
        ("Maths","Matrices and Determinants"): [
            {"question":"Order of product AB where A is 2×3 and B is 3×4:","options":["2×4","3×3","2×3","4×2"],"answer":"2×4","difficulty":"Easy"},
            {"question":"Transpose of matrix A is denoted:","options":["Aᵀ","A⁻¹","adj(A)","|A|"],"answer":"Aᵀ","difficulty":"Easy"},
            {"question":"A square matrix A is singular if:","options":["|A|=0","|A|=1","A is symmetric","A is diagonal"],"answer":"|A|=0","difficulty":"Easy"},
            {"question":"Determinant of identity matrix Iₙ is:","options":["1","0","n","n!"],"answer":"1","difficulty":"Easy"},
            {"question":"|AB| equals:","options":["|A||B|","|A|+|B|","|A|-|B|","|A|/|B|"],"answer":"|A||B|","difficulty":"Medium"},
            {"question":"A matrix equals its transpose ⟹ matrix is:","options":["Symmetric","Skew-symmetric","Orthogonal","Singular"],"answer":"Symmetric","difficulty":"Easy"},
            {"question":"Skew-symmetric matrix has diagonal elements all:","options":["Zero","One","Negative","Equal"],"answer":"Zero","difficulty":"Medium"},
            {"question":"A⁻¹ = adj(A)/|A|. This requires:","options":["|A|≠0","A is symmetric","A is diagonal","A is square only"],"answer":"|A|≠0","difficulty":"Medium"},
            {"question":"Number of elements in a 3×4 matrix:","options":["12","7","9","16"],"answer":"12","difficulty":"Easy"},
            {"question":"For matrices AB = BA is:","options":["Not always true","Always true","Never true","True only for diagonal"],"answer":"Not always true","difficulty":"Medium"},
            {"question":"If |A|=5 for 3×3 matrix A, then |3A| =","options":["135","15","45","5"],"answer":"135","difficulty":"Hard"},
            {"question":"Cofactor C₁₁ of matrix A is:","options":["(-1)²M₁₁","M₁₁","(-1)M₁₁","-M₁₁"],"answer":"(-1)²M₁₁","difficulty":"Hard"},
            {"question":"Rank of zero matrix is:","options":["0","1","∞","Undefined"],"answer":"0","difficulty":"Medium"},
            {"question":"If A is 3×3, |adj(A)| =","options":["|A|²","|A|","|A|³","1/|A|"],"answer":"|A|²","difficulty":"Hard"},
            {"question":"System AX=B has unique solution when:","options":["|A|≠0","|A|=0","B=0","A is symmetric"],"answer":"|A|≠0","difficulty":"Medium"},
            {"question":"(A+B)ᵀ =","options":["Aᵀ+Bᵀ","Aᵀ-Bᵀ","BᵀAᵀ","AᵀBᵀ"],"answer":"Aᵀ+Bᵀ","difficulty":"Easy"},
            {"question":"(AB)ᵀ =","options":["BᵀAᵀ","AᵀBᵀ","Aᵀ+Bᵀ","BA"],"answer":"BᵀAᵀ","difficulty":"Medium"},
            {"question":"The trace of a matrix is:","options":["Sum of diagonal elements","Sum of all elements","Determinant","Product of diagonal"],"answer":"Sum of diagonal elements","difficulty":"Medium"},
            {"question":"Matrix multiplication is:","options":["Associative but not commutative","Commutative","Neither","Both"],"answer":"Associative but not commutative","difficulty":"Hard"},
            {"question":"If A²=A, matrix A is called:","options":["Idempotent","Involutory","Nilpotent","Orthogonal"],"answer":"Idempotent","difficulty":"Hard"},
        ],
        ("Maths","Integrals"): [
            {"question":"∫xⁿ dx =","options":["xⁿ⁺¹/(n+1)+C","nxⁿ⁻¹+C","xⁿ+C","xⁿ⁺¹+C"],"answer":"xⁿ⁺¹/(n+1)+C","difficulty":"Easy"},
            {"question":"∫(1/x) dx =","options":["ln|x|+C","x+C","1/x²+C","eˣ+C"],"answer":"ln|x|+C","difficulty":"Easy"},
            {"question":"∫eˣ dx =","options":["eˣ+C","eˣ/x+C","xeˣ+C","eˣ-1+C"],"answer":"eˣ+C","difficulty":"Easy"},
            {"question":"∫cos x dx =","options":["sin x+C","-sin x+C","cos x+C","-cos x+C"],"answer":"sin x+C","difficulty":"Easy"},
            {"question":"∫sin x dx =","options":["-cos x+C","cos x+C","sin x+C","-sin x+C"],"answer":"-cos x+C","difficulty":"Easy"},
            {"question":"Integration by parts formula: ∫u dv =","options":["uv - ∫v du","uv + ∫v du","u∫dv","∫u·∫v"],"answer":"uv - ∫v du","difficulty":"Medium"},
            {"question":"∫₀^(π/2) sin x dx =","options":["1","0","π/2","-1"],"answer":"1","difficulty":"Medium"},
            {"question":"∫ dx/(1+x²) =","options":["tan⁻¹x+C","sin⁻¹x+C","cos⁻¹x+C","sec⁻¹x+C"],"answer":"tan⁻¹x+C","difficulty":"Medium"},
            {"question":"∫ dx/√(1-x²) =","options":["sin⁻¹x+C","cos⁻¹x+C","tan⁻¹x+C","sec⁻¹x+C"],"answer":"sin⁻¹x+C","difficulty":"Medium"},
            {"question":"If ∫₀ᵃ f(x)dx, property: ∫₀ᵃ f(a-x)dx =","options":["Same as ∫₀ᵃ f(x)dx","Zero","2∫₀ᵃ f(x)dx","Negative"],"answer":"Same as ∫₀ᵃ f(x)dx","difficulty":"Hard"},
            {"question":"∫₋ₐᵃ f(x)dx = 0 when f is:","options":["Odd function","Even function","Constant","Linear"],"answer":"Odd function","difficulty":"Medium"},
            {"question":"∫ sec²x dx =","options":["tan x+C","-cot x+C","sec x+C","sin x+C"],"answer":"tan x+C","difficulty":"Easy"},
            {"question":"∫ x·eˣ dx =","options":["eˣ(x-1)+C","xeˣ+C","eˣ+C","x²eˣ+C"],"answer":"eˣ(x-1)+C","difficulty":"Hard"},
            {"question":"∫₀¹ x² dx =","options":["1/3","1/2","1","1/4"],"answer":"1/3","difficulty":"Medium"},
            {"question":"Substitution for ∫ f(g(x))g'(x)dx is:","options":["Let u=g(x)","Let u=f(x)","Let u=x","No substitution"],"answer":"Let u=g(x)","difficulty":"Medium"},
            {"question":"∫ 2x/(x²+1) dx =","options":["ln(x²+1)+C","2ln x+C","x²+C","2x+C"],"answer":"ln(x²+1)+C","difficulty":"Medium"},
            {"question":"Area under curve y=f(x) from a to b is:","options":["∫ₐᵇ f(x)dx","f(b)-f(a)","f'(x)","(b-a)f(a)"],"answer":"∫ₐᵇ f(x)dx","difficulty":"Easy"},
            {"question":"∫ tan x dx =","options":["ln|sec x|+C","-ln|cos x|+C","Both A and B","sec x+C"],"answer":"Both A and B","difficulty":"Hard"},
            {"question":"∫₀^π sin²x dx =","options":["π/2","π","0","1"],"answer":"π/2","difficulty":"Hard"},
            {"question":"∫ (ax+b)ⁿ dx =","options":["(ax+b)ⁿ⁺¹/[a(n+1)]+C","(ax+b)ⁿ⁺¹/(n+1)+C","a(ax+b)ⁿ⁺¹+C","(ax+b)ⁿ/a+C"],"answer":"(ax+b)ⁿ⁺¹/[a(n+1)]+C","difficulty":"Hard"},
        ],
    }
    key = (subject, chapter)
    return banks.get(key, [])

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("LearnUP — Generating sample data...")
    for subject, chapters in VIDEOS.items():
        for chapter, links in chapters.items():
            path = os.path.join(BASE, "data","resources", subject, f"{chapter}.txt")
            write_file(path, "\n".join(links))
            print(f"  Videos: {subject}/{chapter}")

    for subject, chapters in QUESTIONS.items():
        for chapter, text in chapters.items():
            path = os.path.join(BASE, "data","questions","sample", subject, f"{chapter}.txt")
            write_file(path, text)
            print(f"  Questions: {subject}/{chapter}")

    for subject, chapters in VIDEOS.items():
        for chapter in chapters:
            qs = make_quiz(subject, chapter)
            if qs:
                path = os.path.join(BASE, "data","quizzes", subject, f"{chapter}.json")
                write_file(path, json.dumps(qs, indent=2, ensure_ascii=False))
                print(f"  Quiz ({len(qs)} Qs): {subject}/{chapter}")

    # init empty json files
    for fname in ["scores.json","bookmarks.json"]:
        p = os.path.join(BASE,"data",fname)
        if not os.path.exists(p):
            write_file(p, "[]")

    print("\n✅ All sample data generated successfully!")

if __name__ == "__main__":
    main()
