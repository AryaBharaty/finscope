# backend/scripts/seed_db.py

import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend.app.models.transaction import Transaction
from backend.app.core.database import Base

# 1. Database Setup

# Load database URL from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://username:password@localhost:5432/finscope_db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. CSV Path Setup

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the CSV file
csv_path = os.path.join(BASE_DIR, "..", "data", "sample_transactions.csv")

# Check if CSV exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at {csv_path}")

# 3. Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# 4. Seed Database
def seed_database():
    # Read CSV into pandas DataFrame
    df = pd.read_csv(csv_path)

    # Start database session
    db = SessionLocal()

    try:
        # Add each transaction from CSV to the session
        for _, row in df.iterrows():
            transaction = Transaction(
                date=row["date"],
                amount=row["amount"],
                category=row["category"],
                description=row["description"]
            )
            db.add(transaction)

        # Commit the session to save data in DB
        db.commit()
        print(f"Successfully seeded {len(df)} transactions.")

    except Exception as e:
        # Rollback if any error occurs
        db.rollback()
        print("Error seeding database:", e)

    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    seed_database()
