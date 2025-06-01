
# easy_dream_dashboard.py
# Streamlit UI for Easy Dream powered by ABS Engine

import streamlit as st
import pandas as pd
from abs_engine import ABSEngine

st.set_page_config(page_title="Easy Dream", layout="centered")
st.title("🌌 Easy Dream")
st.subheader("Statistically Smarter Lotto Forecasts")

# File upload for historical draw data
uploaded_file = st.file_uploader("Upload EuroMillions draw history (CSV)", type=["csv"])

# Initialize engine
abs_model = ABSEngine(main_range=50, star_range=12, draws=100000)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Draw history loaded.")
    abs_model.load_draw_history(df)

    st.markdown("---")
    st.subheader("🌀 Simulation Settings")
    draws = st.slider("Number of simulations", 1000, 200000, 50000, step=10000)
    abs_model.draws = draws

    if st.button("🎲 Run Simulation"):
        with st.spinner("Simulating draws using Bayesian priors..."):
            abs_model.simulate_draws()
            top_combos = abs_model.get_top_combinations(top_n=5)
            st.success("Simulation complete!")

            st.markdown("---")
            st.subheader("🔝 Top 5 Predicted Combinations")
            for i, ((main, star), count) in enumerate(top_combos, 1):
                st.markdown(f"**#{i}** → 🎱 {main} ✨ {star}")
                st.text(f"Simulated wins: {count:,} out of {draws:,}")

            st.markdown("---")
            st.caption("Built using Adaptive Bayesian Simulation (ABS)")

else:
    st.info("📥 Please upload your historical CSV data to begin.")
