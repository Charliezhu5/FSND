from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable SQLA event system, config app so that it can run in python interactive mode
app.config['TEMPLATES_AUTO_RELOAD'] = True # So that no need to redo flask run to see html template change.
db = SQLAlchemy(app)

migrate = Migrate(app, db) # link flask app and db to migrate to use migration funciton.

''' Example with Order, Product, and Order Item(association table)
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
'''

class TodoList(db.Model):
    __tablename__ = "todolists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        print(f'<ID: {self.id}, Description: {self.description}>')

# db.create_all() Since we are using flask migration, we wont be needing db.creat_all.
@app.route('/todos/<todo_id>/del_todo', methods=['GET']) # <> make its content available as argument
def del_todo(todo_id):
    error = False
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()

    except:
        error = True # error flag
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/todos/<todo_id>/set_completed', methods=['POST']) # <> make its content available as argument
def updated_completed(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()

    except:
        error = True # error flag
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return redirect(url_for('index'))

@app.route('/todos/create', methods=['POST']) # listen to url /todos/create with particular method POST.
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description

    except:
        error = True # error flag
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/lists/<list_id>')
def get_list_todos(list_id): # where index is the name of route handler that listens to the route '/'.
    return render_template('index.html', 
    lists=TodoList.query.all(),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
    active_list_name=TodoList.query.get(list_id).name
    ) # always return the list order by id.

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))