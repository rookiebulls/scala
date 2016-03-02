from celery import Celery
from pull_health import PullHealth

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost:6379/0')

cm_addresses = PullHealth.get_cm_address()

@celery.task
def get_health(cm):
	# cms = PullHealth.get_cm_address()
    player_health = PullHealth(*cm)
    player_health.run()

