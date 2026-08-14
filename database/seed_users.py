from faker import Faker
import psycopg2
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection parameters from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable not set. "
        "Please create a .env file with DATABASE_URL. "
        "See .env.example for format."
    )

# Parse PostgreSQL connection string
# Format: postgresql://user:password@host:port/database
try:
    from urllib.parse import urlparse
    parsed = urlparse(DATABASE_URL)
    db_config = {
        "host": parsed.hostname,
        "database": parsed.path.lstrip("/"),
        "user": parsed.username,
        "password": parsed.password,
        "port": parsed.port or 5432
    }
except Exception as e:
    raise ValueError(f"Invalid DATABASE_URL format: {e}")

fake = Faker()

conn = psycopg2.connect(**db_config)

cur = conn.cursor()

departments = ["CSE", "AIML", "ECE", "EEE", "MECH"]

for i in range(100):
    name = fake.name()
    email = fake.unique.email()
    department = random.choice(departments)
    year = random.randint(1, 4)

    cur.execute("""
        INSERT INTO users
        (name, email, department, year)
        VALUES (%s, %s, %s, %s)
    """, (name, email, department, year))

conn.commit()

print("100 users inserted successfully!")

cur.close()
conn.close()