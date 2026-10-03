@staticmethod
    def get_vendor_profile(store_slug):
        return cache.get(f"vendor_profile_{store_slug}")

    @staticmethod
    def set_vendor_profile(store_slug, data, timeout=60 * 30):
        cache.set(f"vendor_profile_{store_slug}", data, timeout)

    @staticmethod
    def clear_vendor_profile(store_slug):
        cache.delete(f"vendor_profile_{store_slug}")