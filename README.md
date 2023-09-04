# HAR (HTTP Archive) file analyser
Python program to analyze HAR files (network tab exports) and calculate the number of events for each user_id.
the program produces an output which compares the number of universal analytics events(event_actions) against their google analytics events(event_names)
Any missing events(events that do not have a correspondance) on either side will be set blank, and a total count for either set is porvided at the top.

This program enables data analysts to validate their new GA4 setup against their old UA events. And check whether the new setup has been implemented and is working correctly.
