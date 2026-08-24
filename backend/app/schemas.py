from datetime import datetime

from pydantic import BaseModel, Field, field_validator
import re


# Simple email validation pattern
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    department: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1, le=5)
    # password intentionally omitted from generic create; use Register schema where needed

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()

    @field_validator('email')
    @classmethod
    def email_valid(cls, v):
        if not EMAIL_PATTERN.match(v.strip()):
            raise ValueError('Invalid email format')
        return v.strip().lower()

    @field_validator('department')
    @classmethod
    def department_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Department cannot be empty or whitespace only')
        return v.strip()


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    department: str | None = None
    year: int | None = None
    role: str = Field(..., pattern="^(student|admin)$")
    is_active: bool = Field(...)
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_login: datetime | None = None

    class Config:
        from_attributes = True


class FoodItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)

    calories: int = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)
    sugar: float = Field(..., ge=0)

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Food name cannot be empty or whitespace only')
        return v.strip()

    @field_validator('category')
    @classmethod
    def category_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Category cannot be empty or whitespace only')
        return v.strip()

    @field_validator('price')
    @classmethod
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v


class FoodItemCreate(FoodItemBase):
    pass


class FoodItem(FoodItemBase):
    item_id: int

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)

    @field_validator('user_id')
    @classmethod
    def user_id_positive(cls, v):
        if v <= 0:
            raise ValueError('User ID must be greater than 0')
        return v

    @field_validator('item_id')
    @classmethod
    def item_id_positive(cls, v):
        if v <= 0:
            raise ValueError('Item ID must be greater than 0')
        return v

    @field_validator('quantity')
    @classmethod
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        if v > 1000:
            raise ValueError('Quantity cannot exceed 1000')
        return v

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        if v > 1000000:
            raise ValueError('Amount cannot exceed 1,000,000')
        return v


class Purchase(PurchaseCreate):
    purchase_id: int

    class Config:
        from_attributes = True


class BudgetBase(BaseModel):
    user_id: int = Field(..., gt=0)
    monthly_limit: float = Field(..., gt=0)

    @field_validator('user_id')
    @classmethod
    def user_id_positive(cls, v):
        if v <= 0:
            raise ValueError('User ID must be greater than 0')
        return v

    @field_validator('monthly_limit')
    @classmethod
    def budget_limit_positive(cls, v):
        if v <= 0:
            raise ValueError('Budget limit must be greater than 0')
        if v > 10000000:
            raise ValueError('Budget limit cannot exceed 10,000,000')
        return v


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    budget_id: int

    class Config:
        from_attributes = True


# =============================
# Analytics Response Schemas
# =============================

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


# ------------------
# Authentication schemas
# ------------------

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8)
    department: str | None = None
    year: int | None = None

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    role: str | None = None