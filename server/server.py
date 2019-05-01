from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

tracker = {}


@app.route('/')
def index():

    # Create a list of users and get their highest score
    # (Which is their most likely location)
    users = {}
    for room, info in tracker.items():
        for beacon in info['beacons']:
            user = beacon['name']
            if user not in users or beacon['score'] > users[user]['score']:
                users[user] = {'score': beacon['score'],
                               'room': room, 'dt': info['dt']}

    return render_template('index.html', users=users)


# Beacon info arrives here
@app.route('/readings', methods=['PUT'])
def readings():

    payload = request.get_json()

    # We add a timestamp
    currentDT = datetime.datetime.now()
    dtString = currentDT.strftime("%H:%M:%S %d/%m/%y")

    print(payload)
    # tracker[payload['room']] = {'beacons': payload['beacons'], 'dt': dtString}

    return jsonify(True)

# Make sure the app can be seen by the scanners
app.run(host="0.0.0.0")
