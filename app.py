import io
import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(
    page_title="Amazon Reviews Sentiment App",
    page_icon="📱",
    layout="wide",
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
    }
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 8px;
    }
    .sub-text {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border: 1px solid #eef2f7;
        margin-bottom: 18px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        border-left: 6px solid #4f46e5;
        text-align: center;
    }
    .metric-label {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
    }
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 12px;
    }
    .positive-box {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 16px;
        border-radius: 14px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #a7f3d0;
    }
    .negative-box {
        background-color: #fef2f2;
        color: #991b1b;
        padding: 16px;
        border-radius: 14px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #fecaca;
    }
    .neutral-box {
        background-color: #eff6ff;
        color: #1e3a8a;
        padding: 16px;
        border-radius: 14px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        border: 1px solid #bfdbfe;
    }
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_excel("Amazon_Unlocked_Mobil.xlsx")

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive 😊", polarity
    elif polarity < 0:
        return "Negative 😞", polarity
    else:
        return "Neutral 😐", polarity

df = load_data()
df_clean = df.dropna().copy()

rating_col = "Rating" if "Rating" in df_clean.columns else None
review_col = "Reviews" if "Reviews" in df_clean.columns else None
brand_col = "Brand Name" if "Brand Name" in df_clean.columns else None
product_col = "Product Name" if "Product Name" in df_clean.columns else None

st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.write("استخدمي الفلاتر أو جرّبي تحليل ريفيو جديد.")

df_filtered = df_clean.copy()

if rating_col:
    min_rating = int(df_clean[rating_col].min())
    max_rating = int(df_clean[rating_col].max())

    selected_range = st.sidebar.slider(
        "⭐ Rating Range",
        min_value=min_rating,
        max_value=max_rating,
        value=(min_rating, max_rating)
    )

    df_filtered = df_filtered[
        (df_filtered[rating_col] >= selected_range[0]) &
        (df_filtered[rating_col] <= selected_range[1])
    ]

if brand_col:
    brands = sorted(df_clean[brand_col].astype(str).unique().tolist())
    selected_brands = st.sidebar.multiselect(
        "🏷️ Brand",
        options=brands,
        default=[]
    )
    if selected_brands:
        df_filtered = df_filtered[df_filtered[brand_col].astype(str).isin(selected_brands)]

search_text = ""
if review_col:
    search_text = st.sidebar.text_input("🔍 Search in Reviews")
    if search_text:
        df_filtered = df_filtered[
            df_filtered[review_col].astype(str).str.contains(search_text, case=False, na=False)
        ]

show_raw = st.sidebar.checkbox("📄 Show raw data", value=False)

st.markdown('<div class="main-title">📊 Amazon Reviews Sentiment Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">أدخلي أي review بالإنجليزي، والتطبيق هيحدد إذا كانت Positive أو Negative، مع عرض الداتا بشكل منظم.</div>',
    unsafe_allow_html=True
)

# Sentiment input section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">✍️ Review Sentiment Checker</div>', unsafe_allow_html=True)

user_review = st.text_area(
    "اكتبي Review هنا:",
    placeholder="Example: This phone is amazing and the battery lasts all day."
)

if st.button("Analyze Sentiment"):
    if user_review.strip():
        sentiment, polarity = get_sentiment(user_review)

        if "Positive" in sentiment:
            st.markdown(f'<div class="positive-box">{sentiment}</div>', unsafe_allow_html=True)
        elif "Negative" in sentiment:
            st.markdown(f'<div class="negative-box">{sentiment}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="neutral-box">{sentiment}</div>', unsafe_allow_html=True)

        st.write(f"**Polarity Score:** {polarity:.2f}")
    else:
        st.warning("من فضلك اكتبي review الأول.")
st.markdown('</div>', unsafe_allow_html=True)

# Metrics
avg_rating = df_filtered[rating_col].mean() if rating_col and len(df_filtered) > 0 else 0
total_rows = len(df)
clean_rows = len(df_clean)
filtered_rows = len(df_filtered)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📦 Total Rows</div>
        <div class="metric-value">{total_rows:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🧹 Clean Rows</div>
        <div class="metric-value">{clean_rows:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 Filtered Rows</div>
        <div class="metric-value">{filtered_rows:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⭐ Average Rating</div>
        <div class="metric-value">{avg_rating:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

left_col, right_col = st.columns([1.3, 1])

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⭐ Rating Distribution</div>', unsafe_allow_html=True)
    if rating_col and len(df_filtered) > 0:
        rating_counts = df_filtered[rating_col].value_counts().sort_index()
        st.bar_chart(rating_counts)
    else:
        st.info("مفيش بيانات كفاية لعرض توزيع التقييمات.")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏷️ Top 10 Brands</div>', unsafe_allow_html=True)
    if brand_col and len(df_filtered) > 0:
        top_brands = df_filtered[brand_col].astype(str).value_counts().head(10)
        st.bar_chart(top_brands)
    else:
        st.info("عمود Brand Name غير موجود أو مفيش بيانات.")
    st.markdown('</div>', unsafe_allow_html=True)

table_col1, table_col2 = st.columns(2)

with table_col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Filtered Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df_filtered.head(50), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with table_col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">❗ Missing Values</div>', unsafe_allow_html=True)
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["Column", "Missing Count"]
    st.dataframe(missing_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if product_col and rating_col and len(df_filtered) > 0:
    prod_col1, prod_col2 = st.columns(2)

    with prod_col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏆 Top Rated Products</div>', unsafe_allow_html=True)
        top_products = (
            df_filtered.groupby(product_col)[rating_col]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        st.dataframe(top_products, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with prod_col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚠️ Lowest Rated Products</div>', unsafe_allow_html=True)
        low_products = (
            df_filtered.groupby(product_col)[rating_col]
            .mean()
            .sort_values(ascending=True)
            .head(10)
            .reset_index()
        )
        st.dataframe(low_products, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">ℹ️ Dataset Info</div>', unsafe_allow_html=True)
buffer = io.StringIO()
df_filtered.info(buf=buffer)
info_str = buffer.getvalue()
st.text(info_str)
st.markdown('</div>', unsafe_allow_html=True)

if show_raw:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗂️ Full Raw Data</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
