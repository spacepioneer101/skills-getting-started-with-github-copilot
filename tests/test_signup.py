"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests verify successful signups, error handling for duplicate signups,
and validation of invalid activities.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_signup_successful(self, client, existing_activity, sample_email):
        """
        Test successful signup for an activity.
        
        AAA Pattern:
        - Arrange: Prepare activity name and new student email
        - Act: Send POST request to signup endpoint
        - Assert: Verify successful response and student is added
        """
        # Arrange
        activity_name = existing_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]

    def test_signup_adds_student_to_participants(self, client, existing_activity, sample_email):
        """
        Test that signup actually adds the student to the activity's participants.
        
        AAA Pattern:
        - Arrange: Known activity and new email
        - Act: Sign up, then fetch activities
        - Assert: Verify student is in participants list
        """
        # Arrange
        activity_name = existing_activity
        email = sample_email

        # Act
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        activities_response = client.get("/activities")

        # Assert
        assert signup_response.status_code == 200
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_fails(self, client, existing_activity, existing_participant):
        """
        Test that signing up a student who is already signed up returns error.
        
        AAA Pattern:
        - Arrange: Activity and email of existing participant
        - Act: Attempt signup with duplicate email
        - Assert: Verify 400 error response
        """
        # Arrange
        activity_name = existing_activity
        email = existing_participant

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client, sample_email, nonexistent_activity):
        """
        Test that signing up for a nonexistent activity returns 404.
        
        AAA Pattern:
        - Arrange: Nonexistent activity name and email
        - Act: Attempt signup for activity that doesn't exist
        - Assert: Verify 404 error response
        """
        # Arrange
        activity_name = nonexistent_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_response_format(self, client, existing_activity, sample_email):
        """
        Test that signup returns a properly formatted message.
        
        AAA Pattern:
        - Arrange: Activity and email
        - Act: Sign up
        - Assert: Verify response has correct message format
        """
        # Arrange
        activity_name = existing_activity
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert f"Signed up {email}" in data["message"]
        assert activity_name in data["message"]
