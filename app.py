import io
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Amazon Reviews Dashboard",
    page_icon="📱",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 6px;
    }

    .sub-text {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 24px;
    }

    .card {
        background: white;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #eef2f7;
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

    .small-note {
        color: #6b7280;
        font-size: 13px;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_data():
    return pd.read_excel("Amazon_Unlocked_Mobil.xlsx")

df = load_data()

# ---------- Clean Data ----------
df_clean = df.dropna().copy()

# تحديد أسماء الأعمدة لو موجودة
rating_col = "Rating" if "Rating" in df_clean.columns else None
review_col = "Reviews" if "Reviews" in df_clean.columns else None
brand_col = "Brand Name" if "Brand Name" in df_clean.columns else None
product_col = "Product Name" if "Product Name" in df_clean.columns else None

# ---------- Sidebar ----------
st.sidebar.markdown("## 🎛️ Control Panel")
st.sidebar.write("استخدمي الفلاتر دي علشان تستكشفي البيانات بشكل أسهل.")

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

# ---------- Header ----------
st.markdown('<div class="main-title">📊 Amazon Reviews Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Dashboard احترافي لتحليل مراجعات أمازون، مع فلترة، بحث، وإحصائيات ورسوم بيانية واضحة.</div>',
    unsafe_allow_html=True
)

# ---------- Metrics ----------
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

# ---------- Charts Section ----------
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

st.write("")

# ---------- Data Tables ----------
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

st.write("")

# ---------- Top Products ----------
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

st.write("")

# ---------- Dataset Info ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">ℹ️ Dataset Info</div>', unsafe_allow_html=True)
buffer = io.StringIO()
df_filtered.info(buf=buffer)
info_str = buffer.getvalue()
st.text(info_str)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Raw Data ----------
if show_raw:
    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗂️ Full Raw Data</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
