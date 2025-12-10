import argparse
from pathlib import Path
import sys

# Assicurati che `src` sia nel path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root / "src"))

# Import dei moduli interni
from warewolf.hypno import hypno_toad
from warewolf.data_import import crud, data_loader, db_conn

DB_FILE = project_root / "db" / "warewolf.db"


def setup_database():
    """Crea la cartella data e applica lo schema se disponibile."""
    DB_FILE.parent.mkdir(exist_ok=True)

    conn = db_conn.init_db(DB_FILE)
    if conn:
        conn.close()


def main():
    # Assicurazione DB
    setup_database()

    # Parser CLI
    parser = argparse.ArgumentParser(description="Warewolf CLI")
    parser.add_argument(
        "-hypno", "--hypnotoad",
        action="store_true",
        help="GLORY TO THE HYPNO TOAD"
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subcommand: import recordings
    parser_import = subparsers.add_parser("import-recordings", help="Import recordings from folder")
    parser_import.add_argument("folder", type=str, help="Folder path with files")
    parser_import.add_argument("data", type=str, help="Data value for recordings")
    parser_import.add_argument("coordinates", type=str, help="Coordinates")

    args = parser.parse_args()

    # Flag speciale
    if args.hypnotoad:
        hypno_toad()
        return

    # Gestione subcommands
    if args.command == "import-recordings":
        result = data_loader.import_data(str(DB_FILE), args.folder, args.data, args.coordinates)
        print(result)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()