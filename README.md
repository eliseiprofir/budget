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

```bash
# Clone repository
git clone https://github.com/yourusername/family-budget-tracker.git
cd family-budget-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Run development server
python manage.py runserver  # Backend
streamlit run frontend/app.py  # Frontend
```

## Testing

```bash
pytest
```

## Contributing

Contributions are welcome! Please check our contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file for details.
