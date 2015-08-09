class BaseHandler(object):
    """
    Base class for handlers, contains shared
    signal handler methods.
    """

    def close(self, button, _=None):
        """Close the window, without deleting it."""
        button.get_toplevel().hide()
        return True
