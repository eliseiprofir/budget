# Budget Management System

A comprehensive full-stack application for managing personal and family finances. Built with Django REST Framework backend and Streamlit frontend, this system offers expense tracking, income management, and budget analytics.

## Features

- **Multi-user authentication**  
- **Transaction tracking** (expenses/income)  
- **Category management**  
- **Location-based money tracking** (physical & virtual wallets)  
- **Advanced reporting**:  
  - Monthly category-wise analysis  
  - Yearly profit/loss statements  
  - Multi-year trend analysis  
  - Current balance across locations  
  - Financial bucket distribution  

## Tech Stack

- **Backend**: Django REST Framework  
- **Frontend**: Streamlit  
- **Database**: PostgreSQL  
- **Authentication**: JWT  
- **Testing**: pytest  

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
cd family-budget-tracker
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
pytest
```

## Contributing

Contributions are welcome! Please check our contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
