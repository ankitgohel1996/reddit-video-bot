import praw,pprint
from oauth2client.tools import argparser, run_flow
from db import get_db
from youtube import YouTubeInfo
import isodate

connection = get_db()
youtubeobject = YouTubeInfo()
args = argparser.parse_args()
youtube = youtubeobject.get_authenticated_service(args)

def main():
	reddit = praw.Reddit(client_id='AVvBGy0ZFlVgMw',
	                     client_secret='R9SaacImMQOiXLawVtKs5hZSqcQ',
	                     password='katebeckett   ',
	                     user_agent='python : youtubebot : v1.0.0 (by /u/video_descriptionbot)',
	                     username='video_descriptionbot')
	
	subreddit = reddit.subreddit('test')
	for comment in subreddit.stream.comments():
		find_comments(comment)		
	
def find_comments(comment):
	if comment.author == 'video_descriptionbot':
		return

	if comment.score < 1:
		return

	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM  comments WHERE comment_id = "%s"' % (comment.id))
		result = cursor.rowcount

		if result == 0:

				if 'youtube.com' in comment.body or 'youtu.be' in comment.body:
					reply_post = 'SECTION | CONTENT' +'\n' + ':--|:--' +'\n'

					if '](' in comment.body:
						comment_parts = comment.body.split(']')
						youtube_link = comment_parts[1].split(')')[0][1:]
						if 'youtube.com' in youtube_link or 'youtu.be' in youtube_link:
							reply_title,reply_description,reply_duration = find_id(youtube_link)
							reply_post += 'Title | '+ reply_title +'\n'
							reply_post += 'Description | '+ reply_description +'\n'
							reply_post += 'Length | '+ str(reply_duration) +'\n'
					else:
						words = comment.body.split()
						for word in words:
							if 'youtube.com' in word or 'youtu.be' in word:
								reply_title,reply_description,reply_duration = find_id(word)
								reply_post += 'Title | '+ reply_title +'\n'
								reply_post += 'Description | '+ reply_description +'\n'
								reply_post += 'Length | '+ str(reply_duration) +'\n'
					reply_post += '\n'+'*I am a bot, this is an auto-generated reply*'

					try:
						comment.reply(reply_post)
						with connection.cursor() as cursor:
							cursor.execute('INSERT INTO comments VALUES("%s")' % (comment.id))
							connection.commit()
					except Exception as e:
						print (e)
	
def find_id(link):
	if 'v=' in link:
		link_parts = link.split('v=')
		video_id = link_parts[1].split('&')[0]
	elif 'tu.be' in link:
		link_parts = link.split('tu.be/')
		if '?' in link_parts[1]:
			video_id = link_parts[1].split('?')[0]
		else:
			video_id = link_parts[1]

	results = youtubeobject.list_videos(youtube,video_id)

	for item in results['items']:
		description = item['snippet']['description'].replace('\n',' ')
		title = item['snippet']['title']
		length = isodate.parse_duration(item['contentDetails']['duration'])

	return title, description, length

if __name__ == '__main__':
	main()