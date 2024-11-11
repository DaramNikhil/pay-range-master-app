import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def get_result_df():
    """Fetches the 'result_df_page3' from session state, handling potential absence."""
    if 'result_df_page3' in st.session_state:
        return st.session_state['result_df_page3']
    else:
        st.error("Data not found. Please go back to the previous page and ensure the data is properly uploaded.")
        return None

def save_dataframe(df):
    """Save the dataframe as a CSV or Excel file."""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save as CSV"):
            df.to_csv('data/pay_ranges.csv', index=False)
            st.success("Data saved as pay_ranges.csv")
    with col2:
        if st.button("Save as Excel"):
            df.to_excel('data/pay_ranges.xlsx', index=False)
            st.success("Data saved as pay_ranges.xlsx")

def plot_chart(df):
    """Generate and display a chart based on the DataFrame."""
    plt.figure(figsize=(10, 5))
    
    if 'New Range Mid' in df.columns:
        df_filtered = df[df['New Range Mid'] > 0]
        plt.bar(df_filtered['Grade'], df_filtered['New Range Mid'], color='skyblue')
        plt.xlabel('Grade')
        plt.ylabel('New Range Mid')
        plt.title('Pay Range Distribution by Grade')
        
        if not df_filtered.empty:
            st.pyplot(plt)
        else:
            st.warning("No non-zero 'New Range Mid' values to display.")
    else:
        st.warning("'New Range Mid' column not found or is not numeric.")

def show():
    """Displays Calibration - Page 4 and handles data fetching, ageing, and customization options."""
    st.title("Calibrating Your Pay Ranges")

    df = get_result_df()

    if df is not None:
        if 'New Range Mid' not in df.columns:
            df['New Range Mid'] = 0  # Initialize column if it doesn't exist

        # Allow users to apply a multiplier
        apply_multiplier = st.radio("Apply Multiplier?", ["No", "Yes"])

        if apply_multiplier == "Yes":
            multiplier = st.text_input("Enter the multiplier value:", key="multiplier_value")
            if st.button("Apply Multiplier"):
                try:
                    multiplier_val = float(multiplier)
                    df['Range Mid'] = pd.to_numeric(df['Range Mid'], errors='coerce')
                    df['Range Mid'].fillna(0, inplace=True)
                    df["New Range Mid"] = df["Range Mid"] * multiplier_val
                    st.session_state["multiplied_ranges"] = df.copy()
                    st.success(f"Applied multiplier: {multiplier_val}")
                except ValueError:
                    st.error("Please enter a valid numeric value for the multiplier.")

        # Use the multiplied ranges if available
        df_to_display = st.session_state.get("multiplied_ranges", df)

        # Editable DataFrame
        editable_df = st.data_editor(df_to_display, hide_index=True)

        # Save customized output
        if st.button("Save Changes"):
            st.session_state["multiplied_ranges"] = editable_df
            st.success("Changes saved!")

        # Save options for edited DataFrame
        save_dataframe(editable_df)

        # Generate and display the chart
        plot_chart(editable_df)

        # Display outliers and pay gap summary based on Page 1 selection
        approach = st.session_state.get('selected_approach', "Market Rate Calculations")
        if approach in ["Employee Pay Calculations", "Combination Strategy Calculations"]:
            st.write("### Outlier Summary and Pay Gap Analysis")
            if 'New Range Mid' in editable_df.columns:
                outliers = editable_df[editable_df['New Range Mid'] > editable_df['New Range Mid'].quantile(0.95)]
                st.write("#### Outliers")
                st.dataframe(outliers)
                st.write("#### Suggested Adjustments for Pay Gap")
                pay_gap_adjustments = editable_df[editable_df['New Range Mid'] < editable_df['New Range Mid'].quantile(0.25)]
                st.dataframe(pay_gap_adjustments)
            else:
                st.warning("'New Range Mid' column not available for pay gap analysis.")

