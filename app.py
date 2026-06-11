import streamlit as st
from logic import khoi_tao_tu_vung_phan_so, tim_phan_tu_truc_don_hinh_goc, tao_latex_tu_vung_hien_tai

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# Giả lập Đề bài đã chuẩn hóa: Khả thi (b >= 0), dạng Min, cần 1 bước xoay
# Min z = -3x1 - 2x2
# w1 = 4 - 1x1 - 2x2
# w2 = 12 - 3x1 - 1x2
c_input = [-3, -2] 
A_input = [[1, 2], [3, 1]] 
b_input = [4, 12]

# Khởi tạo định danh biến
non_basic = ["x_1", "x_2"]
basic = ["w_1", "w_2"]

# Tiền xử lý thành Phân số
v, C, D, B = khoi_tao_tu_vung_phan_so(c_input, A_input, b_input)

st.write("### 1. Từ vựng xuất phát:")
st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))

# --- BƯỚC CHỌN PHẦN TỬ TRỤC ---
status, j_in, i_out = tim_phan_tu_truc_don_hinh_goc(C, D, B)

st.write("---")
if status == "PIVOT":
    st.write(f"### 2. Xoay đơn hình lần 1 (Biến vào ${non_basic[j_in]}$, biến ra ${basic[i_out]}$):")
    st.info(f"Hệ thống tự động quét hàm mục tiêu chọn {non_basic[j_in]} do có hệ số âm. Tỷ số ràng buộc nhỏ nhất dẫn đến việc đẩy {basic[i_out]} ra khỏi cơ sở.")
    
    # In lại từ vựng cũ với các mũi tên và khung đánh dấu
    st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out))
    
elif status == "OPTIMAL":
    st.success("Từ vựng tối ưu. Không cần thực hiện phép xoay.")
elif status == "UNBOUNDED":
    st.error("Bài toán không giới nội, $z \\to -\\infty$.")