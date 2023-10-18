#!/usr/bin/env python3
""" Implement get page function """

import requests
import redis
import time

class WebCache:
    def __init__(self):
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """ Check if the page is already cached 
        Fetch the page and store it in the cache"""
        count_key = f"count:{url}"
        page_key = f"page:{url}"

        
        cached_page = self._redis.get(page_key)
        if cached_page:
            self._redis.incr(count_key)
            return cached_page.decode('utf-8')

        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            self._redis.setex(page_key, 10, page_content)
            self._redis.incr(count_key)
            return page_content
        else:
            return f"Error: Unable to fetch the page from {url}"
