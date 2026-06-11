import streamlit as st
from fractions import Fraction
import logic as l

# ─────────────────────────────────────────────
#  CẤU HÌNH TRANG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Giải QHTT – Phương pháp Từ Vựng",
    page_icon="📐",
)

# ─────────────────────────────────────────────
#  CSS TUỲ CHỈNH
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Nền & font chung ── */
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* ── Header chính ── */
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    border-left: 5px solid #e94560;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.main-header h1 {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: #a8b2d8;
    font-size: 0.9rem;
    margin: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.82rem !important;
    color: #8b949e !important;
}

/* ── Nhãn section sidebar ── */
.sidebar-section {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
}
.sidebar-section-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #e94560 !important;
    margin-bottom: 0.5rem;
}

/* ── Nút GIẢI ── */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #e94560, #c62a47);
    color: white !important;
    font-weight: 700;
    font-size: 1rem;
    border: none;
    border-radius: 10px;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 15px rgba(233,69,96,0.4);
    letter-spacing: 0.5px;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(233,69,96,0.5);
}

/* ── Card bước giải ── */
.step-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin: 0.75rem 0;
    transition: border-color 0.2s;
}
.step-card:hover { border-color: #58a6ff; }

.step-badge {
    display: inline-block;
    background: #1f6feb;
    color: white;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.step-badge.phase1  { background: #9e6a03; }
.step-badge.pivot   { background: #1f6feb; }
.step-badge.optimal { background: #1a7f37; }
.step-badge.init    { background: #6e40c9; }
.step-badge.dual    { background: #0e6ebd; }

/* ── Kết quả tối ưu ── */
.result-box {
    background: linear-gradient(135deg, #0d4429, #1a7f37);
    border: 1px solid #2ea043;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    text-align: center;
}
.result-box h2 {
    color: #3fb950;
    font-size: 1.3rem;
    margin: 0 0 0.75rem 0;
}
.result-value {
    color: #ffffff;
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.result-vars {
    color: #adbac7;
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

/* ── Hộp cảnh báo & lỗi ── */
.info-note {
    background: #1c2d3e;
    border-left: 4px solid #58a6ff;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.88rem;
    color: #adbac7;
}
.error-box {
    background: #2d0f0f;
    border-left: 4px solid #e94560;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    color: #ff7b7b;
    font-weight: 500;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* ── Ẩn footer Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  TIÊU ĐỀ TRANG
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📐 Giải Quy Hoạch Tuyến Tính</h1>
    <p>Phương pháp Từ Vựng (Chvátal) · Hỗ trợ Đơn Hình Gốc · Đơn Hình Đối Ngẫu · Hai Pha</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR – NHẬP DỮ LIỆU
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Cài đặt bài toán")
    st.markdown('<div class="sidebar-section-title">Kích thước</div>', unsafe_allow_html=True)

    col_n, col_m = st.columns(2)
    num_vars = col_n.number_input("Số biến (n)", min_value=1, max_value=10, value=2, step=1)
    num_cons = col_m.number_input("Số ràng buộc (m)", min_value=1, max_value=10, value=2, step=1)

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Hàm mục tiêu</div>', unsafe_allow_html=True)
    obj_type = st.radio("Loại", ["Min", "Max"], horizontal=True, label_visibility="collapsed")

    # Hàm mục tiêu – hiển thị dạng z = c1x1 + ...
    obj_label_parts = []
    c_in = []
    coef_cols = st.columns(min(num_vars, 4))
    for j in range(num_vars):
        col = coef_cols[j % len(coef_cols)]
        val = col.number_input(f"c_{j+1}", value=0.0, step=1.0, key=f"c{j}",
                               label_visibility="visible",
                               help=f"Hệ số của x_{j+1} trong hàm mục tiêu")
        c_in.append(val)
        sign = "+" if val >= 0 else ""
        obj_label_parts.append(f"{sign}{val:.4g}x_{j+1}")

    obj_display = f"z = {' '.join(obj_label_parts)}"
    st.caption(f"**{obj_type}** {obj_display}")

    st.markdown("---")
    st.markdown('<div class="sidebar-section-title">Ràng buộc</div>', unsafe_allow_html=True)

    A_in, b_in, dau_in = [], [], []
    for i in range(num_cons):
        st.markdown(f"**Ràng buộc {i+1}**")
        row_cols = st.columns(num_vars + 2)
        row = []
        for j in range(num_vars):
            v = row_cols[j].number_input(
                f"x{j+1}", value=0.0, step=1.0,
                key=f"A{i}{j}", label_visibility="visible"
            )
            row.append(v)
        dau = row_cols[num_vars].selectbox(
            "≤/≥/=", ["<=", ">=", "="],
            key=f"d{i}", label_visibility="collapsed"
        )
        val_b = row_cols[num_vars+1].number_input(
            "b", value=0.0, step=1.0,
            key=f"b{i}", label_visibility="visible"
        )
        A_in.append(row)
        b_in.append(val_b)
        dau_in.append(dau)

    st.markdown("---")
    solve_clicked = st.button("🚀  GIẢI BÀI TOÁN", use_container_width=True)

    # Hướng dẫn nhanh
    with st.expander("📖 Hướng dẫn"):
        st.markdown("""
        1. Chọn số biến và số ràng buộc  
        2. Nhập hệ số hàm mục tiêu  
        3. Nhập ma trận ràng buộc A, dấu và vế phải b  
        4. Nhấn **GIẢI BÀI TOÁN**  

        **Các trường hợp hỗ trợ:**  
        - Đơn hình gốc (b ≥ 0)  
        - Đơn hình đối ngẫu (c ≥ 0, b có thể âm)  
        - Hai pha (b âm và c có hệ số âm)
        """)


# ─────────────────────────────────────────────
#  KHU VỰC KẾT QUẢ
# ─────────────────────────────────────────────
if not solve_clicked:
    # Màn hình chờ
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #484f58;">
        <div style="font-size:4rem; margin-bottom:1rem;">📊</div>
        <h3 style="color:#8b949e; font-weight:500;">Nhập dữ liệu và nhấn <em>GIẢI BÀI TOÁN</em></h3>
        <p style="font-size:0.9rem;">Kết quả từng bước sẽ hiển thị tại đây</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  XỬ LÝ GIẢI
# ─────────────────────────────────────────────

def badge(label: str, kind: str = "pivot") -> str:
    return f'<div class="step-badge {kind}">{label}</div>'

def step_card(content_fn, badge_html: str):
    st.markdown(f'<div class="step-card">{badge_html}', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)

def note_html(text: str):
    st.markdown(f'<div class="info-note">ℹ️ {text}</div>', unsafe_allow_html=True)

def error_html(text: str):
    st.markdown(f'<div class="error-box">⚠️ {text}</div>', unsafe_allow_html=True)


with st.spinner("Đang giải bài toán…"):
    try:
        # ── 1. Chuẩn hoá đầu vào ──────────────────────────────
        c_std, A_std, b_std, notes = l.chuan_hoa_dau_vao(
            c_in, A_in, b_in, obj_type == "Min", dau_in
        )
        v, C, D, B = l.khoi_tao_tu_vung_phan_so(c_std, A_std, b_std)

        non_basic = [f"x_{{{j+1}}}" for j in range(num_vars)]
        basic     = [f"w_{{{i+1}}}" for i in range(len(b_std))]

        # ── Hiển thị từ vựng xuất phát ────────────────────────
        st.markdown("## 📋 Lời Giải Chi Tiết")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        with st.container():
            st.markdown(badge("Từ vựng xuất phát", "init"), unsafe_allow_html=True)
            for n in notes:
                note_html(n)
            st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic))

        # ── 2. Xác định phương pháp ────────────────────────────
        is_feasible    = all(x >= 0 for x in B)
        is_optimal_obj = all(x >= 0 for x in C)
        mode_dual      = (not is_feasible and is_optimal_obj)

        # ── 3. HAI PHA (nếu cần) ───────────────────────────────
        if not is_feasible and not is_optimal_obj:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔄 Hai Pha")
            note_html("Từ vựng không thỏa mãn cả tính khả thi lẫn tối ưu → Kích hoạt phương pháp Hai Pha.")

            # Pha 1
            v_d, C_d, D_p1, non_p1 = l.khoi_tao_pha_1(D, non_basic)
            j_in, i_out = l.buoc_xoay_khoi_tao_pha_1(B, non_p1)

            with st.container():
                st.markdown(badge("Pha 1 · Xoay khởi tạo x₀", "phase1"), unsafe_allow_html=True)
                st.latex(l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, j_in, i_out, True))

            v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                v_d, C_d, D_p1, B, basic, non_p1, j_in, i_out
            )

            it_p1 = 1
            while it_p1 < 30:
                st_p1, jin_p1, iout_p1 = l.tim_phan_tu_truc_don_hinh_goc(C_d, D_p1, B)
                if st_p1 != "PIVOT":
                    break
                with st.container():
                    st.markdown(badge(f"Pha 1 · Bước {it_p1}", "phase1"), unsafe_allow_html=True)
                    st.latex(l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, jin_p1, iout_p1, True))
                v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                    v_d, C_d, D_p1, B, basic, non_p1, jin_p1, iout_p1
                )
                it_p1 += 1

            if abs(float(v_d)) > 1e-9:
                error_html("Pha 1 kết thúc với z₀ ≠ 0 → Bài toán VÔ NGHIỆM (infeasible).")
                st.stop()

            v, C, D, non_basic = l.chuyen_sang_pha2(D_p1, B, basic, non_p1, c_std)

            with st.container():
                st.markdown(badge("Chuyển sang Pha 2", "init"), unsafe_allow_html=True)
                st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic))

            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Pha 2 – Đơn Hình Gốc")

        elif mode_dual:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔁 Đơn Hình Đối Ngẫu")
            note_html("Hệ số hàm mục tiêu ≥ 0 nhưng vế phải có giá trị âm → Áp dụng Đơn Hình Đối Ngẫu.")
        else:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ▶️ Đơn Hình Gốc")

        # ── 4. Vòng lặp đơn hình chính ────────────────────────
        it = 1
        while it <= 50:
            if mode_dual:
                status, j_in, i_out = l.tim_phan_tu_truc_doi_ngau(C, D, B)
            else:
                status, j_in, i_out = l.tim_phan_tu_truc_don_hinh_goc(C, D, B)

            if status in ("OPTIMAL", "FEASIBLE"):
                # ── Hiển thị kết quả tối ưu ──────────────────
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

                with st.container():
                    st.markdown(badge("✅ Tối ưu", "optimal"), unsafe_allow_html=True)
                    st.latex(l.tao_latex_tu_vung(v, C, D, B, basic, non_basic))

                res = l.trich_xuat_nghiem(B, basic, non_basic, num_vars)
                nghiem_str = ", ".join([f"x_{j+1} = {res[j]}" for j in range(len(res))])
                z_str = l.format_frac(v)

                st.markdown(f"""
                <div class="result-box">
                    <h2>🎯 Nghiệm Tối Ưu</h2>
                    <div class="result-value">z* = {z_str}</div>
                    <div class="result-vars">{nghiem_str}</div>
                </div>
                """, unsafe_allow_html=True)
                break

            elif status == "PIVOT":
                kind = "dual" if mode_dual else "pivot"
                label = f"Bước {it} · {'Đối ngẫu' if mode_dual else 'Đơn hình'}"

                with st.container():
                    st.markdown(badge(label, kind), unsafe_allow_html=True)
                    st.latex(l.tao_latex_tu_vung(
                        v, C, D, B, basic, non_basic, j_in, i_out, False, mode_dual
                    ))

                v, C, D, B, basic, non_basic = l.thuc_hien_phep_xoay(
                    v, C, D, B, basic, non_basic, j_in, i_out
                )
                it += 1

            else:
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                if status == "UNBOUNDED":
                    error_html("Bài toán KHÔNG GIỚI NỘI (unbounded) – hàm mục tiêu có thể tiến đến ±∞.")
                elif status == "INFEASIBLE":
                    error_html("Bài toán VÔ NGHIỆM (infeasible) – miền chấp nhận được rỗng.")
                else:
                    error_html(f"Kết thúc với trạng thái không xác định: {status}.")
                break
        else:
            error_html("Vượt quá 50 bước lặp – có thể xảy ra hiện tượng đạp (cycling).")

    except Exception as e:
        st.markdown(f'<div class="error-box">❌ Lỗi khi thực thi: <code>{e}</code></div>',
                    unsafe_allow_html=True)
        st.exception(e)