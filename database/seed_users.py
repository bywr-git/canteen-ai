from faker import Faker
import psycopg2
import random

fake = Faker()

conn = psycopg2.connect(
    host="localhost",
    database="canteen_ai",
    user="postgres",
    password="Yashu2006"
)

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