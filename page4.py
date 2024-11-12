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

def plot_salary_distribution(df, chart_type="line"):
    """Generate and display a chart (line or box) of salary distribution."""
    plt.figure(figsize=(10, 5))
    
    if 'Range Mid' in df.columns and 'New Range Mid' in df.columns:
        if chart_type == "line":
            plt.plot(df['Grade'], df['Range Mid'], label='Original Range Mid', color='blue', linestyle='--')
            plt.plot(df['Grade'], df['New Range Mid'], label='Edited Range Mid', color='orange')
            plt.xlabel('Grade')
            plt.ylabel('Range Mid')
            plt.title('Original vs. Edited Pay Range Distribution')
            plt.legend()
        elif chart_type == "box":
            # Convert 'Range Mid' and 'New Range Mid' to numeric
            df['Range Mid'] = pd.to_numeric(df['Range Mid'], errors='coerce')
            df['New Range Mid'] = pd.to_numeric(df['New Range Mid'], errors='coerce')

            # Remove rows with NaN values in either of the columns
            df = df.dropna(subset=['Range Mid', 'New Range Mid'])

            # Check if the columns are numeric
            if pd.api.types.is_numeric_dtype(df['Range Mid']) and pd.api.types.is_numeric_dtype(df['New Range Mid']):
                plt.boxplot([df['Range Mid'], df['New Range Mid']], labels=['Original Range Mid', 'Edited Range Mid'])
            else:
                st.warning("The data contains non-numeric values. Please clean the data.")

        if not df.empty:
            st.pyplot(plt)
        else:
            st.warning("No data to display in chart.")
    else:
        st.warning("Required columns ('Range Mid' and 'New Range Mid') are not available in the DataFrame.")



def calculate_values(df):
    """Calculate the 'Range Mid' and apply adjustments based on 'Base Pay'."""
    # Check if 'Base Pay' exists in the DataFrame
    if 'Base Pay' in df.columns:
        df['Range Mid'] = df['Base Pay'] / 2  # Adjust this logic based on your requirements
    else:
        st.error("'Base Pay' column is missing!")
        return  # Exit the function if 'Base Pay' is missing
    
    # Continue with the rest of your logic
    st.write(df.head())  # Check the first few rows to ensure everything is correct



def show_page4():
    """Displays Calibration - Page 4 with editable table, aged values, and charting options."""
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

        # Recalculate values
        calculate_values(editable_df)

        # Save customized output
        if st.button("Save Changes"):
            st.session_state["multiplied_ranges"] = editable_df
            st.success("Changes saved!")

        # Save options for edited DataFrame
        save_dataframe(editable_df)

        # Choose chart type
        chart_type = st.selectbox("Select Chart Type", options=["line", "box"])

        # Generate and display the chart
        plot_salary_distribution(editable_df, chart_type=chart_type)

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



def show_page5():
    """Page 5 duplicate of Page 4 with same content."""
    # st.title("Calibrating Your Pay Ranges - Page 5")
    show_page4()  # Duplicate functionality from Page 4

# Uncomment the following line to display Page 4 or Page 5 in the app
show_page4()
show_page5()
