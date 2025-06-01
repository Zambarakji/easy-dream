import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from abs_engine import ABSEngine
from datetime import datetime

st.set_page_config(page_title="Easy Dream", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        footer { visibility: hidden; }
        .footer::after {
            content: 'Easy Dream • Invented by Remy Zambarakji • Powered by ABS';
            visibility: visible;
            display: block;
            position: relative;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: gray;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='color:#0074D9;'>🌌 Easy Dream</h1>
        <p style='font-size: 18px;'>Statistically Smarter Lotto Forecasts</p>
    </div>
""", unsafe_allow_html=True)

archive = []

with st.sidebar:
    st.header("📥 Upload Draw History")
    uploaded_file = st.file_uploader("Choose your EuroMillions CSV", type="csv")
    st.header("⚙️ Settings")
    draws = st.slider("Simulations", 1000, 200000, 50000, step=10000)
    view_mode = st.radio("View", ["Predictions", "Analytics"])
    run_button = st.button("🎲 Run Simulation")

abs_model = ABSEngine(main_range=50, star_range=12, draws=draws)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        abs_model.load_draw_history(df)
        st.success("✅ Data loaded successfully!")

        if run_button:
            with st.spinner("Running simulation..."):
                abs_model.simulate_draws()
                top_combos = abs_model.get_top_combinations(top_n=5)
                st.success("✅ Simulation complete!")

                if view_mode == "Predictions":
                    st.subheader("🎯 Top 5 Predictions")
                        for i, ((main, star), count) in enumerate(top_combos, 1):
                        main_clean = [int(x.item()) if hasattr(x, 'item') else int(x) for x in main]
                        star_clean = [int(x.item()) if hasattr(x, 'item') else int(x) for x in star]
                        st.markdown(f"**#{i}** → 🎱 {main_clean} ✨ {star_clean}")
                        st.text(f"Simulated wins: {count:,} out of {draws:,}")

                elif view_mode == "Analytics":
                    st.subheader("📊 Statistical Analysis")
                    all_main = [int(num) for combo in abs_model.results for num in combo[0]]
                    all_stars = [int(num) for combo in abs_model.results for num in combo[1]]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Main Numbers Frequency**")
                        fig1, ax1 = plt.subplots(figsize=(10, 6))
                        ax1.hist(all_main, bins=range(1, 52), color='skyblue', alpha=0.7)
                        st.pyplot(fig1)
                        plt.close(fig1)
                    with col2:
                        st.write("**Star Numbers Frequency**")
                        fig2, ax2 = plt.subplots(figsize=(10, 6))
                        ax2.hist(all_stars, bins=range(1, 14), color='gold', alpha=0.7)
                        st.pyplot(fig2)
                        plt.close(fig2)
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check your CSV format")
else:
    st.info("📂 Please upload your CSV file to begin analysis")

st.markdown("""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; background: white; border-radius: 10px;'>
        <p style='color: gray;'>Easy Dream • Powered by Advanced Bayesian Statistics</p>
    </div>
""", unsafe_allow_html=True)
