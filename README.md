# Credence Disbursed Cases - Google Sheets to HubSpot Integration

## Overview
This Python script extracts data from a Google Sheet, processes it, and then integrates it with HubSpot CRM by creating contacts and adding them to a specific list. It is designed to be used by businesses needing to automate the process of syncing customer information from Google Sheets to HubSpot.

The script performs the following tasks:

Extract: Fetch data from Google Sheets.
Transform: Clean and format the phone numbers, adding a country code if necessary.
Load: Create new contacts in HubSpot CRM and add them to a specified HubSpot list.
Prerequisites
Python 3.x
Google Sheets API enabled on your Google Cloud Platform project.
A HubSpot account with API access.

## Setup Instructions
1. Google Sheets API Setup
Go to the Google Cloud Console.
Create a new project or use an existing one.
Enable the Google Sheets API and Google Drive API for your project.
Create service account credentials, download the JSON key file, and store it securely.

2. HubSpot API Key
Log in to your HubSpot account.
Navigate to Settings > Integrations > API Key.
Copy the API key.

3. Install Dependencies
Install the required Python packages:
bash
`pip install gspread pandas requests`

4. Script Configuration
Replace the moneyhop_gcp_creds variable with the path to your Google service account credentials JSON file.
Replace the hapi_key variable with your HubSpot API key.
python
`moneyhop_gcp_creds = 'path_to_your_google_credentials.json'
hapi_key = 'your_hubspot_api_key'`

5. Running the Script
Run the script with Python 3:
bash
`python script_name.py
`
The script will:

Fetch data from the Google Sheet named 'Credence Disbursed Cases For Remittance - 08-02-2022'.
Clean and transform the data (e.g., add country codes to phone numbers).
Create contacts in HubSpot CRM and add them to a list with the ID 188.

## Script Breakdown

### Extract

The script uses gspread to connect to the Google Sheets API and retrieve all rows from Sheet1.

`all_rows = wsheet.get_all_values()  # Fetch all the rows of data
`
### Transform

A function add_country_code ensures that all phone numbers have the correct country code (+91 for India).

`def add_country_code(row):
    ...
    # Adds +91 to 10-digit phone numbers`

### Load

The script uses HubSpot's API to create contacts and then adds them to a specific list.

`url = 'https://api.hubapi.com/contacts/v1/contact/?hapikey='+hapi_key
r = requests.post( url = url, data = data, headers = headers )`

## Error Handling
In case of failure while creating a contact, the script will attempt to add the contact to the list:
`except:
    add_to_list(email)`

## License
This project is not licensed.

## Author
This script was created by Nikhil Adiga.

You can modify and expand on this depending on your needs, such as adding more details on error handling, customization, or potential issues.






