import pytest
from ada_tax_prep.income_tax import (
    calculate_tax_2020, calculate_deducted_income_2020, calculate_tax_liability_2020,
    TaxPayer
)

def test_no_income():
    income = 0

    taxes = calculate_tax_2020(income)

    assert taxes == 0

def test_max_bracket_one():
    income = 9875

    taxes = calculate_tax_2020(income)

    assert taxes == 988

def test_min_bracket_two():
    income = 9876

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 0

def test_max_bracket_two():
    income = 40125

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630

def test_min_bracket_three():
    income = 40126

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 0

def test_max_bracket_three():
    income = 85525

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988

def test_min_bracket_four():
    income = 85526

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 0

def test_max_bracket_four():
    income = 163300

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666


def test_min_bracket_five():
    income = 163301

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 0

def test_max_bracket_five():
    income = 207350

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 14096

def test_min_bracket_six():
    income = 207351

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 14096 + 0

def test_max_bracket_six():
    income = 518400

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 14096 + 108868

def test_min_bracket_last():
    income = 518401

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 14096 + 108868 + 0

def test_big_bracket_last():
    income = 1000000

    taxes = calculate_tax_2020(income)

    assert taxes == 988 + 3630 + 9988 + 18666 + 14096 + 108868 + 178192

@pytest.fixture
def all_valid_deductions():
    return {
        "charity": 5000,
        "mortgage": 5000,
        "child": 5000,
        "tuition": 5000,
        "healthcare": 5000
    }    

@pytest.fixture
def some_invalid_deductions():
    return {
        "charity": 5000,
        "mortgage": 5000,
        "child": 5000,
        "invalid": 5000,
        "not_allowed": 5000
    }    

@pytest.fixture
def few_valid_deductions():
    return {
        "charity": 5000,
        "mortgage": 5000,
        "child": 5000
    }    

def test_deducted_income_cannot_fall_below_zero():
    income = 10000

    deducted_income = calculate_deducted_income_2020(income, {})

    assert deducted_income == 0

def test_applies_standard_deduction():
    income = 50000

    deducted_income = calculate_deducted_income_2020(income, {})

    assert deducted_income == 37600

def test_applies_itemized_deductions(all_valid_deductions):
    income = 50000

    deducted_income = calculate_deducted_income_2020(income, all_valid_deductions)

    assert deducted_income == 25000

def test_ignores_invalid_itemized_deductions(some_invalid_deductions):
    income = 50000

    deducted_income = calculate_deducted_income_2020(income, some_invalid_deductions)

    assert deducted_income == 35000

def test_calculate_adjusted_income_tax_burden(all_valid_deductions):
    income = 50000

    adjusted_income_tax = calculate_tax_liability_2020(income, all_valid_deductions)

    assert adjusted_income_tax == 988 + 1815

def test_taxpayer_receiving_a_return_gets_a_return(all_valid_deductions):
    taxpayer = TaxPayer(withholdings=3000, income=50000, deductions=all_valid_deductions)

    refund = taxpayer.calculate_return_2020()

    assert refund == 197

def test_taxpayer_owing_tax_has_negative_return(few_valid_deductions):
    taxpayer = TaxPayer(withholdings=3000, income=50000, deductions=few_valid_deductions)

    refund = taxpayer.calculate_return_2020()

    assert refund == -1003