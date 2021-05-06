var game_id;
var socket;

var game_started_updates;
var updates;

function on_load_into_waiting_room(game_id_local) {
    game_id = game_id_local

    socket = io();

    socket.emit('join', {room: game_id});

    manage_joining();
}

function on_load_game(game_id_local) {
    clearInterval(game_started_updates)

    game_id = game_id_local

    socket = io();

    socket.emit('join', {room: game_id});

    manage_events();
}

function manage_joining() {
    socket.on('game_start', function() {
            window.location.pathname = "/game";
        });
    manage_game_started();
}

function manage_events() {
    socket.on('connect', function() {
            socket.emit('join', {room: game_id});
        });

    socket.on('update', update);

    socket.on('update_players', update_players);

    manage_updates()
}

function attack(game_id, victim_id) {

    let energyElement = document.getElementById('energy_display');
//var b = document.getElementsByTagName('script')[0];

    energyElement.textContent = "Energy: 0.0";

    socket.emit('attack', {game_id: game_id, amount: 10, victim_id: victim_id});
}

function manage_game_started() {
    game_started_updates = setInterval(get_has_game_started, 5000);
}

function manage_updates() {
    updates = setInterval(get_update, 250);
}

function get_has_game_started() {
    socket.emit('check_game_started', {game_id: game_id});
}

function get_update() {
    socket.emit('update', {game_id: game_id});
}

function update(message) {
    update_hp_display(message["hp"], message["max_hp"], message["true_hp"], message["true_max_hp"]);
    update_heal_display(message["heal"]);
    update_armor_display(message["armor"]);
    update_attack_display(message["attack"]);
    update_income_display(message["income"]);
    update_coins_display(message["coins"]);
    update_energy_display(message["energy"]);
    update_level_display(message["level"]);
    update_is_alive(message["is_alive"]);
}

function update_is_alive(new_is_alive) {
    if (!new_is_alive) {

        window.location.reload()

        clearInterval(updates)

        socket.close()
    }
}

function update_level_display(new_level) {
    let levelElement = document.getElementById('level_display');

    levelElement.textContent = "Level: " + String(new_level);
}

function update_hp_display(new_hp, max_hp, true_hp, true_max_hp) {
    let hpElement = document.getElementById('hp_max_hp_display');

    hpElement.textContent = String(new_hp) + " / " + String(max_hp);

    let healthBar = document.getElementById('health');

    healthBar.value = (true_hp / true_max_hp) * 100
}

function update_heal_display(new_heal) {
    let coinsElement = document.getElementById('heal_display');

    coinsElement.textContent = "Healing Rate: " + String(new_heal) + " Units Per Minute";
}

function update_armor_display(new_armor) {
    let coinsElement = document.getElementById('armor_display');

    coinsElement.textContent = "Armor: " + String(new_armor);
}

function update_attack_display(new_attack) {
    let coinsElement = document.getElementById('attack_display');

    coinsElement.textContent = "Attack Strength: " + String(new_attack);
}

function update_income_display(new_income) {
    let coinsElement = document.getElementById('income_display');

    coinsElement.textContent = "Income: " + String(new_income) + " Coins Per Minute";
}

function update_coins_display(new_coins) {
    let coinsElement = document.getElementById('coins_display');

    coinsElement.textContent = "Coins: " + String(new_coins);
}

function update_energy_display(new_energy) {
    let energyElement = document.getElementById('energy_display');

    energyElement.textContent = "Energy: " + String(new_energy);
}

function upgrade(type) {
    let upgradeAmount = document.getElementById('upgrade_amount');

    socket.emit('upgrade', {game_id: game_id, type: type, amount: upgradeAmount.value});

}

function update_players(message) {

    let is_player_alive = message['is_alive']

    let player_id = message['id'];

    let username = message['username'];

    let effective_hp = message['effective_hp'];

    let level = message['level'];

    let playerInfo = document.getElementById("player_" + player_id);

    if(playerInfo != null)
    {

        if(is_player_alive)
        {
            playerInfo.textContent = "Name: " + username + " Level: " + level + " HP: " + effective_hp;
        }
        else
        {
            playerInfo.style.color = "darkred"
            playerInfo.textContent = username + " is Dead";

            let playerAttackButton = document.getElementById("player_" + player_id + "_attack_button");

            playerAttackButton.textContent = null;
        }
    }
}
