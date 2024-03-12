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
    description = db.Column(db.String(50))
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
    print(task.query.all())
    #print each task
    for task1 in task.query.all():
        print(task1,"task1")
        print(task1.title, "task1.title")
        print(task1.description, "task1.description")
        print(task1.status.value, "task1.status")
        print(task1.due_date, "task1.due_date")
    return render_template('view.html', tasks=task.query.all())


@app.route('/add_todo', methods=['POST'])
def add_todo():
    if request.method == 'POST':
        title = request.json['title']
        description = request.json['description']
        status = request.json['status']
        due_date = request.json['due_date']
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
        new_todo = task(title=title, description=description, status=status, due_date=due_date)
        db.session.add(new_todo)
        db.session.commit()

    return "added"
# delete records from a table
# db.session.delete (model object)

# students.query.filter_by(city = ’Tokyo’).all()

if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development
