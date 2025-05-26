from django.core.cache import cache
import redis
from django.conf import settings

# Test simplu
try:
    cache.set('test_key', 'test_value', 10)
    result = cache.get('test_key')
    print(f"Cache test: {result}")
    cache.delete('test_key')
    print("Redis connection OK")
except Exception as e:
    print(f"Redis error: {e}")