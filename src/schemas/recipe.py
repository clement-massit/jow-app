from typing import Optional, Dict
from pydantic import BaseModel
 
class RecipeAsk(BaseModel):
    """
    Attributes
    ----------
    name: str

    """
    name: str

class RecipesAsk(BaseModel):
    """
    Attributes
    ----------
    name: str
    limit: int

    """
    name: str
    limit: int

class Ingredients(BaseModel):
    """
    name: str
    quantity: float
    unit: str
    """
    name: str
    quantity: float
    unit: str
    
class Recipe(BaseModel):
    """
    id: str
    name: str
    url: str
    description: str
    preparationTime: int
    cookingTime: int
    preparationExtraTimePerCover: int
    coversCount: int
    ingredients: list
    """
    id: str
    name: str
    url: str
    description: str
    preparationTime: Optional[int]=0
    cookingTime: Optional[int]=0
    preparationExtraTimePerCover: Optional[int]=0
    coversCount: Optional[int]=0
    ingredients: Optional[list]
    
class RecipeUrl(BaseModel):
    """"""
    recipeUrl: str

        
class ImgUrl(BaseModel):
    """"""
    imgUrl: str