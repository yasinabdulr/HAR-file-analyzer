# HAR (HTTP Archive) file analyser

This tool provides an analysis of HAR (HTTP Archive) files extracted from the network tab, specifically targeting Google Analytics' UA and GA4 events. It counts and compares the number of UA and GA4 events fired in the network tab, providing insights into user interactions and analytics firing frequency.

The count of events for each analytics platform is listed in comparison.
Any missing events (events that do not have a correspondance) on either side will be set blank, and a total count for either set is also generated.
This program enables data analysts to validate their new GA4 setup against their old UA events. Enabling an automated check as to whether the new setup has been implemented right and is working correctly.

# Table of Contents
Prerequisites
Installation
Usage
Contribution
License

## Prerequisites
- Python 3.x
- Pip (Python package manager)

## Installation
Clone the repository:

```
git clone https://github.com/your-username/HAR-file-analyzer.git
cd HAR-file-analyzer
```

Install dependencies:

Using pip:
```
pip install pandas
```
Usage:
1.  Run the main script:

```
python HAR-file-analyzer.py
```

2.  Follow the on-screen prompts to provide the path to your HAR file. The script will then analyze the HAR file and output the results.

## Contribution
Contributions are welcome! Please fork the repository and open a pull request with your changes, or open an issue to discuss a potential change.

## License
This project is open-source and available under the [MIT](https://opensource.org/license/mit/) License.
