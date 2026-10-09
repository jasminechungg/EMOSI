from aws_dynamodb import (
    create_session,
    get_active_session,
    end_session,
    get_all_sessions
)

session = create_session(
    clinician_id="clinician_jasmine",
    participant_id="participant_001",
    notes="Test monitoring session"
)

print("Created session:")
print(session)

active = get_active_session()

print("\nActive session:")
print(active)

if active:
    end_session(
        active["session_id"],
        dominant_emotion="happy",
        notes="Test session completed"
    )

    print("\nEnded session:")
    print(active["session_id"])

print("\nAll sessions:")
for item in get_all_sessions():
    print(item)