import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # TODO : add reviews to user

    def add_user(self, username, password):
        new_user = User(username=username, password=password, id=self.id)
        db.session.add(new_user)
        db.session.commit()

class Review():
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, db.ForeignKey("books.id"), nullable=False)
    writer = db.Column(db.String,db.ForeignKey("users.username"), nullable=False)
    body = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)

class Book():
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String , nullable=False)
    title = db.Column(db.String , nullable=False)
    author = db.Column(db.String , nullable=False)
    year = db.Column(db.Integer , nullable=False)