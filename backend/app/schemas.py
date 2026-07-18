from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    department: str
    year: int

class UserResponse(UserCreate):
    user_id: int

    class Config:
        from_attributes = True

class FoodItemBase(BaseModel):
    name: str
    category: str
    price: float

    calories: int
    protein: float
    carbs: float
    fat: float
    sugar: float


class FoodItemCreate(FoodItemBase):
    pass


class FoodItem(FoodItemBase):
    item_id: int

    class Config:
        from_attributes = True

class PurchaseCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int
    amount: float


class Purchase(PurchaseCreate):
    purchase_id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    user_id: int
    monthly_limit: float


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    budget_id: int

    class Config:
        from_attributes = True

# -----------------------------
# Analytics Response Schemas
# -----------------------------

class BudgetSummaryResponse(BaseModel):
    user_id: int
    monthly_budget: float
    total_spent: float
    remaining: float
    status: str


class HealthScoreResponse(BaseModel):
    user_id: int
    healthy_items: int
    junk_items: int
    neutral_items: int
    healthy_score: float
    message: str

class TopFood(BaseModel):
    food_name: str
    category: str
    times_purchased: int

class CategorySpending(BaseModel):
    category: str
    total_spent: float

class NutritionSummary(BaseModel):
    user_id: int
    total_calories: int
    protein: float
    carbs: float
    fat: float
    sugar: float