# Wild Vision - Deployment Notes

## ✅ Streamlit Cloud Ready

This application has been configured to run gracefully on **Streamlit Cloud** without MongoDB or OpenCV.

### 🎯 Demo Mode (Streamlit Cloud)

When deployed to Streamlit Cloud, the app will run in **demo mode**:

- ✅ **Home page** works fully
- ✅ **Dashboard** shows empty state (no detections)
- ⚠️ **Webcam** shows "not supported" message
- ⚠️ **Upload** shows "not available" message
- ⚠️ **Authentication** is skipped
- ℹ️ **Database features** disabled

### 🚀 Full Features (Local Installation)

To enable all features, run locally with MongoDB:

```bash
# 1. Start MongoDB
mongod

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

### ☁️ Full Features (Cloud with MongoDB Atlas)

To enable database features on Streamlit Cloud:

1. Create a free **MongoDB Atlas** account
2. Get your connection string
3. Add to Streamlit secrets:
   ```toml
   MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
   ```
4. Update `config.py`:
   ```python
   import os
   MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
   ```

### 📋 What Was Changed

#### 1. Made OpenCV Optional
- `ui/webcam_page.py` - wrapped cv2 imports in try-except
- `ui/upload_page.py` - wrapped cv2 imports in try-except
- Shows friendly error messages when unavailable

#### 2. Made MongoDB Optional
- `database/mongodb_client.py` - silent connection failures
- `app.py` - allows app to run without database
- `database/user_manager.py` - returns demo user ID when no DB
- `database/detection_manager.py` - silent failures, returns empty data
- Shows warning banner when database unavailable

### 🎨 User Experience

**With MongoDB unavailable:**
- Shows yellow warning banner at top
- Explains features are disabled
- Provides instructions to enable full features

**With OpenCV unavailable:**
- Webcam/Upload pages show styled error messages
- Explains why feature isn't available
- Provides instructions for local setup

### 🐛 Troubleshooting

**App crashes on Streamlit Cloud:**
- Check the error logs in "Manage app"
- Ensure `requirements.txt` has all dependencies
- Verify secrets are properly configured

**MongoDB not connecting locally:**
```bash
# Start MongoDB service
mongod

# Or on Windows with installation path:
"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe"
```

**Detection not saving:**
- Check MongoDB is running
- Verify database connection in app warning banner
- Check console for any error messages

---

**Last Updated:** 2025-12-07
**Version:** 1.0.0 - Cloud Ready
