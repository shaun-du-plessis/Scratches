#main.py is the main entry point for bookings app A. K. A. geTune.
# Handle library imports


import sys
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Footer, Input, Label, OptionList, Option
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive


# Placeholder screens for File menu actions
class LoginScreen(Screen):
    """Screen for Login/Logout with email and password widget."""
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("LOGIN/LOGOUT", classes="screen-title")
        yield Label("Email:")
        yield Input(placeholder="Enter email", name="email")
        yield Label("Password:")
        yield Input(password=True, placeholder="Enter password", name="password")
        yield Button("Submit", id="submit-login")
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "submit-login":
            # Here, you can add authentication logic
            self.app.pop_screen()


class ExitConfirmationScreen(Screen):
    """Screen with Yes (red) and No (blue) buttons to confirm exit."""
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Are you sure you want to exit?", classes="screen-title")
        # Using colored Buttons for Yes (red) and No (blue)
        yield Horizontal(
            Button("Yes", id="exit-yes", variant="error"),
            Button("No", id="exit-no", variant="primary"),
            classes="exit-buttons"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit-yes":
            self.app.exit()
        elif event.button.id == "exit-no":
            self.app.pop_screen()


# Placeholder screens for Manage Artists
class ArtistsViewScreen(Screen):
    """Screen for viewing artists."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Manage Artists: View Screen", classes="screen-title")
        # Content goes here...
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class ArtistsAddEditScreen(Screen):
    """Screen for adding or editing artists."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Manage Artists: Add/Edit Screen", classes="screen-title")
        # Content goes here...
        yield Button("Back", id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class ArtistsPrintWidget(Static):
    """Widget for printing artists information."""
    def compose(self) -> ComposeResult:
        yield Static("Artists Print Widget", classes="widget-title")
        # Dynamic content can be added here


class ArtistsRemoveWidget(Static):
    """Widget with a drop list for removing artists."""
    def compose(self) -> ComposeResult:
        yield Static("Artists Remove Widget", classes="widget-title")
        option_list = OptionList()
        # Populate with dummy items
        for artist in ["Artist A", "Artist B", "Artist C"]:
            option_list.add_option(Option(artist))
        yield option_list


# Placeholder screens for Manage Bookings
class BookingsViewScreen(Screen):
    """Screen for viewing bookings."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Manage Bookings: View Screen", classes="screen-title")
        # Content goes here...
        yield Button("Back", id="back")
        yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class BookingsAddEditScreen(Screen):
    """Screen for adding or editing bookings."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Manage Bookings: Add/Edit Screen", classes="screen-title")
        # Content goes here...
        yield Button("Back", id="back")
        yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class BookingsPrintWidget(Static):
    """Widget for printing bookings information."""
    def compose(self) -> ComposeResult:
        yield Static("Bookings Print Widget", classes="widget-title")
        # Additional content here


class BookingsExportImportScreen(Screen):
    """Screen for exporting/importing bookings."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Manage Bookings: Export/Import Screen", classes="screen-title")
        # Content goes here...
        yield Button("Back", id="back")
        yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class BookingsRemoveWidget(Static):
    """Widget with a drop list for removing bookings."""
    def compose(self) -> ComposeResult:
        yield Static("Bookings Remove Widget", classes="widget-title")
        option_list = OptionList()
        # Populate with dummy items
        for booking in ["Booking 1", "Booking 2", "Booking 3"]:
            option_list.add_option(Option(booking))
        yield option_list


# Main Application
class GeTuneApp(App):
    CSS_PATH = "styles.css"  # If you want to add a CSS file for styling
    TITLE = "geTune - Bookings App"

    # Flag to track login status (placeholder)
    logged_in = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Create the menu bar as horizontal buttons
        yield Horizontal(
            Button("File", id="menu-file"),
            Button("Manage Artists", id="menu-artists"),
            Button("Manage Bookings", id="menu-bookings"),
            id="menu-bar"
        )
        # A placeholder main content area
        yield Static("Welcome to geTune", id="main-content", expand=True)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "menu-file":
            self.show_file_menu()
        elif button_id == "menu-artists":
            self.show_artists_menu()
        elif button_id == "menu-bookings":
            self.show_bookings_menu()

    def show_file_menu(self):
        # A simple implementation of file menu items
        menu = OptionList(id="file-menu")
        menu.add_option(Option("Login/Logout", id="login"))
        menu.add_option(Option("Exit", id="exit"))
        self.mount(menu, before="#main-content")
        menu.focus()

        # Handle selection
        menu.capture_option_selected(self.handle_file_menu_selection)

    def handle_file_menu_selection(self, option: Option) -> None:
        selected = option.id
        self.query_one("#file-menu").remove()  # Remove menu after selection
        if selected == "login":
            self.push_screen(LoginScreen())
        elif selected == "exit":
            self.push_screen(ExitConfirmationScreen())

    def show_artists_menu(self):
        # Artists menu can show options in a vertical list (for screens)
        menu = OptionList(id="artists-menu")
        menu.add_option(Option("View", id="artists-view"))
        menu.add_option(Option("Add/Edit", id="artists-addedit"))
        menu.add_option(Option("Print Widget", id="artists-print"))
        menu.add_option(Option("Remove Widget", id="artists-remove"))
        self.mount(menu, before="#main-content")
        menu.focus()
        menu.capture_option_selected(self.handle_artists_menu_selection)

    def handle_artists_menu_selection(self, option: Option) -> None:
        selected = option.id
        self.query_one("#artists-menu").remove()
        if selected == "artists-view":
            self.push_screen(ArtistsViewScreen())
        elif selected == "artists-addedit":
            self.push_screen(ArtistsAddEditScreen())
        elif selected == "artists-print":
            # Replace main-content with print widget
            self.query_one("#main-content").update(ArtistsPrintWidget("Displaying Artists Print Widget"))
        elif selected == "artists-remove":
            self.query_one("#main-content").update(ArtistsRemoveWidget("Select an artist to remove"))

    def show_bookings_menu(self):
        menu = OptionList(id="bookings-menu")
        menu.add_option(Option("View", id="bookings-view"))
        menu.add_option(Option("Add/Edit", id="bookings-addedit"))
        menu.add_option(Option("Print Widget", id="bookings-print"))
        menu.add_option(Option("Export/Import", id="bookings-exportimport"))
        menu.add_option(Option("Remove Widget", id="bookings-remove"))
        self.mount(menu, before="#main-content")
        menu.focus()
        menu.capture_option_selected(self.handle_bookings_menu_selection)

    def handle_bookings_menu_selection(self, option: Option) -> None:
        selected = option.id
        self.query_one("#bookings-menu").remove()
        if selected == "bookings-view":
            self.push_screen(BookingsViewScreen())
        elif selected == "bookings-addedit":
            self.push_screen(BookingsAddEditScreen())
        elif selected == "bookings-print":
            self.query_one("#main-content").update(BookingsPrintWidget("Displaying Bookings Print Widget"))
        elif selected == "bookings-exportimport":
            self.push_screen(BookingsExportImportScreen())
        elif selected == "bookings-remove":
            self.query_one("#main-content").update(BookingsRemoveWidget("Select a booking to remove"))

if __name__ == "__main__":
    GeTuneApp().run()
