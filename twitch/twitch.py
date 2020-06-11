import json

import requests
from sql_db import db_interface
import config

# FLASK CMD COMMAND: flask run -h 192.168.0.11
# flask run --host=0.0.0.0

headers = {
    'Authorization': f'Bearer {config.twitch["oath_token"]}',
    'Client-ID': f'{config.twitch["client_id"]}'
}


def get_user_id(username: str) -> str:
    r = requests.get(f'https://api.twitch.tv/helix/streams?user_login={username}', headers=headers)
    data = json.loads(r.content)['data']

    if not data:
        print("Invalid username or Stream is currently offline")    # Discord bot sends data here..
        return ''

    print(str("UID: " + str(data[0]['user_id'])))

    return data[0]['user_id']


def setup_stream_on_webhook(user_id: str, username: str, sub=True):

    hook_headers = headers.copy()
    hook_headers['Content-Type'] = 'application/json'

    body = {
        'hub.callback': config.twitch['server_verify'],
        'hub.mode': 'subscribe' if sub else 'unsubscribe',
        'hub.topic': f'https://api.twitch.tv/helix/streams?user_id={user_id}',
        'hub.lease_seconds': '864000'
    }

    r = requests.post('https://api.twitch.tv/helix/webhooks/hub', headers=hook_headers, json=body)
    print("Response: " + str(r.status_code) + " content; " + str(r.content))

    if sub:
        if r.status_code == 202:
            print("Added user..")
            db_interface.add_twitch_user_mapping(user_id, username)
    else:
        print("Removed user..")
        db_interface.remove_twitch_username_mapping(username)


def toggle_webhook(username: str):
    twitch_user_map = db_interface.get_twitch_user_id_map()
    sub = username not in twitch_user_map.keys()
    uid = get_user_id(username) if sub else twitch_user_map[username]

    if uid:
        setup_stream_on_webhook(uid, username, sub)


toggle_webhook('imaemon')
