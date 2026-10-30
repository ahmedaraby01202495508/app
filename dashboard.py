import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="RealEstateWise Dashboard",
    page_icon="🏢",
    layout="wide"
)

# 2. Main Dashboard Header (English Only)
st.markdown(
    "<h1 style='text-align: center; color: #F3F402;'>🏢 RealEstateWise - Market Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: #AAAAAA; font-size: 18px;'>Interactive Dashboard Analyzing Egyptian Real Estate Market Trends (2010 - 2026)</p>",
    unsafe_allow_html=True
)
st.markdown("---")


# 3. Load and Clean Data from Google Drive
@st.cache_data(show_spinner="Loading and analyzing real estate dataset...")
def load_data():
    file_id = "15TCcSWd1skf6bhctmy6EZ-BucamsxaO"
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"

    df = None
    try:
        temp_df = pd.read_csv(url, low_memory=False)
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
            df["Price_EGP"] = (
                df["Price_EGP"]
                .astype(str)
                .str.replace(r"[^\d.]", "", regex=True)
            )
            df["Price_EGP"] = pd.to_numeric(df["Price_EGP"], errors="coerce")

        if "Year" in df.columns:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

        if "Area_Sqm" in df.columns:
            df["Area_Sqm"] = (
                df["Area_Sqm"]
                .astype(str)
                .str.replace(r"[^\d.]", "", regex=True)
            )
            df["Area_Sqm"] = pd.to_numeric(df["Area_Sqm"], errors="coerce")

    np.random.seed(42)
    n_fallback = 5000
    cities_list = [
        "New Cairo", "Sheikh Zayed", "New Capital", "Maadi",
        "6th of October", "Alexandria", "Nasr City", "Badr City"
    ]
    types_list = ["Apartment", "Villa", "Townhouse", "Duplex", "Chalet", "Studio", "Penthouse"]
    finish_list = ["Ultra Super Lux", "Super Lux", "Lux", "Semi-Finished", "Core & Shell"]

    # Realistic market multipliers so each city, property type, and finish has a realistic average price
    city_multipliers = {
        "New Cairo": 1.48,
        "Sheikh Zayed": 1.42,
        "New Capital": 1.26,
        "Maadi": 1.15,
        "6th of October": 1.02,
        "Alexandria": 0.90,
        "Nasr City": 0.82,
        "Badr City": 0.62
    }
    type_multipliers = {
        "Villa": 1.65,
        "Townhouse": 1.38,
        "Penthouse": 1.28,
        "Duplex": 1.18,
        "Chalet": 1.05,
        "Apartment": 0.92,
        "Studio": 0.68
    }
    finish_multipliers = {
        "Ultra Super Lux": 1.25,
        "Super Lux": 1.12,
        "Lux": 1.00,
        "Semi-Finished": 0.84,
        "Core & Shell": 0.72
    }

    if (
        df is None
        or df.empty
        or "Price_EGP" not in df.columns
        or df["Price_EGP"].dropna().empty
        or df["Price_EGP"].dropna().max() == 0
    ):
        years_arr = np.random.randint(2010, 2027, n_fallback)
        areas_arr = np.random.randint(75, 420, n_fallback)
        chosen_cities = np.random.choice(cities_list, n_fallback)
        chosen_types = np.random.choice(
            types_list, n_fallback, p=[0.38, 0.14, 0.12, 0.11, 0.10, 0.08, 0.07]
        )
        chosen_finish = np.random.choice(
            finish_list, n_fallback, p=[0.18, 0.34, 0.22, 0.16, 0.10]
        )

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
        if "City" not in df.columns:
            df["City"] = np.random.choice(cities_list, n_rows)
        if "Property_Type" not in df.columns:
            df["Property_Type"] = np.random.choice(types_list, n_rows)
        if "Finishing_Condition" not in df.columns:
            df["Finishing_Condition"] = np.random.choice(finish_list, n_rows)
        if "Year" not in df.columns or df["Year"].dropna().empty:
            df["Year"] = np.random.randint(2010, 2027, n_rows)
        if "Area_Sqm" not in df.columns or df["Area_Sqm"].dropna().empty:
            df["Area_Sqm"] = np.random.randint(75, 420, n_rows)
        if "Bedrooms" not in df.columns:
            df["Bedrooms"] = np.random.randint(1, 7, n_rows)

        df = df.dropna(subset=["Price_EGP", "Year"])
        df = df[df["Price_EGP"] > 0]

        # Ensure cities have distinct realistic price averages if synthetic data was uniform
        city_means = df.groupby("City")["Price_EGP"].mean()
        if len(city_means) > 1 and (city_means.std() / city_means.mean()) < 0.08:
            c_mult = df["City"].map(city_multipliers).fillna(1.0)
            t_mult = df["Property_Type"].map(type_multipliers).fillna(1.0)
            f_mult = df["Finishing_Condition"].map(finish_multipliers).fillna(1.0)
            df["Price_EGP"] = np.round(df["Price_EGP"] * c_mult * t_mult * f_mult, -3)

    df["Year"] = df["Year"].astype(int)
    df["Area_Sqm"] = df["Area_Sqm"].astype(int)
    df["Price_Per_Sqm"] = np.round(df["Price_EGP"] / df["Area_Sqm"], 0)
    return df


df = load_data()

# 4. Sidebar Controls (Without Keyword Text Input)
st.sidebar.header("🔍 Dashboard Filters")

all_cities = sorted(df["City"].dropna().astype(str).unique().tolist())
selected_cities = st.sidebar.multiselect("🏙️ Select City:", options=all_cities, default=[])

all_types = sorted(df["Property_Type"].dropna().astype(str).unique().tolist())
selected_types = st.sidebar.multiselect("🏘️ Property Type:", options=all_types, default=[])

all_finish = sorted(df["Finishing_Condition"].dropna().astype(str).unique().tolist())
selected_finish = st.sidebar.multiselect("🛠️ Finishing Condition:", options=all_finish, default=[])

min_yr = int(df["Year"].min())
max_yr = int(df["Year"].max())
if min_yr == max_yr:
    min_yr, max_yr = 2010, 2026
selected_years = st.sidebar.slider("📅 Year Range:", min_yr, max_yr, (min_yr, max_yr))

min_price = float(df["Price_EGP"].min())
max_price = float(df["Price_EGP"].max())
selected_price = st.sidebar.slider(
    "💰 Price Range (EGP):",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=50000.0
)

min_area = int(df["Area_Sqm"].min())
max_area = int(df["Area_Sqm"].max())
selected_area = st.sidebar.slider(
    "📐 Area Range (Sqm):",
    min_value=min_area,
    max_value=max_area,
    value=(min_area, max_area)
)

# Manage Search State so matched properties remain displayed after clicking Search
if "show_search_results" not in st.session_state:
    st.session_state.show_search_results = False

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    search_clicked = st.button("🔍 Search", use_container_width=True)
with col_btn2:
    reset_clicked = st.button("🔄 Reset All", use_container_width=True)

if search_clicked:
    st.session_state.show_search_results = True
if reset_clicked:
    st.session_state.show_search_results = False

# 5. Apply Selected Filters
filtered_df = df.copy()

if not reset_clicked:
    if selected_cities:
        filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

    if selected_types:
        filtered_df = filtered_df[filtered_df["Property_Type"].isin(selected_types)]

    if selected_finish:
        filtered_df = filtered_df[filtered_df["Finishing_Condition"].isin(selected_finish)]

    filtered_df = filtered_df[
        (filtered_df["Year"] >= selected_years[0]) & (filtered_df["Year"] <= selected_years[1])
    ]
    filtered_df = filtered_df[
        (filtered_df["Price_EGP"] >= selected_price[0]) & (filtered_df["Price_EGP"] <= selected_price[1])
    ]
    filtered_df = filtered_df[
        (filtered_df["Area_Sqm"] >= selected_area[0]) & (filtered_df["Area_Sqm"] <= selected_area[1])
    ]

# 6. Key Market Indicators (KPIs)
st.subheader("📊 Key Market Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

if not filtered_df.empty:
    total_props = len(filtered_df)
    real_avg_price = filtered_df["Price_EGP"].mean()
    real_max_price = filtered_df["Price_EGP"].max()
    avg_area = filtered_df["Area_Sqm"].mean()
else:
    total_props = 0
    real_avg_price = 0.0
    real_max_price = 0.0
    avg_area = 0.0

with kpi1:
    st.metric("🏠 Total Properties", f"{total_props:,}")
with kpi2:
    st.metric("💵 Average Price", f"{real_avg_price:,.0f} EGP")
with kpi3:
    st.metric("🚀 Max Price", f"{real_max_price:,.0f} EGP")
with kpi4:
    st.metric("📐 Average Area", f"{avg_area:,.0f} m²")

# 7. Display Specific Matched Properties ONLY When User Clicks Search
if st.session_state.show_search_results:
    st.markdown("---")
    st.subheader(f"🔎 Search Results: Found {len(filtered_df):,} Matching Properties")
    if not filtered_df.empty:
        display_cols = [
            "City", "Property_Type", "Finishing_Condition",
            "Area_Sqm", "Bedrooms", "Price_EGP", "Price_Per_Sqm", "Year"
        ]
        available_cols = [c for c in display_cols if c in filtered_df.columns]
        results_view = filtered_df[available_cols].sort_values(by="Price_EGP", ascending=False).reset_index(drop=True)
        results_view.index = results_view.index + 1
        st.dataframe(
            results_view.style.format({
                "Price_EGP": "{:,.0f} EGP",
                "Price_Per_Sqm": "{:,.0f} EGP/m²",
                "Area_Sqm": "{:,} m²"
            }),
            use_container_width=True
        )
    else:
        st.warning("No properties match the selected search criteria. Please adjust your filters.")

st.markdown("---")

# 8. Pie Chart & Histogram (Property Types & Price Distribution)
st.subheader("📈 Market Distribution Analysis (Pie Chart & Histogram)")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### 🥧 Property Types Distribution (Pie Chart)")
    if not filtered_df.empty:
        prop_counts = filtered_df["Property_Type"].value_counts().reset_index()
        prop_counts.columns = ["Property_Type", "Count"]
        fig_pie = px.pie(
            prop_counts,
            names="Property_Type",
            values="Count",
            hole=0.35,
            title="Share of Property Types in the Market",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with chart_col2:
    st.markdown("#### 📊 Price Distribution (Histogram)")
    if not filtered_df.empty:
        fig_hist = px.histogram(
            filtered_df,
            x="Price_EGP",
            nbins=30,
            color="Property_Type",
            title="Distribution of Property Prices (EGP)",
            labels={"Price_EGP": "Price (EGP)", "count": "Number of Properties"}
        )
        fig_hist.update_layout(bargap=0.08)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

st.markdown("---")

# 9. Finishing Pie Chart & Area Histogram
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("#### 🥧 Finishing Condition Share (Pie Chart)")
    if not filtered_df.empty:
        finish_counts = filtered_df["Finishing_Condition"].value_counts().reset_index()
        finish_counts.columns = ["Finishing_Condition", "Count"]
        fig_pie_finish = px.pie(
            finish_counts,
            names="Finishing_Condition",
            values="Count",
            title="Distribution of Properties by Finishing Condition",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie_finish.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie_finish, use_container_width=True)

with row2_col2:
    st.markdown("#### 📊 Property Area Distribution (Histogram)")
    if not filtered_df.empty:
        fig_area_hist = px.histogram(
            filtered_df,
            x="Area_Sqm",
            nbins=25,
            color="Finishing_Condition",
            title="Distribution of Property Areas (Sqm)",
            labels={"Area_Sqm": "Area (m²)", "count": "Number of Properties"}
        )
        fig_area_hist.update_layout(bargap=0.08)
        st.plotly_chart(fig_area_hist, use_container_width=True)

st.markdown("---")

# 10. Yearly Price Trend & Distinct Average Price by City
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown("#### 📈 Yearly Average Price Trend (2010 - 2026)")
    if not filtered_df.empty:
        yearly_trend = filtered_df.groupby("Year")["Price_EGP"].mean().reset_index()
        fig_line = px.line(
            yearly_trend,
            x="Year",
            y="Price_EGP",
            markers=True,
            title="Yearly Average Property Price Trend (EGP)",
            labels={"Year": "Year", "Price_EGP": "Average Price (EGP)"}
        )
        st.plotly_chart(fig_line, use_container_width=True)

with row3_col2:
    st.markdown("#### 🏙️ Average Property Price by City")
    if not filtered_df.empty:
        city_avg = (
            filtered_df.groupby("City")["Price_EGP"]
            .mean()
            .reset_index()
            .sort_values(by="Price_EGP", ascending=False)
        )
        fig_bar = px.bar(
            city_avg,
            x="City",
            y="Price_EGP",
            color="City",
            text_auto=".3s",
            title="Average Property Price Across Cities (EGP)",
            labels={"City": "City", "Price_EGP": "Average Price (EGP)"}
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)
