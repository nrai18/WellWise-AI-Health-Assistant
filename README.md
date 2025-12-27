# 🏥 WellWise AI Health Assistant

**Smart AI-Powered Wellness Platform**

WellWise is a comprehensive healthcare platform that provides personalized diet plans, exercise recommendations, hydration tracking, and AI-powered health predictions using Google's Gemini AI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🥗 **Personalized Diet Plans**
- AI-generated Indian meal recommendations
- BMI calculator and calorie projections
- 3D flip cards with YouTube recipe links
- Customizable meals per day (3-6 meals)
- Nutritional breakdown (calories, protein, fat, carbs, fiber, sugar)

### 🏃 **Exercise Recommendations**
- AI-powered workout plans based on fitness level
- Equipment-based exercise suggestions
- Weekly structured programs
- Intensity tracking (Low/Medium/High)

### 💧 **Hydration Tracker**
- Daily water intake monitoring
- Visual progress indicators
- Customizable daily goals
- Hydration reminders

### 🤖 **WellAI Chatbot**
- Health predictions powered by Gemini AI
- Conversational health advice
- Life expectancy predictions
- Personalized wellness tips

### 🔐 **User Authentication**
- Secure signup/login with MongoDB
- Password hashing with bcrypt
- Email notifications via Mailtrap
- Device fingerprinting for security
- Welcome emails with account details

### 📧 **Email Notifications**
- Beautiful HTML email templates
- Signup confirmation emails
- Login security alerts
- Device and location tracking

---

## 🏗️ Architecture

```
WellWise-Healthcare/
├── frontend/                # React + Vite application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # State management
│   │   └── assets/         # Images and static files
│   └── package.json
│
├── backend/                # Flask API server
│   ├── app.py             # Main API routes
│   ├── email_utils.py     # Mailtrap integration
│   ├── auth.py            # Authentication utilities
│   └── .env               # Environment variables
│
└── WellWise-AI-Engine-main/  # Gemini AI chatbot
    ├── chatbot.py         # AI conversation engine
    ├── database.py        # MongoDB operations
    └── .env               # AI Engine config
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **MongoDB Atlas Account**
- **Google Gemini API Key**
- **Mailtrap Account**

### 1. Clone Repository
```bash
git clone https://github.com/nrai18/WellWise-AI-Health-Assistant.git
cd WellWise-AI-Health-Assistant
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_gemini_api_key" > .env
echo "MONGODB_URI=your_mongodb_connection_string" >> .env
echo "MAILTRAP_API_TOKEN=your_mailtrap_token" >> .env
echo "FATSECRET_CLIENT_ID=your_client_id" >> .env
echo "FATSECRET_CLIENT_SECRET=your_client_secret" >> .env

# Run backend
python app.py
```

### 3. AI Engine Setup
```bash
cd WellWise-AI-Engine-main
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_gemini_api_key" > .env
echo "MONGODB_URI=your_mongodb_connection_string" >> .env

# Run AI engine
python chatbot.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **AI Engine:** http://localhost:5001

---

## 🔑 Environment Variables

### Backend (.env)
```env
GOOGLE_API_KEY=AIza...        # Gemini AI API key
MONGODB_URI=mongodb+srv://...  # MongoDB Atlas connection
MAILTRAP_API_TOKEN=...         # Mailtrap sending API token
FATSECRET_CLIENT_ID=...        # FatSecret API credentials
FATSECRET_CLIENT_SECRET=...
SECRET_KEY=your-secret-key
```

### AI Engine (.env)
```env
GOOGLE_API_KEY=AIza...        # Gemini AI API key
MONGODB_URI=mongodb+srv://...  # MongoDB Atlas connection
```

---

## 📡 API Documentation

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

### User Signup
```http
POST /api/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

### User Login
```http
POST /api/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

### Exercise Plans
```http
POST /api/get_exercise_plan
Content-Type: application/json

{
  "fitnessLevel": "Intermediate",
  "primaryGoal": "Muscle Gain",
  "availableEquipment": {"dumbbells": true},
  "workoutDaysPerWeek": 4,
  "timePerSession": 60
}
```

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling (optional)
- **React Router** - Navigation
- **Recharts** - Data visualization

### Backend
- **Flask** - Python web framework
- **Google Gemini AI** - AI/ML models
- **MongoDB Atlas** - Database
- **Mailtrap** - Email service
- **bcrypt** - Password hashing

### AI Engine
- **Gemini 2.0 Flash** - Conversational AI
- **LangChain** - AI orchestration
- **Python-dotenv** - Environment management

---

## 📧 Email Features

### Signup Welcome Email
- Professional HTML design with green gradient
- Account creation details
- Device security information (browser, OS, IP)
- Feature highlights
- "Get Started" CTA button

### Login Security Alert
- Blue gradient header
- Login details table (time, device, location)
- "Was this you?" confirmation
- Security warning with action steps
- "Secure My Account" button

---

## 🔒 Security Features

- ✅ Environment variables for all secrets
- ✅ `.gitignore` configured for sensitive files
- ✅ Password hashing with bcrypt
- ✅ Git history cleaned of leaked credentials
- ✅ Device fingerprinting for login tracking
- ✅ Email notifications for security events

---

## 🎨 UI Features

### Diet Cards
- 12 unique gradient color combinations
- 3D flip animation on hover
- Pulsing YouTube watch icon
- Recipe links to YouTube search
- Nutritional information display

### Responsive Design
- Mobile-first approach
- Works on all screen sizes
- Touch-friendly interactions

---

## 📝 License

MIT License - feel free to use this project for learning and development!

---

## 👨‍💻 Developer

**Naman Rai**
- GitHub: [@nrai18](https://github.com/nrai18)
- Email: rai18naman@gmail.com

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For issues or questions, please open an issue on GitHub or contact rai18naman@gmail.com

---

**Built with ❤️ using Gemini AI**