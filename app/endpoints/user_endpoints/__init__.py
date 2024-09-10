from flask_restx import Namespace

from app.schemas.retrievers.user_schema_retriever import UserSchemaRetriever


user_namespace = Namespace("Users", description="User operations")
user_schema_retriever = UserSchemaRetriever(user_namespace)

from .regular_user_endpoints import *
from .admin_user_endpoints import *
