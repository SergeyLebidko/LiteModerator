from django.core.management.base import BaseCommand

from datetime import datetime
from rq_scheduler import Scheduler
from redis import Redis
import rq

from main.tasks import rq_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        queue = rq.Queue('rq_log', connection=Redis())
        queue.enqueue(rq_task)

        scheduler = Scheduler(queue=queue, connection=Redis())
        scheduler.schedule(scheduled_time=datetime.utcnow(), func=rq_task, interval=5, repeat=1)
        scheduler.run()
