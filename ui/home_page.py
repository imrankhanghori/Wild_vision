"""
Home Page - Wild Vision
Modern AdminLTE-inspired landing page
"""

import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from pathlib import Path
import base64
import config
from database.detection_manager import get_detection_stats
from ui.styles import create_stat_card


def show_home_page():
    """Display the Modern AdminLTE-inspired home page with dark theme."""
    
    # === HERO SECTION ===
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style="padding: 60px 40px 60px 0;">
            <h1 style="
                font-size: 3.5rem; 
                font-weight: 900; 
                line-height: 1.1; 
                margin-bottom: 24px;
                color: var(--text-primary);
            ">
                Turn wildlife images into AI-powered insights
            </h1>
            <p style="
                font-size: 1.25rem; 
                color: var(--text-secondary); 
                line-height: 1.6;
                margin-bottom: 40px;
                max-width: 600px;
            ">
                Real-time detection with YOLO11. Advanced 2-layer verification. 
                Instant alerts. No code required — just drag, drop, and protect wildlife.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # CTA Buttons
        btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1.5, 2])
        with btn_col1:
            if st.button("🚀 Start Detection", use_container_width=True, type="primary"):
                st.session_state['current_page'] = "📹 Webcam Detection"
                st.rerun()
        with btn_col2:
            if st.button("📖 Learn More", use_container_width=True, type="secondary"):
                st.session_state['current_page'] = "📊 Dashboard"
                st.rerun()
    
    with col2:
        # Detection visual showcase with gradient background + image slideshow
        image_paths = [
            Path(config.BASE_DIR) / "ui" / "home_page_images" / "ChatGPT Image Dec 4, 2025, 06_46_17 PM.png",
            Path(config.BASE_DIR) / "ui" / "home_page_images" / "ChatGPT Image Dec 4, 2025, 06_46_37 PM.png",
            Path(config.BASE_DIR) / "ui" / "home_page_images" / "ChatGPT Image Dec 4, 2025, 06_46_43 PM.png",
            Path(config.BASE_DIR) / "ui" / "home_page_images" / "ChatGPT Image Dec 4, 2025, 06_46_49 PM.png",
        ]
        valid_paths = [p for p in image_paths if p.exists()]
        if valid_paths:
            count = st_autorefresh(interval=8000, key="home_slider_autoplay")
            idx = count % len(valid_paths)
            img_path = valid_paths[idx]
            try:
                mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"
                data = base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
                    border-radius: var(--radius-xl);
                    padding: 24px;
                    text-align: center;
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    box-shadow: var(--shadow-glow);
                ">
                    <div class="slideshow-container">
                        <img class="slideshow-img" src="data:{mime};base64,{data}" alt="Wildlife" />
                        <div class="slideshow-vignette"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as _:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
                    border-radius: var(--radius-xl);
                    padding: 40px;
                    text-align: center;
                    border: 1px solid rgba(99, 102, 241, 0.2);
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    box-shadow: var(--shadow-glow);
                ">
                    <div style="font-size: 120px; margin-bottom: 20px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));">🐅</div>
                    <p style="margin-top: 30px; color: var(--text-secondary); font-size: 14px;">
                        Slideshow unavailable
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
                border-radius: var(--radius-xl);
                padding: 40px;
                text-align: center;
                border: 1px solid rgba(99, 102, 241, 0.2);
                min-height: 400px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: var(--shadow-glow);
            ">
                <div style="font-size: 120px; margin-bottom: 20px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));">🐅</div>
                <p style="margin-top: 30px; color: var(--text-secondary); font-size: 14px;">
                    Add images to ui/home_page_images to enable slideshow
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === STATS BANNER ===
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h3 style="
            font-size: 14px; 
            font-weight: 600; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            color: var(--primary);
            margin-bottom: 20px;
        ">
            Trusted by Conservation Leaders
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    stats = get_detection_stats()
    col1, col2, col3, col4 = st.columns(4)
    
    # Use the new create_stat_card function for consistency
    stats_data = [
        ("🎯", stats.get('total_detections', 0), "Total Detections", "bg-info"),
        ("🐾", stats.get('unique_species', 0), "Species Tracked", "bg-success"),
        ("📊", stats.get('today_detections', 0), "Today's Count", "bg-warning"),
        ("⚡", "98.6%", "Model Accuracy", "bg-danger")
    ]
    
    for col, (icon, value, label, variant) in zip([col1, col2, col3, col4], stats_data):
        with col:
            st.markdown(create_stat_card(label, value, icon, variant), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === FEATURES SECTION ===
    st.markdown("""
    <div style="text-align: center; margin: 80px 0 60px 0;">
        <h2 style="
            font-size: 2.5rem; 
            font-weight: 800; 
            margin-bottom: 16px;
            color: var(--text-primary);
        ">
            Create powerful AI models like a pro on Wild Vision
        </h2>
        <p style="font-size: 1.125rem; color: var(--text-secondary);">
            Everything you need to detect, verify, and protect wildlife in one platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature grid
    col1, col2, col3 = st.columns(3)
    
    features = [
        {
            "icon": "1️⃣",
            "title": "Train models in seconds",
            "desc": "Upload images and let YOLO11 do the heavy lifting. 98.58% accuracy out of the box."
        },
        {
            "icon": "2️⃣",
            "title": "2-layer verification",
            "desc": "Dual threshold system eliminates false positives. Only verified detections recorded."
        },
        {
            "icon": "3️⃣",
            "title": "Test on mobile device",
            "desc": "IP webcam support lets you use your phone camera for remote wildlife monitoring."
        },
        {
            "icon": "4️⃣",
            "title": "Deploy instantly",
            "desc": "Real-time alerts via email. MongoDB storage for comprehensive analytics."
        },
        {
            "icon": "📹",
            "title": "Live webcam streaming",
            "desc": "Monitor wildlife 24/7 with real-time detection and auto-snapshot capture."
        },
        {
            "icon": "📊",
            "title": "Analytics dashboard",
            "desc": "Species distribution, detection trends, and interactive maps for data-driven insights."
        }
    ]
    
    for i, col in enumerate([col1, col2, col3]):
        for j in range(2):
            idx = i * 2 + j
            if idx < len(features):
                feature = features[idx]
                with col:
                    st.markdown(f"""
                    <div class="card" style="min-height: 240px; padding: 24px;">
                        <div style="font-size: 40px; margin-bottom: 16px;">{feature['icon']}</div>
                        <h3 style="
                            font-size: 1.25rem; 
                            font-weight: 700; 
                            color: var(--text-primary);
                            margin-bottom: 12px;
                        ">{feature['title']}</h3>
                        <p style="
                            font-size: 1rem; 
                            color: var(--text-secondary);
                            line-height: 1.6;
                            margin: 0;
                        ">{feature['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === SPECIES SHOWCASE ===
    st.markdown("""
    <div style="text-align: center; margin: 80px 0 60px 0;">
        <h2 style="
            font-size: 2.5rem; 
            font-weight: 800; 
            margin-bottom: 16px;
            color: var(--text-primary);
        ">
            Powered by Ultralytics YOLO – the state-of-the-art AI
        </h2>
        <p style="font-size: 1.125rem; color: var(--text-secondary);">
            Detect and classify 4 endangered species with industry-leading accuracy
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    species_data = [
        ("🐅", "Tiger"),
        ("🐻", "Bear"),
        ("🐆", "Leopard"),
        ("🐘", "Elephant")
    ]
    
    for col, (emoji, name) in zip([col1, col2, col3, col4], species_data):
        with col:
            st.markdown(f"""
            <div class="card" style="
                text-align: center; 
                padding: 40px 20px;
                background: linear-gradient(135deg, var(--bg-card) 0%, rgba(99, 102, 241, 0.05) 100%);
                border: 1px solid var(--border-color);
            ">
                <div style="font-size: 72px; margin-bottom: 16px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));">{emoji}</div>
                <h3 style="
                    font-size: 1.5rem; 
                    font-weight: 700; 
                    color: var(--primary);
                    margin: 0;
                ">{name}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === USE CASES SECTION ===
    st.markdown("""
    <div style="text-align: center; margin: 80px 0 60px 0;">
        <h2 style="
            font-size: 2.5rem; 
            font-weight: 800; 
            margin-bottom: 16px;
            color: var(--text-primary);
        ">
            We help innovators like you apply computer vision
        </h2>
        <p style="font-size: 1.125rem; color: var(--text-secondary);">
            Trusted by forest departments, researchers, and conservation NGOs worldwide
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    use_cases = [
        {
            "icon": "🏛️",
            "title": "Forest Departments",
            "desc": "Monitor protected areas and prevent poaching with automated real-time surveillance"
        },
        {
            "icon": "🔬",
            "title": "Researchers",
            "desc": "Collect behavioral data and study patterns with comprehensive detection logs"
        },
        {
            "icon": "🌍",
            "title": "Conservation NGOs",
            "desc": "Track biodiversity and measure conservation impact with automated reporting"
        }
    ]
    
    for col, use_case in zip([col1, col2, col3], use_cases):
        with col:
            st.markdown(f"""
            <div class="card" style="
                border-left: 4px solid var(--info);
                padding: 32px;
                min-height: 220px;
            ">
                <div style="font-size: 48px; margin-bottom: 20px;">{use_case['icon']}</div>
                <h3 style="
                    font-size: 1.25rem; 
                    font-weight: 700; 
                    color: var(--info);
                    margin-bottom: 16px;
                ">{use_case['title']}</h3>
                <p style="
                    font-size: 1rem; 
                    color: var(--text-secondary);
                    line-height: 1.6;
                    margin: 0;
                ">{use_case['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === HOW IT WORKS ===
    st.markdown("""
    <div style="text-align: center; margin: 80px 0 60px 0;">
        <h2 style="
            font-size: 2.5rem; 
            font-weight: 800; 
            margin-bottom: 16px;
            color: var(--text-primary);
        ">
            Get started in 3 simple steps
        </h2>
        <p style="font-size: 1.125rem; color: var(--text-secondary);">
            From capture to conservation in minutes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    steps = [
        {
            "num": "1",
            "icon": "📸",
            "title": "Upload or Stream",
            "desc": "Drag and drop images or start live webcam monitoring"
        },
        {
            "num": "2",
            "icon": "🤖",
            "title": "Detect & Verify",
            "desc": "AI identifies species with 2-layer verification"
        },
        {
            "num": "3",
            "icon": "📧",
            "title": "Alert & Analyze",
            "desc": "Instant alerts and comprehensive analytics dashboard"
        }
    ]
    
    for col, step in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div class="card" style="
                text-align: center; 
                padding: 50px 30px;
                position: relative;
                overflow: visible;
            ">
                <div style="
                    position: absolute;
                    top: -20px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 50px;
                    height: 50px;
                    background: linear-gradient(135deg, var(--primary) 0%, #4f46e5 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    font-weight: 900;
                    color: white;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
                ">{step['num']}</div>
                <div style="font-size: 64px; margin: 20px 0;">{step['icon']}</div>
                <h3 style="
                    font-size: 1.25rem; 
                    font-weight: 700; 
                    color: var(--primary);
                    margin-bottom: 16px;
                ">{step['title']}</h3>
                <p style="
                    font-size: 1rem; 
                    color: var(--text-secondary);
                    line-height: 1.6;
                    margin: 0;
                ">{step['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === CTA SECTION ===
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-xl);
        padding: 60px 40px;
        text-align: center;
        margin: 80px 0 40px 0;
        box-shadow: var(--shadow-lg);
    ">
        <h2 style="
            font-size: 2.5rem; 
            font-weight: 800; 
            margin-bottom: 20px;
            background: linear-gradient(to right, #818cf8, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">
            Let's build the future of wildlife protection together!
        </h2>
        <p style="
            font-size: 1.125rem; 
            color: var(--text-secondary);
            margin-bottom: 40px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        ">
            Join conservation leaders using AI-powered detection to protect endangered species
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Free", use_container_width=True, type="primary"):
            st.session_state['current_page'] = "📹 Webcam Detection"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # === FOOTER ===
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h3 style="
            font-size: 1.75rem; 
            font-weight: 800;
            background: linear-gradient(to right, #818cf8, #2dd4bf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        ">🌿 Wild Vision</h3>
        <p style="color: var(--text-secondary); margin-bottom: 30px;">
            AI-Powered Wildlife Detection & Conservation
        </p>
        <p style="color: var(--text-muted); font-size: 0.875rem;">
            © 2025 Wild Vision. Powered by YOLO11 & MongoDB.
        </p>
        <p style="color: var(--text-muted); font-size: 0.8rem; margin-top: 8px;">
            🌱 Conservation technology for a sustainable future
        </p>
    </div>
    """, unsafe_allow_html=True)
