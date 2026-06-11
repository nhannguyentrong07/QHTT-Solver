import streamlit as st
from logic import khoi_tao_tu_vung_phan_so, tim_phan_tu_truc_don_hinh_goc, tao_latex_tu_vung_hien_tai, thuc_hien_phep_xoay, trich_xuat_nghiem

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# Giả lập Đề bài: Min z = -3x1 - 2x2, cần 2 bước xoay để ra kết quả
c_input = [-3, -2] 
A_input = [[1, 2], [3, 1]] 
b_input = [4, 12]
num_bien_goc = len(c_input)

non_basic = [f"x_{{{i+1}}}" for i in range(num_bien_goc)]
basic = [f"w_{{{i+1}}}" for i in range(len(b_input))]

v, C, D, B = khoi_tao_tu_vung_phan_so(c_input, A_input, b_input)

st.write("### 1. Từ vựng xuất phát:")
st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))
st.write("---")

# --- VÒNG LẶP ĐƠN HÌNH ---
iteration = 1
max_iter = 10 # Giới hạn 10 vòng để chống lỗi lặp vô hạn
status = "CONTINUE"

while iteration <= max_iter:
    status, j_in, i_out = tim_phan_tu_truc_don_hinh_goc(C, D, B)
    
    if status == "OPTIMAL":
        break
    elif status == "UNBOUNDED":
        st.error("Bài toán không giới nội, $z \\to -\\infty$ (hoặc $+\\infty$).")
        break
    elif status == "PIVOT":
        st.write(f"### 2.{iteration} Xoay đơn hình lần {iteration} (Biến vào ${non_basic[j_in]}$, biến ra ${basic[i_out]}$):")
        # In từ vựng trước khi xoay (có mũi tên, khung vuông, tỷ số)
        st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out))
        
        # Gọi hàm đại số để rút và thế
        v, C, D, B, basic, non_basic = thuc_hien_phep_xoay(
            v, C, D, B, basic, non_basic, j_in, i_out
        )
        iteration += 1

# --- KẾT LUẬN ---
if status == "OPTIMAL":
    st.write("### 3. Từ vựng Tối ưu:")
    # In ra bảng từ vựng cuối cùng không có dấu hiệu xoay
    st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))
    
    # Rút trích nghiệm chuẩn LaTeX theo quy tắc
    nghiem_str = ", ".join(trich_xuat_nghiem(B, basic, non_basic, num_bien_goc))
    bien_goc_str = ", ".join([f"x_{{{i+1}}}" for i in range(num_bien_goc)])
    
    st.success(f"Từ vựng tối ưu. Phương án tối ưu: $({bien_goc_str}) = ({nghiem_str})$. Giá trị tối ưu $z^* = {v}$")