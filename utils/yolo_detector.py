"""
YOLO Detection Engine
Handles model loading, object detection, and bounding box visualization
"""

import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import config


@st.cache_resource
def load_model():
    """
    Load YOLO model with caching to prevent reloading on every run.
    Handles PyTorch 2.6+ compatibility issues.
    
    Returns:
        YOLO: Loaded YOLO model
    """
    try:
        import torch
        import os
        
        # Workaround for PyTorch 2.6+ weights_only issue
        # Set environment variable before loading
        os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'
        
        # Also monkey-patch torch.load to use weights_only=False
        original_torch_load = torch.load
        
        def patched_torch_load(*args, **kwargs):
            # Force weights_only=False for YOLO model compatibility
            kwargs['weights_only'] = False
            return original_torch_load(*args, **kwargs)
        
        # Temporarily replace torch.load
        torch.load = patched_torch_load
        
        try:
            model = YOLO(str(config.MODEL_PATH))
        finally:
            # Restore original torch.load
            torch.load = original_torch_load
        
        # Verify model loaded correctly
        if model is None:
            raise ValueError("Model is None after loading")
        
        if not hasattr(model, 'names') or model.names is None or len(model.names) == 0:
            raise ValueError("Model loaded but has no class names")
        
        st.success(f"✅ YOLO model loaded! Detecting: {', '.join(model.names.values())}")
        return model
        
    except Exception as e:
        error_msg = str(e)
        st.error(f"❌ Failed to load YOLO model")
        
        if "weights_only" in error_msg.lower() or "weightsunpickler" in error_msg.lower():
            st.warning("""
            **PyTorch 2.6 Compatibility Issue Detected**
            
            The model file cannot load due to PyTorch 2.6 security restrictions.
            
            **Quick Fix:** Downgrade PyTorch to 2.0.1:
            ```
            pip uninstall torch torchvision -y
            pip install torch==2.0.1 torchvision==0.15.2
            ```
            Then restart the application.
            """)
        else:
            st.warning(f"Error details: {error_msg[:200]}")
        
        return None


def detect_objects(image, conf_threshold=0.5):
    """
    Run YOLO detection on an image.
    
    Args:
        image (np.ndarray): Input image (BGR or RGB)
        conf_threshold (float): Confidence threshold for detections
        
    Returns:
        list: List of detections, each containing:
            - class_id (int)
            - class_name (str)
            - confidence (float)
            - bbox (tuple): (x1, y1, x2, y2)
    """
    model = load_model()
    if model is None:
        return []
    
    try:
        # Run inference
        results = model.predict(
            image,
            conf=conf_threshold,
            imgsz=config.INFERENCE_SIZE,
            device=config.DEVICE,
            verbose=False
        )
        
        detections = []
        
        # Parse results
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Extract box information
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Get class name
                class_name = config.CLASS_NAMES.get(class_id, f"Class_{class_id}")
                
                detections.append({
                    'class_id': class_id,
                    'class_name': class_name,
                    'confidence': confidence,
                    'bbox': (int(x1), int(y1), int(x2), int(y2))
                })
        
        return detections
    
    except Exception as e:
        st.error(f"Detection error: {e}")
        return []


def draw_boxes(image, detections, show_confidence=True):
    """
    Draw bounding boxes on image with labels and confidence scores.
    
    Args:
        image (np.ndarray): Input image (BGR format)
        detections (list): List of detection dictionaries
        show_confidence (bool): Whether to show confidence percentage
        
    Returns:
        np.ndarray: Image with drawn bounding boxes
    """
    output_image = image.copy()
    
    for det in detections:
        class_name = det['class_name']
        confidence = det['confidence']
        x1, y1, x2, y2 = det['bbox']
        
        # Get class-specific color (BGR format)
        color = config.CLASS_COLORS.get(class_name, (0, 255, 0))
        
        # Draw bounding box
        thickness = 3
        cv2.rectangle(output_image, (x1, y1), (x2, y2), color, thickness)
        
        # Prepare label text
        if show_confidence:
            label = f"{class_name} {confidence:.1%}"
        else:
            label = f"{class_name}"
        
        # Calculate label background size
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(
            label, font, font_scale, font_thickness
        )
        
        # Draw label background
        cv2.rectangle(
            output_image,
            (x1, y1 - text_height - 10),
            (x1 + text_width + 10, y1),
            color,
            -1  # Filled rectangle
        )
        
        # Draw label text
        cv2.putText(
            output_image,
            label,
            (x1 + 5, y1 - 5),
            font,
            font_scale,
            (255, 255, 255),  # White text
            font_thickness
        )
    
    return output_image


def get_detection_summary(detections):
    """
    Generate a summary of detections.
    
    Args:
        detections (list): List of detection dictionaries
        
    Returns:
        dict: Summary with counts per species
    """
    summary = {}
    
    for det in detections:
        species = det['class_name']
        if species in summary:
            summary[species] += 1
        else:
            summary[species] = 1
    
    return summary


def get_highest_confidence_detection(detections):
    """
    Get the detection with the highest confidence score.
    
    Args:
        detections (list): List of detection dictionaries
        
    Returns:
        dict or None: Detection with highest confidence, or None if no detections
    """
    if not detections:
        return None
    
    return max(detections, key=lambda x: x['confidence'])


def filter_detections_by_species(detections, species_list):
    """
    Filter detections to only include specified species.
    
    Args:
        detections (list): List of detection dictionaries
        species_list (list): List of species names to include
        
    Returns:
        list: Filtered detections
    """
    return [det for det in detections if det['class_name'] in species_list]
