import redis

class RedisConnection:
	def __init__(self):
		config = {
		    'host': 'redis',
		    'port': 6379,
		}
		self.client = redis.StrictRedis(**config)
	
	def getClient(self):
		return self.client