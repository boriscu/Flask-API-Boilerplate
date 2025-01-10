from abc import ABC, abstractmethod


class BaseSchemaRetriever(ABC):
    """
    Abstract base class for schema retrievers.
    """

    @abstractmethod
    def retrieve(self, key: str):
        """
        Retrieve a schema based on a provided key.

        Args:
            key (str): The key for the schema to retrieve.

        Returns:
            Schema: The retrieved schema.
        """
        pass

    def __init__(self, namespace):
        self.namespace = namespace
