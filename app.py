import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import plotly.express as px

#  Set page configuration
st.set_page_config(page_title="LHC ANOMALY DETECTION", layout="wide")

#  Function to apply wallpaper + animations
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    animations = f"""
    <style>
    /* Background Image */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* SLIDE-IN TEXT ANIMATION */
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .slide-in {{
        opacity: 0;
        animation: slideIn 1s ease-out forwards;
    }}

    /*SLIDING SIDEBAR */
    [data-testid="stSidebar"] {{
        transition: all 0.5s ease-in-out;
        transform: translateX(-100%);
        opacity: 0;
    }}
    [data-testid="stSidebar"]:hover {{
        transform: translateX(0);
        opacity: 1;
    }}

    /*PARTICLE ANIMATION */
    @keyframes float {{
        0% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0); }}
    }}
    .particle {{
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        animation: float 3s infinite ease-in-out;
    }}

    /*TWINKLING STARS */
    @keyframes twinkle {{
        0% {{ opacity: 0.2; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.2; }}
    }}
    .star {{
        position: absolute;
        width: 2px;
        height: 2px;
        background: white;
        border-radius: 50%;
        animation: twinkle 2s infinite ease-in-out;
    }}
    </style>
    """

    particles_html = """
    <div>
        <div class="particle" style="top: 10%; left: 15%;"></div>
        <div class="particle" style="top: 30%; left: 25%;"></div>
        <div class="particle" style="top: 50%; left: 45%;"></div>
        <div class="particle" style="top: 70%; left: 65%;"></div>
        <div class="particle" style="top: 90%; left: 85%;"></div>
    </div>
    """

    stars_html = """
    <div>
        <div class="star" style="top: 5%; left: 10%;"></div>
        <div class="star" style="top: 20%; left: 30%;"></div>
        <div class="star" style="top: 40%; left: 50%;"></div>
        <div class="star" style="top: 60%; left: 70%;"></div>
        <div class="star" style="top: 80%; left: 90%;"></div>
    </div>
    """

    st.markdown(animations, unsafe_allow_html=True)
    st.markdown(particles_html, unsafe_allow_html=True)
    st.markdown(stars_html, unsafe_allow_html=True)

image_path = "lhc_project.jpeg"
if os.path.exists(image_path):
    set_background(image_path)
else:
    st.error(f"⚠️ Background image not found: {image_path}")

# Header with SLIDING TEXT animation
st.markdown("<h1 class='slide-in' style='text-align: center; font-size: 50px; color: white;'> LHC Anomaly Detection</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='slide-in' style='text-align: center; color: white;'>Upload a CSV file to detect anomalies in LHC experiment data.</h4>", unsafe_allow_html=True)

#Sidebar with sliding effect
st.sidebar.markdown("<h2 style='color: white;'>⚙️ Settings</h2>", unsafe_allow_html=True)
view_3d = st.sidebar.toggle("Switch to 3D Visualization")  # ✅ 3D Toggle moved to sidebar

#File uploader
uploaded_file = st.file_uploader("Upload LHC Data (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    #Display uploaded data
    st.markdown("<h3 class='slide-in' style='color: white;'> Uploaded Data Preview:</h3>", unsafe_allow_html=True)
    st.dataframe(df.head())

    #Simulating Anomaly Scores (For Testing)
    np.random.seed(42)
    df["Anomaly_Score"] = np.random.uniform(0, 1, len(df))

    #Compute Dynamic Threshold (95th percentile)
    threshold = np.percentile(df["Anomaly_Score"], 95)

    #Mark anomalies based on dynamic threshold
    df["Anomaly"] = (df["Anomaly_Score"] > threshold).astype(int)

    #Histogram for Anomaly Scores
    st.markdown("<h3 class='slide-in' style='color: white;'> Histogram of Anomaly Scores:</h3>", unsafe_allow_html=True)
    fig_hist = px.histogram(df, x="Anomaly_Score", nbins=50, title="Anomaly Score Distribution")
    fig_hist.add_vline(x=threshold, line_dash="dash", line_color="red", annotation_text="95th Percentile Threshold")
    st.plotly_chart(fig_hist)

    #Circle Chart (Pie) for Anomalies
    st.markdown("<h3 class='slide-in' style='color: white;'> Anomaly Percentage Chart:</h3>", unsafe_allow_html=True)
    anomaly_pie = px.pie(
        values=[df["Anomaly"].sum(), len(df) - df["Anomaly"].sum()],
        names=["Anomalies", "Normal"],
        title="Anomaly Percentage",
        color_discrete_sequence=["red", "green"]
    )
    st.plotly_chart(anomaly_pie)

    #Show 3D Visualization Only if Toggled
    if view_3d:
        st.markdown("<h3 class='slide-in' style='color: white;'> Interactive 3D Anomaly Scatter Plot:</h3>", unsafe_allow_html=True)
        fig_3d = px.scatter_3d(
            df,
            x=df.index,
            y="Anomaly_Score",
            z="Anomaly",
            color="Anomaly",
            title="3D Visualization of Anomalies",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_3d)

    #Show anomaly counts
    st.markdown(f"<h3 class='slide-in' style='color: red; text-align: center;'> Total Anomalies Detected: {df['Anomaly'].sum()}</h3>", unsafe_allow_html=True)
