# API Documentation

## Authentication

### Obtain Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "user@example.com",
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

Example Response:
```json
{
    "id": "a8098c1a-f86e-11da-bd1a-00112444be1e",
    "description": "Grocery Shopping",
    "amount": "150.00",
    "category": "http://127.0.0.1:8000/api/categories/550e8400-e29b-41d4-a716-446655440000/",
    "date": "2024-01-15T00:00:00Z",
    "location": "http://127.0.0.1:8000/api/locations/7c9e6679-7425-40de-944b-e07fc1f90ae7/",
    "bucket": "http://127.0.0.1:8000/api/buckets/91461c66-d475-4e76-9d6b-b2a409491578/",
    "split_income": false,
    "user": "http://127.0.0.1:8000/api/users/01477667-aa35-4d40-9730-9190037fd6d8/",
    "created": "2024-01-15T12:00:00Z",
    "modified": "2024-01-15T12:00:00Z"
}
```

Validation Rules:
- `split_income` can only be true for positive transactions
- `split_income` requires all buckets to have complete allocation (sum to 100%)

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/categories/ | List all categories |
| POST   | /api/categories/ | Create new category |
| GET    | /api/categories/{id}/ | Get category details |
| PUT    | /api/categories/{id}/ | Update category |
| DELETE | /api/categories/{id}/ | Delete category |

Example Response:
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Monthly Groceries",
    "transaction_type": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "name": "Expense",
        "sign": "NEGATIVE"
    },
    "is_removed": false,
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z"
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

Example Response:
```json
{
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "name": "ING Debit Card",
    "is_removed": false,
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z"
}
```

### Buckets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/buckets/ | List all buckets |
| POST   | /api/buckets/ | Create new bucket |
| GET    | /api/buckets/{id}/ | Get bucket details |
| PUT    | /api/buckets/{id}/ | Update bucket |
| DELETE | /api/buckets/{id}/ | Delete bucket |

Example Response:
```json
{
    "id": "91461c66-d475-4e76-9d6b-b2a409491578",
    "name": "Necessities",
    "allocation_percentage": "50.00",
    "allocation_status": "INCOMPLETE",
    "is_removed": false,
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z"
}
```

Notes:
- Categories, Locations, Buckets and Transaction Types support soft delete through `is_removed` field
- `allocation_status` in Buckets is read-only and automatically updated
- Names must be unique per user for all entities
- Total bucket allocation percentage cannot exceed 100%

## Analytics Endpoints

### Current Status
```http
GET /api/analytics-current/
```

Response:
```json
{
    "locations": {
        "Main Bank": "4500.00",
        "Savings Account": "10000.00",
        "Cash Wallet": "500.00",
        "total": "15000.00"
    },
    "buckets": {
        "Emergency Fund": "5000.00",
        "Investments": "7000.00",
        "Daily Expenses": "3000.00",
        "total": "15000.00"
    },
    "balance": {
        "positive": "20000.00",
        "negative": "5000.00",
        "balance": "15000.00"
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
        "Salary": "5000.00",
        "Investments": "500.00",
        "Freelance": "1000.00"
    },
    "negative_categories": {
        "Groceries": "800.00",
        "Utilities": "200.00",
        "Entertainment": "300.00"
    },
    "balance": {
        "positive": "6500.00",
        "negative": "1300.00",
        "balance": "5200.00"
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
                "Salary": "5000.00"
            },
            "negative_categories": {
                "Groceries": "800.00"
            },
            "balance": {
                "positive": "5000.00",
                "negative": "800.00",
                "balance": "4200.00"
            }
        },
        // ... other months
        "12": {
            "positive_categories": {},
            "negative_categories": {},
            "balance": {
                "positive": "0.00",
                "negative": "0.00",
                "balance": "0.00"
            }
        }
    },
    "period": {
        "year": 2024
    }
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
    "years": {
        "2024": {
            "positive": "75000.00",
            "negative": "45000.00",
            "balance": "30000.00"
        },
        "2023": {
            "positive": "70000.00",
            "negative": "42000.00",
            "balance": "28000.00"
        },
        ...
    },
    "total": {
        "positive": "145000.00",
        "negative": "87000.00",
        "balance": "58000.00"
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

## Pagination

List endpoints return paginated results with:
- count: Total items
- next: Next page URL
- previous: Previous page URL
- results: Current page items
