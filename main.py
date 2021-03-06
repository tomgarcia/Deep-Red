#!/usr/bin/env python3
"""A GUI for interacting with Deep Red"""
import sys

from gi.repository import Gtk

from gui.main import Handler


class App(Gtk.Application):
    """A Gui for controlling Deep Red"""

    def __init__(self):
        """Initialize the App and connect Actions"""
        Gtk.Application.__init__(self)
        self.connect("activate", self.activate)

    def activate(self, app):
        """Start Application"""
        Handler(app)


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
