"""Tests for FastAPI app endpoints."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_all_activities_returns_success(self, client):
        """Verify GET /activities returns all activities."""
        # Arrange
        # (client fixture provides fresh test data)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_includes_participants(self, client):
        """Verify activities include correct participant lists."""
        # Arrange
        # (client fixture provides fresh test data)

        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert data["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
        assert data["Programming Class"]["participants"] == ["emma@mergington.edu"]
        assert data["Gym Class"]["participants"] == []


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success_adds_participant(self, client):
        """Verify successful signup adds participant to activity."""
        # Arrange
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Verify signup returns 404 for non-existent activity."""
        # Arrange
        activity_name = "Non-Existent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student_rejected(self, client):
        """Verify signup is rejected if student already registered."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"


class TestRemoveFromActivity:
    """Tests for POST /activities/{activity_name}/remove endpoint."""

    def test_remove_success_removes_participant(self, client):
        """Verify successful removal removes participant from activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # In Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_activity_not_found(self, client):
        """Verify remove returns 404 for non-existent activity."""
        # Arrange
        activity_name = "Non-Existent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_remove_participant_not_found(self, client):
        """Verify remove returns 404 if participant not in activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "notinclub@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/remove",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found in activity"
