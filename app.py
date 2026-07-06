import streamlit as st
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="بصمجيات", layout="centered")

# إضافة اللوجو في أعلى الصفحة
try:
    image = Image.open('logo.jpg') 
    st.image(image, width=150)
except:
    st.info("💡 بصمجيات - مساعدك الأكاديمي")

st.title("بصمجيات ⚡")

grade_map = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0}

tab1, tab2 = st.tabs(["الترم الحالي", "التراكمي"])

# حساب الترم (سريع وتلقائي)
with tab1:
    semester_points = 0
    total_hours = 0
    for i in range(6):
        col1, col2 = st.columns([3, 1])
        grade = col1.selectbox(f"مادة {i+1}", list(grade_map.keys()), key=f"g{i}")
        hours = col2.number_input(f"ساعات", 1, 4, 3, key=f"h{i}")
        semester_points += grade_map[grade] * hours
        total_hours += hours
    
    if total_hours == 18:
        gpa = semester_points / 18
        st.success(f"النتيجة: {gpa:.2f}")
    else:
        st.warning(f"مجموع الساعات الحالي: {total_hours}/18")

# حساب التراكمي (تلقائي مع الخيارات)
with tab2:
    num_prev_terms = st.number_input("عدد الترمات السابقة:", min_value=0, value=0)
    prev_gpa = st.number_input("المعدل التراكمي السابق (CGPA):", min_value=0.0, max_value=4.0, step=0.01)
    
    add_term1 = st.checkbox("إضافة بيانات الترم الأول")
    term1_gpa = st.number_input("معدل الترم الأول:", min_value=0.0, max_value=4.0, step=0.01) if add_term1 else 0.0
    
    add_term2 = st.checkbox("إضافة بيانات الترم الثاني")
    term2_gpa = st.number_input("معدل الترم الثاني:", min_value=0.0, max_value=4.0, step=0.01) if add_term2 else 0.0
    
    prev_hours = num_prev_terms * 18
    term1_hours = 18 if add_term1 else 0
    term2_hours = 18 if add_term2 else 0
    
    total_points = (prev_gpa * prev_hours) + (term1_gpa * term1_hours) + (term2_gpa * term2_hours)
    total_hours = prev_hours + term1_hours + term2_hours
    
    if total_hours > 0:
        cgpa = total_points / total_hours
        st.metric("المعدل التراكمي النهائي", f"{cgpa:.2f}")
    else:
        st.info("أدخل البيانات ليظهر التراكمي تلقائياً")
