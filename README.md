##Beschreibung
Ein einfacher RSS Reader, der die Nachrichten (Titel) mit bestimmten Schlagwörtern durchsucht und anschließend eine Zusammenfassung per Mail versendet

##Config.ini
Zum Betreiben des Tools wird noch eine config.ini benötigt. Die Datei muss sich im gleichen Ordner wie die main.py befinden.
```
[CONFIG]
;0 = heute, -1= gestern, -2 = vorgestern usw.
tag = 0
;Stichwörter müssen klein sein.
words = grüne,baerbock,kretschmann,bündnis 90/die grünen,habeck
adressen = test1@test.de,mustermann@test.de,musterfrau@test.de
;Wird ans Ende der Mail gehangen. Eine automatische Abmneldung ist nicht möglich
unsubscribe = abmeldung@test.de
[EMAIL]
host = smtp.example.com
user = test@example.com
port = 465
pass = starkespasswortinklartext
```

##Lizenz
Ein Backlink oder Hinweis zum Author wären nett :)
