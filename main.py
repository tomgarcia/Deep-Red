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
        self.builder = Gtk.Builder.new_from_file("gui.glade")
        self.builder.connect_signals(self)
        self.builder.get_object("actionbox").set_sensitive(False)

    def run(self):
        """Start window and Gtk main loop"""
        self.builder.get_object("window").show_all()
        Gtk.main()

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

    def add_sample(self, actionbox):
        """
        Add a sample to the bot, based on the sample input fields.
        """
        prevcard_entry = self.builder.get_object("sample_prevcard_entry")
        card_entry = self.builder.get_object("sample_card_entry")
        valid_button = self.builder.get_object("valid_checkbox")
        prevcard = tuple_from_s(prevcard_entry.get_text())
        card = tuple_from_s(card_entry.get_text())
        prevcard_entry.set_text("")
        card_entry.set_text("")
        valid_button.set_active(False)
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(card,
                            prevcard,
                            valid_button.get_active(),
                            actions)

    def toggle_valid(self, button):
        """
        Activate or deactivate the action checkboxes, depending on whether
        valid checkbox is clicked.
        """
        actions = self.builder.get_object("actionbox")
        actions.set_sensitive(button.get_active())

    def play(self, widget):
        pass


if __name__ == "__main__":
    gui = Gui()
    gui.start()
