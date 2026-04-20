import io
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Amazon Reviews Dashboard",
    page_icon="📱",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #1f2937;
}
.metric-card {
    background-color: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("Amazon_Unlocked_Mobil.xlsx")
    return df

df = load_data()

st.title("📊 Amazon Reviews Analysis Dashboard")
st.write("استكشاف وتحليل بيانات مراجعات منتجات Amazon بشكل بسيط ومرتب.")

st.sidebar.header("🎛️ Filters")

# تنظيف الداتا
df_clean = df.dropna().copy()

# التأكد من وجود الأعمدة
rating_col = "Rating" if "Rating" in df_clean.columns else None
review_col = "Reviews" if "Reviews" in df_clean.columns else None
brand_col = "Brand Name" if "Brand Name" in df_clean.columns else None

# فلتر Rating
if rating_col:
    ratings = sorted(df_clean[rating_col].dropna().unique().tolist())
    selected_ratings = st.sidebar.multiselect(
        "اختر Rating",
        options=ratings,
        default=ratings
    )
    df_filtered = df_clean[df_clean[rating_col].isin(selected_ratings)]
else:
    df_filtered = df_clean.copy()

# فلتر بحث في الريفيوز
if review_col:
    search_text = st.sidebar.text_input("🔍 ابحث داخل Reviews")
    if search_text:
        df_filtered = df_filtered[
            df_filtered[review_col].astype(str).str.contains(search_text, case=False, na=False)
        ]

# عرض أرقام سريعة
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("عدد الصفوف", f"{len(df):,}")

with col2:
    st.metric("بعد التنظيف", f"{len(df_clean):,}")

with col3:
    st.metric("بعد الفلترة", f"{len(df_filtered):,}")

with col4:
    if rating_col:
        st.metric("متوسط التقييم", f"{df_filtered[rating_col].mean():.2f}")
    else:
        st.metric("متوسط التقييم", "N/A")

st.markdown("---")

left, right = st.columns([2, 1])

with left:
    st.subheader("📄 Sample of Filtered Data")
    st.dataframe(df_filtered.head(50), use_container_width=True)

with right:
    st.subheader("❗ Missing Values")
    st.dataframe(df.isna().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Count"}), use_container_width=True)

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("⭐ Rating Distribution")
    if rating_col:
        rating_counts = df_filtered[rating_col].value_counts().sort_index()
        st.bar_chart(rating_counts)
    else:
        st.info("عمود Rating غير موجود في البيانات.")

with col_b:
    st.subheader("🏷️ Top Brands")
    if brand_col:
        top_brands = df_filtered[brand_col].value_counts().head(10)
        st.bar_chart(top_brands)
    else:
        st.info("عمود Brand Name غير موجود في البيانات.")

st.markdown("---")

st.subheader("ℹ️ Dataset Info")
buffer = io.StringIO()
df_filtered.info(buf=buffer)
info_str = buffer.getvalue()
st.text(info_str)

st.markdown("---")

with st.expander("📌 Show Raw Data"):
    st.dataframe(df, use_container_width=True)
