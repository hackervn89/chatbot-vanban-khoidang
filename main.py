import sys
import os
import subprocess
import threading
import time
from flask import Flask, send_from_directory

app = Flask(__name__)

# Resolve output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(script_dir) == "scripts":
    PROJECT_ROOT = os.path.dirname(script_dir)
else:
    PROJECT_ROOT = os.path.join(script_dir, "taovanban_khoidang")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

@app.route('/')
def home():
    return "🤖 Chuyên Viên Ảo Server is online! Bot Telegram & Zalo đang hoạt động song song."

@app.route('/download/<path:filename>')
def download_file(filename):
    print(f"[File Server] Đang tải file: {filename}")
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

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
            if os.path.exists(OUTPUT_DIR):
                now = time.time()
                # 24 hours in seconds
                cutoff = now - 24 * 3600
                for filename in os.listdir(OUTPUT_DIR):
                    file_path = os.path.join(OUTPUT_DIR, filename)
                    if os.path.isfile(file_path):
                        mtime = os.path.getmtime(file_path)
                        if mtime < cutoff:
                            os.remove(file_path)
                            print(f"[Cleaner] Đã xóa file cũ: {filename}")
        except Exception as e:
            print(f"[Cleaner Error] {e}")
        # Run every 1 hour
        time.sleep(3600)

if __name__ == "__main__":
    # Create threads
    t_web = threading.Thread(target=run_web_server, name="WebServerThread")
    t_telegram = threading.Thread(target=run_telegram, name="TelegramBotThread")
    t_zalo = threading.Thread(target=run_zalo, name="ZaloBotThread")
    t_cleaner = threading.Thread(target=file_cleaner_task, name="CleanerThread", daemon=True)
    
    # Start threads
    t_web.start()
    t_telegram.start()
    t_zalo.start()
    t_cleaner.start()
    
    # Keep main thread alive
    t_web.join()
    t_telegram.join()
    t_zalo.join()
