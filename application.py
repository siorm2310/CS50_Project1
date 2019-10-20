import os

from flask import Flask, session, render_template,redirect,url_for,request,flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=['POST','GET'] )
def main():
    if 'connected_user' in session:
        if request.method == "POST":
            # Check for logout request
            if request.form.get("logoutButton") == "logout":
                session.pop('connected_user',None)
                return redirect(url_for('login'))

            # Check for search request
            isbnSearch = request.form.get("isbnInput")

            if isbnSearch is not None:
                return redirect(url_for('book_page', isbn_num = isbnSearch))
        return render_template("index.html")
    return redirect(url_for('login'))



@app.route("/book/<string:isbn_num>", methods=['GET'] )
def book_page(isbn_num):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn" : isbn_num}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn",{"isbn" : isbn_num}).fetchall()
    if book is None:
        return render_template("error.html", message = "Sorry, ISBN didn't match any book", message_code = 404)

    # TODO: get all book reviews
    return render_template("book_page.html", book = book, reviews = reviews)


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        
        user_to_validate = request.form.get("username")
        pass_to_validate = request.form.get("password")

        db_user = db.execute("SELECT * FROM users WHERE username = :username", 
        {"username" : user_to_validate}).fetchone()

        if db_user is None:
            flash("Sorry, you are not rigstered!")
            return render_template("login.html")

        if (db_user.password != pass_to_validate):
            flash("Sorry, wrong password...")
            return render_template("login.html")

        session['connected_user'] = db_user
        return redirect(url_for('main'))
    return render_template("login.html")


@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        user_to_register = request.form.get("username")
        pass_to_register = request.form.get("password1")
        pass_to_validate = request.form.get("password2")

        if pass_to_register == pass_to_validate:
            if db.execute(f"SELECT * FROM users WHERE username = '{user_to_register}'").rowcount == 0:
                # TODO : register
                db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", 
                {"username" : user_to_register, "password" : pass_to_register})
                db.commit()
                flash("Successfully registered")
                return redirect(url_for('main'))
            flash("Sorry, user already exists")
            return redirect(url_for('register'))
        flash("Sorry, passwords don't match")
        return redirect(url_for('register'))
    return render_template('register.html')

# @app.route("/api/<string:isbn>", methods=["GET"])
# def api_route():
#     return "API book information page"

if __name__ == "__main__":
    app.run(debug = True)
