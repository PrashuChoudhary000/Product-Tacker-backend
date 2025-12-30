# from sqlalchemy import create_engine

# from sqlalchemy.orm import sessionmaker

# db_url = "postgresql://postgres:DeadEnd3@localhost:5432/fastapi_productPage"
# engine = create_engine(db_url)

# session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database for deployment (works everywhere)
db_url = "sqlite:///./products.db"

engine = create_engine(
    db_url, 
    connect_args={"check_same_thread": False}  # Required for SQLite
)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
