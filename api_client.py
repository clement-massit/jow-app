"""Jow API client with offset support."""
import requests
import json as json_lib
from jow_api import Jow


def search_with_offset(query, limit=5, offset=0):
    """
    Search for recipes using the Jow API with offset support.
    
    Args:
        query (str): Search query
        limit (int): Number of results to return
        offset (int): Offset for pagination
        
    Returns:
        list: List of JowResult objects
    """
    # Headers and params similar to Jow API
    option_headers = {
        "accept": "*/*",
        "accept-language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    option_params = {
        "start": offset,
        "availabilityZoneId": "FR",
        "query": query,
        "limit": limit
    }
    
    post_headers = {
        "accept": "application/json",
        "accept-language": "fr",
        "content-type": "application/json",
        "x-jow-withmeta": "1",
    }
    
    post_params = {
        "start": str(offset),
        "availabilityZoneId": "FR",
        "query": query,
        "limit": limit
    }
    
    search_url = "https://api.jow.fr/public/recipe/quicksearch"
    
    # OPTIONS request
    response = requests.options(search_url, headers=option_headers, params=option_params)
    if response.status_code != 204:
        raise ValueError("ERROR IN OPTION REQUEST")
    
    # POST request
    response = requests.post(search_url, headers=post_headers, params=post_params, data="{}")
    if response.status_code != 200:
        raise ValueError("ERROR IN POST REQUEST")
    
    response_json = json_lib.loads(response.text)
    
    # Parse results using Jow's internal methods
    recipes = []
    for recipe_data in response_json.get('data', {}).get('content', []):
        recipes.append(Jow._Jow__get(recipe_data))
    
    return recipes
