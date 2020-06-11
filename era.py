import asyncio
import inspect
import pkgutil
import threading
from importlib import import_module
from pathlib import Path

from discord.ext import commands

import config
from definitions import COGS_PATH
from webserver import app_quart as app

# CLEAN UP PROJECT STRUCTURE (DELETE, MOVE, REFACTOR!)


class EraBot(commands.Bot):

    bot_token = config.discord['bot_token']
    bot_prefix = config.discord['prefix']

    def __init__(self, **options):
        super().__init__(self.bot_prefix, **options)

        for cog in self.get_cog_classes():
            cog_instance = cog(self)

            if 'twitch' in cog.__name__.lower():
                app.set_cog_loop(cog_instance, asyncio.get_event_loop())

            self.add_cog(cog_instance)

        app_daemon = threading.Thread(target=app.main, daemon=True)
        app_daemon.start()

    def post_twitch_request(self):
        pass

    def get_cog_classes(self) -> []:
        cogs = []
        for (_, name, _) in pkgutil.iter_modules([Path(COGS_PATH + '__init__.py').parent]):
            imported_module = import_module('.' + name, package='cogs')
            attrs = list(filter(lambda x: not x.startswith('__'),
                                     dir(imported_module)))
            for attr in attrs:
                n_type = getattr(imported_module, attr)
                if inspect.isclass(n_type) and issubclass(n_type, commands.Cog):
                    cogs.append(n_type)
        return cogs

    async def run_bot(self):
        await self.login(self.bot_token)

    async def close(self):
        await super().close()


if __name__ == '__main__':
    bot = EraBot()
    bot.run(bot.bot_token)
