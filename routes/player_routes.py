from flask import Blueprint, request, jsonify
from schemas.models import db,Player

player_routes = Blueprint('player_routes', __name__)

# Create a new player
@player_routes.route('', methods=['POST'])
def create_player():
    data = request.get_json()
    new_player = Player(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        skill_level=data['skill_level']
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify({'message': 'Player created successfully'}), 201

# Get a list of all players
@player_routes.route('', methods=['GET'])
def get_players():
    players = Player.query.all()
    player_list = []
    for player in players:
        player_data = {
            'player_id': player.player_id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'position': player.position,
            'skill_level': player.skill_level
        }
        player_list.append(player_data)
    return jsonify({'players': player_list})

# Get details of a specific player
@player_routes.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    player = Player.query.get_or_404(player_id)
    player_data = {
        'player_id': player.player_id,
        'first_name': player.first_name,
        'last_name': player.last_name,
        'position': player.position,
        'skill_level': player.skill_level
    }
    return jsonify(player_data)

# Delete a player
@player_routes.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return jsonify({'message': 'Player deleted successfully'})