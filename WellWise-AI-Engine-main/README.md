# 🤖 WellWise AI Engine

**Conversational Health Prediction Chatbot powered by Google Gemini AI**

The WellWise AI Engine is the intelligent core of the WellWise Healthcare platform, providing health predictions, wellness advice, and conversational AI interactions.

---

## ✨ Features

### 🧠 **AI-Powered Health Predictions**
- Life expectancy predictions based on health metrics
- Personalized wellness recommendations
- Conversational health consultations
- Context-aware responses using conversation history

### 💬 **Natural Language Processing**
- Powered by **Gemini 2.0 Flash Experimental**
- Multi-turn conversation support
- Context retention across sessions
- Human-like health advice

### 📊 **Health Data Analysis**
- Age-based health assessments
- Lifestyle factor analysis
- BMI and health metric correlations
- Predictive health modeling

### 🗄️ **MongoDB Integration**
- User data persistence
- Conversation history storage
- Health metrics tracking
- Secure data management

---

## 🏗️ Architecture

```
WellWise-AI-Engine-main/
├── chatbot.py           # Main AI conversation engine
├── database.py          # MongoDB operations
├── app.py              # Flask API server
├── requirements.txt    # Python dependencies
├── .env                # Environment configuration
└── README.md           # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account
- Google Gemini AI API key

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

3. **Run the AI Engine**
```bash
python chatbot.py
```

The server will start on `http://localhost:5001`

---

## 📡 API Endpoints

### Health Prediction
```http
POST /predict
Content-Type: application/json

{
  "age": 25,
  "user_message": "How long will I live?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "prediction": "82 years",
  "advice": "Based on your age and health data...",
  "conversation_id": "uuid-here"
}
```

### Chat Interaction
```http
POST /chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "What exercises should I do?",
  "conversation_history": [...]
}
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Gemini AI API key from Google AI Studio | Yes |
| `MONGODB_URI` | MongoDB Atlas connection string | Yes |
| `PORT` | Server port (default: 5001) | No |

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

#### MongoDB Atlas
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get connection string
4. Replace `<password>` with your database password

---

## 🧪 Usage Examples

### Python Example
```python
import requests

url = "http://localhost:5001/predict"
payload = {
    "age": 30,
    "user_message": "What's my health score?",
    "conversation_history": []
}

response = requests.post(url, json=payload)
print(response.json())
```

### cURL Example
```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "user_message": "Give me health advice",
    "conversation_history": []
  }'
```

---

## 🗃️ Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "email": "user@example.com",
  "name": "John_Doe",
  "password_hash": "hashed_password",
  "created_at": ISODate,
  "last_login": ISODate
}
```

### Health Predictions Collection
```javascript
{
  "_id": ObjectId,
  "user_id": "user123",
  "age": 25,
  "prediction": "85 years",
  "conversation": [...],
  "timestamp": ISODate
}
```

---

## 🤖 AI Model Details

### Gemini 2.0 Flash Experimental
- **Model:** `gemini-2.0-flash-exp`
- **Temperature:** 0.7 (balanced creativity)
- **Max Tokens:** 2048
- **Context Window:** 32k tokens
- **Strengths:**
  - Fast response times
  - High accuracy
  - Conversational context retention
  - Health knowledge domain expertise

### Prompt Engineering
The chatbot uses carefully crafted system prompts to:
- Provide medically sound advice
- Maintain conversational context
- Generate personalized responses
- Handle edge cases gracefully

---

## 📊 Features in Detail

### Conversation History
- Maintains context across multiple exchanges
- Stores previous Q&A pairs
- Enables follow-up questions
- Improves response relevance

### Health Metrics Analysis
- Age-based life expectancy
- BMI calculations
- Activity level assessments
- Nutrition recommendations

### Error Handling
- Graceful API failures
- Database connection retries
- Input validation
- Logging for debugging

---

## 🔒 Security

- ✅ API keys stored in environment variables
- ✅ MongoDB connection with authentication
- ✅ Input sanitization
- ✅ Rate limiting (optional)
- ✅ CORS configuration for trusted origins

---

## 🛠️ Dependencies

```txt
google-generativeai>=0.3.0  # Gemini AI SDK
pymongo>=4.6.0              # MongoDB driver
python-dotenv>=1.0.0        # Environment management
flask>=3.0.0                # Web framework
flask-cors>=4.0.0           # CORS support
```

---

## 📝 Development

### Running in Development Mode
```bash
# Enable debug mode
export FLASK_ENV=development
python chatbot.py
```

### Testing
```bash
# Run unit tests
python -m pytest tests/

# Test API endpoint
python test_chatbot.py
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use environment-specific MongoDB URI
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Monitor API usage

### Deployment Options
- **Heroku:** See `Procfile`
- **AWS Lambda:** Serverless deployment
- **Docker:** Use provided `Dockerfile`
- **Cloud Run:** Google Cloud deployment

---

## 🐛 Troubleshooting

### Common Issues

**MongoDB Connection Error**
```
Solution: Check your MONGODB_URI format and network access in Atlas
```

**Gemini API Quota Exceeded**
```
Solution: Check your API key quota at Google AI Studio
```

**Port Already in Use**
```bash
# Change port in code or kill existing process
lsof -ti:5001 | xargs kill -9
```

---

## 📚 Additional Resources

- [Gemini AI Documentation](https://ai.google.dev/docs)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 👨‍💻 Developer

**Naman Rai**
- GitHub: [@nrai18](https://github.com/nrai18)
- Email: rai18naman@gmail.com

---

## 📄 License

MIT License - See LICENSE file for details

---

**Powered by Google Gemini AI** 🚀
