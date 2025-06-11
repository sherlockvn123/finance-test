import argparse
import csv
import os
from datetime import datetime

DEFAULT_DATA_FILE = 'transactions.csv'


def get_data_file(path=None):
    """Return the path to the data file, defaulting to DEFAULT_DATA_FILE."""
    if path:
        return path
    return os.environ.get('FINANCE_DATA_FILE', DEFAULT_DATA_FILE)


def ensure_file_exists(path):
    """Create the file with headers if it does not exist."""
    if not os.path.exists(path):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'description', 'amount', 'category'])


def add_transaction(args):
    path = get_data_file(args.file)
    ensure_file_exists(path)
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([args.date, args.description, args.amount, args.category])
    print(f"Added transaction to {path}")


def list_transactions(args):
    path = get_data_file(args.file)
    if not os.path.exists(path):
        print(f"No transactions found at {path}")
        return
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"{row['date']}: {row['description']} {row['amount']} ({row['category']})")


def summary(args):
    path = get_data_file(args.file)
    if not os.path.exists(path):
        print(f"No transactions found at {path}")
        return
    income = 0.0
    expense = 0.0
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row['amount'])
            if amount >= 0:
                income += amount
            else:
                expense += amount
    net = income + expense
    print(f"Income: {income:.2f}")
    print(f"Expense: {expense:.2f}")
    print(f"Net: {net:.2f}")


def parse_args():
    parser = argparse.ArgumentParser(description='Personal finance manager')
    parser.add_argument('--file', help='Path to transactions CSV file')
    subparsers = parser.add_subparsers(dest='command')

    add_parser = subparsers.add_parser('add', help='Add a transaction')
    add_parser.add_argument('amount', type=float, help='Transaction amount (use negative for expenses)')
    add_parser.add_argument('description', help='Description of the transaction')
    add_parser.add_argument('--category', default='general', help='Category of the transaction')
    add_parser.add_argument('--date', default=datetime.now().date().isoformat(), help='Date of the transaction')
    add_parser.set_defaults(func=add_transaction)

    list_parser = subparsers.add_parser('list', help='List all transactions')
    list_parser.set_defaults(func=list_transactions)

    summary_parser = subparsers.add_parser('summary', help='Show income, expense, and net totals')
    summary_parser.set_defaults(func=summary)

    return parser.parse_args()


def main():
    args = parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print('No command specified. Use --help for usage information.')


if __name__ == '__main__':
    main()
