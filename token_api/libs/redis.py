#python imports
import redis
import logging

# django imports
from django.conf import settings

HOST = settings.REDIS_CONFIG['HOST']
PORT = settings.REDIS_CONFIG['PORT']
# DB = settings.REDIS_CONFIG['DB']
PASSWORD = settings.REDIS_CONFIG['PASSWORD']


logger = logging.getLogger(__name__)

class MyRedisClient(object):
	"""
	redis client for account app
	"""
	def __init__(self, host=HOST, port=PORT, password=PASSWORD):
		"""
		Init of redis client
		"""
		self.client = redis.Redis(host=HOST)

	def store_key_data(self,key,data):
		"""
		store the data using key
		"""
		try:
			self.client.set(key,data)
			return 1
		except redis.exceptions.RedisError:
			logger.error("Redis: store_data RedisError ", exc_info=True)

	def get_key_data(self,key):
		"""
		retrive data using key
		"""
		try:
			return self.client.get(key)
		except redis.exceptions.RedisError:
			logger.error("Redis: retrive_data RedisError ", exc_info=True)

	def remove_key_data(self,key):
		"""
		remove data using key
		"""
		try:
			self.client.delete(key)
			return 1
		except redis.exceptions.RedisError:
			logger.error("Redis: remove_data RedisError ", exc_info=True)

	def key_exists(self,key):
		
		try:
			return self.client.exists(key)
		except redis.exceptions.RedisError:
			logger.error("Redis: falid RedisError ", exc_info=True)
