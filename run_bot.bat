@echo off
chcp 65001 > nul
title Chuyên Viên Ảo Telegram Bot
echo [INFO] Đang khởi động Chuyên Viên Ảo Telegram Bot...
cd /d "%~dp0"
python -u telegram_bot.py
echo.
echo [WARNING] Bot đã dừng hoạt động. Nhấn phím bất kỳ để thoát.
pause
