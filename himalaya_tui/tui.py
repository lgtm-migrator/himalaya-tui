# -*- coding: utf-8 -*-
from textual.app import App
from textual.widgets import Placeholder


class HimalayaTui(App):
    async def on_mount(self):
        await self.view.dock(Placeholder(), edge="left", size=40)
        await self.view.dock(Placeholder(), Placeholder(), edge="top")

    async def on_load(self, event):
        print(event)
        await self.bind("q", "quit")
        await self.bind("r", "color('red')")
        await self.bind("g", "color('green')")
        await self.bind("b", "color('blue')")

    async def action_color(self, color: str) -> None:
        self.background = f"on {color}"
