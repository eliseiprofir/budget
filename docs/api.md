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
    "count": 125,
    "next": "https://domain.com/api/transactions/?page=2",
    "previous": null,
    "results": [
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
        },
        // ... more transactions
    ]
}
```

#### Pagination
Transactions are paginated with 50 items per page by default. You can control pagination with these parameters:

- `page`: Page number (starts at 1)
- `page_size`: Number of items per page (max 100)

Example:
```http
GET /api/transactions/?page=2&page_size=20
```

#### Filtering
You can filter transactions using these parameters:

- `category`: Filter by category ID
- `date`: Filter by specific date (YYYY-MM-DD)
- `amount`: Filter by exact amount
- `location`: Filter by location ID
- `bucket`: Filter by bucket ID
- `search`: Search in description field

Example:
```http
GET /api/transactions/?category=550e8400-e29b-41d4-a716-446655440000&search=grocery
```

#### Ordering
You can order transactions using the `ordering` parameter:

- `ordering=date`: Order by date (ascending)
- `ordering=-date`: Order by date (descending)
- `ordering=amount`: Order by amount (ascending)
- `ordering=-amount`: Order by amount (descending)

Example:
```http
GET /api/transactions/?ordering=-date
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

### Monthly Analytics
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

### Yearly Analytics
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

### Historical Analytics
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

### Cache Status Endpoints
Each analytics endpoint has a corresponding cache status endpoint that provides information about the cached data:

```http
GET /api/analytics-current/cache-status/
GET /api/analytics-monthly/cache-status/
GET /api/analytics-yearly/cache-status/
GET /api/analytics-historical/cache-status/
```

Response example:
```json
{
    "is_cached": true,
    "cache_key": "current_report_01477667-aa35-4d40-9730-9190037fd6d8",
    "ttl_seconds": 3540,
    "expires_at": "2024-05-15T15:30:45Z",
    "generated_at": "2024-05-15T14:30:45Z"
}
```

For specific time periods, you can check cache status using:

```http
GET /api/analytics-monthly/cache-status/YYYY-MM
GET /api/analytics-yearly/cache-status/YYYY
```

Examples:
```http
GET /api/analytics-monthly/cache-status/2024-05
GET /api/analytics-yearly/cache-status/2024
```

Response example for a specific period:
```json
{
    "is_cached": true,
    "cache_key": "monthly_report_01477667-aa35-4d40-9730-9190037fd6d8_2024_5",
    "month": 5,
    "year": 2024,
    "ttl_seconds": 3540,
    "expires_at": "2024-05-15T15:30:45Z",
    "generated_at": "2024-05-15T14:30:45Z"
}
```

Notes:
- Analytics data is cached for 1 hour by default
- When requesting analytics data, if it's not in cache, it will be generated on-demand and cached
- Additionally, an asynchronous task is triggered to refresh the cache in the background
- This approach ensures fast response times while keeping data up-to-date
- Cache keys are user-specific, ensuring data isolation between users
- Invalid date formats will return a 400 Bad Request response

## Common Headers

All requests require:
```http
Authorization: Bearer <your_access_token>
Content-Type: application/json
```

## Response Codes

- 200: Success - Request was successful
- 201: Created - Resource was successfully created
- 400: Bad Request - Invalid request format or validation error
- 401: Unauthorized - Authentication credentials were not provided or are invalid
- 403: Forbidden - You don't have permission to access this resource
- 404: Not Found - The requested resource does not exist
- 405: Method Not Allowed - The HTTP method is not supported for this endpoint
- 429: Too Many Requests - Rate limit exceeded
- 500: Server Error - An error occurred on the server
