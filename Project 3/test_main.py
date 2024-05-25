from fastapi.testclient import TestClient
from ex3_3.ex3.main import app, get_db_connection
from datetime import datetime, timezone, timedelta
import pytest

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM events")
    db.commit()
    yield db
    db.close()


def test_process_event(test_db):
    response = client.post("/process_event/", json={"userid": "user123", "eventname": "Test Event"})
    assert response.status_code == 200
    assert response.json() == {"message": "Event processed successfully"}

    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM events")
    event_records = cursor.fetchall()
    assert len(event_records) == 1
    assert event_records[0][1] == "user123"
    assert event_records[0][2] == "Test Event"


def test_get_reports(test_db):
    cursor = test_db.cursor()
    eventtimestamputc = datetime.now(timezone.utc) - timedelta(seconds=100)
    cursor.execute('''
    INSERT INTO events (eventtimestamputc, userid, eventname) VALUES (?, ?, ?)
    ''', (eventtimestamputc, 'user123', 'Test Event'))
    test_db.commit()

    response = client.post("/get_reports/", params={"lastseconds": 200, "userid": "user123"})
    assert response.status_code == 200
    response_json = response.json()
    assert "events" in response_json
    assert len(response_json["events"]) == 1
    assert response_json["events"][0]["userid"] == "user123"
    assert response_json["events"][0]["eventname"] == "Test Event"

    response = client.post("/get_reports/", params={"lastseconds": 50, "userid": "user123"})
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["events"]) == 0
