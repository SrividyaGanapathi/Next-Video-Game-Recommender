from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_URL = "sqlite:///./games.db"
engine = create_engine(database_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
