from sympy import Matrix,lcm
from math import gcd
from functools import reduce
import re

VALID_ELEMENTS = {
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
}

def parse_formula(formula):
    pattern = r"([A-Z][a-z]?)(\d*)"

    matches = re.findall(pattern, formula)

    if not matches:
        raise ValueError("Invalid chemical formula")

    # Check that the entire formula was recognized
    if "".join(element + count for element, count in matches) != formula:
        raise ValueError("Invalid chemical formula")

    atom_counts = {}

    for element, count in matches:

        if element not in VALID_ELEMENTS:
            raise ValueError(f"Unknown chemical element: {element}")

        number = int(count) if count else 1

        if number <= 0:
            raise ValueError("Atom count must be positive")

        atom_counts[element] = atom_counts.get(element, 0) + number
   
    return atom_counts

def balance_equation():
    print("Reaction Balancer")
    print("-----------------")
    equation=input("Enter chemical equation:")
    print("You entered:",equation)

def split_equation(equation):
    if equation.count("->") != 1:
        raise ValueError("Equation must contain exactly one ->")

    left, right = equation.split("->")

    reactants = left.split("+")
    products = right.split("+")

    reactants = [item.strip() for item in reactants]
    products = [item.strip() for item in products]

    if not all(reactants) or not all(products):
        raise ValueError("Missing chemical formula")

    return reactants, products


def build_matrix(reactants, products):
    formulas = reactants + products

    # Find every unique element
    elements = set()

    for formula in formulas:
        atom_counts = parse_formula(formula)
        elements.update(atom_counts.keys())

    elements = sorted(elements)

    # Create one row for each element
    matrix_data = []

    for element in elements:
        row = []

        for formula in reactants:
            counts = parse_formula(formula)
            row.append(counts.get(element, 0))

        for formula in products:
            counts = parse_formula(formula)
            row.append(-counts.get(element, 0))

        matrix_data.append(row)

    return Matrix(matrix_data), elements

def calculate_coefficients(matrix):
    solutions = matrix.nullspace()

    if not solutions:
        raise ValueError("This equation cannot be balanced")

    solution = solutions[0]

    # Find a common denominator
    denominator = 1

    for value in solution:
        denominator = lcm(denominator, int(value.q))

    # Convert fractions into integers
    coefficients = [
        int(value * denominator)
        for value in solution
    ]

    # Make all coefficients positive
    if all(value < 0 for value in coefficients):
        coefficients = [-value for value in coefficients]

    if any(value <= 0 for value in coefficients):
        raise ValueError("Invalid balancing coefficients")

    # Simplify to the smallest whole-number ratio
    common_divisor = reduce(gcd, coefficients)

    coefficients = [
        value // common_divisor
        for value in coefficients
    ]

    return coefficients

def format_equation(reactants, products, coefficients):
    all_formulas = reactants + products

    formatted = []

    for formula, coefficient in zip(all_formulas, coefficients):
        if coefficient == 1:
            formatted.append(formula)
        else:
            formatted.append(f"{coefficient}{formula}")

    left_side = " + ".join(formatted[:len(reactants)])
    right_side = " + ".join(formatted[len(reactants):])

    return f"{left_side} -> {right_side}"

def balance_reaction(equation):
    reactants, products = split_equation(equation)

    matrix, elements = build_matrix(reactants, products)

    coefficients = calculate_coefficients(matrix)

    balanced = format_equation(
        reactants,
        products,
        coefficients
    )

    return balanced

if __name__== "__main__":
    equation=input("Enter chemical equation:")
    try:
        result=balance_reaction(equation)
        print("Balanced equation:",result)
    except ValueError as error:
        print("Error:",error)

# reactants,products = split_equation ("H2 +O2 -> H2O")
# matrix,elements=build_matrix(reactants,products)
# coefficients=calculate_coefficients(matrix)
# balanced=format_equation(reactants,products,coefficients)
# print("Reactants:" ,reactants)
# print("Products:",products)
# print(matrix)
# print("Calculated coefficients:",coefficients)
# print("Balanced equation:",balanced)