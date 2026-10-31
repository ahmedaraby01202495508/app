import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
    /* إطار يشبه شاشة الموبايل */
    .mobile-frame {
        background-color: #111827;
        border: 2px solid #374151;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
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


# دالة بيانات وهمية واقعية للعقارات والمدن
@st.cache_data
def load_mock_data():
    return pd.DataFrame({
        "City": ["التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "مصر الجديدة", "التجمع الخامس", "الشيخ زايد"],
        "Property_Type": ["شقة فاخرة", "فيلا مستقلة", "توين هاوس", "شقة", "دوبلكس", "تاون هاوس"],
        "Area_Sqm": [165, 350, 210, 130, 280, 240],
        "Bedrooms": [3, 5, 3, 2, 4, 4],
        "Current_Price": [4500000, 14000000, 6200000, 3200000, 8500000, 9100000],
        "Future_Price_5Y": [7200000, 22000000, 10500000, 49000000, 13500000, 14200000],
        "Features": ["جراج خاص، أمن 24/7", "حديقة خاصة، حمام سباحة", "إطلالة على النهر الأخضر", "قريب من المترو", "تشطيبات فائقة", "نادي صحي"]
    })

df_props = load_mock_data()


# ==========================================
# 1. LOGIN / SIGN IN SCREEN (شاشة تسجيل الدخول واللوجو)
# ==========================================
if not st.session_state.logged_in:
    col_l1, col_l2 = st.columns([2, 1])
    with col_l2:
        st.session_state.lang = st.selectbox("🌐 Language", ["العربية", "English"])

    st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
    # عرض اللوجو الخاص بك المرفق في المحادثة
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=180", width=110)
    
    if st.session_state.lang == "العربية":
        st.markdown("<h2 style='color: #6366F1; margin-top: 10px;'>عقارك | Aqarok</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF;'>بوابتك الذكية للبحث العقاري والتقييم المستقبلي</p>", unsafe_allow_html=True)
        email_lbl = "البريد الإلكتروني (Email)"
        pass_lbl = "كلمة المرور (Password)"
        forgot_lbl = "هل نسيت كلمة المرور؟ (Forgot Password)"
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
# MAIN APP NAVIGATION (التنقل بين الأقسام الـ 4 المطلوبة)
# ==========================================
else:
    # قائمة التنقل تشبه تصميمات تطبيقات الموبايل الحديثة
    if st.session_state.lang == "العربية":
        nav_choice = st.sidebar.radio(
            "📱 شاشات التطبيق (Figma Screens):",
            [
                "🏠 1. Property Finder (البحث عن عقار)",
                "⚖️ 2. City Comparison (مقارنة المدن)",
                "⚙️ 3. Settings & Support (الإعدادات والدعم)",
                "🚪 تسجيل الخروج (Logout)"
            ]
        )
    else:
        nav_choice = st.sidebar.radio(
            "📱 App Screens (Figma View):",
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
    # SCREEN 2: PROPERTY FINDER
    # ------------------------------------------
    if "Property Finder" in nav_choice or "البحث عن عقار" in nav_choice:
        if st.session_state.lang == "العربية":
            st.subheader("🏠 Property Finder (البحث عن العقارات)")
            st.caption("أدخل مواصفات العقار الذي تبحث عنه لعرض عروض البيع والأسعار المستقبلية.")
        else:
            st.subheader("🏠 Property Finder")
            st.caption("Filter property specs to explore listings and future price forecasts.")

        st.divider()

        # إدخال مواصفات العقار
        c1, c2 = st.columns(2)
        with c1:
            sel_city = st.selectbox("📍 المنطقة / المدينة", ["الكل", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "مصر الجديدة"])
            sel_type = st.selectbox("🏘️ نوع العقار", ["الكل", "شقة فاخرة", "فيلا مستقلة", "توين هاوس", "دوبلكس"])
        with c2:
            min_area = st.number_input("📐 الحد الأدنى للمساحة (م²)", min_value=50, max_value=500, value=120)
            budget = st.slider("💰 الميزانية القصوى (جنيه)", 2000000, 20000000, 10000000, step=500000)

        # فلترة البيانات
        filtered = df_props.copy()
        if sel_city != "الكل":
            filtered = filtered[filtered["City"] == sel_city]
        if sel_type != "الكل":
            filtered = filtered[filtered["Property_Type"] == sel_type]
        filtered = filtered[(filtered["Area_Sqm"] >= min_area) & (filtered["Current_Price"] <= budget)]

        st.divider()
        st.markdown(f"### 📋 العقارات المناسبة ({len(filtered)} عقار متاح)")

        if not filtered.empty:
            for idx, row in filtered.iterrows():
                with st.container():
                    st.markdown(f"""
                    **{row['Property_Type']} في {row['City']}**  
                    📐 المساحة: {row['Area_Sqm']} م² | 🛏️ الغرف: {row['Bedrooms']}  
                    💵 **السعر الحالي:** {row['Current_Price']:,.0f} ج.م  
                    📈 **السعر المتوقع (بعد 5 سنوات):** <span style='color: #10B981;'>{row['Future_Price_5Y']:,.0f} ج.م</span>  
                    ✨ **المميزات:** {row['Features']}
                    """, unsafe_allow_html=True)
                    st.divider()
        else:
            st.warning("لا توجد عقارات مطابقة تماماً لشروط البحث، جرب تعديل الميزانية أو المساحة.")

    # ------------------------------------------
    # SCREEN 3: CITY COMPARISON
    # ------------------------------------------
    elif "City Comparison" in nav_choice or "مقارنة المدن" in nav_choice:
        if st.session_state.lang == "العربية":
            st.subheader("⚖️ City Comparison (مقارنة بين مدينتين)")
            st.caption("قارن الأسعار المستقبلية والمميزات بين مدينتين لتحديد أفضل فرصة استثمارية.")
        else:
            st.subheader("⚖️ City Comparison")
            st.caption("Compare current and future pricing, advantages, and maps between two cities.")

        st.divider()

        cc1, cc2 = st.columns(2)
        with cc1:
            city_1 = st.selectbox("المدينة الأولى", ["التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية"], index=0)
        with cc2:
            city_2 = st.selectbox("المدينة الثانية", ["التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية"], index=1)

        st.divider()

        # جدول مقارنة الأسعار والمميزات
        comp_summary = {
            "المؤشر الاستثماري": ["متوسط سعر المتر الحالي", "السعر المتوقع (5 سنوات)", "معدل النمو المتوقع", "أبرز المميزات"],
            city_1: ["32,000 ج.م / م²", "51,000 ج.م / م²", "+59.3%", "قرب المدارس الدولية والخدمات، شبكة طرق جديدة"],
            city_2: ["38,000 ج.م / م²", "60,000 ج.م / م²", "+57.8%", "هدوء، مساحات خضراء واسعة، مجتمعات بوابات مغلقة"]
        }
        st.table(pd.DataFrame(comp_summary))

        st.markdown("🗺️ **خريطة الموقع التفاعلية (Location Map Preview):**")
        # محاكاة عرض خريطة لكل مدينة
        map_data = pd.DataFrame({
            'lat': [30.0444, 30.0131],
            'lon': [31.4556, 30.9853]
        })
        st.map(map_data, zoom=9)

    # ------------------------------------------
    # SCREEN 4: SETTINGS & SUPPORT
    # ------------------------------------------
    elif "Settings" in nav_choice or "الإعدادات والدعم" in nav_choice:
        if st.session_state.lang == "العربية":
            st.subheader("⚙️ Settings & Support (الإعدادات والدعم)")
            st.caption("إدارة الحساب، الدعم الفني، وسياسة الخصوصية.")
        else:
            st.subheader("⚙️ Settings & Support")
            st.caption("App settings, account profile, customer service, and support.")

        st.divider()

        st.markdown("👤 **تعديل الحساب (Account Settings):**")
        st.text_input("الاسم بالكامل", value="أحمد محمد (مقيم عقاري)")
        st.text_input("رقم الهاتف", value="+20 1012345678")
        if st.button("حفظ التعديلات"):
            st.success("تم تحديث بيانات الحساب بنجاح.")

        st.divider()
        st.markdown("📞 **خدمة العملاء والدعم الفني (Customer Support):**")
        st.info("💬 البريد الإلكتروني للدعم: support@aqarok.com \n📞 الخط الساخن: 19888 (متاح 24/7)")

        st.divider()
        st.markdown("ℹ️ **عن التطبيق وسياسة الخصوصية (About Us & Privacy):**")
        st.write("""
        * **About Us:** منصة "عقارك" هي النظام الذكي الأول لمساعدة المستثمرين والموظفيم في تقييم العقارات بدقة بالاعتماد على بيانات السوق المصري.
        * **Privacy Policy:** جميع بيانات العملاء وعمليات البحث مشفرة ومحمية بالكامل وفقاً للمعايير الأمنية المعتمدة.
        """)
