#!/usr/bin/python3
"""A GUI for interacting with Deep Red"""
from threading import Thread

from gi.repository import Gtk

from bot import Bot
from card import deal

class Gui(Thread):
    """A PyGObject GUI for Deep Red"""

    def __init__(self):
        """Setup GUI"""
        Thread.__init__(self)
        builder = Gtk.Builder.new_from_file("gui.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("window")

    def run(self):
        """Start window and Gtk main loop"""
        self.window.show_all()
        Gtk.main()

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

if __name__ == "__main__":
    gui = Gui()
    gui.start()
