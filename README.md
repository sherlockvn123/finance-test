# finance-test

This project provides a simple command line tool for tracking personal finances.

## Features

- Add income and expense transactions
- List all recorded transactions
- Summarize totals for income, expenses, and net balance

## Usage

```bash
# Add an expense of 15.20 for lunch
python -m finance.cli add -15.20 "Lunch" --category food

# Add income of 1000 from salary
python -m finance.cli add 1000 "Salary" --category income

# List transactions
python -m finance.cli list

# Show summary
python -m finance.cli summary
```

By default, transactions are stored in `transactions.csv` in the current
working directory. You can specify a different file with the `--file` option or
by setting the environment variable `FINANCE_DATA_FILE`.
