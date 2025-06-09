import pickle
import datetime
import os
import sys

class Player():
    last_logged_in = datetime.datetime.now().date()
    def __init__(self):
        self.profile = {}
        self.Profile, self.last_logged_in = self.loadProfile()
        self.year, self.month, self.day = self.last_logged_in.year, self.last_logged_in.month, self.last_logged_in.day

    def register(self):
        print("\nRegister yourself.\n")
        name = input("Enter name: ")
        age = input("Enter age: ")
        weight = input("Enter weight in kg: ")
        species = input("Enter species: ")
        level = 0
        self.Profile = {"name": name, "age": age, "weight": weight, "species": species, "level": level}
        self.saveProfile()
        register_date = datetime.datetime.now().date()
        os.system("cls")
        print("\nSuccessfully registered!\n(0 to go back to main menu)")
        choice = input()
        if choice == "0":
            os.system("cls")
            self.main_menu()
    
    def saveProfile(self):
        with open('profile.bin', mode='wb') as file:
            pickle.dump(self.Profile, file)
    
    def loadProfile(self):
        try:
            with open('profile.bin', mode='rb') as file:
                Profile = pickle.load(file)
            return Profile, self.last_logged_in
        except FileNotFoundError:
            print("No profile found.")
            self.register()
        except EOFError:
            print("Profile data not found.")
            self.register()
    
    def viewProfile(self):
        Name = self.Profile['name']
        Age = self.Profile['age']
        Weight = self.Profile['weight']
        Species = self.Profile['species']
        Level = self.Profile['level']
        return Name, Age, Weight, Species, Level
    
    def count_days(self):
        days = (datetime.datetime.now().date() - self.last_logged_in).days
        return days
    
    def daily_missions(self):
        days = self.count_days()
        if days > 0:
            print(f"You have logged in for {days} days.")
            print(f"Daily Missions:")
            print(f"[1] Jumping Jacks: {30*days} seconds.")
            print(f"[2] Bhujangasana: {30*days} seconds.")
            print(f"[3] Push-ups: {6*days} reps.")
            print(f"[4] Sit-ups: {10*days} reps.")
        else:
            print("Daily Missions:")
            print(f"[1] Jumping Jacks: 15 seconds.")
            print(f"[2] Bhujangasana: 15 seconds.")
            print(f"[3] Push-ups: 3 reps.")
            print(f"[4] Sit-ups: 5 reps.")
        complete = input("Have you completed the tasks(Y/N): ")
        if complete.lower() == "y":
            print("\nYou have completed the daily missions. Level will be increased.")
            self.Profile['level'] += 1
            self.saveProfile()
            print("(0 to go back to main menu)\n")
            choice = input()
            if choice == "0":
                os.system("cls")
                self.main_menu()
        else:
            if self.Profile['level'] > 0:
                print("\nYou have not completed the daily missions. Level will be reduced.")
                self.Profile['level'] -= 1
                self.saveProfile()
            else:
                print("\nYou have not completed the daily missions. Level will not be changed.")
            print("(0 to go back to main menu)\n ")
            choice = input()
            if choice == "0":
                os.system("cls")
                self.main_menu()

    def main_menu(self):
        while True:
            print("\n-------Menu----------\n")
            print("[1] View Profile")
            print("[2] Daily Missions")
            print("[0] Exit")
            choice = int(input("Enter choice: "))
            if choice == 1:
                os.system("cls")
                Name, Age, Weight, Species, Level = self.viewProfile()
                print(f"[Name] {Name}")
                print(f"[Age] {Age}")
                print(f"[Weight: {Weight}")
                print(f"[Species: {Species}")
                print(f"[Level: {Level}")
                choice = int(input(("\n0 to go back to main menu: ")))
                if choice == 0:
                    os.system("cls")
                    self.main_menu()
            elif choice == 2:
                os.system("cls")
                self.daily_missions()
            elif choice == 0:
                print("\nExiting...\n")
                sys.exit()
            else:
                os.system("cls")
                self.main_menu()


#main
print("\n\n***********************************************************\n")
print("Thank you for using this program!")
print("Credits: Poseidon4767 for the entire code.")
print("GitHub Profile: https://github.com/Poseidon4767")
print("Discord: poseidon4767 (any issues report to me :D)")
print("\n***********************************************************\n")
player = Player()
player.main_menu()