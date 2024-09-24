import pytest
from mass_spec_app.scripts.chem_utils import (convert_isotope_notation,
                                              get_measured_formula,
                                              get_monoisotopic_mass)


def test_convert_isotope_notation():
    """Test the conversion of isotope notation."""
    input_formula = "C21H25[2]H3O4"
    expected_output = "C21H25[2H3]O4"
    result = convert_isotope_notation(input_formula)
    assert result == expected_output


def test_get_monoisotopic_mass():
    """Test molecular mass computation using molmass."""
    input_formula = "C21H25[2]H3O4"
    input_mass = 347.21758961839
    mass = get_monoisotopic_mass(input_formula)
    assert isinstance(mass, float)
    assert pytest.approx(mass) == input_mass


def test_get_measured_formula():
    """Test converting the measured formula."""
    input_formula = "C21H25[2]H3O4"
    input_adduct = "M-H"
    expected_formula = "C21H24[2]H3O4"
    output_formula = get_measured_formula(
        molecular_formula=input_formula, adduct_name=input_adduct
    )
    assert expected_formula == output_formula
