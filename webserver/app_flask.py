import asyncio
from time import sleep

import requests
from flask import Flask
from flask import request
import config

app = Flask(__name__)
ip = config.twitch['server_ip']

# client_id = 'x26yiqajv5s6ipoq16oka4ybqssbom'
# client_secret = 'k6819b7k7oqqts0d4pywk9ywcuds99'
auth_url = 'https://id.twitch.tv/oauth2/token'
twitch_cog = None


@app.route('/auth')
def auth():
    code = request.args.get('code')

    params = {
        'client_id': config.twitch['client_id'],
        'client_secret': config.twitch['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f'http://{ip}/auth'
    }

    r = requests.post(auth_url, params=params)
    print(str("Response: " + str(r.content)))
    return str(r.status_code)


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'hub.challenge' in request.args.keys():
        print(str(request.args.get('hub.challenge')))
        return request.args.get('hub.challenge'), 200

    twitch_cog.post_stream_info(request.json)
    return 'txt', 200


def set_cog(cog):
    global twitch_cog
    twitch_cog = cog


def main():
    app.run(port=5000, host='0.0.0.0', use_reloader=False)


if __name__ == '__main__':
    main()