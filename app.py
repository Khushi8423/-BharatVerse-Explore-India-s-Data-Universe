import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="BharatVerse | India's Data Universe", layout='wide')

# Load data
df = pd.read_csv('/Users/macos/Downloads/India Data/india.csv')
list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')

# ---------- STYLING ----------
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
        }
        .title-container {
            background-color: #1f4e79;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .main-title {
            color: white;
            font-size: 48px;
            font-weight: 900;
            text-align: center;
            margin: 0;
        }
        .subtitle {
            color: #dce3ea;
            font-size: 20px;
            text-align: center;
            margin-top: 5px;
        }
        .stButton button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
        }
    </style>

    <div class="title-container">
        <div class="main-title">📡 BharatVerse</div>
        <div class="subtitle">Exploring the Data Universe of India, One District at a Time</div>
    </div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg", width=120)
st.sidebar.markdown("### 🔍 Filter your view")
selected_state = st.sidebar.selectbox('Select a State/Region', list_of_states)
primary = st.sidebar.selectbox('Primary Metric (Size)', sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Secondary Metric (Color)', sorted(df.columns[5:]))
plot = st.sidebar.button('📈 Plot Graph')

# ---------- METRICS ----------
if selected_state == 'Overall India':
    num_districts = df['District'].nunique()
    avg_primary = df[primary].mean()
    avg_secondary = df[secondary].mean()
else:
    state_df = df[df['State'] == selected_state]
    num_districts = state_df['District'].nunique()
    avg_primary = state_df[primary].mean()
    avg_secondary = state_df[secondary].mean()

st.markdown("### 📊 Quick Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Districts", num_districts)
col2.metric(f"Avg {primary}", f"{avg_primary:.2f}")
col3.metric(f"Avg {secondary}", f"{avg_secondary:.2f}")

# ---------- PLOTTING ----------
if plot:
    st.markdown("### 🗺️ Interactive Data Map")

    if selected_state == 'Overall India':
        fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", size=primary, color=secondary,
                                zoom=4, size_max=35, mapbox_style="carto-positron",
                                hover_name='District', color_continuous_scale='Plasma')
    else:
        state_df = df[df['State'] == selected_state]
        fig = px.scatter_mapbox(state_df, lat="Latitude", lon="Longitude", size=primary, color=secondary,
                                zoom=5, size_max=35, mapbox_style="carto-positron",
                                hover_name='District', color_continuous_scale='Plasma')

    st.plotly_chart(fig, use_container_width=True)