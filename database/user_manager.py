"""
User Manager
Handles user authentication, registration, and session management with persistent login
"""

import bcrypt
import json
import hashlib
from datetime import datetime
from pathlib import Path
from bson.objectid import ObjectId
import streamlit as st
import config
from database.mongodb_client import get_collection


# Session file path
SESSION_FILE = Path.home() / '.wildvision_session.json'


def _save_session(user_data):
    """Save session to persistent storage."""
    try:
        session_data = {
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'token': hashlib.sha256(f"{user_data['user_id']}{datetime.now()}".encode()).hexdigest()
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_data, f)
        return True
    except Exception as e:
        print(f"Error saving session: {e}")
        return False


def _load_session():
    """Load session from persistent storage."""
    try:
        if SESSION_FILE.exists():
            with open(SESSION_FILE, 'r') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading session: {e}")
        return None


def _clear_session():
    """Clear persistent session file."""
    try:
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
        return True
    except Exception as e:
        print(f"Error clearing session: {e}")
        return False


def hash_password(password):
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    
    Args:
        password (str): Plain text password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def register_user(username, email, password):
    """
    Register a new user.
    
    Args:
        username (str): Username
        email (str): Email address
        password (str): Plain text password
        
    Returns:
        tuple: (success: bool, message: str, user_id: ObjectId or None)
    """
    users_collection = get_collection(config.USERS_COLLECTION)
    
    if users_collection is None:
        return False, "Database connection failed", None
    
    # Validate inputs
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters", None
    
    if not email or '@' not in email:
        return False, "Invalid email address", None
    
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters", None
    
    try:
        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return False, "Username already exists", None
        
        if users_collection.find_one({"email": email}):
            return False, "Email already registered", None
        
        # Create user document
        user_doc = {
            "username": username,
            "email": email,
            "password_hash": hash_password(password),
            "created_at": datetime.now(),
            "last_login": None
        }
        
        result = users_collection.insert_one(user_doc)
        
        return True, "Registration successful!", result.inserted_id
    
    except Exception as e:
        return False, f"Registration failed: {e}", None


def login_user(username, password):
    """
    Authenticate a user and save persistent session.
    
    Args:
        username (str): Username
        password (str): Plain text password
        
    Returns:
        tuple: (success: bool, message: str, user_data: dict or None)
    """
    users_collection = get_collection(config.USERS_COLLECTION)
    
    if users_collection is None:
        return False, "Database connection failed", None
    
    try:
        # Find user
        user = users_collection.find_one({"username": username})
        
        if not user:
            return False, "Invalid username or password", None
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return False, "Invalid username or password", None
        
        # Update last login
        users_collection.update_one(
            {"_id": user['_id']},
            {"$set": {"last_login": datetime.now()}}
        )
        
        # Return user data (excluding password hash)
        user_data = {
            "user_id": str(user['_id']),
            "username": user['username'],
            "email": user['email'],
            "created_at": user['created_at']
        }
        
        # Save persistent session
        _save_session(user_data)
        
        return True, "Login successful!", user_data
    
    except Exception as e:
        return False, f"Login failed: {e}", None


def initialize_session():
    """
    Initialize session state variables for authentication.
    Attempts to restore session from persistent storage.
    """
    # Try to load persistent session
    if 'session_restored' not in st.session_state:
        st.session_state['session_restored'] = True
        
        saved_session = _load_session()
        if saved_session:
            # Restore session state
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = saved_session.get('user_id')
            st.session_state['username'] = saved_session.get('username')
            st.session_state['email'] = saved_session.get('email')
            return
    
    # Initialize default values if not restored
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    if 'email' not in st.session_state:
        st.session_state['email'] = None


def logout_user():
    """
    Logout current user by clearing session state and persistent storage.
    """
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = None
    st.session_state['email'] = None
    st.session_state['session_restored'] = False
    
    # Clear persistent session
    _clear_session()


def is_logged_in():
    """
    Check if user is currently logged in.
    
    Returns:
        bool: True if logged in, False otherwise
    """
    return st.session_state.get('logged_in', False)


def get_current_user_id():
    """
    Get current user's ID.
    Returns a demo ObjectId when running without MongoDB.
    
    Returns:
        ObjectId or None: User ID if logged in, demo ID if no MongoDB, None otherwise
    """
    user_id_str = st.session_state.get('user_id')
    if user_id_str:
        return ObjectId(user_id_str)
    
    # Return demo user ID when MongoDB is unavailable
    if not st.session_state.get('mongodb_available', True):
        return ObjectId('000000000000000000000000')  # Demo user ID
    
    return None


def get_user_by_id(user_id):
    """
    Get user information by ID.
    
    Args:
        user_id (ObjectId): User ID
        
    Returns:
        dict or None: User data (excluding password hash)
    """
    users_collection = get_collection(config.USERS_COLLECTION)
    
    if users_collection is None:
        return None
    
    try:
        user = users_collection.find_one({"_id": user_id})
        
        if user:
            return {
                "user_id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "created_at": user['created_at'],
                "last_login": user.get('last_login')
            }
        
        return None
    
    except Exception as e:
        st.error(f"Error fetching user: {e}")
        return None
