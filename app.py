import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(
    page_title="منظومة إدارة القوى العاملة",
    page_icon="🩺",
    layout="wide"
)

# تحسين المظهر بدعم اللغة العربية واتجاه النص
st.markdown("""
    <style>
    body, [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🩺 منظومة إدارة القوى العاملة لفنيي المعامل")
st.caption("إدارة بئر العبد الصحية – قسم المتوطنة | إعداد وتصميم: أحمد مسعد رشاد")

FILE_NAME = "منظومة_إدارة_القوى_العاملة_احمد_مسعد_رشاد.xlsx"

@st.cache_data
def load_data():
    try:
        df_emp = pd.read_excel(FILE_NAME, sheet_name="cheet1")
        df_units = pd.read_excel(FILE_NAME, sheet_name="الوحدات")
        
        # تنظيف مسافات النصوص في أسماء الوحدات
        if 'الوحدة' in df_emp.columns:
            df_emp['الوحدة_النظيفة'] = df_emp['الوحدة'].astype(str).str.strip()
        if 'الوحدة' in df_units.columns:
            df_units['الوحدة_النظيفة'] = df_units['الوحدة'].astype(str).str.strip()

        return df_emp, df_units
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
        return None, None

df_emp, df_units = load_data()

if df_emp is not None and df_units is not None:
    df_units_clean = df_units[df_units['الوحدة_النظيفة'] != 'الاجمالى'].dropna(subset=['الوحدة'])

    # --- 1. كروت المؤشرات الرئيسية ---
    col1, col2, col3 = st.columns(3)
    total_employees = len(df_emp)
    total_units = len(df_units_clean)
    
    col1.metric("إجمالي الموظفين 👥", f"{total_employees}")
    col2.metric("إجمالي الوحدات الصحية 🏥", f"{total_units}")
    col3.metric("متوسط الموظفين/وحدة 📊", f"{total_employees/total_units:.1f}")

    st.divider()

    # --- 2. الرسم البياني ---
    st.subheader("📊 توزيع الموظفين حسب الوحدات الصحية")
    fig_units = px.bar(
        df_units_clean, 
        x="الوحدة", 
        y="عدد الموظفين",
        text_auto=True,
        color="عدد الموظفين",
        color_continuous_scale="Blues"
    )
    fig_units.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_units, use_container_width=True)

    st.divider()

    # --- 3. البحث والتصفية ---
    st.subheader("🔍 البحث وتصفية الفنيين")
    
    # جلب أسماء الوحدات الفعلية المسجلة لدى الموظفين لتفادي أي اختلاف
    available_units = sorted(list(df_emp['الوحدة_النظيفة'].dropna().unique()))
    
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        search_unit = st.selectbox(
            "اختر الوحدة الصحية:", 
            options=["الكل"] + available_units
        )
        
    with col_search2:
        search_name = st.text_input("أو ابحث باسم الموظف / الرقم القومي:")

    # تطبيق التصفية
    filtered_df = df_emp.copy()
    
    if search_unit != "الكل":
        filtered_df = filtered_df[filtered_df['الوحدة_النظيفة'] == search_unit]
        
    if search_name:
        filtered_df = filtered_df[
            filtered_df['الإسم'].astype(str).str.contains(search_name, case=False, na=False) | 
            filtered_df['الرقم القومي'].astype(str).str.contains(search_name, case=False, na=False)
        ]

    st.write(f"عدد النتائج: **{len(filtered_df)}** فني")

    # عرض الجدول
    st.dataframe(
        filtered_df[['م', 'الإسم', 'الرقم القومي', 'الوحدة', 'رقم الهاتف', 'ملاحظات']], 
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("يرجى التأكد من وجود ملف الإكسيل في نفس مجلد الكود.")
