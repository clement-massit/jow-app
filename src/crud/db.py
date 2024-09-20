import sqlite3
import os

conn = sqlite3.connect('jow.db')

cursor = conn.cursor()
# cursor.execute('''DROP TABLE recipe_ingredients''')
# cursor.execute('''DROP TABLE Ingredients''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Buff_recipes(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    preparationTime INT ,
    cookingTime INT ,
    preparationExtraTimePerCover INT ,
    coversCount INT
);               
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Ingredients(
    recipeId INTEGER NOT NULL,
    name TEXT NOT NULL,
    quantity FLOAT8,
    unit TEXT NOT NULL,
    FOREIGN KEY (recipeId) REFERENCES Buff_recipes(id),
    PRIMARY KEY (name,recipeId)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    recipeId TEXT,
    nameIngredient Name,
    FOREIGN KEY (recipeId) REFERENCES Buff_recipes(id),
    FOREIGN KEY (nameIngredient) REFERENCES Ingredients(name),
    PRIMARY KEY (recipeId, nameIngredient)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS List_ingredients(
    id SERIAL PRIMARY KEY,
    nameIngredient TEXT NOT NULL,
    id_recipe TEXT NOT NULL,
    FOREIGN KEY (nameIngredient) REFERENCES Ingredients(name),
    FOREIGN KEY (id_recipe) REFERENCES Own_Recipe(id)
);
''')




# Insérer des données factices
# cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)")
# cursor.execute("""INSERT INTO Buff_recipes (id,
#                        name,
#                        url,
#                        description,
#                        preparationTime,
#                        cookingTime,
#                        preparationExtraTimePerCover,
#                        coversCount) 
#                VALUES ('id_test',
#                'name_test',
#                'http://google.com', 
#                'decription_test',
#                5,
#                20,
#                0,
#                4);""")


# cursor.execute('''
# INSERT INTO Ingredients (id,name,quantity,unit)
# VALUES (1,'Farine', 0.5, 'Kg');
# ''')
# cursor.execute('''
# INSERT INTO Ingredients (id,name,quantity,unit)
# VALUES (2,'Sucre', 0.1, 'Kg');
# ''')
# cursor.execute('''
# INSERT INTO recipe_ingredients (recipeId, ingredientId) 
# VALUES ('id_test', 1);

# ''')
# cursor.execute('''
# INSERT INTO recipe_ingredients (recipeId, ingredientId) 
# VALUES ('id_test', 2);

# ''')
# conn.commit()
