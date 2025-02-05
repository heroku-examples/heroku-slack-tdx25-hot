herd_data = {
    "location": "Pasture A",
    "health_status": "Good",
    "feed_percentage": 100,
    "water_percentage": 100
}

def get_current_feed_percentage():
    """
    Returns the current feed percentage
    """
    return herd_data['feed_percentage']


def update_feed_percentage(amount):
    """
    Updates the current feed percentage and ensures it stays within 0 & 100 %
    """
    herd_data['feed_percentage'] = max(0, min(100, amount))