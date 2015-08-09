from gi.repository import Gtk

from gui.main import Handler
from gui.base import BaseHandler


class SetupHandler(BaseHandler):
    """Signal Handler for the setup window."""

    def __init__(self, app):
        """Intitialize the setup signal handlers."""
        self.app = app
        builder = Gtk.Builder.new_from_file("gui/setup.ui")
        builder.connect_signals(self)
        self.window = builder.get_object("setup_window")
        self.action_list = builder.get_object("action_list")
        self.app.add_window(self.window)
        self.window.show_all()

    def begin(self, _):
        """Create a bot with the actions listed by the user."""
        actions = [s.strip() for s in self.action_list.get_text().split(",")]
        actions = [a for a in actions if len(a) > 0]
        Handler(self.app, actions)
        self.window.destroy()
