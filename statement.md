# Problem Statement & System Scope

## Problem Statement
Traditional CLI-based banking scripts lack user accessibility and fail to preserve application state across restarts. This project aims to deliver a modern, cross-platform graphical desktop application that demonstrates object-oriented design, decoupled architecture (separating GUI, domain logic, and persistence), and robust input validation.

## Scope of Work

### 1. Functional Requirements
- **Account Registration**:
  - Accept full name, a 4-digit PIN, and an initial deposit ($\ge 0$).
  - Assign a unique, auto-incremented 6-digit account identifier.
- **Authentication**:
  - Authenticate users via account number and 4-digit PIN.
- **Financial Transactions**:
  - Credit (Deposit) and debit (Withdrawal) operations with non-negative validation.
  - Reject debit requests exceeding the available balance.
- **Audit Logging**:
  - Maintain a chronological transaction log for every account.

### 2. Technical & Architectural Requirements
- **Architecture**: Separated presentation layer (`gui.py`), business logic (`models.py`), and storage integration (`storage.py`).
- **UI Framework**: Standard Python `tkinter` / `ttk` library.
- **Storage**: Lightweight, persistent JSON-backed storage engine (`bank_data.json`).
- **Quality Assurance**: Automated testing suite using Python's native `unittest`.
