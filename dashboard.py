import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات صفحة الـ Streamlit
st.set_page_config(
    page_title="RealEstateWise Dashboard",
    page_icon="🏢",
    layout="wide"
)

# عنوان لوحة التحكم الرئيسي
st.markdown("<h1 style='text-align: center; color: #1F3A52;'>RealEstateWise - Market Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555;'>Interactive dashboard analyzing Egyptian real estate trends from 2010 to 2026</p>", unsafe_allow_html=True)
st.markdown("---")

# 2. تحميل البيانات (تأكد أن اسم الملف مطابق للملف المدمج لديك)
@st.cache_data
def load_data():
    # استبدل هذا المسار باسم ملف الداتا الخاص بك
    df = pd.read_csv("RealEstateWise_Egyptian_Dataset_2010_2026_Large.csv")
    return df

df = load_data()

# 3. شريط التحكم الجانبي (Sidebar Filters) للاستكشاف التفاعلي
st.sidebar.header("🎛️ Dashboard Controls")

# تصفية حسب المدينة
selected_city = st.sidebar.selectbox("Filter by City", ["All Cities"] + list(df["City"].unique()))

# تصفية حسب سنة العقار
min_yr, max_yr = int(df["Year"].min()), int(df["Year"].max())
selected_years = st.sidebar.slider("Select Year Range", min_yr, max_yr, (2010, 2026))

# تطبيق الفلاتر على الداتا
filtered_df = df.copy()
if selected_city != "All Cities":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

filtered_df = filtered_df[(filtered_df["Year"] >= selected_years[0]) & (filtered_df["Year"] <= selected_years[1])]

# 4. عرض مؤشرات الأداء الأساسية (KPIs Metrics)
col1, col2, col3, col4 = st.columns(4)

total_properties = len(filtered_df)
avg_price = filtered_df["Price_EGP"].mean() if total_properties > 0 else 0
avg_area = filtered_df["Area_sqm"].mean() if total_properties > 0 else 0
max_price = filtered_df["Price_EGP"].max() if total_properties > 0 else 0

col1.metric("🏠 Total Properties", f"{total_properties:,}")
col2.metric("💰 Average Price", f"EGP {avg_price:,.0f}")
col3.metric("📐 Average Area", f"{avg_area:.1f} sqm")
col4.metric("📈 Max Property Price", f"EGP {max_price:,.0f}")

st.markdown("---")

# 5. الرسوم البيانية والتحليلات (Charts Section)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📈 Yearly Price Evolution (Trend)")
    if not filtered_df.empty:
        yearly_trend = filtered_df.groupby("Year")["Price_EGP"].mean().reset_index()
        fig_trend = px.line(
            yearly_trend, x="Year", y="Price_EGP", markers=True,
            title="Average Price Growth Over Years",
            labels={"Price_EGP": "Avg Price (EGP)", "Year": "Year"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with row1_col2:
    st.subheader("🏙️ Average Price by City")
    if not filtered_df.empty:
        city_price = filtered_df.groupby("City")["Price_EGP"].mean().reset_index()
        fig_city = px.bar(
            city_price, x="City", y="Price_EGP", color="City",
            title="Price Comparison Across Cities",
            labels={"Price_EGP": "Avg Price (EGP)", "City": "City"}
        )
        st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🏷️ Property Types Distribution")
    if not filtered_df.empty:
        prop_counts = filtered_df["Property_Type"].value_counts().reset_index()
        prop_counts.columns = ["Property_Type", "Count"]
        fig_pie = px.pie(
            prop_counts, names="Property_Type", values="Count",
            title="Share of Property Types"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available.")

with row2_col2:
    st.subheader("🛋️ Finishing Condition Impact on Price")
    if not filtered_df.empty:
        finish_price = filtered_df.groupby("Finishing_Condition")["Price_EGP"].mean().reset_index()
        fig_finish = px.bar(
            finish_price, x="Finishing_Condition", y="Price_EGP", color="Finishing_Condition",
            title="Average Price by Finishing Quality",
            labels={"Price_EGP": "Avg Price (EGP)", "Finishing_Condition": "Finishing"}
        )
        st.plotly_chart(fig_finish, use_container_width=True)
    else:
        st.warning("No data available.")

st.markdown("---")

# 6. جدول عرض البيانات المصفاة
st.subheader("📋 Filtered Dataset Records")
st.dataframe(filtered_df.head(100), use_container_width=True)
