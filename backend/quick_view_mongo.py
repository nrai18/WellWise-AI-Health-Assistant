"""
Quick MongoDB Database Viewer - Shows all data instantly
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WellWise-AI-Engine-main'))

from database import get_database
from datetime import datetime

def view_all_data():
    """Display all users and predictions."""
    db = get_database()
    if not db:
        print("❌ Failed to connect to MongoDB")
        print("Make sure:")
        print("1. MongoDB is running (mongod service)")
        print("2. Or MongoDB Atlas connection string is configured in .env")
        return
    
    print("\n" + "="*100)
    print("👥 REGISTERED USERS (Signups)")
    print("="*100 + "\n")
    
    users = list(db.users.find())
    
    if not users:
        print("⚠️  No users found. Try signing up at http://localhost:5173/signup\n")
    else:
        for i, user in enumerate(users, 1):
            print(f"┌─ User #{i} " + "─"*80)
            print(f"│  📧 Email: {user.get('email')}")
            print(f"│  👤 Name: {user.get('name')}")
            print(f"│  📅 Created: {user.get('created_at')}")
            print(f"│  🔐 Last Login: {user.get('last_login', 'Never logged in yet')}")
            print(f"│  🔑 _id: {user.get('_id')}")
            print(f"└" + "─"*90 + "\n")
        
        print(f"✅ Total Users: {len(users)}\n")
    
    print("\n" + "="*100)
    print("🏥 HEALTH PREDICTIONS (Well AI Check-up Forms)")
    print("="*100 + "\n")
    
    predictions = list(db.predictions.find().sort("timestamp", -1).limit(20))
    
    if not predictions:
        print("⚠️  No predictions found. Try filling the health form at http://localhost:5173/About\n")
    else:
        for i, pred in enumerate(predictions, 1):
            print(f"┌─ Prediction #{i} " + "─"*75)
            print(f"│  📧 User: {pred.get('user_email', 'guest@wellwise.com')}")
            print(f"│  ⏰ Submitted: {pred.get('timestamp')}")
            print(f"│  👤 Current Age: {pred.get('current_age')} years")
            print(f"│  🎯 Predicted Life Expectancy: {pred.get('prediction')} years")
            print(f"│  📍 State: {pred.get('state')}")
            
            # Show health data
            health_data = pred.get('health_data', {})
            if health_data:
                print(f"│  ")
                print(f"│  📊 Health Metrics:")
                print(f"│     - Weight: {health_data.get('Weight')} kg")
                print(f"│     - Height: {health_data.get('Height')} cm")
                print(f"│     - BMI: {health_data.get('BMI')}")
                print(f"│     - Smoking: {health_data.get('Smoking')}")
                print(f"│     - Alcohol: {health_data.get('Alcohol')}")
                print(f"│     - Exercise: {health_data.get('Exercise Type')}")
                print(f"│     - Sleep: {health_data.get('Sleep Duration')} hours")
            
            # Health scores
            health_scores = pred.get('health_scores', {})
            if health_scores:
                print(f"│  ")
                print(f"│  ⭐ Health Scores (out of 5.0):")
                for key, value in health_scores.items():
                    bars = "█" * int(value) + "░" * (5 - int(value))
                    print(f"│     - {key}: {value:.1f}/5.0 {bars}")
            
            # Top recommendations
            recommendations = pred.get('recommendations', [])
            if recommendations:
                print(f"│  ")
                print(f"│  💡 Top Recommendations:")
                for j, rec in enumerate(recommendations[:3], 1):
                    print(f"│     {j}. {rec.get('recommendation', 'N/A')}")
            
            print(f"│  🔑 _id: {pred.get('_id')}")
            print(f"└" + "─"*90 + "\n")
        
        print(f"✅ Total Predictions: {db.predictions.count_documents({})}")
        print(f"   (Showing latest {len(predictions)})\n")
    
    # Statistics
    print("\n" + "="*100)
    print("📊 DATABASE STATISTICS")
    print("="*100 + "\n")
    
    user_count = db.users.count_documents({})
    pred_count = db.predictions.count_documents({})
    
    print(f"👥 Total Users: {user_count}")
    print(f"🏥 Total Predictions: {pred_count}")
    
    if user_count > 0 and pred_count > 0:
        avg_predictions = pred_count / user_count
        print(f"📈 Average Predictions per User: {avg_predictions:.1f}")
    
    print()

if __name__ == "__main__":
    try:
        view_all_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if MongoDB is running")
        print("2. Verify MONGODB_URI in .env file")
        print("3. Make sure pymongo is installed: pip install pymongo")
