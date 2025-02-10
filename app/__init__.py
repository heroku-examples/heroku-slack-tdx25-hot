import os

from flask import Flask
from flask_socketio import SocketIO
from slack_bolt import App

from app import slack_integrations

app = Flask(__name__)

slack_app = App(token=os.environ['SLACK_BOT_TOKEN'])
socketio = SocketIO(app)

app.config['SLACK_BOT_TOKEN'] = os.environ['SLACK_BOT_TOKEN']
app.config['SLACK_SIGNING_SECRET'] = os.environ['SLACK_SIGNING_SECRET']
app.config['SLACK_WEBHOOK_URL'] = os.environ['SLACK_WEBHOOK_URL']

slack_integrations.init_slack()

from app import routes


if __name__ == '__main__':
    socketio.run(app, debug=True)