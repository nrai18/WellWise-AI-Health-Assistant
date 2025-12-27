"""
MongoDB Database Viewer
View users and health predictions from MongoDB
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'WellWise-AI-Engine-main'))

from database import get_database

def view_users():
    """Display all registered users."""
    db = get_database()
    if not db:
        print("❌ Failed to connect to MongoDB")
        return
    
    print("\n" + "="*80)
    print("👥 REGISTERED USERS")
    print("="*80 + "\n")
    
    users = list(db.users.find())
    
    if not users:
        print("No users found in database.\n")
        return
    
    for i, user in enumerate(users, 1):
        print(f"User #{i}")
        print(f"  Name: {user.get('name')}")
        print(f"  Email: {user.get('email')}")
        print(f"  Created: {user.get('created_at')}")
        print(f"  Last Login: {user.get('last_login', 'Never')}")
        print(f"  Password Hash: {user.get('password_hash')[:20]}... (truncated)")
        print()
    
    print(f"Total Users: {len(users)}\n")

def view_predictions():
    """Display all health predictions."""
    db = get_database()
    if not db:
        print("❌ Failed to connect to MongoDB")
        return
    
    print("\n" + "="*80)
    print("🏥 HEALTH PREDICTIONS")
    print("="*80 + "\n")
    
    predictions = list(db.predictions.find().sort("timestamp", -1))
    
    if not predictions:
        print("No predictions found in database.\n")
        return
    
    for i, pred in enumerate(predictions, 1):
        print(f"Prediction #{i}")
        print(f"  User Email: {pred.get('user_email')}")
        print(f"  Timestamp: {pred.get('timestamp')}")
        print(f"  Current Age: {pred.get('current_age')}")
        print(f"  Predicted Life Expectancy: {pred.get('prediction')} years")
        print(f"  State: {pred.get('state')}")
        
        # Show health scores if available
        health_scores = pred.get('health_scores', {})
        if health_scores:
            print(f"  Health Scores:")
            for key, value in health_scores.items():
                print(f"    - {key}: {value:.1f}/5.0")
        
        # Show top recommendations
        recommendations = pred.get('recommendations', [])
        if recommendations:
            print(f"  Top Recommendations:")
            for rec in recommendations[:3]:
                print(f"    - {rec.get('recommendation', 'N/A')}")
        
        print()
    
    print(f"Total Predictions: {len(predictions)}\n")

def view_stats():
    """Display database statistics."""
    db = get_database()
    if not db:
        print("❌ Failed to connect to MongoDB")
        return
    
    print("\n" + "="*80)
    print("📊 DATABASE STATISTICS")
    print("="*80 + "\n")
    
    user_count = db.users.count_documents({})
    pred_count = db.predictions.count_documents({})
    
    print(f"Total Users: {user_count}")
    print(f"Total Predictions: {pred_count}")
    
    if user_count > 0:
        # Most active user
        pipeline = [
            {"$group": {"_id": "$user_email", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        most_active = list(db.predictions.aggregate(pipeline))
        if most_active:
            print(f"Most Active User: {most_active[0]['_id']} ({most_active[0]['count']} predictions)")
    
    print()

def main():
    """Main menu."""
    while True:
        print("\n" + "="*80)
        print("🗄️  WELLWISE MONGODB VIEWER")
        print("="*80)
        print("\n1. View All Users")
        print("2. View All Health Predictions")
        print("3. View Database Statistics")
        print("4. View Everything")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            view_users()
        elif choice == '2':
            view_predictions()
        elif choice == '3':
            view_stats()
        elif choice == '4':
            view_users()
            view_predictions()
            view_stats()
        elif choice == '5':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    print("\n🚀 Connecting to MongoDB...")
    main()
