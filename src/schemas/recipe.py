from typing import Optional, Dict
from pydantic import BaseModel
from .shared import ContextCheckingBaseModel
 
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

class Ingredients(ContextCheckingBaseModel):
    """
    name: str
    quantity: float
    unit: str
    """
    name: str
    quantity: float
    unit: str
    
class Recipe(ContextCheckingBaseModel):
    """
    id: str
    name: str
    url: str
    description: str
    preparation_time: int
    cooking_time: int
    preparation_extra_time_per_cover: int
    covers_count: int
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
    
