import sys
import subprocess
import threading

def run_telegram():
    print("Starting Telegram Bot...")
    subprocess.run([sys.executable, "telegram_bot.py"])

def run_zalo():
    print("Starting Zalo Bot...")
    subprocess.run([sys.executable, "zalo_bot.py"])

if __name__ == "__main__":
    # Create threads for each bot
    t_telegram = threading.Thread(target=run_telegram, name="TelegramBotThread")
    t_zalo = threading.Thread(target=run_zalo, name="ZaloBotThread")
    
    # Start threads
    t_telegram.start()
    t_zalo.start()
    
    # Wait for both threads to complete (keeps the main process alive)
    t_telegram.join()
    t_zalo.join()
