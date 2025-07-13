import os
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import telebot
import webbrowser
from PIL import Image, ImageTk
import sys

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Output Directory
output_dir = "C:/ForensicReports"
os.makedirs(output_dir, exist_ok=True)
report_file_path = ""

# GUI Setup
root = tk.Tk()
root.title("🕵️ ForenSight")
root.geometry("460x430")
root.resizable(False, False)
root.configure(bg="#0f1b2e")

# Set taskbar icon (works with .ico only)
try:
    if getattr(sys, 'frozen', False):
        icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    else:
        icon_path = os.path.abspath("icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"[!] Icon load failed: {e}")

# Optional: Logo Image (emoji or PNG converted to .ico)
logo_label = tk.Label(root, text="🕵️", font=("Helvetica", 32), bg="#0f1b2e", fg="#00aced")
logo_label.pack(pady=(10, 5))

title_label = tk.Label(root, text="ForenSight Tool", font=("Helvetica", 16, "bold"), bg="#0f1b2e", fg="#00aced")
title_label.pack(pady=(0, 10))

status_label = tk.Label(root, text="Status: Ready", font=("Helvetica", 12), bg="#0f1b2e", fg="white")
status_label.pack(pady=(0, 10))

progress_bar = ttk.Progressbar(root, length=340, mode="indeterminate")
progress_bar.pack(pady=(0, 15))

def start_forensic_analysis():
    global report_file_path
    progress_bar.start()
    status_label.config(text="Status: Analyzing...")

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_file_path = os.path.join(output_dir, f"Forensic_Report_{timestamp}.html")

        hostname = subprocess.getoutput("hostname")
        windows_version = subprocess.getoutput("ver")

        sec_logs = subprocess.getoutput("wevtutil qe Security /c:20 /rd:true /f:text")
        app_logs = subprocess.getoutput("wevtutil qe Application /c:20 /rd:true /f:text")
        sys_logs = subprocess.getoutput("wevtutil qe System /c:20 /rd:true /f:text")

        netstat_output = subprocess.getoutput("netstat -an")
        tcp_lines = [line for line in netstat_output.splitlines() if "TCP" in line]
        udp_lines = [line for line in netstat_output.splitlines() if "UDP" in line]
        listening_lines = [line for line in netstat_output.splitlines() if "LISTENING" in line]

        sec_entries = sec_logs.count("Event ID")
        app_entries = app_logs.count("Event ID")
        sys_entries = sys_logs.count("Event ID")

        # Write HTML report
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>🕵️ Forensic Report</title>
<style>
    body {{ background: #0e1628; color: #fff; font-family: Arial; padding: 20px; }}
    .card {{ background: #1c2e4a; padding: 15px; margin-bottom: 15px; border-radius: 10px; }}
    pre {{ background: #0f1d30; padding: 10px; border-radius: 8px; max-height: 300px; overflow: auto; white-space: pre-wrap; }}
    footer {{ text-align: center; font-size: 14px; margin-top: 30px; color: #ccc; }}
    .download-btn {{
        background-color: #2ecc71; color: white; padding: 10px 20px;
        text-decoration: none; border-radius: 5px; font-weight: bold;
        display: inline-block; margin-top: 15px;
    }}
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h1>🕵️ ForenSight Report</h1>

<div class="card">
    <strong>Hostname:</strong> {hostname}<br>
    <strong>Windows Version:</strong> {windows_version}<br>
    <strong>Analysis Time:</strong> {analysis_time}
</div>

<div class="card">
    <strong>Summary:</strong><br>
    Security Logs: {sec_entries} | Application Logs: {app_entries} | System Logs: {sys_entries}<br>
    TCP: {len(tcp_lines)} | UDP: {len(udp_lines)} | Listening: {len(listening_lines)}
</div>

<div class="card">
    <strong>Log Chart:</strong><br>
    <canvas id="logChart" width="400" height="200"></canvas>
</div>

<div class="card"><strong>Security Logs:</strong><pre>{sec_logs}</pre></div>
<div class="card"><strong>Application Logs:</strong><pre>{app_logs}</pre></div>
<div class="card"><strong>System Logs:</strong><pre>{sys_logs}</pre></div>
<div class="card"><strong>TCP Connections:</strong><pre>{chr(10).join(tcp_lines)}</pre></div>
<div class="card"><strong>UDP Connections:</strong><pre>{chr(10).join(udp_lines)}</pre></div>
<div class="card"><strong>Listening Ports:</strong><pre>{chr(10).join(listening_lines)}</pre></div>

<div style="text-align:center;">
    <a class="download-btn" href="Forensic_Report_{timestamp}.html" download>💾 Download This Report</a>
</div>

<footer>
    Report by <strong>🕵️ ForenSight</strong> | 
    <a href="https://github.com/DeadpooHackes/ForenSight" target="_blank" style="color:#00aced;">GitHub Repo</a>
</footer>

<script>
const ctx = document.getElementById('logChart').getContext('2d');
const chart = new Chart(ctx, {{
    type: 'bar',
    data: {{
        labels: ['Security Logs', 'Application Logs', 'System Logs', 'TCP', 'UDP', 'Listening'],
        datasets: [{{
            label: 'Forensic Data Overview',
            data: [{sec_entries}, {app_entries}, {sys_entries}, {len(tcp_lines)}, {len(udp_lines)}, {len(listening_lines)}],
            backgroundColor: ['#e74c3c', '#3498db', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22']
        }}]
    }},
    options: {{
        responsive: true,
        scales: {{
            y: {{ beginAtZero: true }}
        }}
    }}
}});
</script>
</body>
</html>
""")

        try:
            with open(report_file_path, 'rb') as doc:
                bot.send_document(TELEGRAM_CHAT_ID, doc, caption="🕵️ HTML Forensic Report")
        except:
            print("[!] Telegram report sending failed.")

        status_label.config(text="Status: Completed ✅")
        messagebox.showinfo("Success", "Report generated successfully!")

    except Exception as e:
        status_label.config(text="Status: Error ❌")
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
    finally:
        progress_bar.stop()

def open_html_report():
    if not report_file_path or not os.path.exists(report_file_path):
        messagebox.showwarning("Not Found", "No report found. Please run analysis first.")
        return
    webbrowser.open(f"file:///{report_file_path}")

# Buttons
btn_style = {"font": ("Helvetica", 12), "fg": "white", "width": 30, "padx": 10, "pady": 10}
tk.Button(root, text="Start Forensic Analysis", command=start_forensic_analysis, bg="#2ecc71", **btn_style).pack(pady=(5, 10))
tk.Button(root, text="Open HTML Report", command=open_html_report, bg="#3498db", **btn_style).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, bg="#e74c3c", **btn_style).pack(pady=5)

root.mainloop()
