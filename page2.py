import streamlit as st
import pandas as pd

def display_page2():
    # Page Title with color
    st.markdown("""
        <h1 style='color: #4A90E2;'>Data Upload</h1>
        """, unsafe_allow_html=True)
    st.markdown("""
        <h2 style='color: #4A90E2;'>Load Your Data</h2>
        """, unsafe_allow_html=True)

    # Retrieve the selected approach from session state
    selected_approach = st.session_state.get('selected_approach', 'Market Rate Calculations')
    st.markdown(f"<p style='color: #2C3E50; font-size: 18px;'>Approach: <b>{selected_approach}</b></p>", unsafe_allow_html=True)

    # Define the required and optional columns for each approach
    required_columns = {
        "Market Rate Calculations": ["Job", "Grade", "Target Pay"],
        "Employee Pay Calculations": ["Employee ID", "Grade", "Base Pay"],
        "Combination Strategy Calculations": ["Employee ID", "Grade", "Base Pay", "Target Pay"]
    }
    optional_columns = ["Gender", "Job Family"] if selected_approach in ["Employee Pay Calculations", "Combination Strategy Calculations"] else []
    expected_columns = required_columns[selected_approach] + optional_columns

    # Display expected columns for the user
    st.markdown(f"<p style='color: #2C3E50; font-size: 16px;'>Please upload your file with the following columns for <b>{selected_approach}</b>:</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #2C3E50;'>{', '.join(expected_columns)}</p>", unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=["xlsx", "csv"])

    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)

            # Check if the uploaded file has the required columns
            missing_columns = set(required_columns[selected_approach]) - set(df.columns)
            if missing_columns:
                st.error(f"The uploaded file is missing the following columns: {', '.join(missing_columns)}")
            else:
                st.success("File successfully uploaded and validated!")
                st.markdown(f"<p style='color: #2C3E50;'>Number of records uploaded: {len(df)}</p>", unsafe_allow_html=True)

                # Sort and display data preview
                df_sorted = df.sort_values(by='Grade').reset_index(drop=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<p style='color: #2C3E50; font-weight: bold;'>Highest Grade - Preview:</p>", unsafe_allow_html=True)
                    st.dataframe(df_sorted.head())
                with col2:
                    st.markdown("<p style='color: #2C3E50; font-weight: bold;'>Lowest Grade - Preview:</p>", unsafe_allow_html=True)
                    st.dataframe(df_sorted.tail())

                # Store dataframe in session state
                st.session_state.imported_data = df
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Navigation buttons with styling
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous", key="previous_button"):
            st.session_state.page = 'page1'
    with col2:
        if st.button("Next", key="next_button"):
            if 'imported_data' in st.session_state:
                st.session_state.page = 'page3'
            else:
                st.warning("Please upload a valid file before proceeding.")

    # Custom CSS for additional styling
    st.markdown("""
        <style>
            h1, h2 {
                text-align: left;
                font-weight: bold;
            }
            p {
                font-size: 16px;
                color: #2C3E50;
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
