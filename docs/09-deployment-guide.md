
# Deployment Guide

## Overview

The EmoSI system was deployed using multiple AWS cloud services to enable real-time physiological data collection, storage, machine learning inference, and dashboard visualization.

The deployment architecture integrates EmotiBit wearable sensors with AWS IoT services, DynamoDB databases, SageMaker machine learning endpoints, and a Streamlit-based clinician dashboard.

---

# Deployment Architecture

The deployed EmoSI architecture follows the workflow below:

```text
EmotiBit Sensor
       │
       ▼
MQTT Communication
       │
       ▼
AWS IoT Core
       │
       ▼
Amazon Kinesis Data Stream
       │
       ▼
AWS Lambda Processing
       │
       ├────────► DynamoDB
       │              │
       │              ▼
       │      Physiological Data Storage
       │
       ▼
Amazon SageMaker Endpoint
       │
       ▼
Emotion Prediction
       │
       ▼
EmotionPredictions Table
       │
       ▼
Streamlit Dashboard
```

---

# AWS Services Used

| Service | Purpose |
|----------|----------|
| AWS IoT Core | Receives physiological data from EmotiBit devices |
| Amazon Kinesis Data Streams | Handles real-time data streaming |
| AWS Lambda | Processes incoming sensor data |
| Amazon DynamoDB | Stores physiological and prediction data |
| Amazon SageMaker | Hosts emotion prediction model |
| Amazon S3 | Stores trained model artifacts |
| IAM | Controls service permissions |
| Streamlit | Clinician dashboard interface |

---

# Step 1: Configure AWS IoT Core

AWS IoT Core acts as the entry point for incoming physiological data.

## Configuration Steps

1. Create an IoT Thing.
2. Generate certificates and keys.
3. Attach IoT policies.
4. Configure MQTT topics.
5. Connect the EmotiBit device.

Example MQTT Topic:

```text
emotibit/sensor_data
```

Data published through MQTT are forwarded to AWS services for processing.

---

# Step 2: Create Kinesis Data Stream

Amazon Kinesis Data Streams is used to handle incoming sensor data in real time.

## Stream Configuration

Stream Name:

```text
EmotiBitSensorStream
```

Purpose:

- Buffer incoming data
- Support scalable processing
- Reduce ingestion bottlenecks
- Enable real-time analytics

---

# Step 3: Configure Lambda Processing Function

AWS Lambda processes records received from Kinesis.

## Responsibilities

The Lambda function performs:

- Record validation
- Data formatting
- Feature extraction
- DynamoDB storage
- SageMaker inference requests

Incoming sensor fields include:

- PPG_RED
- PPG_GREEN
- PPG_INFRARED
- EDA
- EDL
- TEMP_1
- ACC_X
- ACC_Y
- ACC_Z
- GYRO_X
- GYRO_Y
- GYRO_Z
- MAG_X
- MAG_Y
- MAG_Z

---

# Step 4: Create DynamoDB Tables

## Physiological Data Table

Table Name:

```text
emotibit_data
```

Primary Keys:

| Attribute | Type |
|------------|------|
| device_id | Partition Key |
| timestamp | Sort Key |

Stored information includes:

- Physiological signals
- Motion sensor readings
- Temperature readings
- Session information

---

## Emotion Prediction Table

Table Name:

```text
EmotionPredictions
```

Purpose:

- Store model predictions
- Store confidence scores
- Store probability distributions

Example fields:

```text
predicted_emotion
confidence
happy_probability
neutral_probability
nervous_probability
sad_probability
angry_probability
```

---

# Step 5: Train Emotion Classification Model

The machine learning model was trained using the processed WESAD dataset.

## Dataset Preparation

Processing included:

- Signal cleaning
- Feature extraction
- Label mapping
- Feature normalization

Target emotion classes:

- Happy
- Neutral
- Nervous

---

## Model Training

Algorithm:

```text
XGBoost Classifier
```

Training environment:

```text
Amazon SageMaker
```

Performance:

```text
Accuracy: 98.86%
```

The trained model was exported and packaged for deployment.

---

# Step 6: Upload Model to Amazon S3

Model artifacts were stored in Amazon S3 before deployment.

Example files:

```text
xgboost_emotion_model.pkl
label_encoder.pkl
model.tar.gz
```

Purpose:

- Long-term storage
- SageMaker deployment source
- Model version management

---

# Step 7: Deploy SageMaker Endpoint

Amazon SageMaker hosts the trained emotion classification model.

## Deployment Workflow

1. Create SageMaker model.
2. Configure endpoint configuration.
3. Deploy endpoint.
4. Verify endpoint status.

Expected Status:

```text
InService
```

The endpoint receives physiological features and returns emotion predictions.

Example Response:

```json
{
  "predicted_emotion": "happy",
  "confidence": 0.9994
}
```

---

# Step 8: Configure IAM Permissions

IAM roles were created to allow communication between AWS services.

## Permissions Required

### IoT Core

- Publish to Kinesis

### Lambda

- Read from Kinesis
- Write to DynamoDB
- Invoke SageMaker Endpoint

### SageMaker

- Access S3 model artifacts

### Dashboard

- Read DynamoDB tables

---

# Step 9: Deploy Streamlit Dashboard

The clinician dashboard was developed using Streamlit.

Run locally using:

```bash
streamlit run dashboard.py
```

Dashboard capabilities:

- Patient management
- Appointment scheduling
- Session management
- Real-time monitoring
- Emotion visualization
- Historical analysis
- PDF report generation

---

# Step 10: System Verification

The complete deployment was verified by executing end-to-end tests.

## Verification Workflow

1. EmotiBit sends physiological data.
2. AWS IoT Core receives MQTT messages.
3. Kinesis streams incoming data.
4. Lambda processes records.
5. Data stored in DynamoDB.
6. SageMaker predicts emotion.
7. Predictions stored in EmotionPredictions.
8. Dashboard retrieves and visualizes results.

Successful completion of this workflow confirms proper system deployment.

---

# Deployment Outcome

The deployed EmoSI platform successfully integrates wearable sensing, cloud computing, machine learning inference, and clinician-facing visualization into a unified emotional monitoring system.

The architecture supports real-time data processing while maintaining scalability, reliability, and extensibility for future healthcare applications.
