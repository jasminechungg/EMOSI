# Hardware Setup

## Hardware Overview

The EmoSI platform uses the EmotiBit wearable sensor system as the primary physiological data acquisition device. EmotiBit is an open-source wearable sensing platform designed for real-time collection of physiological, biometric, and motion-related signals. The device supports wireless data transmission and can be integrated with external systems for research, monitoring, and machine learning applications.

In this project, EmotiBit was selected due to its ability to simultaneously capture multiple physiological modalities required for emotion recognition, including cardiovascular, electrodermal, thermal, and motion-related signals.

The wearable device is connected to an ESP32 microcontroller, which handles wireless communication and transmits sensor data to the AWS cloud infrastructure through MQTT over TLS.

## Why EmotiBit?

Several wearable sensing platforms are available for physiological monitoring. However, EmotiBit was selected for this project because it provides:

- Open-source hardware and firmware
- Access to raw physiological sensor data
- Real-time wireless streaming capabilities
- Compatibility with ESP32-based systems
- Multiple sensing modalities within a single wearable platform
- Community-supported software tools and documentation

Unlike commercial black-box wearable devices, EmotiBit provides direct access to raw physiological signals, enabling customised preprocessing, feature engineering, machine learning development, and cloud integration.

## EmotiBit Hardware Components

The EmotiBit device integrates several sensors within a compact wearable form factor. These sensors enable simultaneous collection of physiological and movement-related data.

The hardware includes:

- Photoplethysmography (PPG) sensors
- Electrodermal Activity (EDA) electrodes
- Skin temperature sensors
- Thermopile temperature sensor
- 9-axis Inertial Measurement Unit (IMU)
- Battery monitoring circuitry
- MicroSD support
- ESP32 Feather compatibility

Detailed hardware specifications, firmware information, and hardware architecture are available through the official EmotiBit documentation and repositories. :contentReference[oaicite:0]{index=0}

[Insert emotibit-components.PNG]

## Physiological Signals Used

The project utilises multiple physiological signals captured by the EmotiBit device for emotion recognition and behavioural analysis.

### Photoplethysmography (PPG)

PPG measures blood volume changes within peripheral blood vessels using optical sensing techniques.

Signals used:

- PPG_RED
- PPG_GREEN
- PPG_INFRARED

Derived metrics may include:

- Heart Rate (HR)
- Heart Rate Variability (HRV)
- Inter-Beat Interval (IBI)

### Electrodermal Activity (EDA)

EDA measures variations in skin conductance associated with sympathetic nervous system activity and emotional arousal.

Signals used:

- EDA
- EDL (Tonic Component)
- EDR (Phasic Component)

### Temperature Signals

Temperature-related measurements include:

- TEMP_1 (Skin Temperature)
- THERMOPILE Temperature

These signals may provide information related to physiological regulation and emotional responses.

### Motion Signals

The embedded IMU provides:

#### Accelerometer

- ACC_X
- ACC_Y
- ACC_Z

#### Gyroscope

- GYRO_X
- GYRO_Y
- GYRO_Z

#### Magnetometer

- MAG_X
- MAG_Y
- MAG_Z

These measurements support movement analysis and artefact detection during emotion monitoring sessions.

## ESP32 Integration

The EmotiBit device was integrated with an Adafruit Huzzah32 ESP32 Feather microcontroller for wireless communication.

The ESP32 is responsible for:

- Sensor data acquisition
- Local preprocessing
- MQTT message creation
- Secure communication using TLS
- Transmission of physiological data to AWS IoT Core

The ESP32 serves as the bridge between the wearable sensing layer and the cloud processing infrastructure.

## Data Acquisition Workflow

The data acquisition process begins when a participant wears the EmotiBit device. Physiological and motion-related signals are continuously captured and forwarded to the ESP32 microcontroller.

The ESP32 packages sensor readings into MQTT messages and securely transmits the data to AWS IoT Core using MQTT over TLS.

This workflow enables real-time streaming of physiological information to the cloud infrastructure, where subsequent processing, storage, and machine learning inference are performed.

[Insert emotibit-data-acquisition-workflow.PNG]

## Hardware Configuration

The final hardware configuration used in this project consists of:

| Component | Description |
|------------|------------|
| EmotiBit | Physiological sensing platform |
| ESP32 Feather | Wireless microcontroller |
| Wi-Fi Network | Cloud connectivity |
| AWS IoT Core | MQTT communication endpoint |
| AWS Cloud Services | Processing and storage infrastructure |

All physiological data collected by the wearable device is transmitted wirelessly and processed within the AWS ecosystem.

## Limitations and Considerations

Although EmotiBit provides access to a wide range of physiological signals, several considerations should be noted when interpreting the collected data.

### Motion Artefacts

Physiological signals, particularly PPG and EDA measurements, can be affected by participant movement. Excessive motion may introduce noise and reduce signal quality, requiring preprocessing and filtering before analysis.

### Sensor Placement

Signal quality may vary depending on how the device is worn. Improper contact between the skin and sensors can affect physiological measurements, especially EDA and PPG readings.

### Environmental Factors

External conditions such as temperature, humidity, lighting conditions, and physical activity may influence physiological responses and sensor measurements.

### Physiological Variability

Physiological responses differ significantly between individuals. The same emotional state may produce different physiological patterns across participants due to age, health conditions, stress levels, and personal characteristics.

### Research-Oriented Hardware Platform

EmotiBit is designed primarily as a research and development platform. While it provides high flexibility and access to raw sensor data, it is not intended to function as a medical-grade diagnostic device.

### Dataset Generalisation

The physiological data collected using EmotiBit in this project was primarily used to complement publicly available datasets and support model development. Additional data collection and validation involving larger and more diverse participant groups would be required to improve model generalisation and reliability.
