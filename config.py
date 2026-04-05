#!/usr/bin/env python
"""
Production Deployment Configuration for Farmer Advisory System
"""

import os
from datetime import timedelta

class ProductionConfig:
    """Production environment configuration"""
    
    # Flask Configuration
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///farmer_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # File Upload
    MAX_CONTENT_LENGTH = 52428800  # 50MB
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/app.log'
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # API Keys
    WEATHER_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    WEATHER_API_ENABLED = os.getenv('WEATHER_API_ENABLED', False)
    
    # AWS S3 (for production image storage)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

class DevelopmentConfig(ProductionConfig):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class TestingConfig(ProductionConfig):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
