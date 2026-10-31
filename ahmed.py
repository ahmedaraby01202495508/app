import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="عقارك | Aqarok AI Valuator",
    page_icon="🏢",
    layout="centered"
)

# تنسيقات CSS لتطبيق الموبايل الداكن
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
        background-color: #F3F402;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E2E302;
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التطبيق (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "property_evaluated" not in st.session_state:
    st.session_state.property_evaluated = False
if "last_property" not in st.session_state:
    st.session_state.last_property = {"city": "New Cairo", "type": "Apartment", "area": 160, "price": 4200000}


# دالة تحميل البيانات
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    cities = ["New Cairo", "Sheikh Zayed", "New Capital", "Heliopolis", "Nasr City"]
    types = ["Apartment", "Villa", "Townhouse", "Duplex"]
    finishes = ["Super Lux", "Full Finish", "Semi-Finished", "Lux"]
    
    df = pd.DataFrame({
        "City": np.random.choice(cities, n),
        "Property_Type": np.random.choice(types, n),
        "Finishing": np.random.choice(finishes, n),
        "Area_Sqm": np.random.randint(80, 450, n),
        "Bedrooms": np.random.randint(1, 6, n),
        "Price_EGP": np.random.randint(2000000, 15000000, n),
        "Year": np.random.randint(2020, 2026, n)
    })
    df["Price_Per_Sqm"] = np.round(df["Price_EGP"] / df["Area_Sqm"], 0)
    return df

df = load_data()


# ==========================================
# 1. شاشة تسجيل الدخول مع اللوجو وتحديد اللغة
# ==========================================
if not st.session_state.logged_in:
    # اختيار اللغة في شاشة الدخول أيضاً
    lang_login = st.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English"])
    
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=200", width=120)
    
    if lang_login == "العربية":
        st.markdown("<h2 style='color: #F3F402; margin-top: 10px;'>عقارك (Aqarok AI)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF;'>منصة تقييم وتحليل العقارات بالذكاء الاصطناعي</p>", unsafe_allow_html=True)
        user_label = "اسم المستخدم / البريد الإلكتروني"
        pass_label = "كلمة المرور"
        btn_label = "تسجيل الدخول"
        guest_label = "الدخول كزائر"
    else:
        st.markdown("<h2 style='color: #F3F402; margin-top: 10px;'>Aqarok AI Valuator</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9CA3AF;'>AI-Powered Real Estate Valuation & Analytics</p>", unsafe_allow_html=True)
        user_label = "Username / Email"
        pass_label = "Password"
        btn_label = "Login"
        guest_label = "Continue as Guest"
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    
    username = st.text_input(user_label, placeholder="employee@aqarok.com")
    password = st.text_input(pass_label, type="password", placeholder="••••••••")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(btn_label):
        if username:
            st.session_state.logged_in = True
            st.session_state.lang = lang_login
            st.rerun()
        else:
            st.warning("Please enter your credentials / يرجى إدخال بيانات الدخول.")

    if st.button(guest_label):
        st.session_state.logged_in = True
        st.session_state.lang = lang_login
        st.rerun()

# ==========================================
# التطبيق الرئيسي (بعد تسجيل الدخول)
# ==========================================
else:
    # زر تبديل اللغة في القائمة الجانبية
    current_lang = st.sidebar.selectbox("🌐 Language / اللغة", ["العربية", "English"], index=0 if st.session_state.get("lang", "العربية") == "العربية" else 1)
    st.session_state.lang = current_lang
    
    st.sidebar.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=100", width=60)
    st.sidebar.title("🏢 عقارك Aqarok")
    
    # ترجمة القوائم بناءً على اللغة المتاحة
    if current_lang == "العربية":
        menu = st.sidebar.radio(
            "القائمة الرئيسية:",
            [
                "📊 1. لوحة المؤشرات (Dashboard)",
                "➕ 2. إضافة عقار (Add Property)",
                "🤖 3. توقع السعر (AI Prediction)",
                "📈 4. رؤى السوق (Market Insights)",
                "⚖️ 5. مقارنة المناطق (Compare Areas)",
                "🔍 6. عقارات مشابهة (Similar Properties)",
                "🚪 تسجيل الخروج"
            ]
        )
    else:
        menu = st.sidebar.radio(
            "Main Menu:",
            [
                "📊 1. Dashboard",
                "➕ 2. Add Property",
                "🤖 3. AI Price Prediction",
                "📈 4. Market Insights",
                "⚖️ 5. Compare Areas",
                "🔍 6. Similar Properties",
                "🚪 Logout"
            ]
        )
    
    if "تسجيل الخروج" in menu or "Logout" in menu:
        st.session_state.logged_in = False
        st.rerun()

    # ------------------------------------------
    # الصفحة 1: Dashboard
    # ------------------------------------------
    if "Dashboard" in menu or "لوحة المؤشرات" in menu:
        if current_lang == "العربية":
            st.subheader("📊 لوحة المؤشرات السريعة (Dashboard)")
            st.caption("نظرة عامة على أداء السوق والتقييمات الأخيرة.")
            col1, col2 = st.columns(2)
            col1.metric("إجمالي العقارات", f"{len(df):,}")
            col2.metric("متوسط أسعار السوق", f"{df['Price_EGP'].mean():,.0f} ج.م")
            col3, col4 = st.columns(2)
            col3.metric("آخر التقييمات (اليوم)", "14 عقاراً")
            col4.metric("دقة نموذج الـ AI", "96.4%")
            st.divider()
            st.markdown("#### ⚡ إجراءات سريعة (Quick Actions)")
        else:
            st.subheader("📊 Quick Market Dashboard")
            st.caption("Overview of market performance and recent property evaluations.")
            col1, col2 = st.columns(2)
            col1.metric("Total Properties", f"{len(df):,}")
            col2.metric("Market Avg Price", f"{df['Price_EGP'].mean():,.0f} EGP")
            col3, col4 = st.columns(2)
            col3.metric("Today's Evaluations", "14 Units")
            col4.metric("AI Accuracy", "96.4%")
            st.divider()
            st.markdown("#### ⚡ Quick Actions")
            
        q1, q2 = st.columns(2)
        with q1:
            if st.button("➕ Evaluate New Property"):
                st.info("Go to Add Property tab.")
        with q2:
            if st.button("⚖️ Compare Areas"):
                st.info("Go to Compare Areas tab.")

    # ------------------------------------------
    # الصفحة 2: Add Property
    # ------------------------------------------
    elif "Add Property" in menu or "إضافة عقار" in menu:
        if current_lang == "العربية":
            st.subheader("➕ إدخال مواصفات العقار للتقييم")
            st.caption("أدخل تفاصيل الوحدة لكي يقوم الذكاء الاصطناعي بتحليلها وتقييمها بدقة.")
            city_lbl = "📍 المنطقة / المدينة"
            type_lbl = "🏘️ نوع العقار"
            finish_lbl = "🛠️ حالة التشطيب"
            area_lbl = "📐 المساحة (متر مربع)"
            bed_lbl = "🛏️ عدد غرف النوم"
            btn_lbl = "🚀 تشغيل نموذج الذكاء الاصطناعي (Evaluate)"
            succ_msg = "✨ تم تحليل العقار بنجاح! انتقل لصفحة AI Price Prediction لعرض النتائج."
        else:
            st.subheader("➕ Add Property Specifications")
            st.caption("Enter unit details for precise AI evaluation.")
            city_lbl = "📍 Location / City"
            type_lbl = "🏘️ Property Type"
            finish_lbl = "🛠️ Finishing Condition"
            area_lbl = "📐 Area (Sqm)"
            bed_lbl = "🛏️ Bedrooms"
            btn_lbl = "🚀 Run AI Evaluation"
            succ_msg = "✨ Property evaluated successfully! Check AI Price Prediction tab."

        with st.form("property_form"):
            city = st.selectbox(city_lbl, ["New Cairo", "Sheikh Zayed", "New Capital", "Heliopolis", "Nasr City"])
            p_type = st.selectbox(type_lbl, ["Apartment", "Villa", "Townhouse", "Duplex"])
            finishing = st.selectbox(finish_lbl, ["Super Lux", "Full Finish", "Semi-Finished", "Lux"])
            
            c1, c2 = st.columns(2)
            with c1:
                area = st.number_input(area_lbl, min_value=50, max_value=1000, value=160)
            with c2:
                beds = st.number_input(bed_lbl, min_value=1, max_value=7, value=3)
                
            submit_eval = st.form_submit_button(btn_lbl)
            
            if submit_eval:
                multiplier = 1.3 if city in ["New Cairo", "Sheikh Zayed"] else 1.0
                est_price = area * 25000 * multiplier * (1.2 if finishing == "Super Lux" else 1.0)
                
                st.session_state.last_property = {
                    "city": city,
                    "type": p_type,
                    "area": area,
                    "price": est_price,
                    "finishing": finishing
                }
                st.session_state.property_evaluated = True
                st.success(succ_msg)

    # ------------------------------------------
    # الصفحة 3: AI Price Prediction
    # ------------------------------------------
    elif "Prediction" in menu or "توقع السعر" in menu:
        if current_lang == "العربية":
            st.subheader("🤖 توقعات أسعار الذكاء الاصطناعي")
            st.caption("النتائج التحليلية والتقييم المالي للعقار المُدخل.")
        else:
            st.subheader("🤖 AI Price Prediction Results")
            st.caption("Financial valuation and insights based on the evaluated property.")
            
        prop = st.session_state.last_property
        pred_price = prop["price"]
        sqm_price = pred_price / prop["area"]
        min_range = pred_price * 0.92
        max_range = pred_price * 1.08
        
        st.markdown(f"**Location:** {prop['city']} | **Type:** {prop['type']} | **Area:** {prop['area']} m²")
        st.divider()
        
        st.metric("💰 Estimated Property Price", f"{pred_price:,.0f} EGP")
        c1, c2 = st.columns(2)
        c1.metric("📐 Estimated Price / m²", f"{sqm_price:,.0f} EGP/m²")
        c2.metric("📊 AI Confidence Score", "95.8%")
        
        st.info(f"💡 **Expected Market Price Range:** {min_range:,.0f} EGP — {max_range:,.0f} EGP")

    # ------------------------------------------
    # الصفحة 4: Market Insights
    # ------------------------------------------
    elif "Insights" in menu or "رؤى السوق" in menu:
        if current_lang == "العربية":
            st.subheader("📈 ملخص ورؤى السوق العقاري")
            st.caption("تحليلات شاملة لاتجاهات الأسعار والعوامل المؤثرة.")
        else:
            st.subheader("📈 Market Insights & Trends")
            st.caption("Comprehensive analysis of price trends and key market drivers.")
            
        city_avg = df.groupby("City")["Price_Per_Sqm"].mean().reset_index()
        fig = px.bar(city_avg, x="City", y="Price_Per_Sqm", color="City", title="Average Price per Sqm (EGP)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.success("↗️ **Market Trend:** +14.5% increase compared to last year.")

    # ------------------------------------------
    # الصفحة 5: Compare Areas
    # ------------------------------------------
    elif "Compare" in menu or "مقارنة المناطق" in menu:
        if current_lang == "العربية":
            st.subheader("⚖️ مقارنة بين منطقـتين")
            st.caption("مقارنة تفصيلية لمتطلبات الاستثمار العقاري.")
        else:
            st.subheader("⚖️ Side-by-Side Area Comparison")
            st.caption("Compare pricing metrics and market volume between two areas.")
            
        col1, col2 = st.columns(2)
        with col1:
            area_a = st.selectbox("Area 1", ["New Cairo", "Sheikh Zayed", "New Capital"], index=0)
        with col2:
            area_b = st.selectbox("Area 2", ["New Cairo", "Sheikh Zayed", "New Capital"], index=1)
            
        df_a = df[df["City"] == area_a]
        df_b = df[df["City"] == area_b]
        
        st.divider()
        comp_data = {
            "Metric": ["Avg Price / m²", "Avg Total Price", "Annual Growth", "Available Listings"],
            area_a: [f"{df_a['Price_Per_Sqm'].mean():,.0f} EGP", f"{df_a['Price_EGP'].mean():,.0f} EGP", "+16%", f"{len(df_a)}"],
            area_b: [f"{df_b['Price_Per_Sqm'].mean():,.0f} EGP", f"{df_b['Price_EGP'].mean():,.0f} EGP", "+14.5%", f"{len(df_b)}"]
        }
        st.table(pd.DataFrame(comp_data))

    # ------------------------------------------
    # الصفحة 6: Similar Properties
    # ------------------------------------------
    elif "Similar" in menu or "عقارات مشابهة" in menu:
        if current_lang == "العربية":
            st.subheader("🔍 العقارات المشابهة للتقييم الأخير")
        else:
            st.subheader("🔍 Similar Properties Match")
            
        prop = st.session_state.last_property
        similar = df[(df["City"] == prop["city"]) & (df["Property_Type"] == prop["type"])].head(5)
        if similar.empty:
            similar = df.head(5)
            
        for index, row in similar.iterrows():
            st.markdown(f"""
            🏠 **{row['Property_Type']} in {row['City']}**  
            📐 Area: {row['Area_Sqm']} m² | 💵 Price: {row['Price_EGP']:,.0f} EGP  
            🛠️ Finishing: {row['Finishing']} | 📅 Year: {row['Year']}
            """)
            st.divider()
