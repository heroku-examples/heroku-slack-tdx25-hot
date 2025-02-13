import json
import logging
import random

from flask import render_template, jsonify, request
from slack_bolt.adapter.flask import SlackRequestHandler

from app import app, slack_app, socketio
from app.slack_integrations import send_slack_update, handle_slack_interaction, trigger_feed_reorder
from .utils import herd_data, update_feed_percentage

@app.route('/')
def index():
    send_slack_update("Trail boss management is active. Please select an action:")
    send_slack_buttons()
    return render_template('index.html', herd=herd_data)

# Update feed route (sync with Slack)
@app.route('/feed', methods=['POST'])
def feed_herd():
    herd_data['feed_percentage'] = max(0, herd_data['feed_percentage'] - 10)
    send_slack_update("Feed stock updated.")
    update_feed()
    send_slack_buttons()
    return jsonify(herd_data)

@app.route('/update_feed', methods=['POST'])
def update_feed():
    """
    Updates the feed percentage and syncs it across Slack and the web interface.
    """
    data = request.json
    new_feed_percentage = data.get['feed_percentage']
    update_feed_percentage(new_feed_percentage)
    if new_feed_percentage < 25:
        trigger_feed_reorder()
    socketio.emit("update_feed", {"feed_percentage": new_feed_percentage}, broadcast=True)
    send_slack_update(f"🐂 The herd's feed supply is now at {new_feed_percentage}%.")
    send_slack_buttons()
    return jsonify({"status": "updated", "feed_percentage": new_feed_percentage})

# Update water route (sync with Slack)
@app.route('/water', methods=['POST'])
def water_herd():
    herd_data['water_percentage'] = max(0, herd_data['water_percentage'] - 10)
    send_slack_update("Water stock updated.")
    send_slack_buttons()
    return jsonify(herd_data)

# Move herd route (sync with Slack)
@app.route('/move', methods=['POST'])
def move_herd():
    new_location = random.choice(["Main Barn", "North Pasture", "South Pasture", "Corral"])
    herd_data['location'] = new_location
    send_slack_update(f"Herd moved to {new_location}.")
    send_slack_buttons()
    return jsonify(herd_data)

# Request vet route (sync with Slack)
@app.route('/vet', methods=['POST'])
def request_vet():
    herd_data['health_status'] = "Needs attention"
    send_slack_update("Vet requested for herd health.")
    send_slack_buttons()
    return jsonify(herd_data)

@app.route('/send_slack_buttons', methods=['POST'])
def send_slack_buttons():

    message_text = (
        f"-----------\n"
        f"*🐂 Herd Status Update:*\n"
        f"> 📍 *Location:* {herd_data['location']}\n"
        f"> ❤️ *Health Status:* {herd_data['health_status']}\n"
        f"> 🌾 *Feed Available:* {herd_data['feed_percentage']}%\n"
        f"> 🚰 *Water Available:* {herd_data['water_percentage']}%\n\n"
        f"Choose an action below:"
    )

    blocks = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": message_text}
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Feed Herd"},
                    "style": "primary",
                    "value": "feed_herd",
                    "action_id": "feed_herd"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Water Herd"},
                    "style": "primary",
                    "value": "water_herd",
                    "action_id": "water_herd"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "🏇 Move Herd"},
                    "style": "primary",
                    "value": "move_herd",
                    "action_id": "move_herd"
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "🩺 Request Vet Visit"},
                    "style": "danger",
                    "value": "request_vet",
                    "action_id": "request_vet"
                }
            ]
        }
    ]


    try:
        slack_app.client.chat_postMessage(
            channel='#trail-boss',
            text=message_text,
            blocks=blocks
        )
    except Exception as e:
        print(f"Error sending Slack message with buttons: {str(e)}")
    return jsonify({"status": "Buttons sent to Slack"})


@app.route('/slack/events', methods=['POST'])
def slack_events():
    """
    Handles Slack event subscriptions (e.g. listening for mentions, commands).
    """
    handler = SlackRequestHandler(slack_app)
    return handler.handle(request)

@app.route('/slack/actions', methods=['POST'])
def slack_actions():
    """
    Handles Slack interactive button actions and triggers appropriate responses.
    """
    try:
        payload = json.loads(request.form['payload'])
        if payload:
            # payload = request.get_json()
            logging.info(f"Received payload {payload}")
            handle_slack_interaction(payload)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.error(f"Error handling Slack action: {str(e)}")
        return jsonify({"error": "Failed to process action"}), 500

# Slack update function
def send_slack_update(message):
    """
    Sends the message to the Slack channel.
    :param message:
    """
    slack_app.client.chat_postMessage(
        channel='#trail-boss',
        text=message
    )

def sync_updates():
    """
    Synchronizes Slack updates with Web UI.
    """
    socketio.emit("update_herd_data", herd_data, broadcast=True)
    send_slack_buttons()