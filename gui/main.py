from gi.repository import Gtk

from bot import Bot
from card import tuple_from_s, s_from_tuple
from gui.file import FileHandler
from gui.base import BaseHandler
from gui.play import PlayHandler


class Handler(BaseHandler):
    """Class for holding signal handlers. Do not directly call methods."""

    def __init__(self, app, actions):
        """Connect the signals"""
        self.app = app
        self.builder = Gtk.Builder.new_from_file("gui/main.ui")
        self.builder.connect_signals(self)
        self.bot = Bot([], actions)
        self.error_message = self.builder.get_object("error_message")
        self.error_dialog = self.builder.get_object("error_dialog")
        self.window = self.builder.get_object("window")
        self.file_handler = FileHandler(self)
        self.play_handler = PlayHandler(self)
        for action in actions:
            self.add_action(action)
        self.builder.get_object("file_menu").set_submenu(self.file_handler.menu)
        self.app.add_window(self.window)
        self.window.show_all()

    def add_card(self, _):
        """Event handler for added card."""
        new_card_entry = self.builder.get_object("new_card_entry")
        new_card = tuple_from_s(new_card_entry.get_text())
        new_card_entry.set_text("")
        if new_card:
            self.bot.add_card(new_card)
        else:
            self.show_error("Invalid Card")

    def play_card(self, _):
        """Event handler for play card button."""
        prev_card_entry = self.builder.get_object("prevcard_entry")
        label = self.builder.get_object("instructions")
        prev_card = tuple_from_s(prev_card_entry.get_text())
        prev_card_entry.set_text("")
        if not prev_card:
            self.show_error("Invalid Card")
            return
        try:
            play = self.bot.play(prev_card)
        except:
            self.show_error("Hand is Empty")
            return
        if play:
            card, actions = play
            self.play_handler.show(card, prev_card, actions)
        else:
            self.show_error("Pass")

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
        prev_card = tuple_from_s(prev_card_entry.get_text())
        card = tuple_from_s(card_entry.get_text())
        prev_card_entry.set_text("")
        card_entry.set_text("")
        if not prev_card or not card:
            self.show_error("Invalid Card")
            return
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(card,
                            prev_card,
                            valid_button.get_active(),
                            actions)
        valid_button.set_active(False)

    def show_error(self, message):
        self.error_message.set_text(message)
        self.error_dialog.show()

    def add_action(self, action):
        sample_actionbox = self.builder.get_object("actionbox")
        sample_actionbox.add(Gtk.CheckButton(action))
        self.play_handler.add_action(action)
        sample_actionbox.show_all()

    def clear_actions(self):
        sample_actionbox = self.builder.get_object("actionbox")
        sample_actionbox.foreach(sample_actionbox.remove)
        self.play_handler.clear_actions()
