import streamlit as st
import numpy as np
from logic import chuan_hoa_buoc_1_va_2

st.title("Thuật toán Chuẩn hóa QHTT")

# Giả lập một bài toán người dùng nhập vào: Min Z, có vế phải âm
c_input = [3, -2]
A_input = [[1, 1], [2, -1]]
b_input = [4, -5] # Vế phải thứ 2 bị âm
is_min = True     # Bài toán Min
dau_input = ['<=', '<=']

st.write("### 1. Đề bài gốc:")
st.write(f"- Hàm mục tiêu: {'Min' if is_min else 'Max'} Z = {c_input[0]}x1 + {c_input[1]}x2")
st.write(f"- Ràng buộc 1: {A_input[0][0]}x1 + {A_input[0][1]}x2 {dau_input[0]} {b_input[0]}")
st.write(f"- Ràng buộc 2: {A_input[1][0]}x1 + {A_input[1][1]}x2 {dau_input[1]} {b_input[1]}")

# Chạy thuật toán
c_moi, A_moi, b_moi, dau_moi, giai_thich = chuan_hoa_buoc_1_va_2(
    c_input, A_input, b_input, is_min, dau_input
)

st.write("---")
st.write("### 2. Các bước xử lý tự động:")
for cau in giai_thich:
    st.info(cau) # st.info giúp in ra dòng chữ có màu xanh nổi bật

st.write("### 3. Bài toán sau khi chuẩn hóa Bước 1 & 2:")
st.write(f"- Hàm mục tiêu: Max Z' = {c_moi[0]}x1 + {c_moi[1]}x2")
st.write(f"- Ràng buộc 1: {A_moi[0][0]}x1 + {A_moi[0][1]}x2 {dau_moi[0]} {b_moi[0]}")
st.write(f"- Ràng buộc 2: {A_moi[1][0]}x1 + {A_moi[1][1]}x2 {dau_moi[1]} {b_moi[1]}")