# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.SimpleAction.MainTimer import MainTimer
from .actions.SimpleAction.BackupTimer import BackupTimer 

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.main_timer_holder = ActionHolder(
            plugin_base = self,
            action_base = MainTimer,
            action_id = "dev_chillhumanoid_cclocksdcon::MainTimer", # Change this to your own plugin id
            action_name = "Main Timer",
        )
        self.add_action_holder(self.main_timer_holder)
        self.backup_timer_holder = ActionHolder(
            plugin_base = self,
            action_base = BackupTimer,
            action_id = "dev_chillhumanoid_cclocksdcon::BackupTimer",
            action_name = "Backup Timer",
        )
        self.add_action_holder(self.backup_timer_holder)
        # Register plugin
        self.register(
            plugin_name = "ChillClock SD Connector",
            github_repo = "https://github.com/unquenchedservant/ChillClockSDConnector",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )
