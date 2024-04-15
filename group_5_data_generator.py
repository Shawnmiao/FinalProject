import time
import random
import json



def generate_data():
    temperature = round(random.uniform(-10, 35), 2)  # Temperatures between -10 and 35 degrees Celsius
    humidity = round(random.uniform(20, 100), 2)  # Humidity between 20% and 100%
    wind_speed = round(random.uniform(0, 15), 2)  # Wind speeds between 0 and 15 m/s

    data = {
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    return data


def main():
    while True:
        data = generate_data()
        print("Generated data:", json.dumps(data, indent=4))
        time.sleep(5)  # Wait for 5 seconds before generating new data


if __name__ == "__main__":
    main()
