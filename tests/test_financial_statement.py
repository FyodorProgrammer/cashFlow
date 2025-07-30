import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from financial_statement import FinancialStatement


def test_add_income():
    fs = FinancialStatement()
    fs.add_income('Зарплата', 1000)
    assert fs.incomes['Зарплата'] == 1000


def test_edit_income():
    fs = FinancialStatement()
    fs.add_income('Зарплата', 1000)
    fs.edit_income('Зарплата', 1200)
    assert fs.incomes['Зарплата'] == 1200


def test_remove_income():
    fs = FinancialStatement()
    fs.add_income('Зарплата', 1000)
    fs.remove_income('Зарплата')
    assert 'Зарплата' not in fs.incomes


def test_cash_flow_calculation():
    fs = FinancialStatement()
    fs.add_income('Зарплата', 2000)
    fs.add_expense('Аренда', 500)
    fs.add_expense('Еда', 300)
    assert fs.cash_flow() == 1200


def test_children_expense():
    fs = FinancialStatement()
    fs.set_children(2)
    assert fs.expenses['Расходы на детей'] == fs.CHILD_EXPENSE * 2
