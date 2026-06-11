# main.py
# Entry point for the FastAPI app
# this is where everything comes together

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import Offer, Transaction, Payment, Message

# create all database tables if they don't exist yet
# this reads all our models and builds the tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Waste Management & Recycling Hub",
    description="A platform connecting waste sellers with recyclers across Kenya",
    version="1.0.0"
)

# allow the React frontend to talk to this API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# basic health check so we can confirm the server is running
@app.get("/")
def root():
    return {"message": "Waste Hub API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}