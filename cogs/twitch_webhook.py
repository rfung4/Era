import datetime
import json
import urllib

import discord
import requests
from discord.ext import commands
import webserver.app_quart as app
import config
from sql_db import db_interface


class TwitchWebhook(commands.Cog):

    twitch_author_logo = 'https://seeklogo.com/images/T/twitch-tv-logo-51C922E0F0-seeklogo.com.png'
    webhook_channel_id = 649263129422856193

    twitch_user_url = 'https://www.twitch.tv/USERNAME'
    chan = None

    request_auth_headers = {
        'Authorization': f'Bearer {config.twitch["oath_token"]}',
        'Client-ID': f'{config.twitch["client_id"]}'
    }

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def webhook_sub(self, ctx):    # Register webhook for user
        self.chan = ctx.message.channel
        arguments = ctx.message.content.split()[1:]
        username = arguments[0]

        twitch_user_map = db_interface.get_twitch_user_id_map()
        sub = username not in twitch_user_map.keys()
        uid = TwitchWebhook.get_twitch_user_id(username) if sub else twitch_user_map[username]

        if uid:
            result = self.toggle_subscribe_to_webhook(uid, username, sub)
            await ctx.message.channel.send(result)
        else:
            await ctx.message.channel.send("Stream is offline or username entered is invalid")

    async def post_stream_info(self, json):

        posted_json = await json
        print(str(posted_json))

        if not posted_json['data']:
            return  # Stream offline now

        data = posted_json['data'][0]
        username = data['user_name']

        stream_thumbnail = data['thumbnail_url']\
            .replace('{width}', '800').replace('{height}', '600')

        stream_name = data['title']
        twitch_stream_url = self.twitch_user_url.replace("USERNAME", username)

        embed = discord.Embed(title=stream_name, colour=discord.Colour(0xa706bb), url= twitch_stream_url,
                              timestamp=datetime.datetime.utcfromtimestamp(1591441409))

        #embed.set_image(url=stream_thumbnail)
        embed.set_author(name=username + ' is live on Twitch', url= self.twitch_user_url.replace("USERNAME", username),
                         icon_url=self.twitch_author_logo)

        game_id = data['game_id']

        if game_id:
            game_name, game_thumbnail = self.get_game_name_from_id(game_id)
            embed.set_thumbnail(url=game_thumbnail)
            embed.description = f"{game_name}"
            print("Thumbnail: " + game_thumbnail)

        channel = await self.bot.fetch_channel(str(self.webhook_channel_id))
        await channel.send(content='', embed=embed)
        await channel.send(content=twitch_stream_url)


        #await self.post_embed(username=username, description=desc, profile_image='', stream_name='')

    @staticmethod
    def get_twitch_user_id(username: str) -> str:
        print("Getting ID for twitch user: " + username)
        r = requests.get(f'https://api.twitch.tv/helix/streams?user_login={username}', headers=TwitchWebhook.request_auth_headers)
        data = json.loads(r.content)['data']

        if not data:
            print("Invalid username or Stream is currently offline")  # Discord bot sends data here..
            return ''

        return data[0]['user_id']

    @staticmethod
    def get_game_name_from_id(game_id) -> (str, str):
        headers = TwitchWebhook.request_auth_headers.copy()

        r = requests.get(f'https://api.twitch.tv/helix/games?id={str(game_id)}', headers=headers)
        json_response = json.loads(r.content)

        name = urllib.parse.unquote(json_response['data'][0]['name']).strip()
        box_art = json_response['data'][0]['box_art_url'].replace(" ", '')\
            .replace('{width}', '900').replace('{height}', '600')

        return name, box_art

    @staticmethod
    def get_auth_token():
        auth_req_headers = {'client_id': config.twitch['client_id'],
                   'redirect_uri': config.twitch['server_auth'],
                    'response_type': 'token',
                   'scope': 'user_edit'}

        r = requests.get('https://id.twitch.tv/oauth2/authorize', headers=auth_req_headers)

    @staticmethod
    async def generate_embed(username: str, stream_name: str, profile_image: str):

        stream_link = 'https://www.twitch.tv/' + username
        embed = discord.Embed(title=stream_name, colour=discord.Colour(0x9a0bb3),
                              description=f"You can check out the [stream here]({stream_link}) \n\n\n  ```\n{stream_link}``` ",
                              timestamp=datetime.datetime.utcfromtimestamp(1591539147))

        embed.set_thumbnail(url=profile_image)
        embed.set_footer(text="--", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        return embed

    def toggle_subscribe_to_webhook(self, user_id: str, username: str, sub=True):

        hook_headers = self.request_auth_headers.copy()
        hook_headers['Content-Type'] = 'application/json'

        body = {
            'hub.callback': config.twitch['server_verify'],
            'hub.mode': 'subscribe' if sub else 'unsubscribe',
            'hub.topic': f'https://api.twitch.tv/helix/streams?user_id={user_id}',
            'hub.lease_seconds': '864000'
        }

        r = requests.post('https://api.twitch.tv/helix/webhooks/hub', headers=hook_headers, json=body)
        print("Response: " + str(r.status_code) + " content; " + str(r.content))

        if r.status_code != 202:
            return f'Error setting up webhook: ({r.status_code})'

        if sub:
            db_interface.add_twitch_user_mapping(user_id, username)
            print("Added user...")
            return f"Added Webhook subscription for {username}"
        else:
            db_interface.remove_twitch_username_mapping(username)
            print("Removed user..")
            return f"Removed Webhook subscription for {username}"


if __name__ == '__main__':
    wc = TwitchWebhook(None)
    wc.get_game_name_from_id('509672')


# https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=x26yiqajv5s6ipoq16oka4ybqssbom&redirect_uri=http://81.98.31.154:5000/auth&scope=viewing_activity_read&code=
# {'data': [{'game_id': '509672', 'id': '38588959072', 'language': 'en', 'started_at': '2020-06-10T07:24:30Z', 'tag_ids': None, 'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_imaemon-{width}x{height}.jpg', 'title': 'Post fight greg stream', 'type': 'live', 'user_id': '54533417', 'user_name': 'Imaemon', 'viewer_count': 1}]}

