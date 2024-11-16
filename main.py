import argparse
from lib.jiosaavn import JioSaavn
from config.logger import get_logger

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
    logger.info(f"Processing url {args.url}")


if __name__ == "__main__":
    main()
