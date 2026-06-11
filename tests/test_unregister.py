"""
Tests for the DELETE /activities/{activity_name}/participants endpoint.

Tests verify successful unregistration, error handling for non-existent
students and activities, and participant removal from activity.
"""

import pytest


class TestUnregisterParticipant:
    """Test suite for unregistering a student from an activity."""

    def test_unregister_successful(self, client, existing_activity, existing_participant):
        """
        Test successful unregistration from an activity.
        
        AAA Pattern:
        - Arrange: Activity and existing participant email
        - Act: Send DELETE request to unregister endpoint
        - Assert: Verify successful response and removal
        """
        # Arrange
        activity_name = existing_activity
        email = existing_participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_unregister_removes_student_from_participants(self, client, existing_activity, existing_participant):
        """
        Test that unregister actually removes the student from participants.
        
        AAA Pattern:
        - Arrange: Activity and existing participant
        - Act: Unregister student, then fetch activities
        - Assert: Verify student is no longer in participants
        """
        # Arrange
        activity_name = existing_activity
        email = existing_participant

        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        activities_response = client.get("/activities")

        # Assert
        assert unregister_response.status_code == 200
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_nonexistent_student_fails(self, client, existing_activity, sample_email):
        """
        Test that unregistering a student not signed up returns error.
        
        AAA Pattern:
        - Arrange: Activity and email of student not in participants
        - Act: Attempt to unregister student who isn't signed up
        - Assert: Verify 400 error response
        """
        # Arrange
        activity_name = existing_activity
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_nonexistent_activity_fails(self, client, sample_email, nonexistent_activity):
        """
        Test that unregistering from nonexistent activity returns 404.
        
        AAA Pattern:
        - Arrange: Nonexistent activity name and email
        - Act: Attempt to unregister from activity that doesn't exist
        - Assert: Verify 404 error response
        """
        # Arrange
        activity_name = nonexistent_activity
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_unregister_response_format(self, client, existing_activity, existing_participant):
        """
        Test that unregister returns a properly formatted message.
        
        AAA Pattern:
        - Arrange: Activity and existing participant
        - Act: Unregister student
        - Assert: Verify response has correct message format
        """
        # Arrange
        activity_name = existing_activity
        email = existing_participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert f"Unregistered {email}" in data["message"]
        assert activity_name in data["message"]

    def test_unregister_same_student_twice_fails(self, client, existing_activity, existing_participant):
        """
        Test that unregistering a student twice (after removal) fails.
        
        AAA Pattern:
        - Arrange: Activity and existing participant
        - Act: Unregister once (succeeds), unregister again (should fail)
        - Assert: Verify second unregister returns 400
        """
        # Arrange
        activity_name = existing_activity
        email = existing_participant

        # Act - First unregister
        first_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        # Second unregister
        second_response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert "not signed up" in second_response.json()["detail"]
