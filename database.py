from peewee import *

db = SqliteDatabase('emails.db', pragmas={'journal_mode': 'wal'})


class Email(Model):
    email = CharField(unique=True)
    key = CharField(unique=True)
    active = IntegerField()

    class Meta:
        database = db
        db_table = "email"

