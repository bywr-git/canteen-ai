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

conn = psycopg2.connect(**db_config)

cur = conn.cursor()

# Get item prices
cur.execute("""
    SELECT item_id, price
    FROM food_items
""")

items = cur.fetchall()

price_map = {}
for item_id, price in items:
    price_map[item_id] = float(price)

for _ in range(2000):

    user_id = random.randint(1, 100)

    item_id = random.randint(1, 50)

    quantity = random.randint(1, 3)

    amount = price_map[item_id] * quantity

    cur.execute("""
        INSERT INTO purchases
        (
            user_id,
            item_id,
            quantity,
            amount
        )
        VALUES
        (%s,%s,%s,%s)
    """,
    (
        user_id,
        item_id,
        quantity,
        amount
    ))

conn.commit()

print("2000 purchases inserted successfully!")

cur.close()
conn.close()