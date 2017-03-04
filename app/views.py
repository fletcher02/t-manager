from app import app
from flask import render_template
from app.models import TorrentManager

@app.route('/')
def index():
    return render_template('main.html')
