import random
import tkinter as tk
from tkinter import ttk
import json
import paho.mqtt.client as mqtt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from threading import Thread

# MQTT broker details
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'HumidityOverTime'


class RealTimeGraph:
    def __init__(self, root):
        self.root = root
        self.humidity_values = []
        self.setup_gui()
        self.setup_mqtt()

    def setup_gui(self):
        self.mainframe = ttk.Frame(self.root, padding="10")
        self.mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_title("Real-time Humidity Data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Humidity (%)")
        self.line, = self.ax.plot([], [], label='Humidity')

        self.canvas = FigureCanvasTkAgg(fig, master=self.mainframe)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=3)

        self.connect_button = ttk.Button(self.mainframe, text="Connect", command=self.connect_to_broker)
        self.disconnect_button = ttk.Button(self.mainframe, text="Disconnect", command=self.disconnect_from_broker)
        self.connect_button.grid(column=0, row=0)
        self.disconnect_button.grid(column=1, row=0)

    def setup_mqtt(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(MQTT_TOPIC)

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload)
        humidity = payload['humidity']
        self.humidity_values.append(humidity)
        self.update_graph()
        print("received data:",payload)

    def connect_to_broker(self):
        self.client.loop_start()

    def disconnect_from_broker(self):
        self.client.loop_stop()
        self.client.disconnect()

    def update_graph(self):
        self.line.set_ydata(self.humidity_values)
        self.line.set_xdata(range(len(self.humidity_values)))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def simulate_data_publishing(self):
        # This function simulates the data publishing process
        # In a real scenario, this would not be part of the subscriber code
        def publish_fake_data():
            while True:
                fake_humidity = round(random.uniform(30, 70), 2)
                self.client.publish(MQTT_TOPIC, json.dumps({'humidity': fake_humidity}))
                time.sleep(5)

        Thread(target=publish_fake_data).start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MQTT Subscriber with Real-time Graph")
    app = RealTimeGraph(root)
    app.simulate_data_publishing()  # Simulate data publishing
    root.mainloop()
