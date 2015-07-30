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
        self.bot = None
        builder = Gtk.Builder.new_from_file("gui.glade")
        builder.connect_signals(self)
        builder.get_object("actionbox").set_sensitive(False)
        self.setup_window = builder.get_object("setup_window")
        self.window = builder.get_object("window")
        self.play = {"actionbox": builder.get_object("actionbox1"),
                     "prev_card": builder.get_object("prevcard_entry")}
        self.sample = {"actionbox": builder.get_object("actionbox"),
                       "prev_card": builder.get_object("sample_prevcard_entry"),
                       "card": builder.get_object("sample_card_entry"),
                       "valid": builder.get_object("valid_checkbox")}
        self.play_dialog = builder.get_object("play_dialog")
        self.pass_dialog = builder.get_object("pass_dialog")
        self.card = None
        self.prev_card = None

    def run(self):
        """Start window and Gtk main loop"""
        self.setup_window.show_all()
        Gtk.main()

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

    def add_sample(self, actionbox):
        """
        Add a sample to the bot, based on the sample input fields.
        """
        prevcard_entry = self.sample["prev_card"]
        card_entry = self.sample["card"]
        valid_button = self.sample["valid"]
        prevcard = tuple_from_s(prevcard_entry.get_text())
        card = tuple_from_s(card_entry.get_text())
        prevcard_entry.set_text("")
        card_entry.set_text("")
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(card,
                            prevcard,
                            valid_button.get_active(),
                            actions)
        valid_button.set_active(False)

    def toggle_valid(self, button):
        """
        Activate or deactivate the action checkboxes, depending on whether
        valid checkbox is clicked.
        """
        actions = self.sample["actionbox"]
        actions.set_sensitive(button.get_active())

    def add_card(self, entry):
        """Event handler for added card."""
        new_card = tuple_from_s(entry.get_text())
        entry.set_text("")
        self.bot.add_card(new_card)

    def play(self, label):
        """Event handler for play card button."""
        prev_card = tuple_from_s(self.play["prev_card"].get_text())
        self.play["prev_card"].set_text("")
        play = self.bot.play(prev_card)
        if play:
            dialog = self.play_dialog
            actionbox = self.play["actionbox"].get_children()
            card, actions = play
            self.card = card
            self.prev_card = prev_card
            for i in range(len(actions)):
                actionbox[i].set_active(actions[i])
            label.set_text("Deep Red played " + s_from_tuple(card) +
                           """. Is this valid? If the card is valid but the
                           actions are not, simply change the actions and then
                           click valid.""")
        else:
            dialog = self.pass_dialog
        dialog.show_all()

    def valid(self, actionbox):
        """Event handler for valid button"""
        actions = [int(b.get_active()) for b in actionbox.get_children()]
        self.bot.add_sample(self.card, self.prev_card, True, actions)
        dialog = actionbox.get_toplevel()
        dialog.hide()

    def invalid(self, button):
        """Event handler for invalid button"""
        self.bot.add_sample(self.card, self.prev_card, False)
        self.bot.add_card(self.card)
        dialog = button.get_toplevel()
        dialog.hide()

    def close(self, dialog):
        """Default handler for dialog buttons."""
        dialog.hide()

    def begin(self, action_list):
        actions = [s.strip() for s in action_list.get_text().split(",")]
        for action in actions:
            self.sample["actionbox"].add(Gtk.CheckButton(action))
            self.play["actionbox"].add(Gtk.CheckButton(action))
        self.bot = Bot(deal(5), len(actions))
        self.setup_window.hide()
        self.window.show_all()

if __name__ == "__main__":
    gui = Gui()
    gui.start()
