<p align="center">
  <img src="https://placehold.co/1200x400/3498db/ffffff?text=WellWise-M&font=poppins" alt="WellWise-M AI Banner">
</p>

# WellWise-M: AI-Powered Life Expectancy & Wellness Engine

**Turning complex health data into clear, actionable, and personalized wellness guidance.**

[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

---

## 📚 Table of Contents

1.  [**Project Overview**](#-1-project-overview)
2.  [**Project Description**](#-2-project-description)
3.  [**Key Features**](#-3-key-features)
4.  [**Tools & Technologies**](#-4-tools--technologies)
5.  [**Project Folder Structure**](#-5-project-folder-structure)
6.  [**Installation & Setup**](#-6-installation--setup)
7.  [**Usage Workflow**](#-7-usage-workflow)
8.  [**Detailed Overview of the AI Engine**](#-8-detailed-overview-of-the-ai-engine)
    * 8.1 [The Data Generation Pipeline](#81-the-data-generation-pipeline)
    * 8.2 [Model Training](#82-model-training)
    * 8.3 [The Hybrid Prediction Architecture](#83-the-hybrid-prediction-architecture)
9.  [**Detailed Overview of the Web Application**](#-9-detailed-overview-of-the-web-application)
    * 9.1 [Backend API & Logic](#91-backend-api--logic)
    * 9.2 [Dynamic Frontend Interface](#92-dynamic-frontend-interface)
10. [**Future Scope**](#-10-future-scope)
11. [**Author**](#-11-author)
12. [**License**](#-12-license)

---

## 📌 1. Project Overview <a name="1-project-overview"></a>

This project focuses on developing a comprehensive, AI-powered health and wellness application named **WellWise-M**. By combining a sophisticated machine learning model with a user-friendly web interface, the project aims to provide individuals with personalized life expectancy predictions, detailed explanations of influencing health factors, and actionable recommendations to improve their long-term well-being. It was conceived and built as a submission for a hackathon.

## 📌 2. Project Description <a name="2-project-description"></a>

🩺 In an era of abundant health data from wearables and apps, users often face a deluge of disconnected metrics without a clear understanding of their overall health trajectory. **WellWise-M** addresses this gap by creating a holistic, narrative-driven experience.

The project workflow begins with a custom-built data generation engine in Python, which creates a large-scale, logically sound synthetic dataset. This dataset is engineered with real-world statistical data for Indian states, nuanced medical logic, and robust fail-safes to ensure the data is realistic and free of absurdities.

This high-quality data is then used to train a `LightGBM` regression model to predict life expectancy. The core of the application is a **hybrid prediction architecture** within a Flask backend. This system combines the sophisticated, non-linear predictions of the ML model with a transparent, rule-based "Explainer" model. The result is a final prediction that is both accurate and fully interpretable.

The application serves a dynamic frontend with a comprehensive input form and a rich, graphical results dashboard. The dashboard visualizes the user's health profile using charts and provides a personalized narrative summary and a concrete action plan for improvement.

## 📌 3. Key Features <a name="3-key-features"></a>

-   📑 **Sophisticated Data Engine:** Generates 100,000+ records with nuanced logic for state-specific demographics, gender-based life expectancy, and formula-driven parameters (`BMI`, `Diet Quality`, `Sleep Quality`).
-   🧠 **Hybrid AI Architecture:** Combines a predictive `LightGBM` model with a rule-based explainer to ensure predictions are both accurate and logical.
-   ⚕️ **Multi-Condition Handling:** Understands the cumulative impact of multiple health conditions and family histories via one-hot encoding.
-   📜 **Narrative Summaries & Recommendations:** Delivers personalized text summaries and actionable advice, turning a simple prediction into a supportive action plan.
-   🌐 **Dynamic Frontend:** A smart user interface with auto-calculating fields, geolocation for automatic data entry (State, City, AQI), and cascading dropdowns.
-   📊 **Rich Visualizations:** A graphical results dashboard built with `Chart.js`, featuring a life expectancy gauge, a health profile radar chart, and a lifestyle impact bar chart.

## 📌 4. Tools & Technologies <a name="4-tools--technologies"></a>

| Category           | Technologies                                      |
| ------------------ | ------------------------------------------------- |
| **Backend** | `Python`, `Flask`                                 |
| **Machine Learning** | `Scikit-learn`, `LightGBM`, `Pandas`, `NumPy`     |
| **Frontend** | `HTML5`, `CSS3`, `JavaScript`                     |
| **Visualization** | `Chart.js`                                        |
| **Environment** | `Jupyter Notebook` (for development), `VS Code`   |

## 📌 5. Project Folder Structure <a name="5-project-folder-structure"></a>
WellWise-AI-Engine/
├── 📁 data/

│   └── wellwise_health_data_v15_final.csv

├── 📁 models/

│   ├── life_expectancy_model_v15.pkl

│   └── label_encoders_v15.pkl

├── 📁 scripts/

│   ├── generate_data.py

│   └── train_model.py

├── 📁 static/

│   └── css/

│       └── style.css

├── 📁 templates/

│   ├── index.html

│   └── result.html

├── 📄 .gitignore

├── 📄 app.py

├── 📄 requirements_app.txt

├── 📄 requirements_ds.txt

└── 📄 test_api.py

## 📌 6. Installation & Setup <a name="6-installation--setup"></a>

#### 1️⃣ Clone the repository

git clone [https://github.com/nrai18/WellWise-AI-Engine.git](https://github.com/nrai18/WellWise-AI-Engine.git)
cd WellWise-AI-Engine

2️⃣ Set up Python environments

This project uses two separate virtual environments to keep dependencies clean.

For Data Science (generating data, training model):
python -m venv venv-data-science
.\venv-data-science\Scripts\activate
pip install -r requirements_ds.txt

For the Web Application (running the server):
python -m venv venv-webapp
.\venv-webapp\Scripts\activate
pip install -r requirements_app.txt

## 📌 7. Usage Workflow <a name="7-how-to-run"></a>
The project is designed to be run in a three-step sequence.

### 1️⃣ Generate the Dataset
Activate the data science environment: .\venv-data-science\Scripts\activate

Run the script:
python scripts/generate_data.py

### 2️⃣ Train the AI Model
Ensure the data science environment is still active.

Run the script:
python scripts/train_model.py

### 3️⃣ Run the Web Application
Activate the web application environment: .\venv-webapp\Scripts\activate

Run the server:
flask --app app run

Open your web browser and navigate to http://127.0.0.1:5000.

## 📌 8. Detailed Overview of the AI Engine <a name="8-detailed-overview-of-the-ai-engine"></a>
### 8.1 The Data Generation Pipeline <a name="81-the-data-generation-pipeline"></a>
The foundation of this project is a high-quality synthetic dataset. The scripts/generate_data.py script was engineered to produce realistic data by incorporating several layers of logic:

State-Based Demographics: Each record is assigned a state with a corresponding baseline life expectancy, median age, and typical AQI.

Formula-Driven Fields: Key indicators like BMI, Diet Quality, and Sleep Quality are not random; they are calculated based on other inputs.

Advanced Fail-Safes: A granular, multi-tiered, age-dependent fail-safe prevents the creation of absurd data points (e.g., a 25-year-old dying at 33).

One-Hot Encoding: The script handles the complexity of multiple health conditions by creating separate binary columns for each possible Family History and Existing Condition.

### 8.2 Model Training <a name="82-model-training"></a>
The scripts/train_model.py script prepares the generated data and trains the AI model using LightGBM (LGBMRegressor). It performs crucial preprocessing, including splitting Blood Pressure and using LabelEncoder for other categorical data. The script saves the trained model (.pkl) and encoders (.pkl).

### 8.3 The Hybrid Prediction Architecture <a name="83-the-hybrid-prediction-architecture"></a>
The app.py backend employs a sophisticated hybrid approach:

Rule-Based Calculation: It first calculates a transparent, formula-based life expectancy as a logical baseline.

ML Model as a "Fine-Tuner": The LightGBM model makes its own prediction, and the system uses this to calculate a model_adjustment.

Intelligent Blending: This adjustment is scaled and applied to the baseline, allowing the ML model to "fine-tune" the logical prediction within a reasonable range.

Final Sanity Check: A final fail-safe guarantees the output is always sensible and responsible.

## 📌 9. Detailed Overview of the Web Application <a name="9-detailed-overview-of-the-web-application"></a>
### 9.1 Backend API & Logic <a name="91-backend-api--logic"></a>
The app.py file (built with Flask) robustly handles data from both web forms and JSON API calls. It performs all necessary one-hot and label encoding on live user data to match the format the v15 model was trained on. It also contains the logic to generate personalized narrative summaries and actionable recommendations.

### 9.2 Dynamic Frontend Interface <a name="92-dynamic-frontend-interface"></a>
The frontend focuses on a clean and intuitive user experience.

Smart Fields: Includes auto-calculating fields (BMI, Diet Quality, Sleep Quality).

Geolocation API: A "Use My Current Location" button leverages browser geolocation to auto-fill State, City, Urban/Rural status, and Air Quality Index.

Graphical Dashboard: The results page uses Chart.js to render a rich visual summary, including a life expectancy gauge, a health profile radar chart, and an impact bar chart.

### 📌 10. Future Scope <a name="10-future-scope"></a>
Specific Disease Risk Models: Integrate separate, specialized models to predict the risk of conditions like heart disease and diabetes.

Interactive "What-If" Simulator: Add controls to the results page that allow users to change key lifestyle factors and see the potential impact in real-time.

User Accounts & Progress Tracking: Allow users to create accounts, save their results, and track their health improvements over time.

## 📌 11. Author <a name="11-author"></a>
Naman Rai

## 📌 12. License <a name="12-license"></a>
This project is licensed under the MIT License.
