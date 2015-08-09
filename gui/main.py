from gi.repository import Gtk

from bot import Bot
from card import tuple_from_s, s_from_tuple
from gui.file import FileHandler
from gui.base import BaseHandler


class Handler(BaseHandler):
    """Class for holding signal handlers. Do not directly call methods."""

    def __init__(self, app, actions):
        """Connect the signals"""
        self.app = app
        self.builder = Gtk.Builder.new_from_file("gui/main.ui")
        self.builder.connect_signals(self)
        for action in actions:
            self.add_action(action)
        self.bot = Bot([], actions)
        self.card = None
        self.prev_card = None
        self.error_message = self.builder.get_object("error_message")
        self.error_dialog = self.builder.get_object("error_dialog")
        self.window = self.builder.get_object("window")
        self.file_handler = FileHandler(self)
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
        actionbox = self.builder.get_object("actionbox1")
        prev_card_entry = self.builder.get_object("prevcard_entry")
        play_dialog = self.builder.get_object("play_dialog")
        label = self.builder.get_object("instructions")
        self.prev_card = tuple_from_s(prev_card_entry.get_text())
        prev_card_entry.set_text("")
        if not self.prev_card:
            self.show_error("Invalid Card")
            return
        try:
            play = self.bot.play(self.prev_card)
        except:
            self.show_error("Hand is Empty")
            return
        if play:
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
            play_dialog.show_all()
        else:
            self.show_error("Pass")

    def cancel_play(self, button, _=None):
        """Cancel the play that just occured."""
        self.bot.add_card(self.card)
        button.get_toplevel().hide()
        return True

    def valid(self, _):
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

    def save(self, button):
        self.file_handler.save(button)

    def open_dialog(self, _):
        """Generic event handler for opening a dialog window."""
        self.file_handler.open_dialog.show()

    def save_dialog(self, _):
        """Generic event handler for opening a dialog window."""
        self.file_handler.save_dialog.show()

    def show_error(self, message):
        self.error_message.set_text(message)
        self.error_dialog.show()

    def add_action(self, action):
        sample_actionbox = self.builder.get_object("actionbox")
        play_actionbox = self.builder.get_object("actionbox1")
        sample_actionbox.add(Gtk.CheckButton(action))
        play_actionbox.add(Gtk.CheckButton(action))
        sample_actionbox.show_all()

    def clear_actions(self):
        sample_actionbox = self.builder.get_object("actionbox")
        play_actionbox = self.builder.get_object("actionbox1")
        sample_actionbox.foreach(sample_actionbox.remove)
        play_actionbox.foreach(play_actionbox.remove)
