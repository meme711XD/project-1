import streamlit as st
import pandas as pd

st.title("Amazon Reviews Analysis 📊")

# تحميل الداتا
@st.cache_data
def load_data():
    df = pd.read_excel("Amazon_Unlocked_Mobil.xlsx")
    return df

df = load_data()

st.subheader("📄 Raw Data")
st.dataframe(df)

# القيم المفقودة
st.subheader("❗ Missing Values")
st.write(df.isna().sum())

# تنظيف الداتا
df_clean = df.dropna()

st.subheader("✅ Cleaned Data")
st.dataframe(df_clean)

# معلومات عن الداتا
st.subheader("ℹ️ Dataset Info")
buffer = []
df_clean.info(buf=buffer)
st.text(str(buffer))
