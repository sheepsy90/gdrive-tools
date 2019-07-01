from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
	"""Shows basic usage of the Drive v3 API.
	Prints the names and ids of the first 10 files the user has access to.
	"""
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
			
	drive_service = build('drive', 'v3', credentials=creds)
	
	entity_id = '1paENLQDdVmig2IcQbQBgeTDK7bCfRkom'
	# Found folder: Gotland 2018 (1paENLQDdVmig2IcQbQBgeTDK7bCfRkom)
	page_token = None
	
	"""
	while True:
		response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and name contains 'Gotland'", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
		for file in response.get('files', []):
			# Process change
			print ('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
		page_token = response.get('nextPageToken', None)
		if page_token is None:
			break
	"""
	counter = 0
	while True:
		response = drive_service.files().list(q="'1paENLQDdVmig2IcQbQBgeTDK7bCfRkom' in parents", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
		for file in response.get('files', []):
			# Process change
			print ('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
			counter += 1
		page_token = response.get('nextPageToken', None)
		if page_token is None:
			break
	
	print (counter)


if __name__ == '__main__':
	main()
