# EmoSI - Amazon SageMaker

This directory documents the machine learning model used in EmoSI to predict emotions from physiological signals collected using EmotiBit.

The project uses **XGBoost** for emotion classification and **Amazon SageMaker** to host the model for inference. The model supports five emotion classes: Happy, Nervous, Neutral, Sad, and Angry.

Rather than including the full training and deployment scripts, this README highlights the important parts of the implementation to help users understand how the model works and how it integrates with the AWS environment.

## Important Note on the Code Examples

The code snippets shared in this directory are only brief examples of the main steps involved in the EmoSI machine learning pipeline. They are included to give readers a general understanding of how the model training, evaluation, deployment, and inference processes work.

The actual implementation process was much more lengthy and involved repeated trial and error, debugging, testing, and rechecking. Some parts required multiple adjustments before they could work properly with the dataset, Python libraries, model artifacts, and AWS services. The complete implementation also involves more code and configuration than what is shown here.

The snippets have been shortened for easier understanding and are not intended to be copied and run as a complete system without further configuration. Variable names, model parameters, file paths, and other settings may need to be adjusted according to the actual environment.

**Please note:** The code provided is mainly to demonstrate the structure and format of the implementation. It should not be treated as the exact final code or as proof of the model's performance. Actual results must be obtained by running the relevant code against the appropriate dataset.

# Model Evaluation: Accuracy, Precision, Recall, and F1-Score

After training the XGBoost model, its performance can be evaluated using several classification metrics. These metrics help show how well the model predicts each emotion class, rather than relying on accuracy alone.

The following is a sample evaluation code:

```python
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)

# Generate predictions using the test dataset
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Calculate macro and weighted F1-scores
macro_f1 = f1_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

weighted_f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

print(f"Accuracy: {accuracy:.4f}")
print(f"Macro F1-Score: {macro_f1:.4f}")
print(f"Weighted F1-Score: {weighted_f1:.4f}")

# Display precision, recall, and F1-score for each class
print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

# Display the confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
```

### What the metrics mean

- **Accuracy:** The proportion of test samples that the model classifies correctly.
- **Precision:** How often the model's predictions for a particular emotion class are correct.
- **Recall:** How many of the actual samples belonging to a particular class are correctly identified.
- **F1-score:** A balance between precision and recall.
- **Macro F1-score:** Calculates the F1-score for each class and gives every class equal weight.
- **Weighted F1-score:** Calculates the F1-score for each class while accounting for the number of samples in each class.
- **Confusion matrix:** Shows the number of correct and incorrect predictions for each class, helping identify which emotions the model may confuse.

### Remarks

This evaluation code is an example of the format used to assess a classification model. The metrics shown when the code is executed will depend on the model, test dataset, and evaluation procedure.

No fixed accuracy or F1-score is provided here because the actual values should be obtained from the relevant evaluation run. Results from an earlier model or a different dataset should not automatically be presented as the performance of the final deployed five-class model.

For a fair evaluation, the test data should be kept separate from the data used to train the model. The preprocessing steps, feature order, and label mapping must also remain consistent with the trained model.

## Final Remarks

The examples in this repository are intended to help readers understand the general approach used in EmoSI, rather than reproduce the entire development process from a few code snippets. Setting up a similar system may require additional experimentation, dependency adjustments, AWS configuration, and repeated validation before everything works as expected.

---

# 1. Model Training and Evaluation

The model training process uses preprocessed physiological features and their corresponding emotion labels. The dataset is divided into training and testing sets to evaluate the model's performance.

### Preparing the training data

The `LabelEncoder` converts emotion labels into numerical values so they can be used by the XGBoost classifier.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_labels)

X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y_encoded,
    test_size=0.15,
    random_state=42,
    stratify=y_encoded
)
```

Here, `X_features` represents the processed physiological features, while `y_labels` contains the corresponding emotion labels. The split ratio shown above is an example and may differ from the configuration used to train the deployed model.

### Training the XGBoost model

XGBoost is used to classify the physiological features into the supported emotion classes.

```python
model = xgb.XGBClassifier(
    objective="multi:softprob",
    num_class=len(label_encoder.classes_),
    eval_metric="mlogloss",
    random_state=42
)

model.fit(X_train, y_train)
```

The configuration above is a simplified example. The actual model's hyperparameters should be taken from its original training code.

### Evaluating model performance

The model can be evaluated using accuracy, precision, recall, F1-score, and a confusion matrix.

```python
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

These metrics help assess the model's classification performance and identify emotion classes that may be difficult to distinguish. Evaluation results should be reported using the actual output from the relevant test dataset.

## 2. Saving the Model and Supporting Files

After training, the model and its supporting metadata need to be saved for deployment.

Important files include:

- **Model file:** Contains the trained XGBoost model.
- **Label classes:** Defines the emotion labels and their corresponding order.
- **Feature columns:** Records the feature names and order expected by the model.

For example, the model can be saved in JSON format:

```python
model.save_model("hybrid_5emotion_accmag_model.json")
```

Keeping the feature names, feature order, and label mapping consistent is important because the deployed model must receive data in the format it expects.

The code above demonstrates the saving process. It does not recreate the exact model already deployed in AWS.

## 3. SageMaker Inference

The inference script loads the trained model, receives physiological features, and returns the predicted emotion together with its confidence and probability distribution.

The main prediction step can be represented as follows:

```python
probabilities = model.predict_proba(features)[0]

predicted_index = int(np.argmax(probabilities))

prediction = {
    "predicted_emotion": label_classes[predicted_index],
    "confidence": float(probabilities[predicted_index]),
    "probabilities": {
        label_classes[i]: float(probabilities[i])
        for i in range(len(label_classes))
    }
}
```

The output contains:

- `predicted_emotion`: The emotion class with the highest predicted probability.
- `confidence`: The probability associated with the predicted class.
- `probabilities`: The probability distribution across the five emotion classes.

These probabilities represent the model's estimates, not a clinical assessment or a definitive measurement of a person's emotional state.

## 4. Packaging the Model for Deployment

The model and its supporting files are packaged into a compressed archive before being uploaded to Amazon S3 for SageMaker deployment.

An example package structure is:

```text
model_5emotion_v2.tar.gz
├── hybrid_5emotion_accmag_model.json
├── feature_columns_5emotion.json
├── label_classes_5emotion.json
└── requirements.txt
```

The inference script can be supplied separately through the SageMaker deployment configuration.

The filenames and package structure must match the actual model artifacts and inference script used during deployment.

## 5. Deploying the Model to Amazon SageMaker

SageMaker hosts the trained model through an endpoint that accepts input features and returns predictions.

A simplified deployment configuration looks like this:

```python
from sagemaker.sklearn.model import SKLearnModel

model = SKLearnModel(
    model_data="s3://YOUR-BUCKET/YOUR-MODEL-ARCHIVE.tar.gz",
    role=role,
    entry_point="inference.py",
    source_dir="model_package_5emotion",
    framework_version="1.2-1",
    py_version="py3"
)
```

The S3 path, IAM execution role, framework version, and other settings must match the user's own AWS environment.

After deployment, the endpoint status can be checked through the SageMaker console or AWS SDK. An `InService` status indicates that the endpoint is ready to receive inference requests, but it does not by itself confirm prediction accuracy.

## 6. Invoking the Deployed Endpoint

The deployed model can be called from another AWS component, such as an AWS Lambda function, using the SageMaker Runtime API.

```python
response = runtime.invoke_endpoint(
    EndpointName="YOUR-ENDPOINT-NAME",
    ContentType="application/json",
    Accept="application/json",
    Body=json.dumps(features)
)

result = json.loads(
    response["Body"].read().decode("utf-8")
)
```

The endpoint returns the predicted emotion, confidence, and class probabilities. The calling function can then process the result and store the relevant information in DynamoDB.

The endpoint name, input features, and request format must match the deployed model's configuration.

## 7. Integration with the AWS Data Pipeline

SageMaker is one component of the EmoSI real-time processing pipeline. The main workflow is:

1. **EmotiBit and ESP32:** Collect physiological and movement signals.
2. **AWS IoT Core and Kinesis Data Streams:** Receive and transmit sensor records.
3. **AWS Lambda:** Process incoming data, prepare the required features, and invoke the SageMaker endpoint.
4. **Amazon SageMaker:** Generate the emotion prediction and probability distribution.
5. **Amazon DynamoDB:** Store the relevant sensor data and prediction results.
6. **Streamlit Dashboard:** Retrieve and display the available data and emotion predictions.

The following is an example of the type of information stored for a prediction:

```python
item = {
    "device_id": device_id,
    "timestamp": timestamp,
    "predicted_emotion": prediction["predicted_emotion"],
    "confidence": Decimal(str(prediction["confidence"]))
}
```

Additional fields, such as the probabilities for each emotion class, can be included according to the DynamoDB table design.

This is an illustrative excerpt rather than a complete Lambda handler. The actual implementation also needs to handle incoming records, feature preparation, data types, permissions, and errors.

## 8. Configuration and Security

The code snippets in this README are provided to explain the main implementation concepts. They may require modifications before they can run in another environment.

To reproduce the workflow, users need to configure their own:

- AWS account and region
- IAM roles and permissions
- S3 bucket and model artifacts
- SageMaker endpoint
- DynamoDB tables
- Required Python packages and compatible library versions

Actual credentials, private keys, and other sensitive configuration values should not be committed to a public repository. Use appropriate IAM roles and secure configuration methods instead.

## 9. Important Notes

The training, packaging, inference, and deployment snippets are examples of the main steps involved in the EmoSI machine learning pipeline. They are not intended to replace the original training notebook, deployed model artifacts, or complete AWS Lambda implementation.

The model's performance depends on the training data, feature extraction process, and deployment configuration. Predictions should be interpreted as experimental emotion classifications rather than clinically validated conclusions.

For the complete system workflow, refer to the relevant documentation in the [`docs/`](../docs/) directory.

---

# 1. Dataset Storage and Loading from AWS

The EmoSI project uses AWS services to support dataset storage, model development, and real-time processing. Amazon S3 and Amazon DynamoDB serve different purposes in the system.

- **Amazon S3:** Used to store dataset files, such as the WESAD dataset or processed training data, as well as trained model artifacts and deployment packages.
- **Amazon DynamoDB:** Used to store physiological sensor readings and emotion prediction results collected or generated by the system.

### Loading a dataset from Amazon S3

For model training, a dataset stored in Amazon S3 can be downloaded or accessed from a SageMaker notebook for preprocessing and training.

The following is a simplified example of downloading a dataset file from S3:

```python
import boto3

s3 = boto3.client("s3", region_name="ap-southeast-1")

s3.download_file(
    "YOUR-S3-BUCKET",
    "datasets/processed_features.csv",
    "processed_features.csv"
)
```

After downloading the file, it can be loaded for further processing:

```python
import pandas as pd

dataset = pd.read_csv("processed_features.csv")

print(dataset.head())
print("Dataset shape:", dataset.shape)
```

The bucket name, object key, and local filename are examples. Replace them with the actual locations of your dataset files.

### Retrieving data from Amazon DynamoDB

DynamoDB can also be accessed when sensor records or stored predictions are needed for analysis or dashboard integration.

For example, the following code retrieves records from a DynamoDB table:

```python
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-1"
)

table = dynamodb.Table("YOUR-TABLE-NAME")

response = table.scan()
items = response.get("Items", [])

print("Records retrieved:", len(items))
```

For tables containing many records, pagination is needed because a single `scan()` request may not return every item. A `scan()` also reads the table broadly, so queries using the appropriate keys or indexes may be more suitable for larger datasets.

Retrieved records can be converted into a DataFrame for further analysis, provided the records contain the required features and labels.

```python
import pandas as pd

dataset = pd.DataFrame(items)

print(dataset.head())
print("Dataset shape:", dataset.shape)
```

### Important distinction

The data stored in DynamoDB is not automatically ready for model training. Sensor records may require preprocessing, feature extraction, label preparation, and formatting before they can be used by the XGBoost model.

Similarly, loading a dataset from S3 does not automatically make it suitable for training. The data must match the expected feature structure and label format.

These snippets are only examples of how the services can be accessed. They do not necessarily represent the exact data-loading code used in the final implementation. The actual workflow depends on the dataset source and the training process.

**Security note:** Configure AWS access through an appropriate IAM role or secure credentials. Do not place access keys, secret keys, or private participant data in the source code or public repository.
