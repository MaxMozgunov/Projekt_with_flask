import sqlite3
from flask import current_app, g

def init_app(add):
    app.cli.add_command(init_db_command)

def init_db_command():
    db = get_db()


def get_db():
    pass