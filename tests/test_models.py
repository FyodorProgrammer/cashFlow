"""
Тесты для модулей ``cashflow_app.models``.

Эти тесты демонстрируют подход TDD. Сначала формулируются
ожидаемые вычисления, затем код в ``models.py`` реализуется таким
образом, чтобы удовлетворять этим ожиданиям. Вы можете запускать
тесты командой ``python -m unittest`` из корня проекта.
"""

import unittest

from cashflow_app.models import IncomeStatement, BalanceSheet, FinancialStatement


class TestIncomeStatement(unittest.TestCase):
    def setUp(self) -> None:
        # Создаём пример отчёта с предопределёнными значениями
        incomes = {
            'salary': 3000,
            'interest_dividends': 200,
            'real_estate_income': 500,
            'business_income': 0,
            'other_passive_income': 100,
        }
        expenses = {
            'taxes': 400,
            'mortgage': 800,
            'school_loan_payment': 100,
            'car_payment': 150,
            'credit_card_payment': 50,
            'retail_payment': 50,
            'per_child_expense': 0,
            'other_expenses': 300,
            'bank_loan_payment': 100,
        }
        self.statement = IncomeStatement(incomes=incomes, expenses=expenses)

    def test_total_income(self) -> None:
        expected = 3000 + 200 + 500 + 0 + 100
        self.assertAlmostEqual(self.statement.total_income(), expected)

    def test_total_expenses(self) -> None:
        expected = 400 + 800 + 100 + 150 + 50 + 50 + 0 + 300 + 100
        self.assertAlmostEqual(self.statement.total_expenses(), expected)

    def test_passive_income(self) -> None:
        expected = 200 + 500 + 0 + 100
        self.assertAlmostEqual(self.statement.passive_income(), expected)

    def test_cash_flow(self) -> None:
        expected_income = 3000 + 200 + 500 + 0 + 100
        expected_expenses = 400 + 800 + 100 + 150 + 50 + 50 + 0 + 300 + 100
        expected_cash_flow = expected_income - expected_expenses
        self.assertAlmostEqual(self.statement.cash_flow(), expected_cash_flow)


class TestBalanceSheet(unittest.TestCase):
    def setUp(self) -> None:
        assets = {
            'savings': 5000,
            'real_estate': 20000,
            'stocks': 5000,
            'business': 10000,
            'gold': 1000,
            'other_assets': 0,
        }
        liabilities = {
            'mortgage': 15000,
            'school_loan': 2000,
            'car_loan': 3000,
            'credit_card': 1000,
            'retail_debt': 500,
            'bank_loan': 5000,
            'other_liabilities': 0,
        }
        self.balance = BalanceSheet(assets=assets, liabilities=liabilities)

    def test_total_assets(self) -> None:
        expected = 5000 + 20000 + 5000 + 10000 + 1000 + 0
        self.assertAlmostEqual(self.balance.total_assets(), expected)

    def test_total_liabilities(self) -> None:
        expected = 15000 + 2000 + 3000 + 1000 + 500 + 5000 + 0
        self.assertAlmostEqual(self.balance.total_liabilities(), expected)

    def test_net_worth(self) -> None:
        expected_assets = 5000 + 20000 + 5000 + 10000 + 1000 + 0
        expected_liabilities = 15000 + 2000 + 3000 + 1000 + 500 + 5000 + 0
        expected_net = expected_assets - expected_liabilities
        self.assertAlmostEqual(self.balance.net_worth(), expected_net)


class TestFinancialStatement(unittest.TestCase):
    def test_update_and_totals(self) -> None:
        fs = FinancialStatement()
        # Изначально все суммы нулевые
        self.assertEqual(fs.total_income, 0)
        self.assertEqual(fs.total_expenses, 0)
        self.assertEqual(fs.cash_flow, 0)
        self.assertEqual(fs.total_assets, 0)
        self.assertEqual(fs.total_liabilities, 0)
        self.assertEqual(fs.net_worth, 0)

        # Обновляем несколько значений
        fs.update_income('salary', 4000)
        fs.update_income('interest_dividends', 150)
        fs.update_expense('taxes', 600)
        fs.update_expense('mortgage', 1000)
        fs.update_asset('savings', 10000)
        fs.update_liability('mortgage', 50000)

        self.assertAlmostEqual(fs.total_income, 4150)
        self.assertAlmostEqual(fs.total_expenses, 1600)
        self.assertAlmostEqual(fs.passive_income, 150)  # только interest_dividends
        self.assertAlmostEqual(fs.cash_flow, 4150 - 1600)
        self.assertAlmostEqual(fs.total_assets, 10000)
        self.assertAlmostEqual(fs.total_liabilities, 50000)
        self.assertAlmostEqual(fs.net_worth, 10000 - 50000)


if __name__ == '__main__':
    unittest.main()