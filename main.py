import argparse
import os

import tldextract

from config.logger import get_logger
from lib.jiosaavn import JioSaavn


logger = get_logger(__name__)
root_dir_path = os.path.dirname(os.path.abspath(__file__))
output_dir_name = "output"
output_dir_path = os.path.join(root_dir_path, output_dir_name)


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
        jiosaavn = JioSaavn()

        if "/song/" in args.url:
            logger.info(f"Processing jiosaavn song url: {args.url}")

            song_info = jiosaavn.get_song_info_by_url(args.url)
            jiosaavn.download_and_save_song(song_info, output_dir_path)
        else:
            logger.warning(f"Unsupported url {args.url}")
    else:
        logger.warning(f"Unsupported domain {url_domain}")


if __name__ == "__main__":
    main()
