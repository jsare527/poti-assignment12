from flask import Flask, render_template, redirect, url_for, request
import time
from datetime import datetime

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

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
        tasks = [task.strip('/n').strip() for task in f.readlines()]
    
    for line in tasks:
        parsedId = line.split(' ')[0]
        if parsedId == task_id:
            markedComplete = int(time.time())
    
    return redirect(url_for('home'))

@app.route('/delete_task/<task_id>', methods=['GET', 'POST'])
def deleteTask(task_id):
    pass

if __name__ == '__main__':
    app.run(debug=True)