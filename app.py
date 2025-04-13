from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/messages.json'
os.makedirs('data', exist_ok=True)

# Load or initialize message list
def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = load_messages()
    if request.method == 'POST':
        note = request.form['note'].strip()
        if note:
            user_ip = request.remote_addr
            messages.append({
                'text': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': user_ip
            })
            save_messages(messages)
        return redirect(url_for('index'))
    return render_template('index.html', messages=messages)


@app.route('/clear', methods=['POST'])
def clear():
    save_messages([])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
