import requests
import json
import pprint
import sseclient

import requests
import json
import pprint
import time
from datetime import datetime
import urllib

import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

# Fill in from the Service Account and Project:
username = "bmip2l324te000b24tt0"  # this is the key
password = "74b2b08d09f341479e05861c1f3cf908"  # this is the secret
projectId = "bmio9v6jd6rrajvumlng"

# Configure URLs, JSON POST data and default names
studioUrlBase = "https://studio.disruptive-technologies.com"
apiUrlBase = "https://api.disruptive-technologies.com/v2"
emulatorUrlBase = "https://emulator.disruptive-technologies.com/v2"
apiDeviceUrl = "{}/projects/{}/devices".format(apiUrlBase, projectId)
emulatedDeviceUrl = "{}/projects/{}/devices".format(emulatorUrlBase, projectId)
codeExampleSensorDisplayName = "Code Example Touch Sensor"
createEmulatedSensorJSON = {
    "type": "touch",
    "labels": {
        "name": codeExampleSensorDisplayName,
        "virtual-sensor": ""
    }
}
publishEmulatedTouchJSON = {
    "touch": {
        "touch": {
        }
    }
}


def getCodeExampleDeviceName(displayName):
    # URL encode label=value
    urlParamFormatNameLabel = urllib.parse.quote(
        "name={}".format(codeExampleSensorDisplayName))
    # Get devices with Label name=displayName
    device_listing = requests.get(
        apiDeviceUrl + "?label_filters=" + urlParamFormatNameLabel, auth=(username, password))
    # If found, return full resource name, else False
    devices = device_listing.json()['devices']
    if len(devices) > 0:
        return devices[0]["name"]
    return False

# Start MQTT
@asyncio.coroutine
def uptime_coro():
    # Check if code-example Sensor already exists
    name = getCodeExampleDeviceName(codeExampleSensorDisplayName)
    if not name:
        # If not, create it
        print(
            "Creating code-example Touch Sensor '{}'".format(codeExampleSensorDisplayName))
        device = requests.post(emulatedDeviceUrl, data=json.dumps(
            createEmulatedSensorJSON), auth=(username, password))
        name = device.json()["name"]
    else:
        print("Found already existing code-example Touch Sensor '{}'".format(codeExampleSensorDisplayName))

    print()
    print("Direct link to Sensor in Studio: {}".format(
        studioUrlBase + "/" + name))
    print()

    C = MQTTClient()
    yield from C.connect('mqtt://mqtt.eclipse.org')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    # Subscribe to '$SYS/broker/load/#' with QOS=2
    yield from C.subscribe([
      #('$SYS/broker/uptime', QOS_1),
      ('/nrf91/publish/touch', QOS_1),
    ])
    print("subscribed")
    try:
      while 1:
          message = yield from C.deliver_message()
          packet = message.publish_packet
          print("received:  %s => %s" % (
                packet.variable_header.topic_name, str(packet.payload.data)))

          # Emulating sensor activity
          print("{} - Touching Sensor".format(datetime.now()))
          r = requests.post(emulatorUrlBase + "/{}:publish".format(name),
                                  data=json.dumps(publishEmulatedTouchJSON), auth=(username, password))
      yield from C.unsubscribe(['nrf91/publish/touch'])
      yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(uptime_coro())
# End mqtt
##############
