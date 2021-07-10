import os
import feedparser
from datetime import date, timedelta, datetime
import configparser as config
import emails
import time
import http.client, urllib.parse
import json
import urllib
from database import *

class NewsGrab():
    def __init__(self):
        configPath = f"config.ini"
        conf = config.ConfigParser()
        conf.read(configPath)
        self.host = conf["EMAIL"]["host"]
        self.port = int(conf["EMAIL"]["port"])
        self.user = conf["EMAIL"]["user"]
        self.password = conf["EMAIL"]["pass"]
        self.showMail = conf["EMAIL"]["showMail"]
        self.alias = conf["EMAIL"]["alias"]
        self.unsub = conf["CONFIG"]["unsubscribe"]
        self.mediastack = conf["API"]["mediastack"]
        self.newscatcher = conf["API"]["newscatcher"]
        self.days = int(conf["CONFIG"]["tag"])
        datum = date.today() - timedelta(days=self.days)
        self.date = datum.strftime('%d').lstrip("0").replace("0", "")
        self.word_string = conf["CONFIG"]["words"]
        words = conf["CONFIG"]["words"].split(",")
        self.search_words = []
        for word in words:
            self.search_words.append(word)
        rss_file = open('rss_feeds.txt', 'r')
        self.Lines = rss_file.readlines()
        self.artikel = []
        self.html = ""

    def get_rss(self):
        for line in self.Lines:
            feed = feedparser.parse(line)
            for entry in feed.entries:
                for word in self.search_words:
                    if word in entry.title.lower() and str(entry.published_parsed.tm_mday) == self.date:
                        self.artikel.append({"title": entry.title,
                                        "link": entry.link,
                                        "datum": entry.published})
                        break

    def get_news_mediastack(self):
        today = date.today() - timedelta(days=self.days)
        conn = http.client.HTTPConnection('api.mediastack.com')
        params = urllib.parse.urlencode({
            'access_key': self.mediastack,
            'categories': '-general',
            'countries': 'de',
            'languages': 'de',
            'sort': 'published_desc',
            'date': today.strftime('%Y-%m-%d'),
            'limit': 100,
        })
        conn.request('GET', '/v1/news?{}'.format(params))
        res = conn.getresponse()
        data = res.read()
        data = data.decode('utf-8')
        data = json.loads(data)
        for n in data["data"]:
            for word in self.search_words:
                if word in n["title"].lower():
                    self.artikel.append({"title": n["title"],
                                         "link": n["url"],
                                         "datum": n["published_at"]})
                    break



    def get_news_newscatcher(self):
        conn = http.client.HTTPSConnection("newscatcher.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': self.newscatcher,
            'x-rapidapi-host': "newscatcher.p.rapidapi.com"
        }
        conn.request("GET", "/v1/latest_headlines?lang=de&country=de&media=True",
                     headers=headers)

        res = conn.getresponse()
        data = res.read()
        data = data.decode('utf-8')
        data = json.loads(data)
        for n in data["articles"]:
            for word in self.search_words:
                if word in n["summary"].lower():
                    self.artikel.append({"title": n["title"],
                                         "link": n["url"],
                                         "datum": n["published_date"]})
                    break



    def build_mail(self):
        html = '''Hallo, <br><br>
                    mit dieser Email erhälst du die heutigen 
                    Nachrichten die eventuell für den Wahlkampf relevant sind.<br><br>'''


        for art in self.artikel:
            html = html + art["title"] + "<br>" + "<a href=\"" + art["link"] + "\" target=\"_blank\">Klick mich</a><br><br>"

        html = html + "Folgende Schlüsselwörter wurden verwendet:<br>"
        for word in self.search_words:
            html = html + word + ", "

        html = html + "<br><br>Folgende Seiten wurden abgefragt:<br>"
        for line in self.Lines:
            html = html + line + "<br><br>"

        html = html + "Falls du keine weiteren Emails erhalten möchtest, klicke auf folgenden Link: <a href=\"" + self.unsub + "\" target=\"_blank\">Abmelden</a><br><br>"
        self.html = html

    def sendmail(self):
        mailing_liste = Email.select().where(Email.active==1)
        message = emails.html(html=self.html,
                              subject='Aktuelle Nachrichten für den Wahlkampf',
                              mail_from=(self.alias, self.showMail))
        for receiver in mailing_liste:
            r = message.send(to=receiver.email,
                             smtp={'host':self.host, 'port': self.port, 'ssl': True, 'user': self.user, 'password': self.password})
            if r.status_code not in [250, ]:
                print(r.status_code)
            print(receiver.email)
            time.sleep(5)

if "__main__" == __name__:
    news = NewsGrab()
    news.get_rss()
    news.get_news_mediastack()
    news.get_news_newscatcher()
    if len(news.artikel) > 0:
        news.build_mail()
        news.sendmail()