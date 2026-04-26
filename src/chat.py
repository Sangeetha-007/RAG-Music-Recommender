import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from main import PROFILES
from agent import select_profile, get_recommendations, format_response

SONGS_PATH = os.path.join(os.path.dirname(__file__), "../data/songs.csv")


def run():
    print("Music Recommender — type 'quit' to exit\n")
    while True:
        user_message = input("How are you feeling? ").strip()
        if user_message.lower() == "quit":
            break

        print("\nFinding your profile...")
        profile_name = select_profile(user_message, PROFILES)

        if profile_name not in PROFILES:
            print(f"Could not match a profile. Got: '{profile_name}'\n")
            continue

        print(f"Matched profile: {profile_name}")
        print("Fetching recommendations...\n")
        _, results = get_recommendations(profile_name, PROFILES, SONGS_PATH)

        response = format_response(user_message, profile_name, results)
        print(f"\n{response}\n")


if __name__ == "__main__":
    run()
