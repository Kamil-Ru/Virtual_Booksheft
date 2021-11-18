from pprint import pprint

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # TODO: Delete ?
    def __repr__(self):
        return f"title: {self.title}, author: {self.author}, rating: {self.rating}"


if not os.path.isfile("books-collection.db"):
    db.create_all()


@app.route('/')
def home():
    try:
        all_books = db.session.query(Book).all()
        # all_books = Book.query.all()
        pprint(all_books)
        return render_template("index.html", all_books=all_books)
    except:
        return render_template("index.html")


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':

        new_book = Book(
            title=request.form["Name"],
            author=request.form["Author"],
            rating=request.form["Rating"]
            )
        db.session.add(new_book)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit(book_id):
    book_to_update = Book.query.get(book_id)

    if request.method == 'GET':
        return render_template("edit.html", book=book_to_update)

    elif request.method == 'POST':
        book_to_update.rating = request.form["New Rating"]
        db.session.commit()
        return redirect("/")


@app.route("/delete/<int:book_id>", methods=['GET'])
def delete(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
