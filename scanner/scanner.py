import time
import requests
from beacontools import BeaconScanner

serverUrl = "http://192.168.0.2:5000/readings"

room = "Kitchen"
beacons = {}


# This function is called whenever a packet is detected
def callback(bt_addr, rssi, packet, additional_info):

    # Parse out the type of beacon
    typeOfBeacon = type(packet).__name__.split(".").pop()

    # Get the ID of the beacon
    if typeOfBeacon == "EddystoneURLFrame":
        beaconId = packet.url
    elif typeOfBeacon == "IBeaconAdvertisement":
        beaconId = packet.uuid

    # Track how many times we've seen this beacon
    if beaconId not in beacons:
        beacons[beaconId] = 1
    else:
        beacons[beaconId] += 1

# Scan for all advertisements from beacons
print('Starting beacon scanner')
scanner = BeaconScanner(callback)
scanner.start()

while True:

    # Allow a 10-second sample to come through
    print('Waiting 10 seconds')
    time.sleep(10)

    # Now send the current scores to the server
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
    beacons = {}
