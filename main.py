#!/usr/bin/env python3
"""Простое CLI-приложение для отслеживания личных финансов по мотивам игры
"Денежный поток".
"""

from financial_statement import FinancialStatement


def print_menu():
    print("\nВыберите действие:")
    print("1. Добавить доход")
    print("2. Редактировать доход")
    print("3. Удалить доход")
    print("4. Добавить расход")
    print("5. Редактировать расход")
    print("6. Удалить расход")
    print("7. Установить количество детей")
    print("8. Показать отчёт")
    print("9. Выход")


def main():
    fs = FinancialStatement()
    while True:
        print_menu()
        choice = input("Введите номер: ").strip()
        if choice == "1":
            name = input("Название дохода: ")
            amount = int(input("Сумма: "))
            fs.add_income(name, amount)
        elif choice == "2":
            name = input("Название дохода: ")
            amount = int(input("Новая сумма: "))
            fs.edit_income(name, amount)
        elif choice == "3":
            name = input("Название дохода: ")
            fs.remove_income(name)
        elif choice == "4":
            name = input("Название расхода: ")
            amount = int(input("Сумма: "))
            fs.add_expense(name, amount)
        elif choice == "5":
            name = input("Название расхода: ")
            amount = int(input("Новая сумма: "))
            fs.edit_expense(name, amount)
        elif choice == "6":
            name = input("Название расхода: ")
            fs.remove_expense(name)
        elif choice == "7":
            number = int(input("Количество детей: "))
            fs.set_children(number)
        elif choice == "8":
            print("\nДоходы:")
            for k, v in fs.incomes.items():
                print(f"  {k}: {v}")
            print("\nРасходы:")
            for k, v in fs.expenses.items():
                print(f"  {k}: {v}")
            print(f"\nЧистый денежный поток: {fs.cash_flow()}")
        elif choice == "9":
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
