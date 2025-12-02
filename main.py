import argparse
from warewolf.hypno import hypno_toad

def main():
    """Main program access point"""

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
