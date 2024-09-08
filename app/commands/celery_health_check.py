import click
from flask.cli import with_appcontext
from app.tasks.celery_health_check_task import celery_health_check_task


@click.command("health_check:celery")
@with_appcontext
def celery_health_check_command():
    for i in range(4):
        task_name = f"health_check_task_{i+1}"
        celery_health_check_task.delay(task_name)
