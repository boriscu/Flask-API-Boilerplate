import os
import logging
from typing import Optional


class LoggerSetup:
    def __init__(self, log_name, log_dir, file_name_format):
        self.log_name = log_name
        self.log_dir = os.path.join("logs", log_dir)
        self.file_name_format = file_name_format
        self.ensure_log_dir_exists()

    def ensure_log_dir_exists(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)

    def setup_logger(self):
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            log_path = os.path.join(self.log_dir, self.file_name_format)
            file_handler = logging.FileHandler(log_path)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @classmethod
    def get_logger(cls, entity: str, entity_id: Optional[int] = None) -> logging.Logger:
        """
        Retrieves a logger configured for a specific entity and entity ID.

        Args:
            entity (str): The name of the entity for which the logger is created.
                          Supported entities are 'setup', 'cli' and 'migrations'
            entity_id (Optional[int]): The ID of the entity, used to distinguish logs.
                                       This parameter can be None for entities like 'cli'
                                       that do not require a specific ID.

        Returns:
            logging.Logger: A configured logger with an appropriate handler and format set.

        Raises:
            KeyError: If the specified entity is not supported.
        """
        loggers = {
            "cli": cls("cli_output", "cli_output", "cli_output.log"),
            "migrations": cls("migrations", "migrations", "migrations.log"),
            "general": cls("general", "general", "general.log"),
        }
        return loggers[entity].setup_logger()
