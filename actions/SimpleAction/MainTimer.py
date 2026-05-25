# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import json

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class MainTimer(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.update_button()
        
    def on_key_down(self) -> None:
        pass
    
    def on_key_up(self) -> None:
        if not os.path.exists(os.path.expanduser("~/.config/ChillClock/.toggle_primary")):
            if not os.path.exists(os.path.expanduser("~/.config/ChillClock/.long_press_active")):
                open(os.path.expanduser("~/.config/ChillClock/.toggle_primary"), 'a').close()
            else:
                os.remove(os.path.expanduser("~/.config/ChillClock/.long_press_active"))
        self.update_button()

    def on_tick(self) -> None:
        self.update_button()
    
    def update_button(self):
        with open(os.path.expanduser("~/.config/ChillClock/current_timer.json"), 'r') as f:
            data = json.load(f)
        self.set_center_label(f"{data['text']}")
        current_color = data['class']
        if current_color == "red":
            self.set_background_color([255, 0, 0, 255], True)
        elif current_color == "green":
            self.set_background_color([0, 128, 0, 255], True)
        elif current_color == "yellow":
            self.set_background_color([255, 255, 0, 255], True)
        else:
            self.set_background_color([0, 0, 0, 0], True)