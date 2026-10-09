# ESP32 and EmotiBit Setup

This folder contains the code I used to connect the EmotiBit with the ESP32 and send sensor data through MQTT. There are two approaches available here: **AWS IoT Core** and **BeeHiveMQ**. Each approach has its own code, so you can choose whichever one you want to try.

## 1. Arduino IDE Setup

Before running the code, make sure your Arduino IDE is set up properly:

- Install the ESP32 board package. I used **version 3.0.7**, which worked best in my environment. Newer versions may also work, but you can refer to the EmotiBit GitHub repository for any updates or compatibility information.
- Make sure the EmotiBit library is installed in your Arduino IDE.

## 2. EmotiBit Library

When I first installed the EmotiBit library directly from GitHub, I encountered some compatibility issues and errors when trying to run the code. I made some adjustments to the library to resolve those issues, and the modified version included here worked properly in my environment. I also tested it on my friend's laptop, and it worked there too.

In my experience, some of the firmware or library files available in the EmotiBit GitHub repository may need updates or adjustments to work with this setup. If you run into similar issues, you can try using the modified library provided here instead of the original one.

## 3. EmotiBit Driver

Don't forget to install the required EmotiBit driver by following the instructions in the official [EmotiBit GitHub repository](https://github.com/EmotiBit). This is important so your computer can detect the device properly when you connect the ESP32 through USB.

## 4. Configure Your Credentials

Before running either MQTT code, remember to replace the example credentials and connection settings with your own configuration.

- **AWS IoT Core:** Update the required AWS IoT endpoint and certificate or key configuration.
- **BeeHiveMQ:** Update the MQTT broker address, port, username, and password where required.

Make sure you don't upload your actual credentials, private keys, or certificates to a public GitHub repository.

## 5. Final Notes

The code and modified library are based on my own development and testing experience with this project. They worked in my environment, but your results may vary depending on your ESP32 board package version, library setup, and MQTT configuration. If you encounter errors, check the configuration and compatibility first, and refer to the official EmotiBit documentation for further updates.
