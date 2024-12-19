import json
import csv
import requests
from collections import Counter

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

# Get the unique team numbers names
filtered_team_members = [row["Name"] for row in data if row["Name"].isascii()]
unique_team_members = list(set(filtered_team_members))

# Get the person who took the most stats
highest_stats_taken_name = Counter(filtered_team_members).most_common(1)[0][0]
highest_stats_taken = Counter(filtered_team_members).most_common(1)[0][1]

excluded_names = [
    "Null",
    "CO",
    "N/A 0",
    "AW",
    "AN",
    "XB",
    "HS",
    "MC",
    "BK",
    "AM",
    "PS",
    "Calc"
]

final_team_members = [name for name in unique_team_members if name.strip() not in excluded_names]

# Generate the wrapped message
wrapped_message = f"Hey {', '.join(final_team_members)},\n\n"

wrapped_message += "Welcome to SuperSTATS Wrapped! Great year with Crescendo! 🎉\n\n"

wrapped_message += f"A total of {rounds_recorded} rounds were recorded this year, that's a lot of rounds! 🤯\n\n"

wrapped_message += "3255 is my favorite team by the way! 😏 "

wrapped_message += f"Speaking of 3255, {most_stats_on_3255} took the lead and recorded {highest_stats_on_3255} stats on 3255 this year! 🥇\n\n"

wrapped_message += f"But you know what's even more impressive? {highest_stats_taken_name} took {highest_stats_taken} stats this year! Thats a lot of stats! 🤯 "
wrapped_message += f"{highest_stats_taken_name}, thats alot of stats! 🎉\n\n"

print(wrapped_message)