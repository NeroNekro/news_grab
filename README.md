## Beschreibung
Ein einfacher RSS Reader, der die Nachrichten (Titel) mit bestimmten Schlagwörtern durchsucht und anschließend eine Zusammenfassung per Mail versendet.
Falls keine Nachrichten vorhanden sind, wird auch keine Mail versendet. Weiterhin besteht noch die Möglichkeit die Anbieter mediastack und newscatcher zu aktivieren. Dafür muss nur der API Key in der Config hinterlegt werden. Bei 
nicht Verwendung, dass Feld leer oder apikey stehen lassen. 
Die cron.py sollte täglich mit einem Cronjob aufgerufen werden:
```
0 18 * * * cd /home/news_grab/; python3 cron.py >/dev/null 2>&1
```

Die app.py sollte im produktiven Umfeld mit Gunicorn gestartet werden:
```
gunicorn --user=www-data --group=www-data --bind 0.0.0.0:1234 app:app --daemon
```
Die Webanwendung erstellt beim erstmaligen Stadt eine SQLite3 Datenbank, in der alle Emailadressen gespeichert werden. Meldet sich ein User an, wird dieser
erst die Mails empfangen, wenn in der Email der Aktivierungslink angeklickt wird.

## Config.ini
Zum Betreiben des Tools wird noch eine config.ini benötigt. Die Datei muss sich im gleichen Ordner wie die app.py befinden.
```
[CONFIG]
;0 = heute, 1 = gestern, 2 = vorgestern usw.
tag = 0
;Stichwörter müssen klein sein.
words = grüne,baerbock,kretschmann,bündnis 90/die grünen,habeck
;Link für Aktivierungsmail
activate = https://example.com/aktivieren
unsubscribe = https://example.com/abmelden
[API]
mediastack = apikey
newscatcher = apikey
[EMAIL]
host = smtp.example.com
user = test@example.com
;Angezeigte Mailadresse
showMail = test@example.com
;Angezeigter Name
alias = Der Nachrichtenschubser
port = 465
pass = starkespasswortinklartext
```

## rss_feeds.txt
In jeder Zeile nur ein Feed

## Lizenz
Nur für den privaten Gebrauch kostenlos. Für eine kommerzielle Nutzung schickt mir eine Mail an: tobi@jacobs.network

## Datenschutzbestimmungen und Impressum
Die Datenschutzbestimmungen und das Impressum müssen in die Dateien anmeldung.html und abmeldung.html
ergänzt werden.
