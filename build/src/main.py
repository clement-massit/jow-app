from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from src.routers import recipe




    
app = FastAPI()

app.include_router(recipe.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root(request: Request):
    return {"message": 'Welcome to custom JOW app', "root_path": request.scope.get("root_path")}
