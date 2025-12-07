"""
2-Layer Verification System
Implements dual-layer YOLO verification to reduce false positives
"""

import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
import config
from utils.yolo_detector import detect_objects, get_highest_confidence_detection


def save_snapshot(image, detection, source="webcam"):
    """
    Save snapshot with timestamp and detection information.
    
    Args:
        image (np.ndarray): Image to save
        detection (dict): Detection information
        source (str): Source of detection ("webcam" or "upload")
        
    Returns:
        str or None: Path to saved snapshot, or None if failed
    """
    try:
        # Generate timestamp filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Milliseconds
        species = detection['class_name']
        confidence = int(detection['confidence'] * 100)
        
        filename = f"{timestamp}_{species}_{confidence}_{source}.jpg"
        filepath = config.SNAPSHOT_DIR / filename
        
        # Save image
        cv2.imwrite(str(filepath), image)
        
        return str(filepath)
    
    except Exception as e:
        print(f"Error saving snapshot: {e}")
        return None


def delete_snapshot(filepath):
    """
    Delete a snapshot file.
    
    Args:
        filepath (str): Path to snapshot file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        path = Path(filepath)
        if path.exists():
            path.unlink()
            return True
        return False
    
    except Exception as e:
        print(f"Error deleting snapshot: {e}")
        return False


def verify_detection_2layer(image):
    """
    Perform 2-layer verification on an image.
    
    Workflow:
    1. Layer 1: Run detection with LAYER1_CONFIDENCE threshold
    2. If detection found, capture snapshot
    3. Layer 2: Re-run detection on snapshot with LAYER2_CONFIDENCE threshold
    4. If Layer 2 confirms, return verified detection
    5. If Layer 2 fails, delete snapshot and return None
    
    Args:
        image (np.ndarray): Input image (BGR format)
        
    Returns:
        dict or None: Verification result containing:
            - layer1_detections: List of Layer 1 detections
            - layer2_detections: List of Layer 2 detections
            - verified: Boolean indicating if verification passed
            - snapshot_path: Path to snapshot (if verified)
            - best_detection: Highest confidence detection (if verified)
    """
    
    # === LAYER 1: Initial Detection ===
    layer1_detections = detect_objects(image, conf_threshold=config.LAYER1_CONFIDENCE)
    
    if not layer1_detections:
        return {
            'layer1_detections': [],
            'layer2_detections': [],
            'verified': False,
            'snapshot_path': None,
            'best_detection': None,
            'rejection_reason': 'No Layer 1 detection'
        }
    
    # Get highest confidence detection from Layer 1
    best_layer1 = get_highest_confidence_detection(layer1_detections)
    
    # === SNAPSHOT CAPTURE ===
    snapshot_path = save_snapshot(image, best_layer1, source="verification")
    
    if not snapshot_path:
        return {
            'layer1_detections': layer1_detections,
            'layer2_detections': [],
            'verified': False,
            'snapshot_path': None,
            'best_detection': None,
            'rejection_reason': 'Snapshot save failed'
        }
    
    # === LAYER 2: Verification Re-Detection ===
    # Read the saved snapshot for verification
    snapshot_image = cv2.imread(snapshot_path)
    
    if snapshot_image is None:
        delete_snapshot(snapshot_path)
        return {
            'layer1_detections': layer1_detections,
            'layer2_detections': [],
            'verified': False,
            'snapshot_path': None,
            'best_detection': None,
            'rejection_reason': 'Snapshot read failed'
        }
    
    layer2_detections = detect_objects(snapshot_image, conf_threshold=config.LAYER2_CONFIDENCE)
    
    # === VERIFICATION CHECK ===
    if not layer2_detections:
        # Layer 2 failed - delete snapshot
        delete_snapshot(snapshot_path)
        return {
            'layer1_detections': layer1_detections,
            'layer2_detections': [],
            'verified': False,
            'snapshot_path': None,
            'best_detection': None,
            'rejection_reason': 'No Layer 2 detection'
        }
    
    # Check if same species detected in both layers
    best_layer2 = get_highest_confidence_detection(layer2_detections)
    
    if best_layer1['class_name'] != best_layer2['class_name']:
        # Different species detected - delete snapshot
        delete_snapshot(snapshot_path)
        return {
            'layer1_detections': layer1_detections,
            'layer2_detections': layer2_detections,
            'verified': False,
            'snapshot_path': None,
            'best_detection': None,
            'rejection_reason': f"Species mismatch: L1={best_layer1['class_name']}, L2={best_layer2['class_name']}"
        }
    
    # === VERIFICATION PASSED ===
    return {
        'layer1_detections': layer1_detections,
        'layer2_detections': layer2_detections,
        'verified': True,
        'snapshot_path': snapshot_path,
        'best_detection': {
            'species': best_layer2['class_name'],
            'confidence_layer1': best_layer1['confidence'],
            'confidence_layer2': best_layer2['confidence'],
            'bbox_layer1': best_layer1['bbox'],
            'bbox_layer2': best_layer2['bbox']
        },
        'rejection_reason': None
    }


def should_trigger_snapshot(detections):
    """
    Check if any detection exceeds the auto-snapshot threshold.
    
    Args:
        detections (list): List of detection dictionaries
        
    Returns:
        bool: True if snapshot should be triggered
    """
    if not detections:
        return False
    
    best = get_highest_confidence_detection(detections)
    return best['confidence'] >= config.AUTO_SNAPSHOT_THRESHOLD
