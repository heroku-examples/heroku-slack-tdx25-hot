herd_data = {
    "location": "Main Barn",
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

def get_current_water_percentage():
    """
    Returns the current water percentage
    """
    return herd_data['water_percentage']

def update_water_percentage(amount):
    """
    Updates the water percentage and ensures it stays within 0 & 100 %
    :param amount:
    """
    herd_data['water_percentage'] = max(0, min(100, amount))

def get_current_pasture_location():
    """
    Returns the current pasture location
    """
    return herd_data['location']

def get_current_health_status():
    """
    Returns the current herd health status
    """
    return herd_data['health_status']

def get_herd_data():
    """
    Returns the current status of the herd
    """
    return herd_data

