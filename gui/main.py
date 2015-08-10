from gi.repository import Gtk, Gdk

from bot import Bot
from card import tuple_from_s, s_from_tuple
from gui.file import FileHandler
from gui.base import BaseHandler
from gui.play import PlayHandler


class Handler(BaseHandler):
    """Class for holding signal handlers. Do not directly call methods."""

    def __init__(self, app):
        """Connect the signals"""
        self.app = app
        self.builder = Gtk.Builder.new_from_file("gui/main.ui")
        self.builder.connect_signals(self)
        self.bot = Bot([])
        self.error_message = self.builder.get_object("error_message")
        self.error_dialog = self.builder.get_object("error_dialog")
        self.window = self.builder.get_object("window")
        self.play_handler = PlayHandler(self)
        file_handler = FileHandler(self)
        self.builder.get_object("file_menu").set_submenu(file_handler.menu)
        css = Gtk.CssProvider()
        css.load_from_path("css/input.css")
        self.window.get_style_context().add_provider_for_screen(
                Gdk.Screen.get_default(),
                css,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.app.add_window(self.window)
        self.window.show_all()

    def add_card(self, _):
        """Event handler for added card."""
        new_card_entry = self.builder.get_object("new_card_entry")
        new_card = tuple_from_s(new_card_entry.get_text())
        if new_card:
            self.bot.add_card(new_card)
            new_card_entry.set_text("")
            self.builder.get_object("add_frame").get_style_context().remove_class("invalid")
        else:
            self.builder.get_object("add_frame").get_style_context().add_class("invalid")

    def play_card(self, _):
        """Event handler for play card button."""
        prev_card_entry = self.builder.get_object("prevcard_entry")
        label = self.builder.get_object("instructions")
        prev_card = tuple_from_s(prev_card_entry.get_text())
        if not prev_card:
            self.builder.get_object("play_frame").get_style_context().add_class("invalid")
            return
        prev_card_entry.set_text("")
        self.builder.get_object("play_frame").get_style_context().remove_class("invalid")
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
        if not prev_card:
            self.builder.get_object("prev_card_frame").get_style_context().add_class("invalid")
        if not card:
            self.builder.get_object("card_frame").get_style_context().add_class("invalid")
        if not prev_card or not card:
            return
        prev_card_entry.set_text("")
        card_entry.set_text("")
        self.builder.get_object("prev_card_frame").get_style_context().remove_class("invalid")
        self.builder.get_object("card_frame").get_style_context().remove_class("invalid")
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

    def refresh_actions(self):
        sample_actionbox = self.builder.get_object("actionbox")
        sample_actionbox.foreach(sample_actionbox.remove)
        for action in self.bot.actions:
            sample_actionbox.add(Gtk.CheckButton(action))
        sample_actionbox.show_all()

    def new_action(self, entry):
        action = entry.get_text()
        entry.set_text("")
        self.bot.add_action(action)
        self.refresh_actions()
