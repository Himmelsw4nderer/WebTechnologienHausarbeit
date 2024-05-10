from bruno.database.models import Game, players_games
from bruno.database import db
from sqlalchemy import func
from typing import List, Optional
from ..models import User
from werkzeug.security import generate_password_hash
from flask import flash, current_app
from hashids import Hashids


def get_active_games() -> List[dict]:
    """Returns all active games with encoded IDs

    Returns:
        List[dict]: The list of active games with encoded IDs
    """
    active_games_query = db.session.query(
        Game.name,
        Game.id,
        Game.password_hash,
        func.count(players_games.c.user_id).label('player_count')
    ).filter(
        Game.public == 0
    ).outerjoin(
        players_games, players_games.c.game_id == Game.id
    ).group_by(
        Game.id
    ).all()

    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    active_games = [
        {
            'name': game.name,
            'hashed_game_id': hashids.encode(game.id),
            'player_count': game.player_count,
            'password_hash': game.password_hash
        } for game in active_games_query
    ]
    return active_games


def create_games(game_name: str, public: bool, password: str, owner: User) -> Optional[Game]:
    """Create a game by the inputs of the form

    Args:
        game_name (str): The game_name from the form
        public (bool): If the game is public from the form
        password (str): The games password from the form
        owner (User): The games owner

    Returns:
        Optional[Game]: The created game
    """
    try:
        new_game = Game(
            name=game_name,
            owner_id=owner.id,
            public=0 if public else 1,
            password_hash=generate_password_hash(
                password) if password else None
        )
        db.session.add(new_game)
        db.session.commit()
        return new_game
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to create game: {e}")
        return None