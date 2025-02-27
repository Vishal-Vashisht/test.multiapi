Cache = None


class CustomCache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CustomCache, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.cache = {}

    def get(self, key):
        data = self.cache.get(key)
        return data

    def set(self, key, value):
        self.cache[f"cache_{key}"] = value

    def delete(self, key):
        data = self.cache.pop(f"cache_{key}", None)
        if data:
            del data

def intialized_cache(app):
    global Cache
    app.cache = CustomCache()
    Cache = app.cache

