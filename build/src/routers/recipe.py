from fastapi import APIRouter, Depends
from src import crud, schemas


router = APIRouter(tags=["Recipe"])
@router.post("/recipe", response_model=schemas.Recipe, tags=['Recipe'])
def get_recipe(recipe:schemas.RecipeAsk):
    return crud.get_recipe_from_jow(recipe.name)


@router.post("/recipes", response_model=list[schemas.Recipe], tags=['Recipe'])
def get_recipes(recipes:schemas.RecipesAsk):
    return crud.get_recipes_from_jow(recipes.name, recipes.limit)


@router.get("/own/recipes")
def get_own_recipes():
    # print(crud.request())
    return crud.get_own_recipes()

@router.post("/recipes/{recipe_name}")
def add_to_own_recipes(recipe_name:str):
    recipe = crud.get_recipe_from_jow(recipe_name)
    # print(recipe_name)
    crud.add_to_own_recipes(recipe)
    
    
