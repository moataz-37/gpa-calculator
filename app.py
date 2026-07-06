import streamlit as st
from PIL import Image

# إعدادات الصفحة
st.set_page_config(page_title="بصمجيات", layout="centered")

# اللوجو
try:
    image = Image.open('logo.jpg') 
    st.image(image, width=150)
except:
    st.info("💡 بصمجيات - مساعدك الأكاديمي")

st.title("بصمجيات ⚡")

grade_map = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0}

def get_grade_label(gpa):
    if gpa >= 3.50: return "ممتاز"
    elif gpa >= 2.70: return "جيد جداً"
    elif gpa >= 1.70: return "جيد"
    elif gpa >= 1.00: return "مقبول"
    else: return "راسب"

# إضافة التبويب الثالث
tab1, tab2, tab3 = st.tabs(["الترم الحالي", "التراكمي", "حاسبة التخرج 🎓"])

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
        st.success(f"النتيجة: {gpa:.2f} - التقدير: {get_grade_label(gpa)}")
    else:
        st.warning(f"مجموع الساعات الحالي: {total_hours}/18")

with tab2:
    num_prev_terms = st.number_input("عدد الترمات السابقة:", min_value=0, value=0)
    prev_gpa = st.number_input("المعدل التراكمي السابق:", min_value=0.0, max_value=4.0, step=0.01)
    
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
        st.write(f"### التقدير العام: {get_grade_label(cgpa)}")
with tab3:
    st.subheader("تخطيط التخرج الذكي 🎓")
    
    # خدعة التنسيق: السلايدر والزرار جنب بعض
    col_a, col_b = st.columns([3, 1])
    
    # القيمة الافتراضية
    if 'target_val' not in st.session_state:
        st.session_state.target_val = 3.0

    with col_a:
        st.session_state.target_val = st.slider("اختر المعدل التراكمي المستهدف:", 1.0, 4.0, st.session_state.target_val, 0.1)
    with col_b:
        st.session_state.target_val = st.number_input("أو أدخل يدوياً:", min_value=1.0, max_value=4.0, value=st.session_state.target_val, step=0.1)
    
    st.write(f"التقدير المستهدف: **{get_grade_label(st.session_state.target_val)}**")
    
    # بقية المدخلات (تلقائية)
    col1, col2 = st.columns(2)
    with col1:
        terms_left = st.number_input("عدد الترمات المتبقية:", min_value=0, value=4)
    with col2:
        terms_done = st.number_input("عدد الترمات التي أنهيتها:", min_value=0, value=6)
    
    current_cgpa = st.number_input("معدلك التراكمي الحالي:", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    
    # الحساب التلقائي
    done_hours = terms_done * 18
    rem_hours = terms_left * 18
    total_hours = done_hours + rem_hours
    
    if total_hours > 0:
        total_needed_points = st.session_state.target_val * total_hours
        current_points = current_cgpa * done_hours
        
        if rem_hours > 0:
            required_gpa = (total_needed_points - current_points) / rem_hours
            
            st.write(f"---")
            if required_gpa > 4.0:
                st.error(f"للأسف، لا يمكن الوصول لتقدير {get_grade_label(st.session_state.target_val)} بالمعدل الحالي.")
            elif required_gpa < 0:
                st.success("أنت بالفعل حققت هذا التقدير أو أكثر!")
            else:
                st.metric("المعدل المطلوب في الترمات القادمة", f"{required_gpa:.2f}")
                st.info(f"يجب أن تحافظ على معدل **{required_gpa:.2f}** في الترمات المتبقية لتتخرج بتقدير **{get_grade_label(st.session_state.target_val)}**.")
