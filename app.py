import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Page Configuration (Clean & Simple Layout)
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

# Split dashboard layout cleanly into 2 columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 Project Overview")
    st.write(
        "This application analyzes U.S. agricultural production trends using public USDA datasets "
        "to provide supply chain insights and market segmentation."
    )

    st.subheader("🔍 Data Summary")
    
    try:
        # Load only the clean, processed top 5 milk dataset
        df = pd.read_csv("data/top_5_milk_producers.csv")
        df.columns = df.columns.str.strip()

        # Ensure the total_milk numbers are parsed correctly as decimals
        if "total_milk" in df.columns:
            df["total_milk"] = (
                df["total_milk"]
                .astype(str)
                .str.replace(",", "")
                .astype(float)
            )

        # Show the clean dataframe summary table directly
        st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"Failed to load data: {e}")

with col2:
    st.subheader("📊 Milk Production Visualization")

    if "df" in locals() and "total_milk" in df.columns and "State_ANSI" in df.columns:
        # Sort data ascending for a clean bottom-to-top layout
        df_sorted_asc = df.sort_values(by="total_milk", ascending=True)

        # Build a highly stable horizontal bar chart using pure Matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Format millions/billions axis safely (e.g., 457B)
        def format_billion(x, pos):
            return f"{x*1e-9:.0f}B"
        
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(format_billion))

        # Render the custom colored horizontal bars
        y_labels = df_sorted_asc["State_ANSI"].astype(str)
        ax.barh(y_labels, df_sorted_asc["total_milk"], color="#1f77b4", edgecolor="none")
        
        # Grid line configurations
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)
        
        ax.set_title(
            "Top 5 U.S. Milk Producing States by ANSI Code (USDA Data)",
            fontsize=12,
            weight="bold",
        )
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Clean text strategic business insight
        st.markdown("### 📈 Key Insight")
        st.write("Based on the USDA analysis, Iowa (ANSI 19) leads total milk production, followed closely by Pennsylvania (ANSI 42).")
