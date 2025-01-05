from abc import ABC, abstractmethod


class BaseSchemaRetriever(ABC):
    """
    Abstract base class for schema retrievers.
    """

    @abstractmethod
    def retrieve(self, key: str):
        """
        Retrieve a model based on a provided key.

        Args:
            key (str): The key for the model to retrieve.

        Returns:
            Model: The retrieved model.
        """
        pass

    def __init__(self, namespace):
        self.namespace = namespace
