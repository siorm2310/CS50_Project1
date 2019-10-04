import os

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

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
    return render_template("index.html")

@app.route("/register", methods=["POST","GET"])
def register():
    return render_template("register.html")

# @app.route("/api/<string:isbn>", methods=["GET"])
# def api_route():
#     return "API book information page"

@app.route("/error")
def error(err_message): # ???
    return render_template("error.html", message = "err_message")

@app.route("/success")
def success():
    return "custom success page"

if __name__ == "__main__":
    app.run(debug = True)
