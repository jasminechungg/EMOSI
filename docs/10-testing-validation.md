# Testing and Validation

## Overview

Testing and validation were performed throughout the development of EmoSI to ensure that all system components function correctly both individually and as an integrated platform.

The testing process focused on:

- Physiological data acquisition
- Cloud communication
- Real-time data streaming
- Database storage and retrieval
- Machine learning inference
- Dashboard visualization
- Session management
- Report generation

The objective was to verify that physiological sensor data could be collected, transmitted, processed, analyzed, stored, and visualized reliably within the emotional monitoring system.

---

## 10.1 Sensor Data Acquisition Testing

### Objective

Verify that the EmotiBit wearable device successfully captures physiological and motion-related signals.

### Test Procedure

1. Connect the EmotiBit device to the ESP32 microcontroller.
2. Start physiological monitoring.
3. Observe incoming sensor readings.
4. Verify that signals are generated continuously.

### Expected Result

The system should continuously acquire physiological and motion sensor readings.

### Actual Result

The device successfully captured and transmitted:

- PPG Infrared
- PPG Red
- PPG Green
- EDA
- EDL
- Skin Temperature
- Thermopile Temperature
- Accelerometer
- Gyroscope
- Magnetometer

### Status

✅ Passed

---

## 10.2 AWS IoT Core Communication Testing

### Objective

Verify secure MQTT communication between the wearable device and AWS cloud services.

### Test Procedure

1. Connect the ESP32 device to AWS IoT Core.
2. Publish physiological sensor data.
3. Monitor MQTT topics and incoming messages.

### Expected Result

MQTT messages should be received successfully by AWS IoT Core.

### Actual Result

Physiological sensor messages were successfully transmitted from the wearable device and received by AWS IoT Core for downstream processing.

### Status

✅ Passed

---

## 10.3 Amazon Kinesis Data Stream Testing

### Objective

Verify that incoming physiological data streams are forwarded correctly for real-time processing.

### Test Procedure

1. Publish sensor readings through AWS IoT Core.
2. Route messages into Amazon Kinesis Data Streams.
3. Monitor stream activity.

### Expected Result

Incoming physiological data should appear within the Kinesis stream.

### Actual Result

Physiological sensor data was successfully streamed into Amazon Kinesis Data Streams and became available for processing and machine learning inference.

### Status

✅ Passed

---

## 10.4 DynamoDB Storage Testing

### Objective

Verify that physiological readings and prediction results are stored correctly in DynamoDB.

### Test Procedure

1. Start a monitoring session.
2. Transmit physiological data.
3. Verify database records.
4. Retrieve stored information.

### Expected Result

Records should be stored successfully with correct identifiers and timestamps.

### Actual Result

The system successfully stored:

- Physiological sensor data
- Emotion prediction results
- Patient records
- Session information
- Historical monitoring data

### Status

✅ Passed

---

## 10.5 Machine Learning Prediction Testing

### Objective

Evaluate the ability of the machine learning model to classify emotional states from physiological signals.

### Test Procedure

1. Collect physiological sensor readings.
2. Extract relevant features.
3. Submit features to the SageMaker endpoint.
4. Review prediction output.

### Expected Result

The model should return an emotion prediction and confidence values.

### Actual Result

The deployed XGBoost model successfully generated real-time emotion predictions and probability distributions.

Supported emotional categories include:

- Happy
- Nervous
- Neutral
- Sad
- Angry

Prediction results were displayed in the dashboard and stored for historical analysis.

### Status

✅ Passed

---

## 10.6 Dashboard Visualization Testing

### Objective

Verify that clinicians can view physiological signals, emotion predictions, and session information through the dashboard.

### Test Procedure

1. Start a monitoring session.
2. Observe dashboard updates.
3. Review historical records.
4. Verify visualization components.

### Expected Result

The dashboard should display live and historical information accurately.

### Actual Result

The dashboard successfully displayed:

- Live physiological signal trends
- Heart rate monitoring
- EDA, EDL, and EDR signals
- Movement analysis
- Emotion probability summaries
- Historical session records
- Patient information
- Session reports

### Status

✅ Passed

---

## 10.7 Session Management Testing

### Objective

Verify that clinicians can create, monitor, and complete monitoring sessions.

### Test Procedure

1. Select a patient.
2. Start a monitoring session.
3. Add observation notes.
4. End the session.

### Expected Result

Session information should be recorded and linked to the selected patient.

### Actual Result

Monitoring sessions were successfully created, updated, completed, and stored. Observation notes and session summaries were correctly associated with patient records.

### Status

✅ Passed

---

## 10.8 PDF Report Generation Testing

### Objective

Verify that monitoring reports can be generated automatically after session completion.

### Test Procedure

1. Complete a monitoring session.
2. Generate a session report.
3. Review generated content.

### Expected Result

A complete report should be generated containing session information and emotion analysis.

### Actual Result

The generated PDF reports successfully included:

- Patient information
- Session details
- Emotion summaries
- Physiological signal summaries
- Observation timelines
- Session conclusions
- Clinician notes

### Status

✅ Passed

---

## 10.9 Overall System Validation

The completed EmoSI platform successfully demonstrated end-to-end emotional monitoring through the integration of wearable physiological sensing, AWS cloud services, machine learning analysis, and dashboard visualization.

The validation process confirmed that:

- Physiological data can be collected in real time.
- Sensor readings can be transmitted securely through AWS cloud services.
- Data can be streamed using Amazon Kinesis.
- Information can be stored and retrieved from DynamoDB.
- Machine learning models can generate emotion predictions.
- Clinicians can monitor participants through an interactive dashboard.
- Session reports can be generated automatically for review and documentation.

Overall, the system achieved the project objectives and demonstrated the feasibility of cloud-based physiological emotion monitoring using wearable IoT devices, AWS cloud infrastructure, and machine learning technologies.

---

## Testing Summary

| Test Component | Result |
|---------------|---------|
| Sensor Data Acquisition | ✅ Passed |
| AWS IoT Core Communication | ✅ Passed |
| Amazon Kinesis Streaming | ✅ Passed |
| DynamoDB Storage | ✅ Passed |
| Machine Learning Prediction | ✅ Passed |
| Dashboard Visualization | ✅ Passed |
| Session Management | ✅ Passed |
| PDF Report Generation | ✅ Passed |
| Overall System Validation | ✅ Passed |

The testing results indicate that all major system components operated successfully and met the functional requirements defined for the project.
