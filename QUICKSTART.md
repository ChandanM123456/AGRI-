# Quick Start Guide for Farmer Advisory System

## 🚀 Getting Started (5 minutes)

### Option 1: Automated Setup (Recommended)

#### Windows
```bash
python setup_windows.py
```

#### Linux/Mac
```bash
bash setup.sh
```

### Option 2: Manual Setup

#### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Create Directories
```bash
mkdir datasets models uploads logs
```

#### Step 4: Download Datasets
```bash
python enhanced_download_data.py
```

#### Step 5: Build Models
```bash
python land_analysis_model.py
```

#### Step 6: Run Application
```bash
python app.py
```

#### Step 7: Open Browser
Navigate to: **http://localhost:5000**

---

## 👨‍🌾 Using the Application

### First Time User (Farmer)

1. **Register**
   - Click "Register here" on login page
   - Fill in details: Username, Email, Phone, Location, Land Area
   - Click "Register"

2. **Login**
   - Enter username and password
   - Click "Login"

3. **Analyze Your Land**
   - Click "New Crop Plan"
   - Select soil quality (Poor/Average/Good)
   - Select water availability (Low/Medium/High)
   - Enter budget in rupees
   - Enter land area in hectares
   - Enter location (optional)
   - Click "Analyze & Get Recommendations"

4. **View Recommendations**
   - See top 3 recommended crops
   - Review match score, profit, duration
   - Click "Select This Crop" for your choice

5. **Create Crop Plan**
   - View crop details and financial info
   - Select start date
   - Click "Create Crop Plan"

6. **Follow Daily Guide**
   - View day-by-day farming tasks
   - Mark tasks as complete
   - Check today's tasks

7. **Get Selling Guide**
   - Click "Selling Guide" when crop is ready
   - View market information
   - Get selling recommendations
   - Connect with retailers

---

## 🔧 Configuration

### Database
- Default: SQLite (farmer_app.db)
- For production: Use PostgreSQL or MySQL

### API Keys Needed (Optional)
- OpenWeatherMap API for weather data
- AWS S3 for image storage in production

### Environment Variables
Copy `.env.example` to `.env` and update values

---

## 📊 Sample Data

### Test Login
- Username: `testfarmer`
- Password: `password123`

### Test Crops
Available: Tomato, Onion, Chilli, Cabbage, Maize, Potato, Sugarcane, Cotton, Rice, etc.

### Test Locations
Supported: Bangalore, Mysore, Tumkur, Mandya, Punjab, Maharashtra, Gujarat, etc.

---

## 🐛 Troubleshooting

### Issue: "No module named 'flask'"
**Solution:** 
```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution:**
```bash
pip install tensorflow==2.12.0
```

### Issue: Database errors
**Solution:**
```bash
# Delete the old database
rm farmer_app.db
# Restart the application
python app.py
```

### Issue: Models not found
**Solution:**
```bash
python land_analysis_model.py
```

### Issue: Port 5000 already in use
**Solution:**
```bash
python app.py --port 5001
```

---

## 📱 Mobile Access

Access on mobile device:
1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Linux/Mac: `ifconfig` (look for inet)

2. On mobile browser:
   - Go to: `http://<your-ip>:5000`

---

## 🚀 Deployment

### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

### Docker
```bash
docker build -t farmadvisor .
docker run -p 5000:5000 farmadvisor
```

### AWS EC2
1. Launch Ubuntu instance
2. Install Python 3.9+
3. Clone repository
4. Run setup
5. Use Gunicorn + Nginx

---

## 📚 Additional Resources

- **Full Documentation:** README.md
- **Project Summary:** PROJECT_SUMMARY.md
- **API Reference:** README.md (API Endpoints section)
- **Datasets:** datasets/ folder
- **Models:** models/ folder
- **Templates:** templates/ folder

---

## 💡 Tips

1. **Backup Database:** Regularly backup farmer_app.db
2. **Update Data:** Run enhanced_download_data.py monthly
3. **Monitor Logs:** Check logs/ folder for errors
4. **Test Features:** Use test data before production
5. **Security:** Change SECRET_KEY in production

---

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- TensorFlow Guide: https://www.tensorflow.org/learn
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- Pandas Tutorial: https://pandas.pydata.org/docs/

---

## 📞 Support

For issues or questions:
1. Check README.md
2. Review code comments
3. Check logs/ folder
4. Consult documentation files

---

**Enjoy using Farmer Advisory System! 🌾**

Last Updated: April 2026
