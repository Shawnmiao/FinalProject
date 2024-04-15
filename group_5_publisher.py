import json
import time
import threading
from paho import mqtt
import tkinter as tk
from tkinter import ttk
from group_5_data_generator import generate_data

MQTT_BROKER = 'ip_of_the_broker'
MQTT_PORT = 1883
MQTT_TOPIC = 'HumidityOverTime'
# client = None
is_publishing = False

def connect_to_broker():
    global client
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print("Connected to MQTT Broker")

def disconnect_from_broker():
    global client
    if client is not None:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT Broker")

def start_publishing():
    global is_publishing
    is_publishing = True
    while is_publishing:
        value = generate_data()
        publish_data(value)
        time.sleep(5)  # Publishing interval


# Function to stop publishing data
def stop_publishing():
    global is_publishing
    is_publishing = False


# Function to update MQTT topic and values
def update_values():
    global MQTT_TOPIC
    MQTT_TOPIC = topic_entry.get()
    # Update other values as needed



def publish_data(value):
    client = mqtt.Client()
    client.publish(MQTT_TOPIC, json.dumps(value))
    print(f"Published: {value} to Topic: {MQTT_TOPIC}")

# Function to transmit wild data (random large number)
def transmit_wild_data():
    wild_data = generate_data()
    wild_data['humidity'] = 200  # Arbitrary wild value
    publish_data(wild_data)



def start_publishing_thread():
    publish_thread = threading.Thread(target=start_publishing)
    publish_thread.start()

def skip_blocks_of_data():
    pass

# Create the main window
root = tk.Tk()
root.title("Publisher")

# Create the main frame

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add widgets to the main frame
connect_button = ttk.Button(mainframe, text="Connect", command=connect_to_broker)
disconnect_button = ttk.Button(mainframe, text="Disconnect", command=disconnect_from_broker)
min_value_label = ttk.Label(mainframe, text="Min Value:")
min_value_entry = ttk.Entry(mainframe)
max_value_label = ttk.Label(mainframe, text="Max Value:")
max_value_entry = ttk.Entry(mainframe)
daily_mean_label = ttk.Label(mainframe, text="Daily Mean:")
daily_mean_entry = ttk.Entry(mainframe)
readings_label = ttk.Label(mainframe, text="Readings per Day:")
readings_entry = ttk.Entry(mainframe)
update_button = ttk.Button(mainframe, text="Update", command=update_values)
start_button = ttk.Button(mainframe, text="Start Publishing", command=start_publishing_thread)
stop_button = ttk.Button(mainframe, text="Stop Publishing", command=stop_publishing)
topic_label = ttk.Label(mainframe, text="Topic:")
topic_entry = ttk.Entry(mainframe)
wild_data_button = ttk.Button(mainframe, text="Transmit Wild Data", command=transmit_wild_data)
skip_data_button = ttk.Button(mainframe, text="Skip Blocks of Data", command=skip_blocks_of_data)

# Grid the widgets
connect_button.grid(column=0, row=0, columnspan=2)
disconnect_button.grid(column=2, row=0, columnspan=2)
min_value_label.grid(column=0, row=1, sticky=tk.W)
min_value_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))
max_value_label.grid(column=0, row=2, sticky=tk.W)
max_value_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))
daily_mean_label.grid(column=0, row=3, sticky=tk.W)
daily_mean_entry.grid(column=1, row=3, sticky=(tk.W, tk.E))
readings_label.grid(column=0, row=4, sticky=tk.W)
readings_entry.grid(column=1, row=4, sticky=(tk.W, tk.E))
update_button.grid(column=2, row=1, rowspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
start_button.grid(column=0, row=5, columnspan=2)
stop_button.grid(column=2, row=5, columnspan=2)
topic_label.grid(column=0, row=6, sticky=tk.W)
topic_entry.grid(column=1, row=6, sticky=(tk.W, tk.E))
wild_data_button.grid(column=0, row=7, columnspan=2)
skip_data_button.grid(column=2, row=7, columnspan=2)

# Run the application
root.mainloop()
