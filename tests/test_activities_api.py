def test_get_activities_returns_seed_data(client):
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.get("/activities")
    activities = response.json()

    assert response.status_code == 200
    assert "Chess Club" in activities
    assert activities["Chess Club"]["participants"] == expected_participants


def test_signup_adds_new_participant(client):
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}",
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in client.get("/activities").json()[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}",
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    assert client.get("/activities").json()[activity_name]["participants"].count(existing_email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}",
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_rejects_missing_participant(client):
    activity_name = "Drama Club"
    missing_email = "not.registered@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={missing_email}",
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_rejects_unknown_activity(client):
    response = client.delete("/activities/Unknown%20Club/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}