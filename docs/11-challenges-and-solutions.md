# 11. Challenges and Solutions

## Overview

During the development of EMOSI, several technical and implementation challenges were encountered across hardware integration, cloud services, machine learning deployment, data visualization, and system integration. This section summarizes the major challenges faced and the solutions implemented throughout the project.

---

## Challenge 1: EmotiBit Sensor Connectivity Issues

### Problem

During the initial setup phase, the EmotiBit wearable device experienced communication issues with the ESP32 Feather board. The device occasionally failed to establish a stable connection, preventing physiological data from being streamed reliably.

### Solution

Several troubleshooting steps were performed:

- Updated EmotiBit firmware to the latest supported version
- Installed missing Arduino libraries
- Reconfigured Wi-Fi settings
- Verified serial communication between the ESP32 and EmotiBit modules
- Tested sensor outputs individually before full system integration

After these adjustments, stable sensor data streaming was achieved.

---

## Challenge 2: Real-Time Data Transmission

### Problem

The project required continuous transmission of physiological signals from the wearable device to the cloud. Initial approaches using local storage introduced delays and prevented real-time monitoring.

### Solution

A cloud-based streaming architecture was implemented using:

- AWS IoT Core
- Amazon Kinesis Data Streams
- AWS Lambda
- Amazon DynamoDB

This architecture enabled continuous real-time data transmission without relying on local file storage.

---

## Challenge 3: DynamoDB Data Storage Configuration

### Problem

Early testing revealed that incoming sensor data was not being stored correctly in DynamoDB due to partition key and timestamp configuration issues.

### Solution

The DynamoDB table schema was redesigned with:

- `device_id` as the partition key
- `timestamp` as the sort key

Additional validation was added to ensure all incoming records contained valid timestamps before insertion.

This resolved data storage inconsistencies and improved query performance.

---

## Challenge 4: AWS IAM Permission Errors

### Problem

Several AWS services failed to communicate during integration due to insufficient IAM permissions.

Examples included:

- IoT Core unable to write to DynamoDB
- Lambda unable to invoke SageMaker endpoints
- Restricted access to cloud resources

### Solution

Dedicated IAM roles and policies were created for:

- AWS IoT Core
- AWS Lambda
- Amazon SageMaker

Principle-of-least-privilege permissions were applied while ensuring required service access.

---

## Challenge 5: Machine Learning Model Deployment

### Problem

The trained XGBoost model performed well locally but failed during deployment to Amazon SageMaker due to dependency conflicts.

Errors included:

- No module named `numpy._core.multiarray`
- Pandas compatibility issues
- Missing package dependencies

### Solution

The model packaging process was revised by:

- Rebuilding the deployment environment
- Matching library versions between local and cloud environments
- Recreating the model archive
- Re-uploading model artifacts to Amazon S3

The SageMaker endpoint was successfully deployed and entered the `InService` state.

---

## Challenge 6: Emotion Prediction Accuracy

### Problem

Initial model training produced unstable prediction results due to class imbalance within the emotion dataset.

### Solution

Feature engineering and dataset preprocessing techniques were applied:

- Data cleaning
- Feature normalization
- Label balancing
- Feature selection

The final XGBoost model achieved approximately 98.86% classification accuracy during evaluation.

---

## Challenge 7: Real-Time Dashboard Visualization

### Problem

The dashboard initially displayed static graphs that did not update smoothly during live monitoring sessions.

Users experienced:

- Delayed graph updates
- Flat visualizations
- Poor monitoring experience

### Solution

The dashboard data refresh mechanism was redesigned to:

- Continuously retrieve recent DynamoDB records
- Update charts dynamically
- Maintain rolling windows of physiological signals

This provided a more responsive real-time monitoring interface.

---

## Challenge 8: Emotion Probability Presentation

### Problem

Early dashboard versions displayed emotion probabilities using standard bar charts, which were difficult to interpret quickly during monitoring sessions.

### Solution

The visualization was redesigned to display:

- Percentage values for each emotion
- Dominant emotion indicators
- Confidence levels

This improved readability for clinicians during live sessions.

---

## Challenge 9: Historical Session Report Generation

### Problem

Generating meaningful session summaries required combining data from multiple sources including physiological signals, emotion predictions, and clinician observations.

### Solution

A PDF report generation module was developed to automatically compile:

- Patient information
- Session statistics
- Emotion distributions
- Physiological summaries
- Observation notes
- Session conclusions

This provided clinicians with a structured post-session report.

---

## Challenge 10: End-to-End System Integration

### Problem

The project involved multiple interconnected components:

- EmotiBit wearable device
- AWS cloud services
- Machine learning model
- Database
- Dashboard application

Ensuring reliable communication between all components was complex.

### Solution

Incremental integration testing was performed throughout development.

Each module was validated independently before being integrated into the complete system. Continuous testing helped identify issues early and improved overall system stability.

---

## Challenge 11: EmotiBit Device Failure and Recovery

### Problem

During development, the EmotiBit device suddenly became unresponsive. The device showed no indicator lights, could not be charged, and was not detected by the computer. This prevented further sensor testing and data collection activities.

### Solution

Technical support was requested directly from the EmotiBit development team through email communication.

The support team recommended:

- Reinstalling and updating the device firmware using the EmotiBit Firmware Installer
- Verifying USB connection and driver installation
- Performing a firmware recovery process
- Ensuring that the EmotiBit Firmware Installer and Arduino IDE were not running simultaneously, as both applications may attempt to access the same communication port and cause conflicts

After following the recovery procedure and reinstalling the firmware, the device became operational again and data collection was successfully resumed.

### Lessons Learned

The experience highlighted the importance of maintaining communication with official hardware support channels. The EmotiBit support team provided detailed troubleshooting guidance and responded reliably during their office hours.

Future developers working with EmotiBit devices are encouraged to contact the EmotiBit support team whenever hardware-related issues occur, as many firmware and connectivity problems can be resolved through official troubleshooting procedures.

---

## Summary

Despite challenges related to hardware integration, cloud infrastructure, machine learning deployment, and dashboard development, all major system components were successfully integrated into the EMOSI platform. The solutions implemented resulted in a functional end-to-end emotional monitoring system capable of collecting physiological data, performing emotion prediction, and presenting actionable insights through a web-based dashboard.
