"""
Image Upload Page
Modern AdminLTE-inspired upload interface
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
import config
from utils.yolo_detector import draw_boxes
from utils.verification import verify_detection_2layer
from database.user_manager import get_current_user_id
from database.detection_manager import save_detection
from alerts.email_service import send_alert_if_ready
from ui.styles import format_confidence, create_species_badge, create_confidence_bar


def show_upload_page():
    """Display modern image upload page with AdminLTE-inspired design."""
    
    user_id = get_current_user_id()
    
    # === HEADER ===
    st.markdown("""
    <div style="margin-bottom: 40px;">
        <h1 style="
            font-size: 3rem; 
            font-weight: 900; 
            margin-bottom: 8px;
            background: linear-gradient(to right, #818cf8, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">📤 Image Upload</h1>
        <p style="
            font-size: 1.125rem; 
            color: var(--text-secondary);
            margin: 0;
        ">Upload wildlife images for AI-powered detection and analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader with modern styling
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload images containing wildlife (Tiger, Bear, Leopard, Elephant)",
        label_visibility="collapsed"
    )
    
    if not uploaded_file:
        # Empty state
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
            border: 2px dashed var(--border-color);
            border-radius: var(--radius-xl);
            padding: 80px 40px;
            text-align: center;
            margin: 40px 0;
        ">
            <div style="font-size: 100px; margin-bottom: 20px;">📸</div>
            <h3 style="
                font-size: 1.5rem; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 12px;
            ">Drag and drop your image here</h3>
            <p style="
                font-size: 1rem; 
                color: var(--text-secondary);
                margin-bottom: 30px;
            ">or click to browse your files</p>
            <div style="
                display: inline-block;
                background: rgba(14, 165, 233, 0.1);
                border: 1px solid var(--info);
                border-radius: var(--radius-md);
                padding: 12px 24px;
                margin: 8px;
            ">
                <span style="color: var(--text-secondary); font-size: 0.875rem;">
                    ✓ JPG, JPEG, PNG supported
                </span>
            </div>
            <div style="
                display: inline-block;
                background: rgba(14, 165, 233, 0.1);
                border: 1px solid var(--info);
                border-radius: var(--radius-md);
                padding: 12px 24px;
                margin: 8px;
            ">
                <span style="color: var(--text-secondary); font-size: 0.875rem;">
                    ✓ Max 10MB file size
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tips section
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        tips = [
            ("💡", "Best Results", "Use clear, well-lit images with visible animals"),
            ("🎯", "Supported Species", "Tiger, Bear, Leopard, Elephant"),
            ("⚡", "Fast Processing", "Results in seconds with 98.58% accuracy")
        ]
        
        for col, (icon, title, desc) in zip([col1, col2, col3], tips):
            with col:
                st.markdown(f"""
                <div class="card" style="text-align: center; padding: 28px 20px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">{icon}</div>
                    <h4 style="
                        font-size: 1rem; 
                        font-weight: 700; 
                        color: var(--primary);
                        margin-bottom: 10px;
                    ">{title}</h4>
                    <p style="
                        font-size: 0.875rem; 
                        color: var(--text-secondary);
                        line-height: 1.5;
                        margin: 0;
                    ">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        return
    
    # Image uploaded - show preview and detection
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    if len(image_np.shape) == 3 and image_np.shape[2] == 3:
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    else:
        st.error("❌ Invalid image format. Please upload a color image.")
        return
    
    # Display images side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <h3 style="
            font-size: 1.125rem; 
            font-weight: 700; 
            color: var(--text-secondary);
            margin-bottom: 16px;
        ">📷 Original Image</h3>
        """, unsafe_allow_html=True)
        st.image(image, use_column_width=True)
    
    # Detection button
    if st.button("🔍 Detect Wildlife", type="primary", use_container_width=True):
        with col2:
            st.markdown("""
            <h3 style="
                font-size: 1.125rem; 
                font-weight: 700; 
                color: var(--text-secondary);
                margin-bottom: 16px;
            ">✅ Detection Result</h3>
            """, unsafe_allow_html=True)
        
        with st.spinner("🤖 Running 2-Layer AI Detection..."):
            result = verify_detection_2layer(image_bgr)
            
            if result['verified']:
                # Display detected image
                with col2:
                    result_image = draw_boxes(image_bgr, result['layer2_detections'])
                    result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
                    st.image(result_image_rgb, use_column_width=True)
                
                # Get all detected species
                detected_species = {}
                for det in result['layer2_detections']:
                    species = det['class_name']
                    if species not in detected_species or det['confidence'] > detected_species[species]['confidence']:
                        detected_species[species] = det
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Success message
                st.markdown(f"""
                <div class="alert-success" style="
                    background: rgba(16, 185, 129, 0.1);
                    border: 1px solid var(--success);
                    border-radius: var(--radius-lg);
                    padding: 24px;
                    margin: 20px 0;
                    text-align: center;
                ">
                    <div style="font-size: 64px; margin-bottom: 16px;">🎉</div>
                    <h2 style="
                        font-size: 1.75rem; 
                        font-weight: 800; 
                        color: var(--success);
                        margin-bottom: 8px;
                    ">Detected {len(detected_species)} </h2>
                    <p style="color: var(--text-secondary); font-size: 1rem;">
                        2-layer verification completed successfully
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display each detected animal in cards
                cols = st.columns(len(detected_species))
                for idx, (species, det) in enumerate(detected_species.items()):
                    layer1_conf = next((d['confidence'] for d in result['layer1_detections'] if d['class_name'] == species), det['confidence'])
                    
                    with cols[idx]:
                        st.markdown(f"""
                        <div class="card" style="padding: 28px 24px; border-top: 4px solid var(--primary);">
                            <div style="text-align: center; margin-bottom: 20px;">
                                <div style="font-size: 72px; margin-bottom: 12px;">
                                    {config.CLASS_EMOJIS.get(species, '🦁')}
                                </div>
                                <h3 style="
                                    font-size: 1.5rem; 
                                    font-weight: 800; 
                                    color: var(--primary);
                                    margin: 0;
                                ">{species}</h3>
                            </div>
                            {create_confidence_bar(layer1_conf, "Layer 1")}
                            {create_confidence_bar(det['confidence'], "Layer 2")}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Save detections
                saved_count = 0
                for species, det in detected_species.items():
                    layer1_conf = next((d['confidence'] for d in result['layer1_detections'] if d['class_name'] == species), det['confidence'])
                    
                    detection_id = save_detection(
                        user_id=user_id,
                        species=species,
                        confidence_layer1=layer1_conf,
                        confidence_layer2=det['confidence'],
                        snapshot_path=result['snapshot_path'],
                        verification_status="verified",
                        source="upload"
                    )
                    
                    if detection_id:
                        saved_count += 1
                        
                        # Send alert
                        alert_sent, alert_msg = send_alert_if_ready(
                            species=species,
                            confidence_layer1=layer1_conf,
                            confidence_layer2=det['confidence'],
                            snapshot_path=result['snapshot_path'],
                            user_id=user_id,
                            location=config.DEFAULT_LOCATION,
                            source="upload"
                        )
                        
                        if alert_sent:
                            from database.detection_manager import update_detection_alert_status
                            update_detection_alert_status(detection_id, alert_sent=True)
                            st.success(f"📧 {alert_msg}")
                        else:
                            st.info(f"ℹ️ {alert_msg}")
                
                if saved_count > 0:
                    st.success(f"✅ {saved_count} detection(s) saved to database")
            
            else:
                # Detection failed
                with col2:
                    st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
                        border: 2px dashed var(--border-color);
                        border-radius: var(--radius-lg);
                        padding: 60px 30px;
                        text-align: center;
                    ">
                        <div style="font-size: 80px; margin-bottom: 20px; opacity: 0.5;">🔍</div>
                        <h3 style="
                            font-size: 1.25rem; 
                            font-weight: 700; 
                            color: var(--text-secondary);
                            margin-bottom: 10px;
                        ">No detections</h3>
                        <p style="color: var(--text-muted); font-size: 0.875rem;">
                            Upload image to see results
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="alert-warning">
                    <h3 style="margin: 0 0 10px 0; color: var(--warning);">⚠️ No Wildlife Detected</h3>
                    <p style="margin: 0; color: var(--text-secondary);">
                        The 2-layer verification did not find any wildlife in this image.
                    </p>
                    {f'<p style="margin: 10px 0 0 0; font-size: 14px; color: var(--text-muted);">Reason: {result.get("rejection_reason", "Unknown")}</p>' if result.get('rejection_reason') else ''}
                </div>
                """, unsafe_allow_html=True)
                
                if result['layer1_detections']:
                    st.info(f"ℹ️ Layer 1 found {len(result['layer1_detections'])} potential detection(s), but Layer 2 verification failed")
