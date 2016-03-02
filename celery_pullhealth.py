import time
from tasks import get_health
from pull_health import PullHealth

while True:
	cm_addresses = PullHealth.get_cm_address()
	if cm_addresses:
		for cm in cm_addresses:
			result = get_health.apply_async(args=[cm], countdown=60)
			if not result.ready():
				time.sleep(10)
			print result.get()
