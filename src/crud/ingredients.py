from src import schemas, crud
from jow_api import Jow, Ingredient
import requests

def get_ingredients_from_recipe(recipe_name):
    print(recipe_name)
    recipe = Jow.search(recipe_name, limit=1)[0]
    print(recipe.name)
    return [schemas.Ingredients(name=ingredients.name, 
                                quantity=ingredients.quantity, 
                                unit=ingredients.unit) for ingredients in recipe.ingredients]