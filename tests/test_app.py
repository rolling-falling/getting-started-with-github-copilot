"""
Tests for the FastAPI application endpoints
"""
import pytest


class TestRoot:
    """Tests for the root endpoint"""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_all(self, client, reset_db):
        """Test that get_activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Basketball Team" in data
        assert "Tennis Club" in data
        assert len(data) == 9

    def test_get_activities_contains_required_fields(self, client, reset_db):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_strings(self, client, reset_db):
        """Test that participants are strings (emails)"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_data in data.values():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, reset_db):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Signed up newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant(self, client, reset_db):
        """Test that signup actually adds the participant"""
        email = "newstudent@mergington.edu"
        
        # Signup
        response = client.post(f"/activities/Chess%20Club/signup?email={email}")
        assert response.status_code == 200
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client, reset_db):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_multiple_students(self, client, reset_db):
        """Test that multiple students can sign up for same activity"""
        # First signup
        response1 = client.post(
            "/activities/Chess%20Club/signup?email=student1@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Second signup
        response2 = client.post(
            "/activities/Chess%20Club/signup?email=student2@mergington.edu"
        )
        assert response2.status_code == 200
        
        # Verify both are enrolled
        activities = client.get("/activities").json()
        participants = activities["Chess Club"]["participants"]
        assert "student1@mergington.edu" in participants
        assert "student2@mergington.edu" in participants


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client, reset_db):
        """Test successful unregister from an activity"""
        email = "michael@mergington.edu"
        
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Removed" in data["message"]

    def test_unregister_removes_participant(self, client, reset_db):
        """Test that unregister actually removes the participant"""
        email = "michael@mergington.edu"
        
        # Verify participant exists before unregister
        activities_before = client.get("/activities").json()
        assert email in activities_before["Chess Club"]["participants"]
        
        # Unregister
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        # Verify participant was removed
        activities_after = client.get("/activities").json()
        assert email not in activities_after["Chess Club"]["participants"]

    def test_unregister_activity_not_found(self, client, reset_db):
        """Test unregister from non-existent activity returns 404"""
        response = client.delete(
            "/activities/NonExistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_participant_not_found(self, client, reset_db):
        """Test unregister for non-existent participant returns 404"""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=nonexistent@mergington.edu"
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"

    def test_unregister_multiple_times(self, client, reset_db):
        """Test that unregistering same participant twice fails appropriately"""
        email = "michael@mergington.edu"
        
        # First unregister succeeds
        response1 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response2.status_code == 404
