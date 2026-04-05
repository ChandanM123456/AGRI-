# Farmer Advisory System - Complete Real-World Application

## Project Structure

```
Agri/
├── app.py                          # Main Flask application
├── enhanced_download_data.py        # Enhanced dataset collection script
├── land_analysis_model.py           # CNN model for land analysis
├── train_model.py                   # Model training script
├── requirements.txt                 # Python dependencies
├── datasets/                        # Dataset storage
│   ├── enhanced_crop_database.csv
│   ├── enhanced_market_data.csv
│   ├── location_based_data.csv
│   ├── soil_analysis_reference.csv
│   ├── weather_crop_performance.csv
│   ├── crop_management_guide.csv
│   ├── profit_duration_analysis.csv
│   └── crop_selling_guide.csv
├── models/                          # Trained ML models
│   ├── land_analysis_cnn.h5
│   ├── crop_recommendation_model.h5
│   ├── profit_prediction_model.h5
│   └── weather_optimization_model.h5
├── uploads/                         # User uploaded images
├── templates/                       # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── land_analysis.html
│   ├── recommendations.html
│   ├── crop_selection.html
│   ├── crop_detail.html
│   ├── selling_guide.html
│   ├── 404.html
│   └── 500.html
└── static/                          # CSS and static files
    ├── styles.css
    └── images/
```

## Features Implemented

### 1. **User Authentication**
- Secure login system with password hashing
- User registration with farmer details
- Session management with Flask-Login

### 2. **Land Analysis & Recommendation System**
- Analyze land based on soil quality, water source, budget, and area
- CNN model for soil image analysis
- ML-based crop recommendation engine
- Top 3 crop suggestions with match scores

### 3. **Crop Planning**
- Day-by-day crop management guide
- Fertilizer and pest management schedules
- Task tracking and reminders
- Integration with weather data

### 4. **Financial Management**
- Profit prediction models
- Investment cost calculation
- Expected ROI for each crop
- Break-even period analysis

### 5. **Market Intelligence**
- Real-time market pricing data
- Demand analysis by season and region
- Selling guide and strategies
- Retailer connection network

### 6. **Dashboard**
- Active crop monitoring
- Profit tracking
- Task management
- Quick access to key features

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment support

### Installation Steps

1. **Clone the repository**
```bash
cd Agri
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download datasets**
```bash
python enhanced_download_data.py
```

5. **Build models**
```bash
python land_analysis_model.py
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
Open your browser and go to: `http://localhost:5000`

## Key Datasets

### 1. Enhanced Crop Database (10,000+ crops)
- Crop parameters (temperature, rainfall, soil type, etc.)
- Growing season duration
- Water requirements
- Seed quantities
- Average yield per hectare

### 2. Market Data
- Real-time pricing by crop and season
- Market demand levels
- Waste percentage estimates
- Regional variations

### 3. Location-Based Data
- Regional crop suitability
- Soil types by region
- Weather patterns
- Historical yields

### 4. Soil Analysis Reference
- Nitrogen, phosphorus, potassium levels
- pH requirements
- Organic matter content
- Crop suitability mapping

### 5. Weather-Crop Performance
- Season-specific crop performance
- Disease risk analysis
- Optimal growing conditions
- Yield predictions

### 6. Management Guide
- Day-by-day fertilizer schedule
- Pest management strategies
- Pesticide recommendations
- Irrigation schedules

### 7. Profit Analysis
- Investment requirements
- Expected profit ranges
- Break-even analysis
- Duration categories

### 8. Selling Guide
- Market readiness period
- Shelf life
- Packaging recommendations
- Transport strategies

## Machine Learning Models

### 1. Land Analysis CNN
- **Input:** Land image (224x224x3)
- **Output:** Soil quality classification (Poor/Average/Good)
- **Architecture:** 4-block CNN with batch normalization

### 2. Crop Recommendation Model
- **Input:** Soil quality, location, budget, water, season, area
- **Output:** Top 3 crop recommendations with probabilities
- **Architecture:** Deep neural network with 5 layers

### 3. Profit Prediction Model
- **Input:** Crop type, duration, investment, location, season, demand
- **Output:** Expected profit in rupees
- **Architecture:** Regression model with 4 layers

### 4. Weather Optimization Model
- **Input:** Rainfall, temperature, humidity, wind, season
- **Output:** Optimized crop selection
- **Architecture:** Classification model for 12 crop types

## User Flow

1. **Registration:** Farmer creates account with location, phone, and land area
2. **Land Analysis:** Upload land image, provide soil quality, water source, budget
3. **Recommendations:** System analyzes and suggests top 3 crops
4. **Crop Selection:** Choose crop and start date
5. **Daily Guide:** Follow day-by-day farming schedule
6. **Task Tracking:** Mark completed tasks
7. **Selling Guide:** Get market recommendations when ready to harvest
8. **Financial Tracking:** Monitor profit and ROI

## API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Crop Management
- `GET /dashboard` - Main dashboard
- `POST /land-analysis` - Analyze land and get recommendations
- `POST /crop-selection/<crop_name>` - Create crop plan
- `GET /crop/<plan_id>` - View crop details and tasks
- `POST /update-task/<task_id>` - Update task status
- `GET /selling-guide/<plan_id>` - View selling recommendations

### Data APIs
- `GET /api/crops` - Get all crop data
- `GET /api/market-data` - Get market information
- `GET /weather/<location>` - Get weather forecast

## Configuration

### Database
- SQLite database (`farmer_app.db`)
- Models: User, CropPlan, DailyTask

### File Uploads
- Maximum file size: 50MB
- Allowed formats: Image files (JPG, PNG)
- Storage: `uploads/` directory

### Security
- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection enabled

## Future Enhancements

1. **Advanced AI Features**
   - Real satellite data integration
   - Computer vision for soil analysis
   - Weather API integration

2. **Mobile Application**
   - React Native or Flutter app
   - Offline functionality
   - Push notifications

3. **Community Features**
   - Farmer-to-farmer knowledge sharing
   - Community marketplace
   - Expert consultation

4. **Advanced Analytics**
   - Predictive analytics
   - Historical data analysis
   - Performance benchmarking

5. **Integration**
   - Government schemes and subsidies
   - Insurance providers
   - Logistics partners

## Troubleshooting

### Issue: Models not found
**Solution:** Run `python land_analysis_model.py` to build models

### Issue: Datasets not downloaded
**Solution:** Run `python enhanced_download_data.py` with Kaggle API configured

### Issue: Database errors
**Solution:** Delete `farmer_app.db` and restart the application

## Support & Documentation

For more information:
- Check individual script comments
- Review template files for UI details
- Consult dataset schemas in CSV files

## License

This project is open-source and available for agricultural use.

---

**Last Updated:** April 2026
**Version:** 1.0 Beta
