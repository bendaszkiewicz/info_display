import twitter
from datetime import date, time, datetime

def getTweets(numTweets): 

	#"You can get all 4 by heading over to # https://apps.twitter.com. #

	#Once there, sign in with your Twitter account and click on “Create New App” button.

	#Fill in required information (note that app name must be unique) 
	# and select “Create Your Twitter Application”.

	#You will be taken to your application view. 
	# There click on “Keys and Access Tokens” tab. 
	# Look for section called Token Actions and click on “Create my Access Token”. 
	# The page should refresh, and if everything went well you should see both 
	# Consumer Key/Secret and Access Token/Secret."
	# - (@akras14)

	api = twitter.Api(consumer_key='wJ5qIbnmho7fxnT2GEth2K1qi', #Fill in -- Replace with user twitter keys
	  consumer_secret='nT1AcZ8vL2UVD3wrtgvO96j3n5rOeUPtCQxBUPs07jHDujBwkk', #Fill in
	  access_token_key='101409260-tX23vQsxtvfx6p4J7gzymYHBqTlItUItCP7HegSb', #Fill in
	  access_token_secret='67JWctaCdWQmvyqLkU1uDf1Z5ybVNlTJ3wjt42k6uLhsv') #fill in
	  
	#print(api.VerifyCredentials())
	  
	t = api.GetUserTimeline(screen_name="MaliLabNews", count=numTweets) #Put username here, can change count
	  

	  #"The following command uses list comprehension 
	  #which is just a hipster way of doing a for loop on every Tweet, 
	  #converting it to a Dictionary via built in “AsDict” method, 
	  #and storing all of the converted Tweets into a List."
	  # -(@akras14)
	  
	tweets = [i.AsDict() for i in t]
	returnedTweet = ['time','text']
	returnedTweetsList = []
	status = 4

	for t in tweets:
		#print('\n', t['id'], t['text'])
		#print('Time: ' + t['created_at'])
		#print(t['text'] + '\n')
		text = t['text']
		text = text.encode('ascii', 'ignore')
		tempTime = t['created_at']
		tempTime = datetime.strptime(tempTime, '%a %b %d %H:%M:%S %z %Y')
		returnedTweet[0] = datetime.strftime(tempTime, '%A, %B %d, %Y')
		returnedTweet[1] = text

		#Below, searches each tweet and updates status
		#technically last tweet will change the last status
		if (t['text'].find("*Available")) != -1:
			status = 3
			#Status 3 = Available
		if (t['text'].find("*Busy")) != -1:
			status = 2
			#Status 2 = Busy
		if (t['text'].find("*Away")) != -1:
			status = 1
			#Status 1 = Away
		if (t['text'].find("*hide")) != -1 and (t['text'].find("*offline")) != -1:
			status = 0
			#Status 0 = Hide availability meter

		returnedTweetsList.append(returnedTweet[0:])

	returnObject = [returnedTweetsList,status]

	return (returnObject)
