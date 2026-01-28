"""Recipe adaptation logic for adjusting servings."""


def adapt_for_nb_people(recipe, nb_personnes=4):
    """
    Adapt a recipe for a specific number of people.
    
    Args:
        recipe: JowResult object
        nb_personnes (int): Number of people to adapt for
        
    Returns:
        JowResult: Modified recipe object with adapted quantities
    """
    base_covers = getattr(recipe, 'coversCount', 2)
    
    # Adapt preparation time
    extra_time_per_cover = getattr(recipe, 'preparationExtraTimePerCover', 0)
    if extra_time_per_cover is None:
        extra_time_per_cover = 0
    
    # Handle None preparationTime
    if recipe.preparationTime is None:
        recipe.preparationTime = 0
   
    recipe.preparationTimeAdapted = recipe.preparationTime + (extra_time_per_cover * (nb_personnes - base_covers))
    
    # Adapt ingredients
    # IMPORTANT: API returns quantityPerCover (quantity PER PERSON)
    # So we multiply by nb_personnes directly to get total quantity
    for ing in getattr(recipe, 'ingredients', []):
        if ing.quantity:  # Avoid 0 or None
            # ing.quantity is the quantity PER PERSON
            # Total quantity = quantity per person × number of people
            ing.quantityAdapted = ing.quantity * nb_personnes
            ing.quantityAdapted = round(ing.quantityAdapted, 2)
        else:
            ing.quantityAdapted = 0
    
    recipe.adaptedFor = nb_personnes
    recipe.adaptationFactor = nb_personnes / base_covers if base_covers else 1
    return recipe
