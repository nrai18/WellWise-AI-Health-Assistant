"""
FatSecret API Integration for Food Images
"""
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("FATSECRET_CLIENT_ID")
CLIENT_SECRET = os.getenv("FATSECRET_CLIENT_SECRET")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
SEARCH_URL = "https://platform.fatsecret.com/rest/server.api"

def get_access_token():
    """Get OAuth 2.0 access token from FatSecret."""
    if not CLIENT_ID or not CLIENT_SECRET:
        return None
    
    # Create Basic Auth header
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode('ascii')
    
    headers = {
        'Authorization': f'Basic {base64_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'scope': 'basic'
    }
    
    try:
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception as e:
        print(f"FatSecret auth error: {e}")
        return None

def search_food_image(food_name):
    """Search for food and get image URL from FatSecret."""
    token = get_access_token()
    if not token:
        return None
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'method': 'foods.search',
        'search_expression': food_name,
        'format': 'json',
        'max_results': 1
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract image URL if available
        foods = data.get('foods', {}).get('food', [])
        if foods and len(foods) > 0:
            food = foods[0] if isinstance(foods, list) else foods
            # FatSecret doesn't always have images, so we construct a fallback
            food_id = food.get('food_id')
            if food_id:
                return f"https://platform.fatsecret.com/api/static/food/image/{food_id}"
        
        return None
    except Exception as e:
        print(f"FatSecret search error: {e}")
        return None

def get_food_image_for_dish(dish_name):
    """
    Get a food image URL for a given dish name.
    Returns the image URL or None if not found.
    """
    # Try to get from FatSecret
    image_url = search_food_image(dish_name)
    
    # If FatSecret doesn't work, return None (will use emoji fallback in frontend)
    return image_url

# Test function
if __name__ == "__main__":
    test_dish = "biryani"
    print(f"Searching for: {test_dish}")
    image_url = get_food_image_for_dish(test_dish)
    if image_url:
        print(f"Found image: {image_url}")
    else:
        print("No image found, will use emoji fallback")
