"""Logging configuration module for NovaMart Financial Analytics ETL pipeline.
"""

import logging
import sys
from src.config import PIPELINE_LOG_PATH


def setup_logger(name: str = "novamart_etl") -> logging.Logger:
    """Configure and return a structured logger writing to console and log file."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(PIPELINE_LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
