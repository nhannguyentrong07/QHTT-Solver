import streamlit as st
from fractions import Fraction
from logic import (khoi_tao_tu_vung_phan_so, tao_latex_tu_vung_hien_tai,
                   tim_phan_tu_truc_don_hinh_goc, tim_phan_tu_truc_doi_ngau,
                   khoi_tao_pha_1, buoc_xoay_khoi_tao_pha_1)

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# Giả lập Đề bài "Khó": Có vế phải âm và hàm mục tiêu có hệ số âm
# Ví dụ: Min z = -2x1 - 3x2
# Ràng buộc: -x1 - x2 <= -4 (Vi phạm khả thi do b_1 = -4)
#            1x1 - 2x2 <= 2
c_input = [-2, -3]
A_input = [[-1, -1], [1, -2]]
b_input = [-4, 2]
num_bien_goc = len(c_input)

non_basic = [f"x_{{{i+1}}}" for i in range(num_bien_goc)]
basic = [f"w_{{{i+1}}}" for i in range(len(b_input))]

# Khởi tạo ma trận phân số
v, C, D, B = khoi_tao_tu_vung_phan_so(c_input, A_input, b_input)

st.write("### 1. Từ vựng xuất phát:")
st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))
st.write("---")

st.write("### 2. Bộ định tuyến thông minh (Smart Router):")

# Tự động chẩn đoán trạng thái bài toán
is_feasible = all(b >= Fraction(0) for b in B)
is_optimal_obj = all(c >= Fraction(0) for c in C)

if is_feasible:
    st.success("Trạng thái: Khả thi ($b_i \\ge 0$). \n\n👉 **Quyết định: Kích hoạt ĐƠN HÌNH GỐC (Primal Simplex).**")
    
elif is_optimal_obj and not is_feasible:
    st.warning("Trạng thái: Hàm mục tiêu tối ưu ($c_j \\ge 0$), nhưng vi phạm ràng buộc ($b_i < 0$). \n\n👉 **Quyết định: Kích hoạt ĐƠN HÌNH ĐỐI NGẪU (Dual Simplex).**")
    
else:
    st.error("Trạng thái: Không khả thi ($b_i < 0$) và chưa tối ưu ($c_j < 0$). \n\n👉 **Quyết định: Kích hoạt HAI PHA (Two-Phase Simplex).**")
    
    st.write("#### Khởi tạo Pha 1:")
    # Sửa lại thành delta = x_0
    st.info("Hệ thống nhận diện được lệnh: Tự động thêm biến giả tạo $x_0$ mang dấu cộng vào tất cả phương trình và thiết lập hàm mục tiêu phụ $\\delta = x_0$.")
    
    # Kích hoạt hàm tạo x_0 và hàm delta từ logic.py
    v_delta, C_delta, D_pha1, non_basic_pha1 = khoi_tao_pha_1(D, non_basic)
    
    # In ra Từ vựng Pha 1
    st.latex(tao_latex_tu_vung_hien_tai(v_delta, C_delta, D_pha1, B, basic, non_basic_pha1))
    
    # Máy tính tự động tìm bước xoay bắt buộc để phá thế vi phạm
    j_in, i_out = buoc_xoay_khoi_tao_pha_1(B, non_basic_pha1)
    st.write(f"**Phân tích thuật toán:** Để ép hệ thống về trạng thái khả thi, bắt buộc thực hiện một phép xoay đặc biệt. Đưa biến giả tạo $x_0$ vào cơ sở, đẩy biến ${basic[i_out]}$ (có vế phải âm nhất) ra khỏi cơ sở.")