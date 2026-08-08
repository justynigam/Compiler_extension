import redis
from rq import Queue
from app.core.config import settings

redis_conn = redis.from_url(settings.redis_url)
task_queue = Queue("ml_tasks", connection=redis_conn)