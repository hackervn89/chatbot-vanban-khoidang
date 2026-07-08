import os
import sys
import re
import time
import requests
import json
from pypdf import PdfReader
from google import genai
from google.genai import types

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Resolve paths
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define custom dotenv loader to read .env file safely
def load_dotenv():
    dotenv_path = os.path.join(script_dir, '.env')
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    os.environ[key] = val

load_dotenv()

# Detect project structure
if os.path.basename(script_dir) == "scripts":
    PROJECT_ROOT = os.path.dirname(script_dir)
    sys.path.append(script_dir)
else:
    PROJECT_ROOT = os.path.join(script_dir, "taovanban_khoidang")
    sys.path.append(os.path.join(PROJECT_ROOT, "scripts"))

from generate_docx import generate_document

# Configs
ZALO_API_TOKEN = os.environ.get('ZALO_API_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

GEMINI_MODELS = [
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
]

TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "references", "cong_van_giao_viec_mau.docx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
TEMP_DIR = os.path.join(PROJECT_ROOT, "scripts", "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Shared Prompt
GEMINI_SYSTEM_PROMPT = """Bạn là chuyên viên văn thư hành chính Đảng. Nhiệm vụ của bạn là đọc văn bản chỉ đạo của cấp trên và trích xuất chính xác các thông tin sau.

Quy tắc xác định Cơ quan ban hành:
- Nếu văn bản ghi "Ban Thường vụ Tỉnh ủy ban hành" → Cơ quan ban hành là "Ban Thường vụ Tỉnh uỷ"
- Nếu văn bản ghi "Thường trực Tỉnh ủy chỉ đạo/yêu cầu" → Cơ quan ban hành là "Thường trực Tỉnh uỷ"
- Nếu văn bản ghi "Tỉnh ủy ban hành" hoặc "Ban Chấp hành Tỉnh ủy" → Cơ quan ban hành là "Tỉnh uỷ"
- Không ghép thêm tên địa phương (Khánh Hòa, Lâm Đồng...) vào tên cơ quan.

Quy tắc xác định Cơ quan tham mưu triển khai (co_quan_2) — chọn 1 trong 5:
1. "Uỷ ban nhân dân xã" — nếu nội dung liên quan đến: kinh tế, đất đai, môi trường, nông nghiệp, giao thông, xây dựng, y tế, giáo dục, thể dục thể thao, an ninh quốc phòng, giảm nghèo, lao động việc làm, tài chính ngân sách, dịch vụ công.
2. "Uỷ ban kiểm tra Đảng uỷ xã" — nếu nội dung liên quan đến: kiểm tra giám sát đảng viên, kỷ luật đảng, vi phạm, suy thoái, tự diễn biến, kê khai tài sản.
3. "Ban Xây dựng Đảng" — nếu nội dung liên quan đến: tổ chức cán bộ, tuyên giáo, chính trị tư tưởng, học tập nghị quyết, đạo đức cách mạng, nêu gương, xây dựng chỉnh đốn đảng, phát triển đảng viên, dân vận.
4. "Uỷ ban Mặt trận Tổ quốc Việt Nam xã" — nếu nội dung liên quan đến: đại đoàn kết toàn dân, phản biện xã hội, các đoàn thể (thanh niên, phụ nữ, cựu chiến binh, nông dân), vận động nhân dân, an sinh xã hội.
5. "Văn phòng Đảng uỷ xã" — nếu nội dung liên quan đến: quy chế làm việc, văn thư lưu trữ, nội chính, phòng chống tham nhũng lãng phí tiêu cực, chuyển đổi số, cải cách hành chính trong đảng.

Quy tắc xử lý chồng lấn:
- "giám sát" + "phản biện xã hội/cộng đồng/nhân dân" → MTTQ. Còn lại → UBKT.
- "tuyên truyền" + "vận động quần chúng/phong trào nhân dân" → MTTQ. Còn lại → Ban Xây dựng Đảng.
- "phòng chống tham nhũng" + "kiểm tra kỷ luật đảng viên" → UBKT. Còn lại → Văn phòng Đảng uỷ.

Bạn PHẢI trả lời bằng JSON hợp lệ với đúng cấu trúc sau (không thêm bất kỳ văn bản nào khác ngoài JSON):
{
  "doc_type": "Thể loại văn bản (Kế hoạch, Nghị quyết, Chỉ thị, Quy định, Chương trình...)",
  "number": "Ký hiệu số (ví dụ: 19-KH/TU)",
  "date": "Ngày ban hành theo định dạng DD/MM/YYYY",
  "authority": "Cơ quan ban hành",
  "title": "Trích yếu nội dung (phần sau chữ 'về')",
  "co_quan_2": "Tên cơ quan tham mưu triển khai (1 trong 5 cơ quan ở trên)"
}"""

def download_gdrive_file(url, output_path):
    """Tải file PDF công khai từ Google Drive"""
    file_id = None
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
    if match:
        file_id = match.group(1)
    else:
        match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
        if match:
            file_id = match.group(1)
            
    if not file_id:
        return False
        
    download_url = f"https://docs.google.com/uc?export=download&id={file_id}"
    session = requests.Session()
    response = session.get(download_url, stream=True)
    
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break
            
    if token:
        download_url += f"&confirm={token}"
        response = session.get(download_url, stream=True)
        
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    return False

def upload_to_file_io(file_path):
    """Tải tệp lên file.io và lấy link tải về dùng một lần (bảo mật)"""
    try:
        with open(file_path, 'rb') as f:
            r = requests.post('https://file.io', files={'file': f}, timeout=15)
            if r.status_code == 200:
                return r.json().get('link')
    except Exception as e:
        print(f"[!] Lỗi khi tải file lên file.io: {e}")
    return None

def analyze_with_gemini(pdf_path):
    """Hàm trích xuất dữ liệu bằng Gemini API (Giống Telegram)"""
    if not GEMINI_API_KEY:
        raise ValueError("Chưa cấu hình GEMINI_API_KEY")
        
    reader = PdfReader(pdf_path)
    first_page_text = reader.pages[0].extract_text() or ""
    last_page_text = reader.pages[-1].extract_text() or ""
    
    combined_text = first_page_text
    if last_page_text and last_page_text != first_page_text:
        combined_text += "\n\n--- TRANG CUỐI ---\n\n" + last_page_text
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    for model_name in GEMINI_MODELS:
        try:
            print(f"[Zalo API] Đang phân tích bằng mô hình: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=combined_text,
                config=types.GenerateContentConfig(
                    system_instruction=GEMINI_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            raw_text = response.text.strip()
            data = json.loads(raw_text)
            
            # Kiểm tra định dạng trường
            required_fields = ["doc_type", "number", "date", "authority", "title", "co_quan_2"]
            if all(field in data for field in required_fields):
                data["model_used"] = model_name
                return data
            else:
                print(f"[Zalo API] Phản hồi thiếu trường từ {model_name}")
        except Exception as e:
            print(f"[Zalo API] Lỗi ở mô hình {model_name}: {e}")
            
    raise RuntimeError("Tất cả mô hình Gemini đều gặp lỗi hoặc trả về sai cấu trúc JSON.")

def send_zalo_message(chat_id, text):
    """Gửi tin nhắn phản hồi qua Zalo"""
    url = f"https://bot-api.zaloplatforms.com/bot{ZALO_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        return r.json()
    except Exception as e:
        print(f"[Zalo API] Gửi tin nhắn lỗi: {e}")
        return {}

def process_zalo_message(message):
    """Xử lý tin nhắn nhận được"""
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()
    sender_name = message.get("from", {}).get("display_name", "bạn")
    
    if not chat_id:
        return
        
    # 1. Xử lý câu chào hỏi
    if text.lower() in ["xin chào", "chào bot", "hello", "hi", "bắt đầu"]:
        reply = (f"Chào {sender_name}! Tôi là Bot Chuyên viên số của Đảng uỷ xã.\n\n"
                 "👉 Để soạn thảo văn bản tự động, hãy tải file PDF chỉ đạo lên Google Drive, "
                 "thiết lập chia sẻ 'Bất kỳ ai có liên kết' và gửi link liên kết vào đây cho tôi.")
        send_zalo_message(chat_id, reply)
        return

    # 2. Xử lý Google Drive Link
    if "drive.google.com" in text:
        send_zalo_message(chat_id, "⏳ Đã nhận liên kết Google Drive. Đang tiến hành tải tệp và phân tích dữ liệu...")
        
        pdf_filename = f"zalo_{int(time.time())}.pdf"
        pdf_path = os.path.join(TEMP_DIR, pdf_filename)
        
        # Download
        if not download_gdrive_file(text, pdf_path):
            send_zalo_message(chat_id, "❌ Không thể tải file từ liên kết của bạn. Hãy đảm bảo bạn đã bật chia sẻ 'Bất kỳ ai có liên kết' (Public) cho file PDF đó trên Google Drive.")
            return
            
        try:
            # Analyze
            metadata = analyze_with_gemini(pdf_path)
            
            # Generate docx
            docx_filename = f"Cong_van_giao_viec_{metadata['number'].replace('/', '_')}.docx"
            output_docx_path = os.path.join(OUTPUT_DIR, docx_filename)
            
            success = generate_document(TEMPLATE_PATH, output_docx_path, metadata)
            
            if success and os.path.exists(output_docx_path):
                # Upload to file.io
                download_link = upload_to_file_io(output_docx_path)
                
                if download_link:
                    msg = (
                        f"📊 **KẾT QUẢ PHÂN TÍCH (Mô hình {metadata['model_used']}):**\n"
                        f"• Loại văn bản: {metadata['doc_type']}\n"
                        f"• Số hiệu: {metadata['number']}\n"
                        f"• Ngày ban hành: {metadata['date']}\n"
                        f"• Cơ quan ban hành: {metadata['authority']}\n"
                        f"• Cơ quan tham mưu: {metadata['co_quan_2']}\n\n"
                        f"🚀 **Đã tạo văn bản Word thành công!**\n"
                        f"🔗 Tải xuống tại đây (Link bảo mật chỉ dùng 1 lần): {download_link}"
                    )
                    send_zalo_message(chat_id, msg)
                else:
                    send_zalo_message(chat_id, "❌ Soạn văn bản thành công nhưng không thể upload tệp lên dịch vụ chia sẻ. Vui lòng liên hệ quản trị viên.")
            else:
                send_zalo_message(chat_id, "❌ Lỗi trong quá trình tạo tệp văn bản từ biểu mẫu Word.")
        except Exception as e:
            send_zalo_message(chat_id, f"❌ Đã xảy ra lỗi khi phân tích bằng AI: {str(e)}")
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    else:
        # Nhắc nhở cú pháp
        reply = "Tôi không hiểu yêu cầu này. Hãy gửi một đường link Google Drive chứa file PDF văn bản cần xử lý nhé."
        send_zalo_message(chat_id, reply)

def main():
    if not ZALO_API_TOKEN:
        print("[!] LỖI: Không tìm thấy ZALO_API_TOKEN trong môi trường.")
        sys.exit(1)
        
    print("==================================================")
    print("🤖 Zalo Bot Chuyên viên số đang chạy...")
    print("==================================================")
    
    # Xóa Webhook cũ để tránh xung đột với cơ chế getUpdates (Polling)
    url_delete_webhook = f"https://bot-api.zaloplatforms.com/bot{ZALO_API_TOKEN}/deleteWebhook"
    try:
        print("[Zalo API] Đang xóa Webhook cũ...")
        res = requests.post(url_delete_webhook, timeout=10)
        print(f"[Zalo API] Kết quả xóa Webhook: {res.text}")
    except Exception as e:
        print(f"[Zalo API] Lỗi khi gỡ bỏ Webhook: {e}")
        
    url_get_updates = f"https://bot-api.zaloplatforms.com/bot{ZALO_API_TOKEN}/getUpdates"
    
    while True:
        try:
            payload = {"timeout": 30}
            response = requests.post(url_get_updates, json=payload, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and data.get("ok") and data.get("result"):
                    update = data["result"]
                    event_name = update.get("event_name")
                    message = update.get("message", {})
                    
                    if event_name == "message.text.received" or "text" in message:
                        process_zalo_message(message)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nZalo Bot đã dừng.")
            break
        except Exception as e:
            if "Read timed out" not in str(e):
                print(f"[Zalo Bot Error] {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
