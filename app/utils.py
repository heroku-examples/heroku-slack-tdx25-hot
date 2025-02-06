herd_data = {
    "location": "Pasture A",
    "health_status": "Good",
    "feed_percentage": 100,
    "water_percentage": 100
}

def get_herd_data():
    """
    Return the current herd status
    """
    return herd_data

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

def update_water_percentage(new_amount):
    """
    Updates the water percentage and ensures it remains within bounds
    """
    herd_data['water_percentage'] = max(0, min(100,new_amount))

def update_location(new_location):
    """
    Updates the herd location
    """
    herd_data['location'] = new_location

def update_health_status(new_health_status):
    """
    Updates the herd's health status.
    """
    herd_data['health_status'] = new_health_status