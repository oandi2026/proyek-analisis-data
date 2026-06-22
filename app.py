import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

# Using columns for a clean dashboard layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📌 Project Overview")
    st.write(
        "This application analyzes U.S. agricultural production trends using public USDA datasets "
        "to provide supply chain insights and market segmentation."
    )

    st.subheader("🔍 Data Summary")
    # Reading the milk data file located in the data/ folder
    try:
        df = pd.read_csv("data/top_5_milk_producers.csv")
        df.columns = df.columns.str.strip()

        if "Value" in df.columns:
            df = df.rename(columns={"Value": "Total_Milk_Production"})
        if "State_Name" in df.columns:
            df = df.rename(columns={"State_Name": "State"})

        if "Total_Milk_Production" in df.columns:
            df["Total_Milk_Production"] = (
                df["Total_Milk_Production"]
                .astype(str)
                .str.replace(",", "")
                .astype(float)
            )

        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load data: {e}")

with col2:
    st.subheader("📊 Milk Production Visualization")

    if "df" in locals():
        # Sort data so the highest producer is at the top
        df = df.sort_values(by="Total_Milk_Production", ascending=True)

        # Build a safe, stable horizontal bar chart using Matplotlib directly
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Format millions/billions on the x-axis
        def format_billion(x, pos):
            return f"{x*1e-9:.0f}B"
        
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(format_billion))

        # Render bars safely
        bars = ax.barh(df["State"], df["Total_Milk_Production"], color="#1f77b4", edgecolor="none")
        
        # Grid layout
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        
        ax.set_title(
            "Top U.S. Milk Producing States (USDA Data)",
            fontsize=12,
            weight="bold",
        )
        
        plt.tight_layout()
        st.pyplot(fig)
