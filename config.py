"""
Wild Vision - Configuration Settings
Central configuration file for all application settings
"""

import os
from pathlib import Path

# ==================== PATHS ====================
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "train3" / "weights" / "best.pt"
SNAPSHOT_DIR = BASE_DIR / "snapshots"

# Ensure snapshot directory exists
SNAPSHOT_DIR.mkdir(exist_ok=True)

# ==================== DETECTION CLASSES ====================
CLASS_NAMES = {
    0: 'Bear',
    1: 'Elephant',
    2: 'Leopard',
    3: 'Tiger'
}

# Species emojis for UI
CLASS_EMOJIS = {
    'Bear': '🐻',
    'Elephant': '🐘',
    'Leopard': '🐆',
    'Tiger': '🐅'
}

# Species colors for bounding boxes
CLASS_COLORS = {
    'Bear': (139, 69, 19),      # Brown
    'Elephant': (128, 128, 128), # Gray
    'Leopard': (255, 165, 0),    # Orange
    'Tiger': (255, 140, 0)       # Dark Orange
}

# ==================== DETECTION THRESHOLDS ====================
# Layer 1: Initial detection threshold
LAYER1_CONFIDENCE = 0.50

# Layer 2: Verification threshold
LAYER2_CONFIDENCE = 0.40

# Auto-snapshot threshold (high confidence captures)
AUTO_SNAPSHOT_THRESHOLD = 0.75

# ==================== MONGODB SETTINGS ====================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "wild_vision_db"

# Collection names
USERS_COLLECTION = "users"
DETECTIONS_COLLECTION = "detections"
ALERTS_COLLECTION = "alerts"

# ==================== EMAIL SETTINGS ====================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "imrankhanghori2026@gmail.com"
SENDER_APP_PASSWORD = "xjxw aqrx irvm muso"  # Gmail App Password
RECEIVER_EMAIL = "imranghori0096@gmail.com"

# Email template
EMAIL_SUBJECT = "🚨 Wild Vision Alert - {species} Detected!"
DEFAULT_LOCATION = "15.880444°N, 74.518389°E"

# ==================== ALERT SETTINGS ====================
# Cooldown period in seconds (prevents alert spam)
ALERT_COOLDOWN_SECONDS = 5

# ==================== DASHBOARD SETTINGS ====================
# Auto-refresh interval in milliseconds
DASHBOARD_REFRESH_INTERVAL = 5000  # 5 seconds

# Number of recent detections to display
RECENT_DETECTIONS_LIMIT = 20

# Snapshot gallery page size
GALLERY_PAGE_SIZE = 12

# ==================== VIDEO PROCESSING SETTINGS ====================
# Webcam settings
WEBCAM_WIDTH = 640
WEBCAM_HEIGHT = 480
WEBCAM_FPS = 30

# Frame processing
PROCESS_EVERY_N_FRAMES = 2  # Process every 2nd frame for performance

# Video quality
VIDEO_QUALITY = 85  # JPEG quality for streaming

# ==================== UI THEME ====================
# Color scheme
PRIMARY_COLOR = "#1a4d2e"      # Deep Forest Green
ACCENT_COLOR = "#ff6700"       # Wildlife Orange
BACKGROUND_COLOR = "#0e1117"   # Dark Charcoal
CARD_BACKGROUND = "rgba(255, 255, 255, 0.1)"

# Confidence color coding
CONFIDENCE_HIGH = "#00ff88"    # Green (> 80%)
CONFIDENCE_MEDIUM = "#ffaa00"  # Yellow (60-80%)
CONFIDENCE_LOW = "#ff4444"     # Red (< 60%)

# ==================== SECURITY ====================
# Password hashing rounds
BCRYPT_ROUNDS = 12

# Session timeout (minutes)
SESSION_TIMEOUT = 60

# ==================== PERFORMANCE ====================
# Model device (use "cpu" if no GPU available)
DEVICE = "cpu"  # Set to "0" for GPU, "cpu" for CPU-only

# Image size for inference (from training config)
INFERENCE_SIZE = 416

# Maximum concurrent detections
MAX_CONCURRENT_DETECTIONS = 10
