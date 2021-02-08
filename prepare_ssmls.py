from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import yaml

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

stream = open('config.yml', 'r')
keys = yaml.safe_load(stream)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = keys['SAMPLE_SPREADSHEET_ID']
Sentences_Range = keys['Sentences_Range']
Voices_Range = keys['Voices_Range']
ssml_filename = keys['SSMLs']



def main():
    create_ssmls(fetch_data())



def fetch_data():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    sentence = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=Sentences_Range).execute()
    voice = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=Voices_Range).execute()
    values1 = sentence.get('values', [])
    values2 = voice.get('values', [])
    
    data = {}
    data["sentences"] = {}

    for n in range(len(values1[0])):
        data["sentences"][values1[0][n]] = values1[1][n]

    data["voices"] = {}

    for n in range(len(values2)):
        data["voices"][n] = values2[n]

    return data


def create_ssmls(data: dict):

    SSMLs = {}
    all_ssmls = []

    for n in data["voices"]:    
        voice = data["voices"][n][0]
        lang = voice[:5]
        SSMLs[voice] = {}
        for m in data["sentences"]:
            text = data["sentences"][m]
            SSML = f'<speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\" {lang} \"> <voice name=\"{voice}\"> {text} </voice> </speak>'
            SSMLs[voice][m] = SSML
            all_ssmls.append(SSML)
    
    data["SSMLs"] = SSMLs
    data["list_of_SSMLs"] = all_ssmls

    with open('ssmls.json', 'w') as fp:
        json.dump(data, fp)
    


if __name__ == "__main__":
    main()