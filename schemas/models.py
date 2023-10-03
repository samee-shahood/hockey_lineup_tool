from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint

db = SQLAlchemy()

# Define the Player model
class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    position = db.Column(db.String(10))
    skill_level = db.Column(db.Integer)
# Define the Lineup model
class Lineup(db.Model):
    lineup_id = db.Column(db.Integer, primary_key=True)
    lineup_name = db.Column(db.String(50), unique=True)

# Define the PlayerLineup model with a check constraint for slot and unique constraint per lineup
class PlayerLineup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id', ondelete='CASCADE'))
    lineup_id = db.Column(db.Integer, db.ForeignKey('lineup.lineup_id', ondelete='CASCADE'))
    slot = db.Column(db.String(10))

    # Add a check constraint for slot values
    __table_args__ = (
        CheckConstraint(
            db.or_(
                slot.in_(['1LW', '1C', '1RW', '2LW', '2C', '2RW', '3LW', '3C', '3RW', '4LW', '4C', '4RW', '1RD', '2RD', '3RD', '1LD', '2LD', '3LD', 'Starter', 'Backup']),
                slot == None  # Check for null values
            ),
            name='_valid_slot_or_null'
        ),
        UniqueConstraint('lineup_id', 'slot', name='_unique_slot_per_lineup'),
    )