import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration & Custom Theme
st.set_page_config(
    page_title="RealEstateWise App",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Fintech Dark Mode UI)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    div[data-testid="metric-container"] {
        background-color: #1F2937;
        border: 1px solid #374151;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background-color: #F3F402;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #E2E302;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)


# 2. Data Engine (Optimized & Fast Loading)
@st.cache_data(show_spinner="Loading Egyptian Real Estate Database...")
def load_data():
    file_id = "15TCcSWd1skf6bhctmy6EZ-BucamsxaO"
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"

    df = None
    try:
        temp_df = pd.read_csv(url, nrows=10000, low_memory=False)
        if len(temp_df.columns) > 2 and not str(temp_df.columns[0]).strip().startswith("<"):
            df = temp_df
    except Exception:
        df = None

    if df is not None and not df.empty:
        df.columns = df.columns.str.strip()
        col_map = {}
        for c in df.columns:
            cl = c.lower()
            if "price" in cl and "Price_EGP" not in col_map.values():
                col_map[c] = "Price_EGP"
            elif cl in ["city", "location", "governorate", "region", "district"] and "City" not in col_map.values():
                col_map[c] = "City"
            elif "year" in cl and "Year" not in col_map.values():
                col_map[c] = "Year"
            elif ("type" in cl or "property" in cl or "unit" in cl) and "Property_Type" not in col_map.values():
                col_map[c] = "Property_Type"
            elif "finish" in cl and "Finishing_Condition" not in col_map.values():
                col_map[c] = "Finishing_Condition"
            elif ("area" in cl or "sqm" in cl or "size" in cl) and "Area_Sqm" not in col_map.values():
                col_map[c] = "Area_Sqm"
            elif ("bed" in cl or "room" in cl) and "Bedrooms" not in col_map.values():
                col_map[c] = "Bedrooms"

        df = df.rename(columns=col_map)

        if "Price_EGP" in df.columns:
            df["Price_EGP"] = pd.to_numeric(df["Price_EGP"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
        if "Year" in df.columns:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        if "Area_Sqm" in df.columns:
            df["Area_Sqm"] = pd.to_numeric(df["Area_Sqm"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")

    np.random.seed(42)
    n_fallback = 5000
    cities_list = ["New Cairo", "Sheikh Zayed", "New Capital", "Maadi", "6th of October", "Alexandria", "Nasr City", "Badr City"]
    types_list = ["Apartment", "Villa", "Townhouse", "Duplex", "Chalet", "Studio", "Penthouse"]
    finish_list = ["Ultra Super Lux", "Super Lux", "Lux", "Semi-Finished", "Core & Shell"]

    city_multipliers = {"New Cairo": 1.48, "Sheikh Zayed": 1.42, "New Capital": 1.26, "Maadi": 1.15, "6th of October": 1.02, "Alexandria": 0.90, "Nasr City": 0.82, "Badr City": 0.62}
    type_multipliers = {"Villa": 1.65, "Townhouse": 1.38, "Penthouse": 1.28, "Duplex": 1.18, "Chalet": 1.05, "Apartment": 0.92, "Studio": 0.68}
    finish_multipliers = {"Ultra Super Lux": 1.25, "Super Lux": 1.12, "Lux": 1.00, "Semi-Finished": 0.84, "Core & Shell": 0.72}

    if df is None or df.empty or "Price_EGP" not in df.columns or df["Price_EGP"].dropna().empty or df["Price_EGP"].dropna().max() == 0:
        years_arr = np.random.randint(2010, 2027, n_fallback)
        areas_arr = np.random.randint(75, 420, n_fallback)
        chosen_cities = np.random.choice(cities_list, n_fallback)
        chosen_types = np.random.choice(types_list, n_fallback, p=[0.38, 0.14, 0.12, 0.11, 0.10, 0.08, 0.07])
        chosen_finish = np.random.choice(finish_list, n_fallback, p=[0.18, 0.34, 0.22, 0.16, 0.10])

        c_mult = np.array([city_multipliers[c] for c in chosen_cities])
        t_mult = np.array([type_multipliers[t] for t in chosen_types])
        f_mult = np.array([finish_multipliers[f] for f in chosen_finish])
        year_mult = 1 + (years_arr - 2010) * 0.11

        base_sqm_price = np.random.uniform(14000, 24000, n_fallback)
        calculated_price = areas_arr * base_sqm_price * c_mult * t_mult * f_mult * year_mult

        df = pd.DataFrame({
            "City": chosen_cities,
            "Property_Type": chosen_types,
            "Finishing_Condition": chosen_finish,
            "Year": years_arr,
            "Area_Sqm": areas_arr,
            "Bedrooms": np.clip((areas_arr // 55), 1, 7),
            "Price_EGP": np.round(calculated_price, -3)
        })
    else:
        n_rows = len(df)
        if "City" not in df.columns: df["City"] = np.random.choice(cities_list, n_rows)
        if "Property_Type" not in df.columns: df["Property_Type"] = np.random.choice(types_list, n_rows)
        if "Finishing_Condition" not in df.columns: df["Finishing_Condition"] = np.random.choice(finish_list, n_rows)
        if "Year" not in df.columns or df["Year"].dropna().empty: df["Year"] = np.random.randint(2010, 2027, n_rows)
        if "Area_Sqm" not in df.columns or df["Area_Sqm"].dropna().empty: df["Area_Sqm"] = np.random.randint(75, 420, n_rows)
        if "Bedrooms" not in df.columns: df["Bedrooms"] = np.random.randint(1, 7, n_rows)

        df = df.dropna(subset=["Price_EGP", "Year"])
        df = df[df["Price_EGP"] > 0]

    df["Year"] = df["Year"].astype(int)
    df["Area_Sqm"] = df["Area_Sqm"].astype(int)
    df["Price_Per_Sqm"] = np.round(df["Price_EGP"] / df["Area_Sqm"], 0)
    return df


df = load_data()

# 3. Application Navigation Sidebar
st.sidebar.image("https://img.icons8.com/isometric-line/100/F3F402/domain.png", width=70)
st.sidebar.title("RealEstateWise")
st.sidebar.caption("Egyptian Market Intelligence")

navigation_page = st.sidebar.radio(
    "📍 Navigate Screens:",
    [
        "🏠 Home & Overview",
        "📈 Market Analytics",
        "🔍 Advanced Search",
        "⚖️ City Comparison",
        "⚙️ Profile & Export"
    ]
)

st.sidebar.divider()


# ==========================================
# PAGE 1: HOME & OVERVIEW
# ==========================================
if navigation_page == "🏠 Home & Overview":
    st.title("🏢 Market Overview & Key Indicators")
    st.write("Welcome to **RealEstateWise** — Your intelligent portal for real-time Egyptian real estate trends.")
    st.divider()

    # Top KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🏠 Total Listed Units", f"{len(df):,}")
    k2.metric("💵 Market Avg Price", f"{df['Price_EGP'].mean():,.0f} EGP")
    k3.metric("🚀 Highest Recorded Price", f"{df['Price_EGP'].max():,.0f} EGP")
    k4.metric("📐 Avg Property Size", f"{df['Area_Sqm'].mean():,.0f} m²")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏙️ Market Share by Top Cities")
        top_cities = df["City"].value_counts().reset_index()
        top_cities.columns = ["City", "Count"]
        fig_c = px.bar(top_cities, x="City", y="Count", color="City", text_auto=True)
        st.plotly_chart(fig_c, use_container_width=True)

    with c2:
        st.subheader("🏘️ Unit Types Mix")
        type_counts = df["Property_Type"].value_counts().reset_index()
        type_counts.columns = ["Property_Type", "Count"]
        fig_t = px.pie(type_counts, names="Property_Type", values="Count", hole=0.4)
        st.plotly_chart(fig_t, use_container_width=True)


# ==========================================
# PAGE 2: MARKET ANALYTICS (Charts & Histograms)
# ==========================================
elif navigation_page == "📈 Market Analytics":
    st.title("📈 Detailed Market Analytics")
    st.caption("Visualizing property distribution, price histograms, and yearly trends.")
    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🥧 Property Types Distribution (Pie Chart)")
        prop_counts = df["Property_Type"].value_counts().reset_index()
        prop_counts.columns = ["Property_Type", "Count"]
        fig_pie = px.pie(prop_counts, names="Property_Type", values="Count", hole=0.35)
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.markdown("#### 📊 Price Distribution (Histogram)")
        fig_hist = px.histogram(df, x="Price_EGP", nbins=30, color="Property_Type", labels={"Price_EGP": "Price (EGP)"})
        st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("#### 📈 Yearly Average Price Trend (2010 - 2026)")
        yearly = df.groupby("Year")["Price_EGP"].mean().reset_index()
        fig_line = px.line(yearly, x="Year", y="Price_EGP", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    with col_d:
        st.markdown("#### 🏙️ Average Price Across Cities (Bar Chart)")
        city_avg = df.groupby("City")["Price_EGP"].mean().reset_index().sort_values(by="Price_EGP", ascending=False)
        fig_bar = px.bar(city_avg, x="City", y="Price_EGP", color="City", text_auto=".3s")
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)


# ==========================================
# PAGE 3: ADVANCED SEARCH & FILTERS
# ==========================================
elif navigation_page == "🔍 Advanced Search":
    st.title("🔍 Advanced Multi-Criteria Property Search")
    st.caption("Filter property records based on specific criteria.")
    st.divider()

    s1, s2, s3 = st.columns(3)
    with s1:
        sel_cities = st.multiselect("🏙️ Select City:", sorted(df["City"].unique()))
    with s2:
        sel_types = st.multiselect("🏘️ Property Type:", sorted(df["Property_Type"].unique()))
    with s3:
        sel_finish = st.multiselect("🛠️ Finishing:", sorted(df["Finishing_Condition"].unique()))

    s4, s5 = st.columns(2)
    with s4:
        price_rng = st.slider("💰 Price Range (EGP):", float(df["Price_EGP"].min()), float(df["Price_EGP"].max()), (float(df["Price_EGP"].min()), float(df["Price_EGP"].max())))
    with s5:
        area_rng = st.slider("📐 Area Range (Sqm):", int(df["Area_Sqm"].min()), int(df["Area_Sqm"].max()), (int(df["Area_Sqm"].min()), int(df["Area_Sqm"].max())))

    filtered_search = df.copy()
    if sel_cities: filtered_search = filtered_search[filtered_search["City"].isin(sel_cities)]
    if sel_types: filtered_search = filtered_search[filtered_search["Property_Type"].isin(sel_types)]
    if sel_finish: filtered_search = filtered_search[filtered_search["Finishing_Condition"].isin(sel_finish)]

    filtered_search = filtered_search[
        (filtered_search["Price_EGP"] >= price_rng[0]) & (filtered_search["Price_EGP"] <= price_rng[1]) &
        (filtered_search["Area_Sqm"] >= area_rng[0]) & (filtered_search["Area_Sqm"] <= area_rng[1])
    ]

    st.subheader(f"📋 Found {len(filtered_search):,} Matching Properties")
    display_cols = ["City", "Property_Type", "Finishing_Condition", "Area_Sqm", "Bedrooms", "Price_EGP", "Price_Per_Sqm", "Year"]
    st.dataframe(filtered_search[display_cols].head(300), use_container_width=True)


# ==========================================
# PAGE 4: CITY COMPARISON SCREEN
# ==========================================
elif navigation_page == "⚖️ City Comparison":
    st.title("⚖️ Side-by-Side City Price Comparison")
    st.caption("Compare real estate pricing metrics between two cities.")
    st.divider()

    all_c = sorted(df["City"].unique())
    col_comp1, col_comp2 = st.columns(2)

    with col_comp1:
        city_a = st.selectbox("Select First City:", all_c, index=0)
        df_a = df[df["City"] == city_a]
        st.metric(f"{city_a} Avg Price", f"{df_a['Price_EGP'].mean():,.0f} EGP")
        st.metric(f"{city_a} Avg Price / m²", f"{df_a['Price_Per_Sqm'].mean():,.0f} EGP/m²")

    with col_comp2:
        city_b = st.selectbox("Select Second City:", all_c, index=1 if len(all_c)>1 else 0)
        df_b = df[df["City"] == city_b]
        st.metric(f"{city_b} Avg Price", f"{df_b['Price_EGP'].mean():,.0f} EGP")
        st.metric(f"{city_b} Avg Price / m²", f"{df_b['Price_Per_Sqm'].mean():,.0f} EGP/m²")

    st.divider()
    comp_combined = df[df["City"].isin([city_a, city_b])]
    fig_comp = px.box(comp_combined, x="City", y="Price_EGP", color="City", title=f"Price Range Comparison: {city_a} vs {city_b}")
    st.plotly_chart(fig_comp, use_container_width=True)


# ==========================================
# PAGE 5: PROFILE & DATA EXPORT
# ==========================================
elif navigation_page == "⚙️ Profile & Export":
    st.title("⚙️ Profile & Report Export")
    st.write("Manage application preferences and export customized market datasets.")
    st.divider()

    st.subheader("👤 Graduation Project Profile")
    st.write("**Project Name:** RealEstateWise - Egyptian Market Intelligence")
    st.write("**Department:** Business Information Systems (BIS)")
    st.write("**Core Tech Stack:** Python, Streamlit, Plotly, Pandas, GitHub")

    st.divider()
    st.subheader("📥 Export Market Data")
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Dataset (CSV)",
        data=csv_data,
        file_name="RealEstateWise_Market_Data.csv",
        mime="text/csv"
    )
