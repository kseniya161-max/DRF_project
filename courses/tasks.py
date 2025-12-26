from celery import shared_task


@shared_task
def periodic_task():
    print('Выполнение периодической задачи')


@shared_task
def my_task():
    pass