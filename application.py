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
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/book/<string:isbn_num>", methods=['POST','GET'] )
def book_page(isbn_num):
    book = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn_num}'").fetchone()
    if book is None:
        return render_template("error.html", message = "Sorry, ISBN didn't match any book", message_code = 404)

    # TODO: get all book reviews
    return render_template("book_page.html", book = book)


@app.route("/login", methods=["POST","GET"])
def login():
    session.pop('connected_user',None)
    if request.method == "POST":
        
        user_to_validate = request.form.get("username")
        pass_to_validate = request.form.get("password")

        db_user = db.execute(f"SELECT * FROM users WHERE username = '{user_to_validate}'").fetchone()
        if db.execute(f"SELECT * FROM users WHERE username = '{user_to_validate}'").rowcount == 0:
            return render_template("error.html", message = "Sorry, you are not registered", message_code = 400)
            # return render_template("login.html")
        if (db_user.password != pass_to_validate):
            return render_template("error.html", message = "Sorry, wrong password", message_code = 400)
        session['connected_user'] = user_to_validate
        return redirect(url_for('main'))
    return render_template("login.html")


@app.route("/register", methods=["POST","GET"])
def register():
    # TODO : check if user exists. if not, create and redirect to index
    user_to_register = request.form.get("username")
    pass_to_register = request.form.get("password1")
    pass_to_validate = request.form.get("password2")

    if pass_to_register == pass_to_validate:
        if db.execute(f"SELECT * FROM users WHERE username = '{user_to_register}'").rowcount == 0:
            # TODO : register
            db.execute(f"INSERT INTO users VALUES ('{user_to_register}', '{pass_to_register}')")
            return redirect(url_for('main'))
        flash("Sorry, user already exists")
        return redirect(url_for('register'))
    flash("Sorry, passwords don't match")
    return redirect(url_for('register'))

# @app.route("/api/<string:isbn>", methods=["GET"])
# def api_route():
#     return "API book information page"

@app.route("/error")
def error(err_message): # ???
    return render_template("error.html", message = err_message)

@app.route("/success")
def success():
    return "custom success page"

if __name__ == "__main__":
    app.run(debug = True)
