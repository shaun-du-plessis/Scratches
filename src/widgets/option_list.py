from textual.widgets import ListView, ListItem, Static
from textual import events

class Option(ListItem):
    """
    A simple option widget that extends ListItem.
    The id attribute can be used to identify the option.
    """
    def __init__(self, label: str, id: str = None):
        # Wrap the label in a Static widget so that it is a valid Widget subclass
        super().__init__(Static(label))
        self.id = id or label

class OptionList(ListView):
    """
    A wrapper around Textual's ListView to act as an OptionList.
    Allows adding options and capturing selection events.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = None

    def add_option(self, option: Option):
        self.append(option)

    def capture_option_selected(self, callback):
        """
        Sets a callback function to be called when an option is clicked.
        The callback receives the selected Option as an argument.
        """
        self._callback = callback

    async def on_click(self, event: events.Click) -> None:
        # Traverse up the parent chain to see if the click occurred on an Option
        widget = event.target
        while widget is not None and not isinstance(widget, Option):
            widget = widget.parent
        if widget and self._callback:
            self._callback(widget)
        # Allow the event to continue propagating
        await super().on_click(event)
