"""Google API."""


import googleapiclient.discovery
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1WrCzu4p5lFwPljqZ6tMQEJb2vSJQSGjyMsqcYt-yS4M'
SAMPLE_RANGE_NAME = 'A1:A4'


def get_links_from_spreadsheet(id: str, token: str) -> list:
    """Return a list of strings from the first column of a Google Spreadsheet with the given ID."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                token, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=id,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return []
        result = []
        for row in values:
            result.append(*row)
        return result
    except HttpError as err:
        print(err)


def get_links_from_playlist(link: str, developer_key: str) -> list:
    """Return a list of links to songs in the Youtube playlist with the given address."""
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=developer_key)

    request = youtube.playlistItems().list(
        part="contentDetails",
        maxResults=50,
        playlistId=link
    )
    response = request.execute()
    total_results = response["pageInfo"]["totalResults"]
    urls = []
    result = 0
    while result < total_results:
        count = 0
        for value in response["items"]:
            urls.append("https://www.youtube.com/watch?v=" + value["contentDetails"]["videoId"])
            count += 1
        if "nextPageToken" in response.keys():
            new_request = youtube.playlistItems().list(
                part="contentDetails",
                maxResults=50,
                playlistId=link,
                pageToken=response["nextPageToken"]
            )
            response = new_request.execute()
            result += count
            continue
        return urls


if __name__ == '__main__':
    print(get_links_from_spreadsheet('1WrCzu4p5lFwPljqZ6tMQEJb2vSJQSGjyMsqcYt-yS4M', "credentials.json"))
    print(get_links_from_playlist("PLAEfXHuNOsEaPIpoGREE6Ska11g5mtwq5", "AIzaSyAzmuwS86iuBEsZPsIkq4Nkrb47Jmz6hzM"))
