from __future__ import absolute_import, unicode_literals
from celery import Celery

task_server = Celery(__name__,
                     broker='redis://localhost:6379/0',
                     result_backend='redis://localhost:6379/0',
                     include=['celeryapp.tasks'])

task_server.conf.update(
    result_expires=3600,
)


