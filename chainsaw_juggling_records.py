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


"""
Main function with menu
"""


def main():
    # Empty list to store each player data
    data = []

    menu_text = """
    1. Display all records
    2. Add new record
    3. Edit existing record
    4. Delete record 
    5. Quit
    """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_records()
        elif choice == '2':
            add_new_record(data)
        elif choice == '3':
            edit_existing_record()
        elif choice == '4':
            delete_record()
        elif choice == '5':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    print('todo display all records')


def validate_inputs(name, country, catches):
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


def add_new_record(data):
    name = input('Enter player name: ')
    country = input('Which country does this player represents? ')
    catches = input('Now enter number of catches record: ')

    player_name, player_country, number_of_catches = validate_inputs(
        name, country, catches)

    player_record = [player_country.title(
    ), [player_name.title(), number_of_catches]]
    data.append(player_record)
    print('todo add new record. What if user wants to add a record that already exists?')

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
        player_found = Player.get_or_none(Player.name == name)
        if player_found and Player.number_of_catches < catches:
            Player.update(number_of_catches=catches).where(
                name == name and country == country_found)
        else:
            Player.create(name=name, number_of_catches=catches,
                          country=country_found)
            print(f'Player {name} created')


# countries = Country.select()
# for country in countries:
#     print(country, country.name)

# players = Player.select()
# for player in players:
#     print(player.name, player.number_of_catches, player.country.name)


def edit_existing_record():
    print('todo edit existing record. What if user wants to edit record that does not exist?')


def delete_record():
    print('todo delete existing record. What if user wants to delete record that does not exist?')


if __name__ == '__main__':
    main()
