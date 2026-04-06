import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from PIL import Image
import datetime
from pathlib import Path
import json
import hashlib
import hmac
import sqlite3
from datetime import timedelta
import base64
import time
from collections import defaultdict

st.set_page_config(page_title="Agri AI Pro", layout="wide", initial_sidebar_state="expanded")

# ==================== CSS STYLING ====================
def get_css(page):
    base_css = """
    .stApp {
        transition: background 0.5s ease;
    }
    .stButton button {
        border-radius:10px;
        height:3em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }
    h1, h2, h3 {
        text-align:center;
        font-family: 'Arial', sans-serif;
    }
    .card {
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .task-item {
        background: rgba(255,255,255,0.95);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #4caf50;
        color: #222222;
    }
    .task-item b, .task-item p {
        color: #222222;
    }
    """
    if page in ["auth_home", "auth_login", "auth_register"]:
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
        }
        h1, h2, h3 {
            color: #ffffff;
        }
        .card {
            background: rgba(255,255,255,0.95);
            color: #333333;
        }
        .card h1, .card h2, .card h3, .card p, .card b {
            color: #333333;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff6b6b, #ffa500);
            color: white;
        }
        .stTextInput input, .stNumberInput input, .stSlider div {
            color: #333333;
        }
        """
    elif page == "dashboard":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #1f3d23;
        }
        h1, h2, h3 {
            color: #1a5f2f;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1f3d23;
        }
        .stButton button {
            background: linear-gradient(45deg, #1a5f2f, #2ecc71);
            color: white;
        }
        """
    elif page == "upload":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);
            color: #1e4621;
        }
        h1, h2, h3 {
            color: #1b5e20;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1e4621;
        }
        .stButton button {
            background: linear-gradient(45deg, #4caf50, #81c784);
            color: white;
        }
        """
    elif page == "results":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            color: #7b3f00;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5a3400;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff9800, #ffb74d);
            color: white;
        }
        .crop-card {
            background: rgba(255,255,255,0.98);
            border-radius: 15px;
            padding: 10px;
            margin: 6px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            border-left: 4px solid #ff9800;
            transition: transform 0.25s ease, border-color 0.25s ease;
            min-height: 150px;
            width: 100%;
            aspect-ratio: 1 / 1;
        }
        .crop-card:hover {
            transform: translateY(-2px);
        }
        .crop-card.selected {
            border-left: 4px solid #4caf50;
            background: rgba(232, 245, 233, 0.98);
        }
        .crop-card h2 {
            font-size: 1.1rem;
            margin-bottom: 4px;
        }
        .crop-card p {
            font-size: 0.75rem;
            line-height: 1.3;
        }
        .crop-card small {
            color: #555555;
        }
        """
    elif page == "schedule":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            color: #7b3f00;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5a3400;
        }
        .calendar-month-card {
            background: rgba(255,255,255,0.98);
            border-radius: 25px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }
        .calendar-day {
            background: rgba(255,255,255,0.95);
            border-radius: 16px;
            padding: 12px;
            margin: 4px 0;
            text-align: left;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-height: 140px;
        }
        .calendar-day.completed {
            background: rgba(144,238,144,0.95);
        }
        .calendar-day strong {
            display: block;
            margin-bottom: 8px;
            font-size: 1.1rem;
        }
        .calendar-day small {
            color: #444444;
        }
        .month-title {
            font-size: 1.3rem;
            font-weight: 700;
            text-align: center;
            margin: 0 10px;
        }
        .stButton button {
            background: linear-gradient(45deg, #ff9800, #ffb74d);
            color: white;
        }
        """
    elif page == "market":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #ffcdd2 0%, #ffebee 100%);
            color: #7b1f1f;
        }
        h1, h2, h3 {
            color: #d32f2f;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #7b1f1f;
        }
        .stButton button {
            background: linear-gradient(45deg, #f44336, #ef5350);
            color: white;
        }
        """
    elif page == "profile":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            color: #1b5e20;
        }
        h1, h2, h3 {
            color: #1b5e20;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #1b5e20;
        }
        .stButton button {
            background: linear-gradient(45deg, #43a047, #66bb6a);
            color: white;
        }
        """
    elif page == "news":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #0d47a1;
        }
        h1, h2, h3 {
            color: #0d47a1;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #0d47a1;
        }
        .stButton button {
            background: linear-gradient(45deg, #1e88e5, #42a5f5);
            color: white;
        }
        """
    elif page == "selling_strategy":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #f1f8e9 0%, #dcedc8 100%);
            color: #33691e;
        }
        h1, h2, h3 {
            color: #33691e;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #33691e;
        }
        .stButton button {
            background: linear-gradient(45deg, #7cb342, #c0ca33);
            color: white;
        }
        """
    elif page == "government_subsidy":
        return base_css + """
        .stApp {
            background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
            color: #bf360c;
        }
        h1, h2, h3 {
            color: #bf360c;
        }
        .card, .metric-card, .task-item, .crop-card {
            color: #5d4037;
        }
        .stButton button {
            background: linear-gradient(45deg, #ffa726, #ffb74d);
            color: white;
        }
        """
    return base_css

# Initialize session state
conn = sqlite3.connect("farmers.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
c.execute('''CREATE TABLE IF NOT EXISTS farming_plans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    crop TEXT NOT NULL,
    start_date TEXT,
    land_images TEXT,
    soil_data TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (
    id INTEGER PRIMARY KEY,
    plan_id INTEGER NOT NULL,
    task_date TEXT,
    task_description TEXT,
    task_type TEXT,
    is_completed INTEGER DEFAULT 0,
    FOREIGN KEY(plan_id) REFERENCES farming_plans(id)
)''')
conn.commit()

REMEMBER_FILE = Path("remember_me.json")

def get_user_by_username(username):
    try:
        c = conn.cursor()
        c.execute("SELECT id, username, email FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user:
            return {"id": user[0], "username": user[1], "email": user[2]}
    except Exception:
        pass
    return None


def save_remembered_user(username, token):
    try:
        REMEMBER_FILE.write_text(json.dumps({"username": username, "token": token}), encoding="utf-8")
    except Exception:
        pass


def clear_remembered_user():
    try:
        if REMEMBER_FILE.exists():
            REMEMBER_FILE.unlink()
    except Exception:
        pass


def load_remembered_user():
    try:
        if REMEMBER_FILE.exists():
            data = json.loads(REMEMBER_FILE.read_text(encoding="utf-8"))
            username = data.get("username")
            token = data.get("token")
            if username and token:
                user = get_user_by_username(username)
                if user:
                    return user, token
    except Exception:
        pass
    return None, None


def save_farming_plan_to_db(user_id, plan):
    try:
        c = conn.cursor()
        soil_data = json.dumps({
            "soil_health": plan.get("soil_health"),
            "vegetation": plan.get("vegetation"),
            "soil_type": plan.get("soil_type"),
            "estimated_ph": plan.get("estimated_ph"),
            "weather": plan.get("weather"),
            "temp": plan.get("temp"),
            "humidity": plan.get("humidity"),
            "city": plan.get("city"),
            "area": plan.get("area"),
            "recommended_crop": plan.get("recommended_crop"),
            "short_term_crop": plan.get("short_term_crop"),
            "medium_term_crop": plan.get("medium_term_crop"),
            "long_term_crop": plan.get("long_term_crop")
        })
        land_images = json.dumps(plan.get("land_images", []))
        c.execute("SELECT id FROM farming_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
        existing = c.fetchone()
        if existing:
            c.execute("""UPDATE farming_plans SET crop=?, start_date=?, land_images=?, soil_data=?, status=? WHERE id=?""",
                      (plan.get("crop"), plan.get("start_date").isoformat(), land_images, soil_data, plan.get("status", "active"), existing[0]))
            plan_id = existing[0]
        else:
            c.execute("""INSERT INTO farming_plans (user_id, crop, start_date, land_images, soil_data, status) VALUES (?, ?, ?, ?, ?, ?)""",
                      (user_id, plan.get("crop"), plan.get("start_date").isoformat(), land_images, soil_data, plan.get("status", "active")))
            plan_id = c.lastrowid
        conn.commit()
        return plan_id
    except Exception:
        return None


def load_farming_plan_from_db(user_id):
    try:
        c = conn.cursor()
        c.execute("SELECT id, crop, start_date, land_images, soil_data, status FROM farming_plans WHERE user_id=? ORDER BY created_at DESC LIMIT 1", (user_id,))
        row = c.fetchone()
        if row:
            plan_id, crop, start_date, land_images_text, soil_data_text, status = row
            soil_data = json.loads(soil_data_text or "{}")
            return {
                "plan_id": plan_id,
                "crop": crop,
                "start_date": datetime.date.fromisoformat(start_date),
                "land_images": json.loads(land_images_text or "[]"),
                "status": status,
                **soil_data
            }
    except Exception:
        pass
    return None


def save_daily_tasks_to_db(plan_id, schedule):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM daily_tasks WHERE plan_id=?", (plan_id,))
        for item in schedule:
            c.execute("""INSERT INTO daily_tasks (plan_id, task_date, task_description, task_type, is_completed)
                         VALUES (?, ?, ?, ?, ?)""",
                      (plan_id, item["date"], item["task"], item["type"], 1 if item.get("completed") else 0))
        conn.commit()
    except Exception:
        pass


def load_daily_tasks_from_db(plan_id):
    try:
        c = conn.cursor()
        c.execute("SELECT task_date, task_description, task_type, is_completed FROM daily_tasks WHERE plan_id=? ORDER BY task_date", (plan_id,))
        rows = c.fetchall()
        schedule = []
        for row in rows:
            schedule.append({
                "date": row[0],
                "task": row[1],
                "type": row[2],
                "completed": bool(row[3])
            })
        return schedule
    except Exception:
        return []


def update_task_completion(plan_id, task_date, completed):
    try:
        c = conn.cursor()
        c.execute("UPDATE daily_tasks SET is_completed=? WHERE plan_id=? AND task_date=?", (1 if completed else 0, plan_id, task_date))
        conn.commit()
    except Exception:
        pass


def load_user_data(user_id):
    plan = load_farming_plan_from_db(user_id)
    if plan:
        st.session_state.farming_plan = plan
        st.session_state.crop = plan.get("crop", st.session_state.crop)
        st.session_state.plan_id = plan.get("plan_id")
        schedule = load_daily_tasks_from_db(plan["plan_id"])
        if schedule:
            st.session_state.schedule = schedule
            st.session_state.tasks_completed = {item["date"]: item["completed"] for item in schedule}

if "language" not in st.session_state:
    st.session_state.language = "en"

if "page" not in st.session_state:
    st.session_state.page = "auth_home"
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.images = []
    st.session_state.crop = ""
    st.session_state.location = None
    st.session_state.schedule = []
    st.session_state.tasks_completed = {}
    st.session_state.farming_plan = None
    st.session_state.plan_id = None
    remembered_user, remembered_token = load_remembered_user()
    if remembered_user:
        st.session_state.user = remembered_user
        st.session_state.token = remembered_token
        st.session_state.page = "dashboard"
        load_user_data(remembered_user["id"])

st.markdown(f"<style>{get_css(st.session_state.page)}</style>", unsafe_allow_html=True)

# ==================== DATABASE SETUP ====================
def init_db():
    conn = sqlite3.connect("farmers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        location TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS farming_plans (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        crop TEXT NOT NULL,
        start_date TEXT,
        land_images TEXT,
        soil_data TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (
        id INTEGER PRIMARY KEY,
        plan_id INTEGER NOT NULL,
        task_date TEXT,
        task_description TEXT,
        task_type TEXT,
        is_completed INTEGER DEFAULT 0,
        FOREIGN KEY(plan_id) REFERENCES farming_plans(id)
    )''')
    conn.commit()
    return conn

conn = init_db()

# ==================== JWT AUTHENTICATION ====================
SECRET_KEY = "agri_ai_pro_secret_key_2024_farming"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt_token(user_id, username):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": (datetime.datetime.now() + timedelta(days=30)).isoformat()
    }
    header_json = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_json = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    signature = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), f"{header_json}.{payload_json}".encode(), hashlib.sha256).digest()
    ).decode().rstrip('=')
    return f"{header_json}.{payload_json}.{signature}"

def verify_jwt_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload_data = base64.urlsafe_b64decode(parts[1] + '==')
        return json.loads(payload_data)
    except:
        return None

# ==================== USER MANAGEMENT ====================
def register_user(username, password, email, phone):
    try:
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                  (username, hashed_pwd, email, phone))
        conn.commit()
        return True, "✅ Registration successful! Please login."
    except sqlite3.IntegrityError:
        return False, "❌ Username already exists!"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def authenticate_user(username, password):
    try:
        c = conn.cursor()
        hashed_pwd = hash_password(password)
        c.execute("SELECT id, username, email FROM users WHERE username=? AND password=?", (username, hashed_pwd))
        user = c.fetchone()
        if user:
            token = create_jwt_token(user[0], user[1])
            return True, token, {"id": user[0], "username": user[1], "email": user[2]}
        return False, None, None
    except Exception as e:
        return False, None, None

def get_shopping_requirements(crop_name, area_hectares):
    """Get crop-specific shopping requirements with real-world pricing"""
    requirements = {
        "tomato": {
            "seeds": {"name": "Tomato Seeds (Hybrid)", "quantity": f"{int(area_hectares * 500)}g", "price": int(area_hectares * 1500), "unit": "packs"},
            "fertilizer": {"name": "NPK Fertilizer (19-19-19)", "quantity": f"{int(area_hectares * 50)}kg", "price": int(area_hectares * 3000), "unit": "bags"},
            "organic": {"name": "Organic Compost", "quantity": f"{int(area_hectares * 1000)}kg", "price": int(area_hectares * 2000), "unit": "tons"},
            "pesticide": {"name": "Organic Pesticide", "quantity": f"{int(area_hectares * 2)}L", "price": int(area_hectares * 800), "unit": "bottles"},
            "tools": {"name": "Farm Tools & Equipment", "quantity": "1 set", "price": 2500, "unit": "set"},
            "irrigation": {"name": "Drip Irrigation Parts", "quantity": f"{int(area_hectares * 100)}m", "price": int(area_hectares * 1500), "unit": "meters"}
        },
        "maize": {
            "seeds": {"name": "Maize Seeds (Hybrid)", "quantity": f"{int(area_hectares * 25)}kg", "price": int(area_hectares * 2000), "unit": "bags"},
            "fertilizer": {"name": "Urea Fertilizer", "quantity": f"{int(area_hectares * 80)}kg", "price": int(area_hectares * 2500), "unit": "bags"},
            "organic": {"name": "Farm Yard Manure", "quantity": f"{int(area_hectares * 2000)}kg", "price": int(area_hectares * 1500), "unit": "tons"},
            "pesticide": {"name": "Herbicide", "quantity": f"{int(area_hectares * 3)}L", "price": int(area_hectares * 1200), "unit": "bottles"},
            "tools": {"name": "Maize Farming Tools", "quantity": "1 set", "price": 3000, "unit": "set"},
            "irrigation": {"name": "Sprinkler System", "quantity": f"{int(area_hectares * 50)}m", "price": int(area_hectares * 2000), "unit": "meters"}
        },
        "ragi": {
            "seeds": {"name": "Finger Millet Seeds", "quantity": f"{int(area_hectares * 15)}kg", "price": int(area_hectares * 1200), "unit": "bags"},
            "fertilizer": {"name": "Organic Fertilizer", "quantity": f"{int(area_hectares * 30)}kg", "price": int(area_hectares * 1500), "unit": "bags"},
            "organic": {"name": "Vermicompost", "quantity": f"{int(area_hectares * 800)}kg", "price": int(area_hectares * 1200), "unit": "tons"},
            "pesticide": {"name": "Bio-pesticide", "quantity": f"{int(area_hectares * 1.5)}L", "price": int(area_hectares * 600), "unit": "bottles"},
            "tools": {"name": "Traditional Farm Tools", "quantity": "1 set", "price": 2000, "unit": "set"}
        },
        "paddy": {
            "seeds": {"name": "Paddy Seeds (Improved)", "quantity": f"{int(area_hectares * 40)}kg", "price": int(area_hectares * 1800), "unit": "bags"},
            "fertilizer": {"name": "Complex Fertilizer", "quantity": f"{int(area_hectares * 60)}kg", "price": int(area_hectares * 2800), "unit": "bags"},
            "organic": {"name": "Bio-fertilizer", "quantity": f"{int(area_hectares * 500)}kg", "price": int(area_hectares * 1800), "unit": "tons"},
            "pesticide": {"name": "Insecticide", "quantity": f"{int(area_hectares * 2.5)}L", "price": int(area_hectares * 1000), "unit": "bottles"},
            "tools": {"name": "Paddy Farming Equipment", "quantity": "1 set", "price": 3500, "unit": "set"},
            "irrigation": {"name": "Water Pump & Pipes", "quantity": "1 set", "price": int(area_hectares * 2500), "unit": "set"}
        },
        "cotton": {
            "seeds": {"name": "Bt Cotton Seeds", "quantity": f"{int(area_hectares * 5)}kg", "price": int(area_hectares * 3000), "unit": "packs"},
            "fertilizer": {"name": "DAP Fertilizer", "quantity": f"{int(area_hectares * 70)}kg", "price": int(area_hectares * 3500), "unit": "bags"},
            "organic": {"name": "Organic Manure", "quantity": f"{int(area_hectares * 1200)}kg", "price": int(area_hectares * 2200), "unit": "tons"},
            "pesticide": {"name": "Cotton Specific Pesticide", "quantity": f"{int(area_hectares * 4)}L", "price": int(area_hectares * 2000), "unit": "bottles"},
            "tools": {"name": "Cotton Picking Tools", "quantity": "1 set", "price": 4000, "unit": "set"}
        }
    }
    
    # Default for other crops
    default_requirements = {
        "seeds": {"name": f"{crop_name.title()} Seeds", "quantity": f"{int(area_hectares * 20)}kg", "price": int(area_hectares * 1500), "unit": "bags"},
        "fertilizer": {"name": "General Purpose Fertilizer", "quantity": f"{int(area_hectares * 50)}kg", "price": int(area_hectares * 2500), "unit": "bags"},
        "organic": {"name": "Organic Compost", "quantity": f"{int(area_hectares * 1000)}kg", "price": int(area_hectares * 1800), "unit": "tons"},
        "pesticide": {"name": "General Pesticide", "quantity": f"{int(area_hectares * 2)}L", "price": int(area_hectares * 800), "unit": "bottles"},
        "tools": {"name": "Basic Farm Tools", "quantity": "1 set", "price": 2500, "unit": "set"}
    }
    
    return requirements.get(crop_name.lower(), default_requirements)

def get_nearest_markets(location):
    """Get nearest agricultural markets with real market names"""
    markets = {
        "bangalore": [
            {"name": "KR Market", "distance": "2 km", "address": "Krishna Rajendra Market, Bangalore"},
            {"name": "Yelahanka Market", "distance": "15 km", "address": "Yelahanka Agricultural Market, Bangalore"},
            {"name": "Hoskote Market", "distance": "25 km", "address": "Hoskote Agricultural Yard, Bangalore Rural"}
        ],
        "mysore": [
            {"name": "Mysore APMC Market", "distance": "3 km", "address": "APMC Market, Mysore"},
            {"name": "Nazarbad Market", "distance": "5 km", "address": "Nazarbad Agricultural Market, Mysore"},
            {"name": "Hootagalli Market", "distance": "8 km", "address": "Hootagalli Market Yard, Mysore"}
        ],
        "tumkur": [
            {"name": "Tumkur APMC", "distance": "2 km", "address": "APMC Market, Tumkur"},
            {"name": "Kunigal Market", "distance": "20 km", "address": "Kunigal Agricultural Market"},
            {"name": "Gubbi Market", "distance": "25 km", "address": "Gubbi Market Yard"}
        ],
        "mandya": [
            {"name": "Mandya Sugar Market", "distance": "2 km", "address": "Mandya Agricultural Market"},
            {"name": "Maddur Market", "distance": "15 km", "address": "Maddur APMC Market"},
            {"name": "Srirangapatna Market", "distance": "18 km", "address": "Srirangapatna Agricultural Market"}
        ]
    }
    
    # Default markets for other locations
    default_markets = [
        {"name": "Local APMC Market", "distance": "5 km", "address": "Nearest Agricultural Market"},
        {"name": "District Market Yard", "distance": "10 km", "address": "District Agricultural Market"},
        {"name": "Regional Market", "distance": "20 km", "address": "Regional Agricultural Market"}
    ]
    
    location_key = location.lower().split()[0] if location else "default"
    return markets.get(location_key, default_markets)

def get_translated_text(text, lang_code):
    translations = {
        "en": {
            "dashboard": "Dashboard",
            "profile_settings": "Profile Settings",
            "news": "News",
            "selling_strategy": "Selling Strategy",
            "government_subsidies": "Government Subsidies",
            "logout": "Logout",
            "start_farming": "Start Farming",
            "view_schedule": "View Schedule",
            "market_insights": "Market Insights",
            "language": "Language",
            "weather": "Weather",
            "temperature": "Temperature",
            "humidity": "Humidity",
            "location": "Location",
            "shopping_requirements": "Pre-Farming Shopping Requirements",
            "seeds": "Seeds",
            "fertilizer": "Fertilizer",
            "organic": "Organic Manure",
            "pesticide": "Pesticide",
            "tools": "Tools & Equipment",
            "irrigation": "Irrigation",
            "quantity": "Quantity",
            "price": "Price",
            "nearest_markets": "Nearest Agricultural Markets",
            "purchase_checklist": "Purchase Checklist",
            "mark_as_purchased": "Mark as Purchased",
            "total_cost": "Total Estimated Cost",
            "proceed_to_calendar": "Proceed to Farming Calendar",
            "back_to_results": "Back to Results",
            "profile": "Profile",
            "personal_details": "Personal Details",
            "account_status": "Account Status",
            "name": "Name",
            "email": "Email",
            "designation": "Designation",
            "role": "Role",
            "member_since": "Member Since",
            "status": "Status",
            "verified": "Verified",
            "farming_activity": "Farming Activity",
            "current_crop": "Current Crop",
            "land_area": "Land Area",
            "start_date": "Start Date",
            "agriculture_news": "Agriculture News",
            "todays_headlines": "Today's Top Agriculture Headlines",
            "source": "Source",
            "date": "Date",
            "selling_strategies": "Best Selling Strategies",
            "price_range": "Price Range",
            "current_demand": "Current Demand",
            "best_markets": "Best Markets",
            "best_time": "Best Time",
            "selling_strategy": "Selling Strategy",
            "view_market_rates": "View Market Rates",
            "congratulations": "Congratulations!",
            "farming_completed": "All farming days completed. Ready for harvest!",
            "back_to_dashboard": "Back to Dashboard"
        },
        "hi": {
            "dashboard": "डैशबोर्ड",
            "profile_settings": "प्रोफाइल सेटिंग्स",
            "news": "समाचार",
            "selling_strategy": "बिक्री रणनीति",
            "government_subsidies": "सरकारी सब्सिडी",
            "logout": "लॉगआउट",
            "start_farming": "खेती शुरू करें",
            "view_schedule": "अनुसूची देखें",
            "market_insights": "बाजार जानकारी",
            "language": "भाषा",
            "weather": "मौसम",
            "temperature": "तापमान",
            "humidity": "नमी",
            "location": "स्थान",
            "shopping_requirements": "खेती से पहले खरीदारी आवश्यकताएं",
            "seeds": "बीज",
            "fertilizer": "उर्वरक",
            "organic": "जैविक खाद",
            "pesticide": "कीटनाशक",
            "tools": "उपकरण और उपकरण",
            "irrigation": "सिंचाई",
            "quantity": "मात्रा",
            "price": "कीमत",
            "nearest_markets": "निकटतम कृषि बाजार",
            "purchase_checklist": "खरीद सूची",
            "mark_as_purchased": "खरीदे गए के रूप में चिह्नित करें",
            "total_cost": "कुल अनुमानित लागत",
            "proceed_to_calendar": "खेती कैलेंडर पर जाएं",
            "back_to_results": "परिणामों पर वापस जाएं",
            "profile": "प्रोफाइल",
            "personal_details": "व्यक्तिगत विवरण",
            "account_status": "खाता स्थिति",
            "name": "नाम",
            "email": "ईमेल",
            "designation": "पद",
            "role": "भूमिका",
            "member_since": "सदस्यता दिनांक",
            "status": "स्थिति",
            "verified": "सत्यापित",
            "farming_activity": "खेती गतिविधि",
            "current_crop": "वर्तमान फसल",
            "land_area": "भूमि क्षेत्र",
            "start_date": "प्रारंभ तिथि",
            "agriculture_news": "कृषि समाचार",
            "todays_headlines": "आज की प्रमुख कृषि सुर्खियां",
            "source": "स्रोत",
            "date": "तिथि",
            "selling_strategies": "सर्वोत्तम बिक्री रणनीतियां",
            "price_range": "मूल्य सीमा",
            "current_demand": "वर्तमान मांग",
            "best_markets": "सर्वोत्तम बाजार",
            "best_time": "सर्वोत्तम समय",
            "selling_strategy": "बिक्री रणनीति",
            "view_market_rates": "बाजार दरें देखें",
            "congratulations": "बधाई हो!",
            "farming_completed": "सभी खेती दिन पूर्ण हुए। फसल काटने के लिए तैयार!",
            "back_to_dashboard": "डैशबोर्ड पर वापस जाएं"
        },
        "te": {
            "dashboard": "డాష్బోర్డ్",
            "profile_settings": "ప్రొఫైల్ సెట్టింగ్‌లు",
            "news": "వార్తలు",
            "selling_strategy": "అమ్మకాల వ్యూహం",
            "government_subsidies": "ప్రభుత్వ సబ్సిడీలు",
            "logout": "లాగ్‌అవుట్",
            "start_farming": "వ్యవసాయం ప్రారంభించండి",
            "view_schedule": "షెడ్యూల్ చూడండి",
            "market_insights": "మార్కెట్ విశ్లేషణలు",
            "language": "భాష",
            "weather": "వాతావరణం",
            "temperature": "ఉష్ణోగ్రత",
            "humidity": "తేమ",
            "location": "స్థానం",
            "shopping_requirements": "వ్యవసాయం ముందు కొనుగోలు అవసరాలు",
            "seeds": "విత్తనాలు",
            "fertilizer": "ఎరువులు",
            "organic": "సేంద్రీయ ఎరువు",
            "pesticide": "కీటకనాశకాలు",
            "tools": "పనిముట్లు మరియు పరికరాలు",
            "irrigation": "నీటిపారుదల",
            "quantity": "పరిమాణం",
            "price": "�ర",
            "nearest_markets": "సమీప వ్యవసాయ మార్కెట్లు",
            "purchase_checklist": "కొనుగోలు చెక్‌లిస్ట్",
            "mark_as_purchased": "కొనుగోలు చేసినట్లు గుర్తించండి",
            "total_cost": "మొత్తం అంచనా ఖర్చు",
            "proceed_to_calendar": "వ్యవసాయ క్యాలెండర్‌కు వెళ్ళండి",
            "back_to_results": "ఫలితాలకు తిరిగి వెళ్ళండి"
        },
        "kn": {
            "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "profile_settings": "ಪ್ರೊಫೈಲ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
            "news": "ಸುದ್ದಿಗಳು",
            "selling_strategy": "ಮಾರಾಟ ತಂತ್ರ",
            "government_subsidies": "ಸರ್ಕಾರಿ ಸಹಾಯಧನ",
            "logout": "ಲಾಗ್‌ಔಟ್",
            "start_farming": "ಕೃಷಿ ಪ್ರಾರಂಭಿಸಿ",
            "view_schedule": "ವೇಳಾಪಟ್ಟಿ ನೋಡಿ",
            "market_insights": "ಮಾರುಕಟ್ಟೆ ಒಳನೋಟಗಳು",
            "language": "ಭಾಷೆ",
            "weather": "ಹವಾಮಾನ",
            "temperature": "ತಾಪಮಾನ",
            "humidity": "ಆರ್ದ್ರತೆ",
            "location": "ಸ್ಥಳ",
            "shopping_requirements": "ಕೃಷಿಗೆ ಮೊದಲು ಖರೀದಿ ಅಗತ್ಯಗಳು",
            "seeds": "ಬೀಜಗಳು",
            "fertilizer": "ರಸಗೊಬ್ಬರ",
            "organic": "ಜೈವಿಕ ಗೊಬ್ಬರ",
            "pesticide": "ಕೀಟನಾಶಕಗಳು",
            "tools": "ಉಪಕರಣಗಳು ಮತ್ತು ಸಲಕರಣೆಗಳು",
            "irrigation": "ನೀರಾವರಿ",
            "quantity": "ಪ್ರಮಾಣ",
            "price": "ಬೆಲೆ",
            "nearest_markets": "ಹತ್ತಿರದ ಕೃಷಿ ಮಾರುಕಟ್ಟೆಗಳು",
            "purchase_checklist": "ಖರೀದಿ ಚೆಕ್‌ಲಿಸ್ಟ್",
            "mark_as_purchased": "ಖರೀದಿಸಿದಂತೆ ಗುರುತಿಸಿ",
            "total_cost": "ಒಟ್ಟು ಅಂದಾಜು ವೆಚ್ಚ",
            "proceed_to_calendar": "ಕೃಷಿ ಕ್ಯಾಲೆಂಡರ್‌ಗೆ ಹೋಗಿ",
            "back_to_results": "ಫಲಿತಾಂಶಗಳಿಗೆ ಹಿಂದಿರುಗಿ"
        }
    }
    return translations.get(lang_code, {}).get(text, text)

@st.cache_data
def load_data():
    try:
        csv_path = Path("crop-recommendation-dataset/Crop_recommendation.csv")
        if csv_path.exists():
            return pd.read_csv(csv_path)
        else:
            st.warning("Dataset not found. Using default crop recommendations.")
            return pd.DataFrame(columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame(columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])

@st.cache_data
def build_model():
    try:
        data = load_data()
        if data.empty or 'label' not in data.columns:
            return None, None
        X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = data['label']
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y)
        return model, scaler
    except Exception as e:
        st.error(f"Error building model: {e}")
        return None, None

model, scaler = build_model()

CROP_DURATION = {
    'rice': 120, 'maize': 120, 'cotton': 180, 'sugarcane': 360, 'wheat': 120,
    'chickpea': 100, 'soybean': 100, 'kidneybeans': 90, 'pigeonpea': 240,
    'mothbeans': 90, 'pomegranate': 180, 'papaya': 180, 'tomato': 90,
    'arecanut': 180, 'coconut': 180, 'jute': 120, 'coffee': 180, 'tea': 180
}

FARMING_TASKS = {
    'general': [
        {'day': 0, 'type': 'soil_prep', 'task': '🌱 Prepare soil - Plow and add organic matter'},
        {'day': 2, 'type': 'seed', 'task': '🌾 Sow seeds at appropriate depth and spacing'},
        {'day': 7, 'type': 'water', 'task': '💧 First irrigation - Ensure soil moisture'},
        {'day': 14, 'type': 'fertilizer', 'task': '🧪 Apply nitrogen-based fertilizer'},
        {'day': 25, 'type': 'water', 'task': '💧 Second irrigation'},
        {'day': 35, 'type': 'fertilizer', 'task': '🧪 Apply phosphorus-based fertilizer'},
        {'day': 45, 'type': 'pest', 'task': '🐛 Monitor and control pests'},
        {'day': 60, 'type': 'water', 'task': '💧 Third irrigation - Critical stage'},
        {'day': 75, 'type': 'weed', 'task': '🌿 Remove weeds and loose soil'},
        {'day': 90, 'type': 'fertilizer', 'task': '🧪 Final fertilizer application'},
    ]
}

TERM_CROPS = {
    'short_term': 'tomato',
    'medium_term': 'maize',
    'long_term': 'sugarcane'
}

CROP_DETAILS = {
    'tomato': 'Short-term crop with fast harvest. Requires regular watering and balanced fertilizer.',
    'maize': 'Medium-term crop with good yield. Needs warm temperature and consistent rainfall.',
    'sugarcane': 'Long-term crop suited for sustained farming cycles with high water requirement.',
}

# ==================== IMAGE ANALYSIS ====================
def is_valid_land_image(image):
    """Validate if image is actually a land/field image"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) < 2:
            return False, "Invalid image format"
        
        if img_array.shape[0] < 100 or img_array.shape[1] < 100:
            return False, "Image too small - needs to be at least 100x100 pixels"
        
        if len(img_array.shape) == 3:
            std_dev = np.std(img_array)
            if std_dev < 10:
                return False, "Image appears to be a solid color - not a land image"
            
            green = np.mean(img_array[:,:,1])
            red = np.mean(img_array[:,:,0])
            blue = np.mean(img_array[:,:,2])
            
            if green < 30 and red < 30 and blue < 30:
                return False, "Image is too dark - not recognizable as land"
            
            if green > 200 and red > 200 and blue > 200:
                return False, "Image is too bright/washed out"
        
        return True, "✅ Valid land image detected"
    except Exception as e:
        return False, f"Error analyzing image: {str(e)}"

def analyze_soil_quality(image):
    """Analyze soil quality from image including color detection"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            # Calculate average colors
            avg_r = img_array[:,:,0].mean()
            avg_g = img_array[:,:,1].mean()
            avg_b = img_array[:,:,2].mean()
            
            brown_score = abs(avg_r - avg_b) * 0.5
            green_score = max(0, avg_g - 80) * 1.5
            
            # Estimate soil type based on RGB
            if avg_r > avg_g and avg_r > avg_b:  # Reddish
                soil_type = "Clay Soil"
                estimated_ph = 6.5
            elif avg_g > avg_r and avg_g > avg_b:  # Greenish
                soil_type = "Loamy Soil"
                estimated_ph = 6.8
            elif avg_b > avg_r and avg_b > avg_g:  # Bluish (rare)
                soil_type = "Sandy Soil"
                estimated_ph = 7.0
            else:
                soil_type = "Alluvial Soil"
                estimated_ph = 7.2
            
            soil_health = min(100, max(0, (brown_score + green_score) / 2))
            vegetation_index = max(0, green_score / 2)
            
            return soil_health, vegetation_index, soil_type, estimated_ph
        return 50, 50, "Unknown", 7.0
    except:
        return 50, 50, "Unknown", 7.0

def get_weather(city):
    """Get real weather data"""
    try:
        API_KEY = "ce07d5d5aa68971127720f35a704aa4e"
        if not city or city.strip() == "":
            return 25, 60, "Unknown"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url, timeout=5).json()
        if res.get('cod') == 200:
            return (res.get('main', {}).get('temp', 25), 
                   res.get('main', {}).get('humidity', 60),
                   res.get('weather', [{}])[0].get('main', 'Clear'))
        return 25, 60, "Unknown"
    except:
        return 25, 60, "Unknown"

def get_location():
    """Get user location"""
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5).json()
        city = res.get('city', 'Bangalore')
        country = res.get('country_name', 'India')
        if city and city != 'Unknown':
            return f"{city}, {country}"
        else:
            return "Bangalore, India"
    except:
        return "Bangalore, India"


def get_daily_agri_news():
    newspaper_feed = {
        "The Hindu": [
            {
                "title": "Kharif MSP Boost Brings Relief to Farmers",
                "summary": "The Hindu reports higher procurement rates for paddy, cotton and sugarcane this season to support rural incomes.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Farmers Adopt Smart Irrigation to Fight Heatwaves",
                "summary": "New drip irrigation subsidies are helping farmers reduce water use and increase productivity.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Organic Food Demand Climbs Across India",
                "summary": "Demand for certified organic vegetables and fruits is on the rise, offering higher margins for small farmers.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ],
        "Times of India": [
            {
                "title": "Agri Tech Startups Help Farmers Track Crop Health",
                "summary": "IoT sensors and mobile apps are helping farmers detect pests early and improve yields.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "New Solar Pumps Expand Irrigation Options",
                "summary": "Farmers are installing solar water pumps to reduce diesel costs and increase irrigation reliability.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Local Produce Markets See Higher Prices",
                "summary": "Rising demand for fresh vegetables has pushed up prices, especially for onions, tomatoes and leafy greens.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ],
        "Indian Express": [
            {
                "title": "Government Launches New Farm Credit Scheme",
                "summary": "The government is offering low-interest loans to promote crop diversification and climate-smart agriculture.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Pulses Production Expected to Rise",
                "summary": "Higher procurement support and improved seed distribution are set to boost pulse farming this year.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            },
            {
                "title": "Farmers Use Drones for Soil and Pest Monitoring",
                "summary": "Drone technology is becoming affordable and is now widely used for crop scouting.",
                "date": datetime.date.today().strftime('%B %d, %Y')
            }
        ]
    }
    sources = list(newspaper_feed.keys())
    source_index = (datetime.date.today().day - 1) % len(sources)
    source_name = sources[source_index]
    news_items = newspaper_feed[source_name]
    for item in news_items:
        item["source"] = source_name
    return source_name, news_items


def generate_farming_schedule(crop, start_date, duration=None):
    """Generate day-by-day farming schedule"""
    if duration is None:
        duration = CROP_DURATION.get(crop.lower(), 120)
    
    schedule = []
    tasks = FARMING_TASKS.get('general', [])
    task_map = {task['day']: task for task in tasks}
    
    for day_count in range(duration + 1):
        current_date = start_date + timedelta(days=day_count)
        if day_count == duration:
            task_text = '🌾 HARVEST DAY - Ready for market!'
            task_type = 'harvest'
        elif day_count in task_map:
            task_text = task_map[day_count]['task']
            task_type = task_map[day_count]['type']
        elif day_count % 7 == 0:
            task_text = '💧 Weekly field check - inspect soil moisture and pests.'
            task_type = 'weekly_check'
        else:
            task_text = '🌿 Daily care: monitor soil moisture, weeds, and crop health.'
            task_type = 'daily'
        
        schedule.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': day_count,
            'task': task_text,
            'type': task_type,
            'completed': False
        })
    
    return schedule

# ==================== PAGE: AUTHENTICATION HOME ====================
if st.session_state.page == "auth_home":
    st.title("🌾 Agri AI Pro")
    st.markdown("<h3>Professional Farmer Advisory System</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>🚀 Welcome Farmer</h3>
            <p>Choose to Login or Create a New Account</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔐 LOGIN", use_container_width=True, key="goto_login"):
                st.session_state.page = "auth_login"
                st.rerun()
        
        with col2:
            if st.button("📝 REGISTER", use_container_width=True, key="goto_register"):
                st.session_state.page = "auth_register"
                st.rerun()

# ==================== PAGE: LOGIN ====================
elif st.session_state.page == "auth_login":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="card"><h2>🔐 Login</h2></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("LOGIN", use_container_width=True):
                if username and password:
                    success, token, user = authenticate_user(username, password)
                    if success:
                        st.session_state.token = token
                        st.session_state.user = user
                        save_remembered_user(user['username'], token)
                        load_user_data(user['id'])
                        st.session_state.page = "dashboard"
                        st.success(f"✅ Welcome {user['username']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
                else:
                    st.error("❌ Please enter username and password!")
        
        with col2:
            if st.button("BACK", use_container_width=True):
                st.session_state.page = "auth_home"
                st.rerun()

# ==================== PAGE: REGISTER ====================
elif st.session_state.page == "auth_register":
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown('<div class="card"><h2>📝 Register</h2></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("REGISTER", use_container_width=True):
                if not username or not email or not phone or not password or not password_confirm:
                    st.error("❌ Fill all fields!")
                elif password != password_confirm:
                    st.error("❌ Passwords don't match!")
                elif len(password) < 6:
                    st.error("❌ Password must be 6+ characters!")
                elif "@" not in email:
                    st.error("❌ Invalid email!")
                else:
                    success, msg = register_user(username, password, email, phone)
                    if success:
                        st.success("✅ Registration successful!")
                        st.info("Go back and login!")
                        time.sleep(2)
                        st.session_state.page = "auth_home"
                        st.rerun()
                    else:
                        st.error(msg)
        
        with col2:
            if st.button("BACK", use_container_width=True):
                st.session_state.page = "auth_home"
                st.rerun()

# ==================== PAGE: DASHBOARD ====================
elif st.session_state.page == "dashboard":
    
    # Enhanced Sidebar with Better Design
    with st.sidebar:
        # Custom styled header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        ">
            <h2 style="margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 600;">
                👨‍🌾 Farmer Portal
            </h2>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
                Your Complete Farming Companion
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Language Selector with Enhanced Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        ">
            <h4 style="margin: 0 0 10px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                🌐 Language / भाषा / భాష / ಭಾಷೆ
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        language_options = {
            'en': '🇺🇸 English',
            'hi': '🇮🇳 हिंदी',
            'te': '🇮🇳 తెలుగు',
            'kn': '🇮🇳 ಕನ್ನಡ'
        }
        
        selected_lang = st.selectbox(
            "",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            key="language_selector"
        )
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        # Navigation Menu with Enhanced Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        ">
            <h4 style="margin: 0 0 15px 0; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                📱 Quick Navigation
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Navigation Buttons
        nav_buttons = [
            ("👤", get_translated_text("profile_settings", st.session_state.language), "profile"),
            ("📰", get_translated_text("news", st.session_state.language), "news"),
            ("💼", get_translated_text("selling_strategy", st.session_state.language), "selling_strategy"),
            ("🏛️", get_translated_text("government_subsidies", st.session_state.language), "government_subsidy"),
        ]
        
        for icon, text, page in nav_buttons:
            if st.button(f"{icon} {text}", use_container_width=True, key=f"nav_{page}"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        
        # Logout Button with Special Styling
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        ">
        """, unsafe_allow_html=True)
        
        if st.button("🚪 " + get_translated_text("logout", st.session_state.language), 
                     use_container_width=True, key="logout_btn"):
            clear_remembered_user()
            st.session_state.page = "auth_home"
            st.session_state.token = None
            st.session_state.user = None
            st.session_state.crop = ""
            st.session_state.schedule = []
            st.session_state.tasks_completed = {}
            st.session_state.farming_plan = None
            st.session_state.plan_id = None
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.title("🌾 Agri AI Pro Dashboard")
    
    location = get_location()
    temp, humidity, weather_condition = get_weather(location.split(',')[0] if location else "")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>🌡️ {get_translated_text("temperature", st.session_state.language)}</h3>
            <h2>{temp}°C</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>💧 {get_translated_text("humidity", st.session_state.language)}</h3>
            <h2>{humidity}%</h2>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>🌤️ {get_translated_text("weather", st.session_state.language)}</h3>
            <h2>{weather_condition}</h2>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>📍 {get_translated_text("location", st.session_state.language)}</h3>
            <h2>{location}</h2>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚜 " + get_translated_text("start_farming", st.session_state.language), use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()
    
    with col2:
        if st.button("📅 " + get_translated_text("view_schedule", st.session_state.language), use_container_width=True):
            if st.session_state.farming_plan:
                st.session_state.page = "schedule"
                st.rerun()
            else:
                st.warning("⚠️ Please start farming first")
    
    with col3:
        if st.button("📈 " + get_translated_text("market_insights", st.session_state.language), use_container_width=True):
            if st.session_state.crop:
                st.session_state.page = "market"
                st.rerun()
            else:
                st.warning("⚠️ Please analyze land first")

# ==================== PAGE: LAND ANALYSIS & IMAGE UPLOAD ====================
elif st.session_state.page == "upload":
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("📸 Land Analysis & Image Upload")
    
    st.markdown("### 📷 Upload Land Images (3 views)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🔭 Far View")
        img1 = st.file_uploader("Upload far view of your land", type=["jpg", "png", "jpeg"], key="far_view")
        if img1:
            st.image(img1, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img1))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    with col2:
        st.markdown("#### 📷 Mid View")
        img2 = st.file_uploader("Upload mid view of your land", type=["jpg", "png", "jpeg"], key="mid_view")
        if img2:
            st.image(img2, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img2))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    with col3:
        st.markdown("#### 🔍 Close View")
        img3 = st.file_uploader("Upload close view of your land", type=["jpg", "png", "jpeg"], key="close_view")
        if img3:
            st.image(img3, use_column_width=True)
            is_valid, msg = is_valid_land_image(Image.open(img3))
            if is_valid:
                st.success(msg)
            else:
                st.error(f"❌ {msg}")
    
    st.markdown("---")
    st.markdown("### 🌱 Soil & Environmental Data")
    
    detected_location = get_location()
    default_city = detected_location.split(',')[0] if detected_location else ""
    
    col1, col2 = st.columns(2)
    
    with col1:
        city = st.text_input("🏙️ City/Village", value=default_city, key="city_input")
        ph = st.slider("🧪 Soil pH (3-9)", 3.0, 9.0, 6.5)
        area = st.number_input("📏 Land Area (acres)", min_value=0.1, value=1.0, step=0.1, key="area_input")
    
    with col2:
        rainfall = st.slider("🌧️ Rainfall (mm)", 50, 300, 150)
        nitrogen = st.slider("🧬 Nitrogen Level (ppm)", 10, 100, 40)
    
    st.markdown("---")
    
    if st.button("🔍 ANALYZE LAND & PREDICT CROP", use_container_width=True):
        if img1 and img2 and img3:
            if not city:
                city = default_city
            with st.spinner("🔄 Analyzing your land..."):
                img1_valid, msg1 = is_valid_land_image(Image.open(img1))
                img2_valid, msg2 = is_valid_land_image(Image.open(img2))
                img3_valid, msg3 = is_valid_land_image(Image.open(img3))
                
                if not (img1_valid and img2_valid and img3_valid):
                    st.error("❌ One or more images are invalid land images. Please upload actual land/field photos.")
                    if not img1_valid:
                        st.error(f"Far View: {msg1}")
                    if not img2_valid:
                        st.error(f"Mid View: {msg2}")
                    if not img3_valid:
                        st.error(f"Close View: {msg3}")
                else:
                    soil1, veg1, soil_type1, ph_est1 = analyze_soil_quality(Image.open(img1))
                    soil2, veg2, soil_type2, ph_est2 = analyze_soil_quality(Image.open(img2))
                    soil3, veg3, soil_type3, ph_est3 = analyze_soil_quality(Image.open(img3))
                    
                    avg_soil = (soil1 + soil2 + soil3) / 3
                    avg_veg = (veg1 + veg2 + veg3) / 3
                    avg_ph = (ph_est1 + ph_est2 + ph_est3) / 3
                    
                    # Determine dominant soil type
                    soil_types = [soil_type1, soil_type2, soil_type3]
                    dominant_soil = max(set(soil_types), key=soil_types.count)
                    
                    temp, humidity, weather = get_weather(city)
                    
                    K = 40
                    P = 35
                    N = nitrogen
                    
                    if model and scaler:
                        input_data = np.array([[N, P, K, temp, humidity, avg_ph, rainfall]])
                        input_scaled = scaler.transform(input_data)
                        predicted_crop = model.predict(input_scaled)[0]
                        
                        st.session_state.crop = predicted_crop
                        st.session_state.images = [img1, img2, img3]
                        plan_data = {
                            'crop': predicted_crop,
                            'start_date': datetime.date.today(),
                            'soil_health': avg_soil,
                            'vegetation': avg_veg,
                            'soil_type': dominant_soil,
                            'estimated_ph': avg_ph,
                            'weather': weather,
                            'temp': temp,
                            'humidity': humidity,
                            'city': city,
                            'area': area,
                            'recommended_crop': predicted_crop,
                            'short_term_crop': TERM_CROPS['short_term'],
                            'medium_term_crop': TERM_CROPS['medium_term'],
                            'long_term_crop': TERM_CROPS['long_term'],
                            'status': 'active'
                        }
                        st.session_state.farming_plan = plan_data
                        if st.session_state.user:
                            plan_id = save_farming_plan_to_db(st.session_state.user['id'], plan_data)
                            st.session_state.plan_id = plan_id
                        
                        st.session_state.page = "results"
                        st.rerun()
        else:
            st.error("❌ Please upload all three images and ensure city/village information is included")

# ==================== PAGE: RESULTS ====================
elif st.session_state.page == "results":
    
    st.title("✅ Land Analysis Results")
    
    if st.session_state.farming_plan:
        plan = st.session_state.farming_plan
        
        # Load datasets
        try:
            crop_data = pd.read_csv('crop_data.csv')
        except FileNotFoundError:
            st.error("Crop data file not found. Please ensure crop_data.csv exists.")
            crop_data = pd.DataFrame()
        try:
            market_data = pd.read_csv('market_data.csv')
        except FileNotFoundError:
            market_data = pd.DataFrame()
        current_month = datetime.datetime.now().strftime('%B')
        area = plan.get('area', 1.0)
        
        # Soil Insights Section
        st.markdown("### 🌱 Soil Insights")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""<div class="metric-card">
                <h3>🪨 Soil Type</h3>
                <h2>{plan.get('soil_type', 'Unknown').title()}</h2>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""<div class="metric-card">
                <h3>🧪 Est. pH</h3>
                <h2>{plan.get('estimated_ph', 7.0):.1f}</h2>
            </div>""", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""<div class="metric-card">
                <h3>🌱 Soil Health</h3>
                <h2>{plan['soil_health']:.0f}%</h2>
            </div>""", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""<div class="metric-card">
                <h3>🌿 Vegetation</h3>
                <h2>{plan['vegetation']:.0f}%</h2>
            </div>""", unsafe_allow_html=True)
        
        st.markdown(f"**Location:** {plan.get('city', 'Unknown')} | **Weather:** {plan.get('weather', 'Unknown')}, {plan.get('temp', 0)}°C, {plan.get('humidity', 0)}%")
        
        st.markdown("---")
        
        # Crop Options
        st.markdown("### 🌾 Crop Options")
        
        recommended_crop = plan.get('recommended_crop', st.session_state.crop)
        short_crop = plan.get('short_term_crop', TERM_CROPS['short_term'])
        medium_crop = plan.get('medium_term_crop', TERM_CROPS['medium_term'])
        long_crop = plan.get('long_term_crop', TERM_CROPS['long_term'])
        
        crops = [short_crop, medium_crop, long_crop]
        crop_labels = ["Short-term", "Medium-term", "Long-term"]
        
        if 'selected_crop_result' not in st.session_state:
            st.session_state.selected_crop_result = short_crop
        
        selected_crop = st.session_state.selected_crop_result
        
        # Display 3 crops and 1 farmer card in one row
        cols = st.columns(4)
        
        # First card: Motivational Farmer
        with cols[0]:
            st.markdown("""
            <div class="crop-card">
                <h3>🌾 Proud Farmer</h3>
                <p>Farmer holding crop in hand</p>
                <p style="font-size: 3rem;">👨‍🌾🌽</p>
                <p><strong>Keep Growing!</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Crop cards
        for i, (crop_name, label) in enumerate(zip(crops, crop_labels)):
            with cols[i+1]:
                crop_info = crop_data[crop_data['crop'].str.lower() == crop_name.lower()]
                if not crop_info.empty:
                    yield_per_acre = crop_info['yield_per_acre'].values[0]
                    profit_per_acre = crop_info['profit'].values[0]
                    budget_per_acre = crop_info['budget'].values[0]
                    duration_days = CROP_DURATION.get(crop_name.lower(), 120)
                    
                    total_yield = yield_per_acre * area
                    total_profit = profit_per_acre * area
                    total_investment = budget_per_acre * area
                    
                    yield_lower = total_yield * 0.85
                    yield_upper = total_yield * 1.15
                    selected_class = "crop-card selected" if crop_name.lower() == selected_crop.lower() else "crop-card"
                    
                    st.markdown(f"""
                    <div class=\"{selected_class}\">
                        <h3>{label}</h3>
                        <h2>{crop_name.upper()}</h2>
                        <p><strong>Duration:</strong> {duration_days} days</p>
                        <p><strong>Total Yield:</strong> {total_yield:,.0f} kg<br>
                        <small>({yield_lower:,.0f} - {yield_upper:,.0f} kg)</small></p>
                        <p><strong>Total Investment:</strong> ₹{total_investment:,.0f}</p>
                        <p><strong>Total Profit:</strong> ₹{total_profit:,.0f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Choose {label}", key=f"choose_{crop_name.lower()}"):
                        st.session_state.selected_crop_result = crop_name
                        st.session_state.crop = crop_name
                        st.session_state.farming_plan['crop'] = crop_name
                        selected_crop = crop_name
                        st.rerun()
        
        st.markdown("---")
        st.markdown(f"**Selected Crop:** **{selected_crop.upper()}**")
        st.session_state.crop = selected_crop
        st.session_state.farming_plan['crop'] = selected_crop
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🛒 " + get_translated_text("shopping_requirements", st.session_state.language), use_container_width=True):
                st.session_state.page = "shopping"
                st.rerun()
            
            if st.button("📅 Create Farming Schedule", use_container_width=True):
                duration = CROP_DURATION.get(selected_crop.lower(), 120)
                schedule = generate_farming_schedule(
                    selected_crop,
                    plan['start_date'],
                    duration
                )
                st.session_state.schedule = schedule
                st.session_state.tasks_completed = {item['date']: item.get('completed', False) for item in schedule}
                if st.session_state.plan_id:
                    save_daily_tasks_to_db(st.session_state.plan_id, schedule)
                st.session_state.page = "schedule"
                st.rerun()
        
        with col2:
            if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language), use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()

# ==================== PAGE: SHOPPING REQUIREMENTS ====================
elif st.session_state.page == "shopping":
    
    if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language)):
        st.session_state.page = "results"
        st.rerun()
    
    st.title("🛒 " + get_translated_text("shopping_requirements", st.session_state.language))
    
    if st.session_state.farming_plan:
        plan = st.session_state.farming_plan
        crop = st.session_state.crop
        area = plan.get('area', 1.0)
        location = plan.get('city', 'Unknown')
        
        # Initialize shopping checklist in session state
        if 'shopping_checklist' not in st.session_state:
            st.session_state.shopping_checklist = {}
        
        st.markdown(f"### 🌾 Shopping Requirements for {crop.upper()} - {area} acres")
        st.markdown(f"**📍 Location:** {location}")
        
        # Get shopping requirements
        requirements = get_shopping_requirements(crop, area)
        
        # Shopping Checklist Card
        st.markdown("---")
        st.markdown("### ✅ " + get_translated_text("purchase_checklist", st.session_state.language))
        
        total_cost = 0
        all_purchased = True
        
        # Create a beautiful card layout for shopping items
        for category, item in requirements.items():
            category_translated = get_translated_text(category, st.session_state.language)
            
            with st.container():
                st.markdown(f"""
                <div style="border: 2px solid #4CAF50; border-radius: 15px; padding: 20px; margin: 10px 0; background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);">
                    <h4 style="color: #2e7d32; margin-bottom: 15px;">🛍️ {category_translated}</h4>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="font-weight: bold; color: #1b5e20; font-size: 16px;">{item['name']}</p>
                            <p style="color: #388e3c;">📏 {get_translated_text('quantity', st.session_state.language)}: {item['quantity']} ({item['unit']})</p>
                            <p style="color: #388e3c;">💰 {get_translated_text('price', st.session_state.language)}: ₹{item['price']:,.0f}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-size: 18px; font-weight: bold; color: #2e7d32;">₹{item['price']:,.0f}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Checkbox for marking as purchased
                purchased = st.checkbox(
                    get_translated_text("mark_as_purchased", st.session_state.language) + f" - {item['name']}",
                    key=f"purchase_{category}",
                    value=st.session_state.shopping_checklist.get(category, False)
                )
                
                st.session_state.shopping_checklist[category] = purchased
                
                if purchased:
                    total_cost += item['price']
                else:
                    all_purchased = False
                
                st.markdown("---")
        
        # Total Cost Section
        st.markdown(f"""
        <div style="border: 3px solid #FF9800; border-radius: 15px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #fff8e1 0%, #ffe0b2 100%); text-align: center;">
            <h3 style="color: #e65100; margin-bottom: 10px;">💵 {get_translated_text('total_cost', st.session_state.language)}</h3>
            <p style="font-size: 28px; font-weight: bold; color: #ff6f00;">₹{total_cost:,.0f}</p>
            <p style="color: #f57c00; font-size: 14px;">Estimated cost for all marked items</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Nearest Markets Section
        st.markdown("---")
        st.markdown("### 🏪 " + get_translated_text("nearest_markets", st.session_state.language))
        
        markets = get_nearest_markets(location)
        
        for i, market in enumerate(markets, 1):
            st.markdown(f"""
            <div style="border: 1px solid #2196F3; border-radius: 10px; padding: 15px; margin: 10px 0; background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);">
                <h4 style="color: #1565c0; margin-bottom: 10px;">📍 {market['name']}</h4>
                <p style="color: #1976d2;">📏 Distance: {market['distance']}</p>
                <p style="color: #1976d2;">🏠 Address: {market['address']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Action Buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📅 " + get_translated_text("proceed_to_calendar", st.session_state.language), 
                        use_container_width=True, 
                        disabled=not all_purchased,
                        help="Please mark all items as purchased before proceeding"):
                # Add shopping requirements to the first day of schedule
                if st.session_state.plan_id:
                    shopping_task = {
                        'date': datetime.date.today().strftime('%Y-%m-%d'),
                        'task': f'🛒 Completed shopping for {crop}: Seeds, Fertilizer, Tools & Equipment',
                        'type': 'shopping',
                        'completed': True
                    }
                    save_daily_tasks_to_db(st.session_state.plan_id, [shopping_task])
                
                st.session_state.page = "schedule"
                st.rerun()
        
        with col2:
            if st.button("⬅️ " + get_translated_text("back_to_results", st.session_state.language), 
                        use_container_width=True):
                st.session_state.page = "results"
                st.rerun()
        
        if not all_purchased:
            st.warning("⚠️ Please mark all items as purchased before proceeding to the farming calendar.")
        
        # Progress indicator
        purchased_count = sum(1 for v in st.session_state.shopping_checklist.values() if v)
        total_items = len(requirements)
        progress = purchased_count / total_items if total_items > 0 else 0
        
        st.markdown("---")
        st.markdown(f"### 📊 Shopping Progress: {purchased_count}/{total_items} items purchased")
        st.progress(progress)

# ==================== PAGE: DAILY SCHEDULE ====================
elif st.session_state.page == "schedule":
    
    if st.button("⬅️ Back to Results"):
        st.session_state.page = "results"
        st.rerun()
    
    st.title("📅 Farming Schedule Calendar")
    
    if not st.session_state.schedule and st.session_state.plan_id:
        stored_schedule = load_daily_tasks_from_db(st.session_state.plan_id)
        if stored_schedule:
            st.session_state.schedule = stored_schedule
            st.session_state.tasks_completed = {item['date']: item['completed'] for item in stored_schedule}
    
    if st.session_state.schedule:
        crop = st.session_state.crop
        st.markdown(f"### 🌾 {crop.upper()} - Month-by-month Crop Calendar")
        
        schedule = st.session_state.schedule
        schedule_map = {item['date']: item for item in schedule}
        start_date = datetime.datetime.strptime(schedule[0]['date'], '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(schedule[-1]['date'], '%Y-%m-%d').date()
        
        import calendar
        cal = calendar.Calendar(firstweekday=0)
        
        months = []
        current_month = datetime.date(start_date.year, start_date.month, 1)
        last_month = datetime.date(end_date.year, end_date.month, 1)
        while current_month <= last_month:
            months.append((current_month.year, current_month.month))
            if current_month.month == 12:
                current_month = datetime.date(current_month.year + 1, 1, 1)
            else:
                current_month = datetime.date(current_month.year, current_month.month + 1, 1)
        
        if 'schedule_month_index' not in st.session_state:
            st.session_state.schedule_month_index = 0
        if st.session_state.schedule_month_index >= len(months):
            st.session_state.schedule_month_index = len(months) - 1
        
        month_index = st.session_state.schedule_month_index
        year, month = months[month_index]
        month_name = calendar.month_name[month]
        
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("⬅️ Previous Month", key="prev_schedule_month"):
                st.session_state.schedule_month_index = max(0, month_index - 1)
                st.rerun()
        with nav_col3:
            if st.button("Next Month ➡️", key="next_schedule_month"):
                st.session_state.schedule_month_index = min(len(months) - 1, month_index + 1)
                st.rerun()
        with nav_col2:
            st.markdown(f"<div class='month-title'>{month_name} {year}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='calendar-month-card'>", unsafe_allow_html=True)
        header_cols = st.columns(7)
        for idx, weekday_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            header_cols[idx].markdown(f"<div style='text-align:center; font-weight:bold'>{weekday_name}</div>", unsafe_allow_html=True)
        
        for week in cal.monthdatescalendar(year, month):
            cols = st.columns(7)
            for idx, day in enumerate(week):
                with cols[idx]:
                    if day.month != month or day < start_date or day > end_date:
                        st.markdown("<div class='calendar-day' style='opacity:0.25; min-height:160px;'></div>", unsafe_allow_html=True)
                        continue
                    
                    day_str = day.strftime('%Y-%m-%d')
                    entry = schedule_map.get(day_str, {
                        'task': '🌿 Daily care: monitor soil moisture and crop health.',
                        'type': 'daily',
                        'day': (day - start_date).days
                    })
                    completed = st.session_state.tasks_completed.get(day_str, False)
                    box_class = "calendar-day completed" if completed else "calendar-day"
                    
                    st.markdown(f"<div class='{box_class}'><strong>{day.day}</strong><br><small>{entry['task']}</small></div>", unsafe_allow_html=True)
                    checked = st.checkbox("Done", value=completed, key=f"day_{day_str}")
                    if checked != completed and st.session_state.plan_id:
                        update_task_completion(st.session_state.plan_id, day_str, checked)
                    st.session_state.tasks_completed[day_str] = checked
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        completed_count = sum(1 for v in st.session_state.tasks_completed.values() if v)
        total_count = len(schedule)
        progress = completed_count / total_count if total_count > 0 else 0
        
        st.markdown(f"### 📊 Progress: {completed_count}/{total_count} days completed")
        st.progress(progress)
        
        if progress == 1.0:
            st.success(f"🎉 {get_translated_text('congratulations', st.session_state.language)}! {get_translated_text('farming_completed', st.session_state.language)}")
            if st.button("🏪 View Marketing & Selling Options", use_container_width=True):
                st.session_state.page = "marketing"
                st.rerun()
        else:
            st.info("📝 Complete all daily farming tasks to unlock marketing and selling options")

# ==================== PAGE: MARKETING & SELLING ====================
elif st.session_state.page == "marketing":
    
    if st.button("⬅️ Back to Calendar"):
        st.session_state.page = "schedule"
        st.rerun()
    
    st.title("🏪 Marketing & Selling Options")
    st.markdown("### 🌾 Sell Your Harvest for Maximum Profit!")
    
    if st.session_state.farming_plan:
        crop = st.session_state.crop.lower()
        location = st.session_state.farming_plan.get('city', 'Unknown')
        area = st.session_state.farming_plan.get('area', 1.0)
        
        # Enhanced market data with comprehensive information
        market_prices = {
            'tomato': {
                'min': 10, 'max': 25, 'avg': 17, 'demand': 'High', 
                'markets': ['Bangalore', 'Chennai', 'Hyderabad'],
                'strategy': 'Harvest at right ripeness. Sell fresh to local markets. Consider value addition like ketchup for higher returns.',
                'storage': 'Can be stored for 5-7 days at room temperature',
                'transport': 'Requires careful handling, use crates',
                'best_season': 'October - March',
                'price_factors': 'Quality, size, color, and freshness',
                'estimated_yield': f"{area * 25:.0f} - {area * 35:.0f} quintals",
                'estimated_revenue': f"₹{area * 25000:.0f} - ₹{area * 87500:.0f}"
            },
            'maize': {
                'min': 18, 'max': 28, 'avg': 23, 'demand': 'Medium', 
                'markets': ['Pune', 'Nashik', 'Bangalore'],
                'strategy': 'Store in cool, dry place. Sell during high demand seasons. Consider processing into corn flour for better prices.',
                'storage': 'Can be stored for 6-12 months when dried properly',
                'transport': 'Easy to transport, requires dry conditions',
                'best_season': 'Year-round demand, peak in winter',
                'price_factors': 'Moisture content, grain quality, variety',
                'estimated_yield': f"{area * 20:.0f} - {area * 30:.0f} quintals",
                'estimated_revenue': f"₹{area * 36000:.0f} - ₹{area * 84000:.0f}"
            },
            'rice': {
                'min': 20, 'max': 35, 'avg': 27, 'demand': 'High', 
                'markets': ['Bangalore', 'Mysore', 'Delhi'],
                'strategy': 'Sell immediately after harvest to avoid storage losses. Target wholesale markets for bulk sales.',
                'storage': 'Can be stored for 12-18 months with proper conditions',
                'transport': 'Requires dry storage and moisture control',
                'best_season': 'Kharif: Oct-Dec, Rabi: Apr-Jun',
                'price_factors': 'Grain quality, variety, milling recovery',
                'estimated_yield': f"{area * 30:.0f} - {area * 40:.0f} quintals",
                'estimated_revenue': f"₹{area * 60000:.0f} - ₹{area * 140000:.0f}"
            },
            'cotton': {
                'min': 50, 'max': 80, 'avg': 65, 'demand': 'High', 
                'markets': ['Gujarat', 'Maharashtra', 'Telangana'],
                'strategy': 'Ginning and pressing before sale increases value. Sell to textile mills directly for premium prices.',
                'storage': 'Requires controlled humidity, can store 6-12 months',
                'transport': 'Requires covered transport to prevent moisture',
                'best_season': 'October - February',
                'price_factors': 'Staple length, cleanliness, moisture content',
                'estimated_yield': f"{area * 15:.0f} - {area * 25:.0f} quintals",
                'estimated_revenue': f"₹{area * 75000:.0f} - ₹{area * 200000:.0f}"
            },
            'ragi': {
                'min': 15, 'max': 25, 'avg': 20, 'demand': 'Medium', 
                'markets': ['Bangalore', 'Mysore', 'Hubli'],
                'strategy': 'Sell to health food stores and organic markets. Consider value addition through flour processing.',
                'storage': 'Excellent storage capacity, 12-24 months',
                'transport': 'Easy to transport and store',
                'best_season': 'Year-round, higher demand in festivals',
                'price_factors': 'Grain quality, processing method, organic certification',
                'estimated_yield': f"{area * 8:.0f} - {area * 12:.0f} quintals",
                'estimated_revenue': f"₹{area * 12000:.0f} - ₹{area * 30000:.0f}"
            },
            'cabbage': {
                'min': 8, 'max': 15, 'avg': 11, 'demand': 'Medium', 
                'markets': ['Bangalore', 'Mysore', 'Chennai'],
                'strategy': 'Harvest fresh. Sell to wholesale markets. Consider organic certification for higher prices.',
                'storage': 'Cold storage extends life to 2-3 months',
                'transport': 'Requires refrigerated transport for long distances',
                'best_season': 'October - March',
                'price_factors': 'Head size, freshness, color, weight',
                'estimated_yield': f"{area * 40:.0f} - {area * 60:.0f} quintals",
                'estimated_revenue': f"₹{area * 32000:.0f} - ₹{area * 90000:.0f}"
            }
        }
        
        if crop in market_prices:
            prices = market_prices[crop]
            
            # Harvest Summary Card
            st.markdown("---")
            st.markdown("### 📊 Harvest Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="metric-card">
                    <h3>🌾 Crop</h3>
                    <h2>{crop.upper()}</h2>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="metric-card">
                    <h3>📏 Area</h3>
                    <h2>{area} acres</h2>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="metric-card">
                    <h3>⚖️ Est. Yield</h3>
                    <h2>{prices['estimated_yield']}</h2>
                </div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="metric-card">
                    <h3>💰 Est. Revenue</h3>
                    <h2>{prices['estimated_revenue']}</h2>
                </div>""", unsafe_allow_html=True)
            
            # Market Overview Cards
            st.markdown("---")
            st.markdown("### 🏪 Market Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""<div class="metric-card">
                    <h3>💰 Price Range</h3>
                    <h2>₹{prices['min']}-{prices['max']}/kg</h2>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class="metric-card">
                    <h3>📊 Demand</h3>
                    <h2>{prices['demand']}</h2>
                </div>""", unsafe_allow_html=True)
            with col3:
                st.markdown(f"""<div class="metric-card">
                    <h3>🏪 Best Markets</h3>
                    <h2>{len(prices['markets'])} Cities</h2>
                </div>""", unsafe_allow_html=True)
            with col4:
                st.markdown(f"""<div class="metric-card">
                    <h3>📅 Best Season</h3>
                    <h2>{prices['best_season']}</h2>
                </div>""", unsafe_allow_html=True)
            
            # Comprehensive Selling Strategy
            st.markdown("---")
            st.markdown("### 🎯 Selling Strategy")
            st.markdown(f"**{prices['strategy']}**")
            
            # Nearest Markets Section
            st.markdown("---")
            st.markdown("### 📍 Nearest Agricultural Markets")
            
            nearest_markets = get_nearest_markets(location)
            
            for i, market in enumerate(nearest_markets, 1):
                # Check if this market is in the recommended markets list
                is_recommended = market['name'] in prices['markets']
                badge = "⭐ RECOMMENDED" if is_recommended else "📍 Available"
                
                st.markdown(f"""
                <div style="border: 2px solid {'#FFD700' if is_recommended else '#2196F3'}; border-radius: 15px; padding: 20px; margin: 10px 0; background: linear-gradient(135deg, {'#fffacd' if is_recommended else '#e3f2fd'} 0%, {'#f0e68c' if is_recommended else '#bbdefb'} 100%);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="color: {'#ff8c00' if is_recommended else '#1565c0'}; margin: 0;">🏪 {market['name']}</h4>
                        <span style="background: {'#FFD700' if is_recommended else '#2196F3'}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold;">{badge}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">📏 Distance: {market['distance']}</p>
                        <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">💰 Est. Price: ₹{prices['min']}-{prices['max']}/kg</p>
                    </div>
                    <p style="color: {'#ff8c00' if is_recommended else '#1976d2'}; margin: 5px 0;">🏠 Address: {market['address']}</p>
                    {f'<p style="color: #d32f2f; margin: 5px 0; font-weight: bold;">🌟 Top choice for {crop} - Best prices guaranteed!</p>' if is_recommended else ''}
                </div>
                """, unsafe_allow_html=True)
            
            # Additional Market Information
            st.markdown("---")
            st.markdown("### 📋 Important Market Information")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="border: 1px solid #4CAF50; border-radius: 10px; padding: 15px; background: #e8f5e8;">
                    <h4 style="color: #2e7d32;">📦 Storage Guidelines</h4>
                    <p style="color: #388e3c;">{prices['storage']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="border: 1px solid #FF9800; border-radius: 10px; padding: 15px; background: #fff3e0;">
                    <h4 style="color: #e65100;">🚚 Transport Tips</h4>
                    <p style="color: #f57c00;">{prices['transport']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="border: 1px solid #9C27B0; border-radius: 10px; padding: 15px; background: #f3e5f5;">
                <h4 style="color: #6a1b9a;">💡 Price Factors</h4>
                <p style="color: #7b1fa2;">{prices['price_factors']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Value Addition Opportunities
            st.markdown("---")
            st.markdown("### 🚀 Value Addition Opportunities")
            
            value_addition_ideas = {
                'tomato': ['🍅 Tomato Ketchup/Sauce', '🥫 Canned Tomatoes', '🧂 Tomato Powder', '🍷 Tomato Juice'],
                'maize': ['🌽 Corn Flour', '🍿 Popcorn', '🌾 Animal Feed', '🧈 Corn Oil'],
                'rice': ['🍚 Rice Flour', '🍜 Rice Noodles', '🍶 Rice Wine', '🥮 Rice Cakes'],
                'cotton': ['🧵 Cotton Thread', '👕 Cotton Fabric', '🏥 Cotton Medical Supplies', '💊 Cotton Seed Oil'],
                'ragi': ['🌾 Ragi Flour', '🥘 Ragi Porridge', '🍪 Ragi Biscuits', '🥤 Ragi Health Drinks'],
                'cabbage': ['🥗 Cabbage Salad', '🥒 Pickled Cabbage', '🍲 Cabbage Soup', '🥬 Cabbage Rolls']
            }
            
            if crop in value_addition_ideas:
                st.markdown("Consider these value addition options to increase your profits:")
                for idea in value_addition_ideas[crop]:
                    st.markdown(f"- {idea}")
            
            # Motivational Message
            st.markdown("---")
            st.markdown("### 🌾 Congratulations on Successful Harvest!")
            st.markdown("**💪 Dear Farmer, your hard work and dedication have paid off! You've successfully completed your farming cycle. May your harvest bring prosperity and joy to you and your family! Best wishes for selling your produce at the best prices! 🚜✨**")
            
            # Action Buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📈 View Market Rates", use_container_width=True):
                    st.session_state.page = "market"
                    st.rerun()
            
            with col2:
                if st.button("💼 Selling Strategies", use_container_width=True):
                    st.session_state.page = "selling_strategy"
                    st.rerun()
            
            with col3:
                if st.button("🏛️ Government Subsidies", use_container_width=True):
                    st.session_state.page = "government_subsidy"
                    st.rerun()
        else:
            st.info("Market data for this crop is being updated. Please check back later.")

# ==================== PAGE: PROFILE ====================
elif st.session_state.page == "profile":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("👤 " + get_translated_text("profile_settings", st.session_state.language))
    
    if st.session_state.user:
        st.markdown("### " + get_translated_text("personal_details", st.session_state.language))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3>👨‍🌾 {get_translated_text('personal_details', st.session_state.language)}</h3>
                <p><strong>{get_translated_text('name', st.session_state.language)}:</strong> {st.session_state.user['username']}</p>
                <p><strong>{get_translated_text('email', st.session_state.language)}:</strong> {st.session_state.user['email']}</p>
                <p><strong>{get_translated_text('designation', st.session_state.language)}:</strong> Farmer</p>
                <p><strong>{get_translated_text('role', st.session_state.language)}:</strong> Agricultural Producer</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <h3>📊 {get_translated_text('account_status', st.session_state.language)}</h3>
                <p><strong>{get_translated_text('member_since', st.session_state.language)}:</strong> {datetime.datetime.now().strftime('%B %Y')}</p>
                <p><strong>{get_translated_text('status', st.session_state.language)}:</strong> Active Farmer</p>
                <p><strong>{get_translated_text('verified', st.session_state.language)}:</strong> ✅ Yes</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🌾 " + get_translated_text("farming_activity", st.session_state.language))
        
        if st.session_state.farming_plan:
            plan = st.session_state.farming_plan
            st.write(f"**{get_translated_text('current_crop', st.session_state.language)}:** {plan.get('crop', 'None')}")
            st.write(f"**{get_translated_text('land_area', st.session_state.language)}:** {plan.get('area', 0)} acres")
            st.write(f"**{get_translated_text('start_date', st.session_state.language)}:** {plan.get('start_date', 'Not set')}")
        else:
            st.info("No active farming plan. Start farming to see your activity here!")

# ==================== PAGE: NEWS ====================
elif st.session_state.page == "news":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("📰 " + get_translated_text("agriculture_news", st.session_state.language))
    
    source_name, news_items = get_daily_agri_news()
    st.markdown(f"### {get_translated_text('todays_headlines', st.session_state.language)} from {source_name}")
    st.markdown("Stay updated with rotating newspaper-style coverage and crop market trends.")
    for item in news_items:
        st.markdown(f"""
        <div class="card">
            <h3>{item['title']}</h3>
            <p>{item['summary']}</p>
            <small><strong>{get_translated_text('source', st.session_state.language)}:</strong> {item['source']} | <strong>{get_translated_text('date', st.session_state.language)}:</strong> {item['date']}</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

# ==================== PAGE: SELLING STRATEGY ====================
elif st.session_state.page == "selling_strategy":
    
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("💼 Selling Strategies")
    
    st.markdown("### 🚀 Value Addition & Selling Strategies for Farmers")
    
    strategies = [
        {
            "title": "🍹 Juice Production",
            "description": "Process fruits like oranges, apples, and tomatoes into fresh juices. Sell directly to consumers or retailers for 3-5x higher prices.",
            "benefits": "Higher profit margins, longer shelf life, brand building",
            "requirements": "Juicer machine, packaging, refrigeration"
        },
        {
            "title": "⚡ Biofuel & Power Generation",
            "description": "Convert crop residues (straw, husks) into biogas or biomass pellets for energy production. Sell to power companies or use for farm operations.",
            "benefits": "Additional income from waste, sustainable farming, government subsidies",
            "requirements": "Biogas plant, pellet machine, storage facilities"
        },
        {
            "title": "🥫 Canning & Preservation",
            "description": "Can vegetables and fruits for year-round availability. Create pickles, jams, and sauces from your produce.",
            "benefits": "Sell throughout the year, premium pricing, reduced waste",
            "requirements": "Canning equipment, preservatives, quality control"
        },
        {
            "title": "🌱 Organic Certification",
            "description": "Get organic certification for your farm and sell produce at premium prices to health-conscious consumers.",
            "benefits": "30-50% higher prices, export opportunities, government support",
            "requirements": "Organic farming practices, certification process, documentation"
        },
        {
            "title": "🏪 Direct-to-Consumer Sales",
            "description": "Sell directly at farmers' markets, online platforms, or through farm stalls. Build customer relationships.",
            "benefits": "Higher margins (no middlemen), customer loyalty, feedback for improvement",
            "requirements": "Marketing, transportation, quality presentation"
        },
        {
            "title": "🔄 Crop Processing",
            "description": "Process crops into flour, oil, or animal feed. For example, turn maize into corn flour or soybeans into oil.",
            "benefits": "Value addition, multiple products from one crop, industrial demand",
            "requirements": "Processing machinery, storage, quality standards"
        },
        {
            "title": "🌾 Seed Production",
            "description": "Save and sell high-quality seeds from your best crops. Become a seed producer for other farmers.",
            "benefits": "High profit per unit, recurring income, knowledge sharing",
            "requirements": "Seed selection expertise, storage, certification"
        },
        {
            "title": "🐔 Integrated Farming",
            "description": "Combine crop farming with livestock or poultry. Use crop residues as feed and sell meat/eggs.",
            "benefits": "Diversified income, natural fertilizers, risk reduction",
            "requirements": "Animal husbandry knowledge, additional infrastructure"
        },
        {
            "title": "📱 Online Marketplaces",
            "description": "Use apps and websites to sell directly to urban consumers. Platforms like BigBasket, local e-commerce.",
            "benefits": "Wider market reach, real-time pricing, convenience",
            "requirements": "Smartphone, internet, packaging for delivery"
        },
        {
            "title": "🤝 Cooperative Marketing",
            "description": "Join farmer cooperatives for bulk selling, better bargaining power, and shared resources.",
            "benefits": "Better prices through collective bargaining, shared costs, government support",
            "requirements": "Cooperative membership, quality standards, transportation"
        }
    ]
    
    for strategy in strategies:
        st.markdown(f"""
        <div class="card">
            <h3>{strategy['title']}</h3>
            <p><strong>Description:</strong> {strategy['description']}</p>
            <p><strong>Benefits:</strong> {strategy['benefits']}</p>
            <p><strong>Requirements:</strong> {strategy['requirements']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

# ==================== PAGE: GOVERNMENT SUBSIDY ====================
elif st.session_state.page == "government_subsidy":
    
    if st.button("⬅️ " + get_translated_text("back_to_dashboard", st.session_state.language)):
        st.session_state.page = "dashboard"
        st.rerun()
    
    st.title("🏛️ " + get_translated_text("government_subsidies", st.session_state.language))
    st.markdown("### Support schemes and subsidy programs for farmers")
    st.image("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=compress&cs=tinysrgb&h=400&w=800", use_column_width=True)
    
    subsidies = [
        {
            "name": "PM-Kisan Samman Nidhi",
            "description": "Direct income support of up to ₹6,000 per year for small and marginal farmers.",
            "benefits": "Regular cash support, easy online application, bank transfer",
            "eligibility": "All landholding farmers with Aadhaar and bank account"
        },
        {
            "name": "Pradhan Mantri Fasal Bima Yojana",
            "description": "Crop insurance scheme to protect farmers from yield loss due to natural disasters.",
            "benefits": "Low premium, wide coverage, claim settlement support",
            "eligibility": "All farmers growing notified crops"
        },
        {
            "name": "Kisan Credit Card (KCC)",
            "description": "Provides short-term credit at concessional interest rates for agricultural needs.",
            "benefits": "Easy loan access, working capital support, crop cycle financing",
            "eligibility": "Farmers with land records and bank account"
        },
        {
            "name": "Soil Health Card Scheme",
            "description": "Free soil testing and recommendations to improve fertilizer use efficiency.",
            "benefits": "Better yields, reduced input cost, balanced nutrient use",
            "eligibility": "All farmers across India"
        },
        {
            "name": "Sub-Mission on Agroforestry",
            "description": "Support for tree plantation on farms and wasteland to boost income and ecology.",
            "benefits": "Financial assistance for saplings, training, and maintenance",
            "eligibility": "Farmers, forest dwellers, rural households"
        },
        {
            "name": "PMKSY - Per Drop More Crop",
            "description": "Subsidies for micro-irrigation systems such as drip and sprinkler irrigation.",
            "benefits": "Water saving, higher productivity, lower power costs",
            "eligibility": "Irrigated farmers and groups"
        }
    ]
    
    for sub in subsidies:
        st.markdown(f"""
        <div class="card">
            <h3>🌾 {sub['name']}</h3>
            <p><strong>What it is:</strong> {sub['description']}</p>
            <p><strong>Why it matters:</strong> {sub['benefits']}</p>
            <p><strong>Who can apply:</strong> {sub['eligibility']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

# ==================== PAGE: MARKET INSIGHTS ====================
elif st.session_state.page == "market":
    if st.button("⬅️ Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.title("📈 Market Insights")
    st.markdown("### Real-time pricing guidance and best selling locations")
    st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=compress&cs=tinysrgb&h=400&w=800", use_column_width=True)

    market_prices = {
        'rice': {'min': 20, 'max': 35, 'avg': 27, 'demand': 'High', 'markets': ['Bangalore', 'Mysore']},
        'maize': {'min': 18, 'max': 28, 'avg': 23, 'demand': 'Medium', 'markets': ['Pune', 'Nashik']},
        'wheat': {'min': 25, 'max': 40, 'avg': 32, 'demand': 'High', 'markets': ['Delhi', 'Haryana']},
        'cotton': {'min': 50, 'max': 80, 'avg': 65, 'demand': 'High', 'markets': ['Gujarat', 'Maharashtra']},
        'sugarcane': {'min': 3, 'max': 6, 'avg': 4.5, 'demand': 'Medium', 'markets': ['Maharashtra', 'Haryana']},
        'tomato': {'min': 10, 'max': 25, 'avg': 17, 'demand': 'High', 'markets': ['Bangalore', 'Chennai']},
        'potato': {'min': 8, 'max': 18, 'avg': 13, 'demand': 'High', 'markets': ['Punjab', 'Himachal Pradesh']},
    }

    crop_choice = st.selectbox("Choose a crop for market insights", sorted(market_prices.keys()))
    prices = market_prices[crop_choice]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <h3>💰 Min Price</h3>
            <h2>₹{prices['min']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <h3>💵 Avg Price</h3>
            <h2>₹{prices['avg']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
            <h3>💸 Max Price</h3>
            <h2>₹{prices['max']}/kg</h2>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
            <h3>📊 Demand</h3>
            <h2>{prices['demand']}</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏪 Best Markets")
    for market in prices['markets']:
        st.write(f"✅ {market}")

    st.markdown("---")
    st.markdown("### 📱 Selling Guidance")
    st.markdown("Use these estimates to decide the best time and location to sell your harvest.")
