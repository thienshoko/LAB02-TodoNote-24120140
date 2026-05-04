# Lab 2: Application Programming Interface and Firebase Studio

## Thông tin sinh viên
- **Họ và tên:** Nguyễn Lê Hoàng Thiện
- **MSSV:** 24120140
- **Môn học:** Tư duy Tính toán

---

## Giới thiệu dự án
Dự án này là một ứng dụng **Todo App** được xây dựng nhằm thực hiện các yêu cầu của bài thực hành số 2. Ứng dụng cho phép người dùng quản lý công việc cá nhân với cấu trúc Frontend và Backend tách biệt rõ ràng:
- **Frontend:** Xây dựng bằng `Streamlit`.
- **Backend:** Xây dựng bằng `FastAPI`.
- **Database & Auth:** Tích hợp `Firebase Authentication` và `Cloud Firestore`.

---

## Cấu trúc thư mục
Dự án được tổ chức như sau:
lab2_todo/
├── backend/
│   ├── main.py
│   └── serviceAccountKey.json (Đã ẩn)
├── frontend/
│   └── app.py
├── requirements.txt
├── .gitignore
└── README.md

## Hướng dẫn cài đặt
Yêu cầu máy tính đã cài đặt Python.

Bước 1: Clone repository này về máy cục bộ.
Bước 2: Mở terminal tại thư mục gốc và chạy lệnh cài đặt thư viện:

pip install -r requirements.txt

## Hướng dẫn chạy ứng dụng
Sử dụng 2 cửa sổ Terminal riêng biệt để chạy song song Backend và Frontend.

1. Chạy Backend (FastAPI)
Di chuyển vào thư mục backend và khởi chạy server:

cd backend
uvicorn main:app --reload

Server Backend sẽ chạy tại địa chỉ: [http://127.0.0.1:8000](http://127.0.0.1:8000)

2. Chạy Frontend (Streamlit)
Di chuyển vào thư mục frontend và khởi chạy giao diện:

cd frontend
streamlit run app.py

Giao diện sẽ tự động mở trên trình duyệt tại: http://localhost:8501

## Các tính năng chính
1. Đăng nhập/Đăng xuất: Bảo mật với Firebase Authentication (Email/Password).

2. Thêm công việc: Cho phép nhập nội dung Task và Thời gian thực hiện.

3. Xem danh sách: Hiển thị danh sách công việc cá nhân được đồng bộ từ Firestore.

4. Hỗ trợ thay đổi trạng thái (pending, in-progress, completed) và chỉnh sửa thời gian trực tiếp trên giao diện.

Video Demo: 