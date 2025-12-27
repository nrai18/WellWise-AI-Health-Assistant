"""
Authentication utilities for WellWise
Handles user signup, login, and password management
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'WellWise-AI-Engine-main'))

import bcrypt
from WellWise_AI_Engine_main import database

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def signup_user(name, email, password):
    """
    Register a new user.
    Returns: dict with status and message
    """
    # Check if user already exists
    existing_user = database.get_user_by_email(email)
    if existing_user:
        return {
            "status": "error",
            "message": "An account with this email already exists. Please login instead."
        }
    
    # Hash password and save user
    password_hash = hash_password(password)
    result = database.save_user(email, name, password_hash)
    
    if result.get("status") == "success":
        return {
            "status": "success",
            "message": "Account created successfully!",
            "user": {"name": name, "email": email}
        }
    else:
        return {
            "status": "error",
            "message": result.get("message", "Failed to create account")
        }

def login_user(email, password):
    """
    Authenticate a user.
    Returns: dict with status, message, and user data if successful
    """
    # Check if user exists
    user = database.get_user_by_email(email)
    
    if not user:
        return {
            "status": "error",
            "message": "No account found with this email. Please sign up first."
        }
    
    # Verify password
    if not verify_password(password, user["password_hash"]):
        return {
            "status": "error",
            "message": "Incorrect password. Please try again."
        }
    
    # Update last login
    database.update_last_login(email)
    
    return {
        "status": "success",
        "message": "Login successful!",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "last_login": user.get("last_login")
        }
    }
