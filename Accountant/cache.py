from django.core.cache import cache


class RedisCacheManager:
    """
    Centralized manager for all caching operations using Django-Redis.
    """

    @staticmethod
    def get(key):
        return cache.get(key)

    @staticmethod
    def set(key, value, timeout=60 * 15):  # 15 دقيقة افتراضياً
        cache.set(key, value, timeout)

    @staticmethod
    def delete(key):
        cache.delete(key)

    # --- Financial & Accountant Specific Cache Methods ---
    @staticmethod
    def get_accountant_summary():
        return cache.get("accountant_financial_summary")

    @staticmethod
    def set_accountant_summary(data, timeout=60 * 10):  # تخزين مؤقت لمدة 10 دقائق لملخص الحسابات
        cache.set("accountant_financial_summary", data, timeout)

    @staticmethod
    def clear_accountant_summary():
        cache.delete("accountant_financial_summary")