import sys
from pathlib import Path

PARENT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(PARENT_DIR))

from backend.create_tables import create_tables


def main():
    create_tables("games")


if __name__ == "__main__":
    main()
