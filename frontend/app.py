import streamlit as st
import requests

FIREBASE_WEB_API_KEY = "AIzaSyC90QIqYeYyRfWnGAVKVe-HuGNzF1LtKOY"
BACKEND_URL = "http://127.0.0.1:8000"

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return r.json()
    return None

st.title("Todo App - Lab 2")

if "token" not in st.session_state:
    st.subheader("Đăng nhập")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user_data = login(email, password)
        if user_data:
            st.session_state["token"] = user_data["idToken"]
            st.session_state["email"] = user_data["email"]
            st.success("Đăng nhập thành công!")
            st.rerun()
        else:
            st.error("Sai email hoặc mật khẩu.")
else:
    st.write(f"Xin chào, **{st.session_state['email']}**")
    if st.button("Đăng xuất"):
        del st.session_state["token"]
        del st.session_state["email"]
        st.rerun()
    
    st.divider()
    
    st.subheader("Thêm công việc")
    col_task, col_time = st.columns([2, 1])
    with col_task:
        new_task = st.text_input("Nhập nội dung:")
    with col_time:
        new_time = st.text_input("Thời gian (VD: 10:00, Mai...):")

    if st.button("Lưu Task"):
        if new_task:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            payload = {"title": new_task, "status": "pending", "time": new_time}
            r = requests.post(f"{BACKEND_URL}/tasks", json=payload, headers=headers)
            if r.status_code == 200:
                st.success("Đã thêm thành công!")
                st.rerun()
        else:
            st.warning("Vui lòng nhập nội dung công việc!")
    
    st.divider()
    
    st.subheader("Danh sách của bạn:")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    r = requests.get(f"{BACKEND_URL}/tasks", headers=headers)
    
    if r.status_code == 200:
        tasks = r.json().get("tasks", [])
        if not tasks:
            st.info("Chưa có công việc nào.")
        else:
            for idx, t in enumerate(tasks):
                title_display = f"{idx + 1}. {t['title']} | Trạng thái: {t.get('status', 'pending')} | Thời gian: {t.get('time', 'Trống')}"
                
                with st.expander(title_display):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    status_options = ["pending", "in-progress", "completed"]
                    current_status = t.get('status', 'pending')
                    if current_status not in status_options:
                        status_options.append(current_status)
                        
                    with col1:
                        edit_status = st.selectbox("Cập nhật trạng thái", status_options, index=status_options.index(current_status), key=f"status_{t['id']}")
                    with col2:
                        edit_time = st.text_input("Cập nhật thời gian", value=t.get('time', ''), key=f"time_{t['id']}")
                    with col3:
                        st.write("") 
                        st.write("")
                        if st.button("Cập nhật", key=f"btn_{t['id']}"):
                            update_payload = {"status": edit_status, "time": edit_time}
                            ur = requests.put(f"{BACKEND_URL}/tasks/{t['id']}", json=update_payload, headers=headers)
                            if ur.status_code == 200:
                                st.success("Cập nhật thành công!")
                                st.rerun()
                            else:
                                st.error("Lỗi khi cập nhật")
    else:
        st.error("Lỗi khi lấy dữ liệu từ Backend.")