# streamlit_app.py (Ultimate Clean Output Version)

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
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/8/88/Infinity_symbol.svg' width='80'>
        <h1 style='color:#0074D9;'>🌌 Easy Dream</h1>
        <p style='font-size: 18px;'>Statistically Smarter Lotto Forecasts — Powered by ABS</p>
    </div>
""", unsafe_allow_html=True)

archive = []

with st.sidebar:
    st.header("📥 Upload Draw History")
    uploaded_file = st.file_uploader("Choose your EuroMillions CSV", type="csv")
    st.markdown("""<hr>""", unsafe_allow_html=True)
    st.header("🎛️ Settings")
    draws = st.slider("Simulations", 1000, 200000, 50000, step=10000)
    view_option = st.radio("View Mode", ["Predictions", "Scientific View"])
    simulate_btn = st.button("🎲 Run Simulation")

abs_model = ABSEngine(main_range=50, star_range=12, draws=draws)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    abs_model.load_draw_history(df)
    st.success("✅ Data loaded.")

    if simulate_btn:
        with st.spinner("Simulating with Bayesian priors..."):
            abs_model.simulate_draws()
            top_combos = abs_model.get_top_combinations(top_n=5)
            st.success("✅ Simulation complete!")

            if view_option == "Predictions":
                st.subheader("🔝 Top 5 Predicted Combinations")
                for i, ((main, star), count) in enumerate(top_combos, 1):
                    main_clean = [int(x) for x in tuple(main)]
                    star_clean = [int(x) for x in tuple(star)]
                    archive.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), main_clean, star_clean, count))
                    st.markdown(f"**#{i}** → 🎱 {main_clean} ✨ {star_clean}")
                    st.text(f"Simulated wins: {count:,} out of {draws:,}")

                all_main = [num for combo in abs_model.results for num in combo[0]]
                all_stars = [num for combo in abs_model.results for num in combo[1]]

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🎯 Ball Frequency")
                    fig1, ax1 = plt.subplots()
                    ax1.hist(all_main, bins=range(1, 52), color='skyblue', edgecolor='black')
                    ax1.set_title("Main Ball Distribution")
                    st.pyplot(fig1)

                with col2:
                    st.subheader("✨ Star Frequency")
                    fig2, ax2 = plt.subplots()
                    ax2.hist(all_stars, bins=range(1, 14), color='gold', edgecolor='black')
                    ax2.set_title("Star Ball Distribution")
                    st.pyplot(fig2)

            elif view_option == "Scientific View":
                st.subheader("🔬 Scientific View")
                st.markdown("""
                    This dashboard uses **Bayesian inference** to adjust beliefs about ball likelihoods 
                    based on draw history, and runs **Monte Carlo simulations** to find frequent patterns.  

                    - **Bayesian Prior**: Based on past frequencies, adjusted with smoothing.  
                    - **Simulation**: 100,000+ virtual draws using those priors.  
                    - **Outcome**: Ranking of combinations most likely to reappear.  

                    This method embraces **real-world entropy**, seeking subtle biases in draw machines.  
                    It does not claim certainty, but delivers _statistical insight._
                """)
else:
    st.info("📂 Please upload your CSV draw history.")

st.markdown("""<div class='footer'></div>""", unsafe_allow_html=True)
