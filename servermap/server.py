from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# To configure this server for your own beacons
# edit the example below. The 'key' for each
# dictionary member is the UUID (iBeacon) or URL
# (Eddystone). Each key contains a dictionary
# with one key - 'name'. Set the name to what
# you want displayed.
beacons = {
    '5e7c4ded-061a-5f1d-ec22-6ca1d97fdade': {
        'name': 'PJ'
    },
    'http://example.org/jazz': {
        'name': 'Jazz The Cat'
    }
}
tracker = {}


@app.route('/')
def index():

    # Create a list of users and get their highest score
    # (Which is their most likely location)
    users = {}
    for room, info in tracker.items():
        for beacon, score in info['beacons'].items():
            if beacon in beacons:
                user = beacons[beacon]['name']
                if user not in users or score > users[user]['score']:
                    users[user] = {'score': score,
                                   'room': room, 'dt': info['dt']}

    return render_template('index.html', users=users)


# Beacon info arrives here
@app.route('/readings', methods=['PUT'])
def readings():

    payload = request.get_json()

    # We add a timestamp
    currentDT = datetime.datetime.now()
    dtString = currentDT.strftime('%H:%M:%S %d/%m/%y')

    print(payload)
    tracker[payload['room']] = {'beacons': payload['beacons'], 'dt': dtString}

    return jsonify(True)

# Make sure the app can be seen by the scanners
app.run(host="0.0.0.0")
