# 🌿 Wild Vision - Wildlife Detection System

A production-ready wildlife detection system powered by YOLO11, featuring real-time webcam streaming, 2-layer verification, MongoDB database, and email alerts.

![Wildlife Detection](https://img.shields.io/badge/Detection-YOLO11-orange)
![Database](https://img.shields.io/badge/Database-MongoDB-green)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

## 🎯 Features

### 🔍 **Advanced Detection System**
- **YOLO11-Large Model**: 98.58% mAP@50 accuracy
- **Detects 4 Species**: Tiger 🐅, Bear 🐻, Leopard 🐆, Elephant 🐘
- **2-Layer Verification**: Reduces false positives with dual-layer confidence checking
- **Auto-Snapshot**: Captures images when confidence > 75%

### 📹 **Real-Time Webcam Streaming**
- Live camera feed with detection overlay
- Color-coded confidence bounding boxes
- FPS optimization with frame buffering
- Smooth streaming performance

### 📊 **Interactive Dashboard**
- Auto-refresh every 5 seconds
- Live statistics: Total detections, species breakdown, alerts
- Species distribution charts
- Recent detections table
- Snapshot gallery

### 🔔 **Smart Alert System**
- Email notifications with HTML templates
- 5-second cooldown per species (prevents spam)
- Async sending (non-blocking)
- Snapshot attachments

### 🗄️ **MongoDB Integration**
- Detection history storage
- User authentication with bcrypt
- Indexed queries for fast retrieval
- Species statistics and trends

### 🎨 **Modern UI Design**
- Glassmorphism theme
- Responsive mobile-friendly layout
- Accent colors and animations
- Dark mode optimized

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- MongoDB 8.x
- Webcam (for live detection)
- GPU (recommended for real-time performance)

### Step 1: Clone Repository
```bash
cd wild_vision_sgbit
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start MongoDB
```bash
# Make sure MongoDB is running
mongod
```

### Step 5: Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🚀 Quick Start Guide

### 1. **Create Account**
- Click "Create Account" on the login page
- Enter username, email, and password
- Login with your credentials

### 2. **Upload Image Detection**
- Go to "📤 Upload Image" page
- Upload a wildlife image (JPG/PNG)
- Click "Detect Wildlife"
- View 2-layer verification results

### 3. **Webcam Detection**
- Go to "📹 Webcam Detection" page
- Click "Start Webcam"
- Enable detection for real-time monitoring
- Auto-snapshots triggered at 75%+ confidence

### 4. **View Dashboard**
- Go to "📊 Dashboard" page
- See live statistics and charts
- Browse recent detections
- View snapshot gallery

---

## 📂 Project Structure

```
wild_vision_sgbit/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── models/
│   └── train3/weights/
│       └── best.pt            # YOLO11 trained model (51MB)
│
├── utils/
│   ├── yolo_detector.py       # YOLO detection engine
│   ├── verification.py        # 2-layer verification system
│   └── video_processor.py     # Webcam streaming handler
│
├── database/
│   ├── mongodb_client.py      # MongoDB connection
│   ├── user_manager.py        # Authentication system
│   └── detection_manager.py   # Detection CRUD operations
│
├── alerts/
│   └── email_service.py       # Email notification system
│
├── ui/
│   ├── styles.py              # Custom CSS theming
│   ├── auth_pages.py          # Login/Signup pages
│   ├── dashboard.py           # Analytics dashboard
│   ├── webcam_page.py         # Webcam streaming interface
│   └── upload_page.py         # Image upload interface
│
└── snapshots/                 # Auto-saved detection images
```

---

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
# Detection Thresholds
LAYER1_CONFIDENCE = 0.50       # Initial detection threshold
LAYER2_CONFIDENCE = 0.40       # Verification threshold
AUTO_SNAPSHOT_THRESHOLD = 0.75 # Auto-capture threshold

# Email Settings
SENDER_EMAIL = "your-email@gmail.com"
SENDER_APP_PASSWORD = "your-app-password"
RECEIVER_EMAIL = "receiver@gmail.com"

# Alert Cooldown
ALERT_COOLDOWN_SECONDS = 5     # Cooldown between alerts
```

---

## 🧪 Testing the System

### Test Image Upload
1. Find a wildlife image (Tiger/Bear/Leopard/Elephant)
2. Upload via "Upload Image" page
3. Verify Layer 1 and Layer 2 detections
4. Check MongoDB for saved detection
5. Verify email alert received

### Test Webcam Streaming
1. Start webcam on "Webcam Detection" page
2. Show wildlife image to camera
3. Wait for auto-snapshot at 75%+ confidence
4. Verify 2-layer verification runs
5. Check detection saved to database
6. Confirm email alert sent

---

## 📧 Email Setup (Gmail)

### Enable App Password
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Security → 2-Step Verification → App passwords
3. Generate app password for "Mail"
4. Copy password to `config.py`

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB service
mongod
```

### Webcam Not Opening
```python
# Try different camera index in config.py
WEBCAM_INDEX = 0  # Try 1, 2, etc.
```

### Low FPS Performance
```python
# Increase frame skip in config.py
PROCESS_EVERY_N_FRAMES = 3  # Process every 3rd frame
```

### Email Not Sending
- Verify Gmail App Password in `config.py`
- Check internet connection
- Ensure SMTP server is accessible

---

## 📊 Database Collections

### `users`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password_hash": "bcrypt_hash",
  "created_at": "2025-12-03T10:00:00"
}
```

### `detections`
```json
{
  "user_id": "ObjectId",
  "timestamp": "2025-12-03T10:05:00",
  "species": "Tiger",
  "confidence_layer1": 0.85,
  "confidence_layer2": 0.78,
  "snapshot_path": "snapshots/20251203_100500_Tiger_78_webcam.jpg",
  "verification_status": "verified",
  "alert_sent": true,
  "source": "webcam"
}
```

### `alerts`
```json
{
  "species": "Tiger",
  "user_id": "ObjectId",
  "last_alert_time": "2025-12-03T10:05:00"
}
```

---

## 🎓 Model Training Details

- **Architecture**: YOLO11-Large
- **Dataset**: Custom wildlife dataset (Tiger, Bear, Leopard, Elephant)
- **Training**: 50 epochs, batch size 8, image size 416×416
- **Performance**:
  - **Precision**: 99.05%
  - **Recall**: 97.55%
  - **mAP@50**: 98.58%
  - **mAP@50-95**: 75.17%

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is for educational and conservation purposes.

---

## 👨‍💻 Developer

**Developed by**: [Your Name]  
**GitHub**: [Your GitHub]  
**Email**: imrankhanghori2026@gmail.com

---

## 🙏 Acknowledgments

- **Ultralytics YOLO11**: For the detection model
- **Streamlit**: For the web framework
- **MongoDB**: For the database system

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Email: imrankhanghori2026@gmail.com

---

**🌿 Wild Vision - Protecting Wildlife with AI** 🐅🐻🐆🐘
