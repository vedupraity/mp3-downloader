import argparse
import os

import tldextract

from config.logger import get_logger
from config.settings import Settings
from lib.jiosaavn import JioSaavn
from lib.youtube import YouTube


logger = get_logger(__name__)


def get_cli_args():
    """
    Set up and return the command-line arguments parser.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="URL to download")
    return parser.parse_args()


def main() -> None:
    logger.info("Init script")

    args = get_cli_args()
    logger.info(f"Input url: {args.url}")

    url_domain = tldextract.extract(args.url).domain

    if url_domain and "jiosaavn" == url_domain:
        if "/song/" in args.url:
            logger.info(f"Processing jiosaavn song url: {args.url}")

            jiosaavn = JioSaavn()
            song_info = jiosaavn.get_song_info_by_url(args.url)
            jiosaavn.download_and_save_song(song_info, Settings.OUTPUT_DIR_PATH)
        else:
            logger.warning(f"Unsupported url {args.url}")
    elif url_domain and ("youtube" == url_domain or "youtu" == url_domain):
        logger.info(f"Processing youtube song url: {args.url}")

        youtube = YouTube()
        youtube.download_and_save_song(args.url, Settings.OUTPUT_DIR_PATH)

    else:
        logger.warning(f"Unsupported domain {url_domain} in url {args.url}")


if __name__ == "__main__":
    main()
