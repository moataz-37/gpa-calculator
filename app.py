import streamlit as st
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="بصمجيات", layout="wide")

# تخصيص الألوان والواجهة
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    h1 {color: #2c3e50; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# اللوجو والعنوان
try:
    image = Image.open('logo.jpg') 
    st.image(image, width=150)
except:
    st.info("💡 بصمجيات - مساعدك الأكاديمي")

st.title("بصمجيات لحساب التقدير")

# خريطة التقديرات
grade_map = {
    'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
    'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0
}

def get_grade_label(gpa):
    if gpa >= 3.50: return "ممتاز"
    elif gpa >= 2.70: return "جيد جداً"
    elif gpa >= 1.70: return "جيد"
    elif gpa >= 1.00: return "مقبول"
    else: return "راسب"

# التبويبات
tab1, tab2 = st.tabs(["📊 حساب الترم", "📈 حساب التراكمي"])

with tab1:
    st.subheader("إدخال مواد الترم الحالي")
    with st.expander("ℹ️ تعليمات إدخال البيانات"):
        st.write("أدخل تقدير كل مادة وعدد ساعاتها. مجموع الساعات المسموح به هو 18 ساعة.")
    
    semester_points = 0
    total_hours_input = 0
    
    for i in range(6):
        with st.expander(f"مادة رقم {i+1}"):
            col1, col2 = st.columns(2)
            with col1:
                grade = st.selectbox(f"التقدير", list(grade_map.keys()), key=f"s_g{i}")
            with col2:
                hours = st.number_input(f"الساعات", min_value=1, max_value=4, value=3, key=f"s_h{i}")
            semester_points += grade_map[grade] * hours
            total_hours_input += hours
    
    if st.button("احسب GPA الترم"):
        if total_hours_input > 18:
            st.error(f"خطأ: مجموع الساعات ({total_hours_input}) يتجاوز 18 ساعة!")
        elif total_hours_input < 18:
            st.warning(f"تنبيه: مجموع الساعات ({total_hours_input}) أقل من 18.")
        else:
            gpa = semester_points / 18
            col_res1, col_res2 = st.columns(2)
            col_res1.metric("معدل الترم", f"{gpa:.2f}")
            col_res2.metric("التقدير", get_grade_label(gpa))

with tab2:
    st.subheader("حساب التراكمي (CGPA)")
    
    num_prev_terms = st.number_input("عدد الترمات السابقة:", min_value=0, value=0)
    prev_gpa = st.number_input("المعدل التراكمي السابق (CGPA):", min_value=0.0, max_value=4.0, step=0.01)
    
    add_term1 = st.checkbox("إضافة بيانات الترم الأول")
    term1_gpa = st.number_input("معدل الترم الأول:", min_value=0.0, max_value=4.0, step=0.01) if add_term1 else 0.0
    
    add_term2 = st.checkbox("إضافة بيانات الترم الثاني")
    term2_gpa = st.number_input("معدل الترم الثاني:", min_value=0.0, max_value=4.0, step=0.01) if add_term2 else 0.0
    
    if st.button("احسب التراكمي النهائي"):
        prev_hours = num_prev_terms * 18
        term1_hours = 18 if add_term1 else 0
        term2_hours = 18 if add_term2 else 0
        
        total_points = (prev_gpa * prev_hours) + (term1_gpa * term1_hours) + (term2_gpa * term2_hours)
        total_hours = prev_hours + term1_hours + term2_hours
        
        if total_hours > 0:
            cgpa = total_points / total_hours
            st.metric("المعدل التراكمي النهائي", f"{cgpa:.2f}")
            st.success(f"التقدير العام: {get_grade_label(cgpa)}")
        else:
            st.error("يرجى إدخال البيانات المطلوبة")
