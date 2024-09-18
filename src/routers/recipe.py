from fastapi import APIRouter, Depends
from src import crud, schemas


router = APIRouter(tags=["Recipe"])
@router.post("/recipe", response_model=schemas.Recipe, tags=['Recipe'])
def get_recipe(recipe:schemas.RecipeAsk):
    return crud.get_recipe(recipe.name)


@router.post("/recipes", response_model=list[schemas.Recipe], tags=['Recipe'])
def get_recipes(recipes:schemas.RecipesAsk):
    return crud.get_recipes(recipes.name, recipes.limit)


@router.get("/own/recipes")
def get_own_recipes():
    return dict(crud.get_own_recipes())

@router.post("/recipes/{recipe_id}")
def add_to_own_recipes(recipe_id:str):
    
    print(recipe_id)
    # crud.add_to_own_recipes(recipe)
    
    
