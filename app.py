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
