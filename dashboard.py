import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="RealEstateWise Dashboard",
    page_icon="📈",
    layout="wide"
)

# عنوان لوحة التحكم الرئيسي
st.markdown("<h1 style='text-align: center; color: #F3F4D2;'>RealEstateWise Dashboard - Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555555;'>Interactive dashboard analyzing Egyptian real estate trends</h3>", unsafe_allow_html=True)
st.markdown("---")

# تحميل البيانات (استخدام رابط التحميل المباشر من Google Drive)
@st.cache_data
def load_data():
    file_id = "1STCcSXWw1skfeWxctmy6EZ-BucamssaO"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    df = pd.read_csv(url)
    return df

df = load_data()

# استكشاف الداتا (Sidebar Filters) للتحكم في عرض البيانات البياني
st.sidebar.header("🎛️ Dashboard Controls")

# صفية حسب المدينة
selected_city = st.sidebar.selectbox("Filter by City", ["All Cities"] + list(df['City'].unique()) if 'City' in df.columns else ["All Cities"])

# صفية حسب السنة
min_yr = int(df['Year'].min()) if 'Year' in df.columns else 2010
max_yr = int(df['Year'].max()) if 'Year' in df.columns else 2026
selected_years = st.sidebar.slider("Select Year Range", min_yr, max_yr, (2015, 2026))

# فلترة البيانات بناءً على اختيارات المستخدم
filtered_df = df.copy()
if selected_city != "All Cities" and 'City' in df.columns:
    filtered_df = filtered_df[filtered_df['City'] == selected_city]
if 'Year' in df.columns:
    filtered_df = filtered_df[(filtered_df['Year'] >= selected_years[0]) & (filtered_df['Year'] <= selected_years[1])]

# عرض نظرة عامة سريعة ومؤشرات رئيسية
st.subheader("📊 Quick Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Properties", len(filtered_df))
with col2:
    avg_price = filtered_df['Price'].mean() if 'Price' in filtered_df.columns else 0
    st.metric("Average Price", f"{avg_price:,.0f} EGP")
with col3:
    max_price = filtered_df['Price'].max() if 'Price' in filtered_df.columns else 0
    st.metric("Max Price", f"{max_price:,.0f} EGP")

st.markdown("---")

# الرسوم البيانية وتحليل البيانات
st.subheader("📈 Real Estate Trends Analysis")
if 'Year' in filtered_df.columns and 'Price' in filtered_df.columns:
    fig_trend = px.line(filtered_df.groupby('Year')['Price'].mean().reset_index(), x='Year', y='Price', title="Average Price Trend Over Years")
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Columns 'Year' or 'Price' not found for trend analysis.")

# عرض عينة من البيانات المفلترة
st.subheader("📋 Filtered Data Preview")
st.dataframe(filtered_df.head(100))
