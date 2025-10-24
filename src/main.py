import db.database as db
import cli.cli as cli

def main():
    success = db.init_db()
    if success:
        cli.main()
    else:
        print("ERROR: Failed to initialize db.")

if __name__ == "__main__":
    main()
