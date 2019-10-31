# django imports
from django.conf import settings

# app level imports
# from .elasticsearch import MyElasticsearch
from .redis import MyRedisClient


redis_client = MyRedisClient()

