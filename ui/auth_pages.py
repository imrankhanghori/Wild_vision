"""
Authentication Pages
Modern Ultralytics-inspired login and signup with glassmorphism
"""

import streamlit as st
from database.user_manager import register_user, login_user, initialize_session


def _apply_auth_glass_theme():
    """Apply full-page gradient and glassmorphism styling to auth forms."""
    st.markdown(
        """
<style>
    /* Full-page subtle gradient background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #1e293b 0%, #020617 45%, #000000 100%) !important;
        padding-top: 40px;
    }

    /* Center content a bit better */
    [data-testid="stVerticalBlock"] > div:first-child {
        max-width: 900px;
        margin: 0 auto;
    }

    /* Glassmorphism card for Streamlit forms */
    [data-testid="stForm"] {
        max-width: 520px;
        margin: 0 auto 40px auto;
        padding: 32px 32px 28px 32px;
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.45);
        box-shadow: 0 24px 60px rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(18px);
    }

    /* Form labels & inputs slightly adjusted for readability */
    [data-testid="stForm"] label {
        font-weight: 500;
    }

    [data-testid="stForm"] input {
        background-color: rgba(15, 23, 42, 0.9);
        border-radius: 10px;
    }
</style>
        """,
        unsafe_allow_html=True,
    )


def show_login_page():
    """Display modern login page with centered glass auth card."""

    # Split layout: left (branding), right (auth form)
    col_brand, col_form = st.columns([2, 3])

    with col_brand:
        st.markdown("""
        <div style="
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 40px 24px 40px 8px;
        ">
            <h1 style="
                font-size: 42px; 
                font-weight: 900; 
                margin-bottom: 12px;
                background: linear-gradient(135deg, #63D7EB 0%, #a855f7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                🌿 Wild Vision
            </h1>
            <p style="
                font-size: 18px; 
                color: var(--text-secondary);
                margin-bottom: 12px;
            ">
                AI-Powered Wildlife Detection & Conservation
            </p>
            <p style="
                font-size: 14px;
                color: var(--text-muted);
                max-width: 320px;
            ">
                Secure access to your wildlife detection dashboard, alerts and analytics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.form("login_form"):
            st.markdown("""
            <div style="text-align: left; margin-bottom: 16px;">
                <h2 style="
                    font-size: 26px; 
                    font-weight: 700; 
                    color: var(--text-primary);
                    margin-bottom: 6px;
                ">Welcome back</h2>
                <p style="
                    font-size: 14px; 
                    color: var(--text-secondary);
                    margin-bottom: 12px;
                ">Sign in to access your wildlife detection dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
                help="Your unique username"
            )
            st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
                help="Your secure password"
            )

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            with col_btn2:
                if st.form_submit_button("Create Account", use_container_width=True, type="secondary"):
                    st.session_state['show_signup'] = True
                    st.rerun()

            if submit:
                username = st.session_state.get('login_username', '')
                password = st.session_state.get('login_password', '')

                if not username or not password:
                    st.error("⚠️ Please enter both username and password")
                else:
                    with st.spinner("Signing in..."):
                        success, message, user_data = login_user(username, password)

                        if success:
                            # Set session state
                            st.session_state['logged_in'] = True
                            st.session_state['user_id'] = user_data['user_id']
                            st.session_state['username'] = user_data['username']
                            st.session_state['email'] = user_data['email']

                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")


def show_signup_page():
    """Display modern signup page with centered glass auth card."""

    # Split layout: left (branding), right (auth form)
    col_brand, col_form = st.columns([2, 3])

    with col_brand:
        st.markdown("""
        <div style="
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 40px 24px 40px 8px;
        ">
            <h1 style="
                font-size: 42px; 
                font-weight: 900; 
                margin-bottom: 12px;
                background: linear-gradient(135deg, #63D7EB 0%, #a855f7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                🌿 Wild Vision
            </h1>
            <p style="
                font-size: 18px; 
                color: var(--text-secondary);
                margin-bottom: 12px;
            ">
                Join the conservation revolution
            </p>
            <p style="
                font-size: 14px;
                color: var(--text-muted);
                max-width: 320px;
            ">
                Create an account to start monitoring wildlife with AI-powered tools.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.form("signup_form"):
            st.markdown("""
            <div style="text-align: left; margin-bottom: 16px;">
                <h2 style="
                    font-size: 26px; 
                    font-weight: 700; 
                    color: var(--text-primary);
                    margin-bottom: 6px;
                ">Create your account</h2>
                <p style="
                    font-size: 14px; 
                    color: var(--text-secondary);
                    margin-bottom: 12px;
                ">Start protecting wildlife with AI-powered detection</p>
            </div>
            """, unsafe_allow_html=True)
            st.text_input(
                "Username",
                placeholder="Choose a username (min. 3 characters)",
                key="signup_username",
                help="Your unique identifier"
            )
            st.text_input(
                "Email",
                placeholder="your.email@example.com",
                key="signup_email",
                help="We'll send detection alerts here"
            )
            st.text_input(
                "Password",
                type="password",
                placeholder="Strong password (min. 6 characters)",
                key="signup_password",
                help="Keep it secure"
            )
            st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="signup_password_confirm"
            )

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
            with col_btn2:
                if st.form_submit_button("Back to Login", use_container_width=True, type="secondary"):
                    st.session_state['show_signup'] = False
                    st.rerun()

            if submit:
                username = st.session_state.get('signup_username', '')
                email = st.session_state.get('signup_email', '')
                password = st.session_state.get('signup_password', '')
                password_confirm = st.session_state.get('signup_password_confirm', '')

                if not username or not email or not password or not password_confirm:
                    st.error("⚠️ Please fill in all fields")
                elif password != password_confirm:
                    st.error("❌ Passwords do not match")
                elif len(username) < 3:
                    st.error("❌ Username must be at least 3 characters")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    with st.spinner("Creating your account..."):
                        success, message, user_id = register_user(username, email, password)

                        if success:
                            st.success(f"✅ {message}")
                            st.info("Please login with your new account")
                            st.session_state['show_signup'] = False

                            # Auto switch to login after 2 seconds
                            import time
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")


def show_auth_page():
    """Show appropriate auth page based on state."""
    initialize_session()
    
    # Initialize signup state
    if 'show_signup' not in st.session_state:
        st.session_state['show_signup'] = False
    
    # Apply shared glassmorphism theme for auth pages
    _apply_auth_glass_theme()

    # Show appropriate page
    if st.session_state.get('show_signup', False):
        show_signup_page()
    else:
        show_login_page()
