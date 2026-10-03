from django.core.cache import cache

class RedisCacheManager:
    # ... (الدوال السابقة تبقى كما هي)

    @staticmethod
    def get_agent_ticket_stats():
        return cache.get("agent_ticket_stats_summary")

    @staticmethod
    def set_agent_ticket_stats(data, timeout=60 * 5):
        cache.set("agent_ticket_stats_summary", data, timeout)

    @staticmethod
    def clear_agent_ticket_stats():
        cache.delete("agent_ticket_stats_summary")