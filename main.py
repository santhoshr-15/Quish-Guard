import cv2
import numpy as np
import mss
import requests
import time
import base64
import os
import subprocess

# --- 🔐 CONFIGURATION (CONTROL PANEL) 🔐 ---
VT_API_KEY = "PASTE_YOUR_API_KEY_HERE"

# 🛑 TIME LIMIT (in Seconds)
# 300 = 5 Minutes (If you scan the same QR, it waits 5 mins before notifying again)
# 60  = 1 Minute
# 0   = Spam Mode (Notify continuously every scan)
QR_REPEAT_DELAY = 300 
# -------------------------------------------

def log_to_file(status, url):
    """Saves the scan result to a text file on the Desktop."""
    try:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        log_file = os.path.join(desktop, "QuishGuard_Log.txt")
        timestamp = time.strftime("%H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] {status}: {url}\n")
    except Exception:
        pass

def send_notification(title, message):
    """
    Sends a notification via PowerShell (Fire-and-Forget).
    Does not block the scanner.
    """
    # Clean up message to prevent PowerShell errors with special chars
    clean_message = message.replace('"', "'").replace('$', "")
    clean_title = title.replace('"', "'")

    ps_script = f"""
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime] > $null
    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $textNodes = $template.GetElementsByTagName("text")
    $textNodes.Item(0).AppendChild($template.CreateTextNode("{clean_title}")) > $null
    $textNodes.Item(1).AppendChild($template.CreateTextNode("{clean_message}")) > $null
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Quish-Guard")
    $notification = [Windows.UI.Notifications.ToastNotification]::new($template)
    $notifier.Show($notification)
    """
    try:
        subprocess.Popen(["powershell", "-Command", ps_script], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception:
        pass

def check_url_hybrid(url):
    # 1. API CHECK
    if VT_API_KEY != "PASTE_YOUR_VT_API_KEY_HERE" and VT_API_KEY != "":
        try:
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            headers = {"x-apikey": VT_API_KEY}
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                if stats['malicious'] >= 1:
                    return "MALICIOUS", f"Flagged by {stats['malicious']} vendors"
                return "SAFE", "Verified by VirusTotal"
        except:
            pass

    # 2. KEYWORD BACKUP
    suspicious = ["bank", "login", "verify", "update", "secure", "free"]
    if any(w in url.lower() for w in suspicious):
        return "MALICIOUS", "Phishing Keyword Detected"
    
    return "SAFE", "Clean URL"

def start_guard():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        scanned_history = {} # Stores { "http://google.com": 1708123456.0 }
        detector = cv2.QRCodeDetector()

        # Startup Notification
        send_notification("Quish-Guard", f"Active. Repeat Delay: {QR_REPEAT_DELAY}s")

        while True:
            time.sleep(0.2) 
            
            try:
                sct_img = sct.grab(monitor)
                frame = np.array(sct_img)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
                
                value = None
                try:
                    value, points, _ = detector.detectAndDecode(gray)
                except Exception:
                    pass

                if value:
                    current_time = time.time()
                    
                    # --- 🛑 THE TIME LIMIT LOGIC IS HERE 🛑 ---
                    # Check if we have seen this QR before
                    last_seen_time = scanned_history.get(value, 0)
                    
                    # Calculate how long ago we saw it
                    time_passed = current_time - last_seen_time
                    
                    # IF (Never seen before) OR (Time passed > Limit setting)
                    if last_seen_time == 0 or time_passed > QR_REPEAT_DELAY:
                        
                        status, reason = check_url_hybrid(value)
                        
                        clean_msg = f"{reason} - {value[:25]}..."
                        send_notification(f"Quish-Guard: {status}", clean_msg)
                        log_to_file(status, value)
                        
                        # UPDATE the history with the NEW time
                        scanned_history[value] = current_time
                        
            except Exception:
                pass

if __name__ == "__main__":
    start_guard()