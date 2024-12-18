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

# Extract team member names and remove non-ASCII characters
team_members = [entry['Name'].encode('ascii', 'ignore').decode('ascii') for entry in data]
unique_team_members = set(team_members)

# Count stats taken by each member
stats_count = Counter(team_members)

# Count stats taken on team 3255
stats_on_3255 = [entry for entry in data if entry['Team'] == '3255']
stats_on_3255_count = Counter([entry['Name'] for entry in stats_on_3255])

# Count stats taken on AMP and SPEAKER
amp_stats = [entry for entry in data if entry['AUTO_AMP_INT_2'] or entry['TELE_AMP_INT_1']]
speaker_stats = [entry for entry in data if entry['AUTO_SPEAKER_INT_5'] or entry['TELE_SPEAKER_INT_2']]
amp_stats_count = Counter([entry['Name'] for entry in amp_stats])
speaker_stats_count = Counter([entry['Name'] for entry in speaker_stats])

# Generate the wrapped message
filtered_team_members = [name for name in unique_team_members if 'â' not in name]
wrapped_message = f"Hey {', '.join(filtered_team_members)},\n\n"
wrapped_message += "You ready for this year's wrapped?\n\n"
wrapped_message += "Here are some fun stats from the year:\n\n"
wrapped_message += f"🏆 Most stats taken: {stats_count.most_common(1)[0][0]} with {stats_count.most_common(1)[0][1]} stats\n"
wrapped_message += f"🔢 Most stats taken on team 3255: {stats_on_3255_count.most_common(1)[0][0]} with {stats_on_3255_count.most_common(1)[0][1]} stats\n"
wrapped_message += f"🎸 Most stats taken on AMP: {amp_stats_count.most_common(1)[0][0]} with {amp_stats_count.most_common(1)[0][1]} stats\n"
wrapped_message += f"🔊 Most stats taken on SPEAKER: {speaker_stats_count.most_common(1)[0][0]} with {speaker_stats_count.most_common(1)[0][1]} stats\n"

# Additional statistics
total_stats = len(data)
wrapped_message += f"\n📊 Total stats recorded: {total_stats}\n"

average_stats_per_member = total_stats / len(unique_team_members)
wrapped_message += f"📈 Average stats per team member: {average_stats_per_member:.2f}\n"

most_active_member = stats_count.most_common(1)[0][0]
most_active_member_stats = stats_count.most_common(1)[0][1]
wrapped_message += f"🔥 Most active member: {most_active_member} with {most_active_member_stats} stats\n"

print(wrapped_message)