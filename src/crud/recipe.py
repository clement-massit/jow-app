from src import schemas, crud
from jow_api import Jow, Ingredient
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('jow.db')
    # conn.row_factory = sqlite3.Row  # Pour retourner des résultats sous forme de dictionnaire
    return conn


def get_recipe_from_jow(name: str):
    recipe = Jow.search(name, limit=1)[0]
    return schemas.Recipe(
        id=recipe.id,
        name=recipe.name,
        url=recipe.url,
        description=recipe.description,
        preparationTime=recipe.preparationTime,
        cookingTime=recipe.cookingTime,
        preparationExtraTimePerCover=recipe.preparationExtraTimePerCover,
        coversCount=recipe.coversCount,
        ingredients=[schemas.Ingredients(name=ingredient.name, 
                                         quantity=ingredient.quantity,
                                         unit=ingredient.unit) for ingredient in recipe.ingredients]
        
    )

def get_recipes_from_jow(name: str, limit:int):
    recipes = Jow.search(name, limit)
    list_recipes = [
        schemas.Recipe(
        id=recipe.id,
        name=recipe.name,
        url=recipe.url,
        description=recipe.description,
        preparationTime=recipe.preparationTime,
        cookingTime=recipe.cookingTime,
        preparationExtraTimePerCover=recipe.preparationExtraTimePerCover,
        coversCount=recipe.coversCount,
        ingredients=[schemas.Ingredients(name=ingredient.name, 
                                         quantity=ingredient.quantity,
                                         unit=ingredient.unit) for ingredient in recipe.ingredients]
        
    ) for recipe in recipes]

    # for recipe in list_recipes:
    #     print(recipe)
    #     add_to_own_recipes(recipe)
    return list_recipes

def add_to_own_recipes(recipe: schemas.Recipe):
    conn = sqlite3.connect('jow.db')
    cursor = conn.cursor()
    
    sql = '''INSERT or REPLACE INTO Buff_recipes 
                   (id,
                    name,
                    url,
                    description,
                    preparationTime,
                    cookingTime,
                    preparationExtraTimePerCover,
                    coversCount) VALUES (?,?,?,?,?,?,?,?);

                   '''
    cursor.execute(sql,(str(recipe.id),
                        str(recipe.name),
                        str(recipe.url),
                        str(recipe.description),
                        recipe.preparationTime,
                        recipe.cookingTime,
                        recipe.preparationExtraTimePerCover,
                        recipe.coversCount,))
    conn.commit()
    for ingredient in recipe.ingredients:
        cursor.execute('''
        INSERT INTO Ingredients (name,quantity,unit)
        VALUES (?,?,?) RETURNING *;
        ''', (ingredient.name, ingredient.quantity, ingredient.unit))
        ingredient_added =cursor.fetchone()
        print(ingredient_added)

        cursor.execute('''
        INSERT INTO recipe_ingredients (recipeId, ingredientId) 
        VALUES (?,?);
        ''', (recipe.id, ingredient_added[0]))

    conn.commit()
   
    

def get_own_recipes():
    conn = sqlite3.connect('jow.db')
    cursor = conn.cursor()
    recipes = cursor.execute("""SELECT br.*,
     GROUP_CONCAT(i.name || ' (' || i.quantity || ' ' || i.unit || ')', ', ') AS ingredients_list

                             FROM Buff_recipes br 
                             JOIN recipe_ingredients ri ON br.id = ri.recipeId
                             JOIN Ingredients i ON ri.ingredientId = i.id
                             GROUP BY br.name""")
   
    rows = cursor.fetchall()

    # Traitement des résultats
    recipes = []
    for row in rows:
        recipe_data = {
            "id": row[0],
            "name": row[1],
            "url": row[2],
            "description": row[3],
            "preparationTime": row[4],
            "cookingTime": row[5],
            "preparationExtraTimePerCover": row[6] or 0,  # Valeur par défaut
            "coversCount": row[7],
            "ingredients": row[8].split(", ") if row[8] else []  # Liste d'ingrédients
        }
        
        # Création de l'objet Recipe
        recipe = schemas.Recipe(**recipe_data)
        recipes.append(recipe)

  
    return recipes
   


def request():
    conn = sqlite3.connect('jow.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Buff_recipes''')
    res = cursor.fetchall()
    print(res)
    cursor.execute('''SELECT * FROM Ingredients''')
    res = cursor.fetchall()
    print(res)
    cursor.execute('''SELECT * FROM recipe_ingredients''')
    res = cursor.fetchall()
    print(res)