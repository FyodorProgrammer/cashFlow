"""
Графический интерфейс для приложения «Денежный поток».

Основой интерфейса является форма, повторяющая бланк из игры
«Денежный поток». Пользователь может вводить свои доходы, расходы,
активы и обязательства. Итоговые значения (общий доход, пассивный
доход, общие расходы, денежный поток, чистые активы) рассчитываются
автоматически при изменении любой из граф.

Библиотека Tkinter поставляется в стандартной поставке Python, что
позволяет запускать приложение без дополнительных зависимостей. Для
модульных тестов логика расчётов вынесена в ``cashflow_app.models``.

Запустить приложение можно командой::

    python -m cashflow_app.app

"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .models import FinancialStatement


# Определяем категории и их русские названия. Эти словари используются
# для генерации элементов интерфейса и привязки данных к модели.
INCOME_CATEGORIES = {
    'salary': 'Зарплата',
    'interest_dividends': 'Проценты/Дивиденды',
    'real_estate_income': 'Доход от недвижимости',
    'business_income': 'Доход от бизнеса',
    'other_passive_income': 'Другие пассивные доходы',
}

EXPENSE_CATEGORIES = {
    'taxes': 'Налоги',
    'mortgage': 'Ипотека/Аренда',
    'school_loan_payment': 'Студенческий кредит (платёж)',
    'car_payment': 'Автокредит (платёж)',
    'credit_card_payment': 'Кредитная карта (платёж)',
    'retail_payment': 'Розничный кредит (платёж)',
    'per_child_expense': 'Расходы на ребёнка',
    'other_expenses': 'Другие расходы',
    'bank_loan_payment': 'Банковский кредит (платёж)',
}

ASSET_CATEGORIES = {
    'savings': 'Сбережения',
    'real_estate': 'Недвижимость',
    'stocks': 'Акции/Фонды',
    'business': 'Бизнес',
    'gold': 'Золото/Драгоценные металлы',
    'other_assets': 'Прочие активы',
}

LIABILITY_CATEGORIES = {
    'mortgage': 'Ипотека/Кредит на жильё',
    'school_loan': 'Студенческий кредит',
    'car_loan': 'Автомобильный кредит',
    'credit_card': 'Долг по кредитной карте',
    'retail_debt': 'Розничный долг',
    'bank_loan': 'Банковский кредит',
    'other_liabilities': 'Прочие обязательства',
}


class CashflowApp(tk.Tk):
    """Основное окно приложения.

    Наследуется от ``tk.Tk``. Здесь создаются все элементы формы,
    привязываются переменные и задаются правила обновления расчётов.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Денежный поток – личный финансовый отчёт")
        self.resizable(False, False)

        # Модель финансового отчёта, на основе которой выполняются расчёты
        self.statement = FinancialStatement()

        # Словари для хранения переменных Tkinter
        self.vars_income: dict[str, tk.StringVar] = {}
        self.vars_expenses: dict[str, tk.StringVar] = {}
        self.vars_assets: dict[str, tk.StringVar] = {}
        self.vars_liabilities: dict[str, tk.StringVar] = {}

        # Создаём интерфейс
        self._create_widgets()
        # Выполним начальный расчёт, чтобы установить начальные значения
        self.update_summary()

    def _create_widgets(self) -> None:
        """Создание и размещение всех виджетов GUI."""
        # Используем ttk для более современного внешнего вида
        # Разделим форму на две секции: верхняя – отчёт о доходах/расходах,
        # нижняя – баланс (активы/обязательства)
        income_frame = ttk.LabelFrame(self, text="Доходы и Расходы")
        income_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Подразделы
        income_subframe = ttk.LabelFrame(income_frame, text="Доходы")
        expense_subframe = ttk.LabelFrame(income_frame, text="Расходы")
        income_subframe.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        expense_subframe.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Заполняем доходы
        for i, (key, label) in enumerate(INCOME_CATEGORIES.items()):
            ttk.Label(income_subframe, text=label + ":").grid(row=i, column=0, sticky="w", padx=2, pady=2)
            var = tk.StringVar(value="0")
            # Создаём callback, который будет обновлять модель при изменении значения
            var.trace_add('write', lambda *args, key=key, var=var: self.on_income_change(key, var))
            entry = ttk.Entry(income_subframe, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.vars_income[key] = var

        # Заполняем расходы
        for i, (key, label) in enumerate(EXPENSE_CATEGORIES.items()):
            ttk.Label(expense_subframe, text=label + ":").grid(row=i, column=0, sticky="w", padx=2, pady=2)
            var = tk.StringVar(value="0")
            var.trace_add('write', lambda *args, key=key, var=var: self.on_expense_change(key, var))
            entry = ttk.Entry(expense_subframe, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.vars_expenses[key] = var

        # Итоговые значения для отчёта о доходах/расходах
        summary_frame = ttk.Frame(income_frame)
        summary_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
        ttk.Label(summary_frame, text="Общий доход:").grid(row=0, column=0, sticky="w", padx=2)
        self.label_total_income = ttk.Label(summary_frame, text="0")
        self.label_total_income.grid(row=0, column=1, sticky="e", padx=2)

        ttk.Label(summary_frame, text="Пассивный доход:").grid(row=1, column=0, sticky="w", padx=2)
        self.label_passive_income = ttk.Label(summary_frame, text="0")
        self.label_passive_income.grid(row=1, column=1, sticky="e", padx=2)

        ttk.Label(summary_frame, text="Общие расходы:").grid(row=2, column=0, sticky="w", padx=2)
        self.label_total_expenses = ttk.Label(summary_frame, text="0")
        self.label_total_expenses.grid(row=2, column=1, sticky="e", padx=2)

        ttk.Label(summary_frame, text="Денежный поток (остаток):").grid(row=3, column=0, sticky="w", padx=2)
        self.label_cash_flow = ttk.Label(summary_frame, text="0")
        self.label_cash_flow.grid(row=3, column=1, sticky="e", padx=2)

        # Теперь создаём секцию для активов/обязательств
        balance_frame = ttk.LabelFrame(self, text="Баланс: Активы и Обязательства")
        balance_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        asset_subframe = ttk.LabelFrame(balance_frame, text="Активы")
        liability_subframe = ttk.LabelFrame(balance_frame, text="Обязательства")
        asset_subframe.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        liability_subframe.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Заполняем активы
        for i, (key, label) in enumerate(ASSET_CATEGORIES.items()):
            ttk.Label(asset_subframe, text=label + ":").grid(row=i, column=0, sticky="w", padx=2, pady=2)
            var = tk.StringVar(value="0")
            var.trace_add('write', lambda *args, key=key, var=var: self.on_asset_change(key, var))
            entry = ttk.Entry(asset_subframe, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.vars_assets[key] = var

        # Заполняем обязательства
        for i, (key, label) in enumerate(LIABILITY_CATEGORIES.items()):
            ttk.Label(liability_subframe, text=label + ":").grid(row=i, column=0, sticky="w", padx=2, pady=2)
            var = tk.StringVar(value="0")
            var.trace_add('write', lambda *args, key=key, var=var: self.on_liability_change(key, var))
            entry = ttk.Entry(liability_subframe, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=2, pady=2)
            self.vars_liabilities[key] = var

        # Итоговые значения баланса
        balance_summary_frame = ttk.Frame(balance_frame)
        balance_summary_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="nsew")
        ttk.Label(balance_summary_frame, text="Всего активов:").grid(row=0, column=0, sticky="w", padx=2)
        self.label_total_assets = ttk.Label(balance_summary_frame, text="0")
        self.label_total_assets.grid(row=0, column=1, sticky="e", padx=2)
        ttk.Label(balance_summary_frame, text="Всего обязательств:").grid(row=1, column=0, sticky="w", padx=2)
        self.label_total_liabilities = ttk.Label(balance_summary_frame, text="0")
        self.label_total_liabilities.grid(row=1, column=1, sticky="e", padx=2)
        ttk.Label(balance_summary_frame, text="Чистые активы:").grid(row=2, column=0, sticky="w", padx=2)
        self.label_net_worth = ttk.Label(balance_summary_frame, text="0")
        self.label_net_worth.grid(row=2, column=1, sticky="e", padx=2)

    def _parse_value(self, value: str) -> float:
        """Преобразовать строковое значение в float.

        Пустые строки и некорректные данные интерпретируются как 0.
        """
        try:
            # Заменяем запятую на точку для поддержки российской нотации
            cleaned = value.replace(',', '.') if value else '0'
            return float(cleaned)
        except ValueError:
            return 0.0

    def on_income_change(self, key: str, var: tk.StringVar) -> None:
        """Callback вызывается при изменении поля дохода."""
        value = self._parse_value(var.get())
        self.statement.update_income(key, value)
        self.update_summary()

    def on_expense_change(self, key: str, var: tk.StringVar) -> None:
        """Callback вызывается при изменении поля расхода."""
        value = self._parse_value(var.get())
        self.statement.update_expense(key, value)
        self.update_summary()

    def on_asset_change(self, key: str, var: tk.StringVar) -> None:
        """Callback вызывается при изменении поля актива."""
        value = self._parse_value(var.get())
        self.statement.update_asset(key, value)
        self.update_summary()

    def on_liability_change(self, key: str, var: tk.StringVar) -> None:
        """Callback вызывается при изменении поля обязательства."""
        value = self._parse_value(var.get())
        self.statement.update_liability(key, value)
        self.update_summary()

    def update_summary(self) -> None:
        """Обновить текстовые поля итоговых значений на основе модели."""
        # Форматируем числа с двумя десятичными знаками и разделением по пробелу
        def fmt(number: float) -> str:
            return f"{number:,.2f}".replace(',', ' ').replace('.', ',')

        self.label_total_income.config(text=fmt(self.statement.total_income))
        self.label_passive_income.config(text=fmt(self.statement.passive_income))
        self.label_total_expenses.config(text=fmt(self.statement.total_expenses))
        self.label_cash_flow.config(text=fmt(self.statement.cash_flow))
        self.label_total_assets.config(text=fmt(self.statement.total_assets))
        self.label_total_liabilities.config(text=fmt(self.statement.total_liabilities))
        self.label_net_worth.config(text=fmt(self.statement.net_worth))


def main() -> None:
    app = CashflowApp()
    app.mainloop()


if __name__ == '__main__':
    main()