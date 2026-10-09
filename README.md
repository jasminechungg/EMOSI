# EmoSI: Wearable Sensor and Machine Learning Approaches for Detecting Emotional and Behavioural States in Children

EmoSI is my Final Year Project (FYP) for my degree in Computer Science at Universiti Sains Malaysia (USM). This project explores the use of wearable physiological sensors, machine learning, and cloud computing to analyse physiological signals and identify potential emotional states.

The project uses **EmotiBit** to collect physiological data, an **ESP32** to support sensor data transmission through MQTT, **Amazon Web Services (AWS)** to handle data storage and machine learning inference, and a **Streamlit dashboard** to display the collected data and emotion predictions.

This repository contains the code, selected implementation examples, system documentation, diagrams, and screenshots from my project. It is intended to share my development process and help others understand how the system works.

> **Project status:** Academic prototype. The system explores emotion classification using physiological data and has not been clinically validated for assessing emotional or behavioural difficulties in children.

## Table of Contents

- [Project Background](#project-background)
- [Project Objectives](#project-objectives)
- [About EmotiBit](#about-emotibit)
- [System Architecture](#system-architecture)
- [Machine Learning Approach](#machine-learning-approach)
- [AWS Cloud Integration](#aws-cloud-integration)
- [Dashboard](#dashboard)
- [Repository Structure](#repository-structure)
- [Dataset Information](#dataset-information)
- [Getting Started](#getting-started)
- [Important Notes](#important-notes)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)

## Project Background

Emotional and behavioural states can be difficult to understand through observation alone. Physiological signals provide another source of information that can be explored alongside other assessment methods.

For this project, I used EmotiBit, a wearable sensor device that collects physiological signals, to explore whether these signals could be processed by a machine learning model to classify different emotional states.

The collected data is processed and passed through an AWS-based pipeline, where the trained model generates emotion predictions. The results can then be stored and presented through a dashboard for easier monitoring and review.

The main idea behind EmoSI is to explore how wearable technology, machine learning, and cloud computing can be combined into one system. Although the project focuses on the potential application of emotional and behavioural assessment in children, the current prototype should not be treated as a diagnostic tool.

## Project Objectives

The project focuses on three main objectives:

1. **Physiological Data Collection and Storage:** Collect physiological signals using EmotiBit and store the relevant data in AWS DynamoDB during monitoring sessions.
2. **Machine Learning and Emotion Analysis:** Process physiological data and apply machine learning techniques to classify emotional states, with the potential for further analysis using additional methods.
3. **Dashboard Development:** Develop a dashboard to present physiological readings, emotion predictions, historical records, and session reports for easier review.

## About EmotiBit

[EmotiBit](https://github.com/EmotiBit) is a wearable biometric sensing platform designed for collecting physiological signals. I selected EmotiBit as the main sensing device for this project because it provides access to several types of physiological and movement-related data that can be explored for emotion-related analysis.

Some of the signals relevant to this project include:

| Signal | Description |
|---|---|
| PPG (Red, Green, Infrared) | Optical signals used to study pulse-related information |
| EDA | Electrodermal activity, which reflects changes in skin conductance |
| Temperature | Skin or thermopile temperature readings, depending on the device configuration |
| Accelerometer | Measures movement and acceleration along three axes |
| Gyroscope | Measures rotational movement |
| Magnetometer | Measures magnetic field readings along three axes |
| Heart Rate and HRV | Derived metrics that may be calculated from suitable pulse and inter-beat interval data |

The availability of individual signals and derived metrics depends on the hardware, firmware, data processing, and recording configuration.

For more information about the device, setup instructions, available signals, firmware, and data format, please refer to the official EmotiBit resources:

- [EmotiBit GitHub Organisation](https://github.com/EmotiBit)
- [EmotiBit Documentation and Tutorials](https://github.com/EmotiBit/EmotiBit_Docs)
- [EmotiBit Firmware for Feather Boards](https://github.com/EmotiBit/EmotiBit_FeatherWing)
- [EmotiBit Getting Started Guide](https://github.com/EmotiBit/EmotiBit_Docs/blob/master/Getting_Started.md)

For this project, I connected EmotiBit with an ESP32-based setup and developed code to transmit sensor data through MQTT. Two MQTT approaches are provided in the ESP32 directory: AWS IoT Core and HiveMQ Cloud (BeeHiveMQ in my code notes).

More details about the hardware setup and code configuration are available in [`code/esp32/`](code/esp32/).

## System Architecture

EmoSI combines hardware, data transmission, cloud storage, machine learning inference, and a dashboard into one workflow.

The main processing flow is:

1. **Data Collection:** EmotiBit collects physiological and movement-related signals.
2. **ESP32 and MQTT:** The ESP32-based setup transmits sensor data through MQTT.
3. **AWS IoT Core:** Receives incoming sensor messages.
4. **Amazon Kinesis Data Streams:** Streams incoming data for downstream processing.
5. **AWS Lambda:** Processes incoming records, prepares the required features, and invokes the deployed machine learning model.
6. **Amazon SageMaker:** Hosts the trained XGBoost model and generates emotion predictions.
7. **Amazon DynamoDB:** Stores relevant sensor records and prediction results.
8. **Streamlit Dashboard:** Presents available sensor data, emotion predictions, historical information, and session reports.

Amazon S3 is also used for dataset files and machine learning artifacts, including model packages used in the development and deployment process.

The exact configuration of each service depends on the implementation and AWS resources being used.

## Machine Learning Approach

The project uses **XGBoost** for emotion classification. The model takes processed physiological features as input and produces a predicted emotion class along with its associated probability distribution.

The five emotion classes supported by the final model are:

- Happy
- Nervous
- Neutral
- Sad
- Angry

The general machine learning workflow includes:

1. Preparing and processing physiological data.
2. Preparing the corresponding emotion labels.
3. Extracting and arranging the features expected by the model.
4. Training the XGBoost classifier.
5. Evaluating the model using classification metrics.
6. Saving the trained model and supporting metadata.
7. Deploying the model through Amazon SageMaker.
8. Invoking the endpoint to generate predictions.

The evaluation process can include accuracy, precision, recall, F1-score, and a confusion matrix. Actual performance should be reported using the relevant evaluation results rather than assumed from example code.

The [`sagemaker/`](sagemaker/) directory contains selected code examples and explanations of the training, evaluation, model packaging, inference, and deployment process.

## AWS Cloud Integration

AWS provides the cloud infrastructure used to process, store, and serve data throughout the project.

| AWS Service | Role in EmoSI |
|---|---|
| AWS IoT Core | Receives sensor messages through MQTT |
| Amazon Kinesis Data Streams | Streams incoming sensor records |
| AWS Lambda | Processes data and coordinates model inference |
| Amazon S3 | Stores datasets, model artifacts, and deployment packages |
| Amazon DynamoDB | Stores sensor readings and relevant emotion prediction results |
| Amazon SageMaker | Hosts the trained machine learning model |

These services work together to support the prototype's data processing and prediction workflow.

To run the system in another environment, users will need to configure their own AWS resources, IAM permissions, database tables, endpoints, and connection settings. The code examples in this repository do not automatically connect to my private AWS environment.

## Dashboard

The project includes a Streamlit dashboard developed to present the available data and system results through a graphical interface.

The dashboard includes interface components for:

- User login and registration
- Patient or participant management
- Monitoring session management
- Appointment scheduling
- Live or recent physiological readings
- Emotion prediction and probability information
- Historical session information
- Session summary reports

The repository includes screenshots to help users understand the intended interface and workflow.

Some uploaded UI elements and displayed values are hardcoded for prototype demonstration purposes. This allows users to explore the interface and understand how the dashboard is organised without requiring access to my private database or AWS configuration.

To use the dashboard as a fully functional system, users need to connect it to their own database and configure the relevant AWS services so the interface can retrieve and display actual data.

See [`dashboard/`](dashboard/) for the dashboard code and [`docs/08-dashboard-development.md`](docs/08-dashboard-development.md) for further details.

## Project Demonstration

For a better understanding of how EmoSI works, you can watch the project demonstration video below. The video provides a visual overview of the prototype, its features, and how the system is used.

**YouTube Video:** [Watch the EmoSI Project Demonstration](https://youtu.be/tHqJS0l7D4U)
 
## Repository Structure

The repository is organised into several directories to separate the ESP32 code, AWS implementation, dashboard, datasets, documentation, and visual references.

```text
EMOSI/
├── code/
│   ├── aws/
│   │   ├── sagemaker/
│   │   │   └── README.md
│   │   ├── lambda/
│   │   └── dashboard/
│   │       ├── prototype/
│   │       └── README.md
│   └── esp32/
│       ├── README.md
│       ├── libraries.zip
│       ├── mqtt aws iot core
│       └── mqtt hivemq
├── datasets/
│   └── README.md
├── diagrams/
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-system-architecture.md
│   ├── 03-hardware-setup.md
│   ├── 04-cloud-architecture.md
│   ├── 05-data-pipeline.md
│   ├── 06-machine-learning-pipeline.md
│   ├── 07-database-design.md
│   ├── 08-dashboard-development.md
│   ├── 09-deployment-guide.md
│   ├── 10-testing-validation.md
│   ├── 11-challenges-and-solutions.md
│   └── 12-future-work.md
├── screenshots/
├── .gitignore
└── README.md
```

### Directory Descriptions

| Directory | Description |
|---|---|
| [`code/esp32/`](code/esp32/) | Contains the ESP32 code used to connect EmotiBit and transmit sensor data through MQTT. Two approaches are provided: AWS IoT Core and HiveMQ. The directory also includes a supporting library ZIP and setup instructions. |
| [`code/aws/sagemaker/`](code/aws/sagemaker/) | Contains documentation and selected code examples for machine learning training, evaluation, model packaging, inference, and deployment using Amazon SageMaker. |
| [`code/aws/lambda/`](code/aws/lambda/) | Contains AWS Lambda code used for data processing and integration with the machine learning pipeline. |
| [`code/aws/dashboard/prototype/`](code/aws/dashboard/prototype/) | Contains the Python files used to build the individual pages and UI components of the Streamlit dashboard. |
| [`code/aws/dashboard/README.md`](code/aws/dashboard/README.md) | Explains the dashboard prototype, its setup, and the configuration required to connect it to a user's own database and AWS environment. |
| [`datasets/`](datasets/) | Contains dataset information and instructions for accessing publicly available datasets. The private EmotiBit dataset is not included. |
| [`diagrams/`](diagrams/) | Contains diagrams illustrating the system architecture, data flow, and other project designs. |
| [`docs/`](docs/) | Contains detailed project documentation covering the system overview, hardware setup, cloud architecture, data pipeline, machine learning, database design, dashboard development, deployment, testing, challenges, and future work. |
| [`screenshots/`](screenshots/) | Contains screenshots of the dashboard pages and sample session reports to demonstrate the prototype interface. |

### Additional Notes

The repository is organised this way to make it easier to explore the different components of EmoSI without needing to understand the entire system at once.

Some directories contain complete source files, while others provide selected code examples or documentation. Users may need to configure their own hardware, dependencies, database connections, and AWS resources before running the system in their environment.

## Dataset Information

The project uses the WESAD dataset and EmotiBit recordings as part of the work on physiological data and emotion classification.

### WESAD Dataset

The WESAD (Wearable Stress and Affect Detection) dataset is publicly available through the UCI Machine Learning Repository.

Dataset link: [WESAD - Wearable Stress and Affect Detection](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection)

Please refer to the original dataset page for its download instructions, description, and usage conditions.

### EmotiBit Dataset

The EmotiBit dataset collected for this project is not included in this repository because it contains physiological data collected from me and other participants.

To respect the privacy of everyone involved and protect the personal data collected during the sessions, this dataset will not be shared publicly.

Users can still refer to the source code, documentation, and publicly available WESAD dataset to understand the general data processing and machine learning workflow used in this project.

## Getting Started

This repository is intended to help users explore the implementation and understand how the components of EmoSI fit together.

### 1. Clone the repository

```bash
git clone https://github.com/jasminechungg/EMOSI.git
cd EMOSI
```

### 2. Explore the documentation

Start with the project overview and architecture documentation in [`docs/`](docs/). These documents explain the project's design, AWS integration, data storage, machine learning pipeline, dashboard, testing, and future work.

### 3. Review the ESP32 code

Open [`code/esp32/`](code/esp32/) to review the MQTT connection approaches and hardware setup instructions.

You will need a compatible ESP32 board, the required Arduino board package and libraries, and your own MQTT or AWS IoT Core configuration to test the code with hardware.

Refer to the README in that directory for the specific setup details.

### 4. Review the machine learning implementation

Open [`sagemaker/`](sagemaker/) to understand the main steps for training, evaluating, packaging, and deploying the model.

The code snippets are provided as examples and may need to be adapted to your dataset, Python environment, AWS resources, and model artifacts.

### 5. Configure the dashboard

Open [`dashboard/`](dashboard/) and review its dependencies and setup instructions.

The dashboard may display demonstration values until you connect it to a database and configure the required services. You will need your own database configuration and appropriate AWS permissions to retrieve real data.

### 6. Configure AWS resources

If you want to reproduce the cloud workflow, configure the necessary AWS services, including IoT Core, Kinesis Data Streams, Lambda, S3, DynamoDB, and SageMaker.

Use your own AWS account and resources. Do not expect the repository to connect automatically to the original project environment.

## Important Notes

### Code Examples and Implementation Experience

Not every file in this repository represents a complete, ready-to-run implementation. Some directories contain selected code snippets to demonstrate important parts of the system rather than the full original code.

The actual development process involved extensive trial and error, debugging, dependency adjustments, repeated testing, and rechecking. Several parts required multiple revisions before working properly with the hardware, datasets, Python libraries, and AWS services.

The code examples are intended to help readers understand the general implementation approach. They may require further configuration or modification before they can run in another environment.

### Credentials and Configuration

For security reasons, private credentials and sensitive configuration details are not provided.

Before running the code, configure your own credentials, endpoints, certificates, database tables, and other required resources. Never commit AWS access keys, secret keys, private certificates, passwords, or other sensitive information to a public repository.

### Dashboard Demonstration Values

Some dashboard components use hardcoded values to demonstrate the intended UI and workflow. A fully functional deployment requires connecting the dashboard to the appropriate database and services.

### Data Privacy

The EmotiBit dataset collected during the project is not publicly available because it contains personal physiological data from participants. Please respect this restriction and do not assume that the private dataset can be requested from the repository.

## Limitations

EmoSI is an academic prototype developed to explore wearable sensing and machine learning for emotion classification.

The predicted emotion classes represent the model's estimates based on the input features. Physiological signals can be influenced by many factors, including movement, individual differences, sensor placement, and the surrounding environment.

The current prototype has not been clinically validated for diagnosing or assessing emotional and behavioural difficulties in children. Its predictions should not be treated as definitive conclusions about a person's emotional state.

Further work involving appropriate child-specific data, ethical approval, consent, validation, and professional assessment would be required before considering use in real clinical or child-assessment settings.

## Future Work

Possible future improvements include:

- Collecting a larger and more diverse dataset with appropriate consent and privacy protection.
- Evaluating and improving model performance across different participants and conditions.
- Refining physiological signal processing and feature extraction.
- Exploring additional machine learning approaches.
- Improving the dashboard's live data integration and reporting features.
- Conducting further testing and validation before considering practical applications.

## Acknowledgements

I would like to acknowledge the EmotiBit team for providing the wearable sensing platform and its supporting documentation, as well as the researchers who made the WESAD dataset publicly available.

This project was developed as part of my undergraduate Final Year Project at Universiti Sains Malaysia.

Thank you for taking the time to explore my EmoSI project and repository.
