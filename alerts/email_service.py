"""
Email Alert Service
Handles email notifications with cooldown management
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime, timedelta
from pathlib import Path
import threading
import config
from database.mongodb_client import get_collection


def check_alert_cooldown(species, user_id):
    """
    Check if alert can be sent (cooldown check).
    
    Args:
        species (str): Species name
        user_id (ObjectId): User ID
        
    Returns:
        bool: True if alert can be sent, False if in cooldown period
    """
    alerts_collection = get_collection(config.ALERTS_COLLECTION)
    
    if alerts_collection is None:
        return True  # Allow alert if DB check fails
    
    try:
        alert_record = alerts_collection.find_one({
            "species": species,
            "user_id": user_id
        })
        
        if not alert_record:
            return True  # No previous alert, allow
        
        last_alert_time = alert_record.get('last_alert_time')
        
        if not last_alert_time:
            return True
        
        # Calculate time since last alert
        cooldown_period = timedelta(seconds=config.ALERT_COOLDOWN_SECONDS)
        time_since_last = datetime.now() - last_alert_time
        
        return time_since_last >= cooldown_period
    
    except Exception as e:
        print(f"Error checking alert cooldown: {e}")
        return True  # Allow alert if check fails


def update_alert_timestamp(species, user_id):
    """
    Update the last alert timestamp for a species.
    
    Args:
        species (str): Species name
        user_id (ObjectId): User ID
    """
    alerts_collection = get_collection(config.ALERTS_COLLECTION)
    
    if alerts_collection is None:
        return
    
    try:
        alerts_collection.update_one(
            {"species": species, "user_id": user_id},
            {"$set": {"last_alert_time": datetime.now()}},
            upsert=True
        )
    
    except Exception as e:
        print(f"Error updating alert timestamp: {e}")


def create_email_body(species, confidence_layer1, confidence_layer2, timestamp,
                      location=None, source=None):
    """
    Create HTML email body.
    
    Args:
        species (str): Detected species
        confidence_layer1 (float): Layer 1 confidence
        confidence_layer2 (float): Layer 2 confidence
        timestamp (datetime): Detection timestamp
        
    Returns:
        str: HTML email body
    """
    emoji = config.CLASS_EMOJIS.get(species, '🔍')
    
    location_text = location or config.DEFAULT_LOCATION
    source_text = (source.replace('_', ' ').title() if source else "N/A")

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                background-color: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, {config.PRIMARY_COLOR}, {config.ACCENT_COLOR});
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 20px;
            }}
            .emoji {{
                font-size: 48px;
                margin-bottom: 10px;
            }}
            .details {{
                margin: 20px 0;
                padding: 15px;
                background-color: #f9f9f9;
                border-left: 4px solid {config.ACCENT_COLOR};
            }}
            .detail-row {{
                margin: 10px 0;
                font-size: 16px;
            }}
            .label {{
                font-weight: bold;
                color: #333;
            }}
            .value {{
                color: {config.ACCENT_COLOR};
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                color: #777;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="emoji">{emoji}</div>
                <h1>Wild Vision Alert</h1>
                <h2>{species} Detected!</h2>
            </div>
            
            <p>A <strong>{species}</strong> has been detected by the Wild Vision detection system!</p>
            
            <div class="details">
                <div class="detail-row">
                    <span class="label">Species:</span>
                    <span class="value">{emoji} {species}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Layer 1 Confidence:</span>
                    <span class="value">{confidence_layer1:.1%}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Layer 2 Confidence:</span>
                    <span class="value">{confidence_layer2:.1%}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Detection Time:</span>
                    <span class="value">{timestamp.strftime('%Y-%m-%d %H:%M:%S')}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Location:</span>
                    <span class="value">{location_text}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Source:</span>
                    <span class="value">{source_text}</span>
                </div>
            </div>
            
            <p><em>The detection snapshot is attached to this email.</em></p>
            
            <div class="footer">
                <p>🌿 Wild Vision - Wildlife Detection System</p>
                <p>This is an automated alert. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email_sync(species, confidence_layer1, confidence_layer2, snapshot_path,
                    location=None, source=None):
    """
    Send email notification synchronously.
    
    Args:
        species (str): Detected species
        confidence_layer1 (float): Layer 1 confidence
        confidence_layer2 (float): Layer 2 confidence
        snapshot_path (str): Path to snapshot image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config.SENDER_EMAIL
        msg['To'] = config.RECEIVER_EMAIL
        msg['Subject'] = config.EMAIL_SUBJECT.format(species=species)
        
        # Add HTML body
        html_body = create_email_body(
            species=species,
            confidence_layer1=confidence_layer1,
            confidence_layer2=confidence_layer2,
            timestamp=datetime.now(),
            location=location,
            source=source
        )
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach snapshot image
        if snapshot_path and Path(snapshot_path).exists():
            with open(snapshot_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-Disposition', 'attachment', 
                             filename=Path(snapshot_path).name)
                msg.attach(img)
        
        # Connect to SMTP server and send
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SENDER_EMAIL, config.SENDER_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email alert sent for {species}")
        return True
    
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False


def send_email_async(species, confidence_layer1, confidence_layer2, snapshot_path,
                     user_id, location=None, source=None):
    """
    Send email notification asynchronously (non-blocking).
    
    Args:
        species (str): Detected species
        confidence_layer1 (float): Layer 1 confidence
        confidence_layer2 (float): Layer 2 confidence
        snapshot_path (str): Path to snapshot image
        user_id (ObjectId): User ID
    """
    def send_thread():
        success = send_email_sync(
            species=species,
            confidence_layer1=confidence_layer1,
            confidence_layer2=confidence_layer2,
            snapshot_path=snapshot_path,
            location=location,
            source=source
        )
        if success:
            update_alert_timestamp(species, user_id)
    
    thread = threading.Thread(target=send_thread, daemon=True)
    thread.start()


def send_alert_if_ready(species, confidence_layer1, confidence_layer2, snapshot_path,
                        user_id, location=None, source=None):
    """
    Send alert only if cooldown period has passed.
    
    Args:
        species (str): Detected species
        confidence_layer1 (float): Layer 1 confidence
        confidence_layer2 (float): Layer 2 confidence
        snapshot_path (str): Path to snapshot image
        user_id (ObjectId): User ID
        
    Returns:
        tuple: (alert_sent: bool, message: str)
    """
    if not check_alert_cooldown(species, user_id):
        return False, f"Alert in cooldown for {species}"
    
    # Send async email
    send_email_async(
        species=species,
        confidence_layer1=confidence_layer1,
        confidence_layer2=confidence_layer2,
        snapshot_path=snapshot_path,
        user_id=user_id,
        location=location,
        source=source
    )
    
    return True, f"Alert sent for {species}"
