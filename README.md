# 🍽️ Canteen AI

An AI-powered student canteen budget and food habit tracking system built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and later **React** and **AI/ML**.

---

# 📌 Problem Statement

Students often spend money in college canteens without tracking their expenses or food habits. This project helps students monitor their spending, understand their eating patterns, receive healthier recommendations, and stay within their monthly budgets.

---

# ✨ Features

## Current Features

- JWT authentication with student and admin roles
- Food catalogue browsing, search, category filtering, and availability
- Student purchase recording with historical unit-price snapshots
- Student purchase history, filtering, editing, and deletion
- Monthly budget creation, updates, period-aware spending, and utilization
- Personal dashboard and basic spending analytics
- PostgreSQL Database
- FastAPI REST APIs
- Swagger API Documentation
- Stored Procedures
- Database Triggers
- SQL Views
- Seeded Sample Data

## Upcoming Features

- Budget Alerts
- AI Food Recommendations
- OCR Receipt Scanner
- Spending Prediction
- Habit Analytics
- Mood Tracking
- Rewards & Badges
- AI Chatbot (Natural Language → SQL)

---

# 🛠️ Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

## Database

- PostgreSQL
- pgAdmin

## Frontend

- React
- Tailwind CSS

## AI / ML (Upcoming)

- Python
- Scikit-learn
- Pandas
- OCR
- Gemini API

---

# 📂 Project Structure

```
canteen-ai/

backend/
database/
frontend/
ml/
docs/
```

---

# 🗄️ Database Tables

- Users
- Food Items
- Purchases
- Budgets
- Mood Log
- Habits
- Rewards
- Recommendations

---

# 📡 Current APIs

## Authentication

- POST /auth/register
- POST /auth/login
- GET /users/me

## Food Items

- GET /food-items
- GET /food-items/{item_id}
- POST/PUT/DELETE /food-items/{item_id} (admin only)

## Purchases

- GET/POST /purchases
- GET/PUT/DELETE /purchases/{purchase_id}

## Budgets and Analytics

- GET/POST /budgets
- GET /budgets/current
- PUT /budgets/{budget_id}
- GET /analytics/summary
- GET /analytics/spending
- GET /analytics/categories
- GET /dashboard

Protected endpoints require `Authorization: Bearer <access_token>`.

## AI Food Scanner

Authenticated students can upload a JPEG, PNG, GIF, or WebP food photo at
`/food-scanner`. The backend sends the image to Gemini and returns structured
food and nutrition estimates. Images are validated server-side and are not
stored as public files. The user reviews and edits the result before saving
the scan; adding a purchase is a separate optional action using an explicitly
selected catalogue item. Estimates are uncertain and are not medical advice.

Set `GEMINI_API_KEY` in the repository-root `.env` for local scanner use.
The key is read only by the backend and is never placed in frontend code.

---

# 🚀 Getting Started

## Clone

```bash
git clone https://github.com/bywr-git/canteen-ai.git
```

## Backend

```bash
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r ..\requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

For local tests, install the development tools and explicitly enable the
isolated in-memory SQLite database:

```bash
pip install -r ..\requirements-dev.txt
$env:TESTING="true"  # PowerShell
pytest -q
```

---

# 📈 Project Status

Current Progress

✅ Authentication and authorization

✅ Core student food, purchase, budget, dashboard, and analytics flows

✅ React frontend foundation

⬜ AI Recommendation Engine

⬜ OCR

⬜ ML Prediction

---

# 👩‍💻 Author

Bhavanam Yashaswini Reddy

Computer Science (AI & ML)

Bengaluru, India