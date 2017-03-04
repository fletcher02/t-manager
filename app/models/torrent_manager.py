from app import app, db
import requests
import datetime
import urllib,urllib2

class TorrentManager(db.Model):
    __tablename__ = 'Table_Test'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<test {}>'.format(self.id)

    @staticmethod
    def auth():
        """
        This method is useful for retrieve T411 Auth token

        Return string token for Header Authorization in POST REQUEST to T411 API
        """

        payload = {"username": app.config["USERNAME_T411"] or 'user',
                   "password": app.config["PASSWORD_T411"] or 'password'}
        r = requests.post(app.config["URL_API_T411"] + "auth", data=payload)
        json_response = r.json()

        try:
            if json_response["token"]:
                app.config.update(TOKEN_T411=json_response["token"])
                app.config.update(TOKEN_T411_VALIDITY=datetime.datetime.now())
                return app.config["TOKEN_T411"]
        except KeyError:
            return json_response["error"]

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