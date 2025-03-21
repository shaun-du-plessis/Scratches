from textual.widgets import ListView, ListItem, Static
from textual import events

class Option(ListItem):
    """
    A simple option widget that extends ListItem.
    Wraps a label string in a Static widget.
    The id attribute can be used to identify the option.
    """
    def __init__(self, label: str, id: str = None):
        super().__init__(Static(label))
        self.id = id or label
        self.can_focus = True

class OptionList(ListView):
    """
    A wrapper around Textual's ListView to act as an OptionList.
    Supports both mouse clicks and keyboard (Enter) interactions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = None

    def add_option(self, option: Option):
        self.append(option)

    def capture_option_selected(self, callback):
        """
        Sets a callback function to be called when an option is selected.
        The callback receives the selected Option as an argument.
        """
        self._callback = callback

    async def on_click(self, event: events.Click) -> None:
        self.log("OptionList received click event")
        widget = event.target
        while widget is not None and not isinstance(widget, Option):
            widget = widget.parent
        if widget and self._callback:
            self.log(f"Option clicked: {widget.id}")
            self._callback(widget)
        parent_on_click = getattr(super(), "on_click", None)
        if parent_on_click and callable(parent_on_click):
            await parent_on_click(event)
        
    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            focused = None
            for child in self.children:
                if getattr(child, "has_focus", False):
                    focused = child
                    break
            if focused and isinstance(focused, Option) and self._callback:
                self.log(f"Enter pressed on option: {focused.id}")
                self._callback(focused)
        parent_on_key = getattr(super(), "on_key", None)
        if parent_on_key and callable(parent_on_key):
            await parent_on_key(event)
