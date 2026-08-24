from datetime import date, datetime

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
    description: str | None = Field(default=None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., ge=0)

    calories: int | None = Field(default=None, ge=0)
    protein: float | None = Field(default=None, ge=0)
    carbs: float | None = Field(default=None, ge=0)
    fat: float | None = Field(default=None, ge=0)
    fiber: float | None = Field(default=None, ge=0)
    sugar: float | None = Field(default=None, ge=0)
    is_available: bool = True

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
        if v < 0:
            raise ValueError('Price cannot be negative')
        return v


class FoodItemCreate(FoodItemBase):
    pass


class FoodItem(FoodItemBase):
    item_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class PurchaseCreate(BaseModel):
    user_id: int | None = Field(default=None, gt=0)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    amount: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=500)

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
        if v is not None and v < 0:
            raise ValueError('Amount cannot be negative')
        if v is not None and v > 1000000:
            raise ValueError('Amount cannot exceed 1,000,000')
        return v


class Purchase(PurchaseCreate):
    purchase_id: int
    user_id: int
    unit_price: float | None = None
    total_price: float | None = None
    purchased_at: datetime | None = None
    purchase_time: datetime | None = None

    class Config:
        from_attributes = True


class BudgetBase(BaseModel):
    user_id: int | None = Field(default=None, gt=0)
    monthly_limit: float = Field(..., gt=0)
    period: str = Field(default='monthly', pattern='^monthly$')
    start_date: date | None = None
    end_date: date | None = None

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
    user_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

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

    @field_validator('name')
    @classmethod
    def register_name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()

    @field_validator('email')
    @classmethod
    def register_email_valid(cls, v):
        normalized = v.strip().lower()
        if not EMAIL_PATTERN.match(normalized):
            raise ValueError('Invalid email format')
        return normalized

    @field_validator('department')
    @classmethod
    def register_department_valid(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Department cannot be empty or whitespace only')
        return v.strip()

    @field_validator('year')
    @classmethod
    def register_year_valid(cls, v):
        if v is not None and not 1 <= v <= 5:
            raise ValueError('Year must be between 1 and 5')
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


class FoodScanResponse(BaseModel):
    scan_id: int
    user_id: int
    detected_food_name: str | None = None
    confidence: float | None = None
    estimated_calories: float | None = None
    estimated_protein: float | None = None
    estimated_carbohydrates: float | None = None
    estimated_fat: float | None = None
    estimated_fiber: float | None = None
    portion_description: str | None = None
    analysis_notes: str | None = None
    status: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class FoodScanConfirm(BaseModel):
    detected_food_name: str | None = Field(default=None, max_length=255)
    confidence: float | None = Field(default=None, ge=0, le=1)
    estimated_calories: float | None = Field(default=None, ge=0)
    estimated_protein: float | None = Field(default=None, ge=0)
    estimated_carbohydrates: float | None = Field(default=None, ge=0)
    estimated_fat: float | None = Field(default=None, ge=0)
    estimated_fiber: float | None = Field(default=None, ge=0)
    portion_description: str | None = Field(default=None, max_length=500)
    analysis_notes: str | None = Field(default=None, max_length=2000)
    add_to_purchases: bool = False
    food_item_id: int | None = Field(default=None, gt=0)
    quantity: int = Field(default=1, gt=0, le=1000)