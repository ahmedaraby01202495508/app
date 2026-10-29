import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RealEstateWise Analytics", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4e34e2;'>RealEstateWise - Market Analytics & Dashboard</h1>", unsafe_allow_html=True)

# تحميل الداتا (تأكد إن ملف الـ CSV موجود في نفس الفولدر)
@st.cache_data
def load_data():
    # استبدل اسم الملف باسم ملف الداتا المدمج عندك
    return pd.read_csv("RealEstateWise_Egyptian_Dataset_2010_2026_Large.csv")

df = load_data()

st.sidebar.header("🔍 Filter Analytics")
selected_city = st.sidebar.selectbox("Select City", ["All"] + list(df["City"].unique()))

if selected_city != "All":
    filtered_df = df[df["City"] == selected_city]
else:
    filtered_df = df

# عرض مؤشرات سريعة (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Total Properties", f"{len(filtered_df):,}")
col2.metric("Average Price (EGP)", f"{filtered_df['Price_EGP'].mean():,.0f}")
col3.metric("Average Area (sqm)", f"{filtered_df['Area_sqm'].mean():.1f} sqm")

st.markdown("---")

# 1. رسم بياني يوضح تطور الأسعار عبر السنين (2010 - 2026)
st.subheader("📈 Yearly Price Evolution (2010 - 2026)")
yearly_trend = filtered_df.groupby("Year")["Price_EGP"].mean().reset_index()
fig_trend = px.line(yearly_trend, x="Year", y="Price_EGP", markers=True, title="Average Property Price Trend Over Years")
st.plotly_chart(fig_trend, use_container_width=True)

# 2. رسم بياني يوضح متوسط الأسعار حسب المدن
st.subheader("🏙️ Average Price by City")
city_price = filtered_df.groupby("City")["Price_EGP"].mean().reset_index()
fig_city = px.bar(city_price, x="City", y="Price_EGP", color="City", title="Average Property Price Across Cities")
st.plotly_chart(fig_city, use_container_width=True)
