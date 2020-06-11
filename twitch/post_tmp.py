import requests
import config

json = {'data': [{'game_id': '509672', 'id': '38588959072', 'language': 'en', 'started_at': '2020-06-10T07:24:30Z', 'tag_ids': None, 'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_imaemon-{width}x{height}.jpg', 'title': 'Post fight greg stream', 'type': 'live', 'user_id': '54533417', 'user_name': 'Imaemon', 'viewer_count': 1}]}

requests.post(config.twitch['server_verify'], json=json)