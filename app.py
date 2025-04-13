from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

ip_name_map = {}

app = Flask(__name__)
DATA_FILE = 'data/messages.json'
TODO_FILE = 'data/todos.json'
COMPLETED_FILE = 'data/completed.json'

os.makedirs('data', exist_ok=True)

def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

def save_json(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)

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
    if user_ip not in ip_name_map:
        return redirect(url_for('register'))

    messages = load_json(DATA_FILE)
    if request.method == 'POST':
        note = request.form['note'].strip()
        if note:
            messages.append({
                'text': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': user_ip,
                'name': ip_name_map[user_ip]
            })
            save_json(messages, DATA_FILE)
        return redirect(url_for('index'))

    return render_template('index.html', messages=messages)

@app.route('/clear', methods=['POST'])
def clear():
    save_json([], DATA_FILE)
    return redirect(url_for('index'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    user_ip = request.remote_addr
    user_name = ip_name_map.get(user_ip, 'Anonymous')

    todos = load_json(TODO_FILE)
    completed = load_json(COMPLETED_FILE)

    if request.method == 'POST':
        task = request.form['task'].strip()
        priority = request.form['priority']
        reference = request.form.get('reference', '').strip()
        assignee = request.form.get('assignee', user_name)

        if task:
            todos.append({
                'task': task,
                'priority': priority,
                'reference': reference,
                'assignee': assignee,
                'owner': user_name,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            save_json(todos, TODO_FILE)
        return redirect(url_for('todos'))

    return render_template('todos.html', todos=todos, completed=completed, username=user_name, users=list(set(ip_name_map.values())))

@app.route('/complete_todo/<int:index>', methods=['POST'])
def complete_todo(index):
    todos = load_json(TODO_FILE)
    completed = load_json(COMPLETED_FILE)

    if 0 <= index < len(todos):
        completed_task = todos.pop(index)
        completed_task['completed_by'] = ip_name_map.get(request.remote_addr, 'Someone')
        completed.append(completed_task)
        save_json(todos, TODO_FILE)
        save_json(completed, COMPLETED_FILE)

    return redirect(url_for('todos'))

@app.route('/acknowledge/<int:index>', methods=['POST'])
def acknowledge(index):
    completed = load_json(COMPLETED_FILE)

    if 0 <= index < len(completed):
        user_name = ip_name_map.get(request.remote_addr)
        if completed[index]['owner'] == user_name:
            completed.pop(index)
            save_json(completed, COMPLETED_FILE)

    return redirect(url_for('todos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
