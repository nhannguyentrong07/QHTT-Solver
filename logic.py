import numpy as np

def chuan_hoa_va_tao_tu_vung(c, A, b, is_minimize, dau_rang_buoc):
    """
    Chuẩn hóa bài toán về dạng: Min Z, các ràng buộc <=.
    Tạo ra hệ số chuẩn bị cho Từ vựng xuất phát.
    """
    giai_thich = []
    
    # 1. Xử lý hàm mục tiêu
    c_std = np.array(c, dtype=float)
    is_max_converted = False

    if not is_minimize:
        c_std = -c_std  # Đổi dấu hệ số hàm mục tiêu
        is_max_converted = True
        giai_thich.append("- Đổi hàm mục tiêu từ Max sang Min: Đặt z' = -z, nhân các hệ số với -1.")
    else:
        giai_thich.append("- Hàm mục tiêu đã ở dạng Min chuẩn.")

    # 2. Xử lý ràng buộc
    A_std = []
    b_std = []
    
    for i in range(len(b)):
        row_A = np.array(A[i], dtype=float)
        val_b = float(b[i])
        dau = dau_rang_buoc[i]

        if dau == '<=':
            A_std.append(row_A)
            b_std.append(val_b)
        elif dau == '>=':
            A_std.append(-row_A)
            b_std.append(-val_b)
            giai_thich.append(f"- Ràng buộc {i+1} (dấu >=): Đã nhân 2 vế với -1 để chuyển thành <=.")
        elif dau == '=':
            # Tách thành 1 cái <= và 1 cái >= (rồi đổi >= thành <=)
            A_std.append(row_A)
            b_std.append(val_b)
            A_std.append(-row_A)
            b_std.append(-val_b)
            giai_thich.append(f"- Ràng buộc {i+1} (dấu =): Đã tách thành hai bất phương trình <= và >= (sau đó nhân -1 cho >=).")

    return np.array(c_std), np.array(A_std), np.array(b_std), giai_thich, is_max_converted

def tao_latex_tu_vung_xuat_phat(c, A, b, is_max_converted=False):
    """
    Xuất mã LaTeX cấu trúc Từ vựng theo đúng chuẩn quy tắc:
    z = ... \hline w_i = b_i - sum(a_ij * x_j)
    """
    num_vars = len(c)
    num_constraints = len(b)
    lines = []
    
    # Dòng Hàm mục tiêu
    z_label = "z'" if is_max_converted else "z"
    z_line = f"{z_label} & = & 0 "
    for j in range(num_vars):
        val = c[j]
        if val == 0: continue
        sign = "+" if val > 0 else "-"
        # Dùng :g để tự động bỏ số .0 vô nghĩa
        z_line += f"& {sign} {abs(val):g}x_{{{j+1}}} "
    lines.append(z_line)
    
    # Vạch ngăn cách
    lines.append("\\hline")
    
    # Các dòng Biến bù (w_i)
    for i in range(num_constraints):
        w_line = f"w_{{{i+1}}} & = & {b[i]:g} "
        for j in range(num_vars):
            val = A[i][j]
            if val == 0: continue
            # Trong từ vựng w_i = b_i - a_ij*x_j, nên phải lấy số đối của a_ij
            dict_val = -val
            sign = "+" if dict_val > 0 else "-"
            w_line += f"& {sign} {abs(dict_val):g}x_{{{j+1}}} "
        lines.append(w_line)
        
    # Gộp thành môi trường array căn chỉnh các cột (rrcrcrcr...)
    col_format = "rrc" + "rc" * num_vars
    latex_str = "\\begin{array}{" + col_format + "}\n"
    latex_str += " \\\\\n".join(lines)
    latex_str += "\n\\end{array}"
    
    return latex_str