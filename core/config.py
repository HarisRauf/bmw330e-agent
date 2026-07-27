from pathlib import Path
import yaml


class Config:
    def __init__(self, path: str = "config.yaml"):
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(f"Config file '{path}' not found.")

        with open(self.path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get_searches(self):
        return self.data["searches"]

    def get_scheduler_interval(self):
        return self.data["scheduler"]["interval_minutes"]

    def get_database_path(self):
        return self.data["database"]["path"]