import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="USDA Multi-Commodity Dashboard", page_icon="🌾", layout="wide"
)

st.title("🌾 USDA Agricultural Production & Sales Analysis")
st.markdown("Interactive multi-commodity data analysis portal using USDA public datasets.")
st.markdown("---")

# ========================================================
# 2. INTERACTIVE SIDEBAR CONTROL PANEL
# ========================================================
st.sidebar.header("🛠️ Dashboard Control Panel")
commodity_selected = st.sidebar.selectbox(
    "Select Commodity to Analyze:", ["Milk", "Honey", "Cheese", "Coffee", "Eggs", "Yogurt"]
)

# FIXED CONFIGURATION: Mapped directly to your actual local file names from the image!
commodity_mapping = {
    "Milk": {
        "file": "data/top_5_milk_producers.csv",
        "value_col": "total_milk",
        "title": "Top 5 Milk Production Volume",
        "color": "#1f77b4",  # Blue
        "insight": "Based on the USDA analysis, Iowa (ANSI 19) leads total milk production, followed closely by Pennsylvania (ANSI 42).",
    },
    "Honey": {
        "file": "data/honey_production.csv",
        "value_col": "Value",
        "title": "Total Honey Production Volume",
        "color": "#ffc107",  # Honey Yellow
        "insight": "Honey production shows high regional specialization, dominated heavily by North Dakota and South Dakota due to optimal foraging landscapes.",
    },
    "Cheese": {
        "file": "data/cheese_production.csv",
        "value_col": "Value",
        "title": "Total Cheese Production Volume",
        "color": "#fd7e14",  # Cheese Orange/Yellow
        "insight": "Cheese manufacturing tracks closely with milk availability, showing heavy industrial presence across leading dairy states.",
    },
    "Coffee": {
        "file": "data/coffee_production.csv",
        "value_col": "Value",
        "title": "Total Coffee Production Volume",
        "color": "#795548",  # Coffee Brown
        "insight": "Coffee data reflects very unique tropical production clusters, isolated to specific geographical micro-climates.",
    },
    "Eggs": {
        "file": "data/egg_production.csv",
        "value_col": "Value",
        "title": "Total Egg Production Volume",
        "color": "#ff9800",  # Egg Orange
        "insight": "Iowa holds a massive market lead in egg production, driven by large-scale commercial poultry operations and local feed availability.",
    },
    "Yogurt": {
        "file": "data/yogurt_production.csv",
        "value_col": "Value",
        "title": "Total Yogurt Production Volume",
        "color": "#e83e8c",  # Yogurt Pink
        "insight": "Yogurt production is highly centralized near major urban supply chains, with New York leading significant manufacturing capabilities.",
    },
}

current_config = commodity_mapping[commodity_selected]

try:
    # 3. Dynamic Data Loading & Cleaning
    df = pd.read_csv(current_config["file"])
    df.columns = df.columns.str.strip()

    # Dynamic Column Fallback Safety Layer
    val_col = current_config["value_col"]
    if val_col not in df.columns:
        if "Value" in df.columns:
            val_col = "Value"
        elif "total_milk" in df.columns:
            val_col = "total_milk"
        else:
            val_col = df.columns[-1]  # Falls back to the last numeric column automatically

    # Standardize string numeric entries into clean floats safely
    df[val_col] = df[val_col].astype(str).str.replace(",", "").astype(float)

    # ========================================================
    # 4. DYNAMIC HIGH-LEVEL KPI CARDS
    # ========================================================
    df_sorted_desc = df.sort_values(by=val_col, ascending=False)
    
    # Secure fallback values if the dataset contains less rows or columns than expected
    top_state_ansi = df_sorted_desc.iloc[0]["State_ANSI"] if "State_ANSI" in df.columns else "N/A"
    top_state_val = df_sorted_desc.iloc[0][val_col]
    total_production_all = df[val_col].sum()

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(
            label=f"🏆 Top {commodity_selected} Producer (ANSI)",
            value=str(top_state_ansi),
        )
    with kpi2:
        st.metric(
            label="🚀 Highest Volume Registered",
            value=f"{top_state_val*1e-9:.1f}B"
            if top_state_val >= 1e9
            else f"{top_state_val:,.0f}",
        )
    with kpi3:
        st.metric(
            label=f"📈 Aggregated Total Production",
            value=f"{total_production_all*1e-9:.1f}B"
            if total_production_all >= 1e9
            else f"{total_production_all:,.0f}",
        )

    st.markdown("---")

    # ========================================================
    # 5. SPLIT GRID LAYOUT: DATA SUMMARY TABLE & VISUAL CHART
    # ========================================================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🔍 {commodity_selected} Data Summary Table")
        # Restrict viewport to top 20 rows if the files are too massive for presentation
        st.dataframe(df_sorted_desc.head(20), use_container_width=True)

    with col2:
        st.subheader(f"📊 {current_config['title']}")

        # Filter and limit to top 5 for a clean chart representation
        df_top5_asc = df_sorted_desc.head(5).sort_values(by=val_col, ascending=True)

        if not df_top5_asc.empty and "State_ANSI" in df.columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Axis values abbreviations helper function
            def format_axis(x, pos):
                if x >= 1e9:
                    return f"{x*1e-9:.0f}B"
                elif x >= 1e6:
                    return f"{x*1e-6:.0f}M"
                return f"{x:,.0f}"

            from matplotlib.ticker import FuncFormatter
            ax.xaxis.set_major_formatter(FuncFormatter(format_axis))

            # Render Matplotlib custom-colored horizontal bars (Crash-proof syntax)
            y_labels = df_top5_asc["State_ANSI"].astype(str)
            ax.barh(
                y_labels,
                df_top5_asc[val_col],
                color=current_config["color"],
                edgecolor="none",
            )

            ax.grid(axis="x", linestyle="--", alpha=0.7)
            ax.set_axisbelow(True)

            ax.set_title(
                f"Top 5 States - {commodity_selected} Analysis (USDA Data)",
                fontsize=12,
                weight="bold",
            )

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("State_ANSI labels missing or empty dataset. Unable to parse graphical bars.")

        # ========================================================
        # 6. STRATEGIC BUSINESS INSIGHTS
        # ========================================================
        st.markdown("### 📈 Strategic Key Insight")
        st.write(current_config["insight"])

except Exception as e:
    st.error(
        f"Error rendering dashboard. Please check that files match your 'data/' folder names "
        f"exactly. Error Details: {e}"
    )
