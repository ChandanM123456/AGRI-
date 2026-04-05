#!/bin/bash
# Farmer Advisory System Setup Script

echo "🌾 Setting up Farmer Advisory System..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p datasets
mkdir -p models
mkdir -p uploads
mkdir -p logs

# Download datasets
echo "📊 Downloading datasets..."
python enhanced_download_data.py

# Build models
echo "🤖 Building models..."
python land_analysis_model.py

# Initialize database
echo "🗄️ Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all()"

echo "✅ Setup complete! Run 'python app.py' to start the application"
echo "🌍 Application will be available at http://localhost:5000"