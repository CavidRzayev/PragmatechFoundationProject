from flask import Flask, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    username = db.Column(db.String, unique=True, nullable= False)
    email = db.Column(db.String, unique=True, nullable=False)
    
   
@app.route('/')
def home ():
   users=User.query.all()  
   return render_template("index.html",userList=users)
   

@app.route("/add", methods = ["GET","POST"])
def add():
       if request.method == "POST":
               user=User(username=request.form["username"], email=request.form["email"])
               db.session.add(user)
               db.session.commit()
               return redirect("/")
               
       return render_template("add.html")
       
       

if __name__ == '__main__':
   app.run(debug = True)