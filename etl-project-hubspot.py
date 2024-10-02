#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 17:33:58 2022

@author: nikhiladiga
"""

import gspread
import pandas as pd
import requests
import json


#Create a google sheets api in Google Cloud Platform, create a API key and download the json key file 
moneyhop_gcp_creds = 'ADD_YOUR_FILE_PATH'

# EXTRACT
#connect gsheets
gp = gspread.service_account(filename=moneyhop_gcp_creds)
gsheet = gp.open('Credence Disbursed Cases For Remittance - 08-02-2022')
wsheet = gsheet.worksheet("Sheet1")


# TRANSFORM
#Function to clean data and covert to df
def gsheet_to_df(wsheet):
    all_rows = wsheet.get_all_values()  # Fetch all the rows of data
    columns = all_rows.pop(0)  # First row is treated as header (columns)
    df = pd.DataFrame(all_rows,columns=columns)
    
    return df

# Function to append country code to phone number 
def add_country_code(row):
  phone_num = row['Contact No']
  if len(phone_num) == 10:
    phone_num = "+91"+phone_num

    return phone_num
  elif len(phone_num) == 11:
    phone_num = phone_num[1:]
    phone_num = "+91"+phone_num

    return phone_num
  else:
    return phone_num

df = gsheet_to_df(wsheet)


for _, row in df.iterrows():
    row['Contact No'] = add_country_code(row)
    print(row)
    
# LOAD

# Update contact in hs and add it to a list
# Get the HubSpot API key from your HubSpot account and add it below
hapi_key = 'ADD_HUBSPOT_API_KEY'
headers = {}
headers["Content-Type"]="application/json"

# Function to get contact owners from HubSpot
def get_owners():
    owner_url = "https://api.hubapi.com/owners/v2/owners?hapikey="+hapi_key
    r = requests.get(url = owner_url)
    r_dict = json.loads(r.text)
    data = pd.DataFrame.from_dict(r_dict)
    print(r.text)
    return data

contact_owners = get_owners()

# Create a HubSpot CRM contact
def create_hs_contact(data, headers):
    url = 'https://api.hubapi.com/contacts/v1/contact/?hapikey='+hapi_key
    r = requests.post( url = url, data = data, headers = headers )
    return print(r.text)

# Get list id from HubSpot lists
# Add contact to HubSpot CRM lists to perform bulk actions
def add_to_list(email):
    list_id = '188'
    url = 'https://api.hubapi.com/contacts/v1/lists/'+list_id+'/add?hapikey='+hapi_key
    data = json.dumps({
                          "emails": [
                            email
                          ]
                        })
    r = requests.post(url=url, data=data, headers=headers)
    return print(r.text)

# Script to create contact and add to list
for _, row in df.iterrows():
    email = row['Email_id']
    full_name = row['Customer Name']
    first_name = row['First Name']
    hubspot_owner_id = row['Contact Owner']
    phone = row['Contact No']
    
    data = json.dumps({
      "properties": [
        {
          "property": "email",
          "value": email
        },
        {
          "property": "full_name",
          "value": full_name
        },
        {
          "property": "firstname",
          "value": first_name
        },
        {
          "property": "hubspot_owner_id",
          "value": hubspot_owner_id
        },
        {
          "property": "phone",
          "value": phone
        },
        {
          "property": "lead_type",
          "value": "Credenc"
        },
      ]
    })
    try:
        create_hs_contact(data, headers)
        add_to_list(email)
        print(f'Created contact in HubSpot')
    except:
        add_to_list(email)
        print(f'Added contact to list')
    



