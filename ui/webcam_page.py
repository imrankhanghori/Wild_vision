"""
Webcam Streaming Page
Modern AdminLTE-inspired real-time detection interface
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import time
import config
from utils.video_processor import WebcamProcessor
from utils.verification import verify_detection_2layer, should_trigger_snapshot
from database.user_manager import get_current_user_id
from database.detection_manager import save_detection
from alerts.email_service import send_alert_if_ready


def show_webcam_page():
    """Display modern webcam streaming page with AdminLTE-inspired design."""
    
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
        ">📹 Live Webcam Detection</h1>
        <p style="
            font-size: 1.125rem; 
            color: var(--text-secondary);
            margin: 0;
        ">Real-time wildlife monitoring with AI-powered detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === CAMERA SOURCE SELECTION ===
    st.markdown("""
    <h3 style="
        font-size: 1.25rem; 
        font-weight: 700; 
        color: var(--text-primary);
        margin-bottom: 16px;
    ">📱 Camera Source</h3>
    """, unsafe_allow_html=True)
    
    col_src1, col_src2 = st.columns([2, 1])
    
    with col_src1:
        camera_source = st.radio(
            "Select source",
            options=["Laptop Camera (Index 0)", "IP Webcam (Phone)"],
            horizontal=True,
            key="camera_source",
            label_visibility="collapsed"
        )
    
    # IP Webcam URL input
    ip_webcam_url = None
    if camera_source == "IP Webcam (Phone)":
        ip_webcam_url = st.text_input(
            "IP Webcam URL",
            placeholder="http://192.168.1.100:8080/video",
            help="Example: http://YOUR_PHONE_IP:8080/video",
            key="ip_webcam_url"
        )
        
        if ip_webcam_url:
            st.markdown(f"""
            <div class="alert-info" style="
                background: rgba(14, 165, 233, 0.1);
                border-left: 3px solid var(--info);
                padding: 12px 16px;
                border-radius: var(--radius-md);
                margin: 12px 0;
            ">
                <span style="color: var(--info); font-weight: 600;">📡 Using IP Webcam:</span>
                <code style="
                    background: rgba(0,0,0,0.3);
                    padding: 2px 8px;
                    border-radius: 4px;
                    margin-left: 8px;
                    color: var(--text-primary);
                ">{ip_webcam_url}</code>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize webcam processor
    if 'webcam_processor' not in st.session_state:
        camera_input = ip_webcam_url if ip_webcam_url else 0
        st.session_state['webcam_processor'] = WebcamProcessor(camera_index=camera_input)
        st.session_state['webcam_running'] = False
    
    # Reinitialize if source changed
    current_source = ip_webcam_url if ip_webcam_url else 0
    if hasattr(st.session_state.get('webcam_processor'), 'camera_index'):
        if st.session_state['webcam_processor'].camera_index != current_source:
            if st.session_state.get('webcam_running', False):
                st.session_state['webcam_processor'].stop()
                st.session_state['webcam_running'] = False
            st.session_state['webcam_processor'] = WebcamProcessor(camera_index=current_source)
    
    # === CONTROL PANEL ===
    st.markdown("""
    <h3 style="
        font-size: 1.25rem; 
        font-weight: 700; 
        color: var(--text-primary);
        margin-bottom: 16px;
    ">🎮 Controls</h3>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3, col_c4 = st.columns([1.2, 1.2, 1.5, 1])
    
    with col_c1:
        if st.button("▶️ Start", use_container_width=True, type="primary", 
                    disabled=st.session_state.get('webcam_running', False)):
            if st.session_state['webcam_processor'].start():
                st.session_state['webcam_running'] = True
                st.success("✅ Webcam started!")
                st.rerun()
            else:
                st.error("❌ Failed to start webcam")
    
    with col_c2:
        if st.button("⏹️ Stop", use_container_width=True, type="secondary",
                    disabled=not st.session_state.get('webcam_running', False)):
            st.session_state['webcam_processor'].stop()
            st.session_state['webcam_running'] = False
            st.success("Webcam stopped!")
            st.rerun()
    
    with col_c3:
        enable_detection = st.checkbox(
            "🔍 Enable Detection", 
            value=True,
            help="Turn off to improve performance"
        )
    
    with col_c4:
        pass  # Spacer
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === WEBCAM DISPLAY ===
    if st.session_state.get('webcam_running', False):
        # Create placeholders
        video_col, stats_col = st.columns([3, 1])
        
        with video_col:
            video_placeholder = st.empty()
        
        with stats_col:
            st.markdown("""
            <div class="card" style="padding: 20px; margin-bottom: 16px;">
                <h4 style="
                    font-size: 1rem; 
                    font-weight: 700; 
                    color: var(--info);
                    margin: 0 0 16px 0;
                ">📊 Live Stats</h4>
            </div>
            """, unsafe_allow_html=True)
            stats_placeholder = st.empty()
            detection_placeholder = st.empty()
        
        alert_placeholder = st.empty()
        
        processor = st.session_state['webcam_processor']
        frame_skip_counter = 0
        
        # Initialize snapshot cooldown
        if 'last_snapshot_time' not in st.session_state:
            st.session_state['last_snapshot_time'] = 0
        
        SNAPSHOT_COOLDOWN = 5
        
        # === VIDEO LOOP ===
        while processor.is_running():
            success, frame = processor.read_frame()
            
            if not success:
                st.error("❌ Failed to read frame from webcam")
                break
            
            frame_skip_counter += 1
            should_process = frame_skip_counter % config.PROCESS_EVERY_N_FRAMES == 0
            
            if enable_detection and should_process:
                processed_frame, detections = processor.process_frame(
                    frame,
                    enable_detection=True,
                    conf_threshold=config.LAYER1_CONFIDENCE
                )
                
                # Check for auto-snapshot
                if detections and should_trigger_snapshot(detections):
                    current_time = time.time()
                    time_since_last = current_time - st.session_state['last_snapshot_time']
                    is_ip_webcam = isinstance(processor.camera_index, str)
                    can_snapshot = not is_ip_webcam or time_since_last >= SNAPSHOT_COOLDOWN
                    
                    if can_snapshot:
                        st.session_state['last_snapshot_time'] = current_time
                        
                        with stats_col:
                            st.info("🔍 Verifying...")
                        
                        result = verify_detection_2layer(frame)
                        
                        if result['verified']:
                            # Get all detected species
                            detected_species = {}
                            for det in result['layer2_detections']:
                                species = det['class_name']
                                if species not in detected_species or det['confidence'] > detected_species[species]['confidence']:
                                    detected_species[species] = det
                            
                            # Display alert
                            with alert_placeholder:
                                st.markdown(f"""
                                <div class="alert-success" style="
                                    background: rgba(16, 185, 129, 0.1);
                                    border: 1px solid var(--success);
                                    border-radius: var(--radius-md);
                                    padding: 20px;
                                    margin: 16px 0;
                                ">
                                    <h3 style="
                                        font-size: 1.25rem; 
                                        font-weight: 800; 
                                        color: var(--success);
                                        margin: 0 0 12px 0;
                                    ">✅ {len(detected_species)} Animal(s) Detected!</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                cols = st.columns(min(len(detected_species), 4))
                                for idx, (species, det) in enumerate(detected_species.items()):
                                    with cols[idx % 4]:
                                        st.markdown(f"""
                                        <div class="card" style="
                                            background: rgba(14, 165, 233, 0.1);
                                            padding: 12px;
                                            text-align: center;
                                            border: 1px solid var(--info);
                                        ">
                                            <div style="font-size: 2rem; margin-bottom: 6px;">
                                                {config.CLASS_EMOJIS.get(species, '')}
                                            </div>
                                            <div style="
                                                font-weight: 700;
                                                color: var(--info);
                                                font-size: 0.875rem;
                                            ">{species}</div>
                                            <div style="
                                                color: var(--text-secondary);
                                                font-size: 0.75rem;
                                            ">{det['confidence']:.0%}</div>
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
                                    source="webcam"
                                )
                                
                                if detection_id:
                                    saved_count += 1
                                    alert_sent, alert_msg = send_alert_if_ready(
                                        species=species,
                                        confidence_layer1=layer1_conf,
                                        confidence_layer2=det['confidence'],
                                        snapshot_path=result['snapshot_path'],
                                        user_id=user_id,
                                        location=config.DEFAULT_LOCATION,
                                        source="webcam"
                                    )
                                    
                                    if alert_sent:
                                        from database.detection_manager import update_detection_alert_status
                                        update_detection_alert_status(detection_id, alert_sent=True)
                            
                            if saved_count > 0:
                                with alert_placeholder:
                                    st.success(f"💾 {saved_count} detection(s) saved! Check Dashboard.")
            else:
                processed_frame = frame.copy()
                detections = []
            
            # Display frame
            display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            with video_col:
                video_placeholder.image(display_frame, channels="RGB", use_column_width=True)
            
            # Show stats
            with stats_col:
                with stats_placeholder:
                    fps = processor.get_fps()
                    st.markdown(f"""
                    <div style="margin: 16px 0;">
                        <div class="card" style="
                            padding: 12px;
                            margin-bottom: 8px;
                            background: var(--bg-card);
                        ">
                            <div style="color: var(--text-muted); font-size: 0.7rem; margin-bottom: 4px; text-transform: uppercase;">FPS</div>
                            <div style="color: var(--info); font-size: 1.5rem; font-weight: 900;">{fps:.1f}</div>
                        </div>
                        <div class="card" style="
                            padding: 12px;
                            background: var(--bg-card);
                        ">
                            <div style="color: var(--text-muted); font-size: 0.7rem; margin-bottom: 4px; text-transform: uppercase;">DETECTIONS</div>
                            <div style="color: var(--primary); font-size: 1.5rem; font-weight: 900;">{len(detections)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            time.sleep(0.01)
            
            if not st.session_state.get('webcam_running', False):
                break
    
    else:
        # Empty state - show instructions
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(16, 185, 129, 0.05) 100%);
            border: 2px dashed var(--border-color);
            border-radius: var(--radius-xl);
            padding: 60px 40px;
            text-align: center;
            margin: 40px 0;
        ">
            <div style="font-size: 100px; margin-bottom: 20px;">📹</div>
            <h3 style="
                font-size: 1.5rem; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 12px;
            ">Ready to start live detection</h3>
            <p style="
                font-size: 1rem; 
                color: var(--text-secondary);
                margin-bottom: 0;
            ">Click "Start" button above to begin real-time wildlife monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # How it works
        col_hw1, col_hw2 = st.columns(2)
        
        with col_hw1:
            st.markdown("""
            <h3 style="
                font-size: 1.25rem; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 16px;
            ">📋 How It Works</h3>
            """, unsafe_allow_html=True)
            
            steps = [
                ("1️⃣", "Choose Camera", "Select laptop or IP webcam"),
                ("2️⃣", "Start Stream", "Click start button to activate"),
                ("3️⃣", "Auto-Detect", "AI detects wildlife automatically"),
                ("4️⃣", "Verify & Save", "2-layer verification confirms"),
                ("5️⃣", "Alert Sent", "Email notification dispatched")
            ]
            
            for icon, title, desc in steps:
                st.markdown(f"""
                <div class="card" style="
                    padding: 14px 16px;
                    margin-bottom: 10px;
                    display: flex;
                    align-items: center;
                    gap: 14px;
                    flex-direction: row;
                ">
                    <div style="font-size: 28px;">{icon}</div>
                    <div>
                        <div style="
                            font-weight: 700;
                            color: var(--text-primary);
                            font-size: 0.875rem;
                            margin-bottom: 2px;
                        ">{title}</div>
                        <div style="
                            color: var(--text-secondary);
                            font-size: 0.75rem;
                        ">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_hw2:
            st.markdown("""
            <h3 style="
                font-size: 1.25rem; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 16px;
            ">📱 Using IP Webcam</h3>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="card" style="padding: 20px;">
                <ol style="color: var(--text-secondary); font-size: 0.875rem; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li>Download <strong style="color: var(--info);">IP Webcam</strong> app</li>
                    <li>Open app and tap <strong>"Start Server"</strong></li>
                    <li>Note the URL (e.g., 192.168.1.100:8080)</li>
                    <li>Add <code>/video</code> at the end</li>
                    <li>Enter URL above and start!</li>
                </ol>
                <div class="alert-warning" style="
                    margin-top: 16px;
                    padding: 12px;
                ">
                    <div style="color: var(--warning); font-size: 0.8rem; font-weight: 600;">
                        💡 Tip: Ensure phone and laptop are on same WiFi
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
