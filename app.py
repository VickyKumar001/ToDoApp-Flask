from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os

IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    return datetime.now(IST)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=get_ist_time)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"



@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)
    # return "<p>Hello, World!</p>"

@app.route("/show", methods=['GET', 'POST'])
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template("show.html", allTodo=allTodo)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']  
        allTodo = Todo.query.filter((Todo.title.contains(query)) | (Todo.desc.contains(query))).all()
        return render_template("show.html", allTodo=allTodo)
    return render_template("show.html", allTodo=[])

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from env or use 5000
    app.run(debug=True, host='0.0.0.0', port=port)
