# page3.py
import streamlit as st
import pandas as pd
import market_rates_calculations
import employee_pay_calculations
import combination_strategy_calculations

# Function to calculate based on selected approach
def perform_calculation(selected_approach, df):
    if selected_approach == "Market Rate Calculations":
        result_df = market_rates_calculations.calculate(df)
    elif selected_approach == "Employee Pay Calculations":
        result_df = employee_pay_calculations.analyze_salary_distribution(df)
    elif selected_approach == "Combination Strategy Calculations":
        result_df = combination_strategy_calculations.calculate(df)
    else:
        result_df = pd.DataFrame()  # Handle unsupported options gracefully
        st.warning("Unsupported calculation option selected.")
    return result_df

# Page 3: Perform calculations and store result_df in session state
def show():
    # Page title with color and alignment
    st.markdown("""
        <h1 style='color: #4A90E2; text-align: left;'>Pay Ranges</h1>
        """, unsafe_allow_html=True)

    # Retrieve session state variables
    selected_approach = st.session_state.get("selected_approach", None)
    df = st.session_state.get("imported_data", None)

    # Check if data and approach are available
    if df is not None and selected_approach:
        # Information about the selected approach
        st.markdown(f"""
            <p style='color: #2C3E50; font-size: 18px;'>
            Building pay ranges based on <b>{selected_approach}</b> approach.
            </p>
            """, unsafe_allow_html=True)

        # Perform calculations based on the selected approach
        result_df = perform_calculation(selected_approach, df)

        # Display result with custom styling
        st.markdown("""
            <p style='color: #2C3E50; font-size: 16px;'>
            Here are your calculated pay ranges. You can use them as is or apply additional adjustments.
            </p>
            """, unsafe_allow_html=True)
        
        # DataFrame display with improved styling
        st.dataframe(
            result_df.reset_index(drop=True),
            width=800,
            height=400
        )

        # Store result_df in session state for future pages
        st.session_state.result_df_page3 = result_df

    else:
        st.error("No data found or option not selected. Please upload data on the previous page.")

    # Navigation buttons with alignment and styling
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous", help="Go back to the previous page"):
            st.session_state.page = 'page2'
            st.experimental_rerun()  # Reloads the page to update session state
    with col2:
        if st.button("Next", help="Proceed to the next page"):
            if 'result_df_page3' in st.session_state:
                st.session_state.page = 'page4'
            else:
                st.warning("Please complete the calculations before proceeding.")

    # Additional CSS for styling
    st.markdown("""
        <style>
            h1 {
                font-size: 28px;
                font-weight: bold;
            }
            p {
                font-size: 16px;
                margin-bottom: 0;
            }
            .stButton > button {
                width: 100%;
                height: 40px;
                font-size: 16px;
                color: white;
                background-color: #4A90E2;
                border: none;
                border-radius: 8px;
                transition: background-color 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #357ABD;
            }
        </style>
    """, unsafe_allow_html=True)
