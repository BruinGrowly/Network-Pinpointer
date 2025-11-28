"""
Semantic Caching Layer

Provides LRU caching for network operations and semantic analysis.
"""

import time
from typing import Dict, Any, Optional, Tuple
from collections import OrderedDict

class LRUCache:
    """Simple LRU Cache implementation"""
    
    def __init__(self, capacity: int = 1000, ttl: int = 300):
        self.capacity = capacity
        self.ttl = ttl
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        if key not in self.cache:
            return None
            
        value, timestamp = self.cache[key]
        
        # Check TTL
        if time.time() - timestamp > self.ttl:
            del self.cache[key]
            return None
            
        # Move to end (recently used)
        self.cache.move_to_end(key)
        return value
        
    def put(self, key: str, value: Any):
        """Put item in cache"""
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = (value, time.time())
        
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

class SemanticCache:
    """Centralized cache for semantic operations"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SemanticCache, cls).__new__(cls)
            cls._instance.dns_cache = LRUCache(capacity=1000, ttl=3600) # 1 hour DNS cache
            cls._instance.semantic_cache = LRUCache(capacity=5000, ttl=86400) # 24 hour semantic cache
        return cls._instance
        
    def get_dns(self, hostname: str) -> Optional[str]:
        return self.dns_cache.get(hostname)
        
    def put_dns(self, hostname: str, ip: str):
        self.dns_cache.put(hostname, ip)
        
    def get_semantic_analysis(self, text: str) -> Optional[Any]:
        return self.semantic_cache.get(text)
        
    def put_semantic_analysis(self, text: str, result: Any):
        self.semantic_cache.put(text, result)
