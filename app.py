from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
db = SQLAlchemy(app)

app.app_context().push()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.get("/")
def index():
    tasks = Todo.query.order_by(desc(Todo.id)).all()
    return render_template("index.html", tasks=tasks)


@app.post("/")
def create_task():
    task_content = request.form["task"]
    new_task = Todo(task=task_content)

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")
    except:
        return "adding task failed"


@app.delete("/delete/<int:id>")
def delete_task(id: int):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "unabel to delete the task"


@app.patch("/toggle_task/<int:id>")
def toggle_task(id: int):
    task_to_toggle = Todo.query.get(id)
    if task_to_toggle:
        task_to_toggle.done = True if task_to_toggle.done == False else False
        db.session.add(task_to_toggle)
        db.session.commit()
        return redirect("/")


@app.get("/edit/<int:id>")
def edit(id: int):
    task_to_edit = Todo.query.get(id)
    if task_to_edit:
        return render_template("update.html", task=task_to_edit)

@app.put("/<int:id>")
def update_task(id:int):
    task_to_update = Todo.query.get(id)
    print(task_to_update)
    if task_to_update:
        task_to_update.task = request.form['task']
        db.session.add(task_to_update)
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
