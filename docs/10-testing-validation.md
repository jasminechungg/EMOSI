# Testing and Validation

## Overview

Testing and validation were conducted throughout the development of the EmoSI platform to ensure that all system components operated correctly and communicated successfully.

The testing process focused on four major areas:

1. Functional Testing
2. AWS Integration Testing
3. Dashboard Testing
4. Machine Learning Validation

The objective was to verify that physiological data could be collected, processed, stored, analyzed, and visualized accurately within the deployed cloud architecture.

---

# Functional Testing

## Objective

To verify that each module performs its intended functionality correctly.

---

## Functional Testing Results

| Module | Function Tested | Result |
|----------|----------------|----------|
| User Authentication | Login and account registration | Pass |
| Patient Management | Create and view patient records | Pass |
| Appointment Scheduling | Create and manage appointments | Pass |
| Session Management | Start and end monitoring sessions | Pass |
| Observation Notes | Record clinician observations | Pass |
| Historical Sessions | Retrieve previous monitoring sessions | Pass |
| PDF Report Generation | Generate session summary reports | Pass |

---

## Functional Testing Summary

All core system modules operated successfully without critical functional errors.

The dashboard successfully supported the complete monitoring workflow from patient registration to report generation.

---

# AWS Integration Testing

## Objective

To verify communication between AWS services used in the EmoSI architecture.

---

## Components Tested

- AWS IoT Core
- Amazon Kinesis Data Streams
- AWS Lambda
- Amazon DynamoDB
- Amazon SageMaker
- Amazon S3

---

## AWS Integration Results

| Component | Test Description | Result |
|------------|-----------------|----------|
| AWS IoT Core | Receive MQTT messages | Pass |
| Kinesis Data Stream | Receive streaming records | Pass |
| Lambda Trigger | Process incoming records | Pass |
| DynamoDB | Store physiological data | Pass |
| SageMaker Endpoint | Return emotion predictions | Pass |
| S3 Storage | Retrieve model artifacts | Pass |

---

## End-to-End Data Flow Validation

The complete system workflow was successfully verified.

```text
EmotiBit
    ↓
AWS IoT Core
    ↓
Amazon Kinesis Data Stream
    ↓
AWS Lambda
    ↓
Amazon DynamoDB
    ↓
Amazon SageMaker Endpoint
    ↓
Emotion Predictions
    ↓
Streamlit Dashboard
```

All components communicated successfully throughout testing.

---

# DynamoDB Storage Testing

## Objective

To verify successful storage of physiological signals and prediction results.

---

## Physiological Data Storage

The system successfully stored sensor data including:

- PPG_RED
- PPG_GREEN
- PPG_INFRARED
- EDA
- EDL
- EDR
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

Data were successfully written to the `emotibit_data` table.

---

## Emotion Prediction Storage

Emotion prediction results were successfully written to the `EmotionPredictions` table.

Stored fields included:

- Predicted emotion
- Confidence score
- Emotion probabilities
- Timestamp
- Session information

---

# SageMaker Endpoint Testing

## Objective

To verify successful deployment and inference of the machine learning model.

---

## Endpoint Status Verification

The deployed SageMaker endpoint successfully entered the following state:

```text
InService
```

This confirmed successful model deployment.

---

## Prediction Testing

Example prediction output:

```json
{
  "predicted_emotion": "happy",
  "confidence": 0.999454
}
```

The endpoint successfully returned emotion classifications and confidence scores.

---

# Dashboard Testing

## Objective

To verify correct visualization and retrieval of data from DynamoDB.

---

## Dashboard Components Tested

### Patient Management

Functions verified:

- Create patient
- View patient records
- Display session history

Result:

```text
Pass
```

---

### Appointment Scheduling

Functions verified:

- Create appointment
- View appointment schedule
- Update appointment information

Result:

```text
Pass
```

---

### Session Management

Functions verified:

- Start monitoring session
- End monitoring session
- Record observation notes

Result:

```text
Pass
```

---

### Real-Time Monitoring Dashboard

Functions verified:

- Heart Rate visualization
- EDA visualization
- EDL visualization
- EDR visualization
- Accelerometer monitoring
- Gyroscope monitoring
- Magnetometer monitoring

Result:

```text
Pass
```

---

### Emotion Prediction Dashboard

Functions verified:

- Display emotion probabilities
- Display dominant emotion
- Update prediction results

Result:

```text
Pass
```

---

### Historical Session Dashboard

Functions verified:

- Retrieve completed sessions
- Display physiological history
- Display emotion history
- Generate reports

Result:

```text
Pass
```

---

# Machine Learning Validation

## Objective

To evaluate the performance of the emotion classification model.

---

## Dataset Information

Dataset used:

```text
WESAD
```

Processed dataset size:

```text
2187 samples × 55 features
```

Emotion classes:

- Happy
- Nervous
- Neutral

---

## Model Selection

Algorithm used:

```text
XGBoost Classifier
```

The model was selected due to its strong performance on structured physiological features.

---

## Classification Accuracy

Final model accuracy:

```text
98.86%
```

This indicates that the model correctly classified emotional states for the majority of testing samples.

---

## Emotion Distribution

Training data distribution:

| Emotion | Samples |
|----------|----------|
| Neutral | 1180 |
| Nervous | 648 |
| Happy | 359 |

---

# Overall Testing Outcome

The testing results demonstrate that the EmoSI platform successfully integrates wearable sensing, cloud computing, machine learning inference, and web-based visualization into a unified emotional monitoring system.

All major modules passed testing and successfully performed their intended functions.

The deployed AWS architecture operated reliably throughout the validation process, while the machine learning model achieved high classification accuracy for emotion prediction.

These results confirm that the EmoSI platform is capable of supporting real-time physiological monitoring and emotion analysis within the proposed system architecture.
