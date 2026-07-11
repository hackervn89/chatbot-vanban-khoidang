# 🗺️ MAPCODE - Bản Đồ Mã Nguồn Chi Tiết

> Tệp này lưu trữ kiến thức kỹ thuật chi tiết về toàn bộ codebase để AI/developer có thể nhanh chóng hiểu và làm việc với dự án mà không cần đọc lại từng file.

---

## 📐 Tổng Quan Kiến Trúc

```
[Người dùng]
    │
    ├── Telegram (gửi file PDF / câu hỏi text)
    │       │
    │       ▼
    │   telegram_bot.py ──┐
    │                      │
    ├── Zalo (gửi ảnh / link GDrive / câu hỏi text)
    │       │              │
    │       ▼              │
    │   zalo_bot.py ───────┤
    │                      │
    │                      ▼
    │               ┌─────────────┐
    │               │   AI Chain  │
    │               │ DeepSeek ─→ │
    │               │ Gemini(x4) ─│──→ Rule-based (Telegram only)
    │               └─────┬───────┘
    │                     │
    │                     ▼
    │         generate_docx.py (sinh Word)
    │                     │
    │                     ▼
    │         output/*.docx (Công văn kết quả)
    │                     │
    │           ┌─────────┴─────────┐
    │           │                   │
    │       Telegram:           Zalo:
    │     gửi file trực tiếp   Flask server → link tải
    │                              │
    │                          main.py (Flask + threading)
    │
    └── Q&A Flow: text → RAG → AI → trả lời chia nhỏ
```

---

## 📝 Danh Sách File & Chức Năng Chi Tiết

### `main.py` (112 dòng)
**Vai trò:** Điều phối trung tâm - chạy đa luồng.

| Hàm/Route | Dòng | Chức năng |
|---|---|---|
| `get_file_mapping(file_id)` | 21-30 | Đọc `file_map.json` để tra cứu tên file Word thực từ file_id rút gọn |
| `@app.route('/')` | 32-34 | Health check endpoint |
| `@app.route('/download/<filename>')` | 36-46 | Phục vụ tải file Word - thử mapping rút gọn trước, fallback tải trực tiếp |
| `run_web_server()` | 48-51 | Khởi chạy Flask trên port `$PORT` (mặc định 8080) |
| `run_telegram()` | 53-55 | Chạy subprocess `telegram_bot.py` |
| `run_zalo()` | 57-59 | Chạy subprocess `zalo_bot.py` |
| `file_cleaner_task()` | 61-93 | Background daemon: xoá file Word > 24h + dọn mapping cũ, chạy mỗi 1 giờ |

**Biến quan trọng:**
- `OUTPUT_DIR`: Thư mục chứa file Word sinh ra
- `MAP_FILE`: `file_map.json` - bảng mapping file_id → filename

---

### `telegram_bot.py` (≈880 dòng)
**Vai trò:** Bot Telegram hoàn chỉnh - nhận PDF, phân tích AI, tạo Word, Q&A.

| Hàm | Dòng | Chức năng |
|---|---|---|
| `load_dotenv()` | 20-30 | Đọc file `.env` tự custom (không dùng thư viện python-dotenv) |
| `remove_accents(input_str)` | 111-122 | Bỏ dấu tiếng Việt (dùng cho TF-IDF matching) |
| `calculate_idfs(chunks)` | 124-138 | Tính IDF cho toàn bộ RAG chunks |
| `retrieve_chunks(question, ...)` | 140-164 | TF-IDF retrieval: tìm top-N chunks liên quan nhất, trả về (score, chunk) |
| `load_knowledge_bases()` | 166-194 | Tải `kienthuc_dhtn.md` + `hdsd_chunks.json` vào bộ nhớ khi khởi động |
| `search_duckduckgo_free(query)` | 224-234 | Tìm kiếm DuckDuckGo khi RAG score < 35 |
| `ask_dhtn_qa(chat_id, question)` | 236-344 | **Core Q&A:** RAG → DeepSeek/Gemini → trả lời + lưu lịch sử |
| `analyze_with_gemini(pdf_text)` | 346-401 | Phân tích PDF bằng Gemini (4 model fallback), trả JSON chuẩn |
| `analyze_with_deepseek(text)` | 403-446 | Phân tích PDF bằng DeepSeek (ưu tiên), trả JSON chuẩn |
| `parse_pdf_metadata(pdf_path)` | 448-511 | **Rule-based fallback**: regex trích xuất số, ngày, loại VB, cơ quan |
| `get_short_type(doc_type)` | 514-528 | Chuyển loại VB → viết tắt (KH, NQ, CT, ...) |
| `get_short_title(title)` | 531-542 | Rút gọn trích yếu ≤ 6 từ cho tên file |
| `determine_agency_2(title, text)` | 545-680 | **Rule-based:** phân loại cơ quan tham mưu bằng keyword + disambiguation |
| `send_welcome(message)` | 683-690 | Handler `/start`, `/help` |
| `handle_docs(message)` | 693-810 | **Core PDF flow:** download → extract → AI/Rule → generate Word → gửi file |
| `handle_text_questions(message)` | 812-870 | **Core Q&A flow:** split_message → ask_dhtn_qa → gửi phản hồi chia nhỏ |

**Cấu hình quan trọng:**
- `GEMINI_MODELS`: `["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-3.5-flash"]`
- `MAX_HISTORY_LEN = 10`: Lưu 10 tin nhắn gần nhất (5 lượt hội thoại)
- `CONVERSATION_HISTORY`: Dict `{chat_id: [messages]}` - in-memory, mất khi restart
- `GEMINI_SYSTEM_PROMPT`: Prompt phân tích PDF → JSON 6 trường
- `DHTN_QA_SYSTEM_PROMPT`: Prompt Q&A nghiệp vụ + slot `{kienthuc_content}`

**Flow xử lý PDF (handle_docs):**
1. Validate `.pdf` → Download → Extract text (trang 1 + trang cuối)
2. `analyze_with_deepseek(text)` → nếu lỗi → `analyze_with_gemini(text)`
3. Nếu AI thành công: lấy 6 trường JSON (`doc_type`, `number`, `date`, `authority`, `title`, `co_quan_2`)
4. Nếu AI thất bại: `parse_pdf_metadata()` + `determine_agency_2()` (rule-based)
5. Tạo payload → `generate_document()` → Gửi file `.docx` qua Telegram

**Flow Q&A (handle_text_questions):**
1. `ask_dhtn_qa()`: RAG retrieval → build prompt → DeepSeek/Gemini
2. `split_message()`: Chia nhỏ nếu > 3800 ký tự, ưu tiên chia ở `\n\n`
3. Gửi từng phần với retry 2 lần, delay 0.5s giữa mỗi phần

---

### `zalo_bot.py` (≈885 dòng)
**Vai trò:** Bot Zalo - nhận ảnh/link GDrive, Q&A, rút gọn link tải.

| Hàm | Dòng | Chức năng |
|---|---|---|
| `download_gdrive_file(url, output_path)` | 198-232 | Tải PDF từ Google Drive (xử lý confirm download lớn) |
| `download_file_from_url(url, output_path)` | 234-246 | Tải file từ URL bất kỳ (cho ảnh Zalo) |
| `upload_to_file_io(file_path)` | 248-257 | Upload file lên file.io → lấy link dùng 1 lần |
| `save_file_mapping(file_id, filename)` | 259-271 | Lưu mapping rút gọn vào `file_map.json` |
| `analyze_with_gemini(pdf_path)` | 453-493 | Phân tích PDF bằng Gemini (khác Telegram: đọc text rồi gửi) |
| `analyze_image_with_gemini(image_path)` | 495-531 | **Đa phương thức:** Gửi ảnh PIL + prompt cho Gemini OCR |
| `split_message(text, max_len=1800)` | 644-664 | Chia nhỏ tin nhắn, ưu tiên chia ở `\n\n` |
| `send_zalo_message(chat_id, text)` | 666-695 | Gửi tin nhắn Zalo, tự động split + retry 3 lần exponential backoff |
| `send_zalo_chat_action(chat_id, action)` | 697-707 | Gửi trạng thái "đang soạn tin" |
| `generate_and_send_word_doc(chat_id, ...)` | 709-771 | Sinh Word → tạo link tải (server hoặc file.io) → gửi tin |
| `process_zalo_message(message)` | 773-842 | **Core handler:** Parse tin nhắn → ảnh/text → xử lý tương ứng |
| `main()` | 844-886 | Polling loop: `getUpdates` → `process_zalo_message` |

**Khác biệt so với Telegram Bot:**
- Zalo dùng **HTTP polling** (`getUpdates` endpoint) thay vì `infinity_polling` của pyTelegramBotAPI
- Zalo không gửi file trực tiếp → phải qua **Flask server** hoặc **file.io**
- Zalo hỗ trợ nhận **ảnh chụp** (OCR đa phương thức qua Gemini)
- Zalo hỗ trợ nhận **link Google Drive** để tải PDF
- `split_message` dùng `max_len=1800` (Zalo giới hạn chặt hơn Telegram)
- Retry với exponential backoff (1.5s, 3s, 4.5s)

**Flow xử lý ảnh (process_zalo_message → photo_url):**
1. Tải ảnh từ Zalo server → lưu temp
2. `analyze_image_with_gemini()`: PIL.Image → Gemini multimodal → JSON 6 trường
3. `generate_and_send_word_doc()`: Sinh Word → upload/tạo link → gửi tin

**Zalo API Endpoints:**
- `POST /bot{token}/sendMessage` — Gửi tin nhắn
- `POST /bot{token}/sendChatAction` — Gửi trạng thái typing
- `POST /bot{token}/getUpdates` — Long polling lấy tin mới
- `POST /bot{token}/deleteWebhook` — Xoá webhook cũ khi khởi động

---

### `taovanban_khoidang/scripts/generate_docx.py` (457 dòng)
**Vai trò:** Engine sinh văn bản Word từ template + data JSON.

| Hàm | Dòng | Chức năng |
|---|---|---|
| `delete_paragraph(paragraph)` | 17-20 | Xoá paragraph khỏi document XML |
| `format_paragraph_to_standard(p)` | 22-33 | Định dạng Times New Roman 14pt, thụt đầu dòng 1cm |
| `format_agency_list(items)` | 35-66 | Format danh sách cơ quan: `- Tên;` (cuối: `.`), 1 item không có `-` |
| `normalize_agency_name(name)` | 69-75 | Chuẩn hoá tên cơ quan (lowercase + normalize dấu) |
| `sort_agencies(agencies)` | 77-89 | Sắp xếp cơ quan theo thứ tự hành chính (UBND → MTTQ → BXD → UBKT → VPĐU) |
| `convert_to_old_tone_style(text)` | 91-107 | Chuyển dấu thanh mới → cũ (ủy→uỷ, hòa→hoà, úy→uý) |
| `apply_old_tone_style_to_doc(doc)` | 109-120 | Áp dụng chuyển dấu cho toàn bộ document |
| `parse_parent_document_date(...)` | 122-141 | Parse ngày từ chuỗi `van_ban_cap_tren` |
| `calculate_default_deadline(...)` | 143-154 | Tính 10 ngày làm việc (bỏ T7/CN) |
| `apply_bold_italic_to_deadline(p, date)` | 156-206 | Bôi đậm + in nghiêng cụm "trước ngày DD/MM/YYYY" |
| `format_all_deadlines_bold_italic(doc, dates)` | 208-218 | Áp dụng bold-italic cho tất cả deadline trong doc |
| `generate_document(data, template, output)` | 220-422 | **Core function:** Điền template, xử lý gộp, xoá paragraph thừa, format, save |

**Template Variables (trong `cong_van_giao_viec_mau.docx`):**
| Biến | Vị trí | Mô tả |
|---|---|---|
| `{{van_ban_cap_tren}}` | Đoạn mở đầu | Chuỗi đầy đủ văn bản cấp trên |
| `{{van_ban_cap_tren_rut_gon}}` | Đoạn giao việc | Phiên bản rút gọn (không có "của...về...") |
| `{{Ngay_den_han_1}}` | Nhiệm vụ 1 | Hạn hoàn thành quán triệt, tuyên truyền |
| `{{Co_quan_2}}` | Nhiệm vụ 2 | Tên cơ quan tham mưu triển khai |
| `{{ngay_den_han_2}}` | Nhiệm vụ 2 | Hạn hoàn thành triển khai thực hiện |
| `{{TRICH_YEU_CONG_VAN}}` | Table header | Trích yếu nội dung (italic, 12pt, center) |
| `{{DANH_SACH_GUI}}` | Table Kính gửi | Danh sách đơn vị nhận (tự động filter) |
| `{{DANH_SACH_NOI_NHAN}}` | Table Nơi nhận | Danh sách nơi nhận (bị xoá paragraph) |

**Quy tắc gộp (Consolidation):**
- Nếu `Co_quan_2` = "Ban Xây dựng Đảng" (normalize match):
  - Nhiệm vụ 1 → gộp "quán triệt, tuyên truyền VÀ triển khai thực hiện"
  - Nhiệm vụ 2 → **XOÁ paragraph**
  - Không đánh số thứ tự ("1." → bỏ)
  - `DANH_SACH_GUI` chỉ có "Ban Xây dựng Đảng."

---

### `taovanban_khoidang/scripts/run_generation.py` (59 dòng)
**Vai trò:** Script tiện ích để chạy sinh văn bản mẫu từ command line.
- Tạo file JSON mẫu (KH 84-KH/TU) → gọi `generate_docx.py` qua subprocess.

### `taovanban_khoidang/scripts/input_84.json` (18 dòng)
**Vai trò:** Dữ liệu JSON mẫu cho Kế hoạch 84-KH/TU (dùng để test).

### `taovanban_khoidang/SKILL.md` (199 dòng)
**Vai trò:** Tài liệu kỹ năng chi tiết cho AI agent — mô tả đầy đủ 6 quy tắc nghiệp vụ, 5 cơ quan cấp xã, disambiguation rules, formatting standards, naming convention.

---

## 🔑 Danh Sách Biến Môi Trường Đầy Đủ

| Biến | File sử dụng | Bắt buộc | Mô tả |
|---|---|---|---|
| `TELEGRAM_API_TOKEN` | `telegram_bot.py` | ✅ | Token Telegram Bot |
| `ZALO_API_TOKEN` | `zalo_bot.py` | ✅ | Token Zalo Bot |
| `GEMINI_API_KEY` | `telegram_bot.py`, `zalo_bot.py` | ✅ | Google Gemini API Key |
| `DEEPSEEK_API_KEY` | `telegram_bot.py`, `zalo_bot.py` | ⚡ | DeepSeek API Key (ưu tiên chính) |
| `SERVER_DOMAIN` | `zalo_bot.py` | ⬜ | Domain Flask server cho link tải Zalo |
| `PORT` | `main.py` | ⬜ | Cổng Flask (mặc định: 8080) |

---

## 🔄 Chuỗi Fallback AI Chi Tiết

### Phân tích PDF (extract metadata JSON):
```
DeepSeek-V3 ("deepseek-chat")
    ↓ (lỗi/không cấu hình)
Gemini gemini-1.5-flash
    ↓ (lỗi/rate limit)
Gemini gemini-2.5-flash
    ↓ (lỗi/rate limit)
Gemini gemini-1.5-pro
    ↓ (lỗi/rate limit)
Gemini gemini-3.5-flash
    ↓ (tất cả thất bại)
Rule-based: regex + keyword matching [chỉ Telegram]
```

### Hỏi đáp Q&A:
```
1. RAG Retrieval (TF-IDF trên hdsd_chunks.json)
   ├── Score ≥ 35 → Sử dụng tài liệu nội bộ
   └── Score < 35 → Tìm kiếm DuckDuckGo (ddgs)

2. Build prompt = DHTN_QA_SYSTEM_PROMPT + kienthuc_dhtn.md + RAG/Web context

3. DeepSeek-V3 (deepseek-chat)
    ↓ (lỗi)
   Gemini (4 model fallback, có Google Search Grounding nếu score < 35)
    ↓ (tất cả thất bại)
   Thông báo lỗi cho người dùng
```

---

## 📊 Giới Hạn & Ngưỡng Quan Trọng

| Thông số | Giá trị | Vị trí |
|---|---|---|
| RAG score threshold | `35` | `telegram_bot.py:270`, `zalo_bot.py:334` |
| RAG retrieval algorithm | TF-IDF unigram + **bigram boost x3** | `retrieve_chunks()` trong cả 2 bot |
| Max conversation history | `10` tin nhắn | `telegram_bot.py:227`, `zalo_bot.py:291` |
| Telegram split max_len | `3800` ký tự | `telegram_bot.py:838` |
| Zalo split max_len | `1800` ký tự | `zalo_bot.py:660` |
| Telegram retry | `2` lần | `telegram_bot.py:863` |
| Zalo retry | `3` lần, exponential backoff | `zalo_bot.py:697` |
| DeepSeek timeout | `25s` (Q&A), `30s` (analysis) | Các file bot |
| Gemini temperature | `0.1` (analysis), `0.5` (Q&A) | Các file bot |
| File cleanup interval | `3600s` (1 giờ) | `main.py:93` |
| File max age | `24h` | `main.py:68` |
| Default deadline | `10 ngày làm việc` | `generate_docx.py:149` |

---

## 🧩 Thư Viện Phụ Thuộc

| Thư viện | Phiên bản | Mục đích |
|---|---|---|
| `pyTelegramBotAPI` | latest | SDK Telegram Bot (telebot) |
| `pypdf` | latest | Đọc và extract text từ file PDF |
| `python-docx` | latest | Tạo và chỉnh sửa file Word (.docx) |
| `google-genai` | latest | SDK Google Gemini API (genai) |
| `requests` | latest | HTTP client cho DeepSeek API, Zalo API, download file |
| `flask` | latest | Web server phục vụ tải file Word |
| `Pillow` | latest | Xử lý ảnh (PIL.Image) cho Zalo OCR multimodal |
| `ddgs` | latest | Tìm kiếm DuckDuckGo (fallback khi RAG score thấp) |

---

## 📌 Ghi Chú Kỹ Thuật

1. **Không dùng `python-dotenv`:** Cả 2 bot đều tự viết hàm `load_dotenv()` để đọc `.env` file (tránh dependency thừa).
2. **In-memory state:** `CONVERSATION_HISTORY`, `CHUNKS_DATA`, `KIENTHUC_CONTENT` đều lưu trong RAM → **mất khi restart**.
3. **`main.py` chạy bot bằng subprocess**, không import trực tiếp → mỗi bot là process độc lập, crash 1 bot không ảnh hưởng bot kia.
4. **Zalo Bot dùng long polling** (`timeout: 30s`) thay vì webhook → phù hợp deploy đơn giản.
5. **`file_map.json`** lưu ở `scripts/temp/` → cùng lifecycle với file tạm.
6. **Quy tắc dấu thanh cũ** (`oà`, `uỷ`, `uý`) được áp dụng **sau cùng** trong pipeline `generate_document()`.
