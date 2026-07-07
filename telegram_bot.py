import os
import re
import sys
import json
import telebot
from pypdf import PdfReader
from google import genai
from google.genai import types

# Configure UTF-8 for console output on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Dynamically resolve import paths so we can run from anywhere
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

# Detect if we are running at the workspace root or inside taovanban_khoidang/scripts
if os.path.basename(script_dir) == "scripts":
    PROJECT_ROOT = os.path.dirname(script_dir)
    sys.path.append(script_dir)
else:
    PROJECT_ROOT = os.path.join(script_dir, "taovanban_khoidang")
    sys.path.append(os.path.join(PROJECT_ROOT, "scripts"))

from generate_docx import generate_document

# ==================== CONFIGURATION ====================
API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Danh sách mô hình Gemini theo thứ tự ưu tiên (fallback chain)
GEMINI_MODELS = [
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
]
# =======================================================

# Validate tokens are loaded
if not API_TOKEN:
    print("[!] LỖI: Không tìm thấy TELEGRAM_API_TOKEN trong môi trường hoặc tệp .env")
    sys.exit(1)

bot = telebot.TeleBot(API_TOKEN)

# Paths relative to the project root
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "references", "cong_van_giao_viec_mau.docx")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
TEMP_DIR = os.path.join(PROJECT_ROOT, "scripts", "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# System Prompt cho Gemini API (tiếng Việt)
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


def analyze_with_gemini(pdf_text):
    """
    Gửi văn bản PDF cho Gemini API để phân tích.
    Thử lần lượt 3 mô hình theo thứ tự ưu tiên.
    Trả về dict kết quả nếu thành công, None nếu tất cả đều thất bại.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'ĐIỀN_GEMINI_API_KEY_TẠI_ĐÂY':
        print("[!] Chưa cấu hình Gemini API Key. Sử dụng Rule-based.")
        return None

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"[!] Lỗi khởi tạo Gemini Client: {e}")
        return None

    for model_name in GEMINI_MODELS:
        try:
            print(f"[*] Đang thử mô hình: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=pdf_text,
                config=types.GenerateContentConfig(
                    system_instruction=GEMINI_SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )

            # Parse JSON response
            result_text = response.text.strip()
            result = json.loads(result_text)

            # Validate required fields
            required_fields = ["doc_type", "number", "date", "authority", "title", "co_quan_2"]
            if all(field in result and result[field] for field in required_fields):
                result["model_used"] = model_name
                print(f"[+] Phân tích thành công bởi: {model_name}")
                return result
            else:
                print(f"[-] Mô hình {model_name} trả về JSON thiếu trường. Thử mô hình tiếp theo...")
                continue

        except json.JSONDecodeError as e:
            print(f"[-] Mô hình {model_name} trả về JSON không hợp lệ: {e}. Thử mô hình tiếp theo...")
            continue
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"[-] Mô hình {model_name} đã hết hạn mức (Rate Limit). Thử mô hình tiếp theo...")
            else:
                print(f"[-] Lỗi khi gọi mô hình {model_name}: {e}. Thử mô hình tiếp theo...")
            continue

    print("[!] Tất cả mô hình Gemini đều thất bại. Chuyển sang Rule-based.")
    return None

def parse_pdf_metadata(pdf_path):
    """
    Parse PDF to automatically extract document type, number, date, authority, and title.
    """
    reader = PdfReader(pdf_path)
    first_page_text = ""
    for page in reader.pages[:1]:
        first_page_text += page.extract_text() or ""
        
    lines = [line.strip() for line in first_page_text.split('\n') if line.strip()]
    
    # 1. Identify Number
    number = ""
    num_match = re.search(r'Số\s+([^\r\n]+)', first_page_text, re.IGNORECASE)
    if num_match:
        number = num_match.group(1).strip()
        
    # 2. Identify Date
    date_str = ""
    date_match = re.search(r'ngày\s+(\d+)\s+tháng\s+(\d+)\s+năm\s+(\d+)', first_page_text, re.IGNORECASE)
    if date_match:
        d, m, y = date_match.groups()
        date_str = f"{int(d):02d}/{int(m):02d}/{y}"
    else:
        date_match2 = re.search(r'ngày\s+(\d+)[/-](\d+)[/-](\d+)', first_page_text, re.IGNORECASE)
        if date_match2:
            d, m, y = date_match2.groups()
            date_str = f"{int(d):02d}/{int(m):02d}/{y}"
            
    # 3. Identify Document Type and Title
    doc_type = "Kế hoạch"
    title = ""
    
    types = ["KẾ HOẠCH", "NGHỊ QUYẾT", "CHƯƠNG TRÌNH", "CHỈ THỊ", "QUY ĐỊNH", "QUYẾT ĐỊNH", "CÔNG VĂN"]
    type_idx = -1
    for idx, line in enumerate(lines):
        if any(t in line for t in types):
            doc_type = line.title()
            type_idx = idx
            break
            
    if type_idx != -1:
        title_lines = []
        for idx in range(type_idx + 1, len(lines)):
            line = lines[idx]
            if line.startswith("---") or line.startswith("I.") or "mục đích" in line.lower() or "nhằm" in line.lower():
                break
            title_lines.append(line)
        title = " ".join(title_lines).strip()
        
    title = re.sub(r'\s*\-+\s*$', '', title)
    
    # 4. Identify Issuing Authority
    authority = "Ban Thường vụ Tỉnh ủy"
    if "ban thường vụ tỉnh ủy" in first_page_text.lower():
        authority = "Ban Thường vụ Tỉnh ủy"
    elif "thường trực tỉnh ủy" in first_page_text.lower():
        authority = "Thường trực Tỉnh ủy"
    elif "tỉnh ủy" in first_page_text.lower():
        authority = "Tỉnh ủy"
    elif "trung ương" in first_page_text.lower():
        authority = "Ban Chấp hành Trung ương"
        
    return doc_type, number, date_str, authority, title


def get_short_type(doc_type):
    dt = doc_type.lower()
    if "kế hoạch" in dt:
        return "KH"
    elif "nghị quyết" in dt:
        return "NQ"
    elif "chương trình" in dt:
        return "CTr"
    elif "chỉ thị" in dt:
        return "CT"
    elif "quy định" in dt:
        return "QD"
    elif "quyết định" in dt:
        return "QĐ"
    return "CV"


def get_short_title(title):
    # Try to grab the core topic after "về"
    match = re.search(r'về\s+(.*)', title, re.IGNORECASE)
    if match:
        target = match.group(1).strip()
    else:
        target = re.sub(r'^(Thực hiện\s+|Triển khai\s+)', '', title, flags=re.IGNORECASE)
    
    words = target.split()
    if len(words) > 6:
        return " ".join(words[:6])
    return target


def determine_agency_2(title, first_page_text):
    """
    Determine Co_quan_2 automatically based on keyword matching and disambiguation rules.
    """
    text = (title + " " + first_page_text).lower()

    # Pre-process common spelling variations to simplify matching
    text = text.replace("uỷ", "ủy").replace("oà", "òa").replace("uý", "úy")

    # 1. Disambiguation rules first
    # 1.1 "giám sát"
    has_giamsat = "giám sát" in text
    is_mttq_giamsat = has_giamsat and any(
        k in text for k in ["phản biện xã hội", "cộng đồng", "của nhân dân", "giám sát xã hội", "giám sát cộng đồng"]
    )
    is_ubkt_giamsat = has_giamsat and not is_mttq_giamsat

    # 1.2 "phòng chống tham nhũng, lãng phí, tiêu cực"
    has_pctn = any(k in text for k in ["phòng chống tham nhũng", "tiêu cực", "lãng phí"])
    is_ubkt_pctn = has_pctn and any(
        k in text for k in ["kiểm tra", "kỷ luật", "đảng viên", "chi bộ", "dấu hiệu vi phạm", "kê khai tài sản"]
    )
    is_vpdu_pctn = has_pctn and not is_ubkt_pctn

    # 1.3 "tuyên truyền"
    has_tuyentruyen = "tuyên truyền" in text
    is_mttq_tuyentruyen = has_tuyentruyen and any(
        k in text for k in ["vận động quần chúng", "phong trào nhân dân", "cuộc vận động toàn dân", "vận động nhân dân"]
    )
    is_bxd_tuyentruyen = has_tuyentruyen and not is_mttq_tuyentruyen

    # 1.4 "tôn giáo, dân tộc"
    has_tongiao_dantoc = any(k in text for k in ["tôn giáo", "dân tộc"])
    is_mttq_tongiao_dantoc = has_tongiao_dantoc and any(
        k in text for k in ["thiểu số", "vận động nhân dân các tôn giáo", "đại đoàn kết dân tộc", "khối đại đoàn kết"]
    )
    is_bxd_tongiao_dantoc = has_tongiao_dantoc and not is_mttq_tongiao_dantoc

    # 1.5 "khiếu nại, tố cáo"
    has_kntc = any(k in text for k in ["khiếu nại", "tố cáo"])
    is_ubkt_kntc = has_kntc and any(
        k in text for k in ["đảng viên", "tổ chức đảng", "kỷ luật đảng", "đảng phí", "sinh hoạt đảng"]
    )
    is_ubnd_kntc = has_kntc and not is_ubkt_kntc

    # 2. Match with keyword lists
    # UBKT Keywords
    ubkt_keywords = [
        "kiểm tra", "kỷ luật đảng", "thi hành kỷ luật", "kỷ luật", "vi phạm", "dấu hiệu vi phạm",
        "kiểm tra khi có dấu hiệu vi phạm", "giám sát chuyên đề", "khiển trách", "cảnh cáo", "cách chức",
        "khai trừ", "xử lý đảng viên vi phạm", "suy thoái", "tự diễn biến", "tự chuyển hoá", "đảng phí",
        "thẻ đảng", "thu hồi thẻ đảng", "kê khai tài sản", "khiếu nại tố cáo đối với đảng viên",
        "giải quyết tố cáo đảng viên", "sinh hoạt đảng không đúng quy định"
    ]
    
    # Ban Xây dựng Đảng Keywords
    bxd_keywords = [
        "tổ chức cán bộ", "quy hoạch cán bộ", "đào tạo bồi dưỡng cán bộ", "luân chuyển cán bộ",
        "bổ nhiệm", "đề bạt", "sắp xếp tổ chức bộ máy", "tinh giản biên chế", "nhân sự", "tuyên giáo",
        "chính trị tư tưởng", "giáo dục chính trị", "học tập nghị quyết", "quán triệt nghị quyết",
        "sơ kết tổng kết nghị quyết", "đạo đức cách mạng", "học tập và làm theo", "tư tưởng hồ chí minh",
        "tấm gương đạo đức", "nêu gương", "chuẩn mực đạo đức", "xây dựng đảng", "chỉnh đốn đảng",
        "nâng cao năng lực lãnh đạo", "đổi mới phương thức lãnh đạo", "xây dựng tổ chức đảng",
        "kết nạp đảng", "phát triển đảng viên", "chuyển đảng chính thức", "đảng viên dự bị", "dân vận",
        "dân vận khéo", "công tác dân vận", "tuyên truyền"
    ]

    # MTTQ Keywords
    mttq_keywords = [
        "mặt trận tổ quốc", "ban thường trực mặt trận", "khối đại đoàn kết", "phản biện xã hội",
        "giám sát xã hội", "hiệp thương bầu cử", "ý kiến kiến nghị của cử tri", "phong trào thi đua toàn dân",
        "an sinh xã hội", "quyên góp ủng hộ", "đoàn thanh niên", "hội phụ nữ", "hội liên hiệp phụ nữ",
        "hội cựu chiến binh", "hội nông dân", "công đoàn", "các đoàn thể", "tổ chức chính trị - xã hội",
        "từ thiện", "quyên góp", "ủng hộ", "quỹ vì người nghèo", "ngày vì người nghèo", "phong trào",
        "cuộc vận động", "toàn dân", "vận động nhân dân", "ngày hội đại đoàn kết", "ý kiến cử tri",
        "kiến nghị cử tri", "tiếp xúc cử tri", "mặt trận"
    ]

    # VPĐU Keywords
    vpdu_keywords = [
        "văn phòng đảng uỷ", "văn phòng đảng ủy", "văn thư", "lưu trữ", "phục vụ cấp uỷ", "phục vụ cấp ủy",
        "quy chế làm việc", "chương trình công tác", "tổng hợp", "báo cáo định kỳ", "báo cáo sơ kết",
        "báo cáo tổng kết", "hậu cần", "hội nghị", "phiên họp", "chuyển đổi số", "công nghệ thông tin",
        "ứng dụng cntt", "nội chính", "phòng chống tham nhũng", "lãng phí", "tiêu cực", "cải cách hành chính trong đảng"
    ]

    # UBND Keywords
    ubnd_keywords = [
        "ủy ban nhân dân", "uỷ ban nhân dân", "cơ quan chấp hành", "hành chính nhà nước", "quản lý hành chính địa phương",
        "thi hành pháp luật", "dự toán ngân sách xã", "tài sản công cấp xã", "biên chế công chức xã",
        "an ninh trật tự cơ sở", "dịch vụ công thiết yếu", "tiếp công dân cấp xã", "hoạt động tự quản của thôn",
        "kinh tế", "kinh tế - xã hội", "phát triển kinh tế", "đất đai", "tài nguyên", "khoáng sản",
        "môi trường", "biến đổi khí hậu", "nông nghiệp", "nông thôn", "nông thôn mới", "xây dựng nông thôn mới",
        "thuỷ lợi", "thuỷ sản", "lâm nghiệp", "chăn nuôi", "giao thông", "xây dựng", "hạ tầng",
        "cơ sở hạ tầng", "quy hoạch", "đô thị", "văn hoá", "thể dục", "thể thao", "du lịch", "di tích",
        "lễ hội", "giáo dục", "đào tạo", "trường học", "phổ cập giáo dục", "y tế", "trạm y tế", "dịch bệnh",
        "phòng chống dịch", "an toàn thực phẩm", "vệ sinh an toàn thực phẩm", "an ninh", "quốc phòng",
        "an ninh quốc phòng", "an ninh trật tự", "trật tự an toàn xã hội", "phòng chống tội phạm",
        "ma tuý", "phòng chống thiên tai", "phòng chống lụt bão", "cứu hộ cứu nạn", "ứng phó sự cố",
        "xoá đói giảm nghèo", "giảm nghèo", "lao động", "việc làm", "bảo hiểm xã hội", "bảo hiểm y tế",
        "người có công", "chính sách xã hội", "hộ tịch", "chứng thực", "tư pháp", "hoà giải", "thương mại",
        "dịch vụ", "công nghiệp", "tiểu thủ công nghiệp", "ngân sách", "thuế", "phí", "lệ phí", "tài chính",
        "tài sản công", "dịch vụ công", "điện chiếu sáng", "cấp nước", "xử lý rác thải", "phòng chống cháy nổ"
    ]

    # Matching logic using disambiguations and keyword occurrences
    # Check UBKT first (disciplinary/control has high specificity)
    if is_ubkt_giamsat or is_ubkt_pctn or is_ubkt_kntc or any(k in text for k in ubkt_keywords if k != "giám sát" and k != "tố cáo" and k != "khiếu nại"):
        return "Uỷ ban kiểm tra Đảng uỷ xã"
        
    # Check VPĐU (internal administration / PCTN policy / office matters)
    if is_vpdu_pctn or any(k in text for k in vpdu_keywords if k != "phòng chống tham nhũng" and k != "tiêu cực" and k != "lãng phí"):
        return "Văn phòng Đảng uỷ xã"
        
    # Check Ban Xây dựng Đảng
    if is_bxd_tuyentruyen or is_bxd_tongiao_dantoc or any(k in text for k in bxd_keywords if k != "tuyên truyền" and k != "tôn giáo" and k != "dân tộc"):
        return "Ban Xây dựng Đảng"
        
    # Check MTTQ
    if is_mttq_giamsat or is_mttq_tuyentruyen or is_mttq_tongiao_dantoc or any(k in text for k in mttq_keywords if k != "mặt trận"):
        return "Uỷ ban Mặt trận Tổ quốc Việt Nam xã"
        
    # Check UBND (if specific administrative task is matched)
    if is_ubnd_kntc or any(k in text for k in ubnd_keywords if k not in ["tư pháp", "y tế", "giao thông", "xây dựng", "giáo dục", "an ninh", "quốc phòng"]):
        return "Uỷ ban nhân dân xã"
        
    # Fallback checking with general keywords
    if any(k in text for k in ["ủy ban nhân dân", "uỷ ban nhân dân", "ubnd", "chính quyền"]):
        return "Uỷ ban nhân dân xã"
    if any(k in text for k in ["mặt trận", "mttq", "đoàn thanh niên", "hội phụ nữ"]):
        return "Uỷ ban Mặt trận Tổ quốc Việt Nam xã"
    if any(k in text for k in ["tuyên truyền", "đảng viên", "xây dựng đảng", "tổ chức"]):
        return "Ban Xây dựng Đảng"

    # Default is Uỷ ban nhân dân xã
    return "Uỷ ban nhân dân xã"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Chuyên Viên Ảo - Hệ Thống Soạn Thảo Công Văn Tự Động**\n\n"
        "Chào bạn! Để tạo công văn giao việc từ xa, bạn chỉ cần gửi file PDF văn bản chỉ đạo của cấp trên vào phòng chat này.\n\n"
        "Tôi sẽ tự động phân tích và gửi lại file Word (.docx) đã được căn lề, định dạng chuẩn hành chính và áp dụng đầy đủ quy tắc nghiệp vụ Khối Đảng."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    pdf_path = None
    try:
        # 1. Validate PDF format
        pdf_name = message.document.file_name
        if not pdf_name.lower().endswith('.pdf'):
            bot.reply_to(message, "⚠️ Vui lòng gửi tệp định dạng PDF (.pdf).")
            return
            
        bot.reply_to(message, "📥 Đang tải tệp tin và tiến hành phân tích...")
        
        # 2. Download PDF file
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        pdf_path = os.path.join(TEMP_DIR, pdf_name)
        with open(pdf_path, 'wb') as f:
            f.write(downloaded_file)
            
        # 3. Extract PDF text
        reader = PdfReader(pdf_path)
        first_page_text = reader.pages[0].extract_text() or ""
        last_page_text = ""
        if len(reader.pages) > 1:
            last_page_text = reader.pages[-1].extract_text() or ""
        
        # Combine text for AI analysis (page 1 + last page to save tokens)
        combined_text = first_page_text
        if last_page_text and last_page_text != first_page_text:
            combined_text += "\n\n--- TRANG CUỐI ---\n\n" + last_page_text

        # 4. Try AI analysis first, then fallback to Rule-based
        analysis_method = ""
        ai_result = analyze_with_gemini(combined_text)
        
        if ai_result:
            # === AI SUCCESS ===
            doc_type = ai_result["doc_type"]
            number = ai_result["number"]
            date_str = ai_result["date"]
            authority = ai_result["authority"]
            title = ai_result["title"]
            co_quan_2 = ai_result["co_quan_2"]
            analysis_method = f"🤖 {ai_result.get('model_used', 'Gemini')}"
        else:
            # === FALLBACK: Rule-based ===
            doc_type, number, date_str, authority, title = parse_pdf_metadata(pdf_path)
            
            if not number or not date_str:
                bot.reply_to(message, "⚠️ Không thể tự động phân tích số hoặc ngày của văn bản này. Vui lòng kiểm tra lại chất lượng tệp PDF.")
                return
                
            co_quan_2 = determine_agency_2(title, first_page_text)
            analysis_method = "⚙️ Hệ thống quy tắc nội bộ"
        
        # 5. Construct payload variables
        van_ban_cap_tren = f"{doc_type} số {number}, ngày {date_str} của {authority} về {title}"
        trich_yeu = f"V/v thực hiện {doc_type} số {number} ngày {date_str} của {authority}"
        
        # Determine output filename based on convention
        short_type = get_short_type(doc_type)
        short_title = get_short_title(title)
        output_name = f"CV tham mưu {short_type} TU về {short_title}.docx"
        # Sanitize filename (remove characters not allowed in windows filenames)
        output_name = re.sub(r'[\\/*?:"<>|]', "", output_name)
        output_path = os.path.join(OUTPUT_DIR, output_name)
        
        # 6. Prepare JSON Data
        data = {
            "van_ban_cap_tren": van_ban_cap_tren,
            "Ngay_den_han_1": "",  # Automatically computed as default (10 days)
            "Co_quan_2": co_quan_2,
            "ngay_den_han_2": "",  # Automatically computed as default (10 days)
            "TRICH_YEU_CONG_VAN": trich_yeu,
            "DANH_SACH_NOI_NHAN": ["Thường trực Đảng ủy", "Các chi bộ trực thuộc", "Lưu VPĐU"]
        }
        
        bot.send_message(
            message.chat.id, 
            f"🔍 **Thông tin trích xuất:**\n"
            f"- Loại văn bản: {doc_type}\n"
            f"- Số hiệu: {number}\n"
            f"- Ngày ban hành: {date_str}\n"
            f"- Cơ quan ban hành: {authority}\n"
            f"- Cơ quan tham mưu: {co_quan_2}\n"
            f"- Phân tích bởi: {analysis_method}\n\n"
            f"⚡ Đang chạy sinh công văn...",
            parse_mode='Markdown'
        )
        
        # 7. Generate the Document
        generate_document(data, TEMPLATE_PATH, output_path)
        
        # 8. Send Word document back to user
        with open(output_path, 'rb') as doc_file:
            bot.send_document(
                message.chat.id, 
                doc_file, 
                caption=f"✅ Đã soạn thảo xong công văn!\n📁 Tên file: {output_name}\n{analysis_method}"
            )
            
    except Exception as e:
        bot.reply_to(message, f"❌ Có lỗi xảy ra trong quá trình xử lý: {str(e)}")
        
    finally:
        # Clean up downloaded PDF file
        if pdf_path and os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception:
                pass


if __name__ == "__main__":
    if API_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN':
        print("[!] LỖI: Vui lòng điền API Token nhận từ @BotFather vào biến API_TOKEN ở dòng 19 trước khi chạy.")
        sys.exit(1)
        
    print("==================================================")
    print("🤖 Chuyên Viên số  đang khởi động...")
    print("Lắng nghe yêu cầu soạn thảo từ xa...")
    print("==================================================")
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\nBot đã dừng hoạt động.")
        sys.exit(0)
