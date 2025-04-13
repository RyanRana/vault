from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime, timedelta

# 1) Import the scanning function from virus.py
from virus import scan_file

app = Flask(__name__)
app.secret_key = "some_secret_key_for_flask_sessions"

DATA_FILE = 'data/messages.json'
TODO_FILE = 'data/todos.json'

# 2) Where we'll temporarily store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs('data', exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ip_name_map = {}
user_last_seen = {}

def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as f:
        return json.load(f)

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f)

def get_active_users():
    active_window = datetime.now() - timedelta(minutes=5)
    return sorted(set(
        name for ip, name in ip_name_map.items()
        if user_last_seen.get(ip, datetime.min) > active_window
    ))

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_ip = request.remote_addr
    user_last_seen[user_ip] = datetime.now()

    if request.method == 'POST':
        name = request.form['name'].strip()
        if name:
            ip_name_map[user_ip] = name
            return redirect(url_for('index'))
    return '''
        <link rel="stylesheet" href="/static/style.css">
        <h1>Enter Your Name</h1>
        <form method="post">
            <input type="text" name="name" placeholder="Your name" required>
            <button type="submit">Continue</button>
        </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def index():
    user_ip = request.remote_addr
    user_last_seen[user_ip] = datetime.now()

    if user_ip not in ip_name_map:
        return redirect(url_for('register'))

    messages = load_messages()

    if request.method == 'POST':
        # Get the note text (if any)
        note = request.form.get('note', '').strip()

        # Check if a file was uploaded
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename:
            # Save file to UPLOAD_FOLDER
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            print("DEBUG: Saved uploaded file to", file_path)

            # Scan with VirusTotal, with error handling if the scan doesn't run.
            try:
                print("DEBUG: Starting VirusTotal scan for file:", file_path)
                is_clean = scan_file(file_path)
                print("DEBUG: VirusTotal scan complete, result:", is_clean)
            except Exception as e:
                flash("VirusTotal scanning did not run due to an error: " + str(e))
                os.remove(file_path)  # remove the file since we can't verify it
                return redirect(url_for('index'))

            if not is_clean:
                flash("Malicious or suspicious file detected! Message NOT saved.")
                os.remove(file_path)  # optionally remove the uploaded file
                return redirect(url_for('index'))
            else:
                flash("File scanned: it appears clean.")

        # If we got here, either no file was uploaded or it was clean => save the note.
        if note:
            messages.append({
                'text': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': user_ip,
                'name': ip_name_map[user_ip]
            })
            save_messages(messages)

        return redirect(url_for('index'))

    return render_template('index.html', messages=messages, active_users=get_active_users())

@app.route('/clear', methods=['POST'])
def clear():
    save_messages([])
    return redirect(url_for('index'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    todos = load_todos()
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        if task:
            todos.append({'task': task})
            save_todos(todos)
        return redirect(url_for('todos'))
    return render_template('todos.html', todos=todos)

@app.route('/delete_todo/<int:index>', methods=['POST'])
def delete_todo(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for('todos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
