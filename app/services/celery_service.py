from flask import Flask
from celery import Celery, Task


class CeleryService:
    @staticmethod
    def celery_init_app(app: Flask) -> Celery:
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: object) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(app.name, task_cls=FlaskTask)
        celery_app.conf.update(
            broker_url=app.config.get("CELERY_BROKER_URL"),
            result_backend=app.config.get("CELERY_RESULT_BACKEND"),
            task_ignore_result=app.config.get("CELERY_TASK_IGNORE_RESULT", True),
        )
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app
