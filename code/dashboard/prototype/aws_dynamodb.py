import uuid
import hashlib
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key, Attr

REGION = "ap-southeast-1"
DEVICE_ID = "emotibit01"

dynamodb = boto3.resource("dynamodb", region_name=REGION)

raw_table = dynamodb.Table("EmotiBitSensorReadings")
prediction_table = dynamodb.Table("EmotionPredictions")
session_table = dynamodb.Table("Sessions")
user_table = dynamodb.Table("Users")
patient_table = dynamodb.Table("Patients")
summary_table = dynamodb.Table("SessionSummaries")
appointment_table = dynamodb.Table("Appointments")
observation_table = dynamodb.Table("SessionObservations")


def now_iso():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------------------
# Live Sensor / Prediction
# ---------------------------
def get_latest_sensor_readings(limit=30):
    response = raw_table.query(
        KeyConditionExpression=Key("device_id").eq(DEVICE_ID),
        ScanIndexForward=False,
        Limit=limit
    )
    return response.get("Items", [])


def get_latest_prediction():
    response = prediction_table.query(
        KeyConditionExpression=Key("device_id").eq(DEVICE_ID),
        ScanIndexForward=False,
        Limit=1
    )
    items = response.get("Items", [])
    return items[0] if items else None


def get_sensor_readings_between(device_id, start_time, end_time):
    response = raw_table.query(
        KeyConditionExpression=(
            Key("device_id").eq(device_id) &
            Key("timestamp").between(start_time, end_time)
        )
    )
    return response.get("Items", [])


def get_predictions_between(device_id, start_time, end_time):
    response = prediction_table.query(
        KeyConditionExpression=(
            Key("device_id").eq(device_id) &
            Key("timestamp").between(start_time, end_time)
        )
    )
    return response.get("Items", [])


# ---------------------------
# User Registration / Login
# ---------------------------
def register_user(full_name, email, password, role="clinician"):
    user_id = "user_" + str(uuid.uuid4())[:8]

    existing = user_table.scan(
        FilterExpression=Attr("email").eq(email)
    ).get("Items", [])

    if existing:
        return None, "Email already registered"

    item = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "password_hash": hash_password(password),
        "role": role,
        "account_status": "active",
        "created_at": now_iso()
    }

    user_table.put_item(Item=item)
    return item, "User registered successfully"


def login_user(email, password):
    response = user_table.scan(
        FilterExpression=Attr("email").eq(email)
    )

    users = response.get("Items", [])

    if not users:
        return None, "Email not found"

    user = users[0]

    if user.get("password_hash") != hash_password(password):
        return None, "Invalid password"

    if user.get("account_status") != "active":
        return None, "Account is not active"

    return user, "Login successful"


def get_all_users():
    response = user_table.scan()
    return response.get("Items", [])


# ---------------------------
# Patient Management
# ---------------------------
def create_patient(full_name, age="", gender="", guardian_name="", clinician_id="", notes=""):
    patient_id = "patient_" + str(uuid.uuid4())[:8]

    item = {
        "patient_id": patient_id,
        "full_name": full_name,
        "age": str(age),
        "gender": gender,
        "guardian_name": guardian_name,
        "clinician_id": clinician_id,
        "notes": notes,
        "created_at": now_iso()
    }

    patient_table.put_item(Item=item)
    return item


def get_patients(clinician_id=None):
    if clinician_id:
        response = patient_table.scan(
            FilterExpression=Attr("clinician_id").eq(clinician_id)
        )
    else:
        response = patient_table.scan()

    return response.get("Items", [])


def get_patient_by_id(patient_id):
    response = patient_table.get_item(
        Key={"patient_id": patient_id}
    )
    return response.get("Item")


# ---------------------------
# Session Management
# ---------------------------
def create_session(clinician_id="", patient_id="", participant_id="", notes=""):
    session_id = "session_" + str(uuid.uuid4())[:8]

    item = {
        "session_id": session_id,
        "device_id": DEVICE_ID,
        "clinician_id": clinician_id,
        "patient_id": patient_id,
        "participant_id": participant_id,
        "start_time": now_iso(),
        "end_time": "",
        "session_status": "active",
        "dominant_emotion": "",
        "notes": notes
    }

    session_table.put_item(Item=item)
    return item


def get_active_session():
    response = session_table.scan(
        FilterExpression=Attr("session_status").eq("active")
    )
    items = response.get("Items", [])
    return items[0] if items else None


def end_session(session_id, dominant_emotion="", notes=""):
    session_table.update_item(
        Key={"session_id": session_id},
        UpdateExpression="""
            SET session_status = :status,
                end_time = :end_time,
                dominant_emotion = :dominant_emotion,
                notes = :notes
        """,
        ExpressionAttributeValues={
            ":status": "completed",
            ":end_time": now_iso(),
            ":dominant_emotion": dominant_emotion,
            ":notes": notes
        }
    )


def get_all_sessions():
    response = session_table.scan()
    return response.get("Items", [])


def get_sessions_by_patient(patient_id):
    response = session_table.scan(
        FilterExpression=Attr("patient_id").eq(patient_id)
    )
    return response.get("Items", [])


def get_sessions_by_clinician(clinician_id):
    response = session_table.scan(
        FilterExpression=Attr("clinician_id").eq(clinician_id)
    )
    return response.get("Items", [])


def get_session_by_id(session_id):
    response = session_table.get_item(
        Key={"session_id": session_id}
    )
    return response.get("Item")


# ---------------------------
# Session Summaries
# ---------------------------
def save_session_summary(summary):
    summary_table.put_item(Item=summary)


def get_session_summary(session_id):
    response = summary_table.get_item(
        Key={"session_id": session_id}
    )
    return response.get("Item")


def get_all_session_summaries():
    response = summary_table.scan()
    return response.get("Items", [])


# ---------------------------
# Appointment Scheduling
# ---------------------------
def create_appointment(
    patient_id,
    clinician_id,
    appointment_date,
    appointment_time,
    appointment_reason
):
    appointment_id = "appt_" + str(uuid.uuid4())[:8]

    item = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "clinician_id": clinician_id,
        "appointment_date": str(appointment_date),
        "appointment_time": str(appointment_time),
        "appointment_reason": appointment_reason,
        "appointment_status": "Scheduled",
        "created_at": now_iso(),
        "session_id": ""
    }

    appointment_table.put_item(Item=item)
    return item


def get_appointments_by_clinician(clinician_id):
    response = appointment_table.scan(
        FilterExpression=Attr("clinician_id").eq(clinician_id)
    )
    return response.get("Items", [])


def get_appointment_by_id(appointment_id):
    response = appointment_table.get_item(
        Key={"appointment_id": appointment_id}
    )
    return response.get("Item")


def update_appointment_status(appointment_id, status, session_id=""):
    appointment_table.update_item(
        Key={"appointment_id": appointment_id},
        UpdateExpression="""
            SET appointment_status = :status,
                session_id = :session_id
        """,
        ExpressionAttributeValues={
            ":status": status,
            ":session_id": session_id
        }
    )

    # ---------------------------
# Session Observations
# ---------------------------
def add_session_observation(session_id, clinician_id, observation_text):
    item = {
        "session_id": session_id,
        "timestamp": now_iso(),
        "clinician_id": clinician_id,
        "observation_text": observation_text
    }

    observation_table.put_item(Item=item)
    return item


def get_session_observations(session_id):
    response = observation_table.query(
        KeyConditionExpression=Key("session_id").eq(session_id),
        ScanIndexForward=True
    )

    return response.get("Items", [])

def get_appointment_by_session_id(session_id):
    response = appointment_table.scan(
        FilterExpression=Attr("session_id").eq(session_id)
    )
    items = response.get("Items", [])
    return items[0] if items else None

def update_user_status(user_id, account_status):
    user_table.update_item(
        Key={"user_id": user_id},
        UpdateExpression="SET account_status = :status",
        ExpressionAttributeValues={
            ":status": account_status
        }
    )