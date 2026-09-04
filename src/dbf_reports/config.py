import tomllib
from pathlib import Path

import logging
from logging.handlers import RotatingFileHandler

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
config_path = Path(__file__).parent.parent.parent / "config.toml"
with config_path.open("rb") as f:
    config = tomllib.load(f)

db_path = PROJECT_DIR/config["main"]["DATABASE_PATH"]

def setup_logging():
    logger = logging.getLogger()
    if logger.handlers:
        return
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        PROJECT_DIR / "logs" / "app.log",
        maxBytes=10_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    print(PROJECT_DIR)
    setup_logging()

    #print(config["main"]["DBF_START_DIR_TEST"])