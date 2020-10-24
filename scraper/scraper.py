import twitter
import json
from dateutil.parser import parse
from datetime import datetime, timezone
from DB import DB

class Scraper:

	def __init__(self, config):
		
		self.config = config

		#max age of a tweet in days
		self.MAX_TWEET_AGE = config['max_tweet_age']
		#number of tweets to fetch
		self.N_OF_TWEETS = config['number_of_tweets']

		#authenticate to api
		self.api = twitter.Api( consumer_key=config['api_keys']['consumer_key'],
						consumer_secret=config['api_keys']['consumer_secret'],
						access_token_key=config['api_keys']['access_token_key'],
						access_token_secret=config['api_keys']['access_token_secret'],
						tweet_mode="extended"
						)


	# get ids of users in the config file
	# return: dictionary in the form {user_screen_name: user_id}
	def get_ids(self):
		#screen_names of interesting followed accounts
		users_names = [self.config['users'][i]['name'] for i in range(len(self.config['users']))]

		#followed accounts
		friends = self.api.GetFriends()

		users = {}
		#get id of interesting followed accounts
		for friend in friends:
			if friend.screen_name in users_names:
				users[friend.screen_name] = friend.id

		return users


	# get tweets from users
	# return: dictionary of lists of dictionaries in the form {
	# 															'user_screen_name':[
	# 																					{'creation_date': creation_date_of_the_tweet, 'text':text_of_the_tweet}, 
	# 																				]
	#														  }
	def get_tweets(self):

		users = self.get_ids()
		tweets = {}

		for user in users.keys():
			print("[*] Fetching timeline from ",user)
			tweets[user] = []
			#get last N_OF_TWEETS tweets of the user
			#in the N_OF_TWEETS tweets the retweets and the replies are included but we exclude them from the response
			statuses = self.api.GetUserTimeline(users[user], count=self.N_OF_TWEETS, include_rts=False, exclude_replies=True)
			
			for status in statuses:
				#get creation time of the tweet
				creation_date = parse(status.created_at)
				#get text of the tweet
				text = status.full_text
				#if tweet is younger than MAX_TWEET_AGE take it
				if (datetime.now(timezone.utc)-creation_date).days < self.MAX_TWEET_AGE:
					tweets[user].append({'creation_date':creation_date, 'text':text})
							
		return tweets
			

'''
Put logic below in a main script
'''
if __name__=='__main__':

	#read config file
	with open("../config.json","r") as f:
		config = json.loads(f.read())
	
	scraper = Scraper(config)
	tweets = scraper.get_tweets()

	db = DB(config)

	if db.get_count("tweets") > config['db']['max_number_of_documents']:
		print(f"[*] Deleting last {config['db']['documents_to_delete']} tweets from DB")
		db.delete_last_n("tweets", config['db']['documents_to_delete'])


	for user in tweets.keys():
		print(f"[*] Inserting tweets of {user} in the DB")
		for i,tweet in enumerate(tweets[user]):
			#print(f'{i+1}) \t{tweet["creation_date"]} \n\t {tweet["text"]}')
			to_insert = {"user":user, **tweet} 
			db.insert_one("tweets", to_insert)

	print("[*] Done")
	
	#TODO
	# 1. Create web service
	# 2. store also tweet link and other infos
	# 3. Create a logging class to print things in a better way