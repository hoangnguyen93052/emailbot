import os
import json
from datetime import datetime

class Contributor:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.contributions = []

    def add_contribution(self, repo_name, date, contribution_type, description):
        self.contributions.append({
            "repo_name": repo_name,
            "date": date,
            "type": contribution_type,
            "description": description
        })

    def get_contributions(self):
        return self.contributions

    def __repr__(self):
        return f"Contributor({self.name}, {self.email})"

class ContributorTracker:
    def __init__(self):
        self.contributors = []

    def add_contributor(self, name, email):
        contributor = Contributor(name, email)
        self.contributors.append(contributor)

    def find_contributor(self, email):
        for contributor in self.contributors:
            if contributor.email == email:
                return contributor
        return None

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            json.dump([contributor.__dict__ for contributor in self.contributors], file)

    def load_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                contributors_data = json.load(file)
                for contributor_data in contributors_data:
                    contributor = Contributor(contributor_data['name'], contributor_data['email'])
                    contributor.contributions = contributor_data['contributions']
                    self.contributors.append(contributor)

    def display_contributors(self):
        for contributor in self.contributors:
            print(f"Name: {contributor.name}, Email: {contributor.email}")
            for contribution in contributor.get_contributions():
                print(f"\tRepo: {contribution['repo_name']}, Date: {contribution['date']}, Type: {contribution['type']}, Description: {contribution['description']}")

def main():
    tracker = ContributorTracker()
    tracker.load_from_file('contributors.json')

    while True:
        print("\nOpen Source Contributor Tracker")
        print("1. Add Contributor")
        print("2. Add Contribution")
        print("3. Display Contributors")
        print("4. Save and Exit")
        print("5. Exit without Saving")
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            name = input("Enter contributor name: ")
            email = input("Enter contributor email: ")
            tracker.add_contributor(name, email)
            print(f"Contributor {name} added.")
        elif choice == '2':
            email = input("Enter contributor email: ")
            contributor = tracker.find_contributor(email)
            if contributor:
                repo_name = input("Enter repository name: ")
                date = datetime.now().strftime("%Y-%m-%d")
                contribution_type = input("Enter contribution type (e.g., 'code', 'documentation'): ")
                description = input("Enter description of contribution: ")
                contributor.add_contribution(repo_name, date, contribution_type, description)
                print("Contribution added.")
            else:
                print("Contributor not found.")
        elif choice == '3':
            tracker.display_contributors()
        elif choice == '4':
            tracker.save_to_file('contributors.json')
            print("Data saved. Exiting...")
            break
        elif choice == '5':
            print("Exiting without saving...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()