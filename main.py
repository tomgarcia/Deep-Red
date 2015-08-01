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
        self.setup_window = builder.get_object("setup_window")
        self.window = builder.get_object("window")
        self.play_dialog = builder.get_object("play_dialog")
        self.pass_dialog = builder.get_object("pass_dialog")
        self.card = None
        self.prev_card = None
        self.init_setup_window(builder)
        self.init_sample_pane(builder)
        self.init_play_pane(builder)
        builder.get_object("add_card").connect_object(
            "clicked", self.add_card, builder.get_object("new_card_entry"))
        self.window.connect("delete-event", self.quit)

    def init_play_pane(self, builder):
        actionbox = builder.get_object("actionbox1")
        prev_card = builder.get_object("prevcard_entry")
        builder.get_object("play_card").connect_object(
            "clicked",
            self.play_card,
            prev_card,
            actionbox,
            builder.get_object("instructions"))
        builder.get_object("button1").connect(
            "clicked",
            self.close)
        builder.get_object("valid_button").connect_object(
            "clicked",
            self.valid,
            actionbox)
        builder.get_object("invalid_button").connect("clicked", self.invalid)

    def init_setup_window(self, builder):
        builder.get_object("setup_window").connect("delete-event", self.quit)
        builder.get_object("begin").connect_object(
            "clicked",
            self.begin,
            builder.get_object("action_list"),
            builder.get_object("actionbox"),
            builder.get_object("actionbox1"))

    def init_sample_pane(self, builder):
        actionbox = builder.get_object("actionbox")
        prev_card = builder.get_object("sample_prevcard_entry")
        card = builder.get_object("sample_card_entry")
        valid_button = builder.get_object("valid_checkbox")
        actionbox.set_sensitive(False)
        valid_button.connect(
            "toggled",
            self.toggle_valid,
            actionbox)
        builder.get_object("add_sample").connect_object(
            "clicked",
            self.add_sample,
            prev_card,
            card,
            valid_button,
            actionbox)


    def run(self):
        """Start window and Gtk main loop"""
        self.setup_window.show_all()
        Gtk.main()

    def quit(self, widget, event):
        """Close GUI"""
        Gtk.main_quit()

    def add_sample(self, prev_card_entry, card_entry, valid_button, actionbox):
        """
        Add a sample to the bot, based on the sample input fields.
        """
        prev_card = tuple_from_s(prev_card_entry.get_text())
        card = tuple_from_s(card_entry.get_text())
        prev_card_entry.set_text("")
        card_entry.set_text("")
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        self.bot.add_sample(card,
                            prev_card,
                            valid_button.get_active(),
                            actions)
        valid_button.set_active(False)

    def toggle_valid(self, button, actions):
        """
        Activate or deactivate the action checkboxes, depending on whether
        valid checkbox is clicked.
        """
        actions.set_sensitive(button.get_active())

    def add_card(self, entry):
        """Event handler for added card."""
        new_card = tuple_from_s(entry.get_text())
        entry.set_text("")
        self.bot.add_card(new_card)

    def play_card(self, prev_card_entry, actionbox, label):
        """Event handler for play card button."""
        prev_card = tuple_from_s(prev_card_entry.get_text())
        prev_card_entry.set_text("")
        play = self.bot.play(prev_card)
        if play:
            dialog = self.play_dialog
            actionbox = actionbox.get_children()
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

    def close(self, button):
        """Default handler for dialog buttons."""
        button.get_toplevel().hide()

    def begin(self, action_list, sample_actionbox, play_actionbox):
        actions = [s.strip() for s in action_list.get_text().split(",")]
        for action in actions:
            sample_actionbox.add(Gtk.CheckButton(action))
            play_actionbox.add(Gtk.CheckButton(action))
        self.bot = Bot(deal(5), len(actions))
        self.setup_window.hide()
        self.window.show_all()

if __name__ == "__main__":
    gui = Gui()
    gui.start()
