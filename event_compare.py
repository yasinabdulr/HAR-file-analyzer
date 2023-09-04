import json
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
import pandas as pd

def analyze_GA4(file_path):
    """
    Analyze the HAR file to extract GA4 events.
    
    Args:
        file_path (str): Path to the HAR file.
        
    Returns:
        list: List of tuples containing GA4 event names, UID, and counts.
    """
    # Load the HAR file data
    with open(file_path, "r", encoding="utf-8") as file:
        har_data = json.load(file)

    # Filter entries related to GA4 events
    ga4_entries = [entry for entry in har_data["log"]["entries"] if "collect?v=2" in entry["request"]["url"]]
    events_data = []

    for entry in ga4_entries:
        url = entry["request"]["url"]
        # Extract UID from the URL
        uid = parse_qs(urlparse(url).query).get("uid", ["undefined"])[0]

        # Extract event_name from URL if available
        event_name_from_url = parse_qs(urlparse(url).query).get("en")
        if event_name_from_url:
            events_data.append((event_name_from_url[0], uid))

        # Check if the request has postData
        if "postData" in entry["request"]:
            payload_data = entry["request"]["postData"]["text"]
            # Split payload data by newline to get individual events
            events_from_payload = payload_data.split("\n")
            for event_data in events_from_payload:
                # Extract event name from each payload event
                event_name = parse_qs(event_data.split("&")[0]).get("en")
                if event_name:
                    events_data.append((event_name[0], uid))

    # Count the occurrences of each event per UID
    event_uid_counts = defaultdict(int)
    for event, uid in events_data:
        event_uid_counts[(event, uid)] += 1
        
    results = [(event, uid, count) for (event, uid), count in event_uid_counts.items()]
    return results

def analyze_UA(file_path):
    """
    Analyze the HAR file to extract UA events.
    
    Args:
        file_path (str): Path to the HAR file.
        
    Returns:
        list: List of tuples containing UA event actions, UID, and counts.
    """
    # Load the HAR file data
    with open(file_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)

    # Filter entries related to UA events
    UA_entries = [entry for entry in har_data["log"]["entries"] if "collect?v=1" in entry["request"]["url"]]

    event_action_counts = {}
    for entry in UA_entries:
        url = entry['request']['url']
        # Extract parameters from the URL
        query_params = parse_qs(urlparse(url).query)
        ea = query_params.get('ea', [None])[0]  # Event Action
        trigger = query_params.get('t', [None])[0]  # Trigger
        uid = query_params.get('uid', ['undefined'])[0]  # UID

        # Check if the event action is present and then count it
        if ea:
            if ea not in event_action_counts:
                event_action_counts[ea] = {}
            event_action_counts[ea][uid] = event_action_counts[ea].get(uid, 0) + 1

        # If there's a pageview trigger, handle it separately
        elif trigger == 'pageview':
            event_action = 'page_view'
            if event_action not in event_action_counts:
                event_action_counts[event_action] = {}
            event_action_counts[event_action][uid] = event_action_counts[event_action].get(uid, 0) + 1

    # Convert the dictionary to a list of tuples
    results = [(ea, uid, count) for ea, users in event_action_counts.items() for uid, count in users.items()]
    return results

def merge_outputs(file_path):
    """
    Merge the outputs of UA and GA4 analyses and add a total count row.
    
    Args:
        file_path (str): Path to the HAR file.
        
    Returns:
        DataFrame: Pandas DataFrame containing merged results with total count row.
    """
    # Get the results from both the GA4 and UA analyses
    results_GA4 = analyze_GA4(file_path)
    results_UA = analyze_UA(file_path)

    # Convert the results to DataFrames
    df_GA4 = pd.DataFrame(results_GA4, columns=["event_name_GA4", "uid_GA4", "count_GA4"])
    df_UA = pd.DataFrame(results_UA, columns=["event_action_UA", "uid_UA", "count_UA"])

    # Aggregate the GA4 results by event name and UID
    df_GA4_aggregated = df_GA4.groupby(["event_name_GA4", "uid_GA4"]).sum().reset_index()
    # Merge the two DataFrames on event names and UIDs
    merged_df = pd.merge(df_GA4_aggregated, df_UA, left_on=["event_name_GA4", "uid_GA4"], right_on=["event_action_UA", "uid_UA"], how="outer")

    # Calculate the total count of events for both GA4 and UA
    total_GA4 = merged_df['count_GA4'].sum()
    total_UA = merged_df['count_UA'].sum()
    # Create a total count row
    total_row = pd.DataFrame({
        "event_name_GA4": ["TOTAL"],
        "uid_GA4": ["-"],
        "count_GA4": [total_GA4],
        "event_action_UA": ["TOTAL"],
        "uid_UA": ["-"],
        "count_UA": [total_UA]
    })
    # Add the total count row at the top of the merged DataFrame
    merged_df = pd.concat([total_row, merged_df], ignore_index=True)
    # Sort the merged DataFrame by UID and count for GA4
    merged_df_sorted = merged_df.sort_values(by=["uid_GA4", "count_GA4"], ascending=[True, False])
    return merged_df_sorted

if __name__ == "__main__":
    # Prompt the user for the HAR file path
    file_path = input("Enter the path to your HAR file: ")
    # Get the merged output and print it
    merged_output = merge_outputs(file_path)
    print(merged_output)
