import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import os


class CustomFormatter(logging.Formatter):
    # Define ANSI escape codes for colors
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def format(self, record):
        # Convert time to IST (Asia/Kolkata)
        ist_timezone = ZoneInfo("Asia/Kolkata")
        dt = datetime.fromtimestamp(record.created, tz=ist_timezone)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S.%f")[:-3]  # Trim microseconds to milliseconds

        # Level in upper case
        level = record.levelname.upper()

        # Source: "folder.subfolder.filename:function-name:line-number"
        # Start from the relative path of the project
        project_root = os.getcwd()
        pathname = record.pathname
        # Compute relative path
        relative_path = os.path.relpath(pathname, project_root)
        # Replace path separators with dots and remove .py extension
        if relative_path.endswith(".py"):
            relative_path = relative_path[:-3]
        module_path = relative_path.replace(os.sep, ".")
        source = f"{module_path}:{record.funcName}:{record.lineno}"

        # Message
        message = record.getMessage()

        # Apply color to the log level
        color = self.COLORS.get(level, self.COLORS["RESET"])
        reset_color = self.COLORS["RESET"]
        level_colored = f"{color}{level}{reset_color}"

        # Construct log string
        log_str = f"{date_str} {time_str} | {level_colored} | {source} - {message}"

        return log_str


def get_logger(name=None):
    """
    Returns a logger instance with a custom formatter for terminal logging.

    Usage:
    -----
    Import the logger into your module:

    ```
    from config.logger import get_logger
    ```

    Create a logger instance for your module:

    ```
    logger = get_logger(__name__)
    ```

    Use the logger to log messages at different severity levels along with respestive colors:

    ```
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    ```

    Example:
    --------

    ```
    from config.logger import get_logger

    logger = get_logger(__name__)

    def main() -> None:
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning")
        logger.error("This is an error message")
        logger.critical("This is a critical message")

    if __name__ == "__main__":
        main()
    ```
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set desired level

    # Check if handlers already added to avoid duplicate logs
    if not logger.handlers:
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Add custom formatter to the handler
        formatter = CustomFormatter()
        ch.setFormatter(formatter)

        # Add handler to the logger
        logger.addHandler(ch)

    return logger
