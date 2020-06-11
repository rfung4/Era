import sql_db.db as db


def add_twitch_user_mapping(user_id: str, username: str):
    db.add_twitchuser_row(user_id, username)


def get_twitch_user_id_map():
    return {s[1]: s[0] for s in db.get_twitchuser_rows()}


def remove_twitch_username_mapping(username: str):
    db.remove_twitchuser(username)


if __name__ == '__main__':
    print(str(get_twitch_user_id_map()))
