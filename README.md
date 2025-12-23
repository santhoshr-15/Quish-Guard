# 🛡️ Quish-Guard: AI-Powered Phishing Defense

**Quish-Guard** is a real-time, invisible cybersecurity tool designed to detect and block **"Quishing" (QR Code Phishing)** attacks. It operates as a background service ("Ghost Mode") to monitor screen activity and validate QR codes using a hybrid detection engine.

## 🚀 Key Features
* **👻 Ghost Mode:** Runs invisibly in the background without obstructing workflow.
* **🧠 Hybrid Detection Engine:**
    * **Layer 1:** Checks URLs against the **VirusTotal API** for known global threats.
    * **Layer 2:** Uses a local **Heuristic Algorithm** to catch zero-day phishing patterns (e.g., "login", "bank") that cloud databases miss.
* **⚡ Smart Notifications:** Uses native Windows PowerShell commands for non-blocking, fire-and-forget alerts.
* **⏳ Anti-Spam Logic:** Implements a configurable "Debounce Timer" (default: 5 mins) to prevent repetitive alerts for the same QR code.
* **📂 Audit Logging:** Automatically saves scan results to a local forensic log file.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Computer Vision:** OpenCV (`cv2`)
* **Screen Scraping:** MSS (Ultra-low latency capture)
* **Threat Intel:** VirusTotal API v3
* **System Integration:** Windows PowerShell & Subprocess

## ⚙️ Installation & Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Quish-Guard.git](https://github.com/YOUR_USERNAME/Quish-Guard.git)
    cd Quish-Guard
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key:**
    * Open `main.py`.
    * Replace `PASTE_YOUR_API_KEY_HERE` with your valid VirusTotal API Key.
4.  **Run the tool:**
    ```bash
    python main.py
    ```
    *To stop the tool, use Task Manager or run the provided `Stop_Guard.bat`.*

## 📄 License
This project is open-source and available under the MIT License.