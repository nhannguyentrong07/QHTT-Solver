import streamlit as st
from fractions import Fraction
import logic as l

st.set_page_config(layout="wide", page_title="QHTT Chvátal Solver")
st.title("Chương trình Giải QHTT - Phương pháp Từ Vựng")

# --- SIDEBAR INPUT ---
st.sidebar.header("🛠️ Cài đặt Đề Bài")
num_vars = st.sidebar.number_input("Số biến (n)", 2, 10, 2)
num_cons = st.sidebar.number_input("Số ràng buộc (m)", 1, 10, 2)
obj_type = st.sidebar.selectbox("Hàm mục tiêu", ["Min", "Max"])

c_in = [st.sidebar.number_input(f"Hệ số x_{j+1}", value=0.0, step=1.0) for j in range(num_vars)]

A_in = []; b_in = []; dau_in = []
for i in range(num_cons):
    st.sidebar.write(f"**Ràng buộc {i+1}**")
    cols = st.sidebar.columns(num_vars + 2)
    row = [cols[j].number_input(f"x_{j+1}", value=0.0, key=f"A{i}{j}") for j in range(num_vars)]
    dau = cols[num_vars].selectbox("Dấu", ["<=", ">=", "="], key=f"d{i}")
    val_b = cols[num_vars+1].number_input("b", value=0.0, key=f"b{i}")
    A_in.append(row); b_in.append(val_b); dau_in.append(dau)

if st.sidebar.button("🚀 GIẢI BÀI TOÁN"):
    # 1. Chuẩn hóa
    c_std, A_std, b_std, notes = l.chuan_hoa_dau_vao(c_in, A_in, b_in, obj_type=="Min", dau_in)
    v, C, D, B = l.khoi_tao_tu_vung_phan_so(c_std, A_std, b_std)
    non_basic = [f"x_{{{j+1}}}" for j in range(num_vars)]
    basic = [f"w_{{{i+1}}}" for i in range(len(b_std))]
    
    st.write("### 1. Từ vựng xuất phát:")
    for n in notes: st.info(n)
    st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic))

    # 2. Định tuyến & Giải
    is_feasible = all(x >= 0 for x in B)
    is_optimal_obj = all(x >= 0 for x in C)

    if not is_feasible and not is_optimal_obj: # PHA 1
        st.error("Kích hoạt HAI PHA.")
        v_d, C_d, D_p1, non_p1 = l.khoi_tao_pha_1(D, non_basic)
        j_in, i_out = l.buoc_xoay_khoi_tao_pha_1(B, non_p1)
        st.write("**Xoay khởi tạo x0:**")
        st.latex(l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, j_in, i_out, True))
        v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(v_d, C_d, D_p1, B, basic, non_p1, j_in, i_out)
        while True:
            st, jin, iout = l.tim_phan_tu_truc_don_hinh_goc(C_d, D_p1, B)
            if st != "PIVOT": break
            st.write(f"**Xoay Pha 1:**")
            st.latex(l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, jin, iout, True))
            v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(v_d, C_d, D_p1, B, basic, non_p1, jin, iout)
        v, C, D, non_basic = l.chuyen_sang_pha2(D_p1, B, basic, non_p1, c_std)
        st.write("**Chuyển sang Pha 2:**")

    # Vòng lặp giải chính (Gốc hoặc Pha 2)
    mode_dual = (not is_feasible and is_optimal_obj)
    it = 1
    while it < 20:
        status, j_in, i_out = l.tim_phan_tu_truc_doi_ngau(C, D, B) if mode_dual else l.tim_phan_tu_truc_don_hinh_goc(C, D, B)
        if status == "OPTIMAL" or status == "FEASIBLE": 
            st.success("Tối ưu!"); st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic))
            res = l.trich_xuat_nghiem(B, basic, non_basic, num_vars)
            st.write(f"Nghiệm: $({', '.join(res)})$, $z^* = {l.format_frac(v)}$"); break
        if status == "PIVOT":
            st.write(f"**Bước {it}:**")
            st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic, j_in, i_out, False, mode_dual))
            v, C, D, B, basic, non_basic = l.thuc_hien_phep_xoay(v, C, D, B, basic, non_basic, j_in, i_out)
            it += 1
        else: st.error("Vô nghiệm/Không giới nội"); break