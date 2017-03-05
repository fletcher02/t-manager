import requests
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db


class TorrentManager(db.Model):
    __tablename__ = 'api_tokens'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(64), index=True)
    token = db.Column(db.String(64), index=True)
    password_tmanager = db.Column(db.String(256))

    def __repr__(self):
        return '<test {}>'.format(self.id)

    @staticmethod
    def auth(user, password_t411, password_tmanager):
        """
        This method is useful for retrieve T411 Auth token

        Return string token for Header Authorization in POST REQUEST to T411 API
        """

        try:
            # request if user already exists in database
            found_user = False
            check_user = TorrentManager.query.filter(TorrentManager.login_id == user).first()
            if check_user is not None:
                if check_password_hash(check_user.password_tmanager, password_tmanager):
                    # password OK !
                    found_user = True

            if not found_user:
                payload = {"username": user,
                           "password": password_t411}
                r = requests.post(app.config["URL_API_T411"] + "auth", data=payload)
                json_response = r.json()

                if json_response["token"]:
                    # store password_tmanager + login and token in database
                    pw_hash = generate_password_hash(password_tmanager)
                    new_user = TorrentManager(login_id=user, token=json_response["token"], password_tmanager=pw_hash)
                    db.session.add(new_user)
                    db.session.commit()

                    # app.config.update(TOKEN_T411=json_response["token"])
                    # app.config.update(TOKEN_T411_VALIDITY=datetime.datetime.now())
                    return True
            else:
                return True

        except KeyError:
            # return json_response["error"]
            return False


    @staticmethod
    def search(name, category=False):
        if category == False:
            url = app.config["URL_API_T411"] + "torrents/search/" + name + "?limit=10"
            headers = {"Authorization": TorrentManager.auth()}
            r = requests.get(url, headers=headers)

            return r.json()["torrents"]

        elif category != False:
            return "coucou"

    @staticmethod
    def download(id):
        url = app.config["URL_API_T411"] + "torrents/download/" + id
        headers = {"Authorization": TorrentManager.auth()}
        r = requests.get(url, headers=headers)

        with open('file.torrent','wb') as f:
            f.write(r.content)