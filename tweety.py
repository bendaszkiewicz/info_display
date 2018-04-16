import twitter

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

api = twitter.Api(consumer_key='xyz', #Fill in
  consumer_secret='xyzxyz', #Fill in
  access_token_key='xyzxyz', #Fill in
  access_token_secret='xyzxyz') #fill in
  
#print(api.VerifyCredentials())
  
t = api.GetUserTimeline(screen_name="akras14", count=5) #Put username here, can change count
  
  
  
  #"The following command uses list comprehension 
  #which is just a hipster way of doing a for loop on every Tweet, 
  #converting it to a Dictionary via built in “AsDict” method, 
  #and storing all of the converted Tweets into a List."
  # -(@akras14)
  
tweets = [i.AsDict() for i in t]
  
 #return (tweets)
for t in tweets:
	#print('\n', t['id'], t['text'])
	print(t['text'])