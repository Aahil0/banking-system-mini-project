"""
banking_logic.py
------------------
Pure banking logic for the Streamlit Banking System app.

This module has NO Streamlit imports and NO print()/input() calls —
it only operates on a plain Python dictionary (`accounts`) that is
passed in and mutated. Keeping this separate from the UI layer makes
it easy to test and easy to reuse (e.g. in the original console app).
"""

import random
from datetime import datetime


def generate_account_number(accounts):
    """Generate a unique 6-digit account number using the random module."""
    while True:
        acc_number = str(random.randint(100000, 999999))
        if acc_number not in accounts:
            return acc_number


def get_current_time():
    """Return the current date and time as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def record_transaction(accounts, acc_number, txn_type, amount, extra_info=""):
    """Append a transaction record to an account's history."""
    accounts[acc_number]["transactions"].append({
        "type": txn_type,
        "amount": amount,
        "time": get_current_time(),
        "info": extra_info
    })


def create_account(accounts, name, phone, pin):
    """
    Validate inputs and create a new account.
    Returns the new account number.
    Raises ValueError with a user-friendly message on invalid input.
    """
    name = name.strip()
    phone = phone.strip()
    pin = pin.strip()

    if not name or not all(part.isalpha() for part in name.split()):
        raise ValueError("Please enter a valid name (letters only).")

    if not (phone.isdigit() and len(phone) == 10):
        raise ValueError("Phone number must be exactly 10 digits.")

    if not (pin.isdigit() and len(pin) == 4):
        raise ValueError("PIN must be exactly 4 digits.")

    acc_number = generate_account_number(accounts)
    accounts[acc_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }
    return acc_number


def authenticate(accounts, acc_number, pin):
    """Return True if the account number and PIN match an existing account."""
    account = accounts.get(acc_number)
    return account is not None and account["pin"] == pin


def deposit(accounts, acc_number, amount):
    """Deposit a positive amount into the account. Raises ValueError on bad amount."""
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")
    accounts[acc_number]["balance"] += amount
    record_transaction(accounts, acc_number, "Deposit", amount)


def withdraw(accounts, acc_number, amount):
    """Withdraw a positive amount if sufficient balance exists."""
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")
    if amount > accounts[acc_number]["balance"]:
        raise ValueError("Insufficient balance for this withdrawal.")
    accounts[acc_number]["balance"] -= amount
    record_transaction(accounts, acc_number, "Withdrawal", amount)


def transfer(accounts, sender_acc, receiver_acc, amount):
    """Transfer a positive amount from sender to receiver."""
    if sender_acc == receiver_acc:
        raise ValueError("You cannot transfer money to your own account.")
    if receiver_acc not in accounts:
        raise ValueError("Receiver account not found.")
    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")
    if amount > accounts[sender_acc]["balance"]:
        raise ValueError("Insufficient balance for this transfer.")

    accounts[sender_acc]["balance"] -= amount
    record_transaction(accounts, sender_acc, "Transfer Sent", amount,
                        f"To A/C {receiver_acc}")

    accounts[receiver_acc]["balance"] += amount
    record_transaction(accounts, receiver_acc, "Transfer Received", amount,
                        f"From A/C {sender_acc}")


def change_pin(accounts, acc_number, old_pin, new_pin, confirm_pin):
    """Change an account's PIN after verifying the old one."""
    if old_pin != accounts[acc_number]["pin"]:
        raise ValueError("Incorrect current PIN.")
    if not (new_pin.isdigit() and len(new_pin) == 4):
        raise ValueError("New PIN must be exactly 4 digits.")
    if new_pin != confirm_pin:
        raise ValueError("New PINs do not match.")
    accounts[acc_number]["pin"] = new_pin
