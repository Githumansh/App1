import streamlit as st
import pandas as st
import matplotlib.pyplot as plt
import numpy as np

# Set up the app title and layout
st.set_page_config(page_title="Data Forecasting Analyzer", layout="centered")
st.title("📊 Excel Data Analyzer & Forecasting Evaluator")
st.write("Upload an Excel file to analyze numerical columns, view histograms, and check forecasting readiness.")

# File uploader widget
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
        
        # Display raw data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head())

        # Filter for numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if not numerical_cols:
            st.warning("No numerical columns found in this Excel sheet.")
        else:
            st.subheader("📈 Statistical Analysis & Visualization")
            
            for col in numerical_cols:
                # Drop NaN values for accurate calculation
                col_data = df[col].dropna()
                
                if col_data.empty:
                    continue

                st.markdown(f"---")
                st.markdown(f"### **Column: {col}**")

                # Calculate metrics
                mean_val = col_data.mean()
                median_val = col_data.median()
                std_val = col_data.std()

                # Display metrics side-by-side
                col1, col2 = st.columns(2)
                col1.metric("Mean", f"{mean_val:.4f}")
                col2.metric("Median", f"{median_val:.4f}")

                # Create and display Histogram
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.hist(col_data, bins='auto', color='#4F46E5', edgecolor='black', alpha=0.7)
                ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean ({mean_val:.2f})')
                ax.axvline(median_val, color='green', linestyle='dotted', linewidth=2, label=f'Median ({median_val:.2f})')
                ax.set_title(f"Histogram of {col}")
                ax.set_xlabel("Value")
                ax.set_ylabel("Frequency")
                ax.legend()
                st.pyplot(fig)
                plt.close()

                # Evaluation logic: Check if mean and median are close (within 10% of standard deviation)
                # This accounts for the scale of the data
                threshold = 0.1 * std_val if std_val > 0 else 0.01
                
                if abs(mean_val - median_val) <= threshold:
                    st.success(f"✅ **Verdict:** The data in **{col}** is relatively symmetric (Mean and Median are close). **This data can be used for forecasting.**")
                else:
                    st.info(f"⚠️ **Verdict:** The data in **{col}** is skewed (Mean and Median differ significantly). Forecasting models may require transformation first.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
