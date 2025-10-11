import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Initialize Flask App ---
app = Flask(__name__)

# --- Configuration ---
logging.basicConfig(level=logging.INFO)
CORS(app)

try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    logging.error(f"Failed to configure Gemini API: {e}")

# --- NEW: Advanced Calorie Calculator ---
def calculate_calories(weight, height, age, gender, activity_level):
    # Using Mifflin-St Jeor Equation for BMR
    if gender.lower() == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else: # female
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Activity multipliers (maps frontend 0-4 to standard values)
    activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
    tdee = bmr * activity_multipliers[activity_level] # This is maintenance calories

    calories = {
        'maintain': round(tdee),
        'mildLoss': round(tdee - 250),
        'weightLoss': round(tdee - 500),
        'extremeLoss': round(tdee - 750)
    }
    
    # Calculate projected weekly loss (1 kg fat = ~7700 calories)
    projections = {
        'maintain': "0 kg/week",
        'mildLoss': f"~-{(250 * 7) / 7700:.2f} kg/week",
        'weightLoss': f"~-{(500 * 7) / 7700:.2f} kg/week",
        'extremeLoss': f"~-{(750 * 7) / 7700:.2f} kg/week"
    }

    return calories, projections

# --- Helper Functions ---
def get_bmi_status(bmi):
    if bmi < 18.5: return "Underweight"
    if 18.5 <= bmi < 25: return "Normal"
    if 25 <= bmi < 30: return "Overweight"
    return "Obesity"

def calculate_bmi(weight, height):
    if height == 0: return 0
    return round(float(weight) / ((float(height) / 100) ** 2), 2)

# In app.py, replace the old create_diet_prompt function with this one.

def create_diet_prompt(user_inputs, calories):
    meal_names = ["Breakfast", "Lunch", "Dinner"]
    meals_per_day = user_inputs['mealsPerDay']
    if meals_per_day == 4:
        meal_names.insert(2, "Afternoon Snack")
    elif meals_per_day >= 5:
        meal_names.insert(1, "Morning Snack")
        meal_names.insert(3, "Afternoon Snack")

    meal_options_prompt = ""
    for meal_name in meal_names:
        meal_options_prompt += f"""
          {{
            "mealType": "{meal_name}", 
            "options": [
              {{ 
                "name": "A short, common dish name", 
                "calories": "<Integer>", "protein": "<Number>g", "fat": "<Number>g",
                "carbs": "<Number>g", "saturatedFat": "<Number>g", "sodium": "<Number>mg",
                "fiber": "<Number>g", "sugar": "<Number>g",
                "imageUrl": "A relevant placeholder image URL from 'https://placehold.co/600x400'",
                "ingredients": ["Ingredient 1", "Ingredient 2", "Ingredient 3"],
                "instructions": ["Step 1", "Step 2", "Step 3"]
              }},
              {{ 
                "name": "Another short, common dish name", 
                "calories": "<Integer>", "protein": "<Number>g", "fat": "<Number>g",
                "carbs": "<Number>g", "saturatedFat": "<Number>g", "sodium": "<Number>mg",
                "fiber": "<Number>g", "sugar": "<Number>g",
                "imageUrl": "A relevant placeholder image URL from 'https://placehold.co/600x400'",
                "ingredients": ["Ingredient A", "Ingredient B", "Ingredient C"],
                "instructions": ["Step A", "Step B", "Step C"]
              }},
              {{ 
                "name": "A third short, common dish name", 
                "calories": "<Integer>", "protein": "<Number>g", "fat": "<Number>g",
                "carbs": "<Number>g", "saturatedFat": "<Number>g", "sodium": "<Number>mg",
                "fiber": "<Number>g", "sugar": "<Number>g",
                "imageUrl": "A relevant placeholder image URL from 'https://placehold.co/600x400'",
                "ingredients": ["Ingredient X", "Ingredient Y", "Ingredient Z"],
                "instructions": ["Step X", "Step Y", "Step Z"]
              }}
            ]
          }},"""
    meal_options_prompt = meal_options_prompt.rstrip(',')

    prompt = f"""
    You are an expert AI that creates healthy diet plans based on common, everyday Indian home-style food.
    The total calories for the day should be around {calories['weightLoss']} kcal.
    
    **CRITICAL INSTRUCTIONS:**
    1. Your entire response MUST be a single, valid JSON object.
    2. Focus on food that is commonly eaten in Indian homes.
    3. Recipe names MUST be short and simple (e.g., "Rajma Chawal").
    4. You MUST provide exactly three distinct recipe options for each mealType.

    **User Data:**
    - Age: {user_inputs['age']}, Gender: {user_inputs['gender']}, Goal: {user_inputs['weightLossPlan']}

    **JSON Structure to Follow:**
    {{
      "mealPlan": [
          {meal_options_prompt}
      ]
    }}
    """
    return prompt
def make_gemini_call(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro-latest')
        response = model.generate_content(prompt)
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(response_text)
    except Exception as e:
        logging.error(f"Error calling Gemini or parsing JSON: {e}")
        raise

# --- UPDATED: API Route to use new calculators ---
@app.route('/api/get_full_plan', methods=['POST'])
def get_full_plan():
    try:
        data = request.get_json()
        logging.info(f"Received data for diet plan: {data}")
        
        user_inputs = {
            'age': int(data.get('age')), 
            'height': float(data.get('height')),
            'weight': float(data.get('weight')), 
            'gender': data.get('gender'),
            'activityLevel': int(data.get('activityLevel')),
            'weightLossPlan': data.get('weightLossPlan'),
            'mealsPerDay': int(data.get('mealsPerDay'))
        }
        
        # 1. Perform all calculations first
        bmi_value = calculate_bmi(user_inputs['weight'], user_inputs['height'])
        bmi_status = get_bmi_status(bmi_value)
        calories, projections = calculate_calories(
            user_inputs['weight'], user_inputs['height'], user_inputs['age'], 
            user_inputs['gender'], user_inputs['activityLevel']
        )
        
        # 2. Get meal plan from AI
        prompt = create_diet_prompt(user_inputs, calories)
        logging.info("Generating diet plan from Gemini API...")
        plan_data = make_gemini_call(prompt) # This will return {"mealPlan": [...]}
        
        # 3. Combine calculated data with AI data for the final response
        final_response = {
            "bmi": {"value": bmi_value, "category": bmi_status},
            "calories": {
                "maintain": {"value": calories['maintain'], "projection": projections['maintain']},
                "mildLoss": {"value": calories['mildLoss'], "projection": projections['mildLoss']},
                "weightLoss": {"value": calories['weightLoss'], "projection": projections['weightLoss']},
                "extremeLoss": {"value": calories['extremeLoss'], "projection": projections['extremeLoss']}
            },
            "mealPlan": plan_data.get("mealPlan", [])
        }
        
        logging.info("Successfully generated and parsed full plan.")
        return jsonify(final_response)
        
    except Exception as e:
        logging.error(f"An unexpected error occurred in get_full_plan: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

if __name__ == '__main__':
    app.run(debug=True)