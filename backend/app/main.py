from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .routes import users
from .routes import food_items
from .routes import purchases
from .routes import analytics
from .routes import budgets
from .routes import dashboard

app = FastAPI(
    title="Canteen AI API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(food_items.router)
app.include_router(purchases.router)
app.include_router(analytics.router)
app.include_router(budgets.router)
app.include_router(dashboard.router)

@app.get("/")
def home():
    return {
        "message": "Canteen AI Backend Running"
    }