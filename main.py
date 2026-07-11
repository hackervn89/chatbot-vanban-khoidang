import sys
import os
import subprocess
import threading
import time
import json
from flask import Flask, send_from_directory

app = Flask(__name__)

# Resolve output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(script_dir) == "scripts":
    PROJECT_ROOT = os.path.dirname(script_dir)
else:
    PROJECT_ROOT = os.path.join(script_dir, "taovanban_khoidang")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
TEMP_DIR = os.path.join(PROJECT_ROOT, "scripts", "temp")
MAP_FILE = os.path.join(TEMP_DIR, "file_map.json")

def get_file_mapping(file_id):
    """Đọc mapping từ file_id sang tên file Word thực tế"""
    try:
        if os.path.exists(MAP_FILE):
            with open(MAP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(file_id)
    except Exception as e:
        print(f"[File Server Error] Lỗi đọc file_map: {e}")
    return None

@app.route('/')
def home():
    return "🤖 Chuyên Viên Ảo Server is online! Bot Telegram & Zalo đang hoạt động song song."

@app.route('/download/<path:filename>')
def download_file(filename):
    # Thử tra cứu mapping rút gọn trước
    actual_filename = get_file_mapping(filename)
    if actual_filename:
        print(f"[File Server] Đang tải file (Rút gọn): {filename} -> {actual_filename}")
        return send_from_directory(OUTPUT_DIR, actual_filename, as_attachment=True)
        
    # Phục vụ tải trực tiếp (tương thích ngược)
    print(f"[File Server] Đang tải file (Trực tiếp): {filename}")
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

@app.route('/images/<path:filepath>')
def serve_static_image(filepath):
    images_dir = os.path.join(OUTPUT_DIR, "images")
    print(f"[File Server] Đang tải ảnh: {filepath}")
    return send_from_directory(images_dir, filepath)

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Flask File Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

def run_telegram():
    print("Starting Telegram Bot...")
    subprocess.run([sys.executable, "telegram_bot.py"])

def run_zalo():
    print("Starting Zalo Bot...")
    subprocess.run([sys.executable, "zalo_bot.py"])

def file_cleaner_task():
    print("Background File Cleaner started...")
    while True:
        try:
            # 1. Dọn dẹp các tệp Word quá 24h
            if os.path.exists(OUTPUT_DIR):
                now = time.time()
                cutoff = now - 24 * 3600
                for filename in os.listdir(OUTPUT_DIR):
                    file_path = os.path.join(OUTPUT_DIR, filename)
                    if os.path.isfile(file_path):
                        mtime = os.path.getmtime(file_path)
                        if mtime < cutoff:
                            os.remove(file_path)
                            print(f"[Cleaner] Đã xóa file cũ: {filename}")
            
            # 2. Dọn dẹp bảng đối chiếu file_map.json để tránh phình to
            # Chúng ta giữ lại các mapping của các file còn tồn tại trong OUTPUT_DIR
            if os.path.exists(MAP_FILE) and os.path.exists(OUTPUT_DIR):
                with open(MAP_FILE, 'r', encoding='utf-8') as f:
                    mappings = json.load(f)
                
                existing_files = set(os.listdir(OUTPUT_DIR))
                new_mappings = {fid: fname for fid, fname in mappings.items() if fname in existing_files}
                
                if len(new_mappings) != len(mappings):
                    with open(MAP_FILE, 'w', encoding='utf-8') as f:
                        json.dump(new_mappings, f, ensure_ascii=False, indent=2)
                    print(f"[Cleaner] Đã dọn dẹp {len(mappings) - len(new_mappings)} mapping cũ trong file_map.json")
        except Exception as e:
            print(f"[Cleaner Error] {e}")
        # Chạy dọn dẹp mỗi 1 giờ
        time.sleep(3600)

if __name__ == "__main__":
    # Tạo các thread chạy đa nhiệm
    t_web = threading.Thread(target=run_web_server, name="WebServerThread")
    t_telegram = threading.Thread(target=run_telegram, name="TelegramBotThread")
    t_zalo = threading.Thread(target=run_zalo, name="ZaloBotThread")
    t_cleaner = threading.Thread(target=file_cleaner_task, name="CleanerThread", daemon=True)
    
    # Khởi chạy
    t_web.start()
    t_telegram.start()
    t_zalo.start()
    t_cleaner.start()
    
    # Chờ các thread kết thúc
    t_web.join()
    t_telegram.join()
    t_zalo.join()
