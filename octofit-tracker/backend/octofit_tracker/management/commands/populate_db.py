from django.core.management.base import BaseCommand
from django.conf import settings

import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "Team DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "Team DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "Team DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Team Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Team Marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "Team Marvel"},
        ]
        teams = [
            {"name": "Team DC", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
            {"name": "Team Marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
        ]
        activities = [
            {"user_email": "superman@dc.com", "activity": "Flight", "duration": 60},
            {"user_email": "ironman@marvel.com", "activity": "Suit Training", "duration": 45},
        ]
        leaderboard = [
            {"team": "Team DC", "points": 300},
            {"team": "Team Marvel", "points": 350},
        ]
        workouts = [
            {"name": "Strength Training", "description": "General superhero strength workout"},
            {"name": "Agility Drills", "description": "Improve speed and agility"},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
