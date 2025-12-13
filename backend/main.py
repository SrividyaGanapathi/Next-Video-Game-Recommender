import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

PARENT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(PARENT_DIR))

from backend.create_tables import create_tables
from backend.update_games import populate_games, _api_key

def main():
    create_tables("games")
    api_key = _api_key()
    populate_games(api_key)


if __name__ == "__main__":
    main()
