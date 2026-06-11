"""
Tests for the GET /activities endpoint.

Tests verify that the endpoint correctly returns all available activities
and their details (description, schedule, max participants, current participants).
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities.
        
        AAA Pattern:
        - Arrange: Use the test client
        - Act: Make GET request to /activities
        - Assert: Verify status code and response contains expected activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Team",
            "Art Club",
            "Drama Club",
            "Math Club",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == len(expected_activities)
        for activity in expected_activities:
            assert activity in activities

    def test_get_activities_returns_activity_structure(self, client, existing_activity):
        """
        Test that each activity has the required fields.
        
        AAA Pattern:
        - Arrange: Known activity name
        - Act: Get all activities
        - Assert: Verify activity structure includes description, schedule, max_participants, participants
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        activity = activities[existing_activity]
        for field in required_fields:
            assert field in activity
            assert isinstance(activity[field], (str, int, list))

    def test_get_activities_participants_is_list(self, client, existing_activity):
        """
        Test that participants field is a list of emails.
        
        AAA Pattern:
        - Arrange: Known activity name
        - Act: Get activities
        - Assert: Verify participants is a list with valid emails
        """
        # Arrange
        activity_name = existing_activity

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        participants = activities[activity_name]["participants"]
        assert isinstance(participants, list)
        assert len(participants) > 0
        for email in participants:
            assert "@" in email and ".edu" in email
