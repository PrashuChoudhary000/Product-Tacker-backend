from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:DeadEnd3@localhost:5432/fastapi_productPage"
engine = create_engine(db_url)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)