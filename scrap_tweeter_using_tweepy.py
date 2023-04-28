"""
Scrap tweeter using Tweepy
Original file is located at : https://colab.research.google.com/drive/1DwS-rrG748R8aGMTF-KmE-K4Ac9LqMU0
Here some code to scrap Tweeter But due to... 
error : Rate limit exceeded I was not able to create excel file :(
But I have scrapped data successfully
"""

# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os
import re
import tweepy
from .config import api_key, api_key_secret, access_token, access_token_secret

credential_url = "https://gist.githubusercontent.com/vrushangdev/e26987231a1e8517b6b7f3487f74d6d0/raw/9339c09c2298a3b91fc743c67ee880ce79e1c5e7/gsheet_creds.json"

response = requests.get(credential_url)

try:
  cred_file = open('file.json','w')
  cred_file.write(response.text)
  cred_file.close()
except Exception as e:
  print(e)
finally:
  cred_file.close()

gc = gspread.service_account(filename='file.json')
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1slvCX233_Qwqw1JPENxSL7qZzMLFwUmPbvFC6p7YJ_Q")
work_sheet = gsheet.worksheets()[0]
twitter_links = work_sheet.col_values(5)

# replace the values
api_key = api_key
api_key_secret = api_key_secret
access_token = access_token
access_token_secret = access_token_secret

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def scrape_tweet_data(link):
    tweet_link = link
    tweet_ids = re.findall(r"\/status\/(\d+)", tweet_link)
    if tweet_ids: #Checking if tweet_ids is not empty
        tweet_id = tweet_ids[0]
        tweet = api.get_status(tweet_id)
        if not tweet: #Checking if tweet is empty or not
          return None
        time_stamp = tweet.created_at
        promotor_tweet_screen_name = "https://tweeter.com/"+tweet.user.screen_name
        promoter_tweet_link = "https://twitter.com/{}/status/{}".format(tweet.user.screen_name, tweet.id)
        promotor_tweet_likes = tweet.favorite_count
        promotor_tweet_text = tweet.text
        try:
            if tweet.in_reply_to_status_id is not None:
                influencer_tweet = api.get_status(tweet.in_reply_to_status_id)
                influencer_tweet_screen_name = "https://tweeter.com/"+influencer_tweet.user.screen_name
                influencer_tweet_link = "https://twitter.com/{}/status/{}".format(influencer_tweet.user.screen_name, influencer_tweet.id)
                influencer_tweet_likes = influencer_tweet.favorite_count
                influencer_tweet_text = influencer_tweet.text
            else:
                influencer_tweet_screen_name = "none"
                influencer_tweet_link = "none"
                influencer_tweet_likes = "none"
                influencer_tweet_text = "none"
        except:
            influencer_tweet_screen_name = "none"
            influencer_tweet_link = "none"
            influencer_tweet_likes = "none"
            influencer_tweet_text = "none"
        
        #creating a dictionary
        tweet_data = {
            "time_stamp": time_stamp,
            "promotor_tweet_screen_name": promotor_tweet_screen_name,
            "promoter_tweet_link": promoter_tweet_link,
            "promotor_tweet_likes": promotor_tweet_likes,
            "promotor_tweet_text": promotor_tweet_text,
            "influencer_tweet_screen_name": influencer_tweet_screen_name,
            "influencer_tweet_link": influencer_tweet_link,
            "influencer_tweet_likes": influencer_tweet_likes,
            "influencer_tweet_text": influencer_tweet_text
        }
        return tweet_data
    else:
        return None

df = pd.DataFrame()

for tweets in twitter_links:
  dictionary = scrape_tweet_data(tweets)
  if dictionary:
    df = df.append(dictionary, ignore_index=True)

if not df.empty:
  output_path = "output.xlsx"
  writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
  df.to_excel(writer, index=False, sheet_name='Sheet1')
  writer.save()
  print("Data written to", os.path.abspath(output_path))
else:
  print("No data to write to file.")