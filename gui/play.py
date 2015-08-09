from gi.repository import Gtk

from gui.base import BaseHandler
from card import s_from_tuple

class PlayHandler(BaseHandler):

    def __init__(self, app):
        self.app = app
        self.card = None
        builder = Gtk.Builder.new_from_file("gui/play.ui")
        builder.connect_signals(self)
        self.actionbox = builder.get_object("actionbox")
        self.label = builder.get_object("instructions")
        self.dialog = builder.get_object("play_dialog")
        self.dialog.set_transient_for(app.window)
        pass

    def show(self, card, prev_card, actions):
        self.card = card
        self.prev_card = prev_card
        action_list = self.actionbox.get_children()
        for i in range(len(actions)):
            action_list[i].set_active(actions[i])
        label_text = ("Deep Red played " + s_from_tuple(card) +
                      ". Is this valid?")
        if len(self.actionbox) > 0:
            label_text += """
                          If the card is valid but the actions are not,
                          simply change the actions and then click valid.
                          """
        self.label.set_text(label_text)
        self.dialog.show_all()

    def cancel_play(self, button, _=None):
        """Cancel the play that just occured."""
        self.app.bot.add_card(self.card)
        button.get_toplevel().hide()
        return True

    def valid(self, _):
        """Event handler for valid button"""
        actions = [int(b.get_active()) for b in self.actionbox.get_children()]
        self.app.bot.add_sample(self.card, self.prev_card, True, actions)
        dialog = self.actionbox.get_toplevel()
        dialog.hide()

    def invalid(self, button):
        """Event handler for invalid button"""
        self.app.bot.add_sample(self.card, self.prev_card, False)
        self.app.bot.add_card(self.card)
        dialog = button.get_toplevel()
        dialog.hide()

    def add_action(self, action):
        self.actionbox.add(Gtk.CheckButton(action))

    def clear_actions(self):
        self.actionbox.foreach(self.actionbox.remove)
