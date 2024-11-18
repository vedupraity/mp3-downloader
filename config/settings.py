import os


class Settings:
    ROOT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR_NAME = "output"
    OUTPUT_DIR_PATH = os.path.join(ROOT_DIR_PATH, OUTPUT_DIR_NAME)
    YOUTUBE_COOKIES_FILE = os.path.join(ROOT_DIR_PATH, "cookies_netscape.txt")
