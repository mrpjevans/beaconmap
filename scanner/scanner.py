import time
import requests
from beacontools import BeaconScanner

serverUrl = "http://192.168.0.2:5000/readings"

room = "Kitchen"
beacons = [
  {
    "id": "http://example.org/pj",
    "name": "PJ",
    "score": 0
  },
  {
    "id": "5e7c4ded-061a-5f1d-ec22-6ca1d97fdade",
    "name": "Trish",
    "score": 0
  }
]


# This function is called whenever a packet is detected
def callback(bt_addr, rssi, packet, additional_info):

    # Parse out the type of beacon
    typeOfBeacon = type(packet).__name__.split(".").pop()

    # Get the ID of the beacon
    if typeOfBeacon == "EddystoneURLFrame":
        beaconId = packet.url
    elif typeOfBeacon == "IBeaconAdvertisement":
        beaconId = packet.uuid

    # Is it one of ours?
    for index, beacon in enumerate(beacons):
        if beacon['id'] == beaconId:
            beacons[index]['score'] += 1

# Scan for all advertisements from beacons
print('Starting beacon scanner')
scanner = BeaconScanner(callback)
scanner.start()

while True:

    # Allow a 10-second sample to come through
    print('Waiting 10 seconds')
    time.sleep(10)

    # Now send the current rates to the server
    print('Sending to server')
    try:
        response = requests.put(serverUrl, json={"room": room,
                                                 "beacons": beacons})
        if response.status_code == 200:
            print('Success')
        else:
            print('Got response code: ' + str(response.status_code))
    except:
        print("Communication error")

    # Clean the scores
    for index, beacon in enumerate(beacons):
        beacons[index]['score'] = 0
