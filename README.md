# 🤖 Hệ Thống Chuyên Viên Ảo - Soạn Thảo Văn Bản Khối Đảng

Hệ thống tự động hóa phân tích văn bản chỉ đạo của Đảng ủy cấp trên (dạng PDF) để tự động soạn thảo **Công văn giao việc** (dạng Word `.docx`) tuân thủ nghiêm ngặt các quy chế hành chính và quy tắc nghiệp vụ Khối Đảng.

Dự án hỗ trợ chạy trực tiếp trên máy tính thông qua dòng lệnh hoặc điều khiển từ xa thông qua **Telegram Bot** vô cùng tiện lợi khi bạn không có mặt tại văn phòng.

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
Chuyên viên ảo/
│
├── taovanban_khoidang/          # Thư mục lõi chứa mã nguồn sinh văn bản
│   ├── references/              # Thư mục chứa tài liệu mẫu
│   │   └── cong_van_giao_viec_mau.docx   # Mẫu công văn chuẩn Khối Đảng
│   │
│   ├── scripts/                 # Mã nguồn xử lý nghiệp vụ chính
│   │   ├── generate_docx.py     # Script phân tích, tính hạn & tạo tệp Word
│   │   └── fill_template.py     # Bộ lọc điền dữ liệu vào tệp tin mẫu
│   │
│   ├── output/                  # Thư mục lưu trữ công văn Word sau khi sinh
│   └── SKILL.md                 # Tài liệu mô tả kỹ năng và các quy tắc nghiệp vụ
│
├── telegram_bot.py              # Tệp chạy Bot Telegram điều khiển từ xa
├── run_bot.bat                  # Tệp khởi chạy nhanh Bot bằng 1 click chuột
└── requirements.txt             # Danh sách thư viện Python cần thiết
```

---

## ⚙️ Các Quy Tắc Nghiệp Vụ Khối Đảng (Tự Động Hóa)

Hệ thống tự động áp dụng các quy tắc hành chính chuẩn xác từ `SKILL.md`:
*   **Xác định cơ quan tham mưu (Cơ quan 2):** Quét từ khóa trong văn bản cấp trên kết hợp với quy tắc xử lý chồng lấn từ ngữ cảnh để tự động phân vai chính xác cho **5 cơ quan cấp xã**:
    1.  *Uỷ ban nhân dân xã* (Kinh tế - xã hội, dịch vụ công, quốc phòng an ninh).
    2.  *Uỷ ban kiểm tra Đảng uỷ xã* (Kiểm tra, giám sát chuyên đề, kỷ luật đảng viên).
    3.  *Ban Xây dựng Đảng* (Tổ chức cán bộ, Tuyên giáo chính trị tư tưởng, Dân vận Đảng).
    4.  *Uỷ ban Mặt trận Tổ quốc xã* (Đoàn kết toàn dân, giám sát & phản biện xã hội, vận động nhân dân).
    5.  *Văn phòng Đảng uỷ xã* (Hành chính văn phòng, tổng hợp, công tác nội chính, phòng chống tham nhũng chính sách).
*   **Tính toán thời hạn tự động:** Thời hạn mặc định thực hiện là **10 ngày làm việc** tính từ ngày soạn thảo. Nếu trùng vào thứ Bảy hoặc Chủ nhật, hệ thống tự động lùi sang thứ Hai tuần kế tiếp.
*   **Định dạng chuẩn:** Ngày đến hạn thực hiện trong nội dung văn bản sẽ được tự động định dạng vừa **bôi đậm** vừa *in nghiêng* dạng: ***trước ngày DD/MM/YYYY***.
*   **Quy chuẩn chính tả Khối Đảng:** Tự động sửa toàn bộ vị trí đặt dấu thanh truyền thống (ví dụ: chuyển `ủy` -> `uỷ`, `hòa` -> `hoà`, `quý` -> `uý`).
*   **Sắp xếp thứ tự hành chính:** Ưu tiên sắp xếp cơ quan quản lý nhà nước (Ủy ban nhân dân xã) lên trước các ban ngành khác trong phần nơi nhận kính gửi.

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng Telegram Bot từ xa

### Bước 1: Chuẩn bị mã Token Telegram
1. Mở ứng dụng Telegram trên điện thoại, tìm kiếm **`@BotFather`**.
2. Gửi tin nhắn `/newbot` và làm theo hướng dẫn để tạo bot mới.
3. Lưu lại đoạn mã **API Token** được cấp (ví dụ: `8806160877:AAHd79...`).
4. Mở tệp `telegram_bot.py` trên máy tính bằng Notepad hoặc công cụ lập trình, tìm dòng số **21** và điền token của bạn vào:
   ```python
   API_TOKEN = 'ĐIỀN_TOKEN_TẠI_ĐÂY'
   ```

### Bước 2: Khởi chạy Bot
*   **Cách chạy thủ công:** Nhấp đúp chuột vào tệp **`run_bot.bat`** ở thư mục gốc. Một cửa sổ dòng lệnh hiện lên thông báo Bot đang chạy.
*   **Cách sử dụng từ điện thoại:**
    1. Vào Telegram, mở phòng chat với Bot của bạn vừa tạo.
    2. Nhấn nút đính kèm tài liệu (Document) và gửi một tệp chỉ đạo PDF của cấp trên (Ví dụ: `19-KH triển khai thực hiện...`).
    3. Hệ thống sẽ tự động xử lý và gửi lại tệp Word `.docx` hoàn chỉnh trực tiếp vào khung chat trên điện thoại của bạn.

---

## 💻 Hướng Dẫn Tự Động Chạy Khi Mở Máy Tính

### Cách 1: Cho chạy cùng Windows (Xuất hiện cửa sổ CMD thu nhỏ để kiểm tra)
1. Nhấn tổ hợp phím **`Windows + R`**, gõ lệnh **`shell:startup`** rồi nhấn **Enter**.
2. Nhấp chuột phải vào tệp **`run_bot.bat`** $\rightarrow$ Chọn **Create shortcut** (Tạo lối tắt).
3. Di chuyển tệp **Shortcut** vừa tạo vào thư mục Startup vừa hiện ra.

### Cách 2: Chạy ẩn danh hoàn toàn (Không xuất hiện cửa sổ đen CMD)
1. Mở công cụ **`Task Scheduler`** trên Windows.
2. Chọn **Create Basic Task...**, đặt tên cho tác vụ và chọn Trigger là **`When I log on`**.
3. Chọn Action là **`Start a program`**, bấm Browse và dẫn tới tệp **`run_bot.bat`**.
4. Tại ô **Start in (optional)**, dán đường dẫn thư mục dự án: `e:\Viet Design\Chuyên viên ảo`.
5. Bấm Finish. Tiếp tục nhấp đúp vào tác vụ vừa tạo, tại tab *General*, tích chọn **`Run whether user is logged on or not`** và **`Run with highest privileges`** để chạy ẩn.

---

## 📦 Hướng Dẫn Di Chuyển Sang Máy Tính Khác

Dự án được thiết kế hoàn toàn linh động. Khi cần chuyển sang máy khác, bạn thực hiện như sau:

1. Copy toàn bộ thư mục **`Chuyên viên ảo`** sang máy mới.
2. Tải và cài đặt **Python** (từ bản 3.10 trở lên) trên máy mới.
3. Mở dòng lệnh (CMD/PowerShell) tại thư mục dự án trên máy mới và chạy lệnh sau để tự động cài đặt thư viện cần thiết:
   ```powershell
   pip install -r requirements.txt
   ```
4. Bật chạy tệp **`run_bot.bat`** là Bot đã sẵn sàng hoạt động.
