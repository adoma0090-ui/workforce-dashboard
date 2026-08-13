import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة - اسم البرنامج "معامل" فقط والأيقونة ميكروسكوب
st.set_page_config(
    page_title="معامل",
    page_icon="🔬",
    layout="wide"
)

# --- نظام التحكم في تسجيل الدخول (Username & Password) ---
USERS = {
    "ahmed": "123456",       # اسم المستخدم وكلمة المرور الخاصة بك
    "admin": "pass2026"       # يمكنك إضافة مستخدمين آخرين هنا
}

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.markdown("<h2 style='text-align: center;'>🔐 تسجيل الدخول لمنظومة معامل</h2>", unsafe_allow_html=True)
        st.write("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username_input = st.text_input("اسم المستخدم (Username):")
            password_input = st.text_input("كلمة المرور (Password):", type="password")
            login_btn = st.button("تسجيل الدخول 🚀", use_container_width=True)

            if login_btn:
                if username_input in USERS and USERS[username_input] == password_input:
                    st.session_state["logged_in"] = True
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")
        return False
    return True

# التشغيل فقط بعد تسجيل الدخول
if check_login():

    # 2. تصميم الهيدر والترويسة الرسمية
    st.markdown("""
        <style>
        body, [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }
        .header-box {
            background: linear-gradient(135deg, #0e4b56 0%, #176B87 100%);
            color: white;
            padding: 22px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        }
        .header-title {
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 6px;
        }
        .header-sub {
            font-size: 18px;
            color: #E0F4FF;
            margin-bottom: 12px;
        }
        .header-designer {
            background-color: rgba(255, 255, 255, 0.15);
            display: inline-block;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 15px;
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.25);
        }
        </style>
        
        <div class="header-box">
            <div class="header-title">🔬 منظومة إدارة القوى العاملة لفنيي المعامل</div>
            <div class="header-sub">🏛️ إدارة بئر العبد الصحية – قسم المتوطنة</div>
            <div class="header-designer">
                <b>إعداد وتصميم:</b> أحمد مسعد رشاد | <b>مشرف المتوطنة</b> | 📞 01005852737
            </div>
        </div>
        """, unsafe_allow_html=True)

    # زر تسجيل الخروج في الشريط الجانبي
    with st.sidebar:
        st.write("👤 مرحباً بك")
        if st.button("تسجيل الخروج 🚪"):
            st.session_state["logged_in"] = False
            st.rerun()

    FILE_NAME = "منظومة_إدارة_القوى_العاملة_احمد_مسعد_رشاد.xlsx"

    @st.cache_data
    def load_data():
        try:
            df_emp = pd.read_excel(FILE_NAME, sheet_name="cheet1")
            df_units = pd.read_excel(FILE_NAME, sheet_name="الوحدات")
            
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
            color_continuous_scale="Tealgrn"
        )
        fig_units.update_layout(xaxis_tickangle=-45, showlegend=False)
        st.plotly_chart(fig_units, use_container_width=True)

        st.divider()

        # --- 3. البحث والتصفية ---
        st.subheader("🔍 البحث وتصفية الفنيين")
        
        available_units = sorted(list(df_emp['الوحدة_النظيفة'].dropna().unique()))
        
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            search_unit = st.selectbox(
                "اختر الوحدة الصحية:", 
                options=["الكل"] + available_units
            )
            
        with col_search2:
            search_name = st.text_input("أو ابحث باسم الموظف / الرقم القومي:")

        filtered_df = df_emp.copy()
        
        if search_unit != "الكل":
            filtered_df = filtered_df[filtered_df['الوحدة_النظيفة'] == search_unit]
            
        if search_name:
            filtered_df = filtered_df[
                filtered_df['الإسم'].astype(str).str.contains(search_name, case=False, na=False) | 
                filtered_df['الرقم القومي'].astype(str).str.contains(search_name, case=False, na=False)
            ]

        st.write(f"عدد النتائج: **{len(filtered_df)}** فني")

        st.dataframe(
            filtered_df[['م', 'الإسم', 'الرقم القومي', 'الوحدة', 'رقم الهاتف', 'ملاحظات']], 
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #555;'>منظومة معامل القوى العاملة © إعداد وتصميم: <b>أحمد مسعد رشاد</b> (01005852737)</p>", unsafe_allow_html=True)

    else:
        st.warning("يرجى التأكد من وجود ملف الإكسيل في نفس مجلد الكود.")