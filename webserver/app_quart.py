import asyncio

from quart import Quart, request
import requests
import config

app = Quart(__name__)
ip = config.twitch['server_ip']

auth_url = 'https://id.twitch.tv/oauth2/token'

twitch_cog = None
event_loop = None


@app.route('/auth')
async def auth():
    code = request.args.get('code')

    params = {
        'client_id': config.twitch['client_id'],
        'client_secret': config.twitch['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': f'http://{ip}/auth'
    }

    r = requests.post(auth_url, params=params)
    return str(r.status_code)


@app.route('/verify', methods=['GET', 'POST'])
async def verify():
    if 'hub.challenge' in request.args.keys():
        print(str(request.args.get('hub.challenge')))
        return request.args.get('hub.challenge'), 200

    asyncio.ensure_future(twitch_cog.post_stream_info(request.json), loop=event_loop)
    return 'txt', 200


def set_cog_loop(cog, loop):
    global twitch_cog, event_loop
    twitch_cog = cog
    event_loop = loop


def main():
    app.run(port=5000, host='0.0.0.0', use_reloader=False)


if __name__ == '__main__':
    main()