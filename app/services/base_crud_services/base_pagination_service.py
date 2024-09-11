from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Type
from peewee import ModelSelect, Model, DoesNotExist
from peewee import OperationalError, TextField
from functools import reduce
from operator import or_


class BasePaginationService(ABC):

    @classmethod
    @abstractmethod
    def get_rows(
        cls,
        model: Type[Model],
        page: int,
        per_page: int,
        sort_field: str,
        sort_order: str,
        search: str,
        filters: Dict[str, Any],
    ) -> Tuple[List[Model], int, int]:
        """
        Retrieves rows from the database applying pagination, sorting, searching, and filtering.

        Args:
            model (Type[Model]): The model class to retrieve data from.
            page (int): The page number for pagination.
            per_page (int): The number of items per page.
            sort_field (str): The field to sort the results by.
            sort_order (str): The order of sorting ('asc' for ascending, 'desc' for descending).
            search (str): A search term to filter the results.
            filters (Dict[str, Any]): A dictionary of filters to apply to the query.

        Returns:
            Tuple[List[Model], int, int]: A tuple containing the list of models, the total number of entries,
                                           and the total number of pages.
        """

        try:
            query = model.select()
            query = cls.filter_query(query, model, filters)
            query = cls.search_query(query, model, search)
            total_entries = query.count()
            query = cls.sort_query(query, model, sort_field, sort_order)
            models_list = cls.paginate_query(query, page, per_page)
            total_pages = (total_entries + per_page - 1) // per_page
            return (models_list, total_entries, total_pages)
        except AttributeError as e:
            raise ValueError(f"Invalid field name: {e}")
        except OperationalError as e:
            raise ValueError(f"Database operational error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    @staticmethod
    def paginate_query(query: ModelSelect, page: int, per_page: int) -> List[Model]:
        """
        Applies pagination to the given query.

        Args:
            query (ModelSelect): The Peewee query to paginate.
            page (int): The page number for pagination.
            per_page (int): The number of items per page.

        Returns:
            List[Model]: A list of models for the given page.

        Raises:
            ValueError: If the requested page does not exist.
            Exception: For any other pagination errors.
        """

        try:
            return list(query.paginate(page, per_page))
        except DoesNotExist:
            raise ValueError("Requested page does not exist")
        except Exception as e:
            raise Exception(f"Error during pagination: {e}")

    @staticmethod
    def sort_query(
        query: ModelSelect, model: Type[Model], sort_field: str, sort_order: str
    ) -> ModelSelect:
        """
        Sorts the query based on the given sort field and order.

        Args:
            query (ModelSelect): The Peewee query to sort.
            model (Type[Model]): The model class to retrieve the field from.
            sort_field (str): The field name to sort by.
            sort_order (str): The sorting order ('asc' or 'desc').

        Returns:
            ModelSelect: The sorted query.

        Raises:
            ValueError: If the sort field does not exist in the model.
            Exception: For any other sorting errors.
        """

        try:
            model_field = getattr(model, sort_field)
            if sort_order.lower() == "asc":
                query = query.order_by(model_field.asc())
            else:
                query = query.order_by(model_field.desc())
            return query
        except AttributeError:
            raise ValueError(
                f"Sort field {sort_field} does not exist in the model {model.__name__}."
            )
        except Exception as e:
            raise Exception(f"Error during sorting: {e}")

    @staticmethod
    def search_query(
        query: ModelSelect, model: Type[Model], search: str
    ) -> ModelSelect:
        """
        Applies a search filter to the query by checking text fields for the search term.

        Args:
            query (ModelSelect): The Peewee query to apply the search filter to.
            model (Type[Model]): The model class containing the fields to search through.
            search (str): The search term to filter results.

        Returns:
            ModelSelect: The filtered query.

        Raises:
            ValueError: If the search term is not valid.
        """

        if not search:
            return query

        try:
            conditions = []
            for field_name, field in model._meta.fields.items():
                if field_name == "password":
                    continue
                if isinstance(field, TextField):
                    conditions.append(field.contains(search))

            if conditions:
                query = query.where(reduce(or_, conditions))

            return query
        except AttributeError as e:
            raise ValueError("Search field does not exist in the model.")

    @staticmethod
    def filter_query(
        query: ModelSelect, model: Type[Model], filters: Dict[str, Any]
    ) -> ModelSelect:
        """
        Applies filters to the query based on the provided filter dictionary.

        Args:
            query (ModelSelect): The Peewee query to filter.
            model (Type[Model]): The model class containing the fields to filter on.
            filters (Dict[str, Any]): A dictionary of filters where keys are field names and values are the filter values.

        Returns:
            ModelSelect: The filtered query.

        Raises:
            ValueError: If a filter field does not exist in the model.
        """

        if filters is None:
            return query

        try:
            for key, value in filters.items():
                if not hasattr(model, key):
                    raise AttributeError(
                        f"Error in filter query. Field '{key}' does not exist in the model {model.__name__}."
                    )
                field = getattr(model, key)
                query = query.where(field == value)
            return query
        except AttributeError as e:
            raise ValueError(str(e))
