from os import urandom

from app import app

if __name__ == "__main__":
    app.secret_key = urandom(12)
    app.run(debug=app.config["DEBUG"], host=app.config["HOST"], port=app.config["PORT"])
