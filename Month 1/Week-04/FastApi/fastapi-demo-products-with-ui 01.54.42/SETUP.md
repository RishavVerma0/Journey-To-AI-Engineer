# Telusko Trac — Full Setup Guide

## Prerequisites
- Python 3.11+
- Node.js (LTS)
- Homebrew (Mac)

---

## Step 1 — PostgreSQL: Install & Start
> One-time setup

```bash
# Install PostgreSQL
brew install postgresql@15

# Start the service
brew services start postgresql@15

# Add to PATH (run once)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

---

## Step 2 — PostgreSQL: Create User & Database
> One-time setup

```bash
# Open psql shell
psql postgres
```

Inside psql, run these SQL commands one by one:

```sql
-- Create the postgres superuser
CREATE USER postgres WITH SUPERUSER PASSWORD '12345678';

-- Create the telusko database
CREATE DATABASE telusko OWNER postgres;

-- Exit psql
\q
```

---

## Step 3 — Backend: Python & FastAPI
> Terminal 1

```bash
# Navigate to project folder
cd "fastapi-demo-products-with-ui 01.54.42"

# Create virtual environment
python3 -m venv myenv

# Activate virtual environment
source myenv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary

# Start the backend server
uvicorn main:app --reload
```

---

## Step 4 — Frontend: React
> Terminal 2 (new tab)

```bash
# Go into frontend folder
cd frontend

# Install Node dependencies
npm install

# Start React app
npm start
```

---

## Every Time You Return to the Project

```bash
# 1. Ensure PostgreSQL is running
brew services start postgresql@15

# 2. Activate venv + run backend (Terminal 1)
source myenv/bin/activate && uvicorn main:app --reload

# 3. Run frontend (Terminal 2)
cd frontend && npm start
```

---

## URLs

| Service        | URL                          |
|----------------|------------------------------|
| React UI       | http://localhost:3000        |
| FastAPI backend| http://localhost:8000        |
| Swagger docs   | http://localhost:8000/docs   |
| ReDoc          | http://localhost:8000/redoc  |
