# 💰 Budget Tracker – Backend

This is the **backend API** for the Budget Tracker application built using **FastAPI**.

It provides authentication, expense management APIs, and database integration.

---

## 🚀 Live API

👉 https://budget-tracker-backend-production-5826.up.railway.app

---

## 🛠️ Tech Stack

- FastAPI
- Python
- SQLAlchemy
- MySQL
- JWT Authentication
- Uvicorn

---

## ✨ Features

- User Registration & Login
- JWT-based Authentication
- Protected Expense APIs
- CRUD operations on expenses
- Expense summaries (monthly & category-wise)

---

## 📁 Project Structure
<img width="283" height="422" alt="image" src="https://github.com/user-attachments/assets/2cdd10d5-d073-41b9-b39f-f86597bdd923" />

---

## 🔐 Environment Variables

Create a `.env` file in the root of the backend project.

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=budget_tracker

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🧑‍💻 Run Backend Locally

### Prerequisites
- Python 3.10+
- pip / virtualenv

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<backend-repo>.git

# 2. Go to project directory
cd budget-tracker-backend

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create environment file
cp .env.example .env

# 6. Run the server
uvicorn app.main:app --reload
Backend runs at:
http://localhost:8000




