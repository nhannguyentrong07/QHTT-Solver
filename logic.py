import numpy as np

def chuan_hoa_buoc_1_va_2(c, A, b, is_minimize, dau_rang_buoc):
    """
    Hàm này nhận vào ma trận đề bài và thực hiện 2 bước chuẩn hóa đầu tiên.
    - c: vector hệ số hàm mục tiêu
    - A: ma trận hệ số ràng buộc
    - b: vector vế phải (RHS)
    - is_minimize: True nếu là bài toán Min, False nếu là Max
    - dau_rang_buoc: mảng chứa các dấu ('<=', '>=', '=')
    """
    buoc_giai_thich = [] # Nơi lưu trữ các câu giải thích từ vựng
    
    # 1. Chuẩn hóa Hàm mục tiêu (Chuyển Min thành Max)
    c_chuan = np.array(c, dtype=float)
    if is_minimize:
        c_chuan = -c_chuan
        buoc_giai_thich.append("- Phát hiện bài toán Min: Đã nhân hàm mục tiêu với -1 để chuyển về bài toán Max chuẩn.")
    else:
        buoc_giai_thich.append("- Bài toán Max: Hàm mục tiêu đã ở dạng chuẩn.")

    # 2. Chuẩn hóa Vế phải (Đảm bảo RHS >= 0)
    A_chuan = np.array(A, dtype=float)
    b_chuan = np.array(b, dtype=float)
    dau_chuan = list(dau_rang_buoc)

    for i in range(len(b_chuan)):
        if b_chuan[i] < 0:
            # Nhân cả hàng i của ma trận A và b với -1
            A_chuan[i] = -A_chuan[i]
            b_chuan[i] = -b_chuan[i]
            
            # Đảo chiều dấu bất đẳng thức
            if dau_chuan[i] == '<=':
                dau_chuan[i] = '>='
            elif dau_chuan[i] == '>=':
                dau_chuan[i] = '<='
                
            buoc_giai_thich.append(f"- Phát hiện vế phải của ràng buộc {i+1} âm ({b[i]}): Đã nhân cả 2 vế với -1 và đảo chiều bất đẳng thức.")

    return c_chuan, A_chuan, b_chuan, dau_chuan, buoc_giai_thich

def tao_chuoi_latex(he_so, ten_bien):
    """Biến đổi mảng hệ số thành chuỗi toán học định dạng chuẩn"""
    terms = []
    for i, c in enumerate(he_so):
        if c == 0:
            continue
        
        # Loại bỏ đuôi .0 nếu là số nguyên (ví dụ 3.0 thành 3)
        c_val = int(c) if float(c).is_integer() else round(c, 4)
        
        # Ẩn số 1 đứng trước biến (ví dụ 1x thành x)
        if abs(c_val) == 1:
            term = ten_bien[i]
        else:
            term = f"{abs(c_val)}{ten_bien[i]}"
            
        # Xử lý dấu cộng/trừ
        if not terms: # Hạng tử đầu tiên
            if c_val < 0:
                terms.append(f"-{term}")
            else:
                terms.append(term)
        else: # Các hạng tử tiếp theo
            if c_val < 0:
                terms.append(f"- {term}")
            else:
                terms.append(f"+ {term}")
                
    return " ".join(terms) if terms else "0"