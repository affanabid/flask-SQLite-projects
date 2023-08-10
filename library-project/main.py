from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form.get('title'),
            "author": request.form.get('author'),
            "rating": request.form.get('rating')
        }
        #add the contents to database
        add_book_to_db = Book(title=new_book['title'], author=new_book['author'], rating=new_book['rating'])
        db.session.add(add_book_to_db)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    if request.method == 'POST':
        with app.app_context():
            book_to_update = db.session.query(Book).filter_by(id=id).first()
            # book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
            book_to_update.rating = request.form.get('rating')
            db.session.commit() 
        return redirect(url_for('home'))
    else:
        with app.app_context():
            book = db.session.query(Book).filter_by(id=id).first()
            # book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
            title = book.title
            rating = book.rating
    return render_template('edit.html', id=id, rating=rating, title=title)

@app.route('/<int:id>')
def delete(id):
    with app.app_context():
        book_to_delete = db.session.query(Book).filter_by(id=id).first()
        # book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        # or book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

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