# 🔧 WellWise Backend API

**Flask-based RESTful API for WellWise Healthcare Platform**

The backend server handles user authentication, diet recommendations, exercise plans, and email notifications.

---

## ⚡ Features

- 🥗 **AI-Generated Diet Plans** with Gemini AI
- 🏃 **Exercise Recommendations** based on fitness level
- 🔐 **User Authentication** with MongoDB
- 📧 **Email Notifications** via Mailtrap
- 📊 **BMI & Calorie Calculations**
- 🔒 **Secure Password Hashing** with bcrypt

---

## 🏗️ Project Structure

```
backend/
├── app.py              # Main Flask application
├── email_utils.py      # Mailtrap email service
├── auth.py             # Authentication utilities
├── fatsecret_api.py    # FatSecret API integration
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (git-ignored)
```

---

## 🚀 Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MAILTRAP_API_TOKEN=your_mailtrap_token
FATSECRET_CLIENT_ID=your_client_id
FATSECRET_CLIENT_SECRET=your_client_secret
SECRET_KEY=your_flask_secret_key
```

### 3. Run Server
```bash
python app.py
```

Server starts on **http://localhost:5000**

---

## 📡 API Endpoints

### User Authentication

#### Signup
```http
POST /api/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

### Diet Recommendations

```http
POST /api/get_full_plan
Content-Type: application/json

{
  "age": 25,
  "height": 170,
  "weight": 70,
  "gender": "male",
  "activityLevel": 2,
  "weightLossPlan": "weightLoss",
  "mealsPerDay": 3
}
```

**Response:**
```json
{
  "bmi": {
    "value": 24.22,
    "category": "Normal"
  },
  "calories": {
    "maintain": {"value": 2200, "projection": "0 kg/week"},
    "weightLoss": {"value": 1700, "projection": "~-0.45 kg/week"}
  },
  "mealPlan": [
    {
      "mealType": "Breakfast",
      "options": [
        {
          "name": "Idli with Sambar",
          "calories": 350,
          "protein": 12,
          "fat": 8,
          "carbs": 55
        }
      ]
    }
  ]
}
```

### Exercise Plans

```http
POST /api/get_exercise_plan
Content-Type: application/json

{
  "fitnessLevel": "Intermediate",
  "primaryGoal": "Weight Loss",
  "availableEquipment": {"dumbbells": true},
  "workoutDaysPerWeek": 4,
  "timePerSession": 45
}
```

---

## 📧 Email Service

### Features
- Beautiful HTML email templates
- Device fingerprinting
- Security notifications
- Welcome emails

### Email Types

#### 1. Signup Confirmation
- Green gradient design
- Account details
- Device information
- Security alert

#### 2. Login Notification
- Blue gradient design
- Login details table
- Security warning
- Action buttons

---

## 🔒 Security

- Password hashing with **bcrypt**
- Environment variables for secrets
- MongoDB authentication
- Device fingerprinting
- IP tracking

---

## 🛠️ Dependencies

```txt
Flask==3.0.0
flask-cors==4.0.0
google-generativeai==0.3.1
pymongo==4.6.0
bcrypt==4.1.2
python-dotenv==1.0.0
requests==2.31.0
```

---

## 👨‍💻 Developer

**Naman Rai**  
GitHub: [@nrai18](https://github.com/nrai18)
