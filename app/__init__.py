import os

from flask import Flask
from flask_socketio import SocketIO
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# from app import slack_integrations

app = Flask(__name__)

slack_app = App(token=os.environ['SLACK_BOT_TOKEN'], signing_secret=os.environ['SLACK_SIGNING_SECRET'])
slack_handler = SlackRequestHandler(slack_app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SLACK_BOT_TOKEN'] = os.environ['SLACK_BOT_TOKEN']
app.config['SLACK_SIGNING_SECRET'] = os.environ['SLACK_SIGNING_SECRET']


from app import routes, slack_integrations

slack_integrations.init_slack()

if __name__ == '__main__':
    socketio.run(app, debug=True)