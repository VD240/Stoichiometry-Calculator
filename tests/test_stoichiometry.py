import pytest

from backend.stoichiometry import (
    calculate_molar_mass,
    find_limiting_reagent,
    calculate_theoretical_yield
)


def test_water_molar_mass():
    result = calculate_molar_mass("H2O")
    assert result == pytest.approx(18.015)


def test_carbon_dioxide_molar_mass():
    result = calculate_molar_mass("CO2")
    assert result == pytest.approx(44.009)


def test_sodium_chloride_molar_mass():
    result = calculate_molar_mass("NaCl")
    assert result == pytest.approx(58.44)


def test_limiting_reagent():
    result = find_limiting_reagent(
        "H2 + O2 -> H2O",
        {"H2": 3, "O2": 1}
    )
    assert result == "O2"

def test_theoretical_yield():
    result = calculate_theoretical_yield(
        "H2 + O2 -> H2O",
        {"H2": 3, "O2": 2},
        "H2O"
    )

    assert result["product"] == "H2O"
    assert result["moles"] == pytest.approx(3.0)
    assert result["mass_g"] == pytest.approx(54.045)