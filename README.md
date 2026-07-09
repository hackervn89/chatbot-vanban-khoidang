# 🤖 Hệ Thống Chuyên Viên Ảo - Soạn Thảo Văn Bản Khối Đảng

Hệ thống tự động hóa phân tích văn bản chỉ đạo của Đảng ủy cấp trên (dạng PDF) để tự động soạn thảo **Công văn giao việc** (dạng Word `.docx`) tuân thủ nghiêm ngặt các quy chế hành chính và quy tắc nghiệp vụ Khối Đảng.

Dự án hỗ trợ chạy song song đồng thời trên **Telegram Bot** và **Zalo Bot**, triển khai trực tuyến 24/7 trên Cloud hoặc chạy trực tiếp trên máy tính thông qua dòng lệnh.

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
│   │   ├── run_generation.py    # Script tự động hoá chuẩn bị dữ liệu và gọi generate_docx.py
│   │   ├── input_84.json        # Dữ liệu JSON đầu vào mẫu cho Kế hoạch 84-KH/TU
│   │   └── temp/                # Thư mục tạm lưu file PDF tải về (tự động sinh khi chạy)
│   │
│   ├── output/                  # Thư mục lưu trữ công văn Word sau khi sinh
│   └── SKILL.md                 # Tài liệu mô tả kỹ năng và các quy tắc nghiệp vụ
│
├── telegram_bot.py              # Tệp chạy Bot Telegram điều khiển từ xa (gửi file PDF trực tiếp)
├── zalo_bot.py                  # Tệp chạy Bot Zalo điều khiển từ xa (qua link Google Drive)
├── main.py                      # Tệp cầu nối dùng để chạy song song cả 2 Bot (đa luồng)
├── run_bot.bat                  # Tệp chạy nhanh song song cả 2 Bot trên máy tính bằng 1 click chuột
├── requirements.txt             # Danh sách thư viện Python cần thiết
├── .env                         # Tệp ẩn lưu trữ mã bảo mật Token & API Key (tuyệt đối không chia sẻ)
└── .gitignore                   # Cấu hình bỏ qua tệp bảo mật .env và các tệp rác khi đẩy lên GitHub
```

---

## 🔒 Cấu Hình Bảo Mật & File Cấu Hình `.env`

Để bảo mật các khóa API và Token, hệ thống đọc cấu hình từ file ẩn `.env`. Hãy tạo file `.env` ở thư mục gốc của dự án với nội dung như sau:

```env
# Telegram Bot API Token từ @BotFather
TELEGRAM_API_TOKEN=8806160877:AAHd79...

# Zalo Bot Token từ OA Zalo Bot Manager
ZALO_API_TOKEN=459563230010...

# Gemini API Key từ Google AI Studio (Dùng để chạy AI phân tích văn bản)
GEMINI_API_KEY=AQ.Ab8RN6...
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
*   **Tính toán thời hạn tự động:** Thời hạn mặc định thực hiện là **10 ngày làm việc** tính từ ngày soạn thảo (tự động bỏ qua Thứ Bảy và Chủ nhật khi đếm ngày).
*   **Định dạng chuẩn:** Ngày đến hạn thực hiện trong nội dung văn bản sẽ được tự động định dạng vừa **bôi đậm** vừa *in nghiêng* dạng: ***trước ngày DD/MM/YYYY***.
*   **Quy chuẩn chính tả Khối Đảng:** Tự động sửa toàn bộ vị trí đặt dấu thanh truyền thống (ví dụ: chuyển `ủy` -> `uỷ`, `hòa` -> `hoà`, `quý` -> `uý`).
*   **Sắp xếp thứ tự hành chính:** Ưu tiên sắp xếp cơ quan quản lý nhà nước (Ủy ban nhân dân xã) lên trước các ban ngành khác trong phần nơi nhận kính gửi.

---

## 🧠 Hệ Thống Phân Tích AI (Gemini + Rule-based Fallback)

Hệ thống sử dụng **chuỗi 3 mô hình Google Gemini AI** theo thứ tự ưu tiên để phân tích văn bản PDF đầu vào:

1. `gemini-3.5-flash` (ưu tiên cao nhất)
2. `gemini-3-flash-preview`
3. `gemini-2.5-flash` (dự phòng cuối)

Nếu mô hình đầu gặp lỗi (hết hạn mức, JSON sai cấu trúc, thiếu trường...), hệ thống **tự động chuyển sang mô hình kế tiếp** trong chuỗi.

### Cơ chế dự phòng Rule-based (chỉ Telegram Bot)

Nếu **tất cả 3 mô hình AI đều thất bại**, Telegram Bot sẽ tự động chuyển sang **phân tích bằng hệ thống quy tắc nội bộ (Rule-based)** sử dụng regex và từ khoá để trích xuất thông tin từ PDF. Zalo Bot hiện chỉ hỗ trợ phân tích bằng AI.

---

## 🚀 Hướng Dẫn Triển Khai Lên Server Cloud Railway (Chạy 24/7 Miễn Phí)

Để bot có thể chạy trực tuyến 24/7 ngay cả khi tắt máy tính cá nhân, bạn hãy triển khai lên **Railway.app**:

### Bước 1: Đồng bộ mã nguồn lên GitHub
1. Tạo một kho chứa (Repository) ở chế độ **Riêng tư (Private)** trên tài khoản GitHub của bạn.
2. Đẩy toàn bộ mã nguồn của dự án lên kho chứa này. Tệp `.gitignore` sẽ tự động giữ lại file `.env` của bạn dưới máy local để tránh rò rỉ bảo mật.

### Bước 2: Liên kết GitHub với Railway
1. Truy cập [Railway.app](https://railway.app/) và đăng nhập bằng tài khoản GitHub của bạn.
2. Chọn **New Project** $\rightarrow$ Chọn **Deploy từ GitHub repo** $\rightarrow$ Chọn kho chứa mã nguồn của Bot.

### Bước 3: Cấu hình biến môi trường (Bảo mật)
1. Trong giao diện dự án trên Railway, nhấp vào dịch vụ bot của bạn.
2. Di chuyển sang tab **Variables** (Biến môi trường) ở thanh menu trên.
3. Nhấn **Add Variable** để cấu hình 3 biến bảo mật (giống hệt trong file `.env` local của bạn):
   * `TELEGRAM_API_TOKEN` = `Mã Token của Telegram`
   * `ZALO_API_TOKEN` = `Mã Token của Zalo`
   * `GEMINI_API_KEY` = `Mã Gemini API Key`
4. Nhấn **Save** (Lưu). Railway sẽ tự động nhận diện tệp chạy chính `main.py`, cài đặt các thư viện phụ thuộc và khởi chạy song song cả 2 bot tự động.

---

## 📱 Cách Sử Dụng Chatbot từ xa

### 1. Trên Telegram Bot:
* Vào phòng chat của Bot Telegram mà bạn tạo.
* Gửi trực tiếp tệp tin **PDF chỉ đạo** (Dạng Document) vào khung chat.
* Bot sẽ tự động xử lý và gửi trả lại tệp tin Word `.docx` hoàn chỉnh trực tiếp vào khung chat của bạn.

### 2. Trên Zalo Bot:
* Do Zalo chưa hỗ trợ bot gửi/nhận tệp tin trực tiếp, chúng ta sử dụng luồng liên kết trung gian (Link):
* Nhắn tin `Xin chào` để bắt đầu hội thoại và kiểm tra kết nối của Bot.
* Tải file PDF chỉ đạo lên Google Drive của bạn $\rightarrow$ Bật quyền chia sẻ *"Bất kỳ ai có liên kết đều xem được"* $\rightarrow$ Copy link gửi cho Zalo Bot.
* Bot sẽ tự động tải file $\rightarrow$ Phân tích và sinh văn bản Word $\rightarrow$ Trả về link tải file Word trực tiếp (Sử dụng dịch vụ chia sẻ bảo mật dùng 1 lần `file.io`, tự động xóa tệp sau khi tải xong để bảo mật dữ liệu).
