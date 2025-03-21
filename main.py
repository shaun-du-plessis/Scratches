#main.py is the main entry point for bookings app A. K. A. geTune.
# Handle library imports


import sys
import os
import logging
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Footer, Input, Label
from src.widgets.option_list import OptionList, Option
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from src.backup_manager import BackupManager
from src.database_exit import safe_exit

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger('main')


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


class BackupConfirmationScreen(Screen):
    """Screen to confirm backup creation or restoration."""
    def __init__(self, action="create", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action  # "create" or "restore"
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        if self.action == "create":
            yield Static("Create a new backup?", classes="screen-title")
            message = "This will create a new backup of your current database."
        else:
            yield Static("Restore from backup?", classes="screen-title")
            message = "This will replace your current database with the most recent backup."
        yield Static(message)
        yield Horizontal(
            Button("Yes", id="confirm-yes", variant="success"),
            Button("No", id="confirm-no", variant="error"),
            classes="confirmation-buttons"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        from src.backup_manager import BackupManager
        backup_manager = BackupManager()
        if event.button.id == "confirm-yes":
            if self.action == "create":
                backup_path = backup_manager.create_backup()
                if backup_path:
                    self.app.notify("Backup created successfully", severity="information")
                else:
                    self.app.notify("Failed to create backup", severity="error")
            else:
                if backup_manager.restore_from_backup():
                    self.app.notify("Database restored from backup", severity="information")
                else:
                    self.app.notify("Failed to restore from backup", severity="error")
            self.app.pop_screen()
        elif event.button.id == "confirm-no":
            self.app.pop_screen()

class ExitConfirmationScreen(Screen):
    """Screen with confirmation buttons to execute exit logic."""
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Are you sure you want to exit?", classes="screen-title")
        yield Horizontal(
            Button("Yes", id="exit-yes", variant="error"),
            Button("No", id="exit-no", variant="primary"),
            classes="exit-buttons"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit-yes":
            self.perform_exit()
        elif event.button.id == "exit-no":
            self.app.pop_screen()
    
    def perform_exit(self):
        """Perform safe exit with database cleanup."""
        try:
            self.app.query_one("#main-content").update("Preparing to exit... Saving data and encrypting.")
            safe_exit()
            self.app.exit()
        except Exception as e:
            logger.error(f"Error during exit: {str(e)}")
            self.app.exit()


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
        # Mount the widget first before adding options
        yield option_list
        # Populate with dummy items
        for artist in ["Artist A", "Artist B", "Artist C"]:
            option_list.add_option(Option(artist))


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
        # Mount the widget first before adding options
        yield option_list
        # Populate with dummy items
        for booking in ["Booking 1", "Booking 2", "Booking 3"]:
            option_list.add_option(Option(booking))


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
        
    def on_mount(self) -> None:
        """On app mount, check backup integrity and notify user."""
        backup_manager = BackupManager()
        status = backup_manager.check_backup_integrity()
        message, level = backup_manager.get_user_notification()
        severity_map = {"info": "information", "warning": "warning", "error": "error"}
        self.notify(message, severity=severity_map.get(level, "information"))
        # Inform user to backup if none exists or if backup is invalid
        if not status.get("exists") or not status.get("is_valid"):
            self.notify("No valid backup found. It is recommended to backup data before adding new appointments.", severity="warning", timeout=10, title="Backup Recommended")
        elif status.get("age_days") and status["age_days"] > 7:
            self.notify("Your backup is more than a week old. You might consider taking a backup.", severity="warning", timeout=10, title="Backup Outdated")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "menu-file":
            self.show_file_menu()
        elif button_id == "menu-artists":
            self.show_artists_menu()
        elif button_id == "menu-bookings":
            self.show_bookings_menu()

    def show_file_menu(self):
        menu = OptionList(id="file-menu")
        self.mount(menu, before="#main-content")
        menu.add_option(Option("Login/Logout", id="login"))
        menu.add_option(Option("Backup", id="backup"))
        menu.add_option(Option("Restore", id="restore"))
        menu.add_option(Option("Exit", id="exit"))
        menu.focus()
        menu.capture_option_selected(self.handle_file_menu_selection)

    def handle_file_menu_selection(self, option: Option) -> None:
        selected = option.id
        self.query_one("#file-menu").remove()  # Remove menu after selection
        if selected == "login":
            self.push_screen(LoginScreen())
        elif selected == "backup":
            self.push_screen(BackupConfirmationScreen(action="create"))
        elif selected == "restore":
            self.push_screen(BackupConfirmationScreen(action="restore"))
        elif selected == "exit":
            self.push_screen(ExitConfirmationScreen())

    def show_artists_menu(self):
        # Artists menu can show options in a vertical list (for screens)
        menu = OptionList(id="artists-menu")
        # Mount the OptionList first, then add options
        self.mount(menu, before="#main-content")
        menu.add_option(Option("View", id="artists-view"))
        menu.add_option(Option("Add/Edit", id="artists-addedit"))
        menu.add_option(Option("Print Widget", id="artists-print"))
        menu.add_option(Option("Remove Widget", id="artists-remove"))
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
        # Mount the OptionList first, then add options
        self.mount(menu, before="#main-content")
        menu.add_option(Option("View", id="bookings-view"))
        menu.add_option(Option("Add/Edit", id="bookings-addedit"))
        menu.add_option(Option("Print Widget", id="bookings-print"))
        menu.add_option(Option("Export/Import", id="bookings-exportimport"))
        menu.add_option(Option("Remove Widget", id="bookings-remove"))
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
