from flask import render_template, flash, request, session

from app import app
from app.models.torrent_manager import TorrentManager


@app.route("/", methods=['GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Hello, you are logged in !'


@app.route('/login', methods=['POST'])
def login():
    if TorrentManager.auth(request.form['username'], request.form['password_api'],
                           request.form['password_tmanager']):
        session['logged_in'] = True
    else:
        flash('Error')
    return home()


@app.route("/logout", methods=['GET'])
def logout():
    session['logged_in'] = False
    return home()
