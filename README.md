# Waste Management & Recycling Hub — Backend API

FastAPI backend for the Waste Management & Recycling Hub platform. Connects waste sellers with recyclers across Kenya.

## Features
- Offer management (create, accept, reject, counter)
- Transaction lifecycle tracking
- Mock M-Pesa payment processing
- Seller/recycler messaging

## Tech Stack
- FastAPI + Python
- SQLAlchemy ORM
- SQLite (development) / PostgreSQL (production)
- JWT Authentication (utility ready, not yet wired to routes)
- Docker

## Getting Started

### Local Development
```bash
git clone https://github.com/keithkamau/ecoflow-proj-backend
cd ecoflow-proj-backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

API runs at http://localhost:8000  
Swagger docs at http://localhost:8000/docs

### Docker
```bash
docker-compose up -d
```

## Running Tests
```bash
pytest tests/ -v --cov=app
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Root health check |
| GET | /health | Health check |
| **Offers** | | |
| POST | /api/v1/offers/ | Create an offer |
| GET | /api/v1/offers/ | List all offers |
| GET | /api/v1/offers/{id} | Get a single offer |
| PUT | /api/v1/offers/{id} | Accept / reject / counter an offer |
| DELETE | /api/v1/offers/{id} | Delete a pending offer |
| **Transactions** | | |
| POST | /api/v1/transactions/ | Create a transaction from an accepted offer |
| GET | /api/v1/transactions/ | List all transactions |
| GET | /api/v1/transactions/{id} | Get a single transaction |
| PUT | /api/v1/transactions/{id} | Update transaction status |
| **Payments** | | |
| POST | /api/v1/payments/ | Process a payment |
| GET | /api/v1/payments/ | List all payments |
| GET | /api/v1/payments/{transaction_id} | Get payment for a transaction |
| **Messages** | | |
| POST | /api/v1/messages/ | Send a message |
| GET | /api/v1/messages/{offer_id} | Get conversation for an offer |
| PUT | /api/v1/messages/{message_id}/read | Mark message as read |

## Branch
`feature/offers-transactions`


