from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient
from django.db import connections
from django.apps import apps

# Sample superhero data
USERS = [
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
    {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "marvel"},
    {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
    {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
]
TEAMS = [
    {"name": "marvel", "members": ["Iron Man", "Captain America", "Spider-Man"]},
    {"name": "dc", "members": ["Superman", "Batman", "Wonder Woman"]},
]
ACTIVITIES = [
    {"user": "Iron Man", "activity": "Flight", "duration": 60},
    {"user": "Batman", "activity": "Martial Arts", "duration": 45},
]
LEADERBOARD = [
    {"team": "marvel", "points": 300},
    {"team": "dc", "points": 250},
]
WORKOUTS = [
    {"user": "Spider-Man", "workout": "Web Swinging", "reps": 100},
    {"user": "Wonder Woman", "workout": "Lasso Training", "reps": 80},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        for col in ['users', 'teams', 'activities', 'leaderboard', 'workouts']:
            db[col].drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
