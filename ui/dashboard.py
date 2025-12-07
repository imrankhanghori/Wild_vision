"""
Dashboard Page
Ultralytics-inspired modern analytics dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from datetime import datetime
from pathlib import Path
from PIL import Image
import config
from database.user_manager import get_current_user_id
from database.detection_manager import (
    get_recent_detections,
    get_species_statistics,
    get_total_detections,
    get_detections_today
)
from ui.styles import format_confidence, create_species_badge, create_stat_card


def show_dashboard():
    """Display the modern Ultralytics-inspired dashboard."""
    
    user_id = get_current_user_id()
    
    # === HEADER ===
    st.markdown("""
    <div style="margin-bottom: 40px;">
        <h1 style="
            font-size: 42px; 
            font-weight: 900; 
            margin-bottom: 8px;
            background: linear-gradient(135deg, #63D7EB 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">📊 Analytics Dashboard</h1>
        <p style="
            font-size: 18px; 
            color: var(--text-secondary);
            margin: 0;
        ">Real-time wildlife detection insights and statistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # === METRICS CARDS ===
    col1, col2, col3, col4 = st.columns(4)
    
    total = get_total_detections(user_id)
    today_count = len(get_detections_today(user_id))
    species_stats = get_species_statistics(user_id)
    unique_species = len(species_stats)
    
    # Calculate uptime
    uptime_str = "0h 0m"
    if 'app_start_time' in st.session_state:
        uptime_seconds = (datetime.now() - st.session_state['app_start_time']).seconds
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_str = f"{uptime_hours}h {uptime_minutes}m"
    
    metrics_data = [
        (col1, "🎯", total, "Total Detections", "bg-info"),
        (col2, "📅", today_count, "Today's Count", "bg-success"),
        (col3, "🐾", unique_species, "Species Detected", "bg-warning"),
        (col4, "⚡", uptime_str, "System Uptime", "bg-danger")
    ]
    
    for col, icon, value, label, variant in metrics_data:
        with col:
            st.markdown(create_stat_card(label, value, icon, variant), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === CHARTS SECTION ===
    if species_stats:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("""
            <h3 style="
                font-size: 22px; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 20px;
            ">📈 Species Distribution</h3>
            """, unsafe_allow_html=True)
            
            # Donut chart
            df_species = pd.DataFrame(list(species_stats.items()), columns=['Species', 'Count'])
            df_species['Species_Label'] = df_species['Species'].apply(
                lambda x: f"{config.CLASS_EMOJIS.get(x, '')} {x}"
            )
            
            fig = px.pie(
                df_species,
                values='Count',
                names='Species_Label',
                hole=0.5,
                color_discrete_sequence=['#63D7EB', '#a855f7', '#3b82f6', '#fbbf24']
            )
            
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=14,
                marker=dict(line=dict(color='#0a0e27', width=2))
            )
            
            fig.update_layout(
                showlegend=True,
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=13),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                ),
                margin=dict(l=20, r=100, t=20, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            st.markdown("""
            <h3 style="
                font-size: 22px; 
                font-weight: 700; 
                color: var(--text-primary);
                margin-bottom: 20px;
            ">📊 Detection Count</h3>
            """, unsafe_allow_html=True)
            
            # Bar chart
            df_bar = pd.DataFrame(list(species_stats.items()), columns=['Species', 'Count'])
            df_bar = df_bar.sort_values('Count', ascending=True)
            df_bar['Species_Display'] = df_bar['Species'].apply(
                lambda x: f"{config.CLASS_EMOJIS.get(x, '🦁')} {x}"
            )
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    y=df_bar['Species_Display'],
                    x=df_bar['Count'],
                    orientation='h',
                    marker=dict(
                        color=df_bar['Count'],
                        colorscale=[[0, '#63D7EB'], [0.5, '#3b82f6'], [1, '#a855f7']],
                        line=dict(color='rgba(99, 215, 235, 0.5)', width=2)
                    ),
                    text=df_bar['Count'],
                    textposition='outside',
                    textfont=dict(size=14, color='white', family='Inter'),
                    hovertemplate='<b>%{y}</b><br>Detections: %{x}<extra></extra>'
                )
            ])
            
            fig_bar.update_layout(
                yaxis=dict(
                    tickfont=dict(color='#e2e8f0', size=13),
                    showgrid=False
                ),
                xaxis=dict(
                    title='Count',
                    titlefont=dict(color='#94a3b8', size=12),
                    tickfont=dict(color='#94a3b8', size=11),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showgrid=True
                ),
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
                height=350,
                showlegend=False,
                margin=dict(l=10, r=50, t=20, b=40)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px 40px;">
            <div style="font-size: 72px; margin-bottom: 20px;">📊</div>
            <h3 style="
                font-size: 22px; 
                font-weight: 700; 
                color: var(--text-secondary);
                margin-bottom: 12px;
            ">No detections yet</h3>
            <p style="color: var(--text-muted); font-size: 15px;">
                Start detecting wildlife to see analytics and insights
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === RECENT DETECTIONS TABLE ===
    st.markdown("""
    <h3 style="
        font-size: 22px; 
        font-weight: 700; 
        color: var(--text-primary);
        margin-bottom: 20px;
    ">🕒 Recent Detections</h3>
    """, unsafe_allow_html=True)
    
    recent = get_recent_detections(user_id, limit=config.RECENT_DETECTIONS_LIMIT)
    
    if recent:
        table_data = []
        for det in recent:
            table_data.append({
                'Time': det['timestamp'].strftime('%H:%M:%S'),
                'Date': det['timestamp'].strftime('%Y-%m-%d'),
                'Species': f"{config.CLASS_EMOJIS.get(det['species'], '🦁')} {det['species']}",
                'Layer 1': f"{det['confidence_layer1']:.1%}",
                'Layer 2': f"{det['confidence_layer2']:.1%}",
                'Location': f"15.880444°N, 74.518389°E",
                'Source': det['source'].capitalize(),
                'Alert': "✅" if det.get('alert_sent', False) else "⏳"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, hide_index=True, use_container_width=True, height=350)
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        alerts_sent = sum(1 for det in recent if det.get('alert_sent', False))
        avg_conf = sum(det['confidence_layer2'] for det in recent) / len(recent)
        
        stats = [
            (col1, len(recent), "Shown", "#63D7EB"),
            (col2, alerts_sent, "Alerts", "#fbbf24"),
            (col3, f"{avg_conf:.0%}", "Avg Conf", "#a855f7"),
            (col4, "ACTIVE", "Status", "#10b981")
        ]
        
        for col, value, label, color in stats:
            with col:
                st.markdown(f"""
                <div style="
                    background: rgba(99, 215, 235, 0.1);
                    border-left: 3px solid {color};
                    padding: 16px;
                    border-radius: 10px;
                    text-align: center;
                    margin-top: 16px;
                ">
                    <div style="color: {color}; font-size: 28px; font-weight: 900; margin-bottom: 6px;">{value}</div>
                    <div style="color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No recent detections to display")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === LOCATION MAP ===
    st.markdown("""
    <h3 style="
        font-size: 22px; 
        font-weight: 700; 
        color: var(--text-primary);
        margin-bottom: 20px;
    ">📍 Detection Location</h3>
    """, unsafe_allow_html=True)
    
    # Map configuration
    latitude = 15.880444
    longitude = 74.518389
    
    location_data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude],
        'name': ['Wildlife Detection Zone']
    })
    
    radar_core = pdk.Layer(
        'ScatterplotLayer',
        data=location_data,
        get_position='[lon, lat]',
        get_fill_color=[239, 68, 68, 200],
        radius_min_pixels=35,
        pickable=True,
        filled=True,
        stroked=True,
        get_line_color=[239, 68, 68],
        get_line_width=1
    )
    radar_ring1 = pdk.Layer(
        'ScatterplotLayer',
        data=location_data,
        get_position='[lon, lat]',
        get_fill_color=[239, 68, 68, 90],
        radius_min_pixels=60,
        pickable=False,
        filled=True,
        stroked=False
    )
    radar_ring2 = pdk.Layer(
        'ScatterplotLayer',
        data=location_data,
        get_position='[lon, lat]',
        get_fill_color=[239, 68, 68, 50],
        radius_min_pixels=85,
        pickable=False,
        filled=True,
        stroked=False
    )
    
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=14,
        pitch=45,
        bearing=-10
    )
    
    deck = pdk.Deck(
        layers=[radar_core, radar_ring1, radar_ring2],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v10',
        tooltip={
            'html': '<b style="color: #ef4444;">📍 {name}</b><br><span style="color: #94a3b8;">Active Monitoring</span>',
            'style': {'backgroundColor': '#1a1f3a', 'color': 'white', 'border': '1px solid #ef4444', 'borderRadius': '8px', 'padding': '10px'}
        }
    )
    
    st.pydeck_chart(deck, use_container_width=True)
    
    # Location info
    col1, col2, col3 = st.columns(3)
    location_info = [
        (col1, f"{latitude:.6f}°N", "Latitude"),
        (col2, f"{longitude:.6f}°E", "Longitude"),
        (col3, "🟢 ACTIVE", "Status")
    ]
    
    for col, value, label in location_info:
        with col:
            st.markdown(f"""
            <div style="
                background: var(--bg-surface);
                border: 1px solid var(--border-color);
                border-radius: 10px;
                padding: 16px;
                text-align: center;
                margin-top: 16px;
            ">
                <div style="color: var(--accent-cyan); font-size: 18px; font-weight: 700; margin-bottom: 4px;">{value}</div>
                <div style="color: var(--text-muted); font-size: 11px; text-transform: uppercase; letter-spacing: 1px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SNAPSHOT GALLERY ===
    st.markdown("""
    <h3 style="
        font-size: 22px; 
        font-weight: 700; 
        color: var(--text-primary);
        margin-bottom: 20px;
    ">🖼️ Recent Snapshots</h3>
    """, unsafe_allow_html=True)
    
    if recent:
        snapshots = []
        for det in recent[:12]:
            if det.get('snapshot_path'):
                snapshot_path = det['snapshot_path']
                resolved_path = None
                
                if Path(snapshot_path).exists():
                    resolved_path = snapshot_path
                elif not Path(snapshot_path).is_absolute():
                    abs_path = str(config.BASE_DIR / snapshot_path)
                    if Path(abs_path).exists():
                        resolved_path = abs_path
                
                if not resolved_path:
                    filename_only = Path(snapshot_path).name
                    snapshots_path = config.BASE_DIR / "snapshots" / filename_only
                    if snapshots_path.exists():
                        resolved_path = str(snapshots_path)
                
                if resolved_path:
                    snapshots.append({
                        'path': resolved_path,
                        'species': det['species'],
                        'confidence': det['confidence_layer2'],
                        'timestamp': det['timestamp']
                    })
        
        if snapshots:
            cols = st.columns(4)
            for idx, snap in enumerate(snapshots):
                col = cols[idx % 4]
                with col:
                    try:
                        img = Image.open(snap['path'])
                        img.thumbnail((300, 300))
                        st.image(
                            img,
                            caption=f"{config.CLASS_EMOJIS.get(snap['species'], '')} {snap['species']} - {snap['confidence']:.0%}",
                            use_column_width=True
                        )
                    except Exception as e:
                        st.warning(f"⚠️ Image not found")
        else:
            st.info("No snapshot images available")
    else:
        st.info("No snapshots to display")
