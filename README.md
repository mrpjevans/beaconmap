# beaconmap

Pi-Rauder's Map - Using beacons to track people around a building - MagPi #82. Please this issue for full installation instructions and usage of the basic server. [https://www.raspberrypi.org/magpi]()

## Map Server

As discussed in the tutorial, included in this repository is a more advanced version of the server showing locations on a map rather than a list. You'll find in the servermap directory.

### To customise to your own map

As with the basic server, first open server.py and edit the list of known beacons. See the tutorial for details on how to do this.

Now create a 75x75 avatar for each person/thing being tracked. Make sure filename is their name in server.py (case-sensitive) followed by '.jpg'. Place these files in the static directory unedr servermap.

Make sure your house map is a suitable size, say 1000x1000. Call it rooms.png (you can use jpg or anything else, but you'll need to update the template). Also place this file in the static directory.

Now edit templates/index.html. You need to create CSS entries where prompted, one for each room. The two values are the offset from the top-left corner of the map where you would want the avatar displayed. The CSS names must be room- followed by the room name as specified by each beacon scanner (see tutorial).

Finally, locate the code that reads...

```
{%for room in ['Games', 'Study', 'Music', 'Guestroom', 'Bedroom'] %}
```

...and replace the list of room names with your own. Again they must match the beacons exactly.

To start the server:

```bash
python3 server.py
```

Getting the positions right can be fiddly, so you may want to take a copy of the index file and edit it statically to get the values right, or hardcode some avatars by placing HTML such as the following between the ```<div class="avatarContainer">``` block.

```html
<div class="room room-Bedroom">
	<img src="static/PJ.jpg" class="avatar rounded-pill" />
</div>
```

The maps refreshes every 20 seconds. I intend to do a future version that uses AJAX and dynamically updates.
