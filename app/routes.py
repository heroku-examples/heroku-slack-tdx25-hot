from flask import render_template, jsonify, request
from app import app, slack_app
import random

# In-memory data for demo purposes
herd_data = {
    "location": "Pasture A",
    "health_status": "Good",
    "feed_percentage": 100,
    "water_percentage": 100
}

@app.route('/')
def index():
    return render_template('index.html', herd=herd_data)

# Update feed route (sync with Slack)
@app.route('/feed', methods=['POST'])
def feed_herd():
    herd_data['feed_percentage'] = max(0, herd_data['feed_percentage'] - 10)
    send_slack_update("Feed stock updated.")
    return jsonify(herd_data)

# Update water route (sync with Slack)
@app.route('/water', methods=['POST'])
def water_herd():
    herd_data['water_percentage'] = max(0, herd_data['water_percentage'] - 10)
    send_slack_update("Water stock updated.")
    return jsonify(herd_data)

# Move herd route (sync with Slack)
@app.route('/move', methods=['POST'])
def move_herd():
    new_location = random.choice(["Pasture A", "Pasture B", "Corral"])
    herd_data['location'] = new_location
    send_slack_update(f"Herd moved to {new_location}.")
    return jsonify(herd_data)

# Request vet route (sync with Slack)
@app.route('/vet', methods=['POST'])
def request_vet():
    herd_data['health_status'] = "Needs attention"
    send_slack_update("Vet requested for herd health.")
    return jsonify(herd_data)

@app.route('/send_slack_buttons', methods=['POST'])
def send_slack_buttons():
    try:
        slack_app.client.chat_postMessage(
            channel='#trail-boss',
            text="Trail Boss, what action would you like to take?",
            attachments=[
                {
                    "text": "Choose an action",
                    "fallback": "You are unable to choose an action",
                    "callback_id": "herd_action_buttons",
                    "color": "#8B4500",
                    "actions": [
                        {
                            "name": "feed_herd",
                            "text": "Feed Herd",
                            "type": "button",
                            "value": "feed_herd",
                            "action_id": "feed_herd"
                        },
                        {
                            "name": "water_herd",
                            "text": "Water Herd",
                            "type": "button",
                            "value": "water_herd",
                            "action_id": "water_herd"
                        },
                        {
                            "name": "move_herd",
                            "text": "Move Herd",
                            "type": "button",
                            "value": "move_herd",
                            "action_id": "move_herd"
                        },
                        {
                            "name": "request_vet",
                            "text": "Request Vet",
                            "type": "button",
                            "value": "request_vet",
                            "action_id": "request_vet"
                        }
                    ]
                }
            ]
        )
    except Exception as e:
        print(f"Error sending Slack message with buttons: {str(e)}")
    return jsonify({"status": "Buttons sent to Slack"})


# Slack update function
def send_slack_update(message):
    slack_app.client.chat_postMessage(
        channel='#trail-boss',
        text=message
    )