"""
Модели финансовых отчётов
=========================

В этом модуле определены классы, представляющие элементы личной
финансовой отчётности: ``IncomeStatement``, ``BalanceSheet`` и
``FinancialStatement``. Эти модели инкапсулируют данные и логику
вычислений, что позволяет отделить бизнес‑логику от пользовательского
интерфейса и облегчает тестирование.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


def _safe_sum(values: Dict[str, float]) -> float:
    """Безопасно суммировать значения словаря.

    Пустые словари возвращают 0.0. Неинициализированные (None) значения
    интерпретируются как 0.
    """
    return sum(float(v or 0) for v in values.values())


@dataclass
class IncomeStatement:
    """Представляет собой доходы и расходы за месяц.

    Атрибуты
    ---------
    incomes: Dict[str, float]
        Словарь с ключами – категориями доходов, значениями – суммами.
    expenses: Dict[str, float]
        Словарь с ключами – категориями расходов, значениями – суммами.
    passive_categories: set[str]
        Множество ключей из ``incomes``, которые считаются пассивными
        доходами.
    """

    incomes: Dict[str, float] = field(default_factory=dict)
    expenses: Dict[str, float] = field(default_factory=dict)
    passive_categories: set[str] = field(default_factory=lambda: {
        'interest_dividends',
        'real_estate_income',
        'business_income',
        'other_passive_income',
    })

    def total_income(self) -> float:
        """Вернуть сумму всех доходов."""
        return _safe_sum(self.incomes)

    def total_expenses(self) -> float:
        """Вернуть сумму всех расходов."""
        return _safe_sum(self.expenses)

    def passive_income(self) -> float:
        """Вычислить сумму пассивных доходов.

        Пассивные доходы определяются согласно множеству
        ``passive_categories``. Отсутствующие категории считаются равными нулю.
        """
        return sum(float(self.incomes.get(key, 0) or 0) for key in self.passive_categories)

    def cash_flow(self) -> float:
        """Вычислить денежный поток (разница между общими доходами и
        общими расходами)."""
        return self.total_income() - self.total_expenses()


@dataclass
class BalanceSheet:
    """Представляет собой список активов и обязательств.

    Атрибуты
    ---------
    assets: Dict[str, float]
        Категории активов (сбережения, недвижимость и т. д.).
    liabilities: Dict[str, float]
        Категории обязательств (ипотека, кредиты и т. д.).
    """

    assets: Dict[str, float] = field(default_factory=dict)
    liabilities: Dict[str, float] = field(default_factory=dict)

    def total_assets(self) -> float:
        """Вернуть сумму всех активов."""
        return _safe_sum(self.assets)

    def total_liabilities(self) -> float:
        """Вернуть сумму всех обязательств."""
        return _safe_sum(self.liabilities)

    def net_worth(self) -> float:
        """Вычислить чистые активы (разница между активами и
        обязательствами)."""
        return self.total_assets() - self.total_liabilities()


@dataclass
class FinancialStatement:
    """Комплексный финансовый отчёт.

    Содержит ``IncomeStatement`` и ``BalanceSheet`` и объединяет
    вычисления по ним. Это полезно для GUI, где требуется доступ к
    обоим типам отчётов из одного объекта.
    """

    income_statement: IncomeStatement = field(default_factory=IncomeStatement)
    balance_sheet: BalanceSheet = field(default_factory=BalanceSheet)

    def update_income(self, category: str, value: float) -> None:
        """Обновить значение дохода для указанной категории."""
        self.income_statement.incomes[category] = value

    def update_expense(self, category: str, value: float) -> None:
        """Обновить значение расхода для указанной категории."""
        self.income_statement.expenses[category] = value

    def update_asset(self, category: str, value: float) -> None:
        """Обновить значение актива для указанной категории."""
        self.balance_sheet.assets[category] = value

    def update_liability(self, category: str, value: float) -> None:
        """Обновить значение обязательства для указанной категории."""
        self.balance_sheet.liabilities[category] = value

    @property
    def total_income(self) -> float:
        return self.income_statement.total_income()

    @property
    def total_expenses(self) -> float:
        return self.income_statement.total_expenses()

    @property
    def passive_income(self) -> float:
        return self.income_statement.passive_income()

    @property
    def cash_flow(self) -> float:
        return self.income_statement.cash_flow()

    @property
    def total_assets(self) -> float:
        return self.balance_sheet.total_assets()

    @property
    def total_liabilities(self) -> float:
        return self.balance_sheet.total_liabilities()

    @property
    def net_worth(self) -> float:
        return self.balance_sheet.net_worth()