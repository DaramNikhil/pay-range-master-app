import streamlit as st

def display_page1():
    # Page title with left alignment
    st.markdown("""
        <h1 style='text-align: left; color: #4A90E2; margin-bottom: 20px;'>Approach</h1>
        <h2 style='text-align: left; color: #4A90E2;'>What's your approach?</h2>
        """, unsafe_allow_html=True)

    # Radio buttons for selecting an approach with left alignment
    st.markdown("<h3 style='text-align: left; color: #2C3E50;'>I will use:</h3>", unsafe_allow_html=True)
    selected_approach = st.radio(
        "",
        ("Market Rate Calculations", 
         "Employee Pay Calculations", 
         "Combination Strategy Calculations"),
        horizontal=False,
        key="approach_radio"
    )

    # Store the selected approach in session state
    st.session_state.selected_approach = selected_approach

    # Display content based on selected approach with left-aligned styled text
    if selected_approach == "Market Rate Calculations":
        st.markdown("<h4 style='text-align: left; color: #E67E22;'>You got a competitive edge!</h4>", unsafe_allow_html=True)
        st.markdown("""
            <p style='text-align: left; color: #34495E;'>
            This approach focuses on setting pay based on external market rates. It's ideal for attracting top talent 
            and ensuring your pay is competitive within the industry.
            </p>
        """, unsafe_allow_html=True)
    elif selected_approach == "Employee Pay Calculations":
        st.markdown("<h4 style='text-align: left; color: #27AE60;'>Yes, Fairness matters!</h4>", unsafe_allow_html=True)
        st.markdown("""
            <p style='text-align: left; color: #34495E;'>
            This approach centers on internal equity within your organization, ensuring fairness in compensation for employees 
            in similar roles with similar experience.
            </p>
        """, unsafe_allow_html=True)
    elif selected_approach == "Combination Strategy Calculations":
        st.markdown("<h4 style='text-align: left; color: #8E44AD;'>It's a win-win!</h4>", unsafe_allow_html=True)
        st.markdown("""
            <p style='text-align: left; color: #34495E;'>
            This strategy combines both market and employee pay calculations, balancing external competitiveness with internal fairness.
            </p>
        """, unsafe_allow_html=True)

    # Navigation buttons with left alignment
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Home", help="Go back to Home page"):
            st.session_state.page = 'home'
    with col2:
        if st.button("Next", help="Proceed to the next page"):
            st.session_state.page = 'page2'
            st.session_state.selected_approach = selected_approach  # Store the selected approach for later use

    # Additional styling for the page
    st.markdown("""
        <style>
            h1, h2, h3, h4, p {
                text-align: left;
                margin-top: 0;
            }
            .stButton > button {
                width: 100%;
                height: 40px;
                font-size: 16px;
                color: #FFF;
                background-color: #4e67f5;
                border: none;
                border-radius: 8px;
                transition: background-color 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #2E5B8A;
            }
            .stRadio label {
                color: #34495E;
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)
