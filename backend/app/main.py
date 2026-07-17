from fastapi import FastAPI

from .routes import users
from .routes import food_items
from .routes import purchases
from .routes import analytics

app = FastAPI(
    title="Canteen AI API"
)

app.include_router(users.router)
app.include_router(food_items.router)
app.include_router(purchases.router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {
        "message": "Canteen AI Backend Running"
    }