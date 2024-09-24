# 2024-09 Kai-Michael Kammer
"""
Utility functions for handling chemical data parsing and calculations,
such as molecular mass computation.
Includes functions for parsing molecular formulas and converting isotope notation.
"""
import re

from molmass import Formula


def convert_isotope_notation(molecular_formula: str) -> str:
    """
    Converts C18[2]H14 to C18[2H14] which can then be parsed by the molmass package
    """
    # This regex pattern captures elements with isotope notation, such as [13]C3 or [15]N3
    pattern = re.compile(r"(\[([0-9]+)\])([A-Z][a-z]*)(\d*)")

    # The replacer will adjust the position of the isotope and its related element
    def replacer(match) -> str:
        element = match.group(3)  # Element symbol (e.g., 'C', 'H', 'N')
        count = match.group(4)  # Element count (optional, like '3' in 'C3')
        isotope = match.group(2)  # Isotope number (e.g., '13' or '15')

        # Place the isotope number followed by the element and its count
        if count:
            return f"[{isotope}{element}{count}]"
        else:
            return f"[{isotope}{element}]"

    # Apply the transformation to the entire formula string
    return pattern.sub(replacer, molecular_formula)


def get_monoisotopic_mass(molecular_formula: str) -> float:
    """
    Compute the mono-isotopic mass and molecular formula using molmass.
    The molecular formula should be in the format C10[2H]6H4O3Cl1 or C10[2H6]H4O3Cl1.
    The format C10[2]H6H4O3Cl1 is automatically converted
    """
    try:
        # Convert the formula for isotopic elements
        formatted_formula = convert_isotope_notation(molecular_formula)

        # Create a Formula object using molmass
        formula = Formula(formatted_formula)

        # Get the mono-isotopic mass
        monoisotopic_mass = formula.isotope.mass

        # Get the molecular formula in canonical form
        # canonical_formula = formula.formula
        return monoisotopic_mass
    except Exception as e:
        raise ValueError(
            f"Error computing molecular mass for {molecular_formula}/{formatted_formula}: {e}"
        )


def get_measured_formula(molecular_formula: str, adduct_name: str) -> str:
    """
    Compute the measured molecular formula by adding the adduct.
    The molecular formula should be in the format C10[2H]6H4O3Cl1 or C10[2H6]H4O3Cl1.
    """
    # Define the regular expression pattern to match adducts like M+Na, M-H, M+H, etc.
    pattern_adduct = r"M([+-])([A-Z][a-z]?)"
    valid_adducts = ("Na", "H")

    match_adduct = re.match(pattern_adduct, adduct_name)
    if match_adduct:
        adduct_operation = match_adduct.group(1)  # '+' or '-'
        adduct_element = match_adduct.group(2)  # e.g., 'Na', 'H'
        if adduct_element not in valid_adducts:
            raise ValueError(f"Invalid adduct element: {adduct_element}")
        try:
            formatted_formula = convert_isotope_notation(molecular_formula)
            # Use Molmass to parse the molecular formula
            mm_formula = Formula(formatted_formula)
            mm_adduct = Formula(adduct_element)
            # Modify the formula based on the operation
            if adduct_operation == "+":
                mm_formula += mm_adduct
            elif adduct_operation == "-":
                mm_formula -= mm_adduct
            else:
                raise ValueError(
                    "Invalid operation. Use '+' to add or '-' to remove an atom."
                )

            # Return the updated molecular formula
            return str(mm_formula.formula)
        except Exception as e:
            raise ValueError(
                f"Error performing {adduct_operation} operation on {adduct_element}: {e}"
            )
    else:
        raise ValueError(f"Invalid adduct name: {adduct_name}")
