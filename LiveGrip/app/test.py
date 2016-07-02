import redis

class RedisConnection:
	def __init__(self):
		config = {
			'host': 'redis',
			'port': 6379,
		}
		self.client = redis.Redis(**config)

	def getClient(self):
		return self.client

r = RedisConnection().getClient()
r.rpush("lst1", 6)

print r.llen("lst1")