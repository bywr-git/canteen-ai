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