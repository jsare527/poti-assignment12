from flask import Flask, render_template, redirect, url_for, request
import time
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def home():
    tasks = []
    with open('todo.txt', 'r') as f:
        for line in f.readlines():
            try:
                split_str = line.strip('\n').split(' ')
                datecreated = datetime.fromtimestamp(int(split_str[0])).strftime('%Y-%m-%d')
                duedate = int(split_str[1])
                current_time = int(time.time())
                description = ' '.join(i for i in split_str if i.isdigit() == False)
                isCompleted = True if split_str[len(split_str) - 1].isdigit() else False
                isOverdue = current_time > duedate and isCompleted == False
                isPending = current_time < duedate and isCompleted == False
                duedate = datetime.fromtimestamp(duedate).strftime('%Y-%m-%d')
                data = {
                    'DateCreated': datecreated,
                    'DueDate': duedate,
                    'Description': description,
                    'IsCompleted': isCompleted,
                    'IsPending': isPending,
                    'IsOverdue': isOverdue,
                    'taskid': split_str[0]
                }
                tasks.append(data)
            except: pass
                
    return render_template('home.html', data=tasks)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        date = str(request.form.get('inputDate'))
        description = request.form.get('inputDescription')
        timecreated = int(time.time())
        expirationDate = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
        with open('todo.txt', 'a') as f:
            f.write(f"{timecreated} {expirationDate} {description}\n")

    return redirect(url_for('home'))

@app.route('/mark_complete/<task_id>', methods=['GET', 'POST'])
def markComplete(task_id):
    with open('todo.txt', 'r') as f:
        tasks = [task.strip('\n').strip() for task in f.readlines()]
    
    lines = []
    for line in tasks:
        parsedId = line.split(' ')[0]
        if parsedId == task_id:
            markedComplete = int(time.time())
            line += f" {markedComplete}"
        lines.append(line)
    
    with open('todo.txt', 'w') as f:
        for line in lines:
            f.write(line + '\n')

    return redirect(url_for('home'))

@app.route('/delete_task/<task_id>', methods=['GET', 'POST'])
def deleteTask(task_id):
    lines = []
    with open('todo.txt', 'r') as f:
        tasks = [task.strip('\n').strip() for task in f.readlines()]
    for line in tasks:
        parseId = line.split(' ')[0]
        if parseId == task_id:
            continue
        else:
            lines.append(line)

    with open('todo.txt', 'w') as f:
        for line in lines:
            f.write(line + '\n')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port='8765')