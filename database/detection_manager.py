"""
Detection Manager
Handles CRUD operations for wildlife detections
"""

from datetime import datetime, timedelta
from bson.objectid import ObjectId
import streamlit as st
import config
from database.mongodb_client import get_collection


def save_detection(user_id, species, confidence_layer1, confidence_layer2,
                   snapshot_path, verification_status="verified", 
                   alert_sent=False, source="webcam"):
    """
    Save a detection to the database.
    
    Args:
        user_id (ObjectId): User ID
        species (str): Detected species name
        confidence_layer1 (float): Layer 1 confidence score
        confidence_layer2 (float): Layer 2 confidence score
        snapshot_path (str): Path to saved snapshot
        verification_status (str): "verified" or "rejected"
        alert_sent (bool): Whether alert was sent
        source (str): "webcam" or "upload"
        
    Returns:
        ObjectId or None: Detection ID if successful, None otherwise
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return None
    
    try:
        detection_doc = {
            "user_id": user_id,
            "timestamp": datetime.now(),
            "species": species,
            "confidence_layer1": confidence_layer1,
            "confidence_layer2": confidence_layer2,
            "snapshot_path": snapshot_path,
            "verification_status": verification_status,
            "alert_sent": alert_sent,
            "source": source
        }
        
        result = detections_collection.insert_one(detection_doc)
        return result.inserted_id
    
    except Exception as e:
        st.error(f"Error saving detection: {e}")
        return None


def update_detection_alert_status(detection_id, alert_sent=True):
    """
    Update the alert_sent status for a detection.
    
    Args:
        detection_id (ObjectId): Detection ID to update
        alert_sent (bool): Whether alert was sent
        
    Returns:
        bool: True if updated successfully, False otherwise
    """
    try:
        from bson import ObjectId
        
        collection = get_collection(config.DETECTIONS_COLLECTION)
        
        if collection is None:
            return False
        
        result = collection.update_one(
            {"_id": ObjectId(detection_id)},
            {"$set": {"alert_sent": alert_sent}}
        )
        
        return result.modified_count > 0
        
    except Exception as e:
        print(f"Error updating detection alert status: {e}")
        return False


def get_recent_detections(user_id, limit=20):
    """
    Get recent detections for a user.
    
    Args:
        user_id (ObjectId): User ID
        limit (int): Maximum number of detections to return
        
    Returns:
        list: List of detection documents
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return []
    
    try:
        detections = list(detections_collection.find(
            {"user_id": user_id, "verification_status": "verified"}
        ).sort("timestamp", -1).limit(limit))
        
        return detections
    
    except Exception as e:
        st.error(f"Error fetching detections: {e}")
        return []


def get_species_statistics(user_id):
    """
    Get detection statistics by species for a user.
    
    Args:
        user_id (ObjectId): User ID
        
    Returns:
        dict: Species counts {species_name: count}
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return {}
    
    try:
        pipeline = [
            {"$match": {"user_id": user_id, "verification_status": "verified"}},
            {"$group": {"_id": "$species", "count": {"$sum": 1}}}
        ]
        
        results = list(detections_collection.aggregate(pipeline))
        
        stats = {result['_id']: result['count'] for result in results}
        return stats
    
    except Exception as e:
        st.error(f"Error getting species statistics: {e}")
        return {}


def get_total_detections(user_id):
    """
    Get total number of verified detections for a user.
    
    Args:
        user_id (ObjectId): User ID
        
    Returns:
        int: Total detection count
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return 0
    
    try:
        count = detections_collection.count_documents({
            "user_id": user_id,
            "verification_status": "verified"
        })
        return count
    
    except Exception as e:
        st.error(f"Error counting detections: {e}")
        return 0


def get_detections_today(user_id):
    """
    Get detections from today for a user.
    
    Args:
        user_id (ObjectId): User ID
        
    Returns:
        list: List of detection documents
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return []
    
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        detections = list(detections_collection.find({
            "user_id": user_id,
            "verification_status": "verified",
            "timestamp": {"$gte": today_start}
        }).sort("timestamp", -1))
        
        return detections
    
    except Exception as e:
        st.error(f"Error fetching today's detections: {e}")
        return []


def delete_detection(detection_id):
    """
    Delete a detection by ID.
    
    Args:
        detection_id (ObjectId): Detection ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return False
    
    try:
        result = detections_collection.delete_one({"_id": detection_id})
        return result.deleted_count > 0
    
    except Exception as e:
        st.error(f"Error deleting detection: {e}")
        return False


def get_detection_by_id(detection_id):
    """
    Get a specific detection by ID.
    
    Args:
        detection_id (ObjectId): Detection ID
        
    Returns:
        dict or None: Detection document
    """
    detections_collection = get_collection(config.DETECTIONS_COLLECTION)
    
    if detections_collection is None:
        return None
    
    try:
        detection = detections_collection.find_one({"_id": detection_id})
        return detection
    
    except Exception as e:
        st.error(f"Error fetching detection: {e}")
        return None


def get_detection_stats():
    """
    Get aggregated detection statistics for the home page.
    
    Returns:
        dict: Statistics including total_detections, unique_species, today_detections
    """
    from database.user_manager import get_current_user_id
    
    user_id = get_current_user_id()
    
    if user_id is None:
        return {
            'total_detections': 0,
            'unique_species': 0,
            'today_detections': 0
        }
    
    try:
        # Get total detections
        total = get_total_detections(user_id)
        
        # Get unique species count
        species_stats = get_species_statistics(user_id)
        unique_species = len(species_stats)
        
        # Get today's detections count
        today_detections_list = get_detections_today(user_id)
        today_count = len(today_detections_list)
        
        return {
            'total_detections': total,
            'unique_species': unique_species,
            'today_detections': today_count
        }
    
    except Exception as e:
        st.error(f"Error getting detection stats: {e}")
        return {
            'total_detections': 0,
            'unique_species': 0,
            'today_detections': 0
        }
