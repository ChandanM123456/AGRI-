import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import pandas as pd
from pathlib import Path
import os

print("🤖 Building Advanced CNN Model for Land Analysis...")

# ============================================================
# CNN MODEL FOR SOIL AND LAND QUALITY ANALYSIS
# ============================================================

class LandAnalysisCNN:
    def __init__(self, input_shape=(224, 224, 3)):
        self.input_shape = input_shape
        self.model = self.build_model()
    
    def build_model(self):
        """
        Build a CNN model for analyzing land images to determine:
        - Soil quality (Poor, Average, Good)
        - Soil moisture level
        - Vegetation density
        - Land texture analysis
        """
        model = models.Sequential([
            # Block 1
            layers.Conv2D(32, (3, 3), activation='relu', padding='same', 
                         input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 2
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 3
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Block 4
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and Dense Layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            
            # Output Layer (Multi-class: Soil Quality Classification)
            layers.Dense(3, activation='softmax')  # Poor, Average, Good
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return model
    
    def get_model_summary(self):
        return self.model.summary()
    
    def save_model(self, filepath='models/land_analysis_cnn.h5'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"✅ Model saved to {filepath}")

# ============================================================
# CROP RECOMMENDATION MODEL
# ============================================================

class CropRecommendationModel:
    def __init__(self):
        self.model = self.build_model()
        self.crop_classes = ['Tomato', 'Onion', 'Chilli', 'Cabbage', 'Maize', 'Potato',
                             'Sugarcane', 'Cotton', 'Rice', 'Groundnut', 'Ragi', 'Wheat']
        self.num_crops = len(self.crop_classes)
    
    def build_model(self):
        """
        Build a model to recommend top 3 crops based on:
        - Soil quality
        - Location
        - Budget
        - Water source
        - Season/Month
        - Land area
        """
        model = models.Sequential([
            layers.Dense(256, activation='relu', input_shape=(10,)),  # 10 input features
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(12, activation='softmax')  # 12 crops
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def get_top_3_crops(self, predictions):
        """Get top 3 crop recommendations"""
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        top_3_crops = [self.crop_classes[i] for i in top_3_indices]
        top_3_probs = [predictions[0][i] for i in top_3_indices]
        return top_3_crops, top_3_probs
    
    def save_model(self, filepath='models/crop_recommendation_model.h5'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"✅ Model saved to {filepath}")

# ============================================================
# PROFIT PREDICTION MODEL
# ============================================================

class ProfitPredictionModel:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        """
        Predict profit based on:
        - Crop type
        - Duration
        - Investment
        - Location
        - Season
        - Market demand
        """
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(8,)),  # 8 input features
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(1, activation='linear')  # Regression output
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae', 'mape']
        )
        
        return model
    
    def save_model(self, filepath='models/profit_prediction_model.h5'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"✅ Model saved to {filepath}")

# ============================================================
# WEATHER PREDICTION MODEL FOR CROP PLANNING
# ============================================================

class WeatherCropOptimizationModel:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        """
        Optimize crop selection based on weather conditions
        """
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(6,)),  # Rainfall, Temp, Humidity, etc.
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(12, activation='softmax')  # 12 crops
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def save_model(self, filepath='models/weather_optimization_model.h5'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
        print(f"✅ Model saved to {filepath}")

# ============================================================
# INITIALIZE AND SAVE ALL MODELS
# ============================================================

print("\n📦 Creating and Saving Models...")

# Create models
print("  🔹 Building Land Analysis CNN...")
land_analysis = LandAnalysisCNN()
land_analysis.save_model()

print("  🔹 Building Crop Recommendation Model...")
crop_rec = CropRecommendationModel()
crop_rec.save_model()

print("  🔹 Building Profit Prediction Model...")
profit_pred = ProfitPredictionModel()
profit_pred.save_model()

print("  🔹 Building Weather Optimization Model...")
weather_opt = WeatherCropOptimizationModel()
weather_opt.save_model()

print("\n" + "="*70)
print("✅ ALL MODELS CREATED AND SAVED SUCCESSFULLY!")
print("="*70)
print("\n📊 Model Architecture Summary:")
print("  1. Land Analysis CNN - Soil Quality Classification")
print("     Input: (224, 224, 3) - Land Image")
print("     Output: [Poor, Average, Good] probabilities")
print("\n  2. Crop Recommendation - Top 3 Crop Selector")
print("     Input: Soil, Location, Budget, Water, Season, Area")
print("     Output: Top 3 Crop Recommendations with Probabilities")
print("\n  3. Profit Prediction - Financial Forecast")
print("     Input: Crop, Duration, Investment, Location, Season, Demand")
print("     Output: Predicted Profit (₹)")
print("\n  4. Weather Optimization - Seasonal Crop Planning")
print("     Input: Rainfall, Temperature, Humidity, Wind, Season")
print("     Output: Optimized Crop Selection")
print("\n🌾 Models are ready for training with real data!")
