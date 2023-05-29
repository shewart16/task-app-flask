from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    completed = db.Column(db.Boolean)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)


@app.route("/create-task/", methods=["POST"])
def new():
    new_task = Task(content=request.form["content"], completed=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect("/")


@app.route("/completed/<int:id>")
def completed(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.completed = not (task.completed)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
