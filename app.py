import streamlit as st
import duckdb
import pandas as pd
import time
from pipeline import run_pipeline

st.set_page_config(page_title="Live Market Pulse", layout="wide")

# --- UI STATIC HEADER (Never Refreshes) ---
st.title("🏛️ Professional Market Pulse")
st.markdown("Automated AI-Driven Extraction & Real-Time Analytics")

# Placeholders: These stay on the screen, only their CONTENT changes
timestamp_box = st.empty() 
metrics_area = st.empty()
chart_area = st.empty()
table_area = st.empty()

# The Infinite Loop (The "Engine")
while True:
    try:
        # 1. Run the background ETL
        run_pipeline()

        # 2. Fetch fresh data
        conn = duckdb.connect('market_data.db', read_only=True)
        df = conn.execute("SELECT * FROM prices").df()
        last_sync = df['updated_at'].iloc[0] if not df.empty else "Connecting..."
        conn.close()

        # 3. Update the Timestamp (In-place)
        timestamp_box.markdown(f"""
            <div style="background-color: #1e2130; padding: 15px; border-radius: 8px; border-left: 5px solid #00ff00; margin-bottom: 20px;">
                <span style="color: #888; font-size: 12px; letter-spacing: 1px;">SYSTEM STATUS: STREAMING</span><br>
                <span style="color: #ffffff; font-size: 18px;">LAST UPDATED: </span>
                <span style="color: #00ff00; font-weight: bold; font-family: monospace; font-size: 22px;">{last_sync}</span>
            </div>
        """, unsafe_allow_html=True)

        # 4. Update the Results (In-place)
        if not df.empty:
            with metrics_area.container():
                cols = st.columns(4)
                for i, row in df.iterrows():
                    with cols[i % 4]:
                        st.markdown(f"""
                            <div style="background-color: #1e2130; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #31333f;">
                                <div style="color:#888; font-size: 12px;">{row['ticker']}</div>
                                <div style="font-weight:bold; font-size: 16px;">{row['name']}</div>
                                <div style="font-size:22px; color:#29b5e8; font-family: monospace;">${row['price']:.2f}</div>
                                <div style="color:{'#00ff00' if '+' in str(row['change']) else '#ff4b4b'}; font-size: 14px;">{row['change']}</div>
                            </div>
                        """, unsafe_allow_html=True)

            with chart_area.container():
                st.write("### Market Depth")
                st.bar_chart(data=df, x="ticker", y="price", color="#29b5e8")

            with table_area.container():
                st.dataframe(df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.warning(f"Waiting for pipeline sync... ({e})")

    # 5. The Sleep (Crucial for stability)
    time.sleep(5) 
