from flask import Flask,request,redirect,url_for,render_template,send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
import os,os.path
from flask_admin.contrib.sqla import ModelView
 




app=Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/upload'
app.config['PDF_PATH'] = 'static/PDF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/booklist.db'
app.config["SECRET_KEY"] = 'mysecret'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager=Manager(app)
manager.add_command('db', MigrateCommand)

admin = Admin(app)

class BookList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(50), nullable=True)
    genre = db.Column(db.String(50), nullable = True)
    bookpdf =  db.Column(db.String(50), nullable = False)
    bookCoverpic = db.Column(db.String(50), nullable = True)
    bookinformation = db.Column(db.String(50), nullable = True)

admin.add_view(ModelView(BookList, db.session))





@app.route("/")
def index():
   return render_template("index.html")

@app.route("/signup")
def signup():
   return render_template("signup.html")


@app.route("/login")
def login():
   return render_template("login.html")






@app.route("/allbookslist")
def allbooklist():
    books=BookList.query.all()
    return render_template("allbookslist.html", books=books)

@app.route("/upload", methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files ['bookCoverpic']
        f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
        filePath = f"{app.config['UPLOAD_PATH']}/{f.filename}"
        f = request.files ['bookpdf']
        f.save(os.path.join(app.config['PDF_PATH'], f.filename))
        pdfPath = f"{app.config['PDF_PATH']}/{f.filename}"
        booklist = BookList (
            
            bookName = request.form ['bookName'],
            author = request.form ['author'],
            genre = request.form ['genre'],
            bookinformation = request.form['bookinformation'],
            bookCoverpic= filePath,
            bookpdf = pdfPath
        )
        
        db.session.add(booklist)
        db.session.commit()
        return redirect('/allbookslist')
    return render_template ('upload.html')
    
    
@app.route("/delete/<int:id>")
def deleteBook(id):
    book = BookList.query.get(id) 
    db.session.delete(book) 
    db.session.commit()
    return redirect("/allbookslist")    
     
@app.route("/get-pdf/<int:id>",methods = ['GET','POST'])
def get_pdf():

    filename = f"{int:id}.csv"

    try:
        return send_from_directory(app.config["PDF_PATH"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
    

    
    
    
    
    






    
        
    

   
	
if __name__ =='__main__':
    app.run(debug=True)
    manager.run()
    