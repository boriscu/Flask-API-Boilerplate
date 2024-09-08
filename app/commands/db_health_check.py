import click
from flask.cli import with_appcontext
from app.db_init import db
from app.logger_setup import LoggerSetup
from config.app_config import AppConfig


@click.command("health_check:db")
@with_appcontext
def db_health_check_command():
    logger = LoggerSetup.get_logger("cli")
    try:
        cursor = db.connect()
        logger.info(f"Database connection successful. ")
        click.echo(
            click.style(
                f"Database connection successful.",
                fg="green",
            )
        )
    except Exception as e:
        logger.error("Database connection failed.")
        logger.error(e)
        logger.info(
            f"""
            Database configuration: 
                - Host: {AppConfig.DB_HOST} 
                - Port: {AppConfig.DB_PORT} 
                - User: {AppConfig.DB_USER}
                - Name: {AppConfig.DB_NAME} 
                - Password: {AppConfig.DB_PASSWORD}"""
        )
        click.echo(click.style("Database connection failed.", fg="red"))
    finally:
        if not db.is_closed():
            db.close()
