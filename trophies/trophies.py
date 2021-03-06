# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2017 SML

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.ext import commands
from random import choice
from .utils.dataIO import dataIO
from __main__ import send_cmd_help

import os

settings_path = "data/trophies/settings.json"
CLANS = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'eSports']
set_allowed_role = 'Bot Commander'

class Trophies:
    """
    Display the current trophy requirements for RACF

    Note: RACF specific plugin for Red
    """

    def __init__(self, bot):
        self.bot = bot
        self.file_path = settings_path
        self.settings = dataIO.load_json(self.file_path)

    @commands.group(pass_context=True, no_pm=True)
    async def trophies(self, ctx):
        """Display RACF Trophy requirements"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @trophies.command(name="show", pass_context=True, no_pm=True)
    async def _show_trophies(self, ctx):
        """Display the requirements"""

        server = ctx.message.server

        if server.id not in self.settings:
            self.settings[server.id] = {
                "ServerName": str(server),
                "ServerID": str(server.id),
                "Trophies": {}}

        for c in CLANS:
            if c not in self.settings[server.id]["Trophies"]:
                self.settings[server.id]["Trophies"][c] = "0"

        color = ''.join([choice('0123456789ABCDEF') for x in range(6)])
        color = int(color, 16)

        data = discord.Embed(
            color=discord.Color(value=color),
            title="Trophy requirements",
            description="Minimum trophies to join our clans. "
                        "Current trophies required. "
        )

        for clan in CLANS:
            if clan.lower() in self.settings[server.id]["Trophies"]:
                name = clan
                value = self.settings[server.id]["Trophies"][clan.lower()]

                if value.isdigit():
                    value = '{:,}'.format(int(value))

                data.add_field(name=str(name), value=value)

        if server.icon_url:
            data.set_author(name=server.name, url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        await self.bot.say(embed=data)

    @trophies.command(name="set", pass_context=True, no_pm=True)
    @commands.has_role(set_allowed_role)
    async def _set_trophies(self, ctx, clan: str, req: str):
        """Set the trophy requirements for clans"""
        server = ctx.message.server

        if server.id not in self.settings:
            self.settings[server.id] = {
                "ServerName": str(server),
                "ServerID": str(server.id),
                "Trophies": {}}

        for c in CLANS:
            if c not in self.settings[server.id]["Trophies"]:
                self.settings[server.id]["Trophies"][c.lower()] = "0"

        if clan.lower() not in [c.lower() for c in CLANS]:
            await self.bot.say("Clan name is not valid.")

        else:
            self.settings[server.id]["Trophies"][clan.lower()] = req
            await self.bot.say("Trophy requirement for {} updated to {}.".format(clan, req))

        dataIO.save_json(self.file_path, self.settings)



def check_folder():
    if not os.path.exists("data/trophies"):
        print("Creating data/trophies folder...")
        os.makedirs("data/trophies")


def check_file():
    d = {}

    f = settings_path
    if not dataIO.is_valid_json(f):
        print("Creating default trophies‘ settings.json...")
        dataIO.save_json(f, d)


def setup(bot):
    check_folder()
    check_file()
    n = Trophies(bot)
    bot.add_cog(n)

