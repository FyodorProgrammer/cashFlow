from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FinancialStatement:
    CHILD_EXPENSE: int = 100
    incomes: Dict[str, int] = field(default_factory=dict)
    expenses: Dict[str, int] = field(default_factory=lambda: {'Расходы на детей': 0})
    assets: Dict[str, int] = field(default_factory=dict)
    liabilities: Dict[str, int] = field(default_factory=dict)
    children: int = 0

    def add_income(self, name: str, amount: int) -> None:
        self.incomes[name] = amount

    def edit_income(self, name: str, amount: int) -> None:
        if name in self.incomes:
            self.incomes[name] = amount

    def remove_income(self, name: str) -> None:
        self.incomes.pop(name, None)

    def add_expense(self, name: str, amount: int) -> None:
        self.expenses[name] = amount

    def edit_expense(self, name: str, amount: int) -> None:
        if name in self.expenses:
            self.expenses[name] = amount

    def remove_expense(self, name: str) -> None:
        self.expenses.pop(name, None)

    def set_children(self, number: int) -> None:
        self.children = number
        self.expenses['Расходы на детей'] = self.CHILD_EXPENSE * number

    def cash_flow(self) -> int:
        return sum(self.incomes.values()) - sum(self.expenses.values())
