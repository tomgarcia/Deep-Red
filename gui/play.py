from gi.repository import Gtk

from gui.base import BaseHandler
from gui.actionbox import ActionBox
from card import s_from_tuple


class PlayHandler(BaseHandler):

    def __init__(self, app):
        self.app = app
        self.bot = app.bot
        self.card = None
        builder = Gtk.Builder.new_from_file("gui/play.ui")
        builder.connect_signals(self)
        self.actionbox = ActionBox(self.bot,
                                   builder.get_object("actionbox"))
        self.label = builder.get_object("instructions")
        self.dialog = builder.get_object("play_dialog")
        self.dialog.set_transient_for(app.window)

    def show(self, card, prev_card, actions):
        self.card = card
        self.prev_card = prev_card
        self.actionbox.refresh()
        self.actionbox.set_actions(actions)
        label_text = ("Deep Red played " + s_from_tuple(card) +
                      ". Is this valid?")
        if len(actions) > 0:
            label_text += """
                          If the card is valid but the actions are not,
                          simply change the actions and then click valid.
                          """
        self.label.set_text(label_text)
        self.dialog.show_all()

    def cancel_play(self, button, _=None):
        """Cancel the play that just occured."""
        self.bot.add_card(self.card)
        button.get_toplevel().hide()
        return True

    def valid(self, _):
        """Event handler for valid button"""
        actions = self.actionbox.get_actions()
        self.bot.add_sample(self.card, self.prev_card, True, actions)
        dialog = self.actionbox.get_toplevel()
        dialog.hide()

    def invalid(self, button):
        """Event handler for invalid button"""
        self.bot.add_sample(self.card, self.prev_card, False)
        self.bot.add_card(self.card)
        dialog = button.get_toplevel()
        dialog.hide()

    def new_action(self, entry):
        action = entry.get_text()
        entry.set_text("")
        self.bot.add_action(action)
        self.refresh_actions()
        self.app.refresh_actions()
