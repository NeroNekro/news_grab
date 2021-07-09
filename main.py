import os
import feedparser
from datetime import date, timedelta
import configparser as config
import emails
import time

class NewsGrab():
    def __init__(self):
        configPath = f"config.ini"
        conf = config.ConfigParser()
        conf.read(configPath)
        self.host = conf["EMAIL"]["host"]
        self.port = int(conf["EMAIL"]["port"])
        self.user = conf["EMAIL"]["user"]
        self.password = conf["EMAIL"]["pass"]
        self.unsub = conf["CONFIG"]["unsubscribe"]
        datum = date.today() - timedelta(days=int(conf["CONFIG"]["tag"]))
        self.date = datum.strftime('%d').lstrip("0").replace("0", "")

        words = conf["CONFIG"]["words"].split(",")
        self.search_words = []
        for word in words:
            self.search_words.append(word)

        self.mailing_liste = []
        for adr in conf["CONFIG"]["adressen"].split(","):
            self.mailing_liste.append(adr)
        rss_file = open('rss_feeds.txt', 'r')
        self.Lines = rss_file.readlines()
        self.artikel = []
        self.html = ""

    def get_news(self):
        for line in self.Lines:
            feed = feedparser.parse(line)
            for entry in feed.entries:
                article_title = entry.title
                for word in self.search_words:
                    if word in entry.title.lower() and str(entry.published_parsed.tm_mday) == self.date:
                        self.artikel.append({"title": entry.title,
                                        "link": entry.link,
                                        "datum": entry.published})
                        break

    def build_mail(self):
        html = '''Hallo, <br><br>
                    mit dieser Email erhälst du die gestrigen 
                    Nachrichten die eventuell für den Wahlkampf relevant sind.<br><br>'''

        for art in self.artikel:
            html = html + art["title"] + "<br>" + "<a href=\"" + art["link"] + "\" target=\"_blank\">Klick mich</a><br><br>"

        html = html + "Folgende Schlüsselwörter wurden verwendet:<br>"
        for word in self.search_words:
            html = html + word + ", "

        html = html + "<br><br>Folgende Seiten wurden abgefragt:<br>"
        for line in self.Lines:
            html = html + line + "<br><br>"

        html = html + "Falls du keine weiteren Emails erhalten möchtest, schreib einfach eine Mail an " + self.unsub
        self.html = html

    def sendmail(self):
        message = emails.html(html=self.html,
                              subject='Aktuelle Nachrichten für den Wahlkampf',
                              mail_from=('Tobias Jacobs', 'tobi@jacobs.rocks'))
        for receiver in self.mailing_liste:
            r = message.send(to=receiver,
                             smtp={'host':self.host, 'port': self.port, 'ssl': True, 'user': self.user, 'password': self.password})
            if r.status_code not in [250, ]:
                print(r.status_code)
            print(receiver)
            time.sleep(5)

if "__main__" == __name__:
    news = NewsGrab()
    news.get_news()
    news.build_mail()
    news.sendmail()