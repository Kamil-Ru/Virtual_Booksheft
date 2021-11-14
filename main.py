from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []

# class BooksClass(Flask)

@app.route('/')
def home():
    if not all_books:
        print("books empty")
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    print(all_books)

    if request.method == 'GET':
        return render_template("add.html")

    elif request.method == 'POST':

        book_dic = {
            "title": request.form["Name"],
            "author": request.form["Author"],
            "rating": request.form["Rating"]
        }

        all_books.append(book_dic)
        return render_template("add.html")




if __name__ == "__main__":
    app.run(debug=True)

