"""
Wild Vision - Wildlife Detection System
Main Streamlit Application

A production-ready wildlife detection system featuring:
- Real-time webcam streaming with YOLO11 detection
- 2-layer verification to reduce false positives
- MongoDB database for detection history
- Email alerts with cooldown management
- User authentication and session management
- Modern glassmorphism UI design
"""

import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import config
from database.mongodb_client import initialize_database, test_connection
from database.user_manager import initialize_session, is_logged_in, logout_user
from ui.styles import load_custom_css
from ui.auth_pages import show_auth_page
from ui.home_page import show_home_page
from ui.dashboard import show_dashboard
from ui.webcam_page import show_webcam_page
from ui.upload_page import show_upload_page


def main():
    """Main application entry point."""
    
    # Page config
    st.set_page_config(
        page_title="Wild Vision - Wildlife Detection",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session
    initialize_session()
    
    # Track app start time for uptime
    if 'app_start_time' not in st.session_state:
        st.session_state['app_start_time'] = datetime.now()
    
    # === CHECK MONGODB CONNECTION ===
    if not test_connection():
        st.error("❌ MongoDB Connection Failed")
        st.warning("""
        **Please ensure MongoDB is running:**
        1. Start MongoDB service: `mongod`
        2. Verify connection at: `localhost:27017`
        3. Refresh this page
        """)
        st.stop()
    
    # Initialize database (create indexes)
    if 'db_initialized' not in st.session_state:
        if initialize_database():
            st.session_state['db_initialized'] = True
    
    # === AUTHENTICATION CHECK ===
    if not is_logged_in():
        show_auth_page()
        return
    
    # === HEADER NAVIGATION ===
    # Initialize page in session state
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "🏠 Home"
    
    # Create header navigation with Settings as regular button
    header_col1, header_col2, header_col3, header_col4, header_col5, header_col6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1.5])
    
    with header_col1:
        st.markdown("""
        <div style="display: flex; align-items: center; height: 100%; padding: 0;">
            <h2 style="
                margin: 0; 
                background: linear-gradient(to right, #818cf8, #2dd4bf);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 800;
                font-size: 1.75rem;
                line-height: 1;
            ">🌿 Wild Vision</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state['current_page'] == "🏠 Home" else "secondary"):
            st.session_state['current_page'] = "🏠 Home"
            st.rerun()
    
    with header_col3:
        if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state['current_page'] == "📊 Dashboard" else "secondary"):
            st.session_state['current_page'] = "📊 Dashboard"
            st.rerun()
    
    with header_col4:
        if st.button("📹 Webcam", use_container_width=True, type="primary" if st.session_state['current_page'] == "📹 Webcam Detection" else "secondary"):
            st.session_state['current_page'] = "📹 Webcam Detection"
            st.rerun()
    
    with header_col5:
        if st.button("📤 Upload", use_container_width=True, type="primary" if st.session_state['current_page'] == "📤 Upload Image" else "secondary"):
            st.session_state['current_page'] = "📤 Upload Image"
            st.rerun()
    
    with header_col6:
        if st.button("⚙️ Settings", use_container_width=True, 
                    type="primary" if st.session_state.get('show_settings', False) else "secondary"):
            st.session_state['show_settings'] = not st.session_state.get('show_settings', False)
            st.rerun()

    # Divider directly under the navbar
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Settings panel (shows when Settings button clicked)
    if st.session_state.get('show_settings', False):
        st.markdown("---")
        st.markdown("### ⚙️ Settings & Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👤 User Info**")
            st.caption(f"**Name:** {st.session_state.get('username', 'User')}")
            st.caption(f"**Email:** {st.session_state.get('email', '')}")
        
        with col2:
            st.markdown("**⚙️ Settings**")
            auto_refresh_enabled = st.checkbox(
                "Auto-refresh Dashboard",
                value=False,
                help="Refresh dashboard every 5 seconds (keep off for stable map)"
            )
        
        with col3:
            st.markdown("**ℹ️ System Info**")
            st.caption(f"**Model:** YOLO11-Large")
            st.caption(f"**Classes:** {len(config.CLASS_NAMES)}")
            st.caption(f"**Layer 1:** {config.LAYER1_CONFIDENCE:.0%}")
            st.caption(f"**Layer 2:** {config.LAYER2_CONFIDENCE:.0%}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logout button in settings panel
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                logout_user()
                st.rerun()
        
        st.markdown("---")
    else:
        # Default auto-refresh setting when settings not shown
        auto_refresh_enabled = False
    
    # Auto-refresh logic (only if enabled)
    if auto_refresh_enabled and st.session_state['current_page'] == "📊 Dashboard":
        st_autorefresh(interval=config.DASHBOARD_REFRESH_INTERVAL, key="dashboard_refresh")
    
    
    
    # === MAIN CONTENT ===
    page = st.session_state['current_page']
    
    if page == "🏠 Home":
        show_home_page()
    
    elif page == "📊 Dashboard":
        show_dashboard()
    
    elif page == "📹 Webcam Detection":
        show_webcam_page()
    
    elif page == "📤 Upload Image":
        show_upload_page()


if __name__ == "__main__":
    main()
