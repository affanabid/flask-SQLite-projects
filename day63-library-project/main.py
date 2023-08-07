from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

all_books = []

@app.route('/')
def home():
    return render_template('index.html', books=all_books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form.get('title'),
            "author": request.form.get('author'),
            "rating": request.form.get('rating')
        }
        all_books.append(new_book)
        #add the contents to database
        add_book_to_db = Book(title=new_book['title'], author=new_book['author'], rating=new_book['rating'])
        db.session.add(add_book_to_db)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/<id>')
def update_rating(id):
    return f'<h1>{id}</h1>'

class Book(db.Model):
    __tablename__ = 'books'  # Set the table name to 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all() #table created
        except Exception as e:
            print("Error:", e)
    app.run(debug=True)

