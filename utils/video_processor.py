"""
Video Processor
Handles webcam capture and frame processing for real-time detection
"""

import cv2
import numpy as np
from datetime import datetime
import time
import config
from utils.yolo_detector import load_model, detect_objects, draw_boxes


class WebcamProcessor:
    """Handles webcam capture and processing."""
    
    def __init__(self, camera_index=0):
        """
        Initialize webcam processor.
        
        Args:
            camera_index: Camera index (0 for default) or IP webcam URL string
        """
        self.camera_index = camera_index
        self.cap = None
        self.running = False
        self.fps = 0
        self.last_time = time.time()
        self.frame_count = 0
        
        # Load YOLO model
        self.model = load_model()
    
    def start(self):
        """Start webcam capture."""
        try:
            # Open camera (supports both index and URL)
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                return False
            
            # Set resolution if using camera index (not URL)
            if isinstance(self.camera_index, int):
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WEBCAM_WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.WEBCAM_HEIGHT)
                self.cap.set(cv2.CAP_PROP_FPS, config.WEBCAM_FPS)
            
            self.running = True
            self.last_time = time.time()
            return True
            
        except Exception as e:
            print(f"Error starting webcam: {e}")
            return False
    
    def stop(self):
        """Stop webcam capture."""
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def is_running(self):
        """Check if webcam is running."""
        return self.running and self.cap is not None and self.cap.isOpened()
    
    def read_frame(self):
        """
        Read a frame from webcam.
        
        Returns:
            tuple: (success, frame)
        """
        if not self.is_running():
            return False, None
        
        success, frame = self.cap.read()
        
        if not success:
            return False, None
        
        # Resize IP webcam frames to match laptop camera resolution
        if isinstance(self.camera_index, str):  # IP webcam URL
            target_width = config.WEBCAM_WIDTH
            target_height = config.WEBCAM_HEIGHT
            
            # Only resize if frame is larger than target
            h, w = frame.shape[:2]
            if w > target_width or h > target_height:
                frame = cv2.resize(frame, (target_width, target_height))
        
        # Update FPS
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            current_time = time.time()
            self.fps = 10 / (current_time - self.last_time)
            self.last_time = current_time
        
        return success, frame
    
    def process_frame(self, frame, enable_detection=True, conf_threshold=0.5):
        """
        Process a frame with YOLO detection.
        
        Args:
            frame: Input frame (BGR)
            enable_detection: Whether to run detection
            conf_threshold: Confidence threshold for detection
            
        Returns:
            tuple: (processed_frame, detections)
        """
        if not enable_detection or self.model is None:
            return frame.copy(), []
        
        try:
            # Run detection (detect_objects loads model internally)
            detections = detect_objects(
                frame,
                conf_threshold=conf_threshold
            )
            
            # Draw boxes on frame
            processed_frame = draw_boxes(frame, detections)
            
            return processed_frame, detections
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame.copy(), []
    
    def get_fps(self):
        """Get current FPS."""
        return self.fps
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
