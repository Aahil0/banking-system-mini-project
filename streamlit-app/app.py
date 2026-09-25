"""
app.py
-------
Streamlit web UI for the Banking System mini project.

This is a UI layer only — all the actual banking rules (validation,
balance checks, transfers, etc.) live in banking_logic.py.

Run with:
    streamlit run app.py

Note: Accounts are stored in Streamlit's session_state, so data is
in-memory only — it resets whenever the server restarts (this mirrors
the original console app, which also doesn't persist data to disk).
"""

import streamlit as st
import banking_logic as bl

st.set_page_config(page_title="Banking System", page_icon="🏦", layout="centered")

# ---------------------------------------------------------------------------
# Session State Setup
# ---------------------------------------------------------------------------
if "accounts" not in st.session_state:
    st.session_state.accounts = {}        # all accounts, keyed by account number

if "logged_in_acc" not in st.session_state:
    st.session_state.logged_in_acc = None  # currently logged-in account number

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0


def logout():
    st.session_state.logged_in_acc = None
    st.session_state.login_attempts = 0


# ---------------------------------------------------------------------------
# Sidebar - Navigation / Session Info
# ---------------------------------------------------------------------------
st.sidebar.title("🏦 Banking System")

if st.session_state.logged_in_acc:
    acc = st.session_state.accounts[st.session_state.logged_in_acc]
    st.sidebar.success(f"Logged in as **{acc['name']}**")
    st.sidebar.write(f"Account No: `{st.session_state.logged_in_acc}`")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
else:
    st.sidebar.info("Not logged in")

st.sidebar.caption(
    "⚠️ Demo data only — accounts live in memory and reset when the app restarts."
)

# ---------------------------------------------------------------------------
# Main Area
# ---------------------------------------------------------------------------
st.title("Banking System")

# ============================== LOGGED OUT VIEW =============================
if st.session_state.logged_in_acc is None:

    tab_login, tab_create = st.tabs(["🔐 Login", "➕ Create Account"])

    # ---------------- Login Tab ----------------
    with tab_login:
        st.subheader("Login to your account")

        if not st.session_state.accounts:
            st.info("No accounts exist yet. Create one in the 'Create Account' tab.")
        else:
            with st.form("login_form"):
                acc_number = st.text_input("Account Number")
                pin = st.text_input("PIN", type="password", max_chars=4)
                submitted = st.form_submit_button("Login")

            if submitted:
                if bl.authenticate(st.session_state.accounts, acc_number, pin):
                    st.session_state.logged_in_acc = acc_number
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    remaining = 3 - st.session_state.login_attempts
                    if remaining > 0:
                        st.error(f"Incorrect account number or PIN. Attempts remaining: {remaining}")
                    else:
                        st.error("Too many failed attempts. Please try again.")
                        st.session_state.login_attempts = 0

    # ---------------- Create Account Tab ----------------
    with tab_create:
        st.subheader("Create a new account")

        with st.form("create_account_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number (10 digits)")
            pin = st.text_input("Create 4-digit PIN", type="password", max_chars=4)
            confirm_pin = st.text_input("Confirm PIN", type="password", max_chars=4)
            submitted = st.form_submit_button("Create Account")

        if submitted:
            if pin != confirm_pin:
                st.error("PINs do not match.")
            else:
                try:
                    acc_number = bl.create_account(
                        st.session_state.accounts, name, phone, pin
                    )
                    st.success("Account created successfully!")
                    st.info(f"Your Account Number is: **{acc_number}**\n\n"
                            f"Save this number — you'll need it to log in.")
                except ValueError as e:
                    st.error(str(e))

# ============================== LOGGED IN VIEW ==============================
else:
    acc_number = st.session_state.logged_in_acc
    account = st.session_state.accounts[acc_number]

    st.subheader(f"Welcome, {account['name']} 👋")
    st.metric("Current Balance", f"{account['balance']:.2f}")

    (tab_deposit, tab_withdraw, tab_transfer,
     tab_history, tab_pin) = st.tabs(
        ["💰 Deposit", "➖ Withdraw", "🔁 Transfer", "📜 History", "🔑 Change PIN"]
    )

    # ---------------- Deposit ----------------
    with tab_deposit:
        st.subheader("Deposit Money")
        with st.form("deposit_form"):
            amount = st.number_input("Amount to deposit", min_value=0.0, step=1.0)
            submitted = st.form_submit_button("Deposit")
        if submitted:
            try:
                bl.deposit(st.session_state.accounts, acc_number, amount)
                st.success(f"Deposit successful! New balance: "
                           f"{st.session_state.accounts[acc_number]['balance']:.2f}")
            except ValueError as e:
                st.error(str(e))

    # ---------------- Withdraw ----------------
    with tab_withdraw:
        st.subheader("Withdraw Money")
        with st.form("withdraw_form"):
            amount = st.number_input("Amount to withdraw", min_value=0.0, step=1.0)
            submitted = st.form_submit_button("Withdraw")
        if submitted:
            try:
                bl.withdraw(st.session_state.accounts, acc_number, amount)
                st.success(f"Withdrawal successful! New balance: "
                           f"{st.session_state.accounts[acc_number]['balance']:.2f}")
            except ValueError as e:
                st.error(str(e))

    # ---------------- Transfer ----------------
    with tab_transfer:
        st.subheader("Transfer Money")
        with st.form("transfer_form"):
            receiver_acc = st.text_input("Receiver's Account Number")
            amount = st.number_input("Amount to transfer", min_value=0.0, step=1.0)
            submitted = st.form_submit_button("Transfer")
        if submitted:
            try:
                bl.transfer(st.session_state.accounts, acc_number, receiver_acc, amount)
                st.success(f"Transfer successful! New balance: "
                           f"{st.session_state.accounts[acc_number]['balance']:.2f}")
            except ValueError as e:
                st.error(str(e))

    # ---------------- Transaction History ----------------
    with tab_history:
        st.subheader("Transaction History")
        transactions = account["transactions"]
        if not transactions:
            st.info("No transactions yet.")
        else:
            rows = []
            for txn in reversed(transactions):  # most recent first
                rows.append({
                    "Date/Time": txn["time"],
                    "Type": txn["type"],
                    "Amount": f"{txn['amount']:.2f}",
                    "Info": txn["info"]
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)

    # ---------------- Change PIN ----------------
    with tab_pin:
        st.subheader("Change PIN")
        with st.form("change_pin_form"):
            old_pin = st.text_input("Current PIN", type="password", max_chars=4)
            new_pin = st.text_input("New PIN", type="password", max_chars=4)
            confirm_pin = st.text_input("Confirm New PIN", type="password", max_chars=4)
            submitted = st.form_submit_button("Change PIN")
        if submitted:
            try:
                bl.change_pin(st.session_state.accounts, acc_number,
                              old_pin, new_pin, confirm_pin)
                st.success("PIN changed successfully!")
            except ValueError as e:
                st.error(str(e))
