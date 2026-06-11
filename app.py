import streamlit as st
from fractions import Fraction
from logic import (khoi_tao_tu_vung_phan_so, tao_latex_tu_vung_hien_tai,
                   tim_phan_tu_truc_don_hinh_goc, khoi_tao_pha_1, 
                   buoc_xoay_khoi_tao_pha_1, thuc_hien_phep_xoay, 
                   chuyen_tu_pha1_sang_pha2, trich_xuat_nghiem)

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# Đề bài: Min z = -2x1 - 3x2 | -x1 - x2 <= -4 | x1 - 2x2 <= 2
c_input = [-2, -3]
A_input = [[-1, -1], [1, -2]]
b_input = [-4, 2]
num_bien_goc = len(c_input)

non_basic = [f"x_{{{i+1}}}" for i in range(num_bien_goc)]
basic = [f"w_{{{i+1}}}" for i in range(len(b_input))]
v, C, D, B = khoi_tao_tu_vung_phan_so(c_input, A_input, b_input)

st.write("### 1. Từ vựng xuất phát:")
st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))

# --- BỘ ĐỊNH TUYẾN THÔNG MINH ---
is_feasible = all(b >= Fraction(0) for b in B)

if not is_feasible:
    st.error("Trạng thái: Không khả thi ($b_i < 0$). 👉 **Kích hoạt HAI PHA.**")
    st.write("---")
    st.write("### PHA 1: Tìm phương án khả thi")
    
    # 1. Khởi tạo Pha 1
    v_delta, C_delta, D_pha1, non_basic_pha1 = khoi_tao_pha_1(D, non_basic)
    st.latex(tao_latex_tu_vung_hien_tai(v_delta, C_delta, D_pha1, B, basic, non_basic_pha1))
    
    # 2. Xoay bắt buộc lần 1
    j_in, i_out = buoc_xoay_khoi_tao_pha_1(B, non_basic_pha1)
    st.write(f"**Xoay khởi tạo bắt buộc (Biến vào $x_0$, biến ra ${basic[i_out]}$):**")
    v_delta, C_delta, D_pha1, B, basic, non_basic_pha1 = thuc_hien_phep_xoay(
        v_delta, C_delta, D_pha1, B, basic, non_basic_pha1, j_in, i_out
    )
    
    # 3. Vòng lặp giải Pha 1
    iter_p1 = 1
    while True:
        status, j_in, i_out = tim_phan_tu_truc_don_hinh_goc(C_delta, D_pha1, B)
        if status == "OPTIMAL":
            st.success(f"Kết thúc Pha 1. $\\delta^* = {v_delta}$. Loại bỏ $x_0$.")
            break
        elif status == "PIVOT":
            st.write(f"**Xoay Pha 1 lần {iter_p1} (Biến vào ${non_basic_pha1[j_in]}$, biến ra ${basic[i_out]}$):**")
            st.latex(tao_latex_tu_vung_hien_tai(v_delta, C_delta, D_pha1, B, basic, non_basic_pha1, j_in, i_out))
            v_delta, C_delta, D_pha1, B, basic, non_basic_pha1 = thuc_hien_phep_xoay(
                v_delta, C_delta, D_pha1, B, basic, non_basic_pha1, j_in, i_out
            )
            iter_p1 += 1

    # Chuyển tiếp sang Pha 2
    st.write("---")
    st.write("### PHA 2: Tối ưu bài toán gốc")
    v, C, D, non_basic = chuyen_tu_pha1_sang_pha2(D_pha1, B, basic, non_basic_pha1, c_input)

# --- VÒNG LẶP PHA 2 (Hoặc Đơn hình gốc nếu đã khả thi từ đầu) ---
iter_p2 = 1
while True:
    status, j_in, i_out = tim_phan_tu_truc_don_hinh_goc(C, D, B)
    
    if status == "OPTIMAL":
        st.write("#### Từ vựng Tối ưu:")
        st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))
        nghiem_str = ", ".join(trich_xuat_nghiem(B, basic, non_basic, num_bien_goc))
        bien_goc_str = ", ".join([f"x_{{{i+1}}}" for i in range(num_bien_goc)])
        st.success(f"Phương án tối ưu: $({bien_goc_str}) = ({nghiem_str})$. Giá trị tối ưu $z^* = {v}$")
        break
        
    elif status == "UNBOUNDED":
        st.write("#### Từ vựng trước khi phát hiện lỗi:")
        st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in))
        st.error("Kết luận: Bài toán KHÔNG GIỚI NỘI (Unbounded). Cột biến vào toàn dấu cộng, $z \\to -\\infty$.")
        break
        
    elif status == "PIVOT":
        st.write(f"**Xoay Pha 2 lần {iter_p2} (Biến vào ${non_basic[j_in]}$, biến ra ${basic[i_out]}$):**")
        st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out))
        v, C, D, B, basic, non_basic = thuc_hien_phep_xoay(
            v, C, D, B, basic, non_basic, j_in, i_out
        )
        iter_p2 += 1