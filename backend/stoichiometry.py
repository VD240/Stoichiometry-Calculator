from backend.balancer import parse_formula
from backend.balancer import ( split_equation,build_matrix,calculate_coefficients)

ATOMIC_MASSES = {
    "H": 1.008,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845
}
def calculate_molar_mass(formula):
    atom_counts = parse_formula(formula)

    total_mass = 0

    for element, count in atom_counts.items():

        if element not in ATOMIC_MASSES:
            raise ValueError(
                f"Atomic mass not available for {element}"
            )

        atomic_mass = ATOMIC_MASSES[element]

        total_mass += atomic_mass * count

    return round(total_mass, 3)

def calculate_moles(mass, formula):
    if mass < 0:
        raise ValueError("Mass cannot be negative")

    molar_mass = calculate_molar_mass(formula)

    moles = mass / molar_mass

    return round(moles, 3)
def find_limiting_reagent(equation, available_moles):

    reactants, products = split_equation(equation)

    matrix, elements = build_matrix(reactants, products)

    coefficients = calculate_coefficients(matrix)

    reactant_coefficients = coefficients[:len(reactants)]

    ratios = {}

    for formula, coefficient in zip(
        reactants, reactant_coefficients
    ):
        if formula not in available_moles:
            raise ValueError(f"Missing moles for {formula}")

        moles = available_moles[formula]

        if moles <= 0:
            raise ValueError("Available moles must be positive")

        ratios[formula] = moles / coefficient

    limiting_reagent = min(ratios, key=ratios.get)

    return limiting_reagent
def calculate_theoretical_yield(
    equation,
    available_moles,
    product_formula
):
    reactants, products = split_equation(equation)

    if product_formula not in products:
        raise ValueError("Product not found in equation")

    matrix, elements = build_matrix(reactants, products)

    coefficients = calculate_coefficients(matrix)

    reactant_coefficients = coefficients[:len(reactants)]

    product_coefficient = coefficients[
        len(reactants) + products.index(product_formula)
    ]

    ratios = []

    for formula, coefficient in zip(
        reactants, reactant_coefficients
    ):
        if formula not in available_moles:
            raise ValueError(f"Missing moles for {formula}")

        moles = available_moles[formula]

        if moles <= 0:
            raise ValueError("Available moles must be positive")

        ratios.append(moles / coefficient)

    reaction_amount = min(ratios)

    theoretical_moles = reaction_amount * product_coefficient

    molar_mass = calculate_molar_mass(product_formula)

    theoretical_grams = theoretical_moles * molar_mass

    return {
        "product": product_formula,
        "moles": round(theoretical_moles, 3),
        "mass_g": round(theoretical_grams, 3)
    }