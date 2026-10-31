import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة بتصميم يشبه شاشة الموبايل (Figma Prototype UI)
st.set_page_config(
    page_title="عقارك | Aqarok Prototype",
    page_icon="🏢",
    layout="centered"
)

# تنسيقات CSS متقدمة لتبدو مثل تصميمات فيجما (Figma Dark Fintech UI)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    div[data-testid="metric-container"] {
        background-color: #1F2937;
        border: 1px solid #374151;
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .stButton>button {
        background-color: #6366F1;
        color: #FFFFFF;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #4F46E5;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "lang" not in st.session_state:
    st.session_state.lang = "العربية"


# 2. بيانات واقعية موسعة تشمل كل مدن السوق المصري
@st.cache_data
def load_extended_data():
    cities = [
        "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", 
        "مصر الجديدة", "مدينة نصر", "6 أكتوبر", 
        "المعادي", "الشروق", "الهرم", "زايد الجديدة"
    ]
    types_ar = ["شقة فاخرة", "فيلا مستقلة", "توين هاوس", "دوبلكس", "تاون هاوس"]
    types_en = ["Luxury Apartment", "Standalone Villa", "Twin House", "Duplex", "Townhouse"]
    
    np.random.seed(42)
    n = 150
    
    data = []
    for i in range(n):
        c = np.random.choice(cities)
        t_idx = np.random.randint(0, len(types_ar))
        area = np.random.randint(100, 450)
        beds = np.random.randint(2, 6)
        curr_price = area * np.random.randint(25000, 45000)
        fut_price = curr_price * np.random.uniform(1.5, 1.8)
        
        data.append({
            "City": c,
            "Property_Type_Ar": types_ar[t_idx],
            "Property_Type_En": types_en[t_idx],
            "Area_Sqm": area,
            "Bedrooms": beds,
            "Current_Price": curr_price,
            "Future_Price_5Y": fut_price,
            "Features_Ar": "جراج خاص، أمن 24/7، تشطيبات فاخرة",
            "Features_En": "Private garage, 24/7 security, luxury finishes"
        })
    return pd.DataFrame(data)

df_props = load_extended_data()


# ==========================================
# 3. شاشة تسجيل الدخول واللوجو (Login / Sign In)
# ==========================================
if not st.session_state.logged_in:
    col_l1, col_l2 = st.columns([2, 1])
    with col_l2:
        selected_login_lang = st.selectbox("🌐 Language", ["العربية", "English"])
        st.session_state.lang = selected_login_lang

    st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
    # عرض اللوجو الخاص بك
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=180", width=110)
    
    if st.session_state.lang == "العربية":
        st.markdown("<h2 style='color: #6366F1; margin-top: 10px;'>عقارك | Aqarok</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF;'>بوابتك الذكية للبحث العقاري والتقييم المستقبلي</p>", unsafe_allow_html=True)
        email_lbl = "البريد الإلكتروني (Email)"
        pass_lbl = "كلمة المرور (Password)"
        forgot_lbl = "هل نسيت كلمة المرور؟"
        login_btn = "تسجيل الدخول (Sign In)"
    else:
        st.markdown("<h2 style='color: #6366F1; margin-top: 10px;'>Aqarok Prototype</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF;'>Smart Real Estate Finder & Valuation</p>", unsafe_allow_html=True)
        email_lbl = "Email"
        pass_lbl = "Password"
        forgot_lbl = "Forgot Password?"
        login_btn = "Sign In"

    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

    email_input = st.text_input(email_lbl, placeholder="user@aqarok.com")
    password_input = st.text_input(pass_lbl, type="password", placeholder="••••••••")
    st.caption(forgot_lbl)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(login_btn):
        if email_input:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Please enter your email / يرجى إدخال البريد الإلكتروني.")

# ==========================================
# 4. التطبيق الرئيسي بعد الدخول (Figma Mockup Views)
# ==========================================
else:
    is_ar = (st.session_state.lang == "العربية")
    
    # القائمة السفلية أو الجانبية المبرمجة كأنها تطبيق موبايل
    if is_ar:
        nav_choice = st.sidebar.radio(
            "📱 شاشات التطبيق:",
            [
                "🏠 1. Property Finder (البحث عن عقار)",
                "⚖️ 2. City Comparison (مقارنة المدن)",
                "⚙️ 3. Settings & Support (الإعدادات والدعم)",
                "🚪 تسجيل الخروج (Logout)"
            ]
        )
    else:
        nav_choice = st.sidebar.radio(
            "📱 App Screens:",
            [
                "🏠 1. Property Finder",
                "⚖️ 2. City Comparison",
                "⚙️ 3. Settings & Support",
                "🚪 Logout"
            ]
        )

    if "تسجيل الخروج" in nav_choice or "Logout" in nav_choice:
        st.session_state.logged_in = False
        st.rerun()

    # ------------------------------------------
    # SCREEN 1: PROPERTY FINDER
    # ------------------------------------------
    if "Property Finder" in nav_choice or "البحث عن عقار" in nav_choice:
        if is_ar:
            st.subheader("🏠 Property Finder (البحث عن العقارات)")
            st.caption("اختر مواصفات العقار والمنطقة لعرض عروض البيع والأسعار المستقبلية المتوقعة.")
            lbl_city = "📍 اختر المنطقة / المدن المتاحة"
            lbl_type = "🏘️ نوع العقار"
            lbl_area = "📐 الحد الأدنى للمساحة (م²)"
            lbl_budget = "💰 الميزانية القصوى (جنيه)"
            lbl_results = "العقارات المناسبة"
        else:
            st.subheader("🏠 Property Finder")
            st.caption("Select property specs and location to explore available listings & forecasts.")
            lbl_city = "📍 Select City / Location"
            lbl_type = "🏘️ Property Type"
            lbl_area = "📐 Min Area (Sqm)"
            lbl_budget = "Max Budget (EGP)"
            lbl_results = "Matching Properties"

        st.divider()

        all_cities_list = ["الكل / All"] + sorted(df_props["City"].unique().tolist())
        c1, c2 = st.columns(2)
        with c1:
            sel_city = st.selectbox(lbl_city, all_cities_list)
            type_options = ["الكل / All"] + (df_props["Property_Type_Ar"].unique().tolist() if is_ar else df_props["Property_Type_En"].unique().tolist())
            sel_type = st.selectbox(lbl_type, type_options)
        with c2:
            min_area = st.number_input(lbl_area, min_value=50, max_value=500, value=120)
            max_budget = st.slider(lbl_budget, 2000000, 20000000, 10000000, step=500000)

        # فلترة البيانات
        filtered = df_props.copy()
        if sel_city != "الكل / All":
            filtered = filtered[filtered["City"] == sel_city]
        if sel_type != "الكل / All":
            col_t = "Property_Type_Ar" if is_ar else "Property_Type_En"
            filtered = filtered[filtered[col_t] == sel_type]
            
        filtered = filtered[(filtered["Area_Sqm"] >= min_area) & (filtered["Current_Price"] <= max_budget)]

        st.divider()
        st.markdown(f"### 📋 {lbl_results} ({len(filtered)})")

        if not filtered.empty:
            for idx, row in filtered.head(20).iterrows():
                p_type = row['Property_Type_Ar'] if is_ar else row['Property_Type_En']
                feats = row['Features_Ar'] if is_ar else row['Features_En']
                
                with st.container():
                    if is_ar:
                        st.markdown(f"""
                        **{p_type} في {row['City']}**  
                        📐 المساحة: {row['Area_Sqm']} م² | 🛏️ الغرف: {row['Bedrooms']}  
                        💵 **السعر الحالي:** {row['Current_Price']:,.0f} ج.م  
                        📈 **السعر المتوقع (بعد 5 سنوات):** <span style='color: #10B981;'>{row['Future_Price_5Y']:,.0f} ج.م</span>  
                        ✨ **المميزات:** {feats}
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        **{p_type} in {row['City']}**  
                        📐 Area: {row['Area_Sqm']} m² | 🛏️ Beds: {row['Bedrooms']}  
                        💵 **Current Price:** {row['Current_Price']:,.0f} EGP  
                        📈 **5-Year Forecast:** <span style='color: #10B981;'>{row['Future_Price_5Y']:,.0f} EGP</span>  
                        ✨ **Features:** {feats}
                        """, unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning("No properties match your criteria / لا توجد عقارات مطابقة لشروط البحث.")

    # ------------------------------------------
    # SCREEN 2: CITY COMPARISON
    # ------------------------------------------
    elif "City Comparison" in nav_choice or "مقارنة المدن" in nav_choice:
        if is_ar:
            st.subheader("⚖️ City Comparison (مقارنة بين المدن)")
            st.caption("قارن بين أي مدينتين من المدن الجديدة لمعرفة متوسط الأسعار ومعدل النمو.")
        else:
            st.subheader("⚖️ City Comparison")
            st.caption("Compare pricing metrics and growth forecasts between two cities.")

        st.divider()

        cities_available = sorted(df_props["City"].unique().tolist())
        cc1, cc2 = st.columns(2)
        with cc1:
            city_1 = st.selectbox("City 1 / المدينة الأولى", cities_available, index=0)
        with cc2:
            city_2 = st.selectbox("City 2 / المدينة الثانية", cities_available, index=1 if len(cities_available)>1 else 0)

        st.divider()

        # حساب متوسطات حقيقية من الداتا
        mean_p1 = df_props[df_props["City"] == city_1]["Current_Price"].mean() / 150
        mean_p2 = df_props[df_props["City"] == city_2]["Current_Price"].mean() / 150
        
        comp_summary = {
            "Metric / المؤشر": ["Average Price / m²", "5Y Forecast / m²", "Growth Rate", "Available Listings"],
            city_1: [f"{mean_p1:,.0f} EGP", f"{mean_p1*1.6:,.0f} EGP", "+60%", f"{len(df_props[df_props['City']==city_1])}"],
            city_2: [f"{mean_p2:,.0f} EGP", f"{mean_p2*1.55:,.0f} EGP", "+55%", f"{len(df_props[df_props['City']==city_2])}"]
        }
        st.table(pd.DataFrame(comp_summary))

    # ------------------------------------------
    # SCREEN 3: SETTINGS & SUPPORT (إعدادات اللغة والحساب)
    # ------------------------------------------
    elif "Settings" in nav_choice or "الإعدادات والدعم" in nav_choice:
        if is_ar:
            st.subheader("⚙️ Settings & Support (الإعدادات والدعم)")
            st.caption("تغيير اللغة، إعدادات الحساب، وخدمة العملاء.")
        else:
            st.subheader("⚙️ Settings & Support")
            st.caption("Language settings, account profile, and technical support.")

        st.divider()

        # 🌐 خيار تغيير اللغة الفعلي المطلوب
        st.markdown("🌐 **Language Preferences / لغة التطبيق:**")
        new_lang = st.selectbox("Choose Language", ["العربية", "English"], index=0 if is_ar else 1)
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

        st.divider()
        st.markdown("👤 **Account Settings / تعديل الحساب:**")
        st.text_input("Full Name", value="أحمد محمد (Aqarok Expert)")
        st.text_input("Phone Number", value="+20 1012345678")
        if st.button("Save Changes"):
            st.success("Changes saved successfully!")

        st.divider()
        st.markdown("📞 **Customer Support / الدعم الفني:**")
        st.info("💬 Email: support@aqarok.com \n📞 Hotline: 19888 (24/7 Available)")

        st.divider()
        st.markdown("ℹ️ **About Us & Privacy / عن التطبيق:**")
        st.write("Aqarok AI Platform v2.5 — Empowering Egyptian real estate investments with advanced intelligence.")
