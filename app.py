# app.py
from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# Configure MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['github_events']
collection = db['events']

# Utility function to format timestamps
def format_timestamp(ts):
    dt = datetime.fromtimestamp(ts, pytz.UTC)
    return dt.strftime("%d %B %Y - %I:%M %p UTC")

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')


@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB '_id' field
    return jsonify(events)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Handle different GitHub events
    if event_type == 'push':
        ref = data['ref'].split('/')[-1]
        author = data['pusher']['name']
        timestamp = format_timestamp(datetime.now().timestamp())
        event_data = {
            'type': 'push',
            'author': author,
            'branch': ref,
            'timestamp': timestamp
        }
        collection.insert_one(event_data)

    elif event_type == 'pull_request':
        action = data['action']
        pr = data['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        timestamp = format_timestamp(datetime.now().timestamp())
        if action == 'opened':
            event_data = {
                'type': 'pull_request',
                'author': author,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            collection.insert_one(event_data)

    elif event_type == 'pull_request_review':
        action = data['action']
        pr = data['pull_request']
        author = data['review']['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        timestamp = format_timestamp(datetime.now().timestamp())
        if action == 'submitted':
            event_data = {
                'type': 'merge',
                'author': author,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            collection.insert_one(event_data)

    return jsonify({'status': 'success'}), 200

@app.route('/latest', methods=['GET', 'POST'])
def latest_events():
    events = list(collection.find().sort('timestamp', -1).limit(10))
    response = []
    for event in events:
        if event['type'] == 'push':
            response.append(f"{event['author']} pushed to {event['branch']} on {event['timestamp']}")
        elif event['type'] == 'pull_request':
            response.append(f"{event['author']} submitted a pull request from {event['from_branch']} to {event['to_branch']} on {event['timestamp']}")
        elif event['type'] == 'merge':
            response.append(f"{event['author']} merged branch {event['from_branch']} to {event['to_branch']} on {event['timestamp']}")
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
