import argparse

def main():
    parser = argparse.ArgumentParser(description = "Personal Finances Tracker CLI")
    subparsers = parser.add_subparsers(dest = "command", required = True)

    list_parser = subparsers.add_parser("list", help = "Lists all expenses")

    args = parser.parse_args()

    print(args)
    print(args.command)

if __name__ == "__main__":
    main()
