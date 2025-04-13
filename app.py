from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

# 1) Import your virus scanning function
from virus import scan_file  # <--- Make sure the file is named virus.py

app = Flask(__name__)
app.secret_key = "some_secret_key_for_flask_sessions"

DATA_FILE = 'data/messages.json'
UPLOAD_FOLDER = 'uploads'
os.makedirs('data', exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ip_name_map = {}

# Load or initialize message list
def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            ip_name_map[request.remote_addr] = name
            return redirect(url_for('index'))
    return '''
        <h1>Enter Your Name</h1>
        <form method="post">
            <input type="text" name="name" placeholder="Your name" required>
            <button type="submit">Continue</button>
        </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def index():
    user_ip = request.remote_addr

    # First-time visitor? Ask for name
    if user_ip not in ip_name_map:
        return redirect(url_for('register'))

    messages = load_messages()

    if request.method == 'POST':
        note = request.form['note'].strip() if 'note' in request.form else ''
        
        # 2) Check if a file was uploaded
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename:
            # Save file temporarily
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            # 3) Scan with VirusTotal
            is_clean = scan_file(file_path)
            if not is_clean:
                # Malicious => show user an error, do NOT save the message
                flash("Malicious or suspicious file detected! Message NOT saved.")
                os.remove(file_path)  # optionally delete the file
                return redirect(url_for('index'))
            else:
                flash("File scanned: it appears clean.")
                # you can keep or remove the file, depending on your needs

        # 4) If we got here, either no file or it's clean => save the note
        if note:
            messages.append({
                'text': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': user_ip,
                'name': ip_name_map[user_ip]
            })
            save_messages(messages)

        return redirect(url_for('index'))

    return render_template('index.html', messages=messages)

@app.route('/clear', methods=['POST'])
def clear():
    save_messages([])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
