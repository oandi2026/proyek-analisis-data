import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Page Configuration (Clean & Wide Layout)
st.set_page_config(page_title="USDA Analysis", page_icon="📊", layout="wide")

st.title("🌾 USDA Sales and Production Analysis")
st.markdown("---")

try:
    # 2. Load and Clean Processed Milk Data
    df = pd.read_csv("data/top_5_milk_producers.csv")
    df.columns = df.columns.str.strip()

    if "total_milk" in df.columns:
        df["total_milk"] = (
            df["total_milk"]
            .astype(str)
            .str.replace(",", "")
            .astype(float)
        )

    # ========================================================
    # 🏆 DYNAMIC KPI CARDS SECTION (Kembali Ditampilkan)
    # ========================================================
    df_sorted_desc = df.sort_values(by="total_milk", ascending=False)
    top_state_ansi = df_sorted_desc.iloc[0]["State_ANSI"]
    top_state_val = df_sorted_desc.iloc[0]["total_milk"]
    total_production_all = df["total_milk"].sum()

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="🏆 Market Leader (ANSI)", value=str(top_state_ansi))
    with kpi2:
        st.metric(label="🚀 Highest Production Volume", value=f"{top_state_val*1e-9:.1f}B")
    with kpi3:
        st.metric(label="📈 Combined Top 5 Production", value=f"{total_production_all*1e-9:.1f}B")
        
    st.markdown("---")

    # 3. Split Layout Grid for Table and Visualization Chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Data Summary")
        st.dataframe(df_sorted_desc, use_container_width=True)
            
    with col2:
        st.subheader("📊 Milk Production Visualization")

        if "total_milk" in df.columns and "State_ANSI" in df.columns:
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

except Exception as e:
    st.error(f"Failed to load dashboard components: {e}")
