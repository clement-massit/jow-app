from src import schemas, crud
from jow_api import Jow, Ingredient
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('jow.db')
    conn.row_factory = sqlite3.Row  # Pour retourner des résultats sous forme de dictionnaire
    return conn


def get_recipe(name: str):
    recipe = Jow.search(name, limit=1)[0]
    return schemas.Recipe(
        id=recipe.id,
        name=recipe.name,
        url=recipe.url,
        description=recipe.description,
        preparation_time=recipe.preparationTime,
        cooking_time=recipe.cookingTime,
        preparation_extra_time_per_cover=recipe.preparationExtraTimePerCover,
        covers_count=recipe.coversCount,
        ingredients=[schemas.Ingredients(name=ingredient.name, 
                                         quantity=ingredient.quantity,
                                         unit=ingredient.unit) for ingredient in recipe.ingredients]
        
    )

def get_recipes(name: str, limit:int):
    recipes = Jow.search(to_search=name, limit=limit)
    print(recipes)
    list_recipes = [
        schemas.Recipe(
        id=recipe.id,
        name=recipe.name,
        url=recipe.url,
        description=recipe.description,
        preparation_time=recipe.preparationTime,
        cooking_time=recipe.cookingTime,
        preparation_extra_time_per_cover=recipe.preparationExtraTimePerCover,
        covers_count=recipe.coversCount,
        ingredients=[schemas.Ingredients(name=ingredient.name, 
                                         quantity=ingredient.quantity,
                                         unit=ingredient.unit) for ingredient in recipe.ingredients]
        
    ) for recipe in recipes]
    for recipe in recipes:
        add_to_own_recipes(recipe)
    return list_recipes

def add_to_own_recipes(recipe: schemas.Recipe):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO Recipe (
                       id,
                       name,
                       url,
                       description,
                       preparation_time,
                       cooking_time,
                       preparation_extra_time_per_cover,
                       covers_count) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    
                   ''', (recipe.id,
                         recipe.name,
                         recipe.url,
                         recipe.description,
                         recipe.preparationTime,
                         recipe.cookingTime,
                         recipe.preparationExtraTimePerCover,
                         recipe.coversCount,))
    conn.commit()
    conn.close()
    

def get_own_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()
    r = cursor.execute("SELECT * FROM Recipes").fetchall()
    conn.close()
    return r


