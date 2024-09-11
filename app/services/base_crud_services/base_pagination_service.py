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
        Retrieves rows from the model applying pagination, sorting, searching, and filtering.
        Returns a tuple of list of models, total entries, and total pages.
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
