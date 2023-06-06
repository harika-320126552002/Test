from flask import Flask, render_template, request, redirect
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
# This is a comment
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['task_scheduler']
tasks_collection = db['tasks']
@app.route('/')
def index():
    tasks = tasks_collection.find()
    return render_template('index1.html', tasks=tasks)
@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    timestamp = datetime.now()
    task = {'name': task_name, 'timestamp': timestamp}
    tasks_collection.insert_one(task)
    return redirect('/')
@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = tasks_collection.find_one({'_id': ObjectId(task_id)})
    if request.method == 'POST':
        new_task_name = request.form['new_task_name']
        tasks_collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'name': new_task_name}})
        return redirect('/')
    return render_template('edit_task.html', task=task)
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    tasks_collection.delete_one({'_id': ObjectId(task_id)})
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)