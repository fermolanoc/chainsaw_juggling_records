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

    # valid_data = validate_no_empty_inputs(player_name, player_country, number_of_catches)

    player_record = [player_country, [player_name, number_of_catches]]
    data.append(player_record)

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
