#!/usr/bin/python3
"""A GUI for interacting with Deep Red"""
from threading import Thread

from gi.repository import Gtk

from card import deal, tuple_from_s, s_from_tuple
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

    def add_card(self, entry):
        """Event handler for added card."""
        new_card = tuple_from_s(entry.get_text())
        entry.set_text("")
        self.bot.add_card(new_card)

    def play(self, entry):
        """Event handler for add card button."""
        prev_card = tuple_from_s(entry.get_text())
        entry.set_text("")
        play = self.bot.play(prev_card)
        print(play)
        if play:
            dialog = self.builder.get_object("play_dialog")
            actionbox = self.builder.get_object("actionbox1").get_children()
            card, actions = play
            for i in range(len(actions)):
                actionbox[i].set_active(actions[i])
            label = self.builder.get_object("instructions")
            label.set_text("Deep Red played " + s_from_tuple(card) +
                    """. Is this valid? If the card is valid but the
                    actions are not, simply change the actions and then
                    click valid.""")
        else:
            dialog = self.builder.get_object("pass_dialog")
        dialog.show_all()
    def close(self, dialog):
        dialog.hide()

if __name__ == "__main__":
    gui = Gui()
    gui.start()
