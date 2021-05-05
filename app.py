from flask import Flask, render_template, request, redirect, session, send_from_directory
import os
import sys
from flask_session import Session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Include application directories in the path to allow imports
sys.path.insert(1, DIRECTORY + "/static/entities/")
sys.path.insert(1, DIRECTORY + "/static/")

from helpers import *
from User import User, get_user_by_id
from Player import Player
from Game import Game, get_previous_games

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == '__main__':
    socketio.run(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id, is_authenticated = session.get("is_authenticated"))

@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('error_403.html'), 403

@app.errorhandler(401)
def unauthenticated(error):
    return redirect("/login")

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error_500.html'), 500

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



#               Verification pages



@app.route("/register", methods = ["GET"])
def register():
    if not session.get("is_authenticated"):
        return render_template("register.html", invalid = request.args.get("invalid"))
    else:
        return redirect("/logout")

@app.route("/register", methods = ["POST"])
def register2():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if not username or not password or not confirm_password or not password == confirm_password:
        return redirect("/register?invalid=1")
    else:

        new_user = User(username = username, password = password)

        if new_user.create():

            user_id = new_user.get_id()

            login_user(new_user, remember=True)

            session["is_authenticated"] = True
            session["user_id"] = user_id
            session["username"] = username

            return redirect("/")
        else:
            return redirect("/register?invalid=1")

@app.route("/login", methods = ["GET"])
def login():
    if not session.get("is_authenticated"):
        return render_template("login.html", invalid = request.args.get("invalid"))
    else:
        return redirect("/logout")

@app.route("/login", methods = ["POST"])
def login2():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User(username = username, password = password)
    is_correct_password = user.authenticate()

    if is_correct_password:

        login_user(user, remember=True)

        user_id = user.get_id()

        session["is_authenticated"] = True
        session["user_id"] = user_id
        session["username"] = username

        return redirect("/")

    else:
        return redirect("/login?invalid=1")

@app.route("/logout", methods = ["GET"])
def logout():
    return render_template("logout.html")

@app.route("/logout", methods = ["POST"])
def logout2():
    logout_user()
    session.clear()
    return redirect("/")



#             Game-Related Pages



@app.route("/about", methods = ["GET"])
def about():
    return render_template("about.html")

@app.route("/games", methods = ["GET"])
@login_required
def games():

    games = get_game_objects(joinable = True)

    can_create_games = current_user.get_can_create_games()

    return render_template("games.html", games = games)

@app.route("/games", methods = ["POST"])
@login_required
def games2():

    game_id = request.form.get("game_id")

    current_game = Game(id = game_id)

    joining_successful = current_game.attempt_to_join(current_user)

    if joining_successful:
        return redirect("/waiting_room?game_id=" + game_id);

    else:
        return redirect("/games");

@app.route("/waiting_room", methods = ["GET"])
@login_required
def waiting_room():

    game_id = request.args.get("game_id")

    return render_template("waiting_room.html", game_id = game_id, is_logged_in = session.get("is_authenticated"))

@app.route("/game", methods = ["GET"])
@login_required
def game():

    game_id = request.args.get("game_id")

    current_game = Game(id = game_id)

    current_game.check_is_done()

    if not current_game.get_has_started():
        return forbidden(None)

    current_player = Player(user = current_user, game = current_game)

    current_player.get_stats()

    current_player.update_timestamp_to_now_if_unchanged()

    all_players = get_player_objects(current_game)

    return render_template("game.html", game_id = game_id, current_player = current_player, players = all_players)

@app.route("/create_game", methods = ["GET"])
@login_required
def create_game():

    can_create_games = current_user.get_can_create_games()

    if not can_create_games:
        return forbidden(None)

    return render_template("create_game.html", invalid = request.args.get("invalid"))

@app.route("/create_game", methods = ["POST"])
@login_required
def create_game2():

    can_create_games = current_user.get_can_create_games()

    if not can_create_games:
        return forbidden(None)

    number_of_slots = request.form.get("number_of_players")
    waiting_time = request.form.get("waiting_time")

    if (not number_of_slots) or (not waiting_time):
        return redirect("/create_game?invalid=1")

    number_of_slots = int(number_of_slots)
    waiting_time = int(waiting_time)

    if number_of_slots < 2:
        return redirect("/create_game?invalid=1")

    new_game = Game(game_creator = current_user, available_slots = number_of_slots, wait_time = waiting_time)

    new_game.create()

    return redirect("/")



# Other Pages



@app.route("/account", methods = ["GET"])
@login_required
def account():

    previous_games = get_previous_games(current_user)

    return render_template("account.html", previous_games = previous_games)



# SocketIO Events



@socketio.on('join')
def on_join(json):

    room = json['room']
    join_room(room)

@socketio.on('leave')
def on_leave(json):

    room = json['room']
    leave_room(room)

@socketio.on('attack')
def player_event_attack(json):

    game_id = json['game_id']

    victim_id = json['victim_id']

    victim = Player(id = victim_id)

    current_game = Game(id = game_id)

    current_player = Player(user = current_user, game = current_game)

    current_player.get_stats()

    current_player.attack_player(victim)

    data = victim.get_broadcasting_data()

    emit('update_players', broadcast_data, room = game_id)

@socketio.on('upgrade')
def player_event_upgrade(json):

    game_id = json['game_id']

    upgrade_type = json['type']
    upgrade_amount = json['amount']

    current_game = Game(id = game_id)

    current_player = Player(user = current_user, game = current_game)

    current_player.upgrade(upgrade_type, upgrade_amount)

    data = current_player.get_display_data()

    emit('update', data)

@socketio.on('update')
def event_update(json):

    game_id = json['game_id']

    current_game = Game(id = game_id)

    current_player = Player(user = current_user, game = current_game)

    current_player.update_stats()

    data = current_player.get_display_data()

    broadcast_data = current_player.get_broadcasting_data()

    emit('update', data)

    emit('update_players', broadcast_data, room = game_id)

@socketio.on('check_game_started')
def event_check_game_started(json):

    game_id = json['game_id']

    current_game = Game(id = game_id)

    if current_game.get_has_started():

        emit('game_start', room = game_id)
