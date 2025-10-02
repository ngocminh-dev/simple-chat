import os

from sqlalchemy import create_engine, text

user = os.getenv("PGUSER", "pg")
password = os.getenv("PGPASSWORD", "pg")
db = os.getenv("PGDATABASE", "pg")
host = os.getenv("PGHOST", "localhost")
port = os.getenv("PGPORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA public;"))
    conn.commit()

print("Dropped table")
