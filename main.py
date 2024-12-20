import json
import csv
import requests
from collections import Counter

# Load secrets from the JSON file
secrets = json.load(open("secrets.json"))

def download_sheets_raw(gid):
    """
    Downloads a Google Sheets document as a list of dictionaries.

    Args:
        gid (str): The ID of the Google Sheets document.

    Returns:
        list: The downloaded Google Sheets document as a list of dictionaries.
    """
    url = f"https://docs.google.com/spreadsheets/d/{secrets['GSHEET_DOC_ID']}/edit#gid={gid}"
    doc_id, sheet_id = url.split("/")[5:7]
    sheet_id = sheet_id.split("gid=")[1]
    sheet_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={sheet_id}"
    
    response = requests.get(sheet_url)
    response.raise_for_status()
    
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)
    
    data = [row for row in reader]
    return data

data = download_sheets_raw(secrets["GID_RAW"])

# Count the amount of rounds recorded
rounds_recorded = len(data)

# Count the amount of stats recorded on 3255
stats_on_3255 = [row["Name"] for row in data if row["Team"] == "3255"]
most_stats_on_3255 = Counter(stats_on_3255).most_common(1)[0][0]
highest_stats_on_3255 = Counter(stats_on_3255).most_common(1)[0][1]

# Get the unique team members' names
excluded_names = [
    "Null", "CO", "N/A 0", "AW", "AN", "XB", "HS", "MC", "BK", "AM", "PS", "Calc"
]

filtered_team_members = [row["Name"] for row in data if row["Name"].isascii()]
filtered_team_members = [name for name in filtered_team_members if name.strip() not in excluded_names]
unique_team_members = list(set(filtered_team_members))

final_team_members = [f"@{name}" for name in unique_team_members]

# Get the person who took the most stats
highest_stats_taken_name = Counter(filtered_team_members).most_common(1)[0][0]
highest_stats_taken = Counter(filtered_team_members).most_common(1)[0][1]
highest_stats_taken_name = f"@{highest_stats_taken_name}"

# See what color was documented more
most_documented_color = Counter([row["Team Color"] for row in data]).most_common(1)[0][0]
most_documented_color = "Red" if most_documented_color == "R" else "Blue"

# Get the most stats taken on amp
amp_stats = Counter([row["TELE_AMP_INT_1"] for row in data]).most_common(1)[0][1]
amp_stats_name = Counter([row["Name"] for row in data if row["TELE_AMP_INT_1"] == "1"]).most_common(1)[0][0]
amp_stats_name = f"@{amp_stats_name}"

# Get the most stats taken on speaker
speaker_stats = Counter([row["TELE_SPEAKER_INT_2"] for row in data]).most_common(1)[0][1]
speaker_stats_name = Counter([row["Name"] for row in data if row["TELE_SPEAKER_INT_2"] == "1"]).most_common(1)[0][0]
speaker_stats_name = f"@{speaker_stats_name}"

# Get the most defense points
defense_stats = Counter([row["INFO_DEFENSE_INT_1"] for row in data]).most_common(1)[0][1]
defense_stats_team = Counter([row["Team"] for row in data if row["INFO_DEFENSE_INT_1"] == "1"]).most_common(1)[0][0]

# Get the most shuffles made in a match
shuffles_stats = Counter([row["TELE_SHUFFLE_INT_1"] for row in data]).most_common(1)[0][1]
shuffle_stats_name = Counter([row["Name"] for row in data if row["TELE_SHUFFLE_INT_1"] == "1"]).most_common(1)[0][0]
shuffle_stats_name = f"@{shuffle_stats_name}"

# Generate a leaderboard for most stats taken
leaderboard_counter = Counter(name for name in filtered_team_members if name)
leaderboard = "\n".join([f"{i+1}. @{name}: {count} rounds recorded." for i, (name, count) in enumerate(leaderboard_counter.most_common())])

# Generate the wrapped message
wrapped_message = f"Hey{', '.join(final_team_members)}. You where part of this years SuperSTATS Wrapped! 🎉\n\n"
wrapped_message += "Welcome to SuperSTATS Wrapped! Great year with Crescendo! 🎉\n\n"
wrapped_message += f"A total of {rounds_recorded} rounds were recorded this year, that's a lot of rounds! 🤯\n\n"
wrapped_message += "3255 is my favorite team by the way! 😏 "
wrapped_message += f"Speaking of 3255, {most_stats_on_3255} took the lead and recorded {highest_stats_on_3255} rounds on 3255 this year! 🥇\n\n"
wrapped_message += f"But you know what's even more impressive? {highest_stats_taken_name} recorded the most rounds this year with {highest_stats_taken} rounds recorded! 🤯 "
wrapped_message += f"{highest_stats_taken_name}, that's a lot of stats! 🎉\n\n"
wrapped_message += "Did you know that if we laid out all of the wires used in the robots this year, it would probably go really far? 🔌📏\n\n"
wrapped_message += f"{most_documented_color} was the most documented color this year! 🌈 How did that happen? 👀\n\n"
wrapped_message += "Okay, time for rapid fire! 🚀\n\n"
wrapped_message += f"Most stats taken on amp was {amp_stats_name} with {amp_stats} recorded this year. 🤔\n"
wrapped_message += f"Most stats taken on speaker was {speaker_stats} taken by {speaker_stats_name} 🤔\n"
wrapped_message += f"The person who recorded the most shuffles was {shuffle_stats_name} with {shuffles_stats} recorded. 🤔\n"
wrapped_message += f"The team with the most defense points was {defense_stats_team} with an ending score of {defense_stats}. 🤔\n\n"
wrapped_message += f"Its not a challenge, but there is a leaderboard: 👀\n{leaderboard}\n\n"
wrapped_message += "Water games confirmed? https://youtu.be/zaYAjoagqTk?si=D_f9AAoUCgC23jDF 🌊\n\n"

# Closing Messages
wrapped_message += "Here's to a great year of SuperSTATS! 🎉\n\n"
wrapped_message += "GitHub Code for my fellow software nerds: https://github.com/S0L0GUY/SuperSTATS-WRAPPED 💻\n"
wrapped_message += "This program was made in like 2 days so please don't judge me too hard if the stats are wrong. 😅\n\n"
wrapped_message += "Shoutout to @Tej! 🎉 He should get a raise. 💰\n"
wrapped_message += "Made by @Evan Grinnell ❤️\n"
wrapped_message += "P.S, you should definitely follow me on GitHub or I will cry. 😭"

print(wrapped_message)