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
        "sort_field", type=str, default="name", required=False, help="Field to sort by"
    )
    pagination_parser.add_argument(
        "sort_order",
        type=str,
        default="asc",
        required=False,
        help="Sort order: asc or desc",
    )
    pagination_parser.add_argument(
        "search", type=str, required=False, help="Search query"
    )
    pagination_parser.add_argument(
        "filters",
        type=str,
        required=False,
        help="Filtering criteria as a JSON string",
        default='{"is_active":true}',
    )
    return pagination_parser


pagination_parser_model = create_pagination_parser()
