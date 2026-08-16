# Backend — APIs & Real-Time Server

## Goal
Serve patient data, hospital/bed data, and connect frontend to the ML model.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

## Suggested Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/patient` | Submit new patient vitals |
| GET | `/patient/{id}/risk` | Get AI risk score for a patient |
| GET | `/hospitals/nearby` | Get nearby hospitals with bed availability |
| GET | `/dashboard/alerts` | Live feed for doctor dashboard (WebSocket) |

## Run (once app.py is built)
```bash
uvicorn app:app --reload
```

## Next Steps
1. Design DB schema: `patients`, `hospitals`, `beds`
2. Build CRUD APIs
3. Connect to ML model's `/predict` endpoint
4. Add WebSocket for real-time dashboard updates
