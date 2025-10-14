CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT,
    category TEXT,
    amount REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS incomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    description TEXT,
    category TEXT,
    amount REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS balance (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    curr_balance REAL NOT NULL DEFAULT 0
);
