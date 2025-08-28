import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import scipy.stats as stats
from io import BytesIO

# Set up the app
st.set_page_config(page_title="Fake Data Generator", layout="wide")
st.title("📊 Custom Fake Data Generator")

# Initialize Faker
fake = Faker()

# Sidebar for parameters
st.sidebar.header("Data Generation Parameters")

# Basic parameters
num_rows = st.sidebar.number_input("Number of Rows", min_value=1, max_value=100000, value=1000)
num_numeric_cols = st.sidebar.number_input("Number of Numeric Columns", min_value=0, max_value=20, value=3)
num_categorical_cols = st.sidebar.number_input("Number of Categorical Columns", min_value=0, max_value=20, value=2)

# Personal information options
st.sidebar.subheader("Personal Information Fields")
include_name = st.sidebar.checkbox("Name", value=True)
include_email = st.sidebar.checkbox("Email", value=True)
include_address = st.sidebar.checkbox("Address")
include_phone = st.sidebar.checkbox("Phone Number")
include_company = st.sidebar.checkbox("Company")
include_job = st.sidebar.checkbox("Job Title")
include_credit_card = st.sidebar.checkbox("Credit Card Info")

# Data quality parameters
st.sidebar.subheader("Data Quality Parameters")
missing_percentage = st.sidebar.slider("Missing Data Percentage", 0.0, 50.0, 5.0, step=0.5) / 100

# Correlation parameters
if num_numeric_cols > 1:
    st.sidebar.subheader("Correlation Settings")
    enable_correlation = st.sidebar.checkbox("Enable Correlation Between Numeric Variables", value=True)
    if enable_correlation:
        target_correlation = st.sidebar.slider("Target Correlation Strength", -1.0, 1.0, 0.7, step=0.1)
else:
    enable_correlation = False

# Distribution settings
st.sidebar.subheader("Distribution Settings")
distribution_options = ["Normal", "Uniform", "Exponential", "Lognormal"]
selected_distributions = []

for i in range(num_numeric_cols):
    dist = st.sidebar.selectbox(
        f"Distribution for Numeric Column {i+1}", 
        distribution_options, 
        key=f"dist_{i}"
    )
    selected_distributions.append(dist)

# Main content area
tab1, tab2, tab3 = st.tabs(["Generate Data", "Preview Data", "Export Data"])

with tab1:
    if st.button("Generate Data", type="primary"):
        data = {}
        
        # Generate personal information if selected
        if include_name:
            data['name'] = [fake.name() for _ in range(num_rows)]
        if include_email:
            data['email'] = [fake.email() for _ in range(num_rows)]
        if include_address:
            data['address'] = [fake.address() for _ in range(num_rows)]
        if include_phone:
            data['phone'] = [fake.phone_number() for _ in range(num_rows)]
        if include_company:
            data['company'] = [fake.company() for _ in range(num_rows)]
        if include_job:
            data['job'] = [fake.job() for _ in range(num_rows)]
        if include_credit_card:
            data['credit_card'] = [fake.credit_card_full() for _ in range(num_rows)]
        
        # Generate numeric columns with selected distributions
        numeric_data = np.zeros((num_rows, num_numeric_cols))
        
        for i, dist in enumerate(selected_distributions):
            if dist == "Normal":
                numeric_data[:, i] = np.random.normal(0, 1, num_rows)
            elif dist == "Uniform":
                numeric_data[:, i] = np.random.uniform(0, 1, num_rows)
            elif dist == "Exponential":
                numeric_data[:, i] = np.random.exponential(1, num_rows)
            elif dist == "Lognormal":
                numeric_data[:, i] = np.random.lognormal(0, 1, num_rows)
        
        # Apply correlation if enabled
        if enable_correlation and num_numeric_cols > 1:
            # Create a correlation matrix
            corr_matrix = np.eye(num_numeric_cols)
            for i in range(num_numeric_cols):
                for j in range(i+1, num_numeric_cols):
                    corr_matrix[i, j] = target_correlation
                    corr_matrix[j, i] = target_correlation
            
            # Apply Cholesky decomposition to induce correlation
            try:
                L = np.linalg.cholesky(corr_matrix)
                numeric_data = np.dot(numeric_data, L)
            except np.linalg.LinAlgError:
                st.warning("Could not apply correlation with the selected parameters. Generating uncorrelated data.")
        
        # Add numeric columns to data
        for i in range(num_numeric_cols):
            data[f'numeric_{i+1}'] = numeric_data[:, i]
        
        # Generate categorical columns
        categories = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(num_categorical_cols):
            data[f'category_{i+1}'] = np.random.choice(categories, num_rows)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Introduce missing values
        if missing_percentage > 0:
            mask = np.random.random(df.shape) < missing_percentage
            df = df.mask(mask)
        
        # Store the DataFrame in session state
        st.session_state.df = df
        st.success(f"Generated {num_rows} rows with {len(df.columns)} columns!")
        
        # Show basic statistics
        st.subheader("Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            missing_values = df.isnull().sum().sum()
            st.metric("Missing Values", missing_values)

with tab2:
    if 'df' in st.session_state:
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head(20))
        
        st.subheader("Column Information")
        for col in st.session_state.df.columns:
            col_missing = st.session_state.df[col].isnull().sum()
            st.write(f"**{col}**: {st.session_state.df[col].dtype} - {col_missing} missing values")
        
        # Show correlation matrix if we have numeric columns
        numeric_cols = st.session_state.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            st.subheader("Correlation Matrix")
            corr = st.session_state.df[numeric_cols].corr()
            st.dataframe(corr.style.background_gradient(cmap='coolwarm', vmin=-1, vmax=1))
    else:
        st.info("Generate some data first to see the preview!")

with tab3:
    if 'df' in st.session_state:
        st.subheader("Export Data")
        
        export_format = st.radio("Select Export Format", ["CSV", "Excel", "Stata (DTA)"])
        
        if export_format == "CSV":
            csv = st.session_state.df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="synthetic_data.csv",
                mime="text/csv"
            )
        elif export_format == "Excel":
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                st.session_state.df.to_excel(writer, index=False, sheet_name='Synthetic Data')
            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name="synthetic_data.xlsx",
                mime="application/vnd.ms-excel"
            )
        elif export_format == "Stata (DTA)":
            output = BytesIO()
            st.session_state.df.to_stata(output, write_index=False)
            st.download_button(
                label="Download Stata DTA",
                data=output.getvalue(),
                file_name="synthetic_data.dta",
                mime="application/octet-stream"
            )
    else:
        st.info("Generate some data first to export!")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "This app uses Faker to generate synthetic data. "
    "Adjust the parameters in the sidebar to customize your dataset."
)