import requests
from bs4 import BeautifulSoup
from src import schemas


def get_img_from_recipe_url(recipeUrl,recipeName):
    # URL de la page contenant l'image
    
    baseUrl = "https://jow.fr"
    # Récupération de la page HTML
    response = requests.get(recipeUrl)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver l'image (par exemple la première balise <img>)
        img_tag = soup.find('img',alt=recipeName)
        
        if img_tag:
            # URL de l'image
            img_url = baseUrl + img_tag['src']
            return schemas.ImgUrl(imgUrl=img_url)
            # Si l'URL de l'image est relative, la rendre absolue
        else:
            print("Aucune balise img trouvée sur la page.")
            return None
    else:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return None