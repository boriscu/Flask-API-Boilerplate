from flask_restx import reqparse


def create_pagination_parser():
    pagination_parser = reqparse.RequestParser(bundle_errors=True)
    pagination_parser.add_argument(
        "page", type=int, default=1, required=False, help="Page number"
    )
    pagination_parser.add_argument(
        "per_page", type=int, default=10, required=False, help="Items per page"
    )
    pagination_parser.add_argument(
        "sort_field",
        type=str,
        required=False,
        help="Field to sort by",
        default="created_at",
    )
    pagination_parser.add_argument(
        "sort_order",
        type=str,
        required=False,
        help="Sort order: 'asc' or 'desc'",
    )
    pagination_parser.add_argument(
        "search", type=str, required=False, help="Search query"
    )
    pagination_parser.add_argument(
        "filters",
        type=str,
        required=False,
        help="Filtering criteria as a JSON string, {'field1': value, 'field2': value, ...}",
    )
    return pagination_parser
