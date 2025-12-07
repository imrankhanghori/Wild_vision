"""
Custom Styles for Wild Vision App
Modern AdminLTE-inspired design with Slate/Indigo dark theme
Professional UI/UX with modern aesthetics
"""

import streamlit as st
import config


def load_custom_css():
    """Load custom CSS styles inspired by Modern AdminLTE design language."""
    
    css = f"""
    <style>
    /* ========== IMPORT FONTS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    
    /* ========== ROOT VARIABLES (Modern Dark Theme) ========== */
    :root {{
        /* Modern Palette (Slate & Indigo) */
        --bg-body: #0f172a;       /* Slate 900 */
        --bg-card: #1e293b;       /* Slate 800 */
        --bg-sidebar: #0f172a;    /* Slate 900 */
        
        --text-primary: #f8fafc;  /* Slate 50 */
        --text-secondary: #94a3b8; /* Slate 400 */
        --text-muted: #64748b;    /* Slate 500 */
        
        /* Vibrant Accents */
        --primary: #6366f1;       /* Indigo 500 */
        --primary-hover: #4f46e5; /* Indigo 600 */
        --secondary: #64748b;     /* Slate 500 */
        
        --success: #10b981;       /* Emerald 500 */
        --info: #0ea5e9;          /* Sky 500 */
        --warning: #f59e0b;       /* Amber 500 */
        --danger: #ef4444;        /* Red 500 */
        
        --light: #f1f5f9;
        --dark: #0f172a;
        
        --border-color: #334155;  /* Slate 700 */
        
        /* Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        
        /* Modern Shadows */
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-glow: 0 0 15px rgba(99, 102, 241, 0.3); /* Indigo Glow */
        
        --elevation-1: var(--shadow-sm);
        --elevation-2: var(--shadow-md);
    }}
    
    /* ========== GLOBAL STYLES ========== */
    * {{
        font-family: 'Inter', 'Source Sans Pro', sans-serif;
    }}
    
    .stApp {{
        background-color: var(--bg-body);
        color: var(--text-primary);
        background-image: radial-gradient(circle at top right, #1e1b4b 0%, transparent 40%),
                          radial-gradient(circle at bottom left, #064e3b 0%, transparent 40%);
    }}
    
    .block-container {{
        padding-top: 0.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }}

    /* Sticky top header for first columns block */
    .block-container > div[data-testid="stHorizontalBlock"]:first-of-type {{
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: rgba(30, 41, 59, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    }}

    /* Tighten button spacing in header */
    .block-container > div[data-testid="stHorizontalBlock"]:first-of-type .stButton {{
        margin: 0 !important;
    }}
    
    /* ========== TYPOGRAPHY ========== */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.75rem !important;
    }}
    
    h1 {{ 
        font-size: 3rem !important; 
        color: var(--text-primary) !important;
    }}
    
    h2 {{ font-size: 2.25rem !important; }}
    h3 {{ font-size: 1.5rem !important; }}
    
    p {{
        color: var(--text-secondary) !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }}
    
    /* ========== HOME SLIDESHOW EFFECTS ========== */
    .slideshow-container {{
        position: relative;
        width: 100%;
        max-width: 520px;
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.25);
        border: 1px solid var(--border-color);
    }}
    .slideshow-img {{
        width: 100%;
        height: auto;
        display: block;
        transform: translateX(0%);
        animation: slideSlow 8s linear infinite alternate;
        filter: contrast(1.05) saturate(1.05);
    }}
    .slideshow-vignette {{
        position: absolute;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(circle at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%);
    }}
    @keyframes slideSlow {{
        from {{ transform: translateX(-2%) scale(1.03); }}
        to   {{ transform: translateX(2%)  scale(1.06); }}
    }}
    
    .st-emotion-cache-10trblm.e1nzilvr1 {{
        color: var(--text-primary) !important;
        -webkit-text-fill-color: initial !important;
        background: none !important;
        visibility: visible !important;
    }}
    
    /* ========== HEADER / NAVIGATION ========== */
    .main-header {{
        background-color: rgba(30, 41, 59, 0.8); /* Glassy Slate 800 */
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border-color);
        padding: 1.25rem;
        margin-bottom: 2.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .brand-link {{
        font-size: 1.5rem;
        color: var(--text-primary);
        font-weight: 700;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    hr {{
        border: none;
        border-top: 1px solid var(--border-color);
        margin: 0 !important;
        opacity: 1 !important;
    }}
    
    /* ========== BUTTONS (Modern) ========== */
    .stButton > button {{
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        text-transform: none !important;
        box-shadow: var(--shadow-sm) !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1.25rem !important;
    }}
    
    /* Primary Button */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--primary) 0%, #4f46e5 100%) !important;
        color: #fff !important;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4) !important;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.5) !important;
    }}
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background-color: #334155 !important;
        color: var(--text-primary) !important;
        border-color: var(--primary) !important;
    }}
    
    /* ========== CARDS (Modern AdminLTE) ========== */
    .card {{
        background-color: rgba(15, 23, 42, 0.85);
        background-image: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(14, 165, 233, 0.12) 45%, rgba(45, 212, 191, 0.12) 100%);
        box-shadow: 0 12px 30px rgba(2, 6, 23, 0.35);
        margin-bottom: 1.5rem;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(148, 163, 184, 0.35);
        position: relative;
        display: flex;
        flex-direction: column;
        min-width: 0;
        word-wrap: break-word;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        backdrop-filter: blur(12px);
    }}
    
    .card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 45px rgba(2, 6, 23, 0.45);
        border-color: rgba(99, 102, 241, 0.75);
    }}
    
    .card-header {{
        background-color: rgba(15, 23, 42, 0.3);
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 1.5rem;
        border-top-left-radius: var(--radius-lg);
        border-top-right-radius: var(--radius-lg);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .card-title {{
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-primary);
    }}
    
    .card-body {{
        flex: 1 1 auto;
        padding: 1.5rem;
        color: var(--text-secondary);
    }}
    
    /* ========== SMALL BOXES (Modern Stats) ========== */
    .small-box {{
        border-radius: var(--radius-lg);
        position: relative;
        display: block;
        margin-bottom: 24px;
        box-shadow: var(--shadow-md);
        color: #fff;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .small-box:hover {{
        text-decoration: none;
        transform: translateY(-5px) scale(1.02);
        box-shadow: var(--shadow-lg);
    }}
    
    .small-box > .inner {{
        padding: 20px;
        position: relative;
        z-index: 2;
    }}
    
    .small-box h3 {{
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 4px 0;
        white-space: nowrap;
        padding: 0;
        color: #fff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .small-box p {{
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: rgba(255,255,255,0.9) !important;
        margin-bottom: 0;
    }}
    
    .small-box .icon {{
        transition: all .3s linear;
        position: absolute;
        top: -10px;
        right: 10px;
        z-index: 0;
        font-size: 90px;
        color: rgba(255,255,255,0.15);
        transform: rotate(0deg);
    }}
    
    .small-box:hover .icon {{
        transform: scale(1.1) rotate(-10deg);
    }}
    
    .small-box-footer {{
        position: relative;
        text-align: center;
        padding: 8px 0;
        color: rgba(255,255,255,0.9);
        display: block;
        z-index: 10;
        background: rgba(0,0,0,0.15);
        text-decoration: none;
        font-size: 0.875rem;
        font-weight: 500;
        backdrop-filter: blur(4px);
        transition: background 0.2s;
    }}
    
    .small-box-footer:hover {{
        background: rgba(0,0,0,0.25);
        color: #fff;
    }}
    
    /* Modern Gradients */
    .bg-info {{ 
        background: linear-gradient(135deg, var(--info) 0%, #0284c7 100%) !important; 
    }}
    .bg-success {{ 
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%) !important; 
    }}
    .bg-warning {{ 
        background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%) !important; 
        color: #fff !important; 
    }}
    .bg-danger {{ 
        background: linear-gradient(135deg, var(--danger) 0%, #b91c1c 100%) !important; 
    }}
    .bg-primary {{ 
        background: linear-gradient(135deg, var(--primary) 0%, #4338ca 100%) !important; 
    }}
    
    /* ========== METRICS (Streamlit Override) ========== */
    div[data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stMetricLabel"] {{
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
    }}
    
    /* ========== TABLES ========== */
    .dataframe {{
        background-color: var(--bg-card) !important;
        color: var(--text-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        overflow: hidden;
    }}
    
    .dataframe th {{
        background-color: #0f172a !important; /* Darker header */
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--border-color) !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
    }}
    
    .dataframe td {{
        border-bottom: 1px solid var(--border-color) !important;
        color: var(--text-secondary) !important;
        padding: 12px !important;
    }}
    
    .dataframe tr:hover {{
        background-color: rgba(99, 102, 241, 0.05) !important; /* Slight Indigo tint */
    }}
    
    /* ========== INPUTS ========== */
    .stTextInput > div > div > input {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1rem !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }}
    
    /* ========== ALERTS ========== */
    .alert-success {{
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: var(--success);
        padding: 1rem;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
    }}
    
    .alert-warning {{
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: var(--warning);
        padding: 1rem;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
    }}
    
    .alert-danger {{
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.2);
        color: var(--danger);
        padding: 1rem;
        border-radius: var(--radius-md);
        margin-bottom: 1rem;
    }}
    
    /* ========== HIDE STREAMLIT BRANDING ========== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def format_confidence(confidence):
    """
    Format confidence score with color coding (Modern Badges).
    """
    percentage = confidence * 100
    
    if percentage >= 80:
        color = "var(--success)"
        bg = "rgba(16, 185, 129, 0.1)"
    elif percentage >= 60:
        color = "var(--warning)"
        bg = "rgba(245, 158, 11, 0.1)"
    else:
        color = "var(--danger)"
        bg = "rgba(239, 68, 68, 0.1)"
    
    style = f"display: inline-block; padding: 0.25em 0.6em; font-size: 0.75rem; font-weight: 700; line-height: 1; text-align: center; white-space: nowrap; vertical-align: baseline; border-radius: 9999px; color: {color}; background-color: {bg}; border: 1px solid {color};"
    
    return f'<span style="{style}">{percentage:.1f}%</span>'


def create_species_badge(species):
    """
    Create a species badge with emoji.
    """
    emoji = config.CLASS_EMOJIS.get(species, '🔍')
    return f'''
    <span style="display: inline-flex; align-items: center; gap: 8px; color: var(--text-primary); font-weight: 500;">
        <span style="font-size: 1.25em; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">{emoji}</span>
        <span>{species}</span>
    </span>
    '''


def create_confidence_bar(confidence, label="Confidence"):
    """
    Create a visual confidence progress bar (Modern style).
    """
    percentage = confidence * 100
    
    if percentage >= 80:
        bg_color = "var(--success)"
    elif percentage >= 60:
        bg_color = "var(--warning)"
    else:
        bg_color = "var(--danger)"
        
    return f'<div style="margin: 12px 0;"><div style="display: flex; justify-content: space-between; margin-bottom: 6px;"><span style="font-size: 0.8rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">{label}</span><span style="font-size: 0.8rem; font-weight: 700; color: var(--text-primary);">{percentage:.1f}%</span></div><div style="height: 8px; background-color: rgba(255,255,255,0.05); border-radius: 9999px; overflow: hidden;"><div style="width: {percentage}%; height: 100%; background-color: {bg_color}; border-radius: 9999px; box-shadow: 0 0 10px {bg_color}; transition: width 0.5s ease;"></div></div></div>'


def create_stat_card(label, value, icon="📊", variant="bg-info"):
    """
    Create a statistic card (Modern Small Box).
    
    Args:
        label (str): Label for the stat
        value (str/int): Value to display
        icon (str): Emoji icon
        variant (str): CSS class for background (bg-info, bg-success, bg-warning, bg-danger)
        
    Returns:
        str: HTML formatted stat card
    """
    return f'''
    <div class="small-box {variant}">
        <div class="inner">
            <h3>{value}</h3>
            <p>{label}</p>
        </div>
        <div class="icon">
            {icon}
        </div>
        <a href="#" class="small-box-footer">
            More info <span style="font-size: 12px;">➜</span>
        </a>
    </div>
    '''
