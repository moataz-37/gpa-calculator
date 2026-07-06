import streamlit as st

st.set_page_config(page_title="بصمجيات", layout="centered")
st.title("بصمجيات ⚡")

grade_map = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0}

tab1, tab2 = st.tabs(["الترم الحالي", "التراكمي"])

with tab1:
    semester_points = 0
    total_hours = 0
    
    # توزيع بسيط جداً وسريع
    for i in range(6):
        col1, col2 = st.columns([3, 1])
        grade = col1.selectbox(f"مادة {i+1}", list(grade_map.keys()), key=f"g{i}")
        hours = col2.number_input(f"ساعات", 1, 4, 3, key=f"h{i}")
        semester_points += grade_map[grade] * hours
        total_hours += hours
    
    # الحساب التلقائي (من غير زرار)
    if total_hours == 18:
        gpa = semester_points / 18
        st.success(f"النتيجة: {gpa:.2f}")
    else:
        st.warning(f"مجموع الساعات الحالي: {total_hours}/18")

with tab2:
    # نفس التبسيط للتراكمي
    prev_terms = st.number_input("عدد الترمات السابقة", 0, 10, 0)
    prev_gpa = st.number_input("التراكمي السابق", 0.0, 4.0, 0.0)
    
    if st.button("احسب التراكمي"):
        total_gpa = ((prev_gpa * prev_terms * 18) + (semester_points)) / ((prev_terms * 18) + 18)
        st.metric("الـ CGPA النهائي", f"{total_gpa:.2f}")
