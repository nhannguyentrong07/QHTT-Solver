from fractions import Fraction

def format_frac(f):
    """Định dạng phân số, nếu mẫu số là 1 thì in ra số nguyên"""
    if isinstance(f, (int, float)):
        f = Fraction(str(f))
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def khoi_tao_tu_vung_phan_so(c, A, b):
    C = [Fraction(str(x)) for x in c]
    B = [Fraction(str(x)) for x in b]
    D = [[-Fraction(str(val)) for val in row] for row in A]
    return Fraction(0), C, D, B

def tim_phan_tu_truc_don_hinh_goc(C, D, B):
    j_in = -1
    for j, c_val in enumerate(C):
        if c_val < 0:
            j_in = j
            break # Tuân thủ tuyệt đối Quy tắc Bland: Chọn biến âm đầu tiên
            
    if j_in == -1: return "OPTIMAL", -1, -1
    
    min_ratio = None
    i_out = -1
    for i, d_row in enumerate(D):
        if d_row[j_in] < 0:
            ratio = B[i] / abs(d_row[j_in])
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
                i_out = i
    if i_out == -1: return "UNBOUNDED", j_in, -1
    return "PIVOT", j_in, i_out

def tim_phan_tu_truc_doi_ngau(C, D, B):
    i_out = -1
    for i, b_val in enumerate(B):
        if b_val < 0:
            i_out = i
            break # Quy tắc Bland cho Đối ngẫu: Chọn biến ra đầu tiên bị âm
            
    if i_out == -1: return "FEASIBLE", -1, -1
    
    min_ratio = None
    j_in = -1
    for j, d_row_val in enumerate(D[i_out]):
        if d_row_val > 0:
            ratio = C[j] / d_row_val
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
                j_in = j
    if j_in == -1: return "INFEASIBLE", -1, -1
    return "PIVOT", j_in, i_out

def tao_latex_tu_vung(v, C, D, B, basic, non_basic, j_in=-1, i_out=-1, is_p1=False, is_dual=False):
    lines = []
    z_label = "\\delta" if is_p1 else "z"
    z_line = f"{z_label} & = & {format_frac(v)} "
    for j, val in enumerate(C):
        if val == 0: continue
        sign = "+" if val > 0 else "-"
        var_name = f"\\overset{{\\downarrow}}{{{non_basic[j]}}}" if j == j_in else non_basic[j]
        z_line += f"& {sign} {'' if abs(val)==1 else format_frac(abs(val))}{var_name} "
    z_line += "& "
    lines.append(z_line); lines.append("\\hline")
    
    for i in range(len(B)):
        left = f"\\leftarrow {basic[i]}" if i == i_out else basic[i]
        row = f"{left} & = & {format_frac(B[i])} "
        for j, val in enumerate(D[i]):
            if val == 0: continue
            sign = "+" if val > 0 else "-"
            term = f"{'' if abs(val)==1 else format_frac(abs(val))}{non_basic[j]}"
            row += f"& {sign} {'\\boxed{'+term+'}' if (i==i_out and j==j_in) else term} "
        
        ratio_str = "& "
        if not is_dual and j_in != -1 and D[i][j_in] < 0:
            ratio_str = f"& \\quad ({format_frac(B[i]/abs(D[i][j_in]))})"
        row += ratio_str
        lines.append(row)
        
    return "\\begin{array}{rrc" + "rc"*len(C) + "l}\n" + " \\\\\n".join(lines) + "\n\\end{array}"

def thuc_hien_phep_xoay(v, C, D, B, basic, non_basic, j_in, i_out):
    pivot = D[i_out][j_in]
    B_new = list(B); C_new = list(C); D_new = [list(r) for r in D]
    B_new[i_out] = B[i_out] / (-pivot)
    for j in range(len(C)):
        D_new[i_out][j] = D[i_out][j]/(-pivot) if j != j_in else Fraction(1)/pivot
    for i in range(len(B)):
        if i == i_out: continue
        factor = D[i][j_in]
        B_new[i] = B[i] + factor * B_new[i_out]
        for j in range(len(C)):
            D_new[i][j] = D[i][j] + factor * D_new[i_out][j] if j != j_in else factor * D_new[i_out][j_in]
    f_z = C[j_in]
    v_new = v + f_z * B_new[i_out]
    for j in range(len(C)):
        C_new[j] = C[j] + f_z * D_new[i_out][j] if j != j_in else f_z * D_new[i_out][j_in]
    basic_n = list(basic); non_basic_n = list(non_basic)
    basic_n[i_out], non_basic_n[j_in] = non_basic_n[j_in], basic_n[i_out]
    return v_new, C_new, D_new, B_new, basic_n, non_basic_n

def khoi_tao_pha_1(D, non_basic):
    return Fraction(0), [Fraction(0)]*len(non_basic) + [Fraction(1)], [r + [Fraction(1)] for r in D], non_basic + ["x_0"]

def chuyen_sang_pha2(D_p1, B, basic, non_p1, c_orig, exp_names):
    idx_x0 = non_p1.index("x_0")
    non_p2 = non_p1[:idx_x0] + non_p1[idx_x0+1:]
    D_p2 = [r[:idx_x0] + r[idx_x0+1:] for r in D_p1]
    v_n = Fraction(0); C_n = [Fraction(0)]*len(non_p2)
    for j, val in enumerate(c_orig):
        name = exp_names[j]
        if name in non_p2:
            C_n[non_p2.index(name)] += val
        elif name in basic:
            idx = basic.index(name)
            v_n += val * B[idx]
            for k in range(len(non_p2)): C_n[k] += val * D_p2[idx][k]
    return v_n, C_n, D_p2, non_p2