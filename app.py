import streamlit as st
import numpy as np
from logic import chuan_hoa_buoc_1_va_2, tao_chuoi_latex

st.title("Thuật toán Chuẩn hóa QHTT")

# Dữ liệu đầu vào
c_input = [3, -2]
A_input = [[1, 1], [2, -1]]
b_input = [4, -5] 
is_min = True     
dau_input = ['<=', '<=']

# Tự động tạo tên biến x_1, x_2 cho LaTeX
ten_bien_x = [f"x_{{{i+1}}}" for i in range(len(c_input))]

st.write("### 1. Đề bài gốc:")
st.latex(f"\\text{{{'Min' if is_min else 'Max'}}} \\quad Z = {tao_chuoi_latex(c_input, ten_bien_x)}")
for i in range(len(b_input)):
    # Đổi dấu <=, >= thành ký hiệu LaTeX chuẩn \le, \ge
    dau_latex = '\\le' if dau_input[i] == '<=' else '\\ge' if dau_input[i] == '>=' else '='
    st.latex(f"{tao_chuoi_latex(A_input[i], ten_bien_x)} {dau_latex} {b_input[i]}")

# Chạy thuật toán lõi
c_moi, A_moi, b_moi, dau_moi, giai_thich = chuan_hoa_buoc_1_va_2(
    c_input, A_input, b_input, is_min, dau_input
)

st.write("---")
st.write("### 2. Các bước xử lý tự động:")
for cau in giai_thich:
    st.info(cau)

st.write("### 3. Bài toán sau khi chuẩn hóa Bước 1 & 2:")
st.latex(f"\\text{{Max}} \\quad Z' = {tao_chuoi_latex(c_moi, ten_bien_x)}")
for i in range(len(b_moi)):
    dau_latex = '\\le' if dau_moi[i] == '<=' else '\\ge' if dau_moi[i] == '>=' else '='
    st.latex(f"{tao_chuoi_latex(A_moi[i], ten_bien_x)} {dau_latex} {int(b_moi[i]) if b_moi[i].is_integer() else b_moi[i]}")