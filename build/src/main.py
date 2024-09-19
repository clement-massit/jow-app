from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List
from src.routers import recipe



    
app = FastAPI()

app.include_router(recipe.router)


@app.get("/")
def root(request: Request):
    return {"message": 'Welcome to custom JOW app', "root_path": request.scope.get("root_path")}
