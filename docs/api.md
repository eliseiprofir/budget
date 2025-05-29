# API Documentation

## Authentication

### Obtain Token
```http
POST /api/users/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Core Endpoints

```http
GET /api/
```

Response:
```json
{
    "users": "https://domain.com/api/users/",
    "locations": "https://domain.com/api/locations/",
    "buckets": "https://domain.com/api/buckets/",
    "categories": "https://domain.com/api/categories/",
    "transactions": "https://domain.com/api/transactions/",
    "analytics-current": "https://domain.com/api/analytics-current/",
    "analytics-monthly": "https://domain.com/api/analytics-monthly/",
    "analytics-yearly": "https://domain.com/api/analytics-yearly/",
    "analytics-historical": "https://domain.com/api/analytics-historical/"
}
```

### Locations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/locations/ | List all locations |
| POST   | /api/locations/ | Create new location |
| GET    | /api/locations/{id}/ | Get location details |
| PUT    | /api/locations/{id}/ | Update location |
| DELETE | /api/locations/{id}/ | Delete location |

POST/PUT body:
```json
{
    "name": "ING",
    "is_removed": false
}
```

GET /api/locations/ body example:
```json
{
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "name": "ING",
    "is_removed": false,
    "user": "http://domain.com/api/users/01477667-aa35-4d40-9730-9190037fd6d8/"
}
...
```

### Buckets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/buckets/ | List all buckets |
| POST   | /api/buckets/ | Create new bucket |
| GET    | /api/buckets/{id}/ | Get bucket details |
| PUT    | /api/buckets/{id}/ | Update bucket |
| DELETE | /api/buckets/{id}/ | Delete bucket |

POST/PUT body:
```json
{
    "name": "Necessities",
    "allocation_percentage": "50.00",
    "is_removed": false
}
```

GET /api/buckets/ body example:
```json
{
    "id": "91461c66-d475-4e76-9d6b-b2a409491578",
    "name": "Necessities",
    "allocation_percentage": "50",
    "allocation_status": "INCOMPLETE",
    "is_removed": false,
    "user": "http://domain.com/api/users/01477667-aa35-4d40-9730-9190037fd6d8/"
}
```

Notes:
- Categories, Locations, Buckets and Transaction Types support soft delete through `is_removed` field
- `allocation_status` in Buckets is read-only and automatically updated
- Names must be unique per user for all entities
- Total bucket allocation percentage cannot exceed 100%

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/categories/ | List all categories |
| POST   | /api/categories/ | Create new category |
| GET    | /api/categories/{id}/ | Get category details |
| PUT    | /api/categories/{id}/ | Update category |
| DELETE | /api/categories/{id}/ | Delete category |

POST/PUT body:
```json
{
    "name": "Food",
    "sign": "NEGATIVE",
    "is_removed": false
}
```

GET /api/categories/ body example:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Food",
    "sign": "NEGATIVE",
    "is_removed": false,
    "user": "http://domain.com/api/users/01477667-aa35-4d40-9730-9190037fd6d8/"
}
...
```

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/transactions/ | List all transactions |
| POST   | /api/transactions/ | Create new transaction |
| GET    | /api/transactions/{id}/ | Get transaction details |
| PUT    | /api/transactions/{id}/ | Update transaction |
| DELETE | /api/transactions/{id}/ | Delete transaction |

POST/PUT body:
```json
{
    "description": "Grocery Shopping",
    "amount": "150.00",
    "category": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2024-01-15",
    "location": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "bucket": "91461c66-d475-4e76-9d6b-b2a409491578",
    "split_income": false
}
```

GET /api/transactions/ body example:
```json
{
    "id": "a8098c1a-f86e-11da-bd1a-00112444be1e",
    "description": "Grocery Shopping",
    "category": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Food",
        "sign": "NEGATIVE"
    },
    "date": "2024-01-15T00:00:00Z",
    "amount": "150.00",
    "location": {
        "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "name": "ING"
    },
    "bucket": {
        "id": "91461c66-d475-4e76-9d6b-b2a409491578",
        "name": "Necessities"
    },
    "split_income": false,
    "user": "http://domain.com/api/users/01477667-aa35-4d40-9730-9190037fd6d8/"
}
...
```

Validation Rules:
- `split_income` can only be true for positive transactions
- `split_income` requires all buckets to have complete allocation (sum to 100%)

## Analytics Endpoints

### Current Status
```http
GET /api/analytics-current/
```

Response:
```json
{
    "locations": {
        "_total": "15000.0",
        "Main Bank": "4500.0",
        "Savings Account": "10000.0",
        "Cash Wallet": "500.0"
    },
    "buckets": {
        "_total": "15000.0",
        "Emergency Fund": "5000.0",
        "Investments": "7000.0",
        "Daily Expenses": "3000.0"
    },
    "balance": {
        "_total_": "15000.0",
        "positive": "20000.0",
        "negative": "5000.0",
        "neutral": "0.0"
    }
}
```

### Monthly Analysis
```http
GET /api/analytics-monthly/
```
Returns analytics for the current month. For a specific month, use:
```http
GET /api/analytics-monthly/YYYY-MM
```
Example: `/api/analytics-monthly/2024-03`

Response:
```json
{
    "positive_categories": {
        "Salary": "5000.0",
        "Investments": "500.0",
        "Freelance": "1000.0"
    },
    "negative_categories": {
        "Groceries": "800.0",
        "Utilities": "200.0",
        "Entertainment": "300.0"
    },
    "neutral_categories": {
        "Internal transfers": "0.0",
        "Loans": "0.0"
    },
    "balance": {
        "_total": "5200.0",
        "positive": "6500.0",
        "negative": "1300.0",
        "neutral": "0.0"
    },
    "period": {
        "year": 2024,
        "month": 3
    }
}
```

Notes:
- Month format must be between 01-12
- Year format must be between 1900-2100
- Invalid formats will return 400 Bad Request

### Yearly Analysis
```http
GET /api/analytics-yearly/
```
Returns analytics for the current year. For a specific year, use:
```http
GET /api/analytics-yearly/YYYY
```
Example: `/api/analytics-yearly/2024`

Response:
```json
{
    "monthly": {
        "1": {
            "positive_categories": {
                "Salary": "1000.0",
                "Investments": "0.0",
                "Freelance": "0.0"
            },
            "negative_categories": {
                "Groceries": "200.0",
                "Utilities": "50.0"
            },
            "neutral_categories": {
                "Internal transfers": "0.0",
                "Loans": "0.0"
            },
            "balance": {
                "_total": "1750.0",
                "positive": "2000.0",
                "negative": "250.0",
                "neutral": "0.0"
            }
        },
        // ... other months
    },
    "summary": {
        "positive_categories": {
            "Salary": "5000.0",
            "Investments": "500.0",
            "Freelance": "1000.0"
        },
        "negative_categories": {
            "Groceries": "800.0",
            "Utilities": "200.0",
            "Entertainment": "300.0"
        },
        "neutral_categories": {
            "Internal transfers": "0.0",
            "Loans": "0.0"
        },
        "balance": {
            "_total": "5200.0",
            "positive": "6500.0",
            "negative": "1300.0",
            "neutral": "0.0"
        }
    },
    "period": 2024
}
```

Notes:
- Year format must be between 1900-2100
- Invalid formats will return 400 Bad Request

### Historical Analysis
```http
GET /api/analytics-historical/
```

Response:
```json
{
    "yearly": {
        "2024": {
            "positive_categories": {
                "Salary": "5000.0",
                "Investments": "500.0",
                "Freelance": "1000.0"
            },
            "negative_categories": {
                "Groceries": "800.0",
                "Utilities": "200.0",
                "Entertainment": "300.0"
            },
            "neutral_categories": {
                "Internal transfers": "0.0",
                "Loans": "0.0"
            },
            "balance": {
                "_total": "5200.0",
                "positive": "6500.0",
                "negative": "1300.0",
                "neutral": "0.0"
            }
        },
        // ... other years
    },
    "summary": {
        "positive_categories": {
            "Salary": "10000.0",
            "Investments": "100.0",
            "Freelance": "2000.0"
        },
        "negative_categories": {
            "Groceries": "1600.0",
            "Utilities": "400.0",
            "Entertainment": "600.0"
        },
        "neutral_categories": {
            "Internal transfers": "0.0",
            "Loans": "0.0"
        },
        "balance": {
            "_total": "10400.0",
            "positive": "13000.0",
            "negative": "2600.0",
            "neutral": "0.0"
        }
    }
}
```

## Common Headers

All requests require:
```http
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

## Response Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error