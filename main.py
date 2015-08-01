#!/usr/bin/python3
"""A GUI for interacting with Deep Red"""
import sys

from gi.repository import Gtk

from card import deal, tuple_from_s, s_from_tuple
from bot import Bot


class App(Gtk.Application):
    """A Gui for controlling Deep Red"""

    def __init__(self):
        """Initialize the App and connect Actions"""
        Gtk.Application.__init__(self)
        self.connect("activate", self.activate)

    def activate(self, app):
        """Initial Startup Actions"""
        builder = Gtk.Builder.new_from_file("gui.glade")
        builder.connect_signals(Handler(builder))
        setup_window = builder.get_object("setup_window")
        app.add_window(setup_window)
        setup_window.show_all()
        actionbox = builder.get_object("actionbox")
        actionbox.set_sensitive(False)


class Handler(object):
    """Class for holding signal handlers. Do not directly call methods."""

    def __init__(self, builder):
        """Connect the signals"""
        self.builder = builder
        self.bot = None
        self.card = None
        self.prev_card = None

    def begin(self, button):
        """Event handler for beginning the application."""
        action_list = self.builder.get_object("action_list")
        sample_actionbox = self.builder.get_object("actionbox")
        play_actionbox = self.builder.get_object("actionbox1")
        setup_window = self.builder.get_object("setup_window")
        window = self.builder.get_object("window")
        actions = [s.strip() for s in action_list.get_text().split(",")]
        actions = [a for a in actions if len(a) > 0]
        for action in actions:
            sample_actionbox.add(Gtk.CheckButton(action))
            play_actionbox.add(Gtk.CheckButton(action))
        self.bot = Bot(deal(5), len(actions))
        setup_window.hide()
        window.show_all()

    def add_card(self, button):
        """Event handler for added card."""
        new_card_entry = self.builder.get_object("new_card_entry")
        invalid_dialog = self.builder.get_object("invalid_dialog")
        new_card = tuple_from_s(new_card_entry.get_text())
        new_card_entry.set_text("")
        if new_card:
            self.bot.add_card(new_card)
        else:
            invalid_dialog.show()

    def play_card(self, button):
        """Event handler for play card button."""
        actionbox = self.builder.get_object("actionbox1")
        prev_card_entry = self.builder.get_object("prevcard_entry")
        play_dialog = self.builder.get_object("play_dialog")
        pass_dialog = self.builder.get_object("pass_dialog")
        invalid_dialog = self.builder.get_object("invalid_dialog")
        label = self.builder.get_object("instructions")
        self.prev_card = tuple_from_s(prev_card_entry.get_text())
        prev_card_entry.set_text("")
        if not self.prev_card:
            invalid_dialog.show()
            return
        play = self.bot.play(self.prev_card)
        if play:
            dialog = play_dialog
            action_list = actionbox.get_children()
            self.card, actions = play
            for i in range(len(actions)):
                action_list[i].set_active(actions[i])
            label_text = ("Deep Red played " + s_from_tuple(self.card) +
                          ". Is this valid?")
            if len(action_list) > 0:
                label_text += """
                              If the card is valid but the actions are not,
                              simply change the actions and then click valid.
                              """
            label.set_text(label_text)
        else:
            dialog = pass_dialog
        dialog.show_all()

    def valid(self, button):
        """Event handler for valid button"""
        actionbox = self.builder.get_object("actionbox1")
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

    def toggle_valid(self, button):
        """
        Activate or deactivate the action checkboxes, depending on whether
        valid checkbox is clicked.
        """
        actionbox = self.builder.get_object("actionbox")
        actionbox.set_sensitive(button.get_active())

    def add_sample(self, button):
        """
        Add a sample to the bot, based on the sample input fields.
        """
        actionbox = self.builder.get_object("actionbox")
        prev_card_entry = self.builder.get_object("sample_prevcard_entry")
        card_entry = self.builder.get_object("sample_card_entry")
        valid_button = self.builder.get_object("valid_checkbox")
        invalid_dialog = self.builder.get_object("invalid_dialog")
        self.prev_card = tuple_from_s(prev_card_entry.get_text())
        self.card = tuple_from_s(card_entry.get_text())
        prev_card_entry.set_text("")
        card_entry.set_text("")
        if not self.prev_card or not self.card:
            invalid_dialog.show()
            return
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(self.card,
                            self.prev_card,
                            valid_button.get_active(),
                            actions)
        valid_button.set_active(False)

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

    def close(self, button):
        """Default handler for dialog buttons."""
        button.get_toplevel().hide()


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
