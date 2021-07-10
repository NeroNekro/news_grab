from flask import Flask, redirect, render_template, request, flash
from database import *
import uuid
import secrets
import emails
import configparser as config
from emails.template import JinjaTemplate as T

Email.create_table()
app = Flask(__name__, static_url_path='',
                        static_folder='web/static',
                        template_folder='web/templates')

app.secret_key = secrets.token_urlsafe(16)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("anmelden.html")
    if request.method == "POST":
        if request.form.get("privacy") == "1":
            key = uuid.uuid4()
            try:
                Email.insert(email=request.form.get("email"), key=key, active=0).execute()
                flash("Email-Adresse wurde hinzugefügt.")
                sendmail(key, request.form.get("email"))
            except:
                flash("Es ist ein Fehler aufgetreten. Eventuell wurde diese Adresse schon eingetragen.")
        else:
            flash("Bitte stimmen Sie den Datenschutzbestimmungen zu.")
        return redirect("/")


@app.route('/abmelden', methods=['GET', 'POST'])
def abmelden():
    if request.method == "GET":
        return render_template("abmelden.html")
    if request.method == "POST":
        try:
            Email.delete().where(Email.email == request.form.get("email")).execute()
            flash("Email-Adresse wurde entfernt")

        except:
            flash("Email-Adresse nicht im System")

        return redirect("/")

@app.route('/aktivieren/<string:key>', methods=['GET'])
def aktivieren(key):
    Email.update(active=1).where(Email.key == key).execute()
    flash("Anmeldung zum Nachrichten-Netzwerk erfolgreich.")
    return redirect("/")


def sendmail(key, email):
    configPath = f"config.ini"
    conf = config.ConfigParser()
    conf.read(configPath)
    host = conf["EMAIL"]["host"]
    port = int(conf["EMAIL"]["port"])
    user = conf["EMAIL"]["user"]
    showMail = conf["EMAIL"]["showMail"]
    alias = conf["EMAIL"]["alias"]
    password = conf["EMAIL"]["pass"]
    link = conf["CONFIG"]["activate"]
    html = T('''Hallo,<br><br>
    du hast dich für das Nachrichten-Netzwerk angemeldet. Bitte klick auf folgenden Link um deine Anmeldung abzuschließen:
    <a href="{{ link }}/{{ key }}" target=""_blank>Anmeldung abschließend</a>
    
    ''')
    message = emails.html(html=html,
                          subject='Anmeldung für "Aktuelle Nachrichten für den Wahlkampf"',
                          mail_from=(alias, showMail))
    r = message.send(render={"link": link, "key": key},
                    to=email,
                     smtp={'host': host, 'port': port, 'ssl': True, 'user': user,
                           'password': password})
    if r.status_code not in [250, ]:
        pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234)