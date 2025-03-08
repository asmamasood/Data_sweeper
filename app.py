import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Application Setup
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background-color:#B0E0E6;
        }
        .main-title { text-align: center; font-size: 36px; color: #4A90E2; text-decoration: underline; }
        .subheader { font-size: 22px; color: #333; margin-top: 20px; }
        .stButton > button { width: 100%; }
            .custom-text { font-size: 20px; color: #00008B; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown("<h1 class='main-title'>🔄 Info Scrubber 🧹 </h1>", unsafe_allow_html=True)
st.write("Optimize and visualize your CSV and Excel files with seamless conversion and cleaning.")

# File Upload
upload_files = st.file_uploader("📂 Upload your file (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read File
        if file_ext == ".csv":
            df = pd.read_csv(file, encoding='ISO-8859-1')
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ {file_ext} : This File is not supported")
            continue

        # File Info
        st.subheader(f"📄 File: {file.name}")
        st.write(f"**Size:** {file.size/1024:.2f} KB")
        
        # Preview Data
        st.subheader("🔎 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Scrubbing")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🚮 Delete Duplicates for {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Delete!")

            with col2:
                if st.button(f"📝 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled!")
        
        # Column Selection
        st.subheader("🎯 Select Columns")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        # File Conversion Options
        st.subheader("🔄 Convert File Format")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")
