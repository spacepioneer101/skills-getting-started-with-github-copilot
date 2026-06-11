"""
Pytest configuration and shared fixtures for FastAPI tests.

This module provides:
- TestClient fixture for testing the FastAPI application
- Sample test data for consistent test setup
- Fixture to reset app state before each test to ensure test isolation
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture: Automatically reset activities to initial state before each test.
    
    This ensures test isolation by restoring the in-memory activity database
    to its original state before each test runs.
    """
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer team practicing and playing matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Basketball practices and inter-school games",
            "schedule": "Mondays, Wednesdays, 4:30 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["nina@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lily@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater workshops and school play productions",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["sam@mergington.edu"]
        },
        "Math Club": {
            "description": "Problem-solving, competitions, and math enrichment",
            "schedule": "Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["isabel@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate practice and tournaments",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu"]
        }
    }
    
    # Reset activities to original state before test
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (reset again to ensure clean state)
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client():
    """
    Fixture: TestClient for the FastAPI application.
    
    Provides an HTTP client to make requests to the app during tests.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture: A sample student email for testing signup/unregister operations."""
    return "test_student@mergington.edu"


@pytest.fixture
def existing_activity():
    """Fixture: Name of an activity that exists in the app's data."""
    return "Chess Club"


@pytest.fixture
def nonexistent_activity():
    """Fixture: Name of an activity that does not exist in the app's data."""
    return "Nonexistent Club"


@pytest.fixture
def existing_participant():
    """Fixture: Email of a student already signed up for Chess Club."""
    return "michael@mergington.edu"
