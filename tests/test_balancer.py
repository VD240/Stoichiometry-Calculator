import pytest
from backend.balancer import balance_reaction


@pytest.mark.parametrize("equation, expected", [
    ("N2 + H2 -> NH3", "N2 + 3H2 -> 2NH3"),
    ("CH4 + O2 -> CO2 + H2O",
     "CH4 + 2O2 -> CO2 + 2H2O"),
    ("Fe + O2 -> Fe2O3",
     "4Fe + 3O2 -> 2Fe2O3"),
    ("KClO3 -> KCl + O2",
     "2KClO3 -> 2KCl + 3O2"),
    ("Al + HCl -> AlCl3 + H2",
     "2Al + 6HCl -> 2AlCl3 + 3H2")
])

def test_balance_reaction(equation, expected):
    result = balance_reaction(equation)
    assert result == expected