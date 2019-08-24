import os

from flask import Flask, session
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


@app.route("/")
def main():
    return "Main page : search engine + user info display + log in / out"

@app.route("/register", methods=["POST"])
def register():
    return "registration page"

@app.route("/error")
def error():
    return "custom error page"

@app.route("/success")
def success():
    return "custom success page"

if __name__ == "__main__":
    app.run(debug = True)
