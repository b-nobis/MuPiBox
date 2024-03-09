#!/usr/bin/env python3
"""
License
-------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = "Olaf Splitt"
__license__ = "GPLv3"
__version__ = "1.0.0"
__email__ = "splitti@mupibox.de"
__status__ = "stable"

import paho.mqtt.client as mqtt
import datetime
import os
import subprocess
import time
import json
import platform
import re
import socket
import fcntl
import struct
import requests
import alsaaudio
import netifaces as ni

config = "/etc/mupibox/mupiboxconfig.json"
playerstate = "/tmp/playerstate"

# Load MQTT configuration from JSON file
with open(config) as file:
    jsonconfig = json.load(file)

# Extract MQTT configuration parameters
mqtt_name = jsonconfig['mqtt']['name']
mqtt_topic = jsonconfig['mqtt']['topic'] + "/" + jsonconfig['mqtt']['clientId']
mqtt_clientId = jsonconfig['mqtt']['clientId']
mqtt_active = jsonconfig['mqtt']['active']
mqtt_broker = jsonconfig['mqtt']['broker']
mqtt_port = int(jsonconfig['mqtt']['port'])
mqtt_username = jsonconfig['mqtt']['username']
mqtt_password = jsonconfig['mqtt']['password']
mqtt_refresh = int(jsonconfig['mqtt']['refresh'])
mqtt_refreshIdle = int(jsonconfig['mqtt']['refreshIdle'])
mqtt_timeout = int(jsonconfig['mqtt']['timeout'])
mqtt_debug = jsonconfig['mqtt']['debug']
mupi_version = jsonconfig['mupibox']['version']
mupi_host = jsonconfig['mupibox']['host']

def mqtt_publish_ha():
    # Publish on/off state entity
    state_info = {
        "name": "State",
        "payload_on": "online",
        "payload_off": "offline",
        "expire_after": "300",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/state',
        "availability_topic": mqtt_topic + '/' + mqtt_clientId + '/state',
        "unique_id": mqtt_clientId + '_mupibox_state',
        "device_class": "connectivity",
        "icon": "mdi:power",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/switch/" + mqtt_clientId + "_state/config", json.dumps(state_info), qos=0, retain=False)

    # Publish OS Info
    os_info = {
        "name": "Operating System",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/os',
        "unique_id": mqtt_clientId + '_mupibox_os',
        "icon": "mdi:penguin",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_os/config", json.dumps(os_info), qos=0, retain=False)

    # Publish Raspberry Info
    raspi_info = {
        "name": "Raspberry Pi",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/raspi',
        "unique_id": mqtt_clientId + '_mupibox_raspi',
        "icon": "mdi:raspberry-pi",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_raspi/config", json.dumps(raspi_info), qos=0, retain=False)


    # Publish CPU Temperature state entity
    temp_info = {
        "name": "Temperature",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/temperature',
        "unique_id": mqtt_clientId + '_mupibox_temperature',
        "device_class": "temperature",
        "unit_of_measurement": "°C",
        "suggested_display_precision": "1",
        "icon": "mdi:thermometer",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_temperature/config", json.dumps(temp_info), qos=0, retain=False)

    # Publish Hostname
    hostname_info = {
        "name": "Hostname",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/hostname',
        "unique_id": mqtt_clientId + '_mupibox_hostname',
        "icon": "mdi:dns",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_hostname/config", json.dumps(hostname_info), qos=0, retain=False)

    # Publish IP
    ip_info = {
        "name": "IP-Address",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/ip',
        "unique_id": mqtt_clientId + '_mupibox_ip',
        "icon": "mdi:ip",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_ip/config", json.dumps(ip_info), qos=0, retain=False)

    # Publish Shutdown Button
    power_switch = {
        "name": "Power",
        "payload_on": "on",
        "payload_off": "off",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/power',
        "unique_id": mqtt_clientId + '_mupibox_power',
        "command_topic": mqtt_topic + '/' + mqtt_clientId + '/power/set',
        "icon": "mdi:power",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/switch/" + mqtt_clientId + "_power/config", json.dumps(power_switch), qos=0, retain=False)

    reboot_switch = {
        "name": "Reboot",
        #"availability_topic": mqtt_topic + '/' + mqtt_clientId + '/reboot',
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/reboot',
        "command_topic": mqtt_topic + '/' + mqtt_clientId + '/reboot/set',
        "payload_on": "reboot",
        "payload_off": "off",
        "unique_id": mqtt_clientId + '_mupibox_reboot',
        "icon": "mdi:power",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/switch/" + mqtt_clientId + "_reboot/config", json.dumps(reboot_switch), qos=0, retain=False)


    # Publish Architecture
    architecture_info = {
        "name": "Architecture",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/architecture',
        "unique_id": mqtt_clientId + '_mupibox_architecture',
        "icon": "mdi:cpu-64-bit",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_architecture/config", json.dumps(architecture_info), qos=0, retain=False)

    # Publish MAC
    mac_info = {
        "name": "MAC-Address",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/mac',
        "unique_id": mqtt_clientId + '_mupibox_mac',
        "icon": "mdi:network-pos",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_mac/config", json.dumps(mac_info), qos=0, retain=False)

    # Publish Volume
    volume_info = {
        "name": "Volume",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/volume',
        "unique_id": mqtt_clientId + '_mupibox_volume',
        "command_topic": mqtt_topic + '/' + mqtt_clientId + '/volume/set',
        "unit_of_measurement": "%",
        "value_template": "{{ value|int }}",
        "icon": "mdi:volume-high",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/number/" + mqtt_clientId + "_volume/config", json.dumps(volume_info), qos=0)

    # Publish SSID
    ssid_info = {
        "name": "WIFI SSID",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/ssid',
        "unique_id": mqtt_clientId + '_mupibox_ssid',
        "icon": "mdi:wifi",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_ssid/config", json.dumps(ssid_info), qos=0, retain=False)

    # Publish WIFI SIGNAL STRENGTH
    signal_strength_info = {
        "name": "WIFI signal strength",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/signal_strength',
        "unique_id": mqtt_clientId + '_mupibox_signal_strength',
        "icon": "mdi:wifi",
        "unit_of_measurement": "dBm",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_signal_strength/config", json.dumps(signal_strength_info), qos=0, retain=False)

    # Publish WIFI SIGNAL QUALITY
    signal_quality_info = {
        "name": "WIFI signal quality",
        "state_topic": mqtt_topic + '/' + mqtt_clientId + '/signal_quality',
        "unique_id": mqtt_clientId + '_mupibox_signal_quality',
        "icon": "mdi:wifi",
        "unit_of_measurement": "%",
        "platform": "mqtt",
        "device": {
            "identifiers": mqtt_clientId + "_mupibox",
            "name": mqtt_name,
            "manufacturer": "MuPiBox.de",
            "model": "Your MuPiBox: " + mupi_host,
            "sw_version": mupi_version,
            "configuration_url":"http://" + mupi_host
        }
    }
    client.publish("homeassistant/sensor/" + mqtt_clientId + "_signal_quality/config", json.dumps(signal_quality_info), qos=0, retain=False)



def get_ip_address(interface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface[:15].encode())
        )[20:24])
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

def mqtt_systeminfo():
    with open('/etc/os-release', 'r') as file:
        os_release_content = file.read()
    match = re.search(r'PRETTY_NAME="(.+?)"', os_release_content)
    if match:
        pretty_name = match.group(1)
        os_name = pretty_name.split('"')[-1]
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/os', os_name, qos=0, retain=False)
    else:
        print("PRETTY_NAME not found in /etc/os-release")
        
    raspi = subprocess.check_output(["cat", "/sys/firmware/devicetree/base/model"]).decode("utf-8")
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/raspi', raspi, qos=0, retain=False)
    hostname = subprocess.check_output(["hostname"]).decode("utf-8")
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/hostname', hostname, qos=0, retain=False)
    ip = get_ip_address('wlan0')
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/ip', ip, qos=0, retain=False)
    architecture = subprocess.check_output(["uname", "-m"]).decode("utf-8")
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/architecture', architecture, qos=0, retain=False)
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/mac', get_mac_address('wlan0'), qos=0, retain=False)
  
# Callback function for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    # Send "on" message to device topic on connect
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/state', "online", qos=0)
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/power', "on", qos=0)
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/reboot', "off", qos=0)

# Callback function for when the client is disconnected from the broker
def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))
    # Send "off" message to device topic on disconnect
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/state', "offline", qos=0)
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/power', "off", qos=0)
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/reboot', "off", qos=0)


def playback_info():
    url = 'http://127.0.0.1:5005/state'
    state = requests.get(url).json()
    return state

def player_active():
    output = subprocess.check_output(["head", "-n1", playerstate], universal_newlines=True)
    if output.strip() == "play":
        return True
    else:
        return False

def get_cputemp():
    cpu_temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    temp = cpu_temp.strip().split('=')[1].strip("'C") #.replace('.', ',')
    return temp

def get_wifi():
    #ssid = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8")
    try:
        result = subprocess.check_output(['iwconfig', 'wlan0'], universal_newlines=True)
        ssid_match = re.search(r'ESSID:"(.+?)"', result)
        ssid = ssid_match.group(1) if ssid_match else None
        signal_strength_match = re.search(r'Signal level=(-\d+)', result)
        signal_strength = int(signal_strength_match.group(1)) if signal_strength_match else None
        signal_quality = int(subprocess.check_output("sudo iwconfig wlan0 | awk '/Link Quality/{split($2,a,\"=|/\");print int((a[2]/a[3])*100)\"\"}' | tr -d '%'", shell=True))
        
        return ssid, signal_strength, signal_quality
    except subprocess.CalledProcessError as e:
        print("Command error iwconfig:", e)
        return None, None, None

def get_volume():
    mixer = alsaaudio.Mixer()
    volume = mixer.getvolume()[0]
    return volume

def get_mac_address(interface):
    try:
        mac = ni.ifaddresses(interface)[ni.AF_LINK][0]['addr']
        return mac
    except ValueError:
        return None

def on_message(client, flags, msg):
    print("Empfangene Nachricht:")
    print("Topic: " + msg.topic)
    print("Nachricht: " + str(msg.payload.decode("utf-8")))
    
    
###############################################################################################################

# Create an MQTT client instance
client = mqtt.Client()

# Set the username and password for the MQTT connection if they are provided
if mqtt_username and mqtt_password:
    client.username_pw_set(mqtt_username, mqtt_password)

# Set the callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
#mqtt_topics = (mqtt_topic + '/' + mqtt_clientId + '/'), ("homeassistant/switch/" + mqtt_clientId + "_state/")

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, mqtt_timeout)
client.subscribe(mqtt_topic + '/' + mqtt_clientId + '/power/set')
client.subscribe(mqtt_topic + '/' + mqtt_clientId + '/volume/set')
client.subscribe(mqtt_topic + '/' + mqtt_clientId + '/reboot/set')

# Start the MQTT loop
client.loop_start()
mqtt_publish_ha()
mqtt_systeminfo()

try:
    while True:
        ssid, signal_strength, signal_quality = get_wifi()
        print(ssid)
        print(signal_strength)
        print(signal_quality)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/state', "online", qos=0)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/temperature', float(get_cputemp()), qos=0)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/volume', int(get_volume()), qos=0)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/ssid', ssid, qos=0)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/signal_strength', signal_strength, qos=0)
        client.publish(mqtt_topic + '/' + mqtt_clientId + '/signal_quality', signal_quality, qos=0)

        if player_active():
            sleeptime = mqtt_refresh
            print("JOOO")
            test = playback_info()
        else:
            sleeptime = mqtt_refreshIdle
            print("NÖÖÖ")
        time.sleep(sleeptime)
except KeyboardInterrupt:
    # Stop the MQTT loop and clean up
    client.loop_stop()
    # Send "off" message to device topic on script exit
    client.publish(mqtt_topic + '/' + mqtt_clientId + '/state', "offline", qos=0)
