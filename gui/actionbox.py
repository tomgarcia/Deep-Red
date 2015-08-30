from gi.repository import Gtk


class ActionBox(object):

    def __init__(self, bot, box):
        self.bot = bot
        self.box = box

    def refresh(self):
        self.box.foreach(self.box.remove)
        for action in self.bot.actions:
            frame = Gtk.Frame.new(action)
            frame.add(Gtk.SpinButton.new_with_range(0, 100, 1))
            self.box.add(frame)
        self.box.show_all()

    def get_actions(self):
        actions = []
        for frame in self.box.get_children():
            button = frame.get_children()[0]
            actions.append(button.get_value())
            button.set_value(0)
        return actions

    def set_actions(self, actions):
        action_list = self.box.get_children()
        for i in range(len(actions)):
            action_list[i].get_children()[0].set_value(actions[i])

    def reset_actions(self):
        for frame in self.box.get_children():
            button = frame.get_children()[0]
            button.set_value(0)

    def get_toplevel(self):
        return self.box.get_toplevel()
