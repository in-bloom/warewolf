import argparse
import sys
from pathlib import Path

# Ensure `src` is on sys.path so `warewolf` package can be imported when running
# this script from the repository root.
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root / "src"))

from warewolf.hypno import hypno_toad
import importlib

# `import` is a Python keyword, and there's a package directory named `import`.
# Import it dynamically to avoid syntax errors: `warewolf.import.crud`.
crud_mod = importlib.import_module("warewolf.import.crud")
create_db_with_schema = getattr(crud_mod, "create_db_with_schema")


def main():
    """Main program access point

    On startup this will ensure the SQLite database file exists and the
    schema from `src/warewolf/import/schema.sql` is applied (if present).
    """

    # ensure data directory and db exist, apply schema if available
    project_root = Path(__file__).parent.resolve()
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    db_file = data_dir / "warewolf.db"
    schema_file = project_root / "src" / "warewolf" / "import" / "schema.sql"

    if schema_file.exists():
        print(f"Applying schema from {schema_file} to {db_file}")
        conn = create_db_with_schema(str(db_file), schema_file=str(schema_file))
    else:
        print(f"No schema file found at {schema_file}; creating DB file {db_file} without schema")
        conn = create_db_with_schema(str(db_file))

    # close connection immediately; other parts of the app should open when needed
    if conn:
        conn.close()

    parser = argparse.ArgumentParser(
        description="Meta Project"
    )
    parser.add_argument(
        "-hypno", "--hypnotoad",
        action="store_true",
        help="GLORY TO THE HYPNO TOAD"
    )

    args = parser.parse_args()

    if args.hypnotoad:
        hypno_toad()


if __name__ == "__main__":
    main()
