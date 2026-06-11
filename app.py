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
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* ═══ SIDEBAR – NỀN TRẮNG ═══ */
section[data-testid="stSidebar"] {
    background: #f8f9fb !important;
    border-right: 2px solid #e2e8f0;
}
section[data-testid="stSidebar"] > div { padding-top: 1rem; }

section[data-testid="stSidebar"] label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}

/* Ô số nổi bật */
section[data-testid="stSidebar"] input[type="number"] {
    background: #ffffff !important;
    color: #111827 !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 0.35rem 0.6rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
section[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
    outline: none !important;
}

/* Selectbox dấu */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #eef2ff !important;
    border: 2px solid #a5b4fc !important;
    border-radius: 8px !important;
    color: #3730a3 !important;
    font-weight: 700 !important;
}

/* Radio */
section[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem !important; }

/* Tiêu đề nhỏ */
.sb-title {
    font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.2px;
    color: #6366f1; margin: 0.2rem 0 0.5rem 0;
}

/* Preview hàm mục tiêu */
.obj-preview {
    background: #eef2ff; border: 1.5px solid #a5b4fc;
    border-radius: 8px; padding: 0.45rem 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem; font-weight: 600; color: #3730a3;
    margin: 0.4rem 0 0.2rem 0; word-break: break-all;
}

/* Card ràng buộc */
.con-label {
    font-size: 0.72rem; font-weight: 700;
    color: #6366f1; text-transform: uppercase;
    letter-spacing: 0.8px; margin: 0.6rem 0 0.2rem 0;
}

/* NÚT GIẢI */
div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important; font-weight: 700 !important;
    font-size: 1rem !important; border: none !important;
    border-radius: 10px !important; padding: 0.75rem !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(79,70,229,0.4) !important;
    transition: all 0.2s !important; margin-top: 0.3rem;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.5) !important;
}

/* ═══ VÙNG KẾT QUẢ ═══ */
.main-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #1e3a5f 60%, #0f3460 100%);
    border-radius: 14px; padding: 1.75rem 2.25rem;
    margin-bottom: 1.25rem; border-left: 5px solid #6366f1;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}
.main-header h1 { color:#fff; font-size:1.75rem; font-weight:700; margin:0 0 0.25rem; }
.main-header p  { color:#a5b4fc; font-size:0.88rem; margin:0; }

.step-badge {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    padding: 0.2rem 0.75rem; border-radius: 20px;
    margin-bottom: 0.55rem; text-transform: uppercase;
    letter-spacing: 0.6px; color: white;
}
.step-badge.init    { background: #7c3aed; }
.step-badge.pivot   { background: #2563eb; }
.step-badge.phase1  { background: #d97706; }
.step-badge.dual    { background: #0891b2; }
.step-badge.optimal { background: #16a34a; }

.step-card {
    background: #fafafa; border: 1.5px solid #e2e8f0;
    border-radius: 12px; padding: 1.1rem 1.4rem; margin: 0.6rem 0;
}
.step-card:hover { border-color: #6366f1; }

.result-box {
    background: linear-gradient(135deg, #052e16, #14532d);
    border: 1.5px solid #22c55e; border-radius: 14px;
    padding: 1.5rem 2rem; margin: 1rem 0; text-align: center;
}
.result-box h2 { color: #4ade80; font-size: 1.2rem; margin: 0 0 0.6rem; }
.result-value  { color: #fff; font-size: 1.7rem; font-weight: 700;
                 font-family: 'JetBrains Mono', monospace; }
.result-vars   { color: #86efac; font-size: 0.92rem; margin-top: 0.45rem; }

.info-note {
    background: #eff6ff; border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 0.55rem 1rem;
    margin: 0.35rem 0; font-size: 0.86rem; color: #1e40af;
}
.error-box {
    background: #fef2f2; border-left: 4px solid #ef4444;
    border-radius: 0 8px 8px 0; padding: 0.75rem 1rem;
    color: #b91c1c; font-weight: 600;
}
.section-divider { border:none; border-top:1.5px solid #e2e8f0; margin:1.25rem 0; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>📐 Giải Quy Hoạch Tuyến Tính</h1>
    <p>Phương pháp Từ Vựng (Chvátal) · Đơn Hình Gốc · Đơn Hình Đối Ngẫu · Hai Pha</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CHUẨN HOÁ ĐẦU VÀO  (logic không có hàm này → làm tại đây)
# ─────────────────────────────────────────────
def chuan_hoa_dau_vao(c_in, A_in, b_in, is_min, dau_in):
    """
    Chuyển bài toán về dạng chuẩn Minimize z = c^T x, Ax <= b, b >= 0:
    - Max → Min: nhân c với -1
    - '>=' → '<=': nhân cả hai vế với -1
    - '='  → '<=': giữ nguyên một dòng (thêm 2 dòng nếu muốn chặt, ở đây dùng 1 dòng =)
    Trả về (c_std, A_std, b_std, ghi_chu[])
    """
    notes = []
    n = len(c_in)

    # Bước 1: Max → Min
    if not is_min:
        c_std = [-v for v in c_in]
        notes.append("Đổi Max → Min: nhân hàm mục tiêu với −1.")
    else:
        c_std = list(c_in)

    A_std = []
    b_std = []

    for i, (row, dau, bi) in enumerate(zip(A_in, dau_in, b_in)):
        if dau == "<=":
            A_std.append(list(row))
            b_std.append(bi)
        elif dau == ">=":
            A_std.append([-v for v in row])
            b_std.append(-bi)
            notes.append(f"Ràng buộc {i+1}: '≥' → nhân −1 để đổi thành '≤'.")
        else:  # "="
            # Đưa ràng buộc bằng vào như <=  (sẽ được xử lý bằng dual hoặc hai pha)
            A_std.append(list(row))
            b_std.append(bi)
            notes.append(f"Ràng buộc {i+1}: '=' giữ nguyên (xử lý như ≤ trong từ vựng).")

    return c_std, A_std, b_std, notes


# ─────────────────────────────────────────────
#  SIDEBAR – NHẬP DỮ LIỆU
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-title">📏 Kích thước</div>', unsafe_allow_html=True)
    col_n, col_m = st.columns(2)
    num_vars = col_n.number_input("Số biến (n)", 1, 10, 2, step=1)
    num_cons = col_m.number_input("Số ràng buộc (m)", 1, 10, 2, step=1)

    st.markdown("---")
    st.markdown('<div class="sb-title">🎯 Hàm mục tiêu</div>', unsafe_allow_html=True)
    obj_type = st.radio("Loại", ["Min", "Max"], horizontal=True, label_visibility="collapsed")

    c_in = []
    coef_cols = st.columns(min(num_vars, 4))
    for j in range(num_vars):
        val = coef_cols[j % len(coef_cols)].number_input(
            f"c_{j+1}", value=0.0, step=1.0, key=f"c{j}"
        )
        c_in.append(val)

    # Preview hàm mục tiêu
    parts = []
    for j, v in enumerate(c_in):
        sg = "+" if v >= 0 else ""
        parts.append(f"{sg}{v:g}·x<sub>{j+1}</sub>")
    st.markdown(
        f'<div class="obj-preview">{obj_type} z = {" ".join(parts)}</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown('<div class="sb-title">📋 Ràng buộc</div>', unsafe_allow_html=True)

    A_in, b_in, dau_in = [], [], []
    for i in range(num_cons):
        st.markdown(f'<div class="con-label">Ràng buộc {i+1}</div>', unsafe_allow_html=True)
        row_cols = st.columns(num_vars + 2)
        row = []
        for j in range(num_vars):
            v2 = row_cols[j].number_input(
                f"x{j+1}", value=0.0, step=1.0, key=f"A{i}{j}",
                label_visibility="visible"
            )
            row.append(v2)
        dau = row_cols[num_vars].selectbox(
            "≤≥=", ["<=", ">=", "="], key=f"d{i}", label_visibility="collapsed"
        )
        val_b = row_cols[num_vars+1].number_input(
            "b", value=0.0, step=1.0, key=f"b{i}", label_visibility="visible"
        )
        A_in.append(row)
        b_in.append(val_b)
        dau_in.append(dau)

    st.markdown("---")
    solve_clicked = st.button("🚀  GIẢI BÀI TOÁN", use_container_width=True)

    with st.expander("📖 Hướng dẫn"):
        st.markdown("""
**Các bước:**
1. Chọn số biến & ràng buộc
2. Chọn Min / Max
3. Nhập hệ số hàm mục tiêu
4. Nhập ma trận A, dấu, vế phải b
5. Nhấn **GIẢI BÀI TOÁN**

**Hỗ trợ tự động:**
- Đơn hình gốc (b ≥ 0)
- Đối ngẫu (c ≥ 0, tồn tại b < 0)
- Hai pha (cả hai vi phạm)
- Max tự chuyển về Min
        """)

# ─────────────────────────────────────────────
#  MÀN HÌNH CHỜ
# ─────────────────────────────────────────────
if not solve_clicked:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#94a3b8;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">📊</div>
        <h3 style="color:#64748b;font-weight:500;">Nhập dữ liệu và nhấn <em>GIẢI BÀI TOÁN</em></h3>
        <p style="font-size:0.88rem;">Lời giải từng bước sẽ xuất hiện tại đây</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def badge(label, kind="pivot"):
    return f'<span class="step-badge {kind}">{label}</span>'

def note_html(text):
    st.markdown(f'<div class="info-note">ℹ️ {text}</div>', unsafe_allow_html=True)

def error_html(text):
    st.markdown(f'<div class="error-box">⚠️ {text}</div>', unsafe_allow_html=True)

def show_step(badge_html, latex_str):
    """Hiện badge + bảng từ vựng LaTeX trong một card"""
    st.markdown(f'<div class="step-card">{badge_html}', unsafe_allow_html=True)
    st.latex(latex_str)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  GIẢI BÀI TOÁN
# ─────────────────────────────────────────────
with st.spinner("Đang giải bài toán…"):
    try:
        # ── 1. Chuẩn hoá ─────────────────────────────────────
        c_std, A_std, b_std, notes = chuan_hoa_dau_vao(
            c_in, A_in, b_in, obj_type == "Min", dau_in
        )

        # ── 2. Khởi tạo từ vựng phân số ──────────────────────
        v, C, D, B = l.khoi_tao_tu_vung_phan_so(c_std, A_std, b_std)
        non_basic = [f"x_{{{j+1}}}" for j in range(num_vars)]
        basic     = [f"w_{{{i+1}}}" for i in range(len(b_std))]

        # ── 3. Tiêu đề kết quả ────────────────────────────────
        st.markdown("## 📋 Lời Giải Chi Tiết")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # Ghi chú chuẩn hoá
        for n in notes:
            note_html(n)

        # Từ vựng xuất phát
        show_step(
            badge("Từ vựng xuất phát", "init"),
            l.tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic)
        )

        # ── 4. Phân loại phương pháp ──────────────────────────
        is_feasible    = all(x >= 0 for x in B)
        is_optimal_obj = all(x >= 0 for x in C)
        mode_dual      = (not is_feasible and is_optimal_obj)

        # ════════════════════════════════════════
        #  HAI PHA
        # ════════════════════════════════════════
        if not is_feasible and not is_optimal_obj:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔄 Phương Pháp Hai Pha")
            note_html("Từ vựng vi phạm cả tính khả thi lẫn tính tối ưu → Kích hoạt Hai Pha.")

            # --- Khởi tạo Pha 1 ---
            v_d, C_d, D_p1, non_p1 = l.khoi_tao_pha_1(D, non_basic)
            j_in_init, i_out_init   = l.buoc_xoay_khoi_tao_pha_1(B, non_p1)

            show_step(
                badge("Pha 1 · Xoay khởi tạo x₀", "phase1"),
                l.tao_latex_tu_vung_hien_tai(v_d, C_d, D_p1, B, basic, non_p1,
                                             j_in_init, i_out_init)
            )
            v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                v_d, C_d, D_p1, B, basic, non_p1, j_in_init, i_out_init
            )

            # --- Lặp Pha 1 ---
            it_p1 = 1
            while it_p1 <= 30:
                st_p1, jin_p1, iout_p1 = l.tim_phan_tu_truc_don_hinh_goc(C_d, D_p1, B)
                if st_p1 != "PIVOT":
                    break
                show_step(
                    badge(f"Pha 1 · Bước {it_p1}", "phase1"),
                    l.tao_latex_tu_vung_hien_tai(v_d, C_d, D_p1, B, basic, non_p1,
                                                 jin_p1, iout_p1)
                )
                v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                    v_d, C_d, D_p1, B, basic, non_p1, jin_p1, iout_p1
                )
                it_p1 += 1

            # Kiểm tra z₀ = 0
            if abs(float(v_d)) > 1e-9:
                error_html(f"Pha 1 kết thúc với z₀ = {l.format_frac(v_d)} ≠ 0 "
                           "→ Bài toán VÔ NGHIỆM (infeasible).")
                st.stop()

            # --- Chuyển sang Pha 2 ---
            v, C, D, non_basic = l.chuyen_tu_pha1_sang_pha2(
                D_p1, B, basic, non_p1, c_std
            )
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Pha 2 – Đơn Hình Gốc")
            show_step(
                badge("Từ vựng đầu Pha 2", "init"),
                l.tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic)
            )
            mode_dual = False  # Pha 2 dùng đơn hình gốc

        # ════════════════════════════════════════
        #  ĐƠN HÌNH ĐỐI NGẪU
        # ════════════════════════════════════════
        elif mode_dual:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔁 Đơn Hình Đối Ngẫu")
            note_html("Tất cả hệ số hàm mục tiêu ≥ 0, nhưng tồn tại b < 0 "
                      "→ Áp dụng Đơn Hình Đối Ngẫu.")

        # ════════════════════════════════════════
        #  ĐƠN HÌNH GỐC
        # ════════════════════════════════════════
        else:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ▶️ Đơn Hình Gốc")

        # ════════════════════════════════════════
        #  VÒNG LẶP CHÍNH
        # ════════════════════════════════════════
        it = 1
        while it <= 50:
            if mode_dual:
                status, j_in, i_out = l.tim_phan_tu_truc_doi_ngau(C, D, B)
                # Khi đối ngẫu trả về FEASIBLE → chuyển sang đơn hình gốc
                if status == "FEASIBLE":
                    mode_dual = False
                    note_html("Từ vựng đã khả thi → chuyển sang Đơn Hình Gốc.")
                    continue
            else:
                status, j_in, i_out = l.tim_phan_tu_truc_don_hinh_goc(C, D, B)

            # ── Tối ưu ───────────────────────────────────────
            if status == "OPTIMAL":
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                show_step(
                    badge("✅ Tối ưu", "optimal"),
                    l.tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic)
                )
                res   = l.trich_xuat_nghiem(B, basic, non_basic, num_vars)
                z_val = l.format_frac(v)

                # Nếu bài toán gốc là Max → đảo dấu z để in ra
                if obj_type == "Max":
                    z_display = l.format_frac(-v)
                    note_html("Bài toán gốc là Max: z* = −(z_min*)")
                else:
                    z_display = z_val

                vars_html = ",&nbsp; ".join(
                    [f"x<sub>{j+1}</sub> = {res[j]}" for j in range(len(res))]
                )
                st.markdown(f"""
                <div class="result-box">
                    <h2>🎯 Nghiệm Tối Ưu Tìm Được</h2>
                    <div class="result-value">z* = {z_display}</div>
                    <div class="result-vars">{vars_html}</div>
                </div>
                """, unsafe_allow_html=True)
                break

            # ── Xoay ─────────────────────────────────────────
            elif status == "PIVOT":
                kind  = "dual" if mode_dual else "pivot"
                label = f"Bước {it} · {'Đối ngẫu' if mode_dual else 'Đơn hình gốc'}"
                show_step(
                    badge(label, kind),
                    l.tao_latex_tu_vung_hien_tai(v, C, D, B, basic, non_basic, j_in, i_out)
                )
                v, C, D, B, basic, non_basic = l.thuc_hien_phep_xoay(
                    v, C, D, B, basic, non_basic, j_in, i_out
                )
                it += 1

            # ── Vô nghiệm / Không giới nội ────────────────────
            else:
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                if status == "UNBOUNDED":
                    error_html("Bài toán KHÔNG GIỚI NỘI (unbounded) — "
                               "hàm mục tiêu có thể tiến đến ±∞.")
                elif status == "INFEASIBLE":
                    error_html("Bài toán VÔ NGHIỆM (infeasible) — "
                               "miền chấp nhận được rỗng.")
                else:
                    error_html(f"Trạng thái không xác định: <code>{status}</code>.")
                break
        else:
            error_html("Vượt quá 50 bước lặp — có thể xảy ra hiện tượng đạp (cycling).")

    except Exception as e:
        error_html(f"Lỗi: <code>{e}</code>")
        with st.expander("Chi tiết lỗi kỹ thuật"):
            st.exception(e)