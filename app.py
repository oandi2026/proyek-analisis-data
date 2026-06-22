import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="USDA Multi-Commodity Dashboard", page_icon="🌾", layout="wide"
)

st.title("🌾 USDA Agricultural Production & Sales Analysis")
st.markdown("Interactive multi-commodity data analysis portal using USDA public datasets.")
st.markdown("---")

st.sidebar.header("🛠️ Dashboard Control Panel")
commodity_selected = st.sidebar.selectbox(
    "Select Commodity to Analyze:", ["Milk", "Honey", "Yogurt", "Eggs"]
)

commodity_mapping = {
    "Milk": {
        "file": "data/top_5_milk_producers.csv",
        "value_col": "total_milk",
        "title": "Milk Production Volume",
        "color": "#1f77b4",  # Biru
        "insight": "Based on the USDA analysis, Iowa (ANSI 19) leads total milk production, followed closely by Pennsylvania (ANSI 42).",
    },
    "Honey": {
        "file": "data/top_5_honey_producers.csv", 
        "value_col": "total_honey",  
        "title": "Honey Production Volume",
        "color": "#ffc107",  # Kuning Madu
        "insight": "Honey production shows high regional specialization, dominated heavily by North Dakota and South Dakota due to optimal foraging landscapes.",
    },
    "Yogurt": {
        "file": "data/top_5_yogurt_producers.csv",
        "value_col": "total_yogurt",
        "title": "Yogurt Production Volume",
        "color": "#e83e8c",  # Merah Muda/Pink Yogurt
        "insight": "Yogurt production is highly centralized near major urban supply chains, with New York leading significant manufacturing capabilities.",
    },
    "Eggs": {
        "file": "data/top_5_egg_producers.csv",
        "value_col": "total_eggs",
        "title": "Egg Production Volume",
        "color": "#fd7e14",  # Oranye Telur
        "insight": "Iowa holds a massive market lead in egg production, driven by large-scale commercial poultry operations and local feed availability.",
    },
}

current_config = commodity_mapping[commodity_selected]

try:
    
    df = pd.read_csv(current_config["file"])
    df.columns = df.columns.str.strip()

    val_col = current_config["value_col"]

    if val_col not in df.columns:
    
        val_col = df.columns[-1]

    df[val_col] = df[val_col].astype(str).str.replace(",", "").astype(float)

    df_sorted_desc = df.sort_values(by=val_col, ascending=False)
    top_state_ansi = df_sorted_desc.iloc[0]["State_ANSI"]
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
            if top_state_val > 1e9
            else f"{top_state_val:,.0f}",
        )
    with kpi3:
        st.metric(
            label=f"📈 Combined Top 5 {commodity_selected}",
            value=f"{total_production_all*1e-9:.1f}B"
            if total_production_all > 1e9
            else f"{total_production_all:,.0f}",
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🔍 {commodity_selected} Data Summary Table")
        st.dataframe(df_sorted_desc, use_container_width=True)

    with col2:
        st.subheader(f"📊 {current_config['title']}")

        df_sorted_asc = df.sort_values(by=val_col, ascending=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        plt.style.use("seaborn-v0_8-whitegrid")

        def format_axis(x, pos):
            if x >= 1e9:
                return f"{x*1e-9:.0f}B"
            elif x >= 1e6:
                return f"{x*1e-6:.0f}M"
            return f"{x:,.0f}"

        from matplotlib.ticker import FuncFormatter

        ax.xaxis.set_major_formatter(FuncFormatter(format_axis))

        y_labels = df_sorted_asc["State_ANSI"].astype(str)
        ax.barh(
            y_labels,
            df_sorted_asc[val_col],
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

        st.markdown("### 📈 Strategic Key Insight")
        st.write(current_config["insight"])

except Exception as e:
    st.error(f"Please ensure all your commodity CSV files are added in the data/ folder. Error details: {e}")
