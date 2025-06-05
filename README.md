# Message Board Logger

A Python web application that allows users to leave messages for an admin through a simple interface, while discreetly logging keystrokes for educational purposes. Built with Flask, it uses ngrok for public access, generates a QR code for the URL, and provides an admin dashboard to view logs.

## Features
- **Message Board**: Users type messages in a textarea, presented as a "Leave a Message for the Admin" form.
- **Keystroke Logging**: Captures keystrokes (key, code, type, timestamp, IP, User-Agent) and saves to `keylog.txt`.
- **Admin Dashboard**: View the last 50 log entries at `/view-logs`.
- **Ngrok Integration**: Creates a public URL for access, with a shortened version (via TinyURL) and QR code.
- **Persistent Config**: Stores ngrok API key in `config.json` for reuse.
- **Colored Logs**: Concise, color-coded console output for key events and logs.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/message-board-logger.git
   cd message-board-logger


2. Install dependencies:
  ```bash
  pip install flask pyngrok qrcode pillow termcolor pyshorteners
```

3. Obtain an ngrok API key from the ngrok dashboard.
4. Run the script:
  ```bash
  python3 main.py
```

Enter your ngrok API key when prompted (saved to config.json).
Access the public URL (printed in console) or scan qrcode.png to visit the message board.
Type messages in the textarea, logs are saved to keylog.txt.
Visit <public_url>/view-logs to view logged keystrokes and more details.


Educational Use: Designed for learning about web apps, logging, and risks regarding cybersecurity.

File Structure
main.py: Main script with Flask app, ngrok, and QR code generation.
config.json: Stores ngrok API key (created on first run).
keylog.txt: Logs keystrokes and visit details.
qrcode.png: Generated QR code for the public URL.

Future Improvements
Add a user consent form to the UI.
Implement authentication for /view-logs.
Use SQLite for structured log storage.
Gather more info from the user (os version etc...)

