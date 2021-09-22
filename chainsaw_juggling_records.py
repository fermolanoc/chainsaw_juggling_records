from peewee import *

# Create database
db = SqliteDatabase('chainsaw_juggling_records.sqlite')


# Create Base Model
class Record(Model):
    class Meta:
        database = db
