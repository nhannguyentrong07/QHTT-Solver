import streamlit as st
from logic import chuan_hoa_va_tao_tu_vung, tao_latex_tu_vung_xuat_phat

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# --- Giả lập Input Đề Bài ---
# Ví dụ: Max Z, có ràng buộc >= và = để test hệ thống phân giải
c_input = [3, 2]            # Hàm mục tiêu Max z = 3x1 + 2x2
A_input = [[1, 2], [1, -1], [2, 1]]
b_input = [4, 1, 6]
is_min = False              # Đang là Max
dau_input = ['<=', '>=', '=']

st.write("### 1. Đề bài gốc:")
st.latex(r"\text{Max} \quad Z = 3x_1 + 2x_2")
st.latex(r"1x_1 + 2x_2 \le 4")
st.latex(r"1x_1 - 1x_2 \ge 1")
st.latex(r"2x_1 + 1x_2 = 6")
st.latex(r"x_1, x_2 \ge 0")

# --- Xử lý Thuật toán ---
c_std, A_std, b_std, giai_thich, is_max = chuan_hoa_va_tao_tu_vung(
    c_input, A_input, b_input, is_min, dau_input
)

st.write("---")
st.write("### 2. Tiền xử lý Dạng chuẩn:")
for cau in giai_thich:
    st.info(cau)

st.write("---")
st.write("### 3. Từ vựng xuất phát (Initial Dictionary):")
st.write("Hệ thống tự động thêm các biến bù $w_i \ge 0$ để tạo hệ phương trình:")

# Gọi hàm tạo LaTeX
latex_tu_vung = tao_latex_tu_vung_xuat_phat(c_std, A_std, b_std, is_max)
st.latex(latex_tu_vung)

# Cảnh báo định tuyến (Smart Routing Trigger)
if any(val < 0 for val in b_std):
    st.warning("Hệ thống nhận diện: $b_i < 0$. Từ vựng xuất phát KHÔNG khả thi. Sẽ cần kích hoạt Phương pháp Hai Pha (Two-Phase) hoặc Đơn hình Đối ngẫu (Dual Simplex) ở bước tiếp theo.")
else:
    st.success("Hệ thống nhận diện: Từ vựng khả thi. Đủ điều kiện kích hoạt Đơn hình Gốc (Primal Simplex).")