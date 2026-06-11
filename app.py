import streamlit as st
from fractions import Fraction
import logic as l

# ══════════════════════════════════════════════════
#  CẤU HÌNH TRANG
# ══════════════════════════════════════════════════
st.set_page_config(layout="wide", page_title="Giải QHTT – Từ Vựng", page_icon="📐")

# ══════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* ─── SIDEBAR trắng sáng ─── */
section[data-testid="stSidebar"] { background:#f8f9fb !important; border-right:2px solid #e2e8f0; }
section[data-testid="stSidebar"] > div { padding-top:.8rem; }
section[data-testid="stSidebar"] label { color:#374151 !important; font-weight:600 !important; font-size:.81rem !important; }

/* Ô số nổi bật */
section[data-testid="stSidebar"] input[type="number"] {
    background:#fff !important; color:#111827 !important;
    border:2px solid #cbd5e1 !important; border-radius:8px !important;
    font-weight:700 !important; font-size:.97rem !important;
    font-family:'JetBrains Mono',monospace !important;
    padding:.3rem .55rem !important; transition:border-color .2s,box-shadow .2s;
}
section[data-testid="stSidebar"] input[type="number"]:focus {
    border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,.18) !important; outline:none !important;
}

/* Selectbox dấu & điều kiện */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background:#eef2ff !important; border:2px solid #a5b4fc !important;
    border-radius:8px !important; color:#3730a3 !important; font-weight:700 !important;
}

/* Radio */
section[data-testid="stSidebar"] .stRadio label { font-size:.9rem !important; }

/* Tiêu đề nhỏ sidebar */
.sb-title { font-size:.69rem; font-weight:700; text-transform:uppercase;
            letter-spacing:1.2px; color:#6366f1; margin:.15rem 0 .45rem 0; }

/* Preview mục tiêu */
.obj-preview { background:#eef2ff; border:1.5px solid #a5b4fc; border-radius:8px;
               padding:.42rem .75rem; font-family:'JetBrains Mono',monospace;
               font-size:.84rem; font-weight:600; color:#3730a3;
               margin:.35rem 0 .15rem 0; word-break:break-all; }

/* Label ràng buộc */
.con-label { font-size:.7rem; font-weight:700; color:#6366f1;
             text-transform:uppercase; letter-spacing:.8px; margin:.55rem 0 .2rem 0; }

/* Nút GIẢI */
div[data-testid="stSidebar"] .stButton > button {
    width:100%; background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    color:white !important; font-weight:700 !important; font-size:1rem !important;
    border:none !important; border-radius:10px !important; padding:.72rem !important;
    box-shadow:0 4px 14px rgba(79,70,229,.4) !important; transition:all .2s !important; margin-top:.3rem;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    transform:translateY(-2px) !important; box-shadow:0 6px 20px rgba(79,70,229,.5) !important;
}

/* ─── MAIN HEADER ─── */
.main-header { background:linear-gradient(135deg,#1e1b4b 0%,#1e3a5f 60%,#0f3460 100%);
               border-radius:14px; padding:1.6rem 2.2rem; margin-bottom:1.2rem;
               border-left:5px solid #6366f1; box-shadow:0 8px 30px rgba(0,0,0,.2); }
.main-header h1 { color:#fff; font-size:1.7rem; font-weight:700; margin:0 0 .22rem; }
.main-header p  { color:#a5b4fc; font-size:.87rem; margin:0; }

/* ─── Khung đề bài ─── */
.problem-box { background:#fff; border:2px solid #6366f1; border-radius:14px;
               padding:1.4rem 1.8rem; margin:1rem 0 1.2rem 0;
               box-shadow:0 2px 16px rgba(99,102,241,.1); }
.problem-box h3 { color:#4338ca; font-size:1rem; font-weight:700;
                  margin:0 0 .75rem 0; letter-spacing:.3px; }
.problem-line { font-size:.96rem; color:#1e1b4b; margin:.28rem 0;
                font-family:'JetBrains Mono',monospace; }
.problem-divider { border:none; border-top:1.5px dashed #c7d2fe; margin:.65rem 0; }

/* ─── Bước giải ─── */
.step-badge { display:inline-block; font-size:.69rem; font-weight:700;
              padding:.18rem .7rem; border-radius:20px; margin-bottom:.5rem;
              text-transform:uppercase; letter-spacing:.6px; color:white; }
.step-badge.init    { background:#7c3aed; }
.step-badge.pivot   { background:#2563eb; }
.step-badge.phase1  { background:#d97706; }
.step-badge.dual    { background:#0891b2; }
.step-badge.optimal { background:#16a34a; }

.step-card { background:#fafafa; border:1.5px solid #e2e8f0; border-radius:12px;
             padding:1rem 1.35rem; margin:.55rem 0; }
.step-card:hover { border-color:#6366f1; }

/* ─── Kết quả ─── */
.result-box { background:linear-gradient(135deg,#052e16,#14532d);
              border:1.5px solid #22c55e; border-radius:14px;
              padding:1.4rem 2rem; margin:.9rem 0; text-align:center; }
.result-box h2 { color:#4ade80; font-size:1.15rem; margin:0 0 .55rem; }
.result-value  { color:#fff; font-size:1.65rem; font-weight:700;
                 font-family:'JetBrains Mono',monospace; }
.result-vars   { color:#86efac; font-size:.9rem; margin-top:.42rem; }

/* ─── Ghi chú & lỗi ─── */
.info-note { background:#eff6ff; border-left:4px solid #3b82f6; border-radius:0 8px 8px 0;
             padding:.5rem 1rem; margin:.3rem 0; font-size:.85rem; color:#1e40af; }
.error-box { background:#fef2f2; border-left:4px solid #ef4444; border-radius:0 8px 8px 0;
             padding:.7rem 1rem; color:#b91c1c; font-weight:600; }
.section-divider { border:none; border-top:1.5px solid #e2e8f0; margin:1.2rem 0; }

#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <h1>📐 Giải Quy Hoạch Tuyến Tính</h1>
    <p>Phương pháp Từ Vựng (Chvátal) · Đơn Hình Gốc · Đơn Hình Đối Ngẫu · Hai Pha</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
#  HÀM TIỆN ÍCH: ĐỊNH DẠNG SỐ CHO ĐỀ BÀI
# ══════════════════════════════════════════════════
def fmt(val):
    return f"{val:g}"

def build_linear_expr(coeffs, var_names, show_zero=False):
    terms = []
    for c, var in zip(coeffs, var_names):
        if c == 0 and not show_zero: continue
        abs_c = abs(c)
        coef_str = "" if abs_c == 1 else fmt(abs_c)
        if not terms: 
            sign = "-" if c < 0 else ""
            terms.append(f"{sign}{coef_str}{var}")
        else:
            sign = " - " if c < 0 else " + "
            terms.append(f"{sign}{coef_str}{var}")
    return "".join(terms) if terms else "0"

def buoc_xoay_khoi_tao_pha_1(B, non_p1):
    """Hàm bổ trợ an toàn để đảm bảo lấy x_0 làm phần tử trục cho Pha 1"""
    j_in = len(non_p1) - 1 
    min_b = Fraction(0)
    i_out = -1
    for i, b_val in enumerate(B):
        if b_val < min_b:
            min_b = b_val
            i_out = i
    return j_in, i_out

# ══════════════════════════════════════════════════
#  CHUẨN HOÁ ĐẦU VÀO
# ══════════════════════════════════════════════════
def chuan_hoa_dau_vao(c_in, A_in, b_in, is_min, dau_in, var_cond):
    notes = []
    n = len(c_in)
    c_exp   = [] 
    A_exp   = [[] for _ in range(len(A_in))]
    names   = [] 

    for j in range(n):
        cond = var_cond[j]
        if cond == "≥ 0":
            c_exp.append(c_in[j])
            for i in range(len(A_in)): A_exp[i].append(A_in[i][j])
            names.append(f"x_{{{j+1}}}")
        elif cond == "≤ 0":
            c_exp.append(-c_in[j])
            for i in range(len(A_in)): A_exp[i].append(-A_in[i][j])
            names.append(f"x_{{{j+1}}}'")
            notes.append(f"x_{j+1} ≤ 0 → đặt x_{j+1} = −x_{j+1}′ (x_{j+1}′ ≥ 0).")
        else:
            c_exp.append( c_in[j])
            c_exp.append(-c_in[j])
            for i in range(len(A_in)):
                A_exp[i].append( A_in[i][j])
                A_exp[i].append(-A_in[i][j])
            names.append(f"x_{{{j+1}}}^+")
            names.append(f"x_{{{j+1}}}^-")
            notes.append(f"x_{j+1} tự do → đặt x_{j+1} = x_{j+1}⁺ − x_{j+1}⁻.")

    if not is_min:
        c_std = [-v for v in c_exp]
        notes.append("Đổi Max → Min: nhân hàm mục tiêu với −1.")
    else:
        c_std = list(c_exp)

    A_std, b_std = [], []
    for i, (row, dau, bi) in enumerate(zip(A_exp, dau_in, b_in)):
        if dau == "<=":
            A_std.append(list(row)); b_std.append(bi)
        elif dau == ">=":
            A_std.append([-v for v in row]); b_std.append(-bi)
            notes.append(f"Ràng buộc {i+1}: '≥' → nhân −1 để thành '≤'.")
        else:
            A_std.append(list(row)); b_std.append(bi)
            notes.append(f"Ràng buộc {i+1}: '=' — xử lý trong từ vựng.")
    return c_std, A_std, b_std, notes, names

# ══════════════════════════════════════════════════
#  HIỂN THỊ ĐỀ BÀI (LaTeX)
# ══════════════════════════════════════════════════
def hien_thi_de_bai(obj_type, c_in, A_in, b_in, dau_in, var_cond, num_vars):
    var_names_tex = [f"x_{{{j+1}}}" for j in range(num_vars)]
    obj_expr = build_linear_expr(c_in, var_names_tex)
    obj_line = rf"{obj_type}\; z = {obj_expr}"
    con_lines = []
    dau_map = {"<=": r"\leq", ">=": r"\geq", "=": "="}
    for i, (row, dau, bi) in enumerate(zip(A_in, dau_in, b_in)):
        lhs = build_linear_expr(row, var_names_tex)
        con_lines.append(rf"{lhs} & {dau_map[dau]} & {fmt(bi)}")
    groups = {"≥ 0": [], "≤ 0": [], "Tự do": []}
    for j, cond in enumerate(var_cond):
        groups[cond].append(f"x_{{{j+1}}}")
    cond_lines = []
    if groups["≥ 0"]: cond_lines.append(", ".join(groups["≥ 0"]) + r" \geq 0")
    if groups["≤ 0"]: cond_lines.append(", ".join(groups["≤ 0"]) + r" \leq 0")
    if groups["Tự do"]: cond_lines.append(", ".join(groups["Tự do"]) + r"\; \text{tự do}")
    rows_tex = " \\\\ ".join(con_lines)
    cond_tex = " \\\\ ".join(cond_lines) if cond_lines else ""
    latex = (r"\begin{aligned}" rf"& {obj_line} \\" r"& \text{s.t.} \begin{cases}" + rows_tex + r"\end{cases} \\")
    if cond_tex: latex += rf"& {cond_tex}"
    latex += r"\end{aligned}"
    return latex

# ══════════════════════════════════════════════════
#  SIDEBAR – NHẬP DỮ LIỆU
# ══════════════════════════════════════════════════
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
        val = coef_cols[j % len(coef_cols)].number_input(f"c_{j+1}", value=0.0, step=1.0, key=f"c{j}")
        c_in.append(val)

    var_names_prev = [f"x<sub>{j+1}</sub>" for j in range(num_vars)]
    parts = []
    for j, v in enumerate(c_in):
        if v == 0: continue
        sg = "+" if (v > 0 and parts) else ("-" if v < 0 else "")
        abs_v = abs(v)
        coef = "" if abs_v == 1 else f"{abs_v:g}"
        parts.append(f"{sg}{coef}{var_names_prev[j]}")
    preview_expr = "".join(parts) if parts else "0"
    st.markdown(f'<div class="obj-preview">{obj_type} z = {preview_expr}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="sb-title">🔒 Điều kiện biến</div>', unsafe_allow_html=True)
    var_cond = []
    cond_cols = st.columns(min(num_vars, 3))
    for j in range(num_vars):
        cond = cond_cols[j % len(cond_cols)].selectbox(f"x_{j+1}", ["≥ 0", "≤ 0", "Tự do"], key=f"cond{j}", index=0)
        var_cond.append(cond)

    st.markdown("---")
    st.markdown('<div class="sb-title">📋 Ràng buộc</div>', unsafe_allow_html=True)
    A_in, b_in, dau_in = [], [], []
    for i in range(num_cons):
        st.markdown(f'<div class="con-label">Ràng buộc {i+1}</div>', unsafe_allow_html=True)
        row_cols = st.columns(num_vars + 2)
        row = []
        for j in range(num_vars):
            v2 = row_cols[j].number_input(f"x{j+1}", value=0.0, step=1.0, key=f"A{i}{j}", label_visibility="visible")
            row.append(v2)
        dau = row_cols[num_vars].selectbox("dấu", ["<=", ">=", "="], key=f"d{i}", label_visibility="collapsed")
        val_b = row_cols[num_vars+1].number_input("b", value=0.0, step=1.0, key=f"b{i}", label_visibility="visible")
        A_in.append(row); b_in.append(val_b); dau_in.append(dau)

    st.markdown("---")
    solve_clicked = st.button("🚀  GIẢI BÀI TOÁN", use_container_width=True)

# ══════════════════════════════════════════════════
#  MÀN HÌNH CHỜ
# ══════════════════════════════════════════════════
if not solve_clicked:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#94a3b8;">
        <div style="font-size:3.5rem;margin-bottom:1rem;">📊</div>
        <h3 style="color:#64748b;font-weight:500;">Nhập dữ liệu và nhấn <em>GIẢI BÀI TOÁN</em></h3>
        <p style="font-size:.88rem;">Đề bài và lời giải từng bước sẽ xuất hiện tại đây</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════
#  HELPERS HIỂN THỊ
# ══════════════════════════════════════════════════
def badge(label, kind="pivot"):
    return f'<span class="step-badge {kind}">{label}</span>'
def note_html(text):
    st.markdown(f'<div class="info-note">ℹ️ {text}</div>', unsafe_allow_html=True)
def error_html(text):
    st.markdown(f'<div class="error-box">⚠️ {text}</div>', unsafe_allow_html=True)
def show_step(badge_html, latex_str):
    st.markdown(f'<div class="step-card">{badge_html}', unsafe_allow_html=True)
    st.latex(latex_str)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════
#  PHẦN 1 – HIỂN THỊ ĐỀ BÀI
# ══════════════════════════════════════════════════
st.markdown("## 📝 Đề Bài")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

try:
    de_bai_latex = hien_thi_de_bai(obj_type, c_in, A_in, b_in, dau_in, var_cond, num_vars)
    st.markdown('<div class="problem-box"><h3>Bài toán gốc</h3>', unsafe_allow_html=True)
    st.latex(de_bai_latex)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    error_html(f"Không thể hiển thị đề bài: {e}")

# ══════════════════════════════════════════════════
#  PHẦN 2 – GIẢI BÀI TOÁN
# ══════════════════════════════════════════════════
st.markdown("## 📋 Lời Giải Chi Tiết")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

with st.spinner("Đang giải bài toán…"):
    try:
        # ── Chuẩn hoá ────────────────────────────────────────
        c_std, A_std, b_std, notes, exp_names = chuan_hoa_dau_vao(
            c_in, A_in, b_in, obj_type == "Min", dau_in, var_cond
        )
        num_exp = len(c_std) 

        # ── Khởi tạo từ vựng ─────────────────────────────────
        v, C, D, B = l.khoi_tao_tu_vung_phan_so(c_std, A_std, b_std)
        non_basic = [exp_names[j] for j in range(num_exp)]
        basic     = [f"w_{{{i+1}}}" for i in range(len(b_std))]

        for n in notes: note_html(n)

        # Từ vựng xuất phát (Đã sửa tên hàm l.tao_latex_tu_vung)
        show_step(
            badge("Từ vựng xuất phát", "init"),
            l.tao_latex_tu_vung(v, C, D, B, basic, non_basic)
        )

        is_feasible    = all(x >= 0 for x in B)
        is_optimal_obj = all(x >= 0 for x in C)
        mode_dual      = (not is_feasible and is_optimal_obj)

        # ════ HAI PHA ════════════════════════════════════════
        if not is_feasible and not is_optimal_obj:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔄 Phương Pháp Hai Pha")
            note_html("Vi phạm cả tính khả thi lẫn tối ưu → Kích hoạt Hai Pha.")

            v_d, C_d, D_p1, non_p1 = l.khoi_tao_pha_1(D, non_basic)
            j_in_init, i_out_init   = buoc_xoay_khoi_tao_pha_1(B, non_p1)

            show_step(
                badge("Pha 1 · Xoay khởi tạo x₀", "phase1"),
                l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, j_in_init, i_out_init, is_p1=True)
            )
            v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                v_d, C_d, D_p1, B, basic, non_p1, j_in_init, i_out_init
            )

            it_p1 = 1
            while it_p1 <= 30:
                st_p1, jin_p1, iout_p1 = l.tim_phan_tu_truc_don_hinh_goc(C_d, D_p1, B)
                if st_p1 != "PIVOT": break
                show_step(
                    badge(f"Pha 1 · Bước {it_p1}", "phase1"),
                    l.tao_latex_tu_vung(v_d, C_d, D_p1, B, basic, non_p1, jin_p1, iout_p1, is_p1=True)
                )
                v_d, C_d, D_p1, B, basic, non_p1 = l.thuc_hien_phep_xoay(
                    v_d, C_d, D_p1, B, basic, non_p1, jin_p1, iout_p1
                )
                it_p1 += 1

            if abs(float(v_d)) > 1e-9:
                error_html(f"Pha 1 kết thúc với z₀ = {l.format_frac(v_d)} ≠ 0 → Bài toán VÔ NGHIỆM.")
                st.stop()

            # Đã sửa tên hàm l.chuyen_sang_pha2
            v, C, D, non_basic = l.chuyen_sang_pha2(D_p1, B, basic, non_p1, c_std)
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Pha 2 – Đơn Hình Gốc")
            show_step(
                badge("Từ vựng đầu Pha 2", "init"),
                l.tao_latex_tu_vung(v, C, D, B, basic, non_basic)
            )
            mode_dual = False

        # ════ ĐƠN HÌNH ĐỐI NGẪU ═════════════════════════════
        elif mode_dual:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### 🔁 Đơn Hình Đối Ngẫu")
            note_html("Tất cả c ≥ 0, tồn tại b < 0 → Áp dụng Đơn Hình Đối Ngẫu.")

        # ════ ĐƠN HÌNH GỐC ══════════════════════════════════
        else:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("### ▶️ Đơn Hình Gốc")

        # ════ VÒNG LẶP CHÍNH ════════════════════════════════
        it = 1
        while it <= 50:
            if mode_dual:
                status, j_in, i_out = l.tim_phan_tu_truc_doi_ngau(C, D, B)
                if status == "FEASIBLE":
                    mode_dual = False
                    note_html("Từ vựng đã khả thi → chuyển sang Đơn Hình Gốc.")
                    continue
            else:
                status, j_in, i_out = l.tim_phan_tu_truc_don_hinh_goc(C, D, B)

            if status == "OPTIMAL":
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                show_step(
                    badge("✅ Tối ưu", "optimal"),
                    l.tao_latex_tu_vung(v, C, D, B, basic, non_basic)
                )
                
                # Trích nghiệm chuẩn bằng Fractions trực tiếp, bỏ qua logic cũ bị lỗi
                res_raw = []
                for name in exp_names:
                    if name in non_basic:
                        res_raw.append(Fraction(0))
                    else:
                        idx = basic.index(name)
                        res_raw.append(B[idx])

                nghiem_goc = {}
                exp_idx = 0
                for j in range(num_vars):
                    cond = var_cond[j]
                    if cond == "≥ 0":
                        nghiem_goc[j] = res_raw[exp_idx]
                        exp_idx += 1
                    elif cond == "≤ 0":
                        nghiem_goc[j] = -res_raw[exp_idx]
                        exp_idx += 1
                    else:  # Tự do
                        nghiem_goc[j] = res_raw[exp_idx] - res_raw[exp_idx+1]
                        exp_idx += 2

                z_min = v
                z_display_val = (-z_min) if obj_type == "Max" else z_min

                def frac_to_str(f):
                    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

                z_str   = frac_to_str(z_display_val)
                vars_html = ",&nbsp; ".join(
                    [f"x<sub>{j+1}</sub> = {frac_to_str(nghiem_goc[j])}" for j in range(num_vars)]
                )
                if obj_type == "Max":
                    note_html("Bài toán gốc là Max: z* = −(z_min*)")

                st.markdown(f"""
                <div class="result-box">
                    <h2>🎯 Nghiệm Tối Ưu</h2>
                    <div class="result-value">z* = {z_str}</div>
                    <div class="result-vars">{vars_html}</div>
                </div>
                """, unsafe_allow_html=True)
                break

            elif status == "PIVOT":
                kind  = "dual" if mode_dual else "pivot"
                label = f"Bước {it} · {'Đối ngẫu' if mode_dual else 'Đơn hình gốc'}"
                show_step(
                    badge(label, kind),
                    l.tao_latex_tu_vung(v, C, D, B, basic, non_basic, j_in, i_out, is_dual=mode_dual)
                )
                v, C, D, B, basic, non_basic = l.thuc_hien_phep_xoay(
                    v, C, D, B, basic, non_basic, j_in, i_out
                )
                it += 1

            else:
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
                if status == "UNBOUNDED":
                    error_html("Bài toán KHÔNG GIỚI NỘI — hàm mục tiêu tiến đến ±∞.")
                elif status == "INFEASIBLE":
                    error_html("Bài toán VÔ NGHIỆM — miền chấp nhận được rỗng.")
                else:
                    error_html(f"Trạng thái không xác định: <code>{status}</code>.")
                break
        else:
            error_html("Vượt quá 50 bước lặp — có thể xảy ra hiện tượng lặp vòng (cycling).")

    except Exception as e:
        error_html(f"Lỗi: <code>{e}</code>")
        with st.expander("Chi tiết lỗi kỹ thuật"):
            st.exception(e)