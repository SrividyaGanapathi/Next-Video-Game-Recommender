from sqlalchemy import Column,Integer,Float,String,Date
from .database import Base

class Games(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key = True, index = True)
    rawg_id = Column(Integer, unique=True, index = True)
    slug = Column(String, unique = True, index = True)
    name = Column(String, index = True, nullable = False)
    description = Column(String)
    genres = Column(String)
    platforms = Column(String)
    released = Column(String) #'YYYY-MM-DD'
    rating = Column(Float) # RAWG user rating (0–5)
    metacritic_rating = Column(Float) 
    

