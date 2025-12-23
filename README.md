# 🛡️ Quish-Guard: AI-Powered QR Phishing Defense System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%2011-orange?style=for-the-badge&logo=windows)
![Security](https://img.shields.io/badge/Security-Hybrid%20Engine-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Quish-Guard** is an advanced, invisible cybersecurity agent designed to mitigate the rising threat of **"Quishing" (QR Code Phishing)**. Unlike browser extensions that only protect the web, Quish-Guard uses **Computer Vision** to monitor the entire screen layer, protecting users across all applications (Email clients, WhatsApp Desktop, PDFs, Images).

> **Unique Value Proposition:** It features a **"Fail-Safe Hybrid Engine"** that combines Cloud Intelligence (API) with Local Heuristics to catch both known malware and zero-day phishing attacks that haven't been blacklisted yet.

---

## 🧠 System Architecture & Logic
Quish-Guard operates on a non-blocking, multi-threaded architecture to ensure zero impact on system performance.

### 1. 👁️ The "Ghost" Monitor
* **Tech:** `MSS` (Screen Scraping) + `OpenCV`
* **Function:** Silently captures screen frames at **0.2s intervals** (5 FPS) in the background. It converts frames to grayscale for optimized processing speed.

### 2. 🛡️ The Dual-Core Detection Engine
The system uses a decision tree to minimize false negatives:
* **Layer 1 (Cloud Brain):** Queries **VirusTotal API v3** to check if the URL is a known global threat.
* **Layer 2 (Local Brain):** If the API returns "Clean/Unknown" (common for new phishing sites), the **Heuristic Backup** activates. It scans for suspicious keyword patterns (e.g., `login`, `secure`, `bank`, `update`) often used in social engineering.

### 3. ⚡ Intelligent UX Logic
* **Asynchronous Alerts:** Uses `PowerShell` subprocesses to trigger Windows Notifications. This "Fire-and-Forget" method ensures the scanner **never freezes** while waiting for a UI response.
* **Smart Debouncing:** Implements a **300-second (5-minute) cooldown** for duplicate QR codes. This prevents "Alert Fatigue" (spamming the user) while still instantly flagging *new* threats.

---

## 🚀 Key Features
* **👻 True Invisible Mode:** Runs as a background system process without any taskbar icon or window (`--noconsole`).
* **🛑 Zero-Day Protection:** Capable of detecting brand-new fake banking sites that VirusTotal hasn't seen yet.
* **📝 Forensic Logging:** Automatically generates a `QuishGuard_Log.txt` on the Desktop with timestamps and classification reasons (Safe/Malicious/Suspicious).
* **🔋 Efficiency First:** Optimized to use <1% CPU by utilizing thread sleeping and grayscale reduction.

---

## 🛠️ Tech Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Core** | Python 3.12 | Application Logic |
| **Vision** | OpenCV (`cv2`) | QR Code Detection & Decoding |
| **Capture** | MSS | Ultra-fast Screen Capture |
| **Intelligence** | VirusTotal API | Threat Database |
| **OS Integration** | Windows PowerShell | Native Notifications |

---

## ⚙️ Installation & Usage

### Option A: Run the Executable (Recommended)
Download the latest version from the [Releases Page](../../releases).
1.  Download `QuishGuard_Final.exe`.
2.  Double-click to start protection.
3.  *(Optional)* Create a shortcut in `shell:startup` to run on boot.

### Option B: Run from Source
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/santhoshr-15/Quish-Guard.git](https://github.com/santhoshr-15/Quish-Guard.git)
    cd Quish-Guard
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key:**
    * Open `main.py`.
    * Insert your VirusTotal API Key in the configuration section.
4.  **Run:**
    ```bash
    python main.py
    ```

---

## 🔮 Future Roadmap
* [ ] **Entropy Analysis:** Detect random URL strings (e.g., `xy7-z.com`) to catch generated phishing domains.
* [ ] **OCR Integration:** Read text *inside* the QR image (not just the link) to detect fake instructions.
* [ ] **GUI Dashboard:** A simple tray app to view logs and pause protection.

---

## ⚖️ License & Disclaimer
This project is for **Educational Purposes** and **Ethical Hacking Research**.
Licensed under the **MIT License**.