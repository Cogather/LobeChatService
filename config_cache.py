from flask_caching import Cache

class CacheConfig:
    # 其他配置项
    CACHE_TYPE = "SimpleCache"  # 使用内存缓存
    CACHE_DEFAULT_TIMEOUT = 86400  # 默认缓存超时时间（秒）
    @staticmethod
    def init_app(app):
        pass
cache = Cache()