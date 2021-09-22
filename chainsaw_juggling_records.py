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


def validate_no_empty_inputs(name, country, catches):
    while not name:
        name = input('Player name cannot be empty: ')

    while not country:
        country = input('Enter a valid country name: ')

    while not catches:
        catches = input('Now enter number of catches record: ')
        try:
            int(catches)
        except ValueError:
            print('Data given is not a number')
            catches = ''

    return name, country, catches


def add_record(data):
    name = input('Enter player name: ')
    country = input('Which country does this player represents? ')
    catches = input('Now enter number of catches record: ')

    player_name, player_country, number_of_catches = validate_no_empty_inputs(
        name, country, catches)

    player_record = [player_country.title(
    ), [player_name.title(), number_of_catches]]
    data.append(player_record)


# Empty list to store each player data
data = []

# Ask user for Player data to insert into DB tables
enter_record = input("Press 'Y' to add a record or any other key to quit ")

while enter_record.upper() == 'Y':
    add_record(data)
    enter_record = input(
        "Press 'Y' to add another record or any other key to quit ")


# print(data)
for country, player in data:
    country_found = Country.get_or_none(Country.name == country)
    name = player[0]
    catches = player[1]

    if not country_found:
        country = Country.create(name=country)

        Player.create(name=name, number_of_catches=catches,
                      country=country)
        print(f'Player {name} created')
    else:
        Player.create(name=name, number_of_catches=catches,
                      country=country_found)
        print(f'Player {name} created')


countries = Country.select()
for country in countries:
    print(country, country.name)

players = Player.select()
for player in players:
    print(player.name, player.number_of_catches, player.country.name)
