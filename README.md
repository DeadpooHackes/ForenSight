# ForenSight
Forensic Insight is a powerful desktop application designed for forensic analysts and cybersecurity professionals. It automates the collection of critical system data from Windows environments, enabling fast and structured evidence gathering.
import os
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import telebot
import webbrowser

# Telegram Bot Setup
TELEGRAM_BOT_TOKEN = "5337889327:AAG3gmvlBaNMBN0MySQFamh-Orq1MfQ4z2E"
TELEGRAM_CHAT_ID = "1311015628"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Output Directory
output_dir = "C:/ForensicReports"
os.makedirs(output_dir, exist_ok=True)
report_file_path = ""

# GUI Setup
root = tk.Tk()
root.title("Forensic Insight")
root.geometry("420x380")
root.configure(bg="#1f1f1f")

status_label = tk.Label(root, text="Status: Ready", font=("Helvetica", 12), bg="#1f1f1f", fg="white")
status_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode="indeterminate")
progress_bar.pack(pady=10)

def start_forensic_analysis():
    global report_file_path
    progress_bar.start()
    status_label.config(text="Status: Analyzing...")

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_file_path = os.path.join(output_dir, f"Forensic_Report_{timestamp}.html")

        # System Info
        hostname = subprocess.getoutput("hostname")
        windows_version = subprocess.getoutput("ver")

        # Logs
        sec_logs = subprocess.getoutput("wevtutil qe Security /c:20 /rd:true /f:text")
        app_logs = subprocess.getoutput("wevtutil qe Application /c:20 /rd:true /f:text")
        sys_logs = subprocess.getoutput("wevtutil qe System /c:20 /rd:true /f:text")

        # Network Info
        netstat_output = subprocess.getoutput("netstat -an")
        tcp_lines = [line for line in netstat_output.splitlines() if "TCP" in line]
        udp_lines = [line for line in netstat_output.splitlines() if "UDP" in line]
        listening_lines = [line for line in netstat_output.splitlines() if "LISTENING" in line]

        # Event counts
        sec_entries = sec_logs.count("Event ID")
        app_entries = app_logs.count("Event ID")
        sys_entries = sys_logs.count("Event ID")

        # Generate HTML Report
        with open(report_file_path, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forensic Report</title>
<style>
    body {{ background: #0e1628; color: #fff; font-family: Arial; padding: 20px; }}
    .card {{ background: #1c2b3a; padding: 15px; margin-bottom: 15px; border-radius: 10px; }}
    pre {{ background: #0e1b2d; padding: 10px; border-radius: 8px; max-height: 300px; overflow: auto; white-space: pre-wrap; }}
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
<h1>🕵️ Forensic Insight Report</h1>

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
</html>""")

        # Send HTML to Telegram
        try:
            with open(report_file_path, 'rb') as doc:
                bot.send_document(TELEGRAM_CHAT_ID, doc, caption="🕵️ HTML Forensic Report")
        except:
            print("[!] Failed to send HTML report to Telegram.")

        status_label.config(text="Status: Completed ✅")
        messagebox.showinfo("Success", "Report generated successfully.")

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

# GUI Buttons
tk.Button(root, text="Start Forensic Analysis", font=("Helvetica", 12), command=start_forensic_analysis, bg="#2ecc71", fg="white").pack(pady=20)
tk.Button(root, text="Open HTML Report", font=("Helvetica", 12), command=open_html_report, bg="#3498db", fg="white").pack(pady=10)
tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.quit, bg="#e74c3c", fg="white").pack(pady=10)

root.mainloop()
