"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "Academic",
        "tags": ["Strategy", "Competition", "Critical Thinking"],
        "difficulty_level": "Beginner"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "Technical",
        "tags": ["STEM", "Computer Science", "Beginner-Friendly"],
        "difficulty_level": "Beginner"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "Sports",
        "tags": ["Fitness", "Health", "Team Sports"],
        "difficulty_level": "All Levels"
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "category": "Sports",
        "tags": ["Team Sports", "Competition", "Outdoor"],
        "difficulty_level": "Intermediate"
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "category": "Sports",
        "tags": ["Team Sports", "Competition", "Indoor"],
        "difficulty_level": "Intermediate"
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "category": "Arts",
        "tags": ["Creative", "Visual Arts", "Relaxing"],
        "difficulty_level": "All Levels"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "category": "Arts",
        "tags": ["Performing Arts", "Public Speaking", "Creative"],
        "difficulty_level": "Beginner"
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "category": "Academic",
        "tags": ["STEM", "Problem Solving", "Competition"],
        "difficulty_level": "Advanced"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "category": "Academic",
        "tags": ["Public Speaking", "Critical Thinking", "Communication"],
        "difficulty_level": "Intermediate"
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/categories")
def get_categories():
    """Get all unique categories and their activity counts"""
    categories = {}
    for activity_name, activity in activities.items():
        category = activity.get("category", "Uncategorized")
        if category not in categories:
            categories[category] = {"count": 0, "activities": []}
        categories[category]["count"] += 1
        categories[category]["activities"].append(activity_name)
    return categories


@app.get("/activities")
def get_activities(category: str = None, tag: str = None, difficulty: str = None):
    """Get activities with optional filtering by category, tag, or difficulty"""
    filtered_activities = activities.copy()
    
    # Filter by category
    if category:
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if activity.get("category", "").lower() == category.lower()
        }
    
    # Filter by tag
    if tag:
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if tag.lower() in [t.lower() for t in activity.get("tags", [])]
        }
    
    # Filter by difficulty
    if difficulty:
        filtered_activities = {
            name: activity for name, activity in filtered_activities.items()
            if activity.get("difficulty_level", "").lower() == difficulty.lower()
        }
    
    return filtered_activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
