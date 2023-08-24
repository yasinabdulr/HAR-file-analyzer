import json
from collections import defaultdict

def process_har(file_path):
    # Load the HAR file with utf-8 encoding
    with open(file_path, "r", encoding="utf-8") as file:
        har_data = json.load(file)

    # Extract relevant GA4 network calls from the HAR file
    ga4_entries = [entry for entry in har_data["log"]["entries"] if entry["request"]["url"].startswith("https://region1.google-analytics.com/g/collect?v=2")]

    # Extract event name and profile_gigyaid from each entry
    events_data = []
    for entry in ga4_entries:
        url = entry["request"]["url"]
        event_name = None
        profile_gigyaid = "undefined"
        
        # Extracting parameters from URL
        params = url.split("?")[1].split("&")
        for param in params:
            key, value = param.split("=")
            
            # Extract event name
            if key == "en":
                event_name = value
                
            # Extract profile_gigyaid
            if key == "ep.profile_gigyaid":
                profile_gigyaid = value
        
        # If event_name is not found in the URL, check the postData (request payload)
        if not event_name and "postData" in entry["request"]:
            payload_data = entry["request"]["postData"]["text"]
            if "en=" in payload_data:
                for param in payload_data.split("&"):
                    key, value = param.split("=")
                    if key == "en":
                        event_name = value
                    if key == "ep.profile_gigyaid":
                        profile_gigyaid = value
        
        if event_name:
            events_data.append((event_name, profile_gigyaid))

    # Counting occurrences of each event along with its profile_gigyaid
    event_gigyaid_counts = defaultdict(int)
    for event, gigyaid in events_data:
        event_gigyaid_counts[(event, gigyaid)] += 1

    # Sorting based on gigyaid, then count (descending), and then event name
    sorted_results = sorted(event_gigyaid_counts.items(), key=lambda x: (x[0][1], -x[1], x[0][0]))

    return sorted_results

# Main function to execute the script
if __name__ == "__main__":
    results = process_har("radio.har")
    
    # Printing the table header
    print("{:<30} | {:<10} | {:<40}".format("Event Name", "Count", "Profile Gigyaid"))
    print("-" * 85)  # Line separator

    # Printing the table rows
    for (event, gigyaid), count in results:
        print("{:<30} | {:<10} | {:<40}".format(event, count, gigyaid))
