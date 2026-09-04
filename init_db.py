import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database with schema and seed data."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found, skipping remote init.")
        return

    print("Connecting to database...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cursor = conn.cursor()

    # Run create.sql
    print("Running create.sql...")
    with open("create.sql", "r") as f:
        cursor.execute(f.read())
    print("Tables created.")

    # Run insert.sql
    print("Running insert.sql...")
    with open("insert.sql", "r") as f:
        cursor.execute(f.read())
    print("Seed data inserted.")

    cursor.close()
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    init_database()
