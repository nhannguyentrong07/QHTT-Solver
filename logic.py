from fractions import Fraction

def khoi_tao_tu_vung_phan_so(c, A, b):
    """Chuyển đổi dữ liệu thô thành phân số để tính toán chính xác tuyệt đối"""
    C = [Fraction(x) for x in c]
    B = [Fraction(x) for x in b]
    D = [[-Fraction(val) for val in row] for row in A]
    return Fraction(0), C, D, B

def tim_phan_tu_truc_don_hinh_goc(C, D, B):
    """Tìm biến vào, biến ra theo quy tắc Đơn hình gốc (Minimization)"""
    min_c = Fraction(0)
    j_in = -1
    for j, c_val in enumerate(C):
        if c_val < min_c:
            min_c = c_val
            j_in = j
            
    if j_in == -1:
        return "OPTIMAL", -1, -1

    min_ratio = None
    i_out = -1
    for i, d_row in enumerate(D):
        d_val = d_row[j_in]
        if d_val < Fraction(0):
            ratio = B[i] / abs(d_val)
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
                i_out = i
                
    if i_out == -1:
        return "UNBOUNDED", j_in, -1

    return "PIVOT", j_in, i_out

def format_frac(f):
    """Định dạng phân số bỏ mẫu số 1"""
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def tao_latex_tu_vung_hien_tai(v, C, D, B, basic_vars, non_basic_vars, j_in=-1, i_out=-1):
    """Tạo mã LaTeX theo chuẩn, gắn mũi tên, khoanh tròn phần tử trục và in tỷ số"""
    lines = []
    
    z_line = f"z & = & {format_frac(v)} "
    for j, c_val in enumerate(C):
        if c_val == 0: continue
        sign = "+" if c_val > 0 else "-"
        var_str = f"\\overset{{\\downarrow}}{{{non_basic_vars[j]}}}" if j == j_in else non_basic_vars[j]
        val_str = "" if abs(c_val) == 1 else format_frac(abs(c_val))
        z_line += f"& {sign} {val_str}{var_str} "
    
    z_line += "& "
    lines.append(z_line)
    lines.append("\\hline")
    
    for i in range(len(B)):
        left_side = f"\\leftarrow {basic_vars[i]}" if i == i_out else basic_vars[i]
        row_line = f"{left_side} & = & {format_frac(B[i])} "
        
        for j, d_val in enumerate(D[i]):
            if d_val == 0: continue
            sign = "+" if d_val > 0 else "-"
            val_str = "" if abs(d_val) == 1 else format_frac(abs(d_val))
            
            if i == i_out and j == j_in:
                row_line += f"& {sign} \\boxed{{{val_str}{non_basic_vars[j]}}} "
            else:
                row_line += f"& {sign} {val_str}{non_basic_vars[j]} "
                
        ratio_str = "& "
        if j_in != -1 and D[i][j_in] < Fraction(0):
            ratio_val = B[i] / abs(D[i][j_in])
            ratio_str = f"& \\quad ({format_frac(ratio_val)})"
            
        row_line += ratio_str
        lines.append(row_line)
        
    col_format = "rrc" + "rc" * len(C) + "l"
    return "\\begin{array}{" + col_format + "}\n" + " \\\\\n".join(lines) + "\n\\end{array}"

def thuc_hien_phep_xoay(v, C, D, B, basic_vars, non_basic_vars, j_in, i_out):
    """Thực hiện phép thế đại số: Rút biến vào từ dòng biến ra và thế vào các dòng khác"""
    v_new = v
    C_new = list(C)
    D_new = [list(row) for row in D]
    B_new = list(B)
    
    basic_new = list(basic_vars)
    non_basic_new = list(non_basic_vars)
    
    pivot = D[i_out][j_in] 
    
    B_new[i_out] = B[i_out] / (-pivot)
    for j in range(len(C)):
        if j == j_in:
            D_new[i_out][j] = Fraction(1) / pivot 
        else:
            D_new[i_out][j] = D[i_out][j] / (-pivot)
            
    for i in range(len(B)):
        if i == i_out: continue
        factor = D[i][j_in]
        B_new[i] = B[i] + factor * B_new[i_out]
        for j in range(len(C)):
            if j == j_in:
                D_new[i][j] = factor * D_new[i_out][j_in] 
            else:
                D_new[i][j] = D[i][j] + factor * D_new[i_out][j]
                
    factor_z = C[j_in]
    v_new = v + factor_z * B_new[i_out]
    for j in range(len(C)):
        if j == j_in:
            C_new[j] = factor_z * D_new[i_out][j_in]
        else:
            C_new[j] = C[j] + factor_z * D_new[i_out][j]
            
    basic_new[i_out], non_basic_new[j_in] = non_basic_new[j_in], basic_new[i_out]
    
    return v_new, C_new, D_new, B_new, basic_new, non_basic_new

def trich_xuat_nghiem(B, basic_vars, non_basic_vars, num_goc):
    """Lấy giá trị của các biến x_1, x_2... từ Từ vựng tối ưu"""
    nghiem = []
    for k in range(1, num_goc + 1):
        ten_x = f"x_{{{k}}}"
        if ten_x in non_basic_vars:
            nghiem.append("0") 
        else:
            idx = basic_vars.index(ten_x)
            nghiem.append(format_frac(B[idx]))
    return nghiem

def tim_phan_tu_truc_doi_ngau(C, D, B):
    """Tìm biến vào/ra theo Đơn hình Đối ngẫu (Dual Simplex)"""
    # 1. Biến ra (chọn trước): b_i âm nhất
    min_b = Fraction(0)
    i_out = -1
    for i, b_val in enumerate(B):
        if b_val < min_b:
            min_b = b_val
            i_out = i
            
    if i_out == -1:
        return "FEASIBLE", -1, -1 # Đã khả thi, trở lại Đơn hình gốc
        
    # 2. Biến vào (chọn sau): Tỷ số C[j] / |D[i_out][j]| nhỏ nhất (chỉ xét D > 0)
    min_ratio = None
    j_in = -1
    for j, d_val in enumerate(D[i_out]):
        if d_val > Fraction(0):
            ratio = C[j] / d_val
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
                j_in = j
                
    if j_in == -1:
        return "INFEASIBLE", -1, -1 # Hệ thống báo bài toán Vô nghiệm
        
    return "PIVOT", j_in, i_out

def khoi_tao_pha_1(D, non_basic_vars):
    """Thiết lập Từ vựng Pha 1: Thêm x_0 và tạo hàm delta = x_0"""
    non_basic_new = list(non_basic_vars) + ["x_0"]
    # Thêm hệ số +1 cho x_0 ở tất cả các phương trình (Dấu +x_0)
    D_new = [row + [Fraction(1)] for row in D]
    
    # Sửa lại chuẩn xác: Hàm mục tiêu tạm thời delta = 0 + x_0 (Hệ số là +1)
    C_delta = [Fraction(0)] * len(non_basic_vars) + [Fraction(1)]
    v_delta = Fraction(0)
    
    return v_delta, C_delta, D_new, non_basic_new

def buoc_xoay_khoi_tao_pha_1(B, non_basic_vars):
    """Bước xoay khởi tạo bắt buộc: Biến vào là x_0, biến ra là b_i âm nhất"""
    j_in = len(non_basic_vars) - 1 # Vị trí của x_0 (nằm cuối cùng)
    
    min_b = Fraction(0)
    i_out = -1
    for i, b_val in enumerate(B):
        if b_val < min_b:
            min_b = b_val
            i_out = i
            
    return j_in, i_out

def chuyen_tu_pha1_sang_pha2(D_pha1, B, basic_vars, non_basic_pha1, c_original):
    """Bỏ x_0 khỏi Từ vựng, thiết lập lại hàm mục tiêu z gốc cho Pha 2"""
    # 1. Loại bỏ cột x_0 ra khỏi ma trận và danh sách biến
    try:
        idx_x0 = non_basic_pha1.index("x_0")
        non_basic_new = non_basic_pha1[:idx_x0] + non_basic_pha1[idx_x0+1:]
        D_new = [row[:idx_x0] + row[idx_x0+1:] for row in D_pha1]
    except ValueError:
        non_basic_new = list(non_basic_pha1)
        D_new = [list(row) for row in D_pha1]

    # 2. Khởi tạo lại hàm Z gốc: z = 0
    v_new = Fraction(0)
    C_new = [Fraction(0)] * len(non_basic_new)

    # 3. Thế các biến vào hàm Z (z = sum(c_j * x_j))
    for j, c_val in enumerate(c_original):
        ten_x = f"x_{{{j+1}}}"
        if ten_x in non_basic_new:
            # Nếu x_j đang ở vế phải (phi cơ sở), cộng thẳng hệ số vào C
            idx = non_basic_new.index(ten_x)
            C_new[idx] += Fraction(c_val)
        elif ten_x in basic_vars:
            # Nếu x_j đang ở vế trái (cơ sở), thế phương trình của nó vào z
            idx_i = basic_vars.index(ten_x)
            v_new += Fraction(c_val) * B[idx_i] # Cộng hằng số tự do
            for k, _ in enumerate(non_basic_new):
                C_new[k] += Fraction(c_val) * D_new[idx_i][k] # Nhân phân phối hệ số

    return v_new, C_new, D_new, non_basic_new