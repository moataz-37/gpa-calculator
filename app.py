import streamlit as st
from PIL import Image

st.set_page_config(page_title="بصمجيات", layout="centered")

try:
    image = Image.open('logo.jpg') 
    st.image(image, width=150)
except:
    st.info("بصمجيات لحساب التقدير ")

st.title("بصمجيات لحساب التقدير ")

grade_map = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'F': 0.0}

def get_grade_label(gpa):
    if gpa >= 3.50: return "ممتاز"
    elif gpa >= 2.70: return "جيد جداً"
    elif gpa >= 1.70: return "جيد"
    elif gpa >= 1.00: return "مقبول"
    else: return "راسب"


tab1, tab2, tab3 = st.tabs(["الترم الحالي", "التراكمي", "تقدير التخرج 🎓"])

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
    st.subheader("تخطيط للتخرج")

    # تعريف التقديرات
    labels = ["مقبول", "جيد", "جيد جداً", "ممتاز"]
    values = [1.0, 1.7, 2.7, 3.5]
    
    if 'idx' not in st.session_state:
        st.session_state.idx = 1 

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("➕"):
            if st.session_state.idx < len(labels) - 1: st.session_state.idx += 1
        if st.button("➖"):
            if st.session_state.idx > 0: st.session_state.idx -= 1
            
    with col_btn2:
        st.write(f"### التقدير المستهدف: {labels[st.session_state.idx]}")
        
    target_val = values[st.session_state.idx]
    
    col1, col2 = st.columns(2)
    terms_left = col1.number_input("عدد الترمات المتبقية:", min_value=0, max_value=10, value=4)
    terms_done = col2.number_input("عدد الترمات التي أنهيتها:", min_value=0, max_value=10, value=6)
    current_cgpa = st.number_input("معدلك التراكمي الحالي:", min_value=0.0, max_value=4.0, value=2.0, step=0.01)
    
    total_terms = terms_left + terms_done
    
    if total_terms > 10:
        st.error(f"⚠️ خطأ: إجمالي عدد الترمات ({total_terms}) يتجاوز 10.")
    elif total_terms > 0 and terms_left > 0:
        done_hours = terms_done * 18
        rem_hours = terms_left * 18
        total_hours = done_hours + rem_hours
        

        min_required_gpa = (target_val * total_hours - current_cgpa * done_hours) / rem_hours
        
        st.write("---")
        
        if min_required_gpa > 4.0:
            st.error(f"لا يمكن الوصول لتقدير {labels[st.session_state.idx]} بالمعدل الحالي.")
        elif min_required_gpa < 0:
            st.success("أنت بالفعل حققت هذا التقدير أو أكثر!")
        else:

            st.info(f"للحصول على تقدير **{labels[st.session_state.idx]}**:")
            

            next_idx = min(st.session_state.idx + 1, len(values) - 1)
            next_val = values[next_idx]
            max_required_gpa = (next_val * total_hours - current_cgpa * done_hours) / rem_hours
            
            # عرض الرينج
            if st.session_state.idx < len(values) - 1:
                st.metric("الرينج المطلوب", f"{max(0, min_required_gpa):.2f} - {min(4.0, max_required_gpa):.2f}")
                st.caption(f"يجب أن تحافظ على معدل بين {max(0, min_required_gpa):.2f} و {min(4.0, max_required_gpa):.2f} للوصول لهذه الفئة.")
            else:
                st.metric("المعدل الأدنى المطلوب", f"{max(0, min_required_gpa):.2f}")
