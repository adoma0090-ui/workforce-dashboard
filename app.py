import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(
    page_title="منظومة إدارة القوى العاملة",
    page_icon="🩺",
    layout="wide"
)

# تحسين المظهر بدعم اللغة العربية واتجاه النص من اليمين لليسار
st.markdown("""
    <style>
    body, [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 منظومة إدارة القوى العاملة لفنيي المعامل")
st.caption("إدارة بئر العبد الصحية – قسم المتوطنة | إعداد وتصميم: أحمد مسعد رشاد")

# اسم ملف الإكسيل المتوقع
FILE_NAME = "منظومة_إدارة_القوى_العاملة_احمد_مسعد_رشاد.xlsx"

@st.cache_data
def load_data():
    try:
        # قراءة البيانات من الشيت الرئيسي
        df_emp = pd.read_excel(FILE_NAME, sheet_name="cheet1")
        df_units = pd.read_excel(FILE_NAME, sheet_name="الوحدات")
        return df_emp, df_units
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        return None, None

df_emp, df_units = load_data()

if df_emp is not None and df_units is not None:
    # تنظيف البيانات السريع
    df_units_clean = df_units[df_units['الوحدة'] != 'الاجمالى'].dropna()

    # --- 1. كروت المؤشرات الرئيسية (KPIs) ---
    col1, col2, col3 = st.columns(3)
    
    total_employees = len(df_emp)
    total_units = len(df_units_clean)
    
    col1.metric("إجمالي الموظفين 👥", f"{total_employees}")
    col2.metric("إجمالي الوحدات الصحية 🏥", f"{total_units}")
    col3.metric("متوسط الموظفين/وحدة 📊", f"{total_employees/total_units:.1f}")

    st.divider()

    # --- 2. الرسوم البيانية التفاعلية ---
    st.subheader("📊 توزيع الموظفين حسب الوحدات الصحية")
    
    fig_units = px.bar(
        df_units_clean, 
        x="الوحدة", 
        y="عدد الموظفين",
        text_auto=True,
        color="عدد الموظفين",
        color_continuous_scale="Blues",
        title="توزيع القوى العاملة على الوحدات"
    )
    fig_units.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_units, use_container_width=True)

    st.divider()

    # --- 3. البحث وتصفية بيانات الموظفين ---
    st.subheader("🔍 البحث والتصفية")
    
    search_unit = st.selectbox(
        "اختر الوحدة الصحية لعرض الموظفين:", 
        options=["الكل"] + list(df_units_clean['الوحدة'].dropna().unique())
    )
    
    search_name = st.text_input("أو ابحث باسم الموظف / الرقم القومي:")

    # تطبيق التصفية
    filtered_df = df_emp.copy()
    
    if search_unit != "الكل":
        filtered_df = filtered_df[filtered_df['الوحدة'] == search_unit]
        
    if search_name:
        filtered_df = filtered_df[
            filtered_df['الإسم'].astype(str).str.contains(search_name, case=False, na=False) | 
            filtered_df['الرقم القومي'].astype(str).str.contains(search_name, case=False, na=False)
        ]

    # عرض الجدول
    st.dataframe(
        filtered_df[['م', 'الإسم', 'الرقم القومي', 'الوحدة', 'رقم الهاتف', 'ملاحظات']], 
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("يرجى التأكد من وجود ملف الإكسيل في نفس مجلد الكود.")