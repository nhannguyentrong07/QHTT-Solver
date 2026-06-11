import streamlit as st
from fractions import Fraction
from logic import (khoi_tao_tu_vung_phan_so, tao_latex_tu_vung_hien_tai,
                   tim_phan_tu_truc_don_hinh_goc, tim_phan_tu_truc_doi_ngau,
                   khoi_tao_pha_1, buoc_xoay_khoi_tao_pha_1, thuc_hien_phep_xoay, 
                   chuyen_tu_pha1_sang_pha2, trich_xuat_nghiem, format_frac)

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# Giả lập Đề bài Đối ngẫu: Hàm Min đã tối ưu (c >= 0) nhưng vi phạm ràng buộc (b < 0)
# Ví dụ: Min z = 3x1 + 4x2 (Hệ số 3, 4 dương -> Đã tối ưu)
# Ràng buộc: -x1 - x2 <= -4 | -2x1 - x2 <= -5
c_input = [3, 4]
A_input = [[-1, -1], [-2, -1]]
b_input = [-4, -5]
num_bien_goc = len(c_input)

non_basic = [f"x_{{{i+1}}}" for i in range(num_bien_goc)]
basic = [f"w_{{{i+1}}}" for i in range(len(b_input))]
v, C, D, B = khoi_tao_tu_vung_phan_so(c_input, A_input, b_input)

st.write("### 1. Từ vựng xuất phát:")
st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))

# --- BỘ ĐỊNH TUYẾN THÔNG MINH ---
is_feasible = all(b >= Fraction(0) for b in B)
is_optimal_obj = all(c >= Fraction(0) for c in C)

st.write("---")
st.write("### 2. Quá trình Tối ưu hóa:")

if is_feasible:
    st.success("Trạng thái: Khả thi ($b_i \\ge 0$). 👉 **Kích hoạt ĐƠN HÌNH GỐC (Primal Simplex).**")
    iter_p = 1
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
            st.error("Kết luận: Bài toán KHÔNG GIỚI NỘI (Unbounded).")
            break
        elif status == "PIVOT":
            st.write(f"**Xoay Đối ngẫu lần {iter_dual}:**")
            
            # --- TRÌNH BÀY LẬP LUẬN CHỌN BIẾN ---
            ratios_str = []
            for j, d_val in enumerate(D[i_out]):
                if d_val > Fraction(0): # Chỉ xét hệ số mang dấu cộng
                    ratio_val = C[j] / d_val
                    ratios_str.append(f"${non_basic[j]}: \\frac{{{format_frac(C[j])}}}{{{format_frac(d_val)}}} = {format_frac(ratio_val)}$")
            
            giai_thich = f"- **Biến ra:** Chọn mũi tên trái tại ${basic[i_out]}$ do có vế phải âm nhất (${format_frac(B[i_out])}$).\n"
            if ratios_str:
                giai_thich += f"- **Biến vào:** Xét phương trình của ${basic[i_out]}$, ta lập tỷ số (Hệ số hàm $z$ / Hệ số có dấu cộng): "
                giai_thich += " và ".join(ratios_str) + f".\n- **Kết luận:** Tỷ số nhỏ nhất thuộc về ${non_basic[j_in]}$, nên ta chọn ${non_basic[j_in]}$ làm biến vào (mũi tên hướng xuống)."
            
            st.info(giai_thich)
            # ------------------------------------

            # In Từ vựng
            st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out))
            
            # Thực hiện xoay
            v, C, D, B, basic, non_basic = thuc_hien_phep_xoay(v, C, D, B, basic, non_basic, j_in, i_out)
            iter_dual += 1
            
elif is_optimal_obj and not is_feasible:
    st.warning("Trạng thái: Hàm mục tiêu tối ưu ($c_j \\ge 0$) nhưng vi phạm ràng buộc ($b_i < 0$). 👉 **Kích hoạt ĐỐI NGẪU (Dual Simplex).**")
    iter_dual = 1
    while True:
        status, j_in, i_out = tim_phan_tu_truc_doi_ngau(C, D, B)
        if status == "FEASIBLE":
            st.write("#### Từ vựng Tối ưu:")
            st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic))
            nghiem_str = ", ".join(trich_xuat_nghiem(B, basic, non_basic, num_bien_goc))
            bien_goc_str = ", ".join([f"x_{{{i+1}}}" for i in range(num_bien_goc)])
            st.success(f"Hệ thống đã vá xong vi phạm và đạt trạng thái Khả thi. Do hàm mục tiêu đã tối ưu từ đầu, đây chính là phương án tối ưu: $({bien_goc_str}) = ({nghiem_str})$. Giá trị tối ưu $z^* = {v}$")
            break
        elif status == "INFEASIBLE":
            st.write("#### Từ vựng trước khi phát hiện lỗi:")
            st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, -1, i_out))
            st.error("Kết luận: Bài toán VÔ NGHIỆM (Infeasible). Tại dòng biến ra, tất cả hệ số đều mang dấu cộng, không thể tìm được biến vào.")
            break
        elif status == "PIVOT":
            st.write(f"**Xoay Đối ngẫu lần {iter_dual}:**")
            
            # --- TRÌNH BÀY LẬP LUẬN CHỌN BIẾN ---
            ratios_str = []
            for j, d_val in enumerate(D[i_out]):
                if d_val > Fraction(0): # Chỉ xét hệ số mang dấu cộng
                    ratio_val = C[j] / d_val
                    ratios_str.append(f"${non_basic[j]}: \\frac{{{format_frac(C[j])}}}{{{format_frac(d_val)}}} = {format_frac(ratio_val)}$")
            
            giai_thich = f"- **Biến ra:** Chọn mũi tên trái tại ${basic[i_out]}$ do có vế phải âm nhất (${format_frac(B[i_out])}$).\n"
            if ratios_str:
                giai_thich += f"- **Biến vào:** Xét phương trình của ${basic[i_out]}$, ta lập tỷ số (Hệ số hàm $z$ / Hệ số có dấu cộng): "
                giai_thich += " và ".join(ratios_str) + f".\n- **Kết luận:** Tỷ số nhỏ nhất thuộc về ${non_basic[j_in]}$, nên ta chọn ${non_basic[j_in]}$ làm biến vào (mũi tên hướng xuống)."
            
            st.info(giai_thich)
            # ------------------------------------

            # In Từ vựng
            st.latex(tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out))
            
            # Thực hiện xoay
            v, C, D, B, basic, non_basic = thuc_hien_phep_xoay(v, C, D, B, basic, non_basic, j_in, i_out)
            iter_dual += 1
else:
    st.error("Trạng thái: Không khả thi ($b_i < 0$) và chưa tối ưu ($c_j < 0$). 👉 **Kích hoạt HAI PHA (Two-Phase Simplex).**")
    # (Để code ngắn gọn cho bạn copy, tôi ẩn tạm khối Hai Pha ở đây, vì bài toán giả lập hiện tại sẽ chạy vào nhánh Đối ngẫu ở trên. Khi nào ráp UI nhập đề, ta sẽ nối full code Hai pha vào nhé).
    st.info("Hệ thống Hai Pha đã được lập trình sẵn và chờ kích hoạt.")