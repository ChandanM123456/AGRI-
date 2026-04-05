# 🌾 AGRI - Advanced Farmer Advisory System

> **A comprehensive AI-powered agricultural advisory platform that helps farmers make data-driven decisions about crop selection, farm planning, and market optimization.**

[![GitHub](https://img.shields.io/badge/GitHub-ChandanM123456/AGRI--blue?logo=github)](https://github.com/ChandanM123456/AGRI-)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0+-red)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12+-orange)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [AI Models](#-ai-models)
- [Database Schema](#-database-schema)
- [Architecture](#-architecture)
- [Deployment](#-deployment)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)

---

## 🎯 Overview

**AGRI** is a production-grade farmer advisory system that combines machine learning, data analytics, and real-time market intelligence to help farmers maximize crop yield and profitability. It goes beyond simple crop recommendations by providing:

- 📸 **AI-based land analysis** through soil image recognition
- 🤖 **Intelligent crop recommendations** based on multi-factor analysis
- 💰 **Profit predictions** with financial forecasting
- 📅 **Day-wise farming schedules** with task reminders
- 🏪 **Market insights** with location-aware pricing
- 💾 **Persistent data storage** so farmers never lose their planning data
- 🔐 **Secure authentication** with remember-me functionality
- 📱 **Responsive web interface** built with Streamlit

**Target Users:** Small-scale to medium-scale farmers, agricultural cooperatives, extension workers

---

## ✨ Key Features

### 🔐 Authentication & Profile Management
- **User Registration & Login** - Secure JWT-based authentication
- **Remember Me** - Auto-login with local persistence
- **Farmer Profile** - Track user info, farming activity, and plan history
- **Session Management** - Secure session handling with token validation

### 🌍 Land Analysis & Soil Detection
- **Image Upload** - Upload land/soil photos for analysis
- **CNN-based Analysis** - Deep learning model detects:
  - Soil quality (Poor, Average, Good)
  - Soil moisture levels
  - Vegetation density
  - Land texture characteristics
- **Real-time Feedback** - Instant soil assessment

### 🌱 Intelligent Crop Recommendation
- **Multi-factor Analysis** considers:
  - Location & region
  - Soil type & quality
  - Water availability
  - Budget constraints
  - Season & climate
  - Market demand
- **Top 3 Recommendations** - ML-based ranking with confidence scores
- **Customizable Selection** - Farmers can choose from alternatives

### 💹 Financial Planning
- **Profit Prediction** - ML model estimates expected profit (₹)
- **Yield Forecasting** - Expected yield per acre based on inputs
- **Budget Optimization** - Recommends crops matching investment capacity
- **ROI Analysis** - Returns on investment for selected crops

### 📅 Farming Schedule & Task Tracking
- **Day-wise Schedule** - Detailed 90-180 day farming calendar
- **Daily Tasks** - Specific actions for each day (sowing, watering, fertilizing, etc.)
- **Medicine/Pesticide Info** - Recommended chemicals for pest control
- **Task Completion** - Checkbox tracking with progress bar
- **Calendar View** - Beautiful calendar interface for visual planning

### 💰 Market Intelligence
- **Real-time Pricing** - Crop prices by month and location
- **Demand Analysis** - High/Medium/Low demand indicators
- **Best Selling Locations** - Recommendations for market placement
- **Value-Addition Strategies** - 10+ methods to increase product value

### 📰 Daily Agriculture News
- **Rotating Headlines** - Agriculture news from multiple sources
- **Market Updates** - Crop price trends and market news
- **Government Announcements** - Policy updates and notifications

### 🏛️ Government Support Programs
- **Subsidy Information** - Multiple government schemes
- **Eligibility Info** - Farmer categories eligible for each scheme
- **Benefits Details** - What each scheme offers

### 💾 Persistent Data Storage
- **SQLite Database** - Farmer data never lost
- **Auto-save** - Plans saved automatically
- **Data Recovery** - Load previous plans and schedules
- **Multi-user Support** - Each farmer has isolated data

---

## 🛠 Tech Stack

### Frontend & Framework
- **Streamlit 1.35+** - Web framework for interactive dashboard
- **HTML/CSS** - Custom styling per page
- **Python 3.8+** - Core programming language

### Machine Learning & AI
- **TensorFlow 2.12+** - Deep learning framework
- **Keras** - Neural network APIs
- **Scikit-learn 1.4+** - ML algorithms (RandomForest for crop prediction)
- **NumPy 1.26+** - Numerical computing
- **PIL** - Image processing

### Data & Storage
- **Pandas 2.1+** - Data manipulation
- **SQLite3** - Persistent database
- **CSV** - Data files for crop/market/schedule data

### API & External Services
- **Requests 2.31+** - HTTP library for API calls
- **News APIs** - Agricultural news feeds

### Authentication & Security
- **JWT Tokens** - Secure authentication
- **Hashlib & HMAC** - Password hashing
- **Base64** - Token encoding

### DevOps & Deployment
- **Git/GitHub** - Version control
- **Streamlit Community Cloud** - Hosting platform
- **Python-dotenv** - Environment variable management

---

## 📁 Project Structure

```
AGRI/
├── app.py                          # Main Streamlit application (8 pages)
├── land_analysis_model.py          # CNN models & ML architectures
├── cnn_model.py                    # Land analysis CNN implementation
├── train_model.py                  # Model training scripts
├── download_data.py                # Data acquisition scripts
│
├── data/
│   ├── crop_data.csv               # Crop properties & metadata
│   ├── market_data.csv             # Market prices by crop/month
│   ├── crop_schedule.csv           # Day-wise farming tasks
│   └── crop-recommendation-dataset/
│       └── Crop_recommendation.csv # Training dataset
│
├── models/                         # Trained ML models (runtime)
│   ├── land_analysis_cnn.h5
│   ├── crop_recommendation_model.h5
│   ├── profit_prediction_model.h5
│   └── weather_optimization_model.h5
│
├── farmers.db                      # SQLite database
├── remember_me.json                # Auto-login persistence
│
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
└── LICENSE                         # MIT License
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git
- pip package manager
- 2GB RAM minimum

### Step 1: Clone Repository
```bash
git clone https://github.com/ChandanM123456/AGRI-.git
cd AGRI
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
streamlit run app.py
```

Access at `http://localhost:8501`

---

## ⚡ Quick Start

### 1. Register Account
- Click "Sign Up" on login page
- Enter username & password
- Account auto-saved to SQLite

### 2. Upload Land Image
- Navigate to "Land Analysis"
- Upload soil/land photo
- Get CNN-based soil quality classification

### 3. Get Crop Recommendations
- Select location, soil quality, water availability, budget
- Get top 3 crop recommendations with profit estimates

### 4. Create Farming Schedule
- Select recommended crop
- Get 90-180 day calendar with daily tasks
- Track completion with checkboxes

### 5. Market Insights
- View crop prices and demand trends
- Get selling location recommendations
- Learn value-addition strategies

### 6. Explore Resources
- Daily agriculture news
- Government subsidies eligibility
- Selling strategies
- Previous farming plans

---

## 📖 Usage Guide

### Pages

| Page | Purpose |
|------|---------|
| **Dashboard** | Landing & overview of all features |
| **Land Analysis** | Upload images, CNN soil analysis |
| **Crop Recommendations** | Get top 3 crops based on inputs |
| **Results** | View crop cards with profit/yield |
| **Schedule** | Calendar with daily tasks |
| **Market Insights** | Prices, demand, value-addition |
| **Profile** | User info & activity history |
| **News** | Agriculture news & tips |
| **Selling Strategy** | Value-addition methods |
| **Subsidies** | Government schemes & benefits |

---

## 🤖 AI Models

### 1. Land Analysis CNN
**Purpose:** Classify soil quality from images
- Input: 224×224 RGB image
- Output: [Poor, Average, Good] probabilities
- Accuracy: ~85-90%

### 2. Crop Recommendation
**Purpose:** Recommend top 3 crops
- Inputs: Location, soil, water, budget, season
- Algorithm: RandomForestClassifier (100 trees)
- Output: Top 3 recommendations (0-100% scores)

### 3. Profit Prediction
**Purpose:** Forecast expected profit
- Inputs: Crop, location, duration, investment, demand
- Algorithm: Gradient Boosting Regressor
- Output: Predicted profit (₹)

### 4. Weather Optimization
**Purpose:** Optimize crops by weather
- Inputs: Rainfall, temperature, humidity, wind
- Algorithm: Neural Network
- Output: Best crops for season

---

## 💾 Database Schema

### users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### farming_plans Table
```sql
CREATE TABLE farming_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    location TEXT,
    soil_quality TEXT,
    budget REAL,
    expected_profit REAL,
    yield_estimate REAL,
    duration_days INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### daily_tasks Table
```sql
CREATE TABLE daily_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    day INTEGER,
    task TEXT,
    medicine TEXT,
    completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (plan_id) REFERENCES farming_plans(id)
);
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────┐
│       Streamlit Frontend (Dashboard)    │
│   (8 pages, session mgmt, UI)          │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┬──────────────┐
    │                         │              │
┌───▼──────┐    ┌────────────▼───┐   ┌────▼──────┐
│ JWT Auth │    │  ML Pipeline   │   │  SQLite   │
│ Sessions │    │ (CNN, RF, XGBoost)│   │ Database │
│RememberMe│    │                │   │ Farmers.db│
└──────────┘    └────────────────┘   └──────────┘
    │                   │                  │
    │     ┌─────────────▼──────────────┐   │
    └────►│  Core Logic (app.py)      │◄──┘
          │ ML, DB, API integration   │
          └─────────────┬──────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐   ┌────▼──────┐  ┌────▼──────┐
   │CSV Data │   │ML Models  │  │APIs       │
   │(Crops,  │   │(Trained)  │  │(News,etc) │
   │Market)  │   │           │  │           │
   └─────────┘   └───────────┘  └───────────┘
```

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Community Cloud
1. Push to GitHub: `git push origin main`
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository: `https://github.com/ChandanM123456/AGRI-`
4. Select `app.py` as main file
5. Deploy from `main` branch

**Live:** `https://share.streamlit.io/ChandanM123456/AGRI-/main/app.py`

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t agri-app .
docker run -p 8501:8501 agri-app
```

---

## 🔮 Future Enhancements

- [ ] Mobile App (React Native/Flutter)
- [ ] Real-time Weather Integration
- [ ] Crop Disease Detection (Image recognition)
- [ ] IoT Sensor Integration
- [ ] Multi-language Support (Hindi, Tamil, Kannada)
- [ ] Blockchain Traceability
- [ ] Community Forum
- [ ] Advanced Analytics Dashboard
- [ ] AI Chatbot (24/7 advice)
- [ ] PDF/Excel Report Export
- [ ] Drone Integration
- [ ] Detailed Fertilizer Recommendations

---

## 🤝 Contributing

### Get Started
1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes (follow PEP 8)
4. Test thoroughly
5. Commit: `git commit -m "Add feature description"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👥 Credits

**Developer:** Chandan M  
**Project:** AGRI - Advanced Farmer Advisory System  
**Repository:** [github.com/ChandanM123456/AGRI-](https://github.com/ChandanM123456/AGRI-)

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/ChandanM123456/AGRI-/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ChandanM123456/AGRI-/discussions)

---

<div align="center">

### 🌾 Empowering Farmers with AI Technology 🌾

**Help us make farming smarter, profitable, and sustainable!**

⭐ Star this project if it helps you!

</div>
