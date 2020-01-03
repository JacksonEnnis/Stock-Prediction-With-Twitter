import tweepy
import logging
from config import create_api
import time
import re
def check_mentions(api, keywords, since_id):
  new_since_id = since_id
  for tweet in tweepy.Cursor(api.mentions_timeline,
    since_id=since_id).items():
    new_since_id = max(tweet.id, new_since_id)
    if tweet.in_reply_to_status_id is not None:
      continue
    if any(keyword in tweet.text.lower() for keyword in keywords):
      #if "predict" in tweet.text.lower():     
      regMatch = re.findall(r'\"(.+?)\"', tweet.text.upper())
      if len(regMatch) == 1:
        ticker = regMatch[0]

        from Analyst import Analyst
        result = Analyst.generatePrediction(ticker)

        from Stock import Stock
        
        date = Stock("AAPL").lastDay

        customMessage = "@" + str(tweet.in_reply_to_screen_name) + "\n"
        customMessage += "My Prediction:\n"
        if result[0] == 1:
          customMessage += ticker + "\n +1% for trading day after " + date + "\n %" + str(round(result[1]*100, 2)) + " model accuracy"

        elif result[0] == 0:
          customMessage += ticker + "\n +0% for trading day after " + date + "\n %" + str(round(result[1]*100, 2)) + " model accuracy"
        
        else:
          customMessage += ticker + "\n -0% for trading day after " + date + "\n %" + str(round(result[1]*100, 2)) + " model accuracy"

        api.update_status(
                  status=customMessage,
                  in_reply_to_status_id=tweet.id,
                )
        
        """
        elif "info" in tweet.text.lower():
          customMessage = "@" + str(tweet.in_reply_to_screen_name) + "\n" + "Hello! My name is Jackson and I am studying CS at IU. I am currently looking for internship oppurtunities, so if you are interested in working with me please email me at jackennisres@gmail.com"
          api.update_status(
          status=customMessage,
          in_reply_to_status_id=tweet.id,
        )
        """
            
    return new_since_id

def main():
  print("WE ARE RUNNING")
  api = create_api()
  since_id = 1
  while True:
    try:
      since_id = check_mentions(api, ["predict", "info"], since_id)
      print("Sleep a little")
      time.sleep(60)
    except:
      time.sleep(60)
      print("OOF")

if __name__ == "__main__":
    main()