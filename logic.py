from fractions import Fraction
import numpy as np

def khoi_tao_tu_vung_phan_so(c, A, b):
    """Chuyển đổi dữ liệu thô thành phân số để tính toán chính xác tuyệt đối"""
    C = [Fraction(x) for x in c]
    B = [Fraction(x) for x in b]
    # Trong từ vựng w = b - Ax, nên hệ số D sẽ là -A
    D = [[-Fraction(val) for val in row] for row in A]
    return Fraction(0), C, D, B

def tim_phan_tu_truc_don_hinh_goc(C, D, B):
    """Tìm biến vào, biến ra theo quy tắc Đơn hình gốc (Minimization)"""
    # 1. Tìm biến vào: Hệ số âm nhất trong hàm mục tiêu Min
    min_c = Fraction(0)
    j_in = -1
    for j, c_val in enumerate(C):
        if c_val < min_c:
            min_c = c_val
            j_in = j
            
    if j_in == -1:
        return "OPTIMAL", -1, -1  # Đã tối ưu

    # 2. Tìm biến ra: Xét tỷ số B_i / |D_i,j| với điều kiện D_i,j < 0
    min_ratio = None
    i_out = -1
    for i, d_row in enumerate(D):
        d_val = d_row[j_in]
        if d_val < Fraction(0): # Hệ số mang dấu âm trong phương trình biến bù
            ratio = B[i] / abs(d_val)
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
                i_out = i
                
    if i_out == -1:
        return "UNBOUNDED", j_in, -1 # Không giới nội

    return "PIVOT", j_in, i_out

def format_frac(f):
    """Định dạng phân số bỏ mẫu số 1"""
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

def tao_latex_tu_vung_hien_tai(v, C, D, B, basic_vars, non_basic_vars, j_in=-1, i_out=-1):
    """Tạo mã LaTeX theo chuẩn, tự động gắn mũi tên và khoanh tròn phần tử trục"""
    lines = []
    
    # Dòng z
    z_line = f"z & = & {format_frac(v)} "
    for j, c_val in enumerate(C):
        if c_val == 0: continue
        sign = "+" if c_val > 0 else "-"
        # Nếu là biến vào, gắn mũi tên xuống
        var_str = f"\\overset{{\\downarrow}}{{{non_basic_vars[j]}}}" if j == j_in else non_basic_vars[j]
        val_str = "" if abs(c_val) == 1 else format_frac(abs(c_val))
        z_line += f"& {sign} {val_str}{var_str} "
    lines.append(z_line)
    lines.append("\\hline")
    
    # Các dòng phương trình
    for i in range(len(B)):
        left_side = f"\\leftarrow {basic_vars[i]}" if i == i_out else basic_vars[i]
        row_line = f"{left_side} & = & {format_frac(B[i])} "
        
        for j, d_val in enumerate(D[i]):
            if d_val == 0: continue
            sign = "+" if d_val > 0 else "-"
            val_str = "" if abs(d_val) == 1 else format_frac(abs(d_val))
            
            # Nếu là phần tử trục, đóng khung
            if i == i_out and j == j_in:
                row_line += f"& {sign} \\boxed{{{val_str}{non_basic_vars[j]}}} "
            else:
                row_line += f"& {sign} {val_str}{non_basic_vars[j]} "
        lines.append(row_line)
        
    col_format = "rrc" + "rc" * len(C)
    return "\\begin{array}{" + col_format + "}\n" + " \\\\\n".join(lines) + "\n\\end{array}"