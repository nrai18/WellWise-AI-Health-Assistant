# --- Imports ---
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai
import email_utils

# Load environment variables
load_dotenv()

# --- Initialize Flask App ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super-secret-key')

# Enable CORS so frontend can call backend
CORS(app)

# Configure Gemini API
try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    logging.error(f"Failed to configure Gemini API: {e}")

# --- Helper Functions ---

def calculate_bmi(weight, height):
    if height == 0: return 0
    return round(float(weight) / ((float(height)/100) ** 2), 2)

def get_bmi_status(bmi):
    if bmi < 18.5: return "Underweight"
    if 18.5 <= bmi < 25: return "Normal"
    if 25 <= bmi < 30: return "Overweight"
    return "Obesity"

def calculate_calories(weight, height, age, gender, activity_level):
    if gender.lower() == 'male':
        bmr = (10*weight) + (6.25*height) - (5*age) + 5
    else:
        bmr = (10*weight) + (6.25*height) - (5*age) - 161

    activity_multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
    tdee = bmr * activity_multipliers[activity_level]

    calories = {
        'maintain': round(tdee),
        'mildLoss': round(tdee - 250),
        'weightLoss': round(tdee - 500),
        'extremeLoss': round(tdee - 750)
    }

    projections = {
        'maintain': "0 kg/week",
        'mildLoss': f"~-{(250*7)/7700:.2f} kg/week",
        'weightLoss': f"~-{(500*7)/7700:.2f} kg/week",
        'extremeLoss': f"~-{(750*7)/7700:.2f} kg/week"
    }

    return calories, projections

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
              {{ "name": "Dish 1", "description": "Brief appetizing description", "calories": 300, "protein": 15, "fat": 10, "carbs": 40, "saturatedFat": 3, "sodium": 500, "fiber": 5, "sugar": 6, "ingredients": ["Ingredient1", "Ingredient2"], "instructions": ["Step1", "Step2"] }},
              {{ "name": "Dish 2", "description": "Brief appetizing description", "calories": 350, "protein": 20, "fat": 12, "carbs": 45, "saturatedFat": 4, "sodium": 600, "fiber": 6, "sugar": 7, "ingredients": ["IngredientA", "IngredientB"], "instructions": ["StepA", "StepB"] }},
              {{ "name": "Dish 3", "description": "Brief appetizing description", "calories": 400, "protein": 18, "fat": 15, "carbs": 50, "saturatedFat": 5, "sodium": 700, "fiber": 7, "sugar": 8, "ingredients": ["IngredientX", "IngredientY"], "instructions": ["StepX", "StepY"] }}
            ]
          }},
        """
    meal_options_prompt = meal_options_prompt.rstrip(',')

    prompt = f"""
    You are an AI that creates Indian diet plans. Total calories: {calories['weightLoss']} kcal.
    For each meal, provide 3 diverse, authentic Indian dish options with REAL names and descriptions.
    Make the descriptions appetizing and specific to the dish.
    DO NOT include imageUrl field - we'll use text descriptions only.
    Provide JSON in this format: {{ "mealPlan": [ {meal_options_prompt} ] }}
    """
    return prompt

def make_gemini_call(prompt):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(response_text)
    except Exception as e:
        logging.error(f"Error calling Gemini or parsing JSON: {e}")
        # fallback dummy response
        return {"mealPlan": []}

# --- API Route ---
@app.route('/api/get_full_plan', methods=['POST'])
def get_full_plan():
    try:
        data = request.get_json()
        user_inputs = {
            'age': int(data.get('age')),
            'height': float(data.get('height')),
            'weight': float(data.get('weight')),
            'gender': data.get('gender'),
            'activityLevel': int(data.get('activityLevel')),
            'weightLossPlan': data.get('weightLossPlan'),
            'mealsPerDay': int(data.get('mealsPerDay'))
        }

        bmi_value = calculate_bmi(user_inputs['weight'], user_inputs['height'])
        bmi_status = get_bmi_status(bmi_value)
        calories, projections = calculate_calories(
            user_inputs['weight'], user_inputs['height'], user_inputs['age'], 
            user_inputs['gender'], user_inputs['activityLevel']
        )

        prompt = create_diet_prompt(user_inputs, calories)
        plan_data = make_gemini_call(prompt)

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
        return jsonify(final_response)

    except Exception as e:
        logging.error(f"Error in get_full_plan: {e}")
        return jsonify({"error": "Server error"}), 500
    
# ==============================================================
# 🏋️ EXERCISE HUB ROUTE (Add below your existing diet code)
# ==============================================================

@app.route('/api/get_exercise_plan', methods=['POST'])
def get_exercise_plan():
    try:
        data = request.get_json()

        fitness_level = data.get("fitnessLevel", "Beginner")
        primary_goal = data.get("primaryGoal", "Weight Loss")
        equipment = data.get("availableEquipment", {})
        days = int(data.get("workoutDaysPerWeek", 3))
        time = int(data.get("timePerSession", 45))

        prompt = f"""
        You are a certified fitness coach.
        Create a {days}-day structured weekly workout plan based on:
        - Fitness Level: {fitness_level}
        - Goal: {primary_goal}
        - Equipment: {equipment}
        - Days per week: {days}
        - Duration per session: {time} minutes

        Each day must include:
        - day (e.g., Monday)
        - focus (e.g., Chest & Triceps)
        - exercises: list of dicts with "name", "sets", "reps", "rest", "equipment"
        - intensity: Low/Medium/High
        - icon: short emoji (💪, 🧘, 🏃 etc.)

        Return strictly JSON in this structure:
        {{
          "weeklyPlan": [
            {{
              "day": "Monday",
              "focus": "Upper Body",
              "exercises": [
                {{
                  "name": "Push-ups",
                  "sets": 3,
                  "reps": 12,
                  "rest": "60s",
                  "equipment": "Bodyweight"
                }}
              ],
              "intensity": "Medium",
              "icon": "💪"
            }}
          ]
        }}
        """

        plan_data = make_gemini_call(prompt)

        # Ensure fallback structure if Gemini fails
        if "weeklyPlan" not in plan_data:
            plan_data = {"weeklyPlan": []}

        return jsonify(plan_data), 200

    except Exception as e:
        logging.error(f"Error in get_exercise_plan: {e}", exc_info=True)
        return jsonify({"weeklyPlan": []}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    """User signup endpoint - checks if account exists, creates if not"""
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WellWise-AI-Engine-main'))
        import database as db
        import bcrypt
        
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not name or len(name) < 2:
            return jsonify({"status": "error", "message": "Name must be at least 2 characters"}), 400
        if not email or '@' not in email:
            return jsonify({"status": "error", "message": "Valid email required"}), 400
        if not password or len(password) < 6:
            return jsonify({"status": "error", "message": "Password must be at least 6 characters"}), 400
        
        # Sanitize username - replace spaces with underscores
        username_sanitized = name.replace(' ', '_')
        
        # Check if user exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({
                "status": "error",
                "message": "Account already exists. Please login instead."
            }), 409
        
        # Hash password and create user
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Save with sanitized username but return original name
        result = db.save_user(email, username_sanitized, password_hash)
        
        if result.get("status") == "success":
            # Send welcome email
            try:
                from datetime import datetime
                device_info = {
                    'browser': request.headers.get('User-Agent', 'Unknown')[:50],
                    'os': 'Windows' if 'Windows' in request.headers.get('User-Agent', '') else 'Other',
                    'ip': request.remote_addr or 'Unknown',
                    'location': 'Unknown',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'device_id': request.headers.get('User-Agent', 'Unknown')[-20:]
                }
                email_utils.send_signup_notification(email, name, device_info)
            except Exception as e:
                logging.error(f"Signup email error: {e}")
            
            return jsonify({
                "status": "success",
                "message": "Account created successfully!",
                "user": {"name": name, "email": email}
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to create account"
            }), 500
            
    except Exception as e:
        logging.error(f"Signup error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Server error"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint - verifies credentials from MongoDB"""
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WellWise-AI-Engine-main'))
        import database as db
        import bcrypt
        
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"status": "error", "message": "Email and password required"}), 400
        
        # Check if user exists
        user = db.get_user_by_email(email)
        if not user:
            return jsonify({
                "status": "error",
                "message": "No account found. Please sign up first."
            }), 404
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            return jsonify({
                "status": "error",
                "message": "Incorrect password"
            }), 401
        
        # Update last login
        db.update_last_login(email)
        
        # Send login notification email
        try:
            from datetime import datetime
            device_info = {
                'browser': request.headers.get('User-Agent', 'Unknown')[:50],
                'os': 'Windows' if 'Windows' in request.headers.get('User-Agent', '') else 'Other',
                'ip': request.remote_addr or 'Unknown',
                'location': 'Unknown',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'device_id': request.headers.get('User-Agent', 'Unknown')[-20:]
            }
            email_utils.send_login_notification(email, user["name"], device_info)
        except Exception as e:
            logging.error(f"Login email error: {e}")
        
        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "user": {
                "name": user["name"],
                "email": user["email"]
            }
        }), 200
        
    except Exception as e:
        logging.error(f"Login error: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "Server error"}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
