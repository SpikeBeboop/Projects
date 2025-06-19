import json
from pathlib import Path
from src.config import Config

class DataManager:
    def __init__(self):
        self.config = Config()