from django.core.cache import cache

class RedisCacheManager:
    # ... (الدوال السابقة تبقى كما هي)

    @staticmethod
    def get_catalog_categories():
        return cache.get("catalog_categories_list")

    @staticmethod
    def set_catalog_categories(data, timeout=60 * 30):
        cache.set("catalog_categories_list", data, timeout)

    @staticmethod
    def clear_catalog_categories():
        cache.delete("catalog_categories_list")

    @staticmethod
    def get_catalog_product(product_slug):
        return cache.get(f"catalog_product_{product_slug}")

    @staticmethod
    def set_catalog_product(product_slug, data, timeout=60 * 15):
        cache.set(f"catalog_product_{product_slug}", data, timeout)

    @staticmethod
    def clear_catalog_product(product_slug):
        cache.delete(f"catalog_product_{product_slug}")