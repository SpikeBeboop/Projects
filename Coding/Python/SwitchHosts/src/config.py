import json
from pathlib import Path



class Config:

    DEFAULT_CONFIG_PATH = Path("config.json")
    DEFAULT_CONFIG = {
        "paths": {
            "data_dir": "data",
            "log_dir": "log",
        }
    }

    def __init__(self):
        self.config = self.DEFAULT_CONFIG
        if self.DEFAULT_CONFIG_PATH.exists():
            self.load_config()
        else:
            self.save_config()

    def save_config(self)->None:
        json.dump(self.config, self.DEFAULT_CONFIG_PATH.open("w", encoding="utf-8"), indent=4)

    def load_config(self)->None:
        config_data = json.load(self.DEFAULT_CONFIG_PATH.open("r", encoding="utf-8"))
        self.config.update(config_data)