import tweepy

def create_api():
  auth = tweepy.OAuthHandler("nXUZNML7heaDWqbZYGDgwovfI", input("What is your secret consumer key? "))
  auth.set_access_token("1212837998007443456-I6IW18hInhd0MhbqeNHRffyKcWmFAL", input("What is your secret access key? "))


  api = tweepy.API(auth)
  return api