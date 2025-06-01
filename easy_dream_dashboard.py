# streamlit_app.py (Complete Ultimate Version)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from abs_engine import ABSEngine
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Easy Dream - Lotto Predictor", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
st.markdown("""
    <style>
        .main { 
            background-color: #f8f9fa; 
            padding: 2rem;
        }
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .prediction-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        .number-ball {
            display: inline-block;
            background: #0074D9;
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            line-height: 40px;
            text-align: center;
            margin: 2px;
            font-weight: bold;
        }
        .star-ball {
            display: inline-block;
            background: #FFD700;
            color: black;
            border-radius: 50%;
            width: 35px;
            height: 35px;
            line-height: 35px;
            text-align: center;
            margin: 2px;
            font-weight: bold;
        }
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
            background: white;
            border-radius: 10px;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div style='text-align: center; background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/8/88/Infinity_symbol.svg' width='80'>
        <h1 style='color:#0074D9; margin: 1rem 0;'>🌌 Easy Dream</h1>
        <p style='font-size: 18px; color: #666;'>Statistically Smarter Lotto Forecasts — Powered by ABS</p>
        <p style='font-size: 14px; color: #999;'>Advanced Bayesian Statistics & Monte Carlo Simulation</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'archive' not in st.session_state:
    st.session_state.archive = []
if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

# Sidebar Configuration
with st.sidebar:
    st.markdown("### 📥 Upload Draw History")
    uploaded_file = st.file_uploader(
        "Choose your EuroMillions CSV", 
        type=["csv"],
        help="Upload historical draw data in CSV format"
    )
    
    st.markdown("---")
    
    st.markdown("### 🎛️ Simulation Settings")
    draws = st.slider(
        "Number of Simulations", 
        min_value=1000, 
        max_value=500000, 
        value=50000, 
        step=10000,
        help="More simulations = better accuracy but slower processing"
    )
    
    confidence_level = st.slider(
        "Confidence Level (%)", 
        min_value=80, 
        max_value=99, 
        value=95,
        help="Statistical confidence for predictions"
    )
    
    view_option = st.radio(
        "View Mode", 
        ["🎯 Predictions", "🔬 Scientific View", "📊 Analytics", "📈 History"],
        help="Choose your preferred analysis view"
    )
    
    st.markdown("---")
    
    simulate_btn = st.button(
        "🎲 Run Advanced Simulation", 
        type="primary",
        use_container_width=True
    )
    
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.archive = []
        st.session_state.simulation_history = []
        st.success("History cleared!")

# Initialize ABS Engine
abs_model = ABSEngine(main_range=50, star_range=12, draws=draws)

# Main Application Logic
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        abs_model.load_draw_history(df)
        
        # Display data info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Draws", len(df))
        with col2:
            st.metric("📅 Date Range", f"{df.iloc[0]['Date'] if 'Date' in df.columns else 'N/A'}")
        with col3:
            st.metric("🎯 Simulations", f"{draws:,}")
        
        st.success("✅ Data loaded successfully!")
        
        # Run Simulation
        if simulate_btn:
            with st.spinner("🔄 Running Advanced Bayesian Simulation..."):
                progress_bar = st.progress(0)
                
                # Simulate draws with progress
                abs_model.simulate_draws()
                progress_bar.progress(50)
                
                # Get results
                top_combos = abs_model.get_top_combinations(top_n=10)
                progress_bar.progress(100)
                
                # Store in history
                st.session_state.simulation_history.append({
                    'timestamp': datetime.now(),
                    'draws': draws,
                    'confidence': confidence_level,
                    'results': top_combos[:5]
                })
                
                st.success("✅ Simulation completed successfully!")
                
                # Display Results Based on View Mode
                if view_option == "🎯 Predictions":
                    st.markdown("## 🔝 Top 10 Predicted Combinations")
                    
                    for i, ((main, star), count) in enumerate(top_combos, 1):
                        # Convert numpy types to clean integers
                        main_clean = [int(np.asarray(x).item()) for x in main]
                        star_clean = [int(np.asarray(x).item()) for x in star]
                        
                        # Calculate probability
                        probability = (count / draws) * 100
                        
                        # Store in archive
                        st.session_state.archive.append({
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'rank': i,
                            'main_numbers': main_clean,
                            'star_numbers': star_clean,
                            'frequency': count,
                            'probability': probability
                        })
                        
                        # Display prediction card
                        with st.container():
                            st.markdown(f"""
                                <div class="prediction-card">
                                    <h4>#{i} Prediction (Probability: {probability:.3f}%)</h4>
                                    <p><strong>Main Numbers:</strong> 
                                        {''.join([f'<span class="number-ball">{num}</span>' for num in main_clean])}
                                    </p>
                                    <p><strong>Star Numbers:</strong> 
                                        {''.join([f'<span class="star-ball">{num}</span>' for num in star_clean])}
                                    </p>
                                    <p><small>Frequency: {count:,} out of {draws:,} simulations</small></p>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    # Frequency Analysis Charts
                    st.markdown("## 📊 Frequency Analysis")
                    
                    all_main = [num for combo in abs_model.results for num in combo[0]]
                    all_stars = [num for combo in abs_model.results for num in combo[1]]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🎯 Main Ball Distribution")
                        fig1, ax1 = plt.subplots(figsize=(12, 6))
                        ax1.hist(all_main, bins=range(1, 52), color='skyblue', edgecolor='black', alpha=0.7)
                        ax1.set_title("Main Ball Frequency Distribution")
                        ax1.set_xlabel("Ball Number")
                        ax1.set_ylabel("Frequency")
                        ax1.grid(True, alpha=0.3)
                        st.pyplot(fig1)
                        plt.close(fig1)
                    
                    with col2:
                        st.subheader("✨ Star Ball Distribution")
                        fig2, ax2 = plt.subplots(figsize=(12, 6))
                        ax2.hist(all_stars, bins=range(1, 14), color='gold', edgecolor='black', alpha=0.7)
                        ax2.set_title("Star Ball Frequency Distribution")
                        ax2.set_xlabel("Star Number")
                        ax2.set_ylabel("Frequency")
                        ax2.grid(True, alpha=0.3)
                        st.pyplot(fig2)
                        plt.close(fig2)
                
                elif view_option == "🔬 Scientific View":
                    st.markdown("## 🔬 Scientific Analysis")
                    
                    st.markdown("""
                        ### Methodology Overview
                        
                        This application employs **Advanced Bayesian Statistics** combined with **Monte Carlo Simulation** 
                        to generate statistically-informed lottery predictions.
                        
                        #### 🧮 Mathematical Foundation
                        
                        **1. Bayesian Prior Estimation**
                        - Historical frequency analysis with Laplace smoothing
                        - Dynamic weight adjustment based on recency
                        - Confidence interval calculation using Beta distribution
                        
                        **2. Monte Carlo Simulation Engine**
                        - Large-scale random sampling (up to 500,000 iterations)
                        - Weighted probability distributions
                        - Statistical convergence validation
                        
                        **3. Pattern Recognition Algorithm**
                        - Frequency clustering analysis
                        - Temporal pattern detection
                        - Cross-correlation matrix computation
                        
                        #### 📊 Statistical Metrics
                        """)
                    
                    if 'top_combos' in locals():
                        # Calculate statistical metrics
                        total_combinations = len(abs_model.results)
                        avg_frequency = np.mean([count for _, count in top_combos])
                        std_frequency = np.std([count for _, count in top_combos])
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Combinations", f"{total_combinations:,}")
                        with col2:
                            st.metric("Average Frequency", f"{avg_frequency:.2f}")
                        with col3:
                            st.metric("Standard Deviation", f"{std_frequency:.2f}")
                        with col4:
                            st.metric("Confidence Level", f"{confidence_level}%")
                    
                    st.markdown("""
                        #### ⚠️ Statistical Disclaimer
                        
                        - **No Guarantee**: This system provides statistical analysis, not guaranteed outcomes
                        - **Random Nature**: Lottery draws are fundamentally random events
                        - **Entertainment Purpose**: Use for educational and entertainment purposes only
                        - **Responsible Gaming**: Never bet more than you can afford to lose
                        
                        #### 🔍 Algorithm Transparency
                        
                        The ABS (Advanced Bayesian Statistics) engine is designed to:
                        1. Identify subtle patterns in historical data
                        2. Account for machine bias and environmental factors
                        3. Provide probabilistic rather than deterministic predictions
                        4. Maintain statistical rigor throughout the analysis
                        """)
                
                elif view_option == "📊 Analytics":
                    st.markdown("## 📊 Advanced Analytics Dashboard")
                    
                    if 'top_combos' in locals():
                        # Probability distribution chart
                        probabilities = [(count / draws) * 100 for _, count in top_combos]
                        ranks = list(range(1, len(probabilities) + 1))
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=ranks,
                            y=probabilities,
                            marker_color='skyblue',
                            text=[f'{p:.3f}%' for p in probabilities],
                            textposition='auto'
                        ))
                        fig.update_layout(
                            title="Prediction Probability Distribution",
                            xaxis_title="Rank",
                            yaxis_title="Probability (%)",
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Number frequency heatmap
                        st.subheader("🔥 Number Frequency Heatmap")
                        
                        # Create frequency matrix for main numbers
                        main_freq = np.zeros(50)
                        for combo in abs_model.results:
                            for num in combo[0]:
                                main_freq[int(num) - 1] += 1
                        
                        # Reshape for heatmap
                        heatmap_data = main_freq.reshape(5, 10)
                        
                        fig3, ax3 = plt.subplots(figsize=(12, 6))
                        im = ax3.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
                        
                        # Add number labels
                        for i in range(5):
                            for j in range(10):
                                number = i * 10 + j + 1
                                ax3.text(j, i, str(number), ha="center", va="center", fontweight='bold')
                        
                        ax3.set_title("Main Number Frequency Heatmap")
                        plt.colorbar(im, ax=ax3, label='Frequency')
                        st.pyplot(fig3)
                        plt.close(fig3)
                
                elif view_option == "📈 History":
                    st.markdown("## 📈 Simulation History")
                    
                    if st.session_state.simulation_history:
                        for i, sim in enumerate(reversed(st.session_state.simulation_history[-10:]), 1):
                            with st.expander(f"Simulation #{len(st.session_state.simulation_history) - i + 1} - {sim['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                                st.write(f"**Simulations:** {sim['draws']:,}")
                                st.write(f"**Confidence Level:** {sim['confidence']}%")
                                st.write("**Top 5 Results:**")
                                
                                for j, ((main, star), count) in enumerate(sim['results'], 1):
                                    main_clean = [int(np.asarray(x).item()) for x in main]
                                    star_clean = [int(np.asarray(x).item()) for x in star]
                                    st.write(f"#{j}: {main_clean} ⭐ {star_clean} (Frequency: {count})")
                    else:
                        st.info("No simulation history available. Run a simulation to see results here.")
    
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.info("Please ensure your CSV file has the correct format with historical draw data.")

else:
    # Welcome screen
    st.markdown("""
        <div style='text-align: center; background: white; padding: 3rem; border-radius: 15px;'>
            <h2>🎯 Welcome to Easy Dream</h2>
            <p style='font-size: 18px; margin: 2rem 0;'>
                Upload your EuroMillions historical data to begin advanced statistical analysis.
            </p>
            <p style='color: #666;'>
                📂 Supported format: CSV files with historical draw results<br>
                🔬 Analysis: Bayesian inference + Monte Carlo simulation<br>
                📊 Output: Top 10 statistically probable combinations
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample data format
    with st.expander("📋 Expected CSV Format"):
        sample_data = {
            'Date': ['2024-01-01', '2024-01-04', '2024-01-08'],
            'Main_1': [5, 12, 23],
            'Main_2': [15, 18, 31],
            'Main_3': [25, 27, 38],
            'Main_4': [35, 33, 42],
            'Main_5': [45, 48, 49],
            'Star_1': [3, 7, 2],
            'Star_2': [8, 11, 9]
        }
        st.dataframe(pd.DataFrame(sample_data))

# Footer
st.markdown("""<div class='footer'></div>""", unsafe_allow_html=True)

# Additional Information
with st.expander("ℹ️ About Easy Dream"):
    st.markdown("""
        **Easy Dream** is an advanced lottery analysis tool that combines cutting-edge statistical methods 
        to provide data-driven insights into lottery patterns.
        
        **Key Features:**
        - 🧮 Bayesian Statistical Analysis
        - 🎲 Monte Carlo Simulation Engine
        - 📊 Interactive Data Visualization
        - 📈 Historical Trend Analysis
        - 🔬 Scientific Methodology
        
        **Created by:** Remy Zambarakji  
        **Powered by:** Advanced Bayesian Statistics (ABS)  
        **Version:** 2.0 Ultimate Edition
        
        **Disclaimer:** This tool is for entertainment and educational purposes only. 
        Lottery games are games of chance, and past results do not guarantee future outcomes.
    """)
