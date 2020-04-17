from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

#   BU AŞAĞIDAKİ 3 SATIR FİKS EKLENECEK
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/safa_/Desktop/Sifirdan-Ileri-Seviyeye-Python-Programlama-master/WORK/TodoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos=todos)

#   TAMAMLAMA DÖNGÜSÜ   #
@app.route("/complete/<string:id>")     #DİNAMİK URL OLARAK YAZDIK
def completeTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete       #BİR ÜSTTEKİ İF DÖNGÜSÜ İLE AYNI İŞİ YAPIYOR
    db.session.commit()
    return redirect(url_for("index"))

#   TO DO EKLEME DÖNGÜSÜ  #
@app.route("/add",methods= ["POST"])
def addTodo():
    title = request.form.get("title")       #TİTLE DEĞERİNE SAHİP DEĞERİ ALMIŞ OLUYORUZ
    newTodo = Todo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

#   TO DO SİLME İŞLEMİ  #
@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)        #HER YENİ TODO OLUŞTUĞU ZAMAN TAMAMLANMAMIŞ BİR İŞ OLUŞUYOR.BU İŞİ TAMAMLAMIŞSAK VERİTABANIMIZA BUNU TRUE YAPACAĞIZ
                                            #YANİ İKİ DEĞERİMİZ OLACAK. 1 TRUE, 0 FALSE OLACAK

if __name__=="__main__":                    #SERVER I AYAĞA KALDIRMAK İÇİN GEREKLİ
    db.create_all()                         #HER SEFERİNDE YENİ BİR TABLO OLUŞTURMAYACAK.O YÜZDEN BURAYA EKLİYORUZ KOMUTU
    app.run(debug=True)             

