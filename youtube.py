from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser, run_flow

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

class YouTubeInfo(object):
	API_SERVICE_NAME = "youtube"
	API_VERSION = "v3"

	def get_authenticated_service(self,args):
		return build(API_SERVICE_NAME, API_VERSION,developerKey = 'AIzaSyAYDkFT5QHhh5b7niKuqrlKJjpn0nfrCvQ')

	def list_videos(self,youtube,video_id):
		results = youtube.videos().list(
		  part = 'snippet,contentDetails,statistics',
		  id = video_id
		).execute()
		
		return results





