import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="canteen_ai",
    user="postgres",
    password="Yashu2006"
)

cur = conn.cursor()

food_items = [
    ("Tea", "Drinks", 15, 80, 1, 15, 2, 10),
    ("Coffee", "Drinks", 20, 90, 2, 12, 3, 8),
    ("Samosa", "Snacks", 25, 250, 5, 30, 12, 2),
    ("Idli", "Breakfast", 30, 150, 4, 28, 1, 1),
    ("Dosa", "Breakfast", 40, 280, 6, 40, 8, 2),
    ("Poha", "Breakfast", 35, 200, 5, 35, 4, 2),
    ("Veg Rice", "Lunch", 60, 350, 8, 60, 6, 3),
    ("Paneer Roll", "Snacks", 70, 400, 12, 45, 15, 4),
    ("Cold Drink", "Drinks", 30, 140, 0, 35, 0, 35),
    ("Burger", "Snacks", 80, 450, 14, 40, 20, 6),
    ("Sandwich", "Snacks", 50, 250, 8, 30, 7, 3),
    ("Vada", "Breakfast", 20, 180, 4, 20, 10, 1),
    ("Upma", "Breakfast", 30, 190, 5, 32, 5, 2),
    ("Pongal", "Breakfast", 40, 280, 7, 38, 9, 1),
    ("Lemon Rice", "Lunch", 50, 300, 6, 50, 6, 2),
    ("Curd Rice", "Lunch", 45, 270, 7, 42, 5, 3),
    ("Fried Rice", "Lunch", 70, 420, 8, 65, 10, 4),
    ("Noodles", "Lunch", 75, 430, 9, 68, 11, 5),
    ("Maggie", "Snacks", 40, 320, 6, 50, 12, 2),
    ("Puffs", "Snacks", 25, 230, 4, 28, 11, 2),
    ("Banana", "Fruits", 10, 90, 1, 23, 0, 12),
    ("Apple", "Fruits", 25, 95, 1, 25, 0, 19),
    ("Orange", "Fruits", 20, 70, 1, 18, 0, 14),
    ("Watermelon", "Fruits", 15, 50, 1, 13, 0, 10),
    ("Milk", "Drinks", 25, 120, 8, 12, 5, 12),
    ("Lassi", "Drinks", 35, 180, 6, 20, 4, 18),
    ("Buttermilk", "Drinks", 20, 60, 3, 8, 2, 5),
    ("Chocolate Milk", "Drinks", 40, 220, 7, 30, 6, 25),
    ("Veg Biryani", "Lunch", 90, 500, 10, 75, 12, 4),
    ("Paneer Biryani", "Lunch", 120, 650, 18, 70, 20, 5),
    ("Chapati", "Dinner", 15, 120, 3, 22, 2, 1),
    ("Dal", "Dinner", 40, 180, 9, 25, 3, 2),
    ("Paneer Curry", "Dinner", 80, 350, 15, 12, 22, 4),
    ("Veg Curry", "Dinner", 60, 220, 6, 18, 10, 4),
    ("Ice Cream", "Dessert", 50, 300, 4, 35, 15, 30),
    ("Brownie", "Dessert", 60, 380, 5, 45, 18, 35),
    ("Cake", "Dessert", 70, 420, 6, 50, 20, 40),
    ("Muffin", "Dessert", 45, 280, 4, 38, 12, 24),
    ("Cookies", "Dessert", 30, 210, 3, 30, 9, 18),
    ("Fruit Salad", "Dessert", 50, 140, 2, 30, 1, 22),
    ("Corn", "Snacks", 25, 130, 4, 26, 2, 4),
    ("Sprouts", "Healthy", 35, 160, 10, 24, 2, 3),
    ("Oats", "Healthy", 40, 180, 8, 30, 3, 1),
    ("Protein Shake", "Healthy", 90, 250, 25, 12, 5, 4),
    ("Green Tea", "Healthy", 20, 5, 0, 1, 0, 0),
    ("Smoothie", "Healthy", 80, 220, 5, 40, 2, 25),
    ("Peanut Chikki", "Healthy", 20, 150, 5, 15, 8, 6),
    ("Boiled Eggs", "Healthy", 30, 140, 12, 1, 10, 0),
    ("Omelette", "Breakfast", 40, 200, 14, 2, 15, 0),
    ("Veg Wrap", "Snacks", 60, 300, 8, 35, 10, 3)
]

for item in food_items:
    cur.execute("""
        INSERT INTO food_items
        (name, category, price, calories, protein, carbs, fat, sugar)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, item)

conn.commit()

print("50 food items inserted successfully!")

cur.close()
conn.close()