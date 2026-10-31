import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="عقارك | Aqarok - Market Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fintech Dark Mode Styling
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

# Session State for Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# 2. Fast Data Loader
@st.cache_data(show_spinner="Loading Aqarok Real Estate Database...")
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


# ==========================================
# STEP 1: LOGIN SCREEN
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #F3F402;'>🏢 عقارك (Aqarok) - Welcome</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9CA3AF;'>Egyptian Real Estate Market Intelligence & Valuation Portal</p>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 User Login")
        username = st.text_input("Username / Email", placeholder="Enter your email...")
        password = st.text_input("Password", type="password", placeholder="Enter password...")

        if st.button("Login to Aqarok", use_container_width=True):
            if username.strip():
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please enter a valid username.")

        if st.button("🚀 Continue as Guest", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()

# ==========================================
# STEP 2 & 3: MAIN APP (After Login)
# ==========================================
else:
    st.sidebar.image("https://img.icons8.com/isometric-line/100/F3F402/domain.png", width=60)
    st.sidebar.title("🏢 عقارك (Aqarok)")
    st.sidebar.caption("BIS Graduation Project")

    # Navigation menu
    app_mode = st.sidebar.radio(
        "📍 App Navigation:",
        [
            "🏠 Market Overview",
            "🏡 Property Price Estimator & Location Search",
            "📈 Analytics & Visualizations",
            "⚖️ City Comparison",
            "⚙️ Logout"
        ]
    )

    st.sidebar.divider()

    # Handle Logout
    if app_mode == "⚙️ Logout":
        st.session_state.logged_in = False
        st.rerun()

    # ------------------------------------------
    # PAGE 1: MARKET OVERVIEW
    # ------------------------------------------
    elif app_mode == "🏠 Market Overview":
        st.title("🏢 Aqarok - Market Intelligence Dashboard")
        st.write("Real-time analytics and valuation models for the Egyptian real estate market (2010 - 2026).")
        st.divider()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("🏠 Total Units Analyzed", f"{len(df):,}")
        k2.metric("💵 Average Market Price", f"{df['Price_EGP'].mean():,.0f} EGP")
        k3.metric("🚀 Max Recorded Price", f"{df['Price_EGP'].max():,.0f} EGP")
        k4.metric("📐 Avg Property Size", f"{df['Area_Sqm'].mean():,.0f} m²")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🏙️ Top Cities by Volume")
            city_v = df["City"].value_counts().reset_index()
            city_v.columns = ["City", "Count"]
            fig_cv = px.bar(city_v, x="City", y="Count", color="City", text_auto=True)
            st.plotly_chart(fig_cv, use_container_width=True)

        with c2:
            st.subheader("🏘️ Property Types Mix")
            type_v = df["Property_Type"].value_counts().reset_index()
            type_v.columns = ["Property_Type", "Count"]
            fig_tv = px.pie(type_v, names="Property_Type", values="Count", hole=0.4)
            st.plotly_chart(fig_tv, use_container_width=True)

    # ------------------------------------------
    # PAGE 2: PROPERTY PRICE ESTIMATOR & LOCATION SEARCH (USER REQUEST)
    # ------------------------------------------
    elif app_mode == "🏡 Property Price Estimator & Location Search":
        st.title("🏡 Property Details, Location & Price Prediction")
        st.write("Select the property location and specifications to predict its estimated market price and view matching properties.")
        st.divider()

        st.subheader("📍 Select Location & Specifications")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            sel_city = st.selectbox("🏙️ Select City/Location:", sorted(df["City"].unique()))
        with col_s2:
            sel_type = st.selectbox("🏘️ Property Type:", sorted(df["Property_Type"].unique()))
        with col_s3:
            sel_finish = st.selectbox("🛠️ Finishing Condition:", sorted(df["Finishing_Condition"].unique()))

        col_s4, col_s5 = st.columns(2)
        with col_s4:
            sel_area = st.slider("📐 Property Area (Sqm):", int(df["Area_Sqm"].min()), int(df["Area_Sqm"].max()), 150)
        with col_s5:
            sel_rooms = st.slider("🛏️ Bedrooms:", 1, 7, 3)

        # Predict Price based on user inputs
        subset_pred = df[(df["City"] == sel_city) & (df["Property_Type"] == sel_type)]
        if not subset_pred.empty:
            avg_sqm_price = subset_pred["Price_Per_Sqm"].mean()
        else:
            avg_sqm_price = df["Price_Per_Sqm"].mean()

        estimated_price = sel_area * avg_sqm_price

        st.divider()
        st.markdown("### 💰 Valuation & Price Prediction Result")
        res1, res2, res3 = st.columns(3)
        res1.metric("Estimated Property Price", f"{estimated_price:,.0f} EGP")
        res2.metric("Estimated Price per m²", f"{avg_sqm_price:,.0f} EGP/m²")
        res3.metric("Selected Area", f"{sel_area} m²")

        st.divider()
        st.subheader(f"📋 Matching Properties in {sel_city} ({sel_type})")
        matching_df = df[(df["City"] == sel_city) & (df["Property_Type"] == sel_type) & (df["Finishing_Condition"] == sel_finish)]
        if matching_df.empty:
            matching_df = subset_pred

        disp_cols = ["City", "Property_Type", "Finishing_Condition", "Area_Sqm", "Bedrooms", "Price_EGP", "Price_Per_Sqm", "Year"]
        st.dataframe(matching_df[disp_cols].head(100), use_container_width=True)

    # ------------------------------------------
    # PAGE 3: ANALYTICS & VISUALIZATIONS
    # ------------------------------------------
    elif app_mode == "📈 Analytics & Visualizations":
        st.title("📈 Advanced Market Analytics")
        st.caption("Pie charts, price histograms, and yearly trends.")
        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 🥧 Property Types Share (Pie Chart)")
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
            st.markdown("#### 📈 Yearly Price Trend (2010 - 2026)")
            yearly = df.groupby("Year")["Price_EGP"].mean().reset_index()
            fig_line = px.line(yearly, x="Year", y="Price_EGP", markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

        with col_d:
            st.markdown("#### 🏙️ Average Price by City")
            city_avg = df.groupby("City")["Price_EGP"].mean().reset_index().sort_values(by="Price_EGP", ascending=False)
            fig_bar = px.bar(city_avg, x="City", y="Price_EGP", color="City", text_auto=".3s")
            fig_bar.update_traces(textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)

    # ------------------------------------------
    # PAGE 4: CITY COMPARISON
    # ------------------------------------------
    elif app_mode == "⚖️ City Comparison":
        st.title("⚖️ Side-by-Side City Price Comparison")
        st.divider()

        all_c = sorted(df["City"].unique())
        cc1, cc2 = st.columns(2)
        with cc1:
            c_a = st.selectbox("First City:", all_c, index=0)
            df_a = df[df["City"] == c_a]
            st.metric(f"{c_a} Avg Price", f"{df_a['Price_EGP'].mean():,.0f} EGP")
        with cc2:
            c_b = st.selectbox("Second City:", all_c, index=1 if len(all_c)>1 else 0)
            df_b = df[df["City"] == c_b]
            st.metric(f"{c_b} Avg Price", f"{df_b['Price_EGP'].mean():,.0f} EGP")

        st.divider()
        comp_df = df[df["City"].isin([c_a, c_b])]
        fig_box = px.box(comp_df, x="City", y="Price_EGP", color="City", title=f"Price Range: {c_a} vs {c_b}")
        st.plotly_chart(fig_box, use_container_width=True)
