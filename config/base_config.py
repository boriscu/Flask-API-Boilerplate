from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """
    Base configuration class that provides a common interface for all configuration classes.
    Includes a method for checking missing configuration values.
    """

    @classmethod
    @abstractmethod
    def load_config(cls):
        """
        Abstract method that must be implemented by subclasses to load configuration data.
        Calls check_none_values to ensure all values are set.
        """
        cls.check_none_values()

    @classmethod
    def check_none_values(cls):
        """
        Checks for any None values in the class attributes and logs a warning if any are found.
        """
        from app.logger_setup import LoggerSetup

        logger = LoggerSetup.get_logger("general")
        for key, value in cls.__dict__.items():
            if not key.startswith("__") and not callable(value) and value is None:
                logger.warning(f"Warning: {key} is not set in the configuration.")
