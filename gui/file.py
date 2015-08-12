from gi.repository import Gtk

from bot import Bot
from gui.base import BaseHandler


class FileHandler(BaseHandler):
    """Signal Handler for filechoosers."""

    def __init__(self, app):
        """Initialize the filechooser signal handlers."""
        self.app = app
        self.filename = None
        builder = Gtk.Builder.new_from_file("gui/file.ui")
        builder.connect_signals(self)
        self.menu = builder.get_object("menu")
        self.save_dialog = builder.get_object("save_dialog")
        self.open_dialog = builder.get_object("open_dialog")
        self.save_dialog.set_transient_for(app.window)
        self.open_dialog.set_transient_for(app.window)

    def open_profile(self, _):
        """Load bot from the file selected by the user."""
        self.filename = self.open_dialog.get_filename()
        self.app.bot = Bot.load(self.filename)
        self.app.refresh_actions()
        self.app.refresh_hand()
        self.open_dialog.hide()

    def save(self, _):
        """Save the bot to the current profile."""
        if self.filename:
            self.app.bot.save(self.filename)
        else:
            self.save_dialog.show()

    def save_as(self, _):
        """Save the bot to the file selected by the user."""
        self.filename = self.save_dialog.get_filename()
        self.app.bot.save(self.filename)
        self.save_dialog.hide()
