import json
import paho.mqtt.client as mqtt
import ssl

from package import variables as v
# this is a helper method that catches errors and prints them
# it is necessary because on_message is called by paho-mqtt in a different thread and exceptions
# are not handled in that thread
#
# you don't need to change this method at all
def on_message_excepthandler(client, data, message):
    try:
        on_message(client, data, message)
    except:
        import traceback
        traceback.print_exc()
        raise

# Callback function for receiving messages
def on_message(client, data, message):
    print('Got message with topic "{}":'.format(message.topic))
    data = json.loads(message.payload.decode('utf-8'))
    print(json.dumps(data, indent=2))
    print("\n")


# Basic configuration of MQTT
client = mqtt.Client(client_id=f"{v.mqtt_user}", clean_session=False,protocol=mqtt.MQTTv31)

client.on_message = on_message_excepthandler  # Assign pre-defined callback function to MQTT client
client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.username_pw_set(f'{v.mqtt_user}',
                       password=f'{v.mqtt_pass}')
client.connect(f'{v.mqtt_server}', port=1883)
client.subscribe(f'comtest/009', qos=2)
# Start listening to incoming messages in the background
client.loop_start()

while True:
    user_input = input('Enter disconnect to close the connection...\n')

    if user_input == 'disconnect':
        break

data_message = {
    "from": "client",
    "type": "ready"
}

client.publish("comtest/009", data_message)

# you could add some code to send a message here

client.loop_stop()
client.disconnect()
print("Connection closed, program ended!")

