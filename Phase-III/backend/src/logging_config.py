"""
Logging configuration for the Todo AI Agent
"""
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(log_level: str = "INFO"):
    """
    Set up logging configuration for the application.

    Args:
        log_level: The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Get the logger
    logger = logging.getLogger()

    # Set the log level
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Reduce noise from third-party libraries
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.INFO)


def get_logger(name: str):
    """
    Get a logger with the specified name.

    Args:
        name: The name of the logger

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)