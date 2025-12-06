from pathlib import Path
from .database import Base, engine

PARENT_DIR = Path(__file__).resolve().parents[1]


def create_tables(table_name):
    filename = table_name if table_name.endswith(".db") else f"{table_name}.db"
    path = Path(filename)
    db_path = path if path.is_absolute() else PARENT_DIR / path
    if db_path.exists():
        print(f"{db_path.name} already exists at {db_path}.")
        return
    Base.metadata.create_all(bind = engine)
    print(f"{table_name} Tables created successfully at {db_path}.")
