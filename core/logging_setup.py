import logging
import logging.handlers
import sys
from pathlib import Path
from configs.settings import settings

def setup_logging() -> None:
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    if root_logger.handlers:
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    log_file = settings.logs_dir / "jarvis.log"
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)