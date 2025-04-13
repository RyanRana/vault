from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = 'data/messages.json'
os.makedirs('data', exist_ok=True)

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
        note = request.form['note'].strip()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
