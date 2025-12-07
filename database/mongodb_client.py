"""
MongoDB Client
Handles database connection and basic operations
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import streamlit as st
import config


@st.cache_resource
def get_mongo_client():
    """
    Create and cache MongoDB client connection.
    Silently returns None if connection fails (allows app to run without DB).
    
    Returns:
        MongoClient: MongoDB client instance or None if connection fails
    """
    try:
        client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        return client
    except (ConnectionFailure, Exception):
        # Silently fail - app will handle this gracefully
        return None


def get_database():
    """
    Get database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    client = get_mongo_client()
    if client is None:
        return None
    return client[config.DB_NAME]


def get_collection(collection_name):
    """
    Get collection instance.
    
    Args:
        collection_name (str): Name of the collection
        
    Returns:
        Collection: MongoDB collection instance
    """
    db = get_database()
    if db is None:
        return None
    return db[collection_name]


def initialize_database():
    """
    Initialize database with required indexes and collections.
    Creates indexes for optimized queries.
    """
    db = get_database()
    if db is None:
        return False
    
    try:
        # Users collection indexes
        users_collection = db[config.USERS_COLLECTION]
        users_collection.create_index([("username", ASCENDING)], unique=True)
        users_collection.create_index([("email", ASCENDING)], unique=True)
        
        # Detections collection indexes
        detections_collection = db[config.DETECTIONS_COLLECTION]
        detections_collection.create_index([("user_id", ASCENDING)])
        detections_collection.create_index([("timestamp", DESCENDING)])
        detections_collection.create_index([("species", ASCENDING)])
        detections_collection.create_index([("verification_status", ASCENDING)])
        
        # Alerts collection indexes
        alerts_collection = db[config.ALERTS_COLLECTION]
        alerts_collection.create_index([("species", ASCENDING), ("user_id", ASCENDING)])
        
        return True
    
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return False


def test_connection():
    """
    Test MongoDB connection and return status.
    Silently returns False if connection fails.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        client = get_mongo_client()
        if client is None:
            return False
        
        # Test database access
        db = get_database()
        if db is None:
            return False
        
        # List collections to verify access
        db.list_collection_names()
        
        return True
    
    except Exception:
        # Silently fail
        return False


def get_database_stats():
    """
    Get database statistics.
    
    Returns:
        dict: Database statistics including collection counts
    """
    db = get_database()
    if db is None:
        return {}
    
    try:
        stats = {
            'users': db[config.USERS_COLLECTION].count_documents({}),
            'detections': db[config.DETECTIONS_COLLECTION].count_documents({}),
            'alerts': db[config.ALERTS_COLLECTION].count_documents({})
        }
        return stats
    
    except Exception as e:
        st.error(f"Error getting database stats: {e}")
        return {}
