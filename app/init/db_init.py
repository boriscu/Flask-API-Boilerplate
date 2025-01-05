from peewee import PostgresqlDatabase
from peewee_migrate import Router
from dotenv import load_dotenv, find_dotenv

from config.app_config import AppConfig

_ = load_dotenv(find_dotenv())

db = PostgresqlDatabase(
    AppConfig.DB_NAME,
    user=AppConfig.DB_USER,
    password=AppConfig.DB_PASSWORD,
    host=AppConfig.DB_HOST,
    port=AppConfig.DB_PORT,
)
router = Router(db, migrate_dir="migrations")
