import psycopg2
import random

conn = psycopg2.connect(
    host="localhost",
    database="canteen_ai",
    user="postgres",
    password="Yashu2006"
)

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