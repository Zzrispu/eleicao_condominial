from flask import render_template
from app import app

@app.get('/')
def homepage():
    return render_template('index.html')