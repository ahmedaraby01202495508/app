import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Aqarz", page_icon="🏠", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4e34e2;'>Aqarz - AI Property Valuation</h1>", unsafe_allow_html=True)

st.sidebar.header("📝 Property Specifications Input")

city = st.sidebar.selectbox("City", ["Cairo", "Giza", "Alexandria", "New Cairo", "6th of October City", "Nasr City", "Maadi", "Sheikh Zayed"])
category = st.sidebar.selectbox("Property Category", ["Residential", "Commercial", "Industrial"])

if category == "Residential":
    prop_type = st.sidebar.selectbox("Property Type", ["Apartment", "Villa", "Townhouse", "Standalone House"])
elif category == "Commercial":
    prop_type = st.sidebar.selectbox("Property Type", ["Office", "Retail Shop", "Commercial Center", "Mall"])
else:
    prop_type = st.sidebar.selectbox("Property Type", ["Warehouse", "Industrial Land", "Factory"])

area = st.sidebar.slider("Area (sqm)", 50, 1000, 150)
rooms = st.sidebar.slider("Number of Rooms", 1, 10, 3)
bathrooms = st.sidebar.slider("Number of Bathrooms", 1, 5, 2)
floor_level = st.sidebar.selectbox("Floor Level", ["Ground Floor", "1st Floor", "2nd Floor", "3rd Floor", "4th Floor", "5th Floor", "Higher Floors", "Penthouse"])
finishing = st.sidebar.selectbox("Finishing Condition", ["Core & Shell", "Semi Finished", "Super Lux", "Ultra Super Lux", "Lux"])
furnished = st.sidebar.checkbox("Furnished")

data = {
    'City': [city],
    'Category': [category],
    'Property_Type': [prop_type],
    'Area': [area],
    'Rooms': [rooms],
    'Bathrooms': [bathrooms],
    'Floor_Level': [floor_level],
    'Finishing': [finishing],
    'Furnished': [furnished]
}

if st.button("Calculate Estimated Price 💰"):
    estimated_price = area * 15000 + rooms * 50000 + bathrooms * 30000
    if furnished:
        estimated_price += 100000
    if finishing == "Ultra Super Lux":
        estimated_price += 200000
    formatted_price = "{:,.2f}".format(estimated_price)
    st.success(f"The Estimated Price of your property is: EGP {formatted_price}")
