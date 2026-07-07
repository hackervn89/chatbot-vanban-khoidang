import os
import json
import subprocess
import sys

# Configure UTF-8 for console output
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def main():
    base_dir = r"e:\Viet Design\Chuyên viên ảo\taovanban_khoidang"
    
    # 1. Prepare JSON input data
    data = {
        "van_ban_cap_tren": "Kế hoạch số 84-KH/TU, ngày 15/6/2026 của Ban Thường vụ Tỉnh ủy về triển khai thực hiện Quy định chuẩn mực đạo đức cách mạng của cán bộ, đảng viên, công chức, viên chức thuộc Đảng bộ và hệ thống chính trị tỉnh Khánh Hòa trong giai đoạn mới",
        "Ngay_den_han_1": "15/07/2026",
        "Co_quan_2": "Ban xây dựng Đảng", # Triggers the merge rule
        "ngay_den_han_2": "15/07/2026",
        "TRICH_YEU_CONG_VAN": "V/v triển khai thực hiện Kế hoạch số 84-KH/TU ngày 15/6/2026 của Ban Thường vụ Tỉnh ủy",
        "DANH_SACH_GUI": [
            "Ủy ban nhân dân xã",
            "Ủy ban kiểm tra Đảng ủy xã",
            "Ban xây dựng Đảng xã",
            "Ủy ban Mặt trận Tổ quốc Việt Nam xã"
        ],
        "DANH_SACH_NOI_NHAN": [
            "Thường trực Đảng ủy",
            "Các chi bộ trực thuộc",
            "Lưu VPĐU"
        ]
    }
    
    # Write JSON data to a temp file
    json_path = os.path.join(base_dir, "scripts", "input_84.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print(f"[+] Đã tạo file dữ liệu JSON đầu vào tại: {json_path}")
    
    # 2. Run the generator script
    generator_script = os.path.join(base_dir, "scripts", "generate_docx.py")
    output_docx = os.path.join(base_dir, "output", "CV tham mưu KH TU về chuẩn mực đạo đức cách mạng.docx")
    
    print("[*] Đang tiến hành sinh file Word...")
    cmd = [sys.executable, generator_script, json_path, output_docx]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode == 0:
        print(f"[+] Thành công! File công văn đã được tạo tại: {output_docx}")
        print(result.stdout)
    else:
        print("[-] Có lỗi xảy ra khi chạy script generate_docx.py:")
        print(result.stderr)

if __name__ == "__main__":
    main()
