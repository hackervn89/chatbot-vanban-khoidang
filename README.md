# 🤖 Hệ Thống Chuyên Viên Ảo - Soạn Thảo Văn Bản Khối Đảng

Hệ thống tự động hóa phân tích văn bản chỉ đạo của Đảng ủy cấp trên (dạng PDF) để tự động soạn thảo **Công văn giao việc** (dạng Word `.docx`) tuân thủ nghiêm ngặt các quy chế hành chính và quy tắc nghiệp vụ Khối Đảng.

Ngoài ra, hệ thống còn tích hợp **Chuyên viên ảo hỏi đáp nghiệp vụ** (Q&A) sử dụng trí tuệ nhân tạo kết hợp bộ tri thức nội bộ để giải đáp mọi thắc mắc về thao tác phần mềm Hệ thống Điều hành tác nghiệp (ĐHTN), Thủ tục hành chính Đảng (TTHC) và các quy trình nghiệp vụ Đảng.

Dự án hỗ trợ chạy song song đồng thời trên **Telegram Bot** và **Zalo Bot**, triển khai trực tuyến 24/7 trên Cloud hoặc chạy trực tiếp trên máy tính thông qua dòng lệnh.

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
Chuyên viên ảo/
│
├── taovanban_khoidang/              # Thư mục lõi chứa mã nguồn sinh văn bản
│   ├── references/                  # Thư mục chứa tài liệu mẫu và tri thức
│   │   ├── cong_van_giao_viec_mau.docx  # Mẫu công văn chuẩn Khối Đảng (chứa các thẻ biến {{...}})
│   │   ├── kienthuc_dhtn.md         # Bộ kiến thức nghiệp vụ ĐHTN (hệ thống prompt cho Q&A)
│   │   ├── hdsd_chunks.json         # RAG database: chunks hướng dẫn sử dụng (JSON, TF-IDF retrieval)
│   │   ├── HDSD DHTN/               # Thư mục gốc tài liệu hướng dẫn sử dụng ĐHTN (không push Git)
│   │   └── TTHC/                    # Thư mục gốc tài liệu TTHC Đảng (không push Git)
│   │
│   ├── scripts/                     # Mã nguồn xử lý nghiệp vụ chính
│   │   ├── generate_docx.py         # Script phân tích dữ liệu, tính hạn, gộp nhiệm vụ & tạo file Word
│   │   ├── run_generation.py        # Script tự động hoá chuẩn bị dữ liệu JSON mẫu và gọi generate_docx
│   │   ├── input_84.json            # Dữ liệu JSON đầu vào mẫu cho Kế hoạch 84-KH/TU
│   │   └── temp/                    # Thư mục tạm lưu file PDF/ảnh tải về (tự động sinh khi chạy)
│   │
│   ├── output/                      # Thư mục lưu trữ công văn Word sau khi sinh (tự động dọn sau 24h)
│   └── SKILL.md                     # Tài liệu mô tả kỹ năng và các quy tắc nghiệp vụ chi tiết
│
├── telegram_bot.py                  # Bot Telegram: nhận file PDF, hỏi đáp Q&A, phân tích AI + Rule-based
├── zalo_bot.py                      # Bot Zalo: nhận ảnh/link Google Drive, hỏi đáp Q&A, rút gọn link tải
├── main.py                          # Điều phối đa luồng: Flask file server + Telegram + Zalo + File Cleaner
├── run_bot.bat                      # Script chạy nhanh song song cả 2 Bot trên Windows bằng 1 click chuột
├── requirements.txt                 # Danh sách thư viện Python cần thiết
├── .env                             # Tệp ẩn lưu trữ mã bảo mật Token & API Key (không push lên Git)
├── .gitignore                       # Cấu hình bỏ qua file .env, file tạm, thư mục tri thức nặng
├── README.md                        # Tệp hướng dẫn này
└── MAPCODE.md                       # Bản đồ mã nguồn chi tiết (kiến thức kỹ thuật cho AI/developer)
```

---

## 🔒 Cấu Hình Bảo Mật & File Cấu Hình `.env`

Để bảo mật các khóa API và Token, hệ thống đọc cấu hình từ file ẩn `.env`. Hãy tạo file `.env` ở thư mục gốc của dự án với nội dung như sau:

```env
# Telegram Bot API Token từ @BotFather
TELEGRAM_API_TOKEN=8806160877:AAHd79...

# Zalo Bot Token từ OA Zalo Bot Manager
ZALO_API_TOKEN=459563230010...

# Gemini API Key từ Google AI Studio (Dự phòng phân tích PDF & Q&A khi DeepSeek lỗi)
GEMINI_API_KEY=AQ.Ab8RN6...

# DeepSeek API Key (Mô hình AI ưu tiên chính cho phân tích PDF & Q&A)
DEEPSEEK_API_KEY=sk-...

# Domain server cho Zalo tải file Word (tuỳ chọn, nếu không có sẽ dùng file.io)
SERVER_DOMAIN=https://your-app.up.railway.app
```

| Biến môi trường | Bắt buộc | Mô tả |
|---|---|---|
| `TELEGRAM_API_TOKEN` | ✅ | Token của Telegram Bot từ @BotFather |
| `ZALO_API_TOKEN` | ✅ | Token của Zalo Bot từ OA Bot Manager |
| `GEMINI_API_KEY` | ✅ | API Key Google Gemini (dự phòng + phân tích ảnh Zalo) |
| `DEEPSEEK_API_KEY` | ⚡ Khuyên dùng | API Key DeepSeek (mô hình AI chính, chất lượng cao) |
| `SERVER_DOMAIN` | ⬜ Tuỳ chọn | Domain server Flask để tạo link tải Word cho Zalo Bot |
| `PORT` | ⬜ Tuỳ chọn | Cổng Flask server (mặc định: 8080) |

---

## ⚙️ Các Quy Tắc Nghiệp Vụ Khối Đảng (Tự Động Hóa)

Hệ thống tự động áp dụng các quy tắc hành chính chuẩn xác từ `SKILL.md`:
*   **Xác định cơ quan tham mưu (Cơ quan 2):** Quét từ khóa trong văn bản cấp trên kết hợp với quy tắc xử lý chồng lấn từ ngữ cảnh để tự động phân vai chính xác cho **5 cơ quan cấp xã**:
    1.  *Uỷ ban nhân dân xã* (Kinh tế - xã hội, dịch vụ công, quốc phòng an ninh).
    2.  *Uỷ ban kiểm tra Đảng uỷ xã* (Kiểm tra, giám sát chuyên đề, kỷ luật đảng viên).
    3.  *Ban Xây dựng Đảng* (Tổ chức cán bộ, Tuyên giáo chính trị tư tưởng, Dân vận Đảng).
    4.  *Uỷ ban Mặt trận Tổ quốc xã* (Đoàn kết toàn dân, giám sát & phản biện xã hội, vận động nhân dân).
    5.  *Văn phòng Đảng uỷ xã* (Hành chính văn phòng, tổng hợp, công tác nội chính, phòng chống tham nhũng chính sách).
*   **Quy tắc gộp nhiệm vụ:** Nếu Cơ quan 2 trùng với Ban Xây dựng Đảng, hệ thống tự động gộp 2 nhiệm vụ thành 1 đoạn văn duy nhất và xoá đoạn thừa.
*   **Tính toán thời hạn tự động:** Thời hạn mặc định thực hiện là **10 ngày làm việc** tính từ ngày soạn thảo (tự động bỏ qua Thứ Bảy và Chủ nhật khi đếm ngày).
*   **Định dạng chuẩn:** Ngày đến hạn thực hiện trong nội dung văn bản sẽ được tự động định dạng vừa **bôi đậm** vừa *in nghiêng* dạng: ***trước ngày DD/MM/YYYY***.
*   **Quy chuẩn chính tả Khối Đảng:** Tự động sửa toàn bộ vị trí đặt dấu thanh truyền thống (ví dụ: chuyển `ủy` -> `uỷ`, `hòa` -> `hoà`, `quý` -> `uý`).
*   **Sắp xếp thứ tự hành chính:** Ưu tiên sắp xếp cơ quan quản lý nhà nước (Ủy ban nhân dân xã) lên trước các ban ngành khác trong phần nơi nhận kính gửi.

---

## 🧠 Hệ Thống Phân Tích AI Đa Tầng

Hệ thống sử dụng **chuỗi phân tích đa tầng (Multi-tier Fallback Chain)** để đảm bảo luôn trả kết quả:

### Tầng 1: DeepSeek-V3 (Ưu tiên chính)
- Mô hình: `deepseek-chat` (DeepSeek-V3)
- Ưu điểm: Chất lượng phân tích cao, hỗ trợ JSON output.
- Sử dụng cho: Phân tích văn bản PDF + Hỏi đáp Q&A nghiệp vụ.

### Tầng 2: Google Gemini (Dự phòng)
Nếu DeepSeek lỗi/hết tiền, hệ thống tự động chuyển sang Gemini với **4 mô hình** theo thứ tự:

1. `gemini-1.5-flash` (ưu tiên cao nhất)
2. `gemini-2.5-flash`
3. `gemini-1.5-pro`
4. `gemini-3.5-flash` (dự phòng cuối)

Nếu mô hình đầu gặp lỗi (hết hạn mức, JSON sai cấu trúc, thiếu trường...), hệ thống **tự động chuyển sang mô hình kế tiếp** trong chuỗi.

### Tầng 3: Rule-based (Dự phòng cuối - chỉ Telegram Bot)

Nếu **tất cả mô hình AI đều thất bại**, Telegram Bot sẽ tự động chuyển sang **phân tích bằng hệ thống quy tắc nội bộ (Rule-based)** sử dụng regex và từ khoá để trích xuất thông tin từ PDF. Zalo Bot hiện chỉ hỗ trợ phân tích bằng AI.

---

## 💬 Hệ Thống Hỏi Đáp Nghiệp Vụ (Q&A)

Cả Telegram Bot và Zalo Bot đều tích hợp tính năng hỏi đáp nghiệp vụ thông minh:

### Cơ chế hoạt động
1. **Người dùng gửi câu hỏi** bằng tin nhắn văn bản (không phải file PDF/ảnh).
2. **RAG Retrieval (TF-IDF):** Hệ thống tìm kiếm trong `hdsd_chunks.json` (chunks hướng dẫn sử dụng) để lấy tài liệu liên quan nhất:
   - Nếu điểm TF-IDF **≥ 35**: Sử dụng tài liệu nội bộ làm ngữ cảnh.
   - Nếu điểm TF-IDF **< 35**: Tìm kiếm Web qua DuckDuckGo để bổ sung thông tin thời gian thực.
3. **System Prompt + Bộ kiến thức** (`kienthuc_dhtn.md`) được ghép với ngữ cảnh RAG/Web.
4. **Gọi AI** (DeepSeek → Gemini fallback) để sinh câu trả lời.
5. **Lưu lịch sử hội thoại** (10 tin gần nhất) để duy trì ngữ cảnh liên tục.

### Chia nhỏ tin nhắn tự động
Khi câu trả lời quá dài, hệ thống tự động chia nhỏ tin nhắn:
- **Telegram Bot:** Chia ở ranh giới đoạn văn (`\n\n`), giới hạn 3800 ký tự/phần, retry 2 lần.
- **Zalo Bot:** Chia ở ranh giới đoạn văn (`\n\n`), giới hạn 1800 ký tự/phần, retry 3 lần với exponential backoff.

---

## 🌐 Flask File Server & Cơ Chế Tải File Zalo

### File Server (`main.py`)
`main.py` là tệp điều phối chính, chạy đồng thời **4 luồng (threads)**:

| Luồng | Chức năng |
|---|---|
| `WebServerThread` | Flask server phục vụ tải file Word qua HTTP (route `/download/<file_id>`) |
| `TelegramBotThread` | Chạy Telegram Bot (subprocess `telegram_bot.py`) |
| `ZaloBotThread` | Chạy Zalo Bot (subprocess `zalo_bot.py`) |
| `CleanerThread` | Background task dọn dẹp file Word cũ (> 24h) và mapping cũ mỗi 1 giờ |

### Cơ chế rút gọn link tải cho Zalo
Do Zalo Bot không hỗ trợ gửi file trực tiếp:
1. Sau khi tạo file Word, hệ thống tạo một **mã file ID ngắn** (dựa trên epoch time).
2. Lưu mapping `file_id → tên_file` vào `file_map.json`.
3. Gửi link dạng `https://<SERVER_DOMAIN>/download/<file_id>` cho người dùng.
4. Khi truy cập link, Flask server tra cứu mapping và trả file Word tương ứng.
5. Nếu `SERVER_DOMAIN` chưa cấu hình, hệ thống fallback sang **file.io** (link dùng 1 lần).

---

## 🚀 Hướng Dẫn Triển Khai Lên Server Cloud Railway (Chạy 24/7 Miễn Phí)

Để bot có thể chạy trực tuyến 24/7 ngay cả khi tắt máy tính cá nhân, bạn hãy triển khai lên **Railway.app**:

### Bước 1: Đồng bộ mã nguồn lên GitHub
1. Tạo một kho chứa (Repository) ở chế độ **Riêng tư (Private)** trên tài khoản GitHub của bạn.
2. Đẩy toàn bộ mã nguồn của dự án lên kho chứa này. Tệp `.gitignore` sẽ tự động giữ lại file `.env` của bạn dưới máy local để tránh rò rỉ bảo mật.

### Bước 2: Liên kết GitHub với Railway
1. Truy cập [Railway.app](https://railway.app/) và đăng nhập bằng tài khoản GitHub của bạn.
2. Chọn **New Project** → Chọn **Deploy từ GitHub repo** → Chọn kho chứa mã nguồn của Bot.

### Bước 3: Cấu hình biến môi trường (Bảo mật)
1. Trong giao diện dự án trên Railway, nhấp vào dịch vụ bot của bạn.
2. Di chuyển sang tab **Variables** (Biến môi trường) ở thanh menu trên.
3. Nhấn **Add Variable** để cấu hình các biến bảo mật:
   * `TELEGRAM_API_TOKEN` = `Mã Token của Telegram`
   * `ZALO_API_TOKEN` = `Mã Token của Zalo`
   * `GEMINI_API_KEY` = `Mã Gemini API Key`
   * `DEEPSEEK_API_KEY` = `Mã DeepSeek API Key`
   * `SERVER_DOMAIN` = `https://your-app.up.railway.app` (URL Railway tự cung cấp)
4. Nhấn **Save** (Lưu). Railway sẽ tự động nhận diện tệp chạy chính `main.py`, cài đặt các thư viện phụ thuộc và khởi chạy song song cả 2 bot tự động.

---

## 📱 Cách Sử Dụng Chatbot Từ Xa

### 1. Trên Telegram Bot:
* **Soạn công văn:** Gửi trực tiếp tệp tin **PDF chỉ đạo** (Dạng Document) vào khung chat. Bot sẽ tự động xử lý và gửi trả lại tệp tin Word `.docx` hoàn chỉnh.
* **Hỏi đáp nghiệp vụ:** Gửi tin nhắn văn bản bất kỳ (ví dụ: "Hướng dẫn chuyển sinh hoạt Đảng"). Bot sẽ trả lời dựa trên bộ tri thức nội bộ và AI.

### 2. Trên Zalo Bot:
Do Zalo Bot cá nhân hạn chế gửi nhận tệp trực tiếp, bạn sử dụng 2 cách:
*   **Cách 1 (Nhanh nhất - Khuyên dùng):** Chụp ảnh rõ nét trang đầu của văn bản chỉ đạo và gửi trực tiếp vào phòng chat Zalo. Bot sẽ sử dụng Gemini AI đa phương thức để tự quét ảnh, đọc chữ (OCR), trích xuất thông tin, soạn thảo văn bản Word và gửi link tải.
*   **Cách 2:** Tải tệp PDF chỉ đạo lên Google Drive → Thiết lập chia sẻ "Bất kỳ ai có liên kết đều xem được" → Copy link gửi cho Zalo Bot.
*   **Hỏi đáp nghiệp vụ:** Gửi tin nhắn văn bản bất kỳ. Bot sẽ trả lời tương tự Telegram Bot.
*   **Kết quả trả về:** Bot gửi link tải trực tiếp file Word qua server riêng hoặc dịch vụ bảo mật `file.io`.

---

## 📦 Cài Đặt & Chạy Local

### Yêu cầu
- Python 3.9+
- Các thư viện trong `requirements.txt`

### Cài đặt
```bash
pip install -r requirements.txt
```

### Chạy
```bash
# Chạy song song cả 2 bot + file server
python main.py

# Hoặc trên Windows, double-click file:
run_bot.bat

# Chạy riêng từng bot
python telegram_bot.py
python zalo_bot.py
```
