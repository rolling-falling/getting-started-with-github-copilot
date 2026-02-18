"""
Pytest configuration and fixtures for FastAPI tests
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Provide a TestClient for testing the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_db():
    """Reset the activities database to initial state before each test"""
    from app import activities as app_activities
    
    # Save original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join our competitive basketball team and participate in games and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["sarah@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
        },
        "Theater Club": {
            "description": "Perform in school plays and develop acting skills",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ashley@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debate",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
            "participants": ["david@mergington.edu", "isabella@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore advanced scientific concepts",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu"]
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
        }
    }
    
    # Reset before test
    app_activities.clear()
    app_activities.update({k: {**v, "participants": v["participants"].copy()} for k, v in original_activities.items()})
    
    yield
    
    # Reset after test
    app_activities.clear()
    app_activities.update({k: {**v, "participants": v["participants"].copy()} for k, v in original_activities.items()})
