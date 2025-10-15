# 💰 Personal Finances Tracker

A **cross-platform personal finance management tool** built in **Python**, designed to help you track your expenses and incomes easily. It currently runs through a **Command-Line Interface (CLI)** and stores your financial data locally using **SQLite**. Future versions will include a **desktop GUI** for macOS and other operating systems.

---

## 📖 Table of Contents

* [Features](#-features)
* [Project Structure](#-project-structure)
* [Getting Started](#-getting-started)
  * [1. Prerequisites](#1-prerequisites)
  * [2. Clone the Repository](#2-clone-the-repository)
  * [3. Initialize the Database](#3-initialize-the-database)
  * [4. Run the CLI](#4-run-the-cli)
* [Usage](#-usage)
* [License](#️-license)

---

## 🚀 Features

✅ Track **expenses** and **incomes** with categories

✅ Add, list, edit, and delete entries directly from the CLI

✅ Persistent local **SQLite database**

✅ Built-in **schema initialization**

✅ **Summary** functionality (balance tracking, future analytics planned)

✅ Extensible architecture — easily add new features

✅ Unit-tested (TBD)

---

## 🗂 Project Structure

```
PERSONAL-FINANCES-TRACKER/
├── src/
│   ├── cli/                    # Command-line interface
│   │   ├── cli.py
│   │   └── __init__.py
│   │
│   ├── db/                     # Database logic
│   │   ├── database.py
│   │   ├── schema.sql
│   │   └── __init__.py
│   │
│   ├── internal_libs/          # Core data models and shared logic
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── income.py
│   │   └── __init__.py
│   │
│   └── main.py                 # Application entry point
│
├── unit_tests/                 # Unit tests (pytest)
│
├── README.md
│
└── .gitignore
```

---

## 🧰 Getting Started

### 1. Prerequisites

You need:

* **Python 3.10+**
* **pip**
* **git**

Check your versions:

```bash
python3 --version
git --version
```

---

### 2. Clone the Repository

```bash
git clone git@github.com:<your-username>/personal-finances-tracker.git
cd personal-finances-tracker
```

---

### 3. Initialize the Database

The first time you run the app it will automatically create the database in a empty state. So you can run any command to setup the database. It will create `finances.db` file and populate it using `schema.sql`.

---

### 4. Run the CLI

From the project root:

```bash
python3 src/main.py -h
```

---

## 💻 Usage

Run the app from the project root:

```bash
python3 src/main.py [command] [options]
```

### 🧩 Available Commands

| Command        | Description                                       |
| -------------- | ------------------------------------------------- |
| `show_balance` | Displays the current balance                      |
| `set_balance`  | Sets or updates the current balance               |
| `list_exp`     | Lists all recorded expenses                       |
| `list_inc`     | Lists all recorded incomes                        |
| `categories`   | Lists all available expense and income categories |
| `add_exp`      | Adds a new expense                                |
| `add_inc`      | Adds a new income                                 |
| `edit_exp`     | Edits an existing expense (by ID)                 |
| `edit_inc`     | Edits an existing income (by ID)                  |
| `del_exp`      | Deletes an expense (by ID)                        |
| `del_inc`      | Deletes an income (by ID)                         |

---

### ⚙️ Command Examples

**List all expenses:**

```bash
python3 src/main.py list_exp
```

**Add a new expense:**

```bash
python3 src/main.py add_exp --amount 45.90 --description "Groceries" --category FOOD
```

**Add a new income:**

```bash
python3 src/main.py add_inc --amount 1500 --description "Salary" --category SALARY
```

**Edit an expense (ID 3):**

```bash
python3 src/main.py edit_exp 3 --amount 55.00 --description "Weekly shopping"
```

**Delete an income (ID 2):**

```bash
python3 src/main.py del_inc 2
```

**Check current balance:**

```bash
python3 src/main.py show_balance
```

**Manually set balance:**

```bash
python3 src/main.py set_balance 200.00
```

**List all categories:**

```bash
python3 src/main.py categories
```

---

### 🆘 Help

You can view help for any command by running:

```bash
python3 src/main.py [command] --help
```

Example:

```bash
python3 src/main.py add_exp --help
```

---

## 🧪 Testing

Unit tests are written using **pytest**.

Run all tests:

```bash
pytest -v
```

Example output:

```
tests/test_expense.py::test_expense_default_values PASSED
tests/test_expense_custom_values PASSED
```

---

## ⚖️ License

This project is released under the **MIT License**.
Feel free to use, modify, and distribute it with attribution.

---
