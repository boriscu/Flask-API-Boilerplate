import time
from app.logger_setup import LoggerSetup
from celery import shared_task


@shared_task(ignore_result=False)
def celery_health_check_task(task_name):
    logger = LoggerSetup.get_logger("cli")
    start_time = time.time()
    logger.info(f"Starting Task: {task_name}, Start Time: {start_time}")
    for i in range(1, 6):
        logger.info(
            f"Task: {task_name}, Iteration: {i}, Celery ID: {celery_health_check_task.request.hostname}"
        )
        time.sleep(2)
    end_time = time.time()
    logger.info(f"Finished Task: {task_name}, Duration: {end_time - start_time}")
