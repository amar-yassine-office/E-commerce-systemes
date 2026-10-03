@staticmethod
    def get_inventory_warehouses():
        return cache.get("inventory_warehouses_list")

    @staticmethod
    def set_inventory_warehouses(data, timeout=60 * 30):
        cache.set("inventory_warehouses_list", data, timeout)

    @staticmethod
    def clear_inventory_warehouses():
        cache.delete("inventory_warehouses_list")