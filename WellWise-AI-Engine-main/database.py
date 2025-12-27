from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = "wellwise_db"

def get_database():
    """Get MongoDB database connection."""
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        return client[DATABASE_NAME]
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return None

def init_database():
    """Initialize MongoDB and create collections if needed."""
    db = get_database()
    if db is None:
        print("Failed to connect to MongoDB")
        return False
    
    # Create collections  if they don't exist
    collections = db.list_collection_names()
    
    if 'predictions' not in collections:
        db.create_collection('predictions')
        # Create indexes
        db.predictions.create_index([("user_email", 1), ("timestamp", -1)])
        print("Created 'predictions' collection with indexes")
    
    if 'users' not in collections:
        db.create_collection('users')
        db.users.create_index("email", unique=True)
        print("Created 'users' collection with indexes")
    
    print("MongoDB initialized successfully!")
    return True

def save_prediction(user_email, form_data, prediction_data):
    """
    Save a health prediction to MongoDB.
    
    Args:
        user_email (str): User's email
        form_data (dict): Health form data
        prediction_data (dict): Prediction results
    """
    db = get_database()
    if db is None:
        return {"status": "error", "message": "Database connection failed"}
    
    prediction_doc = {
        "user_email": user_email,
        "timestamp": datetime.now(),
        "age": form_data.get('Age'),
        "prediction": prediction_data.get('prediction'),
        "current_age": prediction_data.get('current_age'),
        "state": form_data.get('State'),
        "health_data": form_data,
        "adjustments": prediction_data.get('adjustments', []),
        "recommendations": prediction_data.get('recommendations', []),
        "health_scores": prediction_data.get('health_scores', {})
    }
    
    try:
        result = db.predictions.insert_one(prediction_doc)
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_user_predictions(user_email, limit=10):
    """
    Get recent predictions for a user.
    
    Args:
        user_email (str): User's email
        limit (int): Number of predictions to retrieve
    
    Returns:
        list: List of prediction documents
    """
    db = get_database()
    if db is None:
        return []
    
    try:
        predictions = db.predictions.find(
            {"user_email": user_email}
        ).sort("timestamp", -1).limit(limit)
        
        results = []
        for pred in predictions:
            results.append({
                "id": str(pred["_id"]),
                "timestamp": pred["timestamp"].isoformat(),
                "prediction": pred.get("prediction"),
                "current_age": pred.get("current_age"),
                "state": pred.get("state"),
                "health_scores": pred.get("health_scores", {})
            })
        
        return results
    except Exception as e:
        print(f"Error retrieving predictions: {e}")
        return []

def save_user(email, name, password_hash):
    """
    Save user to MongoDB.
    
    Args:
        email (str): User's email
        name (str): User's name
        password_hash (str): Hashed password
    """
    db = get_database()
    if db is None:
        return {"status": "error", "message": "Database connection failed"}
    
    user_doc = {
        "email": email,
        "name": name,
        "password_hash": password_hash,
        "created_at": datetime.now(),
        "last_login": None
    }
    
    try:
        result = db.users.insert_one(user_doc)
        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        if "duplicate key" in str(e).lower():
            return {"status": "error", "message": "Email already exists"}
        return {"status": "error", "message": str(e)}

def get_user_by_email(email):
    """Get user by email."""
    db = get_database()
    if db is None:
        return None
    
    try:
        user = db.users.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def update_last_login(email):
    """Update user's last login timestamp."""
    db = get_database()
    if db is None:
        return
    
    try:
        db.users.update_one(
            {"email": email},
            {"$set": {"last_login": datetime.now()}}
        )
    except Exception as e:
        print(f"Error updating last login: {e}")

# Initialize database when module is imported
if __name__ == "__main__":
    init_database()

