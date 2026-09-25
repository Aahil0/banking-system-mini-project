# 🏦 Banking System – Streamlit Web App

A web-based version of the [console Banking System mini project](../banking-system),
rebuilt with [Streamlit](https://streamlit.io) so it can be run and demoed in
a browser instead of a terminal.

> This is a **portfolio/demo extension**, built after the original console
> assignment was submitted (the assignment itself required a plain console
> app with no frameworks). The underlying banking rules are identical —
> only the interface changed.

---

## Features

Everything from the original project, in a browser UI:

- Create an account (name, phone number, 4-digit PIN)
- Login with account number + PIN
- Check balance
- Deposit / Withdraw money (with validation)
- Transfer money between accounts
- View transaction history (as a table)
- Change PIN
- Logout

---

## Project Structure

```text
banking-streamlit/
├── app.py              # Streamlit UI layer (all st.* code lives here)
├── banking_logic.py     # Pure Python banking logic (no Streamlit dependency)
├── requirements.txt     # streamlit
```

The logic is intentionally kept separate from the UI in `banking_logic.py` —
this is the same reasoning behind why the original console app used
functions: it keeps each operation testable and reusable no matter what
interface sits on top of it.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

Streamlit will open the app automatically in your browser (usually at
`http://localhost:8501`).

### Running from Google Colab

Streamlit apps don't display inline in Colab the way `input()`-based scripts
do. The simplest options are:
- Run it locally on your own machine (recommended), or
- Use a tunneling tool like `localtunnel` inside Colab, e.g.:
  ```bash
  !pip install streamlit -q
  !streamlit run app.py &>/content/logs.txt &
  !npx localtunnel --port 8501
  ```
  then open the tunnel URL it prints.

### Deploying online (optional)

To make it accessible via a public link, you can deploy it for free on
[Streamlit Community Cloud](https://streamlit.io/cloud):
1. Push this folder to a GitHub repo (or a subfolder of one).
2. Go to share.streamlit.io, sign in with GitHub, and point it at `app.py`.
3. It will give you a public URL.

---

## Important Notes

- **Data is not persisted.** Accounts live in Streamlit's `session_state`
  (in-memory) and are lost whenever the app restarts — same as the
  original console version, which also didn't save to disk.
- **Not production-grade security.** PINs are stored in plain text in
  memory, purely for learning purposes, just like the console version.

---

## Relationship to the Original Console Project

| | Console version | Streamlit version |
|---|---|---|
| Interface | Terminal (`input()`/`print()`) | Browser (Streamlit widgets) |
| Banking logic | Inline in `banking_system.py` | Extracted into `banking_logic.py`, reused |
| Data storage | In-memory dict | In-memory `session_state` dict |
| Assignment requirement | ✅ Matches PDF scope | Extra / optional |
