# -*- coding: utf-8 -*-
"""
-------------------------------------------------

File Name:        tui.py

Description:

Author:           jack@fireworkhq.com

Date:             $$(format-time-string "%Y-%m-%d-%H:%M:%S")

Version:          v1.0

Lastmodified:     $(format-time-string "%Y-%m-%d-%H:%M:%S") by Jack Deng

-------
"""
import asyncio
import json
import sys

from rich.table import Table
from textual.app import App
from textual.events import Event
from textual.widgets import Footer
from textual.widgets import Header
from textual.widgets import Placeholder
from textual.widgets import ScrollView


class HimalayaTui(App):
    """
    Tui class for himalaya
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = Header()
        self.footer = Footer()
        # self.sidebar = ScrollView(name="sidebar")
        self.sidebar = Placeholder(name="sidebar")
        self.main = None
        # self.main = Placeholder(name="main")

    async def on_key(self, event: Event):
        if event.key == "s":
            await self.set_focus(self.sidebar)
        elif event.key == "m":
            await self.set_focus(self.main)

    async def on_load(self):
        """
        on load
        """
        proc = await asyncio.create_subprocess_exec(
            "himalaya",
            "-a",
            "jack-local",
            "-o",
            "json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stderr:
            sys.exit(1)
        json_raw = stdout.decode()
        content = json.loads(json_raw)
        # content = JSON(json_raw)
        response = content["response"]
        table = Table(title="Emails")
        for header in response[0].keys():
            if header == "id":
                continue
            table.add_column(header)
        for each in response:
            hashid = each["hash"]
            flags = " ".join(each["flags"])
            subject = each["subject"]
            sender = each["sender"]
            date = each["date"]
            table.add_row(hashid, flags, subject, sender, date)
        self.main = ScrollView(name="main", contents=table)
        await self.bind("q", "quit", "Quit")
        await self.bind("s", "", "Focus Sidebar")
        await self.bind("m", "", "Focus Sidebar")
        await self.bind("b", "view.toggle('sidebar')", "Toggle Sidebar")

    async def on_mount(self):
        """
        on mount
        """
        await self.view.dock(self.sidebar, edge="left", size=20)
        await self.view.dock(self.header, edge="top")
        await self.view.dock(self.footer, edge="bottom")
        await self.view.dock(self.main)
