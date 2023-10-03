from flask import Blueprint, request, jsonify
from schemas.models import db, Lineup, Player, PlayerLineup
from sqlalchemy.exc import IntegrityError

lineup_routes = Blueprint('lineup_routes', __name__)

# Create a new lineup
@lineup_routes.route('', methods=['POST'])
def create_lineup():
    data = request.get_json()
    lineup_name = data.get('lineup_name')

    if not lineup_name:
        return jsonify({'error': 'Lineup name is required'}), 400

    new_lineup = Lineup(lineup_name=lineup_name)
    db.session.add(new_lineup)
    db.session.commit()
    return jsonify({'message': 'Lineup created successfully'}), 201

# Get a list of all lineups
@lineup_routes.route('', methods=['GET'])
def get_lineups():
    lineups = Lineup.query.all()
    lineup_list = []
    for lineup in lineups:
        lineup_data = {
            'lineup_id': lineup.lineup_id,
            'lineup_name': lineup.lineup_name
        }
        lineup_list.append(lineup_data)
    return jsonify({'lineups': lineup_list})

# Get lineup details including players
@lineup_routes.route('/<int:lineup_id>', methods=['GET'])
def get_lineup(lineup_id):
    lineup = Lineup.query.get_or_404(lineup_id)

    # Query the players and their positions in the lineup
    player_lineups = PlayerLineup.query.filter_by(lineup_id=lineup_id).all()

    player_data_list = []
    for player_lineup in player_lineups:
        player = Player.query.get(player_lineup.player_id)
        player_data = {
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'position': player.position,
            'slot': player_lineup.slot
        }
        player_data_list.append(player_data)

    lineup_data = {
        'lineup_id': lineup.lineup_id,
        'lineup_name': lineup.lineup_name,
        'players': player_data_list
    }

    return jsonify(lineup_data)

# Add a player to a lineup
@lineup_routes.route('/<int:lineup_id>/add_player', methods=['POST'])
def add_player_to_lineup(lineup_id):
    lineup = Lineup.query.get_or_404(lineup_id)
    data = request.get_json()

    if 'player_id' not in data:
        return jsonify({'error': 'Player ID is required'}), 400

    player_id = data['player_id']

    # Check if the player exists
    player = Player.query.get(player_id)
    if player is None:
        return jsonify({'error': 'Player not found'}), 404

    # Check if the player is already in the lineup
    existing_player_lineup = PlayerLineup.query.filter_by(player_id=player_id, lineup_id=lineup_id).first()
    if existing_player_lineup:
        return jsonify({'error': 'Player is already in the lineup'}), 400

    # Create a new player lineup entry
    player_lineup = PlayerLineup(player_id=player_id, lineup_id=lineup_id)
    
    db.session.add(player_lineup)
    db.session.commit()
    
    return jsonify({'message': 'Player added to the lineup successfully'}), 201

# Delete a player from a lineup
@lineup_routes.route('/<int:lineup_id>/delete_player/<int:player_id>', methods=['DELETE'])
def delete_player_from_lineup(lineup_id, player_id):
    lineup = Lineup.query.get_or_404(lineup_id)
    player = Player.query.get_or_404(player_id)
    
    # Check if the player is in the lineup
    player_lineup = PlayerLineup.query.filter_by(player_id=player_id, lineup_id=lineup_id).first()
    if player_lineup:
        db.session.delete(player_lineup)
        db.session.commit()
        return jsonify({'message': 'Player removed from the lineup successfully'}), 200
    else:
        return jsonify({'error': 'Player is not in the lineup'}), 404

# Update a lineup with players and their slots
@lineup_routes.route('/<int:lineup_id>/update', methods=['PUT'])
def update_lineup(lineup_id):
    try:
        lineup = Lineup.query.get_or_404(lineup_id)
        data = request.get_json()

        if 'players' not in data:
            return jsonify({'error': 'Players data is required'}), 400

        # Retrieve the list of players and their new slots from the request
        players_data = data['players']

        # Get the existing player lineups for the lineup
        existing_player_lineups = PlayerLineup.query.filter_by(lineup_id=lineup_id).all()

        # Create a dictionary to map player IDs to their existing slots
        player_slot_mapping = {player_lineup.player_id: player_lineup.slot for player_lineup in existing_player_lineups}

        # Create a dictionary to track players with slots to update
        players_to_update = {}

        # Iterate through the new player data and update the slots
        for player_data in players_data:
            player_id = player_data.get('player_id')
            new_slot = player_data.get('slot')

            if player_id is None or new_slot is None:
                return jsonify({'error': 'Both player_id and slot are required for each player'}), 400

            if new_slot == "Benched":
                new_slot = None

            # Check if the player is in the lineup
            if player_id not in player_slot_mapping:
                return jsonify({'error': 'Player with ID {} is not in the lineup'.format(player_id)}), 400

            # Track players with slots to update
            players_to_update[player_id] = new_slot

        # Update the player lineups with the new slots (temporary set to null)
        for player_id, new_slot in players_to_update.items():
            player_lineup = PlayerLineup.query.filter_by(player_id=player_id, lineup_id=lineup_id).first()
            player_lineup.slot = None  # Temporarily set to null
            db.session.commit()

        # Now, update the player lineups with the final slots
        for player_id, new_slot in players_to_update.items():
            player_lineup = PlayerLineup.query.filter_by(player_id=player_id, lineup_id=lineup_id).first()
            player_lineup.slot = new_slot
            db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'You can not have multiple players in the same slot'}), 409

    return jsonify({'message': 'Lineup updated successfully'}), 200
