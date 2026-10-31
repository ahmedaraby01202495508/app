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


# 2. بيانات المدن مع الإحداثيات الجغرافية (للخريطة) والمميزات الحقيقية
@st.cache_data
def load_cities_data():
    return {
        "التجمع الخامس": {
            "lat": 30.0321, "lon": 31.4704,
            "advantages_ar": "قريب من الجامعة الأمريكية، مجتمعات عمرانية حديثة، شبكة طرق رئيسية، خدمات متكاملة.",
            "advantages_en": "Close to AUC, modern gated communities, major highway access, full amenities."
        },
        "الشيخ زايد": {
            "lat": 30.0636, "lon": 30.9783,
            "advantages_ar": "هدوء و مساحات خضراء واسعة، مولات تجارية كبرى، تخطيط عمراني منظم.",
            "advantages_en": "Quiet environment, vast green spaces, major commercial malls, well-planned layout."
        },
        "العاصمة الإدارية": {
            "lat": 30.0160, "lon": 31.7582,
            "advantages_ar": "مستقبل الاستثمار، النهر الأخضر، الحي الحكومي، عوائد استثمارية مستقبلية عالية.",
            "advantages_en": "Future of investment, Green River, government district, high future ROI."
        },
        "مصر الجديدة": {
            "lat": 30.0898, "lon": 31.3291,
            "advantages_ar": "عراقة المنطقة، قربها من المطار، شبكة مواصلات ومترو ممتازة، طابع معماري فريد.",
            "advantages_en": "Historic charm, close to airport, excellent metro/transit network, unique architecture."
        },
        "مدينة نصر": {
            "lat": 30.0570, "lon": 31.3404,
            "advantages_ar": "حيوية المنطقة، كثافة تجارية عالية، سهولة الوصول لجميع أنحاء القاهرة.",
            "advantages_en": "Vibrant area, high commercial activity, easy access to all parts of Cairo."
        },
        "6 أكتوبر": {
            "lat": 29.9577, "lon": 30.9168,
            "advantages_ar": "مدن صناعية كبرى، جامعات عريقة، مجتمعات سكنية متنوعة تناسب كافة الفئات.",
            "advantages_en": "Major industrial zones, prominent universities, diverse housing options for all tiers."
        },
        "المعادي": {
            "lat": 29.9602, "lon": 31.2569,
            "advantages_ar": "إطلالة مميزة على النيل، طابع هادئ، أشجار كثيفة، سفارات وأجانب.",
            "advantages_en": "Nile views, quiet atmosphere, leafy streets, popular among expats and embassies."
        },
        "الشروق": {
            "lat": 30.1185, "lon": 31.6033,
            "advantages_ar": "هدوء، أسعار مناسبة للاستثمار المتوسط، جامعات وكليات حديثة.",
            "advantages_en": "Peaceful, affordable for mid-tier investment, modern universities."
        }
    }

cities_info = load_cities_data()


@st.cache_data
def load_extended_data():
    cities = list(cities_info.keys())
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
# 4. التطبيق الرئيسي بعد الدخول (مع ترجمة كاملة لكل النصوص)
# ==========================================
else:
    is_ar = (st.session_state.lang == "العربية")
    
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

        all_cities_list = ["الكل / All"] + sorted(list(cities_info.keys()))
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
    # SCREEN 2: CITY COMPARISON (مع الخرائط والمميزات المطلوبة)
    # ------------------------------------------
    elif "City Comparison" in nav_choice or "مقارنة المدن" in nav_choice:
        if is_ar:
            st.subheader("⚖️ City Comparison & Maps (مقارنة المدن والخرائط)")
            st.caption("قارن بين أي مدينتين، وتعرف على المميزات، الأسعار المستقبلية، والخرائط التفاعلية.")
            lbl_c1 = "المدينة الأولى"
            lbl_c2 = "المدينة الثانية"
            adv_title = "🌟 أبرز مميزات المدينة:"
            map_title = "🗺️ خريطة الموقع الجغرافي:"
        else:
            st.subheader("⚖️ City Comparison & Maps")
            st.caption("Compare pricing metrics, advantages, and interactive maps between two cities.")
            lbl_c1 = "First City"
            lbl_c2 = "Second City"
            adv_title = "🌟 City Advantages:"
            map_title = "🗺️ Geographical Map Preview:"

        st.divider()

        cities_available = sorted(list(cities_info.keys()))
        cc1, cc2 = st.columns(2)
        with cc1:
            city_1 = st.selectbox(lbl_c1, cities_available, index=0)
        with cc2:
            city_2 = st.selectbox(lbl_c2, cities_available, index=1 if len(cities_available)>1 else 0)

        st.divider()

        # حساب متوسطات حقيقية
        mean_p1 = df_props[df_props["City"] == city_1]["Current_Price"].mean() / 150
        mean_p2 = df_props[df_props["City"] == city_2]["Current_Price"].mean() / 150
        
        comp_summary = {
            "Metric / المؤشر": ["Average Price / m²", "5Y Forecast / m²", "Growth Rate", "Available Listings"],
            city_1: [f"{mean_p1:,.0f} EGP", f"{mean_p1*1.6:,.0f} EGP", "+60%", f"{len(df_props[df_props['City']==city_1])}"],
            city_2: [f"{mean_p2:,.0f} EGP", f"{mean_p2*1.55:,.0f} EGP", "+55%", f"{len(df_props[df_props['City']==city_2])}"]
        }
        st.table(pd.DataFrame(comp_summary))

        # عرض المميزات لكل مدينة
        st.markdown(f"### {adv_title}")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.info(f"**{city_1}:**\n\n" + (cities_info[city_1]["advantages_ar"] if is_ar else cities_info[city_1]["advantages_en"]))
        with col_m2:
            st.info(f"**{city_2}:**\n\n" + (cities_info[city_2]["advantages_ar"] if is_ar else cities_info[city_2]["advantages_en"]))

        # عرض الخرائط التفاعلية لكل مدينة
        st.markdown(f"### {map_title}")
        map_col1, map_col2 = st.columns(2)
        with map_col1:
            st.text(city_1)
            df_map1 = pd.DataFrame({'lat': [cities_info[city_1]["lat"]], 'lon': [cities_info[city_1]["lon"]]})
            st.map(df_map1, zoom=11)
        with map_col2:
            st.text(city_2)
            df_map2 = pd.DataFrame({'lat': [cities_info[city_2]["lat"]], 'lon': [cities_info[city_2]["lon"]]})
            st.map(df_map2, zoom=11)

    # ------------------------------------------
    # SCREEN 3: SETTINGS & SUPPORT (تغيير اللغة الفعلي وشامل)
    # ------------------------------------------
    elif "Settings" in nav_choice or "الإعدادات والدعم" in nav_choice:
        if is_ar:
            st.subheader("⚙️ Settings & Support (الإعدادات والدعم)")
            st.caption("تغيير اللغة، إعدادات الحساب، وخدمة العملاء.")
            lbl_lang_change = "🌐 لغة التطبيق (App Language):"
            lbl_acc = "👤 إعدادات الحساب (Account Settings):"
            lbl_name = "الاسم بالكامل"
            lbl_phone = "رقم الهاتف"
            lbl_save = "حفظ التعديلات"
            lbl_supp = "📞 خدمة العملاء والدعم الفني:"
            lbl_about = "ℹ️ عن التطبيق وسياسة الخصوصية:"
        else:
            st.subheader("⚙️ Settings & Support")
            st.caption("Language settings, account profile, and technical support.")
            lbl_lang_change = "🌐 App Language:"
            lbl_acc = "👤 Account Settings:"
            lbl_name = "Full Name"
            lbl_phone = "Phone Number"
            lbl_save = "Save Changes"
            lbl_supp = "📞 Customer Support & Technical Help:"
            lbl_about = "ℹ️ About Us & Privacy Policy:"

        st.divider()

        # 🌐 تغيير لغة التطبيق بالكامل من الإعدادات
        st.markdown(lbl_lang_change)
        new_lang = st.selectbox("Choose Language / اختر اللغة", ["العربية", "English"], index=0 if is_ar else 1)
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.rerun()

        st.divider()
        st.markdown(lbl_acc)
        st.text_input(lbl_name, value="أحمد محمد (Aqarok Expert)")
        st.text_input(lbl_phone, value="+20 1012345678")
        if st.button(lbl_save):
            st.success("Changes saved successfully! / تم حفظ التعديلات بنجاح.")

        st.divider()
        st.markdown(lbl_supp)
        st.info("💬 Email / البريد الإلكتروني: support@aqarok.com \n📞 Hotline / الخط الساخن: 19888 (24/7 Available)")

        st.divider()
        st.markdown(lbl_about)
        if is_ar:
            st.write("""
            * **من نحن (About Us):** منصة "عقارك" هي النظام الذكي الأول لمساعدة المستثمرين والموظفين في تقييم العقارات بدقة بالاعتماد على بيانات السوق المصري.
            * **سياسة الخصوصية (Privacy Policy):** جميع بيانات العملاء وعمليات البحث مشفرة ومحمية بالكامل وفقاً للمعايير الأمنية المعتمدة.
            """)
        else:
            st.write("""
            * **About Us:** Aqarok platform is the leading intelligent system empowering investors and professionals to accurately evaluate Egyptian real estate.
            * **Privacy Policy:** All customer data and search operations are fully encrypted and protected according to certified security standards.
            """)
