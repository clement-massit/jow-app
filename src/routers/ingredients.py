from fastapi import APIRouter, Depends
from src import crud, schemas

router = APIRouter(tags=["Ingredients"])
@router.get("/recipe/{recipe_id}/ingredients", response_model=list[schemas.Ingredients], tags=['Ingredients'])
def get_ingredients_from_recipe(recipe_id:str):
    return crud.get_ingredients_from_recipe(recipe_id)
