@staticmethod
    def get_marketing_banners():
        return cache.get("marketing_active_banners")

    @staticmethod
    def set_marketing_banners(data, timeout=60 * 60):
        cache.set("marketing_active_banners", data, timeout)

    @staticmethod
    def clear_marketing_banners():
        cache.delete("marketing_active_banners")

    @staticmethod
    def get_marketing_coupon(code):
        return cache.get(f"marketing_coupon_{code}")

    @staticmethod
    def set_marketing_coupon(code, data, timeout=60 * 15):
        cache.set(f"marketing_coupon_{code}", data, timeout)

    @staticmethod
    def clear_marketing_coupon(code):
        cache.delete(f"marketing_coupon_{code}")