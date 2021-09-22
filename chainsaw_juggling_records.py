from peewee import *

# Create database
db = SqliteDatabase('chainsaw_juggling_records.sqlite')


# Create Base Model
class RecordModel(Model):
    class Meta:
        database = db


# Model Country to store only country names
class Country(RecordModel):
    name = CharField()


# Model Player to store chainsaw juggling players who are on the record list
class Player(RecordModel):
    name = CharField()
    number_of_catches = IntegerField()
    # foreign key related to Country Model/Table
    country = ForeignKeyField(Country, backref='players')


# Connect to DB and create tables that map to Models Player and Country
db.connect()
db.create_tables([Country, Player])

# Empty list to store each player data
data = []

# Ask user for Player data to insert into DB tables
enter_record = input("Press 'Y' to add a record or any other key to quit ")

while enter_record.upper() == 'Y':
    player_name = input('Enter player name: ')
    player_country = input('Which country does this player represents? ')
    number_of_catches = int(input('Now enter number of catches record: '))

    player_record = (player_country, player_name, number_of_catches)
    data.append(player_record)

    enter_record = input(
        "Press 'Y' to add another record or any other key to quit ")

# print(data)
data_tuple = tuple(data)
# print(data_tuple)
