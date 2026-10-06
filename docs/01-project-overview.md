# Project Overview

## Introduction

## Problem Statement

## Objectives

## Scope

## Key Features

## Expected Outcome

# Introduction

Emotional states influence communication, learning, behaviour, and overall well-being. However, emotions are often difficult to assess accurately because conventional methods typically rely on observation, interviews, questionnaires, or self-reporting. These approaches may not always reflect an individual's actual emotional state, particularly when the person experiences communication difficulties or struggles to express emotions verbally.

This challenge is especially relevant when considering children with emotional, behavioural, developmental, or communication difficulties. In such situations, caregivers, educators, and healthcare professionals may face difficulties obtaining objective insights into a child's emotional condition. While behavioural observations remain important, physiological responses may provide additional information that complements traditional assessment approaches.

To address this challenge, EmoSI was developed as a cloud-based emotion monitoring system that integrates wearable physiological sensing, machine learning, cloud computing, and real-time data visualisation. The system uses the EmotiBit wearable device to collect physiological signals including photoplethysmography (PPG), electrodermal activity (EDA), skin temperature, and motion-related data. These signals are transmitted through AWS cloud services, analysed using machine learning models, and presented through an interactive dashboard for monitoring and review.

The machine learning component was developed using a hybrid dataset approach. Publicly available physiological data from the WESAD dataset was initially used to establish baseline emotion recognition capabilities and develop the feature engineering pipeline. To improve compatibility with the target sensing platform, additional physiological data was collected using the EmotiBit wearable device. During these sessions, emotional states were manually labelled and processed using the same preprocessing and feature extraction workflow, allowing both datasets to be aligned into a consistent feature structure for model development and evaluation.

It is important to note that the current implementation represents a foundational platform rather than a completed child-focused assessment solution. Although the project was motivated by challenges associated with emotional expression and assessment, the system has not been specifically trained or validated using large-scale datasets collected from children. Future development would require extensive data collection from the intended target population, additional model training and validation, ethical approval processes, and collaboration with domain experts to ensure reliability and suitability for real-world deployment.

Beyond child-focused applications, the platform may also serve as a foundation for future research involving emotion-aware learning environments, communication support systems, stress monitoring, behavioural studies, and other applications where physiological responses can provide additional insight into an individual's internal emotional state. The primary contribution of EmoSI is the development of an end-to-end cloud-based platform capable of acquiring physiological signals, processing data in real time, performing machine learning inference, and presenting interpretable results through a centralised dashboard.

## Problem Statement

Emotional states influence how individuals communicate, learn, behave, and interact with others. However, understanding emotions is often challenging because traditional emotional assessment methods primarily rely on observation, interviews, questionnaires, or self-reporting. These approaches may not always provide an accurate representation of an individual's actual emotional state, particularly when the individual has difficulty expressing emotions verbally or behaviourally.

For children with emotional, behavioural, developmental, or communication challenges, the difficulty of accurately expressing feelings can be even more significant. Caregivers, educators, and healthcare professionals may therefore face challenges in obtaining timely and objective insights into a child's emotional condition. Similar challenges may also occur in other situations where individuals struggle to communicate their thoughts or emotions effectively, such as language learning environments, high-stress situations, or communication-related difficulties.

Recent advancements in wearable sensing technologies have enabled physiological signals to be collected continuously and non-invasively. Signals such as heart activity, skin conductance, body temperature, and movement patterns may provide additional information about an individual's physiological responses associated with emotional states. However, collecting physiological data alone is insufficient without an effective system to process, analyse, and present meaningful insights.

Furthermore, many existing emotion monitoring solutions are either limited to research environments, lack real-time cloud integration, or require specialised expertise to interpret physiological data. There remains a need for a scalable platform capable of integrating physiological sensing, cloud computing, machine learning, and user-friendly visualisation into a single ecosystem.

Therefore, this project proposes EmoSI, a cloud-based emotion monitoring platform that combines EmotiBit wearable sensing, AWS cloud services, machine learning, and interactive dashboard visualisation. The system serves as a foundational platform for exploring how physiological data can support emotion-related analysis and future research applications.

## Objectives

The primary objective of EmoSI is to develop a cloud-based emotion monitoring platform that combines wearable physiological sensing, machine learning, and cloud computing technologies to support emotion-related analysis and monitoring.

The specific objectives of the project are:

1. To collect and transmit physiological signals from the EmotiBit wearable device to AWS cloud services in real time.

2. To process physiological data using a machine learning pipeline developed from both publicly available datasets and manually labelled EmotiBit data for emotion recognition.

3. To develop an interactive dashboard that visualises physiological signals, emotion predictions, and historical records for monitoring and analysis purposes.

## Scope

EmoSI focuses on the collection, processing, analysis, and visualisation of physiological signals for emotion recognition using wearable sensing and cloud-based technologies. The project integrates hardware, cloud services, machine learning, and dashboard visualisation into a unified platform.

The scope of the project includes:

### Wearable Physiological Data Acquisition

The system uses the EmotiBit wearable device to collect physiological and motion-related signals, including:

- Photoplethysmography (PPG)
  - PPG_RED
  - PPG_GREEN
  - PPG_INFRARED

- Electrodermal Activity (EDA)
  - EDA
  - EDL (Tonic Component)
  - EDR (Phasic Component)

- Temperature Sensors
  - Skin Temperature (TEMP_1)
  - Thermopile Temperature

- Motion Sensors
  - Accelerometer (ACC_X, ACC_Y, ACC_Z)
  - Gyroscope (GYRO_X, GYRO_Y, GYRO_Z)
  - Magnetometer (MAG_X, MAG_Y, MAG_Z)

### Cloud-Based Data Processing

The project utilises AWS cloud services to support:

- Real-time data ingestion through AWS IoT Core
- Stream processing using Amazon Kinesis
- Data processing through AWS Lambda
- Emotion inference using Amazon SageMaker
- Data storage using Amazon DynamoDB

### Machine Learning-Based Emotion Recognition

The machine learning pipeline combines publicly available physiological datasets and manually labelled EmotiBit data. The system currently supports recognition of the following emotional states:

- Happy
- Neutral
- Nervous
- Sad
- Angry

For each prediction, the model produces probability scores for all supported emotion classes and identifies the dominant emotion based on the highest confidence value.

### Dashboard Visualisation

The Streamlit dashboard provides:

- Real-time physiological monitoring
- Real-time emotion prediction
- Dominant emotion display
- Emotion probability distribution
- Historical data visualisation
- Session monitoring and review

### Project Limitations

The current implementation is intended as a research and development platform and should not be considered a clinical, medical, or diagnostic tool. Although the project is motivated by challenges related to emotional assessment and communication difficulties, the system has not been specifically validated using large-scale datasets collected from children or other specialised populations. Additional data collection, model refinement, and validation studies would be required before deployment in specific real-world applications.

## Key Features

EmoSI provides several integrated features that support physiological data acquisition, cloud-based processing, machine learning inference, and emotion monitoring.

### Real-Time Physiological Monitoring

- Continuous acquisition of physiological signals using the EmotiBit wearable device.
- Collection of PPG, EDA, temperature, and motion sensor data.
- Real-time transmission of sensor readings to AWS cloud services.

### Cloud-Based Data Pipeline

- Secure data transmission using MQTT communication.
- Real-time data ingestion through AWS IoT Core.
- Stream processing using Amazon Kinesis.
- Serverless data processing with AWS Lambda.
- Scalable data storage using Amazon DynamoDB.

### Machine Learning-Based Emotion Recognition

- Hybrid dataset approach using WESAD and manually labelled EmotiBit data.
- Physiological signal preprocessing and feature engineering.
- Emotion classification using an XGBoost machine learning model.
- Real-time emotion inference through Amazon SageMaker.

### Emotion Analysis and Prediction

- Recognition of five emotional states:
  - Happy
  - Neutral
  - Nervous
  - Sad
  - Angry
- Probability scores generated for all emotion classes.
- Automatic identification of the dominant emotion based on the highest confidence score.

### Interactive Dashboard Visualisation

- Real-time physiological signal monitoring.
- Live emotion prediction display.
- Emotion probability distribution visualisation.
- Historical data review and trend analysis.
- Centralised monitoring through a user-friendly Streamlit dashboard.

### Scalable and Extensible Architecture

- Modular system architecture for future enhancements.
- Support for additional sensors and datasets.
- Potential integration with future emotion-aware applications and research platforms.

## Expected Outcome

The expected outcome of EmoSI is the development of a fully integrated cloud-based emotion monitoring platform capable of collecting physiological signals, processing data in real time, performing machine learning-based emotion recognition, and presenting meaningful insights through an interactive dashboard.

The project demonstrates the feasibility of combining wearable sensing technology, cloud computing infrastructure, and machine learning techniques within a single end-to-end system. Through the integration of EmotiBit, AWS cloud services, and an XGBoost-based emotion recognition model, the platform provides a foundation for future research involving physiological signal analysis and emotion-related applications.

In addition to demonstrating real-time emotion monitoring capabilities, the project establishes a reusable architecture that can support future work involving larger datasets, specialised target populations, improved machine learning models, and additional application domains. The platform serves as a proof-of-concept that can be extended and refined for future academic, research, or industry-focused developments.
