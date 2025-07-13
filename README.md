# 🕵️ Forensic Insight

**Forensic Insight** is a desktop forensic analysis tool for Windows that helps cybersecurity professionals and forensic analysts collect critical system data quickly and generate structured reports. It collects logs, registry data, and network activity, and creates comprehensive HTML reports with built-in charts.

---

## 📦 Features

- ✅ Collects:
  - Windows **Security**, **Application**, and **System** Event Logs
  - **Network activity**: TCP/UDP connections and listening ports
  - **Hostname** and **Windows version**
- 📊 Automatically generates:
  - Interactive **HTML report** with log statistics and charts (via Chart.js)
- 📤 Optional: Send reports via **Telegram bot**
- 🧠 User-friendly **Tkinter GUI**
- 🌐 Offline-safe – skips Telegram if no connection

---
C:\Users\TarunSharma\OneDrive\Desktop\demo learning\Screenshot 2025-07-14 043318.png
C:\Users\TarunSharma\OneDrive\Desktop\demo learning\Screenshot_14-7-2025_43834_.jpeg

---

## 🚀 Getting Started

### 1. 🔧 Requirements

- **Windows OS**
- Python 3.x installed
- Required Python packages:
  ```bash
  pip install telebot
  ```

---

## ⚙️ How to Use

1. Download or clone this repository.
2. Open a terminal or double-click to run the script:
   ```bash
   python forensic_insight.py
   ```
3. Click **"Start Forensic Analysis"** to begin.
4. After completion:
   - The HTML report will open automatically.
   - The report will also be saved to disk (see below).

---

## 📁 Output Location

All generated reports are saved in:

```
C:/ForensicReports/
```

Files are named like:

```
Forensic_Report_YYYYMMDDHHMMSS.html
```

Example:

```
C:/ForensicReports/Forensic_Report_20250713124530.html
```

---

## 📤 Telegram Integration (Optional)

1. Create a bot on [Telegram BotFather](https://t.me/BotFather).
2. Replace this in your script:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
   TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
   ```
3. If online, the bot will send the HTML report to your Telegram chat.

---

## ⚠️ Disclaimer

This tool is for **educational and authorized forensic use only**. Use it responsibly. The author is not liable for misuse.

---

## 👨‍💻 Created By

**Tarun Sharma**  
For any questions, contributions, or improvements — feel free to reach out!
