import sqlite3
from flask import current_app, g
from dotenv import load_dotenv
import os
import hashlib
import click

load_dotenv()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('users.db')
        g.db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        );
        ''')
        g.db.commit()

    return g.db

def close_db(error=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
        hashed_password = hashlib.sha256('admin_password'.encode()).hexdigest()
        db.execute('''
        INSERT INTO users (username, password, role)
        VALUES ('admin', ?, 'admin');
        ''', (hashed_password,))
        db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
