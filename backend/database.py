
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_url = "postgresql+psycopg2://postgres:Siddharth@localhost:5432/HRDatabase"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
