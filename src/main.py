import db.database as db
import cli.cli as cli

def main():
    db.init_db()
    cli.main()

if __name__ == "__main__":
    main()
