import os
import pickle
import hashlib
import random
from datetime import datetime, timedelta

class User:
    def __init__(self, username, password):
        # User profile attributes
        self.username = username
        self.password_hash = self.hash_password(password)
        self.level = 1
        self.experience = 0
        self.physical_stats = {
            'strength': 1,
            'endurance': 1,
            'flexibility': 1
        }
        self.academic_stats = {
            'study_hours': 0,
            'homework_completed': 0
        }
        self.daily_quests = []
        self.monthly_challenge = None

    def hash_password(self, password):
        # Simple password hashing for basic security
        return hashlib.sha256(password.encode()).hexdigest()

    def save_profile(self, profiles_dir):
        # Save individual user profile to a binary file in specified directory
        filename = os.path.join(profiles_dir, f"{self.username}_profile.bin")
        with open(filename, 'wb') as f:
            pickle.dump({
                'level': self.level,
                'experience': self.experience,
                'physical_stats': self.physical_stats,
                'academic_stats': self.academic_stats,
                'monthly_challenge': self.monthly_challenge
            }, f)

    def load_profile(self, profiles_dir):
        # Load individual user profile from binary file in specified directory
        filename = os.path.join(profiles_dir, f"{self.username}_profile.bin")
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                profile_data = pickle.load(f)
                self.level = profile_data['level']
                self.experience = profile_data['experience']
                self.physical_stats = profile_data['physical_stats']
                self.academic_stats = profile_data['academic_stats']
                self.monthly_challenge = profile_data['monthly_challenge']

class QuestSystem:
    def __init__(self):
        # Create directories for storing user data
        self.base_dir = 'solo_leveling_data'
        self.profiles_dir = os.path.join(self.base_dir, 'user_profiles')
        self.users_file = os.path.join(self.base_dir, 'users.bin')

        # Create directories if they don't exist
        os.makedirs(self.profiles_dir, exist_ok=True)

        self.users = {}
        self.current_user = None
        self.load_users()

    def load_users(self):
        # Load existing users from binary file
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'rb') as f:
                    self.users = pickle.load(f)
            except (EOFError, pickle.UnpicklingError):
                # Handle potential file corruption
                self.users = {}

    def save_users(self):
        # Save users to binary file
        with open(self.users_file, 'wb') as f:
            pickle.dump(self.users, f)

    def register(self, username, password):
        # User registration
        if username in self.users:
            print("Username already exists!")
            return False
        
        new_user = User(username, password)
        new_user.save_profile(self.profiles_dir)  # Save initial profile
        self.users[username] = new_user
        self.save_users()
        print(f"User {username} registered successfully!")
        return True

    def login(self, username, password):
        # User login
        if username not in self.users:
            print("User not found!")
            return False
        
        user = self.users[username]
        if user.password_hash == user.hash_password(password):
            self.current_user = user
            self.current_user.load_profile(self.profiles_dir)  # Load user's saved profile
            print(f"Welcome, {username}!")
            return True
        else:
            print("Incorrect password!")
            return False

    def generate_daily_physical_quests(self):
        # Generate physical training quests based on user's current level
        level = self.current_user.physical_stats['strength']
        quests = [
            f"Do {5 * level} push-ups",
            f"Hold plank for {30 * level} seconds",
            f"Do {3 * level} pull-ups",
            f"Run {1 * level} kilometers"
        ]
        return quests

    def generate_daily_academic_quests(self):
        # Generate study and homework quests
        return [
            "Complete 2 hours of focused study",
            "Finish pending homework assignments",
            "Review notes from last week's classes",
            "Solve 10 practice problems"
        ]

    def start_monthly_challenge(self):
        # 30-day physical transformation challenge
        challenges = [
            "Develop visible bicep definition",
            "Increase overall muscle mass",
            "Improve core strength",
            "Enhance cardiovascular endurance"
        ]
        self.current_user.monthly_challenge = {
            'challenge': random.choice(challenges),
            'start_date': datetime.now(),
            'completed': False
        }
        self.current_user.save_profile(self.profiles_dir)  # Save profile after creating challenge

    def update_progress(self, quest_type, completed):
        # Update user progress and experience
        if completed:
            self.current_user.experience += 10
            if quest_type == 'physical':
                self.current_user.physical_stats['strength'] += 0.1
            elif quest_type == 'academic':
                self.current_user.academic_stats['study_hours'] += 1

            # Level up mechanism
            if self.current_user.experience >= 100:
                self.current_user.level += 1
                self.current_user.experience = 0

            # Save user's profile after updating progress
            self.current_user.save_profile(self.profiles_dir)

    def display_profile(self):
        # Show user's current profile and stats
        user = self.current_user
        print(f"\n--- {user.username}'s Profile ---")
        print(f"Level: {user.level}")
        print(f"Experience: {user.experience}/100")
        print("\nPhysical Stats:")
        for stat, value in user.physical_stats.items():
            print(f"{stat.capitalize()}: {value:.1f}")
        print("\nAcademic Stats:")
        for stat, value in user.academic_stats.items():
            print(f"{stat.replace('_', ' ').capitalize()}: {value}")

def main():
    quest_system = QuestSystem()

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            quest_system.register(username, password)
        
        elif choice == '2':
            username = input("Username: ")
            password = input("Password: ")
            if quest_system.login(username, password):
                # Main user interaction loop
                while True:
                    print("\n1. Daily Quests\n2. Monthly Challenge\n3. View Profile\n4. Logout")
                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        physical_quests = quest_system.generate_daily_physical_quests()
                        academic_quests = quest_system.generate_daily_academic_quests()
                        
                        print("\nPhysical Training Quests:")
                        for quest in physical_quests:
                            print(quest)
                            completed = input("Completed? (y/n): ").lower() == 'y'
                            quest_system.update_progress('physical', completed)

                        print("\nAcademic Quests:")
                        for quest in academic_quests:
                            print(quest)
                            completed = input("Completed? (y/n): ").lower() == 'y'
                            quest_system.update_progress('academic', completed)

                    elif user_choice == '2':
                        quest_system.start_monthly_challenge()
                        print(f"Monthly Challenge: {quest_system.current_user.monthly_challenge['challenge']}")

                    elif user_choice == '3':
                        quest_system.display_profile()

                    elif user_choice == '4':
                        break

        elif choice == '3':
            break

if __name__ == "__main__":
    main()
