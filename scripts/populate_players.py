import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:database@localhost:5432/hockey'  # Replace with your database URI
db = SQLAlchemy(app)

# Define the Player model
class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    position = db.Column(db.String(10))
    skill_level = db.Column(db.Integer)

# Function to populate the players table from a CSV file
def populate_players_table(csv_filename):
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            player = Player(
                first_name=row['first_name'],
                last_name=row['last_name'],
                position=row['position'],
                skill_level=int(row['skill_level'])
            )
            db.session.add(player)

    db.session.commit()

if __name__ == '__main__':
    # Specify the CSV file containing player data
    csv_filename = 'scripts/players.csv'  # Replace with your CSV file name

    # Call the populate_players_table function to insert data into the players table
    populate_players_table(csv_filename)

    print("Player data has been inserted into the players table.")