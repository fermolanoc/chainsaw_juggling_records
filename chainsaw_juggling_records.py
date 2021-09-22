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
    """ Empty list to store each player data
    : this list will be used to populate database tables
    """
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
            name = input('Enter player name you want to update: ').title()
            player_found = Player.get_or_none(Player.name == name)

            if player_found:
                # print(player_found)
                country = input(f'Which country {name} represents? ')
                catches = int(input('Enter new catches record number: '))
                edit_existing_record(catches, player_found, country)
            else:
                print(f'Player {name} is not on our records\n')
        elif choice == '4':
            delete_record()
        elif choice == '5':
            break
        else:
            print('Not a valid selection, please try again')


def display_all_records():
    print('List of Players holders of Chainsaw Juggling Record\n')
    players = Player.select()
    for player in players:
        print(player.name, player.number_of_catches, player.country.name)


def validate_inputs(name, country, catches):
    """ This function will not end until all 3 inputs contain data"""
    while not name:
        name = input('Player name cannot be empty: ')

    while not country:
        country = input('Enter a valid country name: ')

    while not catches:
        catches = input('Now enter number of catches record: ')
        try:  # Once user has input data, try to cast it to integer to verify is not string
            int(catches)
        except ValueError:  # if input data is not an integer, print message and clear catches value to keep asking user to enter data
            print('Data given is not a number')
            catches = ''

    return name, country, catches


def add_new_record(data):
    # Get data from user
    name = input('Enter player name: ')
    country = input('Which country does this player represents? ')
    catches = input('Now enter number of catches record: ')

    # validate that non input is empty and that number_of_catches is converted into integer
    player_name, player_country, number_of_catches = validate_inputs(
        name, country, catches)

    # Create a list with player data
    player_record = [player_country.title(
    ), [player_name.title(), number_of_catches]]

    data.append(player_record)  # insert player record into data list

    # Read data list to get info and populate tables with it
    for country, player in data:
        # Check if country already exists on Country table
        country_found = Country.get_or_none(Country.name == country)

        # Get player name and # of catches
        name = player[0]
        catches = player[1]

    if not country_found:  # If country wasn't found on Country table, then create it
        country = Country.create(name=country)

        # Then save player info into Player table, including country id (FK referencing Country table)
        Player.create(name=name, number_of_catches=catches,
                      country=country)
        print(f'Player {name} created')
    else:  # If country is already on Country table, check if player exists already as well
        player_found = Player.get_or_none(Player.name == name)

        # If player has been created already, check if new number_of_catches data is higher and update row
        if player_found and player_found.number_of_catches < catches:
            edit_existing_record(catches, player_found, country_found)
        else:  # Otherwise, create a new player record using country id that was found already
            Player.create(name=name, number_of_catches=catches,
                          country=country_found)
            print(f'Player {name} has been created')


# countries = Country.select()
# for country in countries:
#     print(country, country.name)


def edit_existing_record(catches, player, country_found):
    Player.update(number_of_catches=int(catches)).where(
        Player.name == player.name and Player.country == country_found).execute()
    print(f'Player: {player.name} record was updated')


def delete_record():
    print('todo delete existing record. What if user wants to delete record that does not exist?')


if __name__ == '__main__':
    main()
