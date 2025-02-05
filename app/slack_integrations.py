import os

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import request, jsonify
# from app import app, socketio
from .utils import herd_data, get_current_feed_percentage, update_feed_percentage
from slack_sdk.errors import SlackApiError
import random

# Initialize Slack app and request handler
slack_app = App(token=os.environ['SLACK_BOT_TOKEN'], signing_secret=os.environ['SLACK_SIGNING_SECRET'])  # Replace with your actual bot token
handler = SlackRequestHandler(slack_app)

def init_slack():
    """
    Initialize the Slack integration with the Flask app context.
    This function will be called after the app is initialized.
    """
    from app import app
    slack_app.logger.setLevel("INFO")


# Send Slack update message with buttons
def send_slack_update(message):
    """
    Send a Slack message with buttons to the #trail-boss channel.
    """
    from app import app
    try:
        slack_app.client.chat_postMessage(
            channel='#trail-boss',  # Replace with your channel name
            text=message,
            blocks=[  # Using Block Kit for interactive messages
                {
                    "type": "section",
                    "block_id": "herd_status",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{message}\n\nWhat would you like to do?"
                    },
                    "accessory": {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Feed Herd"
                                },
                                "action_id": "feed_herd",
                                "value": "feed_herd"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Water Herd"
                                },
                                "action_id": "water_herd",
                                "value": "water_herd"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Move Herd"
                                },
                                "action_id": "move_herd",
                                "value": "move_herd"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Request Vet"
                                },
                                "action_id": "request_vet",
                                "value": "request_vet"
                            }
                        ]
                    }
                }
            ]
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


# Callback for button interactions
@slack_app.action("feed_herd")
def handle_feed_herd(ack, body, logger):
    # Acknowledge the button click
    ack()

    # Update herd data (feed percentage)
    herd_data['feed_percentage'] = max(0, herd_data['feed_percentage'] - 10)

    # Send a message to Slack and sync data
    send_slack_update(f"Feed stock updated and is now at {herd_data['feed_percentage']}%.")

    # Emit the data change to the web page
    from app import socketio
    socketio.emit('update_herd_data', herd_data)


@slack_app.action("water_herd")
def handle_water_herd(ack, body, logger):
    # Acknowledge the button click
    ack()

    # Update herd data (water percentage)
    herd_data['water_percentage'] = max(0, herd_data['water_percentage'] - 10)

    # Send a message to Slack and sync data
    send_slack_update("Water stock updated.")

    # Emit the data change to the web page
    from app import socketio
    socketio.emit('update_herd_data', herd_data)


@slack_app.action("move_herd")
def handle_move_herd(ack, body, logger):
    # Acknowledge the button click
    ack()

    # Update herd data (location)
    new_location = random.choice(["Pasture A", "Pasture B", "Corral"])
    herd_data['location'] = new_location

    # Send a message to Slack and sync data
    send_slack_update(f"Herd moved to {new_location}.")

    # Emit the data change to the web page
    from app import socketio
    socketio.emit('update_herd_data', herd_data)


@slack_app.action("request_vet")
def handle_request_vet(ack, body, logger):
    # Acknowledge the button click
    ack()

    # Update herd data (health status)
    herd_data['health_status'] = "Needs attention"

    # Send a message to Slack and sync data
    send_slack_update("Vet requested for herd health.")

    # Emit the data change to the web page
    from app import socketio
    socketio.emit('update_herd_data', herd_data)


def handle_slack_interaction(payload):
    """
    Processes Slack button interactions and responds with appropriate messages.
    Ensures the herd management actions are reflected both in Slack and on the web UI.

    :param payload: The Slack interaction payload (dict)
    """
    from app import socketio
    if "actions" not in payload:
        print("No 'actions' in payload:", payload)
        return


    action = payload["actions"][0]["value"]
    response_text = ""

    # Define action responses
    if action == "feed_herd":
        new_feed_percentage = get_current_feed_percentage() - 10
        update_feed_percentage(new_feed_percentage)
        socketio.emit("update_feed", {"feed_percentage": new_feed_percentage}) #, broadcast=True)
        response_text = f"The herd has been fed! 🐂 The feed level is now at {new_feed_percentage}"
    elif action == "water_herd":
        response_text = "The herd has been given water! 💧"
    elif action == "move_herd":
        response_text = "The herd is on the move! 🏇"
    elif action == "vet_visit":
        response_text = "A vet has been requested for the herd! 🚑"

    # Send response message to Slack
    slack_app.client.chat_postMessage(
        channel=payload["channel"]["id"],
        text=response_text
    )

    # Sync the web UI by emitting an update through SocketIO
    from app import socketio  # Lazy import to avoid circular import issues
    socketio.emit("update_herd_status", {"message": response_text})

