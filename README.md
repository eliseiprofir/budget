# Budget Management System

A comprehensive full-stack application for managing personal and family finances. Built with Django REST Framework backend and Streamlit frontend, this system offers expense tracking, income management, and budget analytics.

## Features

- **Multi-user authentication**
  - Email-based authentication system
  - Complete user account management
  - Secure JWT authentication

- **Transaction management**
  - Record transactions (income/expenses)
  - Detailed descriptions for each transaction
  - Precise transaction dating

- **Category management**
  - Customizable categories for income and expenses
  - Transaction types (positive, negative, neutral)
  - Hierarchical organization of categories

- **Location-based money tracking**
  - Physical and virtual wallets (bank accounts, cash, etc.)
  - Balance tracking by location
  - Transfers between locations

- **Financial Buckets system**
  - Percentage allocation of income into different financial buckets
  - Automatic distribution of income based on allocations
  - Balance tracking by buckets

- **Advanced reporting**:
  - Monthly category-wise analysis
  - Yearly profit/loss statements
  - Multi-year trend analysis
  - Current balance across locations
  - Financial bucket distribution
  - Complete historical reports

## Tech Stack

- **Backend**:
  - Django 5.1.4
  - Django REST Framework 3.15.2
  - Django Allauth for authentication
  - Django Model Utils for advanced models
  - PostgreSQL for database

- **Frontend**:
  - Streamlit 1.41.1
  - Pandas for data manipulation
  - Requests for API communication

- **Authentication**:
  - JWT (JSON Web Tokens)
  - Secure authentication system

- **Testing**:
  - pytest
  - pytest-django
  - Model Bakery for fixtures

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- `virtualenv`

### Setup

#### 1. Clone the repository

```bash
# Clone the repository
git clone https://github.com/eliseiprofir/budget.git
cd budget
```

#### 2. Backend setup (Django)

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment for backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install backend dependencies
pip install -r requirements.txt

# Database setup for backend
python manage.py migrate

# Run development server for backend
python manage.py runserver
```

#### 3. Frontend setup (Streamlit)

```bash
# ⚠️ Important: Open a new terminal window or tab for the frontend setup
# to ensure the backend server continues running uninterrupted.

# Navigate to the frontend directory
cd ../frontend

# Create virtual environment for frontend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install frontend dependencies
pip install -r requirements.txt

# Run development server for frontend
streamlit run app.py
```

### Final steps

- Ensure both the backend and frontend servers are running:
  - Backend will run at `http://127.0.0.1:8000/`
  - Frontend will run at `http://localhost:8501/`

## Testing

```bash
# From the backend directory
cd backend
pytest
```

## Contributing

Contributions are welcome! Please check our contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
