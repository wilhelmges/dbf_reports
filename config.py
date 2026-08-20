import tomllib
from pathlib import Path
from sqlmodel import create_engine

PROJECT_DIR = Path(__file__).resolve().parent
config_path = Path(__file__).parent / "config.toml"
with config_path.open("rb") as f:
    config = tomllib.load(f)

db_path = PROJECT_DIR/config["main"]["DATABASE_PATH"]


if __name__ == "__main__":
    print(PROJECT_DIR)
    print(db_path)
    #print(config["main"]["DBF_START_DIR_TEST"])