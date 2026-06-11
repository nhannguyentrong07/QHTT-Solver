import streamlit as st
from fractions import Fraction
from logic import (khoi_tao_tu_vung_phan_so, tao_latex_tu_vung_hien_tai,
                   tim_phan_tu_truc_don_hinh_goc, tim_phan_tu_truc_doi_ngau,
                   khoi_tao_pha_1, buoc_xoay_khoi_tao_pha_1, thuc_hien_phep_xoay, 
                   chuyen_tu_pha1_sang_pha2, trich_xuat_nghiem, format_frac)

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải Quy hoạch Tuyến tính - Phương pháp Từ Vựng")

st.sidebar.header("🛠️ Cài đặt Đề Bài")

# Cấu hình số biến và số ràng buộc
num_vars = st.sidebar.number_input("Số lượng biến quyết định (n)", min_value=2, max_value=5, value=2, step=1)
num_constraints = st.sidebar.number_input("Số lượng ràng buộc (m)", min_value=1, max_value=5, value=2, step=1)

# Chọn loại hàm mục tiêu
obj_type = st.sidebar.selectbox("Hàm mục tiêu", ["Min", "Max"])
is_minimize = (obj_type == "Min")

st.sidebar.write("---")
st.sidebar.write("### 1. Hệ số hàm mục tiêu (c)")
c_input = []
for j in range(num_vars):
    val = st.sidebar.number_input(f"Hệ số x_{j+1}", value=float(j-2), step=1.0)
    c_input.append(val)

st.sidebar.write("---")
st.sidebar.write("### 2. Hệ số các ràng buộc (A, dấu, b)")
A_input = []
b_input = []
dau_input = []
st.sidebar.write("---")
st.sidebar.write("### 2. Hệ số các ràng buộc (A, dấu, b)")
A_input = []
b_input = []
dau_input = []

for i in range(num_constraints):
    st.sidebar.write(f"**Ràng buộc {i+1}:**")
    
    # Co giãn số cột linh hoạt theo số biến + 1 (dấu) + 1 (vế phải)
    cols = st.sidebar.columns(num_vars + 2)
    row_A = []
    
    # Nhập hệ số cho từng biến x_1 ... x_n
    for j in range(num_vars):
        with cols[j]:
            v_A = st.number_input(
                f"x_{j+1}", 
                value=float(1.0 if i == j else 0.0), 
                step=0.5, 
                key=f"A_{i}_{j}"
            )
        row_A.append(v_A)
        
    # Chọn dấu bất đẳng thức
    with cols[num_vars]:
        d = st.selectbox(
            "Dấu", 
            ["<=", ">=", "="], 
            key=f"dau_{i}"
        )
        
    # Nhập vế phải (b)
    with cols[num_vars + 1]:
        v_b = st.number_input(
            "Vế phải", 
            value=float(4.0 + i), 
            step=1.0, 
            key=f"b_{i}"
        )
        
    A_input.append(row_A)
    dau_input.append(d)
    b_input.append(v_b)

# Hiển thị đề bài vừa nhập
ten_bien_x = [f"x_{{{k+1}}}" for k in range(num_vars)]
st.write("### 📋 Đề bài của bạn:")

latex_obj_sign = "\\min" if is_minimize else "\\max"
latex_obj_terms = " + ".join([f"{c_input[k]:g}{ten_bien_x[k]}" for k in range(num_vars)])
st.latex(f"{latex_obj_sign} \\quad Z = {latex_obj_terms}")

for i in range(num_constraints):
    latex_A_terms = " + ".join([f"{A_input[i][k]:g}{ten_bien_x[k]}" for k in range(num_vars)])
    d_latex = '\\le' if dau_input[i] == '<=' else '\\ge' if dau_input[i] == '>=' else '='
    st.latex(f"{latex_A_terms} \\quad {d_latex} \\quad {b_input[i]:g}")

st.markdown("---")
st.write("### ⚙️ Tiến trình giải thuật toán Từ vựng (Chvátal)")

# Tạm thời khóa logic giải xuất ra để bạn test phần nhập liệu giao diện trước 
# (Sẽ mở khóa gọi hàm chuẩn hóa và chạy vòng lặp sau khi bạn xác nhận giao diện chạy mượt)
st.info("Giao diện đã thiết lập xong. Hãy nhập liệu ở thanh menu bên trái (Sidebar) để kiểm tra mô phỏng sinh công thức toán học.")