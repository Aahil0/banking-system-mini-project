"""
Banking System - Mini Project
------------------------------
A simple, menu-driven console banking application built with core Python.

Python concepts demonstrated:
    - Variables & Data Types
    - Conditional Statements
    - Loops
    - Functions
    - Lists & Dictionaries
    - String Operations
    - Modules (random, datetime)

Run with:  python banking_system.py
"""

import random
from datetime import datetime

# ---------------------------------------------------------------------------
# Data Storage
# ---------------------------------------------------------------------------
# All accounts are stored in a dictionary, keyed by account number (string).
# Each account is itself a dictionary holding the account's details and a
# list of transaction records.
#
# accounts = {
#     "100234": {
#         "name": "John Doe",
#         "phone": "9876543210",
#         "pin": "1234",
#         "balance": 5000,
#         "transactions": [
#             {"type": "Deposit", "amount": 5000, "time": "2026-09-25 10:00:00"}
#         ]
#     },
#     ...
# }
accounts = {}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def generate_account_number():
    """Generate a unique 6-digit account number using the random module."""
    while True:
        acc_number = str(random.randint(100000, 999999))
        if acc_number not in accounts:
            return acc_number


def get_current_time():
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def record_transaction(acc_number, txn_type, amount, extra_info=""):
    """Add a transaction record to an account's transaction history."""
    transaction = {
        "type": txn_type,
        "amount": amount,
        "time": get_current_time(),
        "info": extra_info
    }
    accounts[acc_number]["transactions"].append(transaction)


def get_valid_amount(prompt):
    """Ask the user for a positive numeric amount, re-prompting on bad input."""
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")


def get_valid_pin(prompt):
    """Ask the user for a 4-digit numeric PIN, re-prompting on bad input."""
    while True:
        pin = input(prompt).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("PIN must be exactly 4 digits. Please try again.")


def press_enter_to_continue():
    input("\nPress Enter to continue...")


# ---------------------------------------------------------------------------
# Core Banking Features
# ---------------------------------------------------------------------------
def create_account():
    """Create a new bank account: collects name, phone number and PIN."""
    print("\n----- CREATE NEW ACCOUNT -----")

    name = input("Enter your full name: ").strip()
    while name == "" or not all(part.isalpha() for part in name.split()):
        print("Please enter a valid name (letters only).")
        name = input("Enter your full name: ").strip()

    phone = input("Enter your 10-digit phone number: ").strip()
    while not (phone.isdigit() and len(phone) == 10):
        print("Invalid phone number. It must be exactly 10 digits.")
        phone = input("Enter your 10-digit phone number: ").strip()

    pin = get_valid_pin("Create a 4-digit PIN: ")
    confirm_pin = get_valid_pin("Confirm your 4-digit PIN: ")

    while pin != confirm_pin:
        print("PINs do not match. Please try again.")
        pin = get_valid_pin("Create a 4-digit PIN: ")
        confirm_pin = get_valid_pin("Confirm your 4-digit PIN: ")

    acc_number = generate_account_number()

    accounts[acc_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    print("\nAccount created successfully!")
    print(f"Your Account Number is: {acc_number}")
    print("Please save this account number. You will need it to log in.")
    press_enter_to_continue()


def login():
    """Log a user in using account number and PIN. Returns the account number
    on success, or None on failure/cancel."""
    print("\n----- LOGIN -----")

    if not accounts:
        print("No accounts exist yet. Please create an account first.")
        press_enter_to_continue()
        return None

    acc_number = input("Enter Account Number: ").strip()
    if acc_number not in accounts:
        print("Account number not found.")
        press_enter_to_continue()
        return None

    attempts = 3
    while attempts > 0:
        pin = input("Enter PIN: ").strip()
        if pin == accounts[acc_number]["pin"]:
            print(f"\nWelcome, {accounts[acc_number]['name']}!")
            press_enter_to_continue()
            return acc_number
        else:
            attempts -= 1
            print(f"Incorrect PIN. Attempts remaining: {attempts}")

    print("Too many failed attempts. Returning to main menu.")
    press_enter_to_continue()
    return None


def check_balance(acc_number):
    print("\n----- ACCOUNT BALANCE -----")
    account = accounts[acc_number]
    print(f"Account Holder : {account['name']}")
    print(f"Account Number : {acc_number}")
    print(f"Current Balance: {account['balance']:.2f}")
    press_enter_to_continue()


def deposit_money(acc_number):
    print("\n----- DEPOSIT MONEY -----")
    amount = get_valid_amount("Enter amount to deposit: ")

    accounts[acc_number]["balance"] += amount
    record_transaction(acc_number, "Deposit", amount)

    print(f"Deposit successful! New balance: {accounts[acc_number]['balance']:.2f}")
    press_enter_to_continue()


def withdraw_money(acc_number):
    print("\n----- WITHDRAW MONEY -----")
    amount = get_valid_amount("Enter amount to withdraw: ")

    if amount > accounts[acc_number]["balance"]:
        print("Insufficient balance for this withdrawal.")
        press_enter_to_continue()
        return

    accounts[acc_number]["balance"] -= amount
    record_transaction(acc_number, "Withdrawal", amount)

    print(f"Withdrawal successful! New balance: {accounts[acc_number]['balance']:.2f}")
    press_enter_to_continue()


def transfer_money(acc_number):
    print("\n----- TRANSFER MONEY -----")
    receiver_acc = input("Enter receiver's account number: ").strip()

    if receiver_acc == acc_number:
        print("You cannot transfer money to your own account.")
        press_enter_to_continue()
        return

    if receiver_acc not in accounts:
        print("Receiver account not found.")
        press_enter_to_continue()
        return

    amount = get_valid_amount("Enter amount to transfer: ")

    if amount > accounts[acc_number]["balance"]:
        print("Insufficient balance for this transfer.")
        press_enter_to_continue()
        return

    # Deduct from sender
    accounts[acc_number]["balance"] -= amount
    record_transaction(acc_number, "Transfer Sent", amount, f"To A/C {receiver_acc}")

    # Add to receiver
    accounts[receiver_acc]["balance"] += amount
    record_transaction(receiver_acc, "Transfer Received", amount, f"From A/C {acc_number}")

    print(f"Transfer successful! New balance: {accounts[acc_number]['balance']:.2f}")
    press_enter_to_continue()


def view_transaction_history(acc_number):
    print("\n----- TRANSACTION HISTORY -----")
    transactions = accounts[acc_number]["transactions"]

    if not transactions:
        print("No transactions yet.")
    else:
        for index, txn in enumerate(transactions, start=1):
            info = f" ({txn['info']})" if txn["info"] else ""
            print(f"{index}. [{txn['time']}] {txn['type']:<18} "
                  f"Amount: {txn['amount']:.2f}{info}")

    press_enter_to_continue()


def change_pin(acc_number):
    print("\n----- CHANGE PIN -----")
    old_pin = input("Enter current PIN: ").strip()

    if old_pin != accounts[acc_number]["pin"]:
        print("Incorrect current PIN.")
        press_enter_to_continue()
        return

    new_pin = get_valid_pin("Enter new 4-digit PIN: ")
    confirm_pin = get_valid_pin("Confirm new 4-digit PIN: ")

    if new_pin != confirm_pin:
        print("New PINs do not match. PIN change cancelled.")
        press_enter_to_continue()
        return

    accounts[acc_number]["pin"] = new_pin
    print("PIN changed successfully!")
    press_enter_to_continue()


# ---------------------------------------------------------------------------
# Menus
# ---------------------------------------------------------------------------
def account_menu(acc_number):
    """Menu shown after a successful login."""
    while True:
        print("\n===== ACCOUNT MENU =====")
        print(f"Logged in as: {accounts[acc_number]['name']} (A/C: {acc_number})")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance(acc_number)
        elif choice == "2":
            deposit_money(acc_number)
        elif choice == "3":
            withdraw_money(acc_number)
        elif choice == "4":
            transfer_money(acc_number)
        elif choice == "5":
            view_transaction_history(acc_number)
        elif choice == "6":
            change_pin(acc_number)
        elif choice == "7":
            print("Logging out...")
            press_enter_to_continue()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


def main_menu():
    """Top-level menu of the application."""
    while True:
        print("\n===== BANKING SYSTEM - MAIN MENU =====")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            acc_number = login()
            if acc_number:
                account_menu(acc_number)
        elif choice == "3":
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=========================================")
    print("      WELCOME TO THE BANKING SYSTEM       ")
    print("=========================================")
    main_menu()
