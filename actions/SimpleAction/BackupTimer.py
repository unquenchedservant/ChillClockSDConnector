# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os
import json
import requests

def _load_server():
    config_path = os.path.expanduser("~/.config/ChillClock/config.json")
    try:
        with open(config_path) as f:
            return json.load(f)["server_url"]
    except Exception:
        return "http://localhost:2420"

def _load_api_key():
    env_path = os.path.expanduser("~/.config/ChillClock/.env")
    try:
        with open(env_path) as f:
            for line in f:
                if line.startswith("CHILLCLOCK_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception:
        pass
    return ""

SERVER = _load_server()
_API_KEY = _load_api_key()
AUTH_HEADERS = {"X-API-KEY": _API_KEY} if _API_KEY else {}

# Import gtk modules - used for the config rowss
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class BackupTimer(ActionBase):
    long_press_active = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.update_button()
        
    def on_key_down(self) -> None:
        BackupTimer.long_press_active = True
        requests.post(f"{SERVER}/toggle?timer=2", headers=AUTH_HEADERS).json()
        self.update_button()

    # def on_tick(self) -> None:
    #     self.update_button()
    
    def update_button(self):
        try:
            data = requests.get(f"{SERVER}/status", timeout=1, headers=AUTH_HEADERS).json()
        except Exception:
            return
        color = data["class"]
        if color == "red":
            self.set_background_color([255, 0, 0, 255], True)
        elif color == "green":
            self.set_background_color([0,128,0,255], True)
        elif color == "yellow":
            self.set_background_color([255,255,0,255], True)
        elif color == "white":
            self.set_background_color([0,0,0,0], True)
        self.set_center_label(data["text"]) # for some reason if this goes before the color if-else block, it breaks the StreamDeck's ability to update the background color
        
