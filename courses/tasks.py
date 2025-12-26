from celery import shared_task
from .models import Subscription, Course


# @shared_task
# def periodic_task(course_id, user_id):
#     print(f'Выполнение задачи для курса с ID: {course_id} и пользователя с ID: {user_id}')


@shared_task
def my_task(course_id, user_id):
    print(f'Выполнение задачи для курса с ID: {course_id} и пользователя с ID: {user_id}')