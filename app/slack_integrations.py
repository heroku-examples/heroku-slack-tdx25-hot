from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import request
from app import app, herd_data, socketio
from slack_sdk.errors import SlackApiError
import random

# Initialize Slack app and request handler
slack_app = App(token="your-slack-bot-token")  # Replace with your actual bot token
handler = SlackRequestHandler(slack_app)


# Callback for button interactions
@slack_app.action("feed_herd")
def handle_feed_herd(ack, body, logger):
    # Acknowledge the button click
    ack()

    # Update herd data (feed percentage)
    herd_data['feed_percentage'] = max(0, herd_data['feed_percentage'] - 10)

    # Send a message to Slack and sync data
    send_slack_update("Feed stock updated.")

    # Emit the data change to the web page
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
    socketio.emit('update_herd_data', herd_data)


# Function to send updates to Slack
def send_slack_update(message):
    try:
        slack_app.client.chat_postMessage(
            channel='#trail-boss',  # Replace with your channel ID or name
            text=message
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")


# Slack request handler for events
@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
