from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, barang
from config.db import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(barang.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Stoky API"}