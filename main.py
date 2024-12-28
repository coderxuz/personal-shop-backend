from fastapi import FastAPI

from app.api import auth

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"running"}

app.include_router(auth.router)