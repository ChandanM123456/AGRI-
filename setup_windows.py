#!/usr/bin/env python
"""
Farmer Advisory System - Quick Setup Script for Windows
Run this to quickly set up and start the application
"""

import os
import sys
import subprocess
import shutil

def print_header():
    print("=" * 70)
    print("🌾 FARMER ADVISORY SYSTEM - SETUP WIZARD")
    print("=" * 70)
    print()

def check_python():
    print("✓ Checking Python installation...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor} found")
        return True
    else:
        print(f"  ❌ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def create_venv():
    print("\n✓ Creating virtual environment...")
    if not os.path.exists('venv'):
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        print("  ✅ Virtual environment created")
    else:
        print("  ℹ️ Virtual environment already exists")

def install_dependencies():
    print("\n✓ Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_exe = os.path.join('venv', 'Scripts', 'pip.exe')
    else:  # Linux/Mac
        pip_exe = os.path.join('venv', 'bin', 'pip')
    
    subprocess.run([pip_exe, 'install', '--upgrade', 'pip'])
    subprocess.run([pip_exe, 'install', '-r', 'requirements.txt'])
    print("  ✅ Dependencies installed")

def create_directories():
    print("\n✓ Creating directories...")
    directories = ['datasets', 'models', 'uploads', 'logs', 'templates', 'static']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  ✅ Created {directory}/")
        else:
            print(f"  ℹ️ {directory}/ already exists")

def download_datasets():
    print("\n✓ Downloading datasets...")
    try:
        print("  ⏳ This may take a few minutes...")
        if os.name == 'nt':  # Windows
            python_exe = os.path.join('venv', 'Scripts', 'python.exe')
        else:
            python_exe = os.path.join('venv', 'bin', 'python')
        subprocess.run([python_exe, 'enhanced_download_data.py'])
        print("  ✅ Datasets downloaded and processed")
    except Exception as e:
        print(f"  ⚠️ Warning: {e}")
        print("  ℹ️ You can manually run: python enhanced_download_data.py")

def build_models():
    print("\n✓ Building ML models...")
    try:
        if os.name == 'nt':  # Windows
            python_exe = os.path.join('venv', 'Scripts', 'python.exe')
        else:
            python_exe = os.path.join('venv', 'bin', 'python')
        subprocess.run([python_exe, 'land_analysis_model.py'])
        print("  ✅ Models built and saved")
    except Exception as e:
        print(f"  ⚠️ Warning: {e}")
        print("  ℹ️ You can manually run: python land_analysis_model.py")

def print_final_instructions():
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print("\n🚀 To start the application:\n")
    
    if os.name == 'nt':  # Windows
        print("  1. Run: venv\\Scripts\\activate")
        print("  2. Run: python app.py")
    else:  # Linux/Mac
        print("  1. Run: source venv/bin/activate")
        print("  2. Run: python app.py")
    
    print("\n🌍 Then open your browser and go to: http://localhost:5000")
    print("\n📚 Documentation:")
    print("  - Full README: README.md")
    print("  - Project Summary: PROJECT_SUMMARY.md")
    print("  - API Docs: README.md (API Endpoints section)")
    print("\n" + "=" * 70)

def main():
    print_header()
    
    if not check_python():
        print("\n❌ Setup failed. Please install Python 3.8+")
        sys.exit(1)
    
    create_venv()
    install_dependencies()
    create_directories()
    download_datasets()
    build_models()
    print_final_instructions()

if __name__ == '__main__':
    main()
