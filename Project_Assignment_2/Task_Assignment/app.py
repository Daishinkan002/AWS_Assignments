from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)



#Create db Model
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    #Create a function to return a string when we add something
    def __repr__(self):
        return 'Name' + " " + str(self.id)
    



@app.route('/')
def index():
    title = "TASK_SHEET - OVERVIEW"
    return render_template('index.html', title= title)



@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    title = "ADD TASK"
    if request.method == 'POST':
        task_name = request.form['name']
        task_description = request.form['description']
        new_task = Tasks(name = task_name, description = task_description)

        #Push to Database
        try:
            if((new_task.name != '') and (new_task.description != '')):
                db.session.add(new_task)
                db.session.commit()
            else:
                return 'All fields are mandatory'
            return redirect('/show_task')
        except:
            return "There's something wrong in the addition in Database"
    return render_template('add_task.html', title= title)




@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task_to_update = Tasks.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.name = request.form['name']
        task_to_update.description = request.form['description']
        try:
            db.session.commit()
            return redirect('/show_task')
        except:
            return "There was a problem updating that task"
    else:

        title = "TASKS - UPDATE"
        return render_template('update.html', title= title, task_to_update = task_to_update)



@app.route('/delete/<int:id>', methods = ['POST', 'GET'])
def delete(id):
    task_to_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/show_task')
    except:
        return "there was a problem deleting that task"





@app.route('/show_task')
def show_task():
    title = "ALL TASKS ASSIGNED"
    tasks = Tasks.query.order_by(Tasks.date_created)
    return render_template('show_task.html', title= title, tasks = tasks)



if __name__ == '__main__':
    app.run(debug=True)