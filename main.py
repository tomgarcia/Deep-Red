#!/usr/bin/python3
"""A GUI for interacting with Deep Red"""
from threading import Thread

from gi.repository import Gtk

from card import deal, tuple_from_s
from bot import Bot

class Gui(Thread):
    """A PyGObject GUI for Deep Red"""

    def __init__(self):
        """Setup GUI"""
        Thread.__init__(self)
        self.bot = Bot(deal(5), 2)
        builder = Gtk.Builder.new_from_file("gui.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("window")
        self.prevcard = builder.get_object("sample_prevcard_entry")
        self.card = builder.get_object("sample_card_entry")
        self.actions = builder.get_object("actionbox")

    def run(self):
        """Start window and Gtk main loop"""
        self.window.show_all()
        Gtk.main()

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

    def add_sample(self, widget):
        prevcard = tuple_from_s(self.prevcard.get_text())
        card = tuple_from_s(self.card.get_text())
        self.prevcard.set_text("")
        self.card.set_text("")
        actions = []
        for button in self.actions.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(card, prevcard, True, actions)

if __name__ == "__main__":
    gui = Gui()
    gui.start()
