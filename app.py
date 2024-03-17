import enum
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from sqlalchemy import Enum

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
db = SQLAlchemy(app)


class statusEnum(enum.Enum):
    Backlog = 'Backlog'
    Done = 'Done'
    Pending = 'In Progress'


class task(db.Model):
    id = db.Column('task_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(Enum(statusEnum))
    due_date = db.Column(db.DateTime)


def __init__(self, id, title, description, status, due_date):
    self.id = id
    self.title = title
    self.description = description
    self.status = status
    self.due_date = due_date
db.create_all()


@app.route('/')
def hello_world():

    Tasks=task.query.all()
    #print each task

    return render_template('view.html', tasks=Tasks)


@app.route('/add_todo', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        try:
            title = request.json['title']
            if not title:
                return jsonify({'error': 'Title cannot be empty'}), 400
            description = request.json['description']
            status = request.json['status']
            if status not in ['Pending', 'Backlog', 'Done']:
                return jsonify({'error': 'Invalid status, Please only put "Pending","Done","Backlog"'}), 400
            due_date = request.json['due_date']
            if not due_date:
                return jsonify({'error': 'Due date cannot be empty'}), 400
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except:
                return jsonify({'error': 'Invalid date format, Please use YYYY-mm-dd'}), 400
        except KeyError :
            return jsonify({'Invalid JSON Key': "Ensure the following keys exist 'title','status','due_date','description'"}), 400

        new_todo = task(title=title, description=description, status=status, due_date=due_date)
        db.session.add(new_todo)
        db.session.commit()
    return jsonify({'message': 'New todo created!'}), 200
    # return render_template('view.html', tasks=task.query.all())
# delete records from a table
@app.route('/delete_todo', methods=['DELETE'])
def delete_todo():
    if request.method == 'DELETE':
        id = request.json['id']
        todo = task.query.filter_by(id=id).first()
        db.session.delete(todo)
        db.session.commit()
    return jsonify({'message': 'Todo deleted!'}), 200
    # return render_template('view.html', tasks=task.query.all())

#edit records from a table
@app.route('/edit_todo', methods=['PUT'])
def edit_todo():
    if request.method == 'PUT':
        try:
            id = request.json['id']
            title = request.json['title']
            if not title:
                return jsonify({'error': 'Title cannot be empty'}), 400
            description = request.json['description']
            status = request.json['status']
            if status not in ['Pending', 'Backlog', 'Done']:
                return jsonify({'error': 'Invalid status, Please only put "Pending","Done","Backlog"'}), 400
            due_date = request.json['due_date']
            if not due_date:
                return jsonify({'error': 'Due date cannot be empty'}), 400
            try:
                due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except:
                return jsonify({'error': 'Invalid date format, Please use YYYY-mm-dd'}), 400
        except KeyError :
            return jsonify({'Invalid JSON Key': "Ensure the following keys exist 'id','title','status','due_date','description'"}), 400

        todo = task.query.filter_by(id=id).first()
        todo.title = title
        todo.description = description
        todo.status = status
        todo.due_date = due_date
        db.session.commit()
    return jsonify({'message': 'Todo updated!'}), 200
# students.query.filter_by(city = ’Tokyo’).all()

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
