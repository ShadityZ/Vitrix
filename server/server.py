"""
Server version:     v1.1.0
"""

"""
"properties" file:
line 1: MAX_PLAYERS
"""

import os,sys,socket,json,time,random,threading

script_path = os.path.dirname(os.path.abspath(__file__))
print(script_path)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

properties = open(f"{script_path}/properties", 'r').read().split("\n")

from vitrix.lib.api.anticheat import *

ADDR = "0.0.0.0"
PORT = 26822
MAX_PLAYERS = int(properties[0])
MSG_SIZE = 2048


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(MAX_PLAYERS)


players = {}
kicked_users = []
recently_banned_users = []


def ban_user(user: str):
    blacklist_file = open(f"{os.path.dirname(os.path.realpath(__file__))}/blacklist.json", "r")
    blacklist = json.loads(blacklist_file.read())
    blacklist["banned_users"].append(user)
    with open("blacklist.json", "w") as file:
        json.dump(blacklist, file)
    recently_banned_users.append(user)


def is_moderator(user: str):
    moderators_file = open(f"{os.path.dirname(os.path.realpath(__file__))}/moderators.json", "r")
    mods = json.loads(moderators_file.read())["moderators"]
    if user in mods:
        return True
    else:
        return False

def is_banned(user: str):
    blacklist_file = open(f"{os.path.dirname(os.path.realpath(__file__))}/blacklist.json", "r")
    blacklist = json.loads(blacklist_file.read())["banned_users"]
    if user in blacklist:
        return True
    else:
        return False


def generate_id(player_list: dict, max_players: int):
    """
    Generate a unique identifier

    Args:
        player_list (dict): dictionary of existing players
        max_players (int): maximum number of players allowed

    Returns:
        str: the unique identifier
    """

    while True:
        unique_id = str(random.randint(1, max_players))
        if unique_id not in player_list:
            return unique_id


def handle_messages(identifier: str):
    client_info = players[identifier]
    conn: socket.socket = client_info["socket"]
    username = client_info["username"]

    while True:
        if username in recently_banned_users:
            conn.send("banned".encode("utf8"))
            break
        if username in kicked_users:
            conn.send("kicked".encode("utf8"))
            break

        try:
            msg = conn.recv(MSG_SIZE)
        except ConnectionResetError:
            break

        if not msg:
            break

        msg_decoded = msg.decode("utf8")

        try:
            left_bracket_index = msg_decoded.index("{")
            right_bracket_index = msg_decoded.index("}") + 1
            msg_decoded = msg_decoded[left_bracket_index:right_bracket_index]
        except ValueError:
            continue

        try:
            msg_json = json.loads(msg_decoded)
        except Exception as e:
            print(e)
            continue

        if msg_json["object"] == "player":
            players[identifier]["position"] = msg_json["position"]
            players[identifier]["rotation"] = msg_json["rotation"]
            players[identifier]["health"] = msg_json["health"]

        if msg_json["object"] == "command":
            if msg_json["type"] == "ban" and is_moderator(msg_json["author"]):
                ban_user(msg_json["target"])
            if msg_json["type"] == "kick" and is_moderator(msg_json["author"]):
                kicked_users.append(msg_json["target"])

        for player_id in players:
            if player_id != identifier:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]
                try:
                    player_conn.sendall(msg_decoded.encode("utf8"))
                except OSError:
                    pass

    for player_id in players:
        if player_id != identifier:
            player_info = players[player_id]
            player_conn: socket.socket = player_info["socket"]
            try:
                player_conn.send(json.dumps({"id": identifier, "object": "player", "joined": False, "left": True}).encode("utf8"))
            except OSError:
                pass

    print(f"Player {username} with ID {identifier} has left the game...")
    del players[identifier]

    if username in kicked_users:
        kicked_users.remove(username)
    if username in recently_banned_users:
        recently_banned_users.remove(username)

    conn.close()


def main():
    print("Server started, listening for new connections...")

    while True:
        conn, addr = s.accept()
        new_id = generate_id(players, MAX_PLAYERS)
        conn.send(new_id.encode("utf8"))
        username = conn.recv(MSG_SIZE).decode("utf8")
        if is_banned(username):
            conn.send("False".encode("utf8"))
        else:
            conn.send("True".encode("utf8"))
            new_player_info = {"socket": conn, "username": username, "position": (0, 1, 0), "rotation": 0, "health": 150}


            for player_id in players:
                if player_id != new_id:
                    player_info = players[player_id]
                    player_conn: socket.socket = player_info["socket"]
                    try:
                        player_conn.send(json.dumps({
                            "id": new_id,
                            "object": "player",
                            "username": new_player_info["username"],
                            "position": new_player_info["position"],
                            "health": new_player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                    except OSError:
                        pass

            for player_id in players:
                if player_id != new_id:
                    player_info = players[player_id]
                    try:
                        conn.send(json.dumps({
                            "id": player_id,
                            "object": "player",
                            "username": player_info["username"],
                            "position": player_info["position"],
                            "health": player_info["health"],
                            "joined": True,
                            "left": False
                        }).encode("utf8"))
                        time.sleep(0.1)
                    except OSError:
                        pass

            players[new_id] = new_player_info

            msg_thread = threading.Thread(target=handle_messages, args=(new_id,), daemon=True)
            msg_thread.start()

            print(f"New connection from {addr}, assigned ID: {new_id}")



if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        pass

    except SystemExit:
        pass

    finally:
        print("Exiting")
        
        s.close()
