import paho.mqtt.client as mqtt

player_inputs = []

def rps(player_inputs):
    message = ""

    p1_choice = player_inputs[0]
    p2_choice = player_inputs[1]

    if p1_choice == p2_choice:
        message = "TIE"
    elif p1_choice == "rock":
        if p2_choice == "paper":
            message = "Player 2 WINS"
        else:
            message = "Player 1 WINS"
    elif p1_choice == "paper":
        if p2_choice == "scissors":
            message = "Player 2 WINS"
        else:
            message = "Player 1 WINS"
    elif p1_choice == "scissors":
        if p2_choice == "rock":
            message = "Player 2 WINS"
        else:
            message = "Player 1 WINS"

    return message

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("rps", qos=1)
2

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
# The default message callback.
# (you can create separate callbacks per subscribed topic)

def on_message(client, userdata, message):
    global player_inputs
    message = message.payload.decode()
    player_inputs.append(message)
    print(player_inputs)

    if len(player_inputs) == 2:
        message = rps(player_inputs)
        client.publish("rps/server", message, qos=1)
        player_inputs = []
        print(player_inputs)

# 1. create a client instance.
client = mqtt.Client()

# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# 2. connect to a broker using one of the connect*() functions.
# client.connect_async("test.mosquitto.org")
client.connect_async("mqtt.eclipseprojects.io")
# client.connect("test.mosquitto.org", 1883, 60)
# client.connect("mqtt.eclipse.org")

# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()
# client.loop_forever()
while True: # perhaps add a stopping condition using some break or something.
    pass
# use subscribe() to subscribe to a topic and receive messages.
# use publish() to publish messages to the broker.
# use disconnect() to disconnect from the broker.
client.loop_stop()
client.disconnect()