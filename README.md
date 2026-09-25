# Banking System – Mini Project

A simple, menu-driven **Banking System** built in pure Python. This console
application simulates the core operations of a bank: creating accounts,
logging in securely, managing balances, transferring money between accounts,
and tracking transaction history.

This project was built to combine fundamental Python concepts into one
real-world, functional application.

## 🔗 Live Demo
[Try it here](https://banking-system-mini-project-78dfyrkjzqdqxzviezpjj6.streamlit.app/)

---

## Project Overview

The Banking System allows a user to:
- Create a new bank account with their name, phone number, and a PIN
- Log in securely using their account number and PIN
- Perform everyday banking operations (deposit, withdraw, transfer, etc.)
- View a full history of their transactions
- Change their PIN
- Log out and return to the main menu

All data is stored in memory (Python dictionaries and lists) for the
duration of the program run — no external database is required.

---

## Features

| Feature                     | Description                                             |
|------------------------------|-----------------------------------------------------------|
| Create Account               | Enter name, phone number, and create a 4-digit PIN       |
| Login                        | Authenticate using Account Number + PIN (3 attempts)      |
| Check Balance                | View current account balance                              |
| Deposit Money                | Add funds to the account                                   |
| Withdraw Money                | Withdraw funds with sufficient-balance validation          |
| Transfer Money                | Send money to another existing account                     |
| Transaction History           | View all deposits, withdrawals, and transfers with timestamps |
| Change PIN                    | Update PIN after verifying the old one                    |
| Logout                       | End the session and return to the main menu                |

---

## Python Concepts Used

- **Variables & Data Types** – strings, floats, booleans for account data
- **Conditional Statements** – validating input, balance checks, PIN checks
- **Loops** – `while` loops for menus and input validation
- **Functions** – each banking operation is a dedicated, reusable function
- **Lists & Dictionaries** – `accounts` dictionary stores all account data;
  each account's `transactions` is a list of dictionaries
- **String Operations** – formatting, stripping, validation (`.isdigit()`,
  `.isalpha()`, f-strings)
- **Modules** – `random` and `datetime`

---

## Modules Used

- **`random`** – generates a unique 6-digit account number for every new account
- **`datetime`** – records the date and time of every transaction

Both are part of the Python Standard Library, so **no external installation
is required**.

---

## Application Flow

```text
CREATE ACCOUNT
      ↓
Account Number + PIN
      ↓
     LOGIN
      ↓
┌─────────────────────────┐
│      ACCOUNT MENU        │
├─────────────────────────┤
│ 1. Check Balance          │
│ 2. Deposit                │
│ 3. Withdraw                │
│ 4. Transfer                │
│ 5. Transaction History     │
│ 6. Change PIN              │
│ 7. Logout                  │
└─────────────────────────┘
      ↓
     LOGOUT
      ↓
   MAIN MENU
```

---

## Project Structure

```text
banking-system/
├── banking_system.py   # Complete application source code
├── README.md            # Project documentation (this file)
├── requirements.txt     # External dependencies (none required)
├── .gitignore            # Files/folders excluded from Git
└── screenshots/          # (Optional) screenshots of the app in action
```

---

## How to Run

### Requirements
- Python 3.7 or higher (no external packages needed)

### Steps

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run the application:

   ```bash
   python banking_system.py
   ```

   or, depending on your system:

   ```bash
   python3 banking_system.py
   ```

### Running in Google Colab

1. Upload `banking_system.py` to your Colab environment (or paste the code
   into a cell).
2. Run the cell/script. Since this is an interactive, input()-driven program,
   Colab will prompt you for input directly below the running cell each time
   the program asks a question.

---

## Example Usage

```
=========================================
      WELCOME TO THE BANKING SYSTEM
=========================================

===== BANKING SYSTEM - MAIN MENU =====
1. Create Account
2. Login
3. Exit
Enter your choice (1-3): 1

----- CREATE NEW ACCOUNT -----
Enter your full name: John Doe
Enter your 10-digit phone number: 9876543210
Create a 4-digit PIN: 1234
Confirm your 4-digit PIN: 1234

Account created successfully!
Your Account Number is: 700348
Please save this account number. You will need it to log in.

===== BANKING SYSTEM - MAIN MENU =====
1. Create Account
2. Login
3. Exit
Enter your choice (1-3): 2

----- LOGIN -----
Enter Account Number: 700348
Enter PIN: 1234

Welcome, John Doe!

===== ACCOUNT MENU =====
Logged in as: John Doe (A/C: 700348)
1. Check Balance
2. Deposit
3. Withdraw
4. Transfer
5. Transaction History
6. Change PIN
7. Logout
Enter your choice (1-7): 2

----- DEPOSIT MONEY -----
Enter amount to deposit: 1000
Deposit successful! New balance: 1000.00
```
<img width="1787" height="857" alt="image" src="https://github.com/user-attachments/assets/e5a966ba-9010-428b-bf77-df264d38d2ba" />
<img width="1817" height="652" alt="image" src="https://github.com/user-attachments/assets/97300c6b-7b55-41ad-beac-0fdbca118288" />
<img width="1801" height="430" alt="image" src="https://github.com/user-attachments/assets/f74c4bdd-0ae0-471e-9272-c58d9b092e9a" />




---

## Validation & Error Handling

The application validates user input at every step and never crashes on bad
input:

- **Name** – must contain letters only (no numbers/symbols)
- **Phone number** – must be exactly 10 digits
- **PIN** – must be exactly 4 digits, and confirmation must match
- **Account number (login/transfer)** – checked against existing accounts
- **Login PIN** – limited to 3 attempts before returning to the main menu
- **Amounts (deposit/withdraw/transfer)** – must be a valid positive number;
  non-numeric or negative/zero input is rejected and re-prompted
- **Withdrawals/Transfers** – blocked if the balance is insufficient
- **Self-transfer** – blocked (you cannot transfer money to your own account)
- **Menu choices** – invalid options display an error and re-show the menu

> **Note:** This is an educational project built to practice core Python
> concepts. It is **not** intended to represent production-grade banking
> security (for example, PINs are stored in plain text in memory for
> simplicity).

---

## Future Improvements

- Persist accounts to a file or database so data survives between runs
- Hash/encrypt PINs instead of storing them in plain text
- Add account statements exportable to a file (CSV/PDF)
- Add interest calculation for savings accounts
- Add an admin view to see all accounts (for demo/testing purposes)
- Build a simple GUI (Tkinter) or web interface on top of the same logic

---

##  Author

Built as part of a Python mini-project assignment on core programming
concepts (variables, conditionals, loops, functions, lists, dictionaries,
strings, and modules).
