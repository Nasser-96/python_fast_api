from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from scout_apm.sqlalchemy import instrument_sqlalchemy

import os
from dotenv import load_dotenv

load_dotenv()

class BaseDb:
    def __init__(self, db_url: str, read_db_url: str = None):
        # Create the main engine
        self.engine = create_engine(db_url, future=True)

        # Create a read-only engine if provided, else reuse the main one
        self.read_engine = create_engine(read_db_url, future=True) if read_db_url else self.engine

        # instrument_sqlalchemy :
        # Monitoring Metrics: This enables Scout APM to:
        # - Measure the execution time of each query.
        # - Record query metadata (e.g., query type, table accessed).
        # - Identify slow queries or potential bottlenecks.
        instrument_sqlalchemy(self.engine)
        instrument_sqlalchemy(self.read_engine)
        # Configure sessionmaker for both engines
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.ReadSessionLocal = sessionmaker(bind=self.read_engine, autocommit=False, autoflush=False)

    # Example method to get a session
    def get_session(self):
        with self.SessionLocal() as session:
            yield session

    # Optional: Method for read-only sessions
    def get_read_session(self):
        with self.ReadSessionLocal() as session:
            yield session


Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
db = BaseDb(db_url=DATABASE_URL)
