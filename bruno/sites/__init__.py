from bruno.forms.base import GamePasswordForm
from bruno.database.interaction import get_players_by_game_id, game_has_password, check_game_password
from flask_login import login_required
from flask import Blueprint, render_template, current_app
from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from flask_login.utils import login_required, current_user
from bruno.database import get_active_games, create_games, create_player
from bruno.forms.base import CreateGameForm, JoinGameForm, CreatePlayerForm
from hashids import Hashids
from flask_login import logout_user, login_user

site = Blueprint("sites", __name__,
                 template_folder="templates", url_prefix="/")

@site.get("/")
def index():
    return render_template("index.html")


@site.route("/games/", methods=["GET", "POST"])
@login_required
def games():
    games = get_active_games()
    create_game_form = CreateGameForm(name=current_user.name)
    join_game_form = JoinGameForm()
    if 'create_game_submit' in request.form and create_game_form.validate_on_submit():
        game = create_games(create_game_form.game_name.data,
                            create_game_form.public.data,
                            create_game_form.password.data,
                            current_user)
        hashids = Hashids(salt=current_app.config.get(
            "SECRET_KEY"), min_length=5)
        if game:
            return redirect(url_for('sites.join', hashed_game_id=hashids.encode(game.id)))
    elif 'join_game_submit' in request.form and join_game_form.validate_on_submit():
        return redirect(url_for('sites.join', hashed_game_id=join_game_form.hashed_game_id.data))

    return render_template("games.html", games=games, create_game_form=create_game_form, join_game_form=join_game_form)


@site.route('/choose_name', methods=['GET', 'POST'])
def choose_name():
    """The login and register handler for post and get request. Using
       WTForms to validate the players input. login or register the player

    Returns:
        HTTPResponse: Either the side the player wants to be redirected to or the login and register form
    """
    # TODO redirect after logged in
    create_player_form = CreatePlayerForm(prefix='create_player')
    player = None
    if request.form and create_player_form.validate_on_submit():
        player = create_player(create_player_form.name.data)
    if player:
        login_user(player)
        next = request.args.get('next')
        # TODO possible security risk
        return redirect(next or url_for('sites.index'))
    return render_template('create_player.html', create_player_form=create_player_form)


@site.get("/logout")
def logout():
    """Listens to /logout via get and logs the player out.

    Returns:
        HTTPResponse: The redirect to the index page
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('sites.index'))

@site.route('/join/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def join(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO check for not valid game id
    # TODO check if user is owner then no password
    # TODO redirect if no game
    # TODO check if player in game
    if game_has_password(game_id):
        game_password_form = GamePasswordForm()
        if not (game_password_form.validate_on_submit() and check_game_password(game_id, game_password_form.password.data)):
            return render_template("password.html", hashed_game_id=hashed_game_id, game_password_form=game_password_form)
    players = get_players_by_game_id(game_id)
    return render_template("lobby.html", hashed_game_id=hashed_game_id)


@site.route('/game/<string:hashed_game_id>', methods=['GET', 'POST'])
@login_required
def game(hashed_game_id):
    hashids = Hashids(salt=current_app.config.get("SECRET_KEY"), min_length=5)
    game_id = hashids.decode(hashed_game_id)[0]
    # TODO check if player in game
    return render_template("game.html", hashed_game_id=hashed_game_id)