#!/usr/bin/python3
"""A GUI for interacting with Deep Red"""
from threading import Thread

from gi.repository import Gtk

from card import deal, tuple_from_s, s_from_tuple
from bot import Bot


def init(builder):
    """Setup GUI"""
    init_setup_window(builder)
    init_sample_pane(builder)
    init_play_pane(builder)
    new_card_entry = builder.get_object("new_card_entry")
    invalid_dialog = builder.get_object("invalid_dialog")

    def add_card(button):
        """Event handler for added card."""
        new_card = tuple_from_s(new_card_entry.get_text())
        new_card_entry.set_text("")
        if new_card:
            bot.add_card(new_card)
        else:
            invalid_dialog.show()

    builder.get_object("add_card").connect("clicked", add_card)
    builder.get_object("button2").connect("clicked", close)

def init_play_pane(builder):
    actionbox = builder.get_object("actionbox1")
    prev_card_entry = builder.get_object("prevcard_entry")
    play_dialog = builder.get_object("play_dialog")
    pass_dialog = builder.get_object("pass_dialog")
    invalid_dialog = builder.get_object("invalid_dialog")
    label = builder.get_object("instructions")
    card = None
    prev_card = None

    def play_card(button):
        """Event handler for play card button."""
        nonlocal card, prev_card
        prev_card = tuple_from_s(prev_card_entry.get_text())
        prev_card_entry.set_text("")
        if not prev_card:
            invalid_dialog.show()
            return
        play = bot.play(prev_card)
        if play:
            dialog = play_dialog
            action_list = actionbox.get_children()
            card, actions = play
            for i in range(len(actions)):
                action_list[i].set_active(actions[i])
            label_text = ("Deep Red played " + s_from_tuple(card) +
                          ". Is this valid?")
            if(len(action_list) > 0):
                label_text += """
                              If the card is valid but the actions are not,
                              simply change the actions and then click valid.
                              """
            label.set_text(label_text)
        else:
            dialog = pass_dialog
        dialog.show_all()

    def valid(button):
        """Event handler for valid button"""
        actions = [int(b.get_active()) for b in actionbox.get_children()]
        bot.add_sample(card, prev_card, True, actions)
        dialog = actionbox.get_toplevel()
        dialog.hide()

    def invalid(button):
        """Event handler for invalid button"""
        bot.add_sample(card, prev_card, False)
        bot.add_card(card)
        dialog = button.get_toplevel()
        dialog.hide()

    builder.get_object("play_card").connect("clicked", play_card)
    builder.get_object("button1").connect("clicked", close)
    builder.get_object("valid_button").connect("clicked", valid)
    builder.get_object("invalid_button").connect("clicked", invalid)

def init_setup_window(builder):
    action_list = builder.get_object("action_list")
    sample_actionbox = builder.get_object("actionbox")
    play_actionbox = builder.get_object("actionbox1")
    setup_window = builder.get_object("setup_window")
    window = builder.get_object("window")
    window.connect("delete-event", quit)

    def begin(button):
        global bot
        actions = [s.strip() for s in action_list.get_text().split(",")]
        actions = list(filter(lambda x: len(x) > 0, actions))
        for action in actions:
            sample_actionbox.add(Gtk.CheckButton(action))
            play_actionbox.add(Gtk.CheckButton(action))
        bot = Bot(deal(5), len(actions))
        setup_window.hide()
        window.show_all()

    setup_window.connect("delete-event", quit)
    builder.get_object("begin").connect("clicked", begin)
    setup_window.show_all()

def init_sample_pane(builder):
    actionbox = builder.get_object("actionbox")
    prev_card_entry = builder.get_object("sample_prevcard_entry")
    card_entry = builder.get_object("sample_card_entry")
    valid_button = builder.get_object("valid_checkbox")
    invalid_dialog = builder.get_object("invalid_dialog")
    actionbox.set_sensitive(False)

    def toggle_valid(button):
        """
        Activate or deactivate the action checkboxes, depending on whether
        valid checkbox is clicked.
        """
        actionbox.set_sensitive(button.get_active())

    def add_sample(button):
        """
        Add a sample to the bot, based on the sample input fields.
        """
        prev_card = tuple_from_s(prev_card_entry.get_text())
        card = tuple_from_s(card_entry.get_text())
        prev_card_entry.set_text("")
        card_entry.set_text("")
        if not prev_card or not card:
            invalid_dialog.show()
            return
        actions = []
        for button in actionbox.get_children():
            actions.append(int(button.get_active()))
            button.set_active(False)
        bot.add_sample(card,
                            prev_card,
                            valid_button.get_active(),
                            actions)
        valid_button.set_active(False)

    valid_button.connect("toggled", toggle_valid)
    builder.get_object("add_sample").connect("clicked", add_sample)

def quit(widget, event):
    """Close GUI"""
    Gtk.main_quit()

def close(button):
    """Default handler for dialog buttons."""
    button.get_toplevel().hide()

if __name__ == "__main__":
    bot = None
    builder = Gtk.Builder.new_from_file("gui.glade")
    init(builder)
    Gtk.main()
