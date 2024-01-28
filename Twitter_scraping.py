import time

import snscrape.modules.twitter as sntwitter
import streamlit as st
import pandas as pd
import pymongo
from pymongo import MongoClient
from PIL import Image
from datetime import date
import json

atlas_username = 'karthick3003'
atlas_password = 'sk3003'
atlas_cluster = 'cluster0'
client = MongoClient(
    f"mongodb+srv://{atlas_username}:{atlas_password}@{atlas_cluster}.gel395d.mongodb.net/?retryWrites=true&w=majority"
)
db = client['Twitter_project']
collection = db['Scraping']

def main():
    tweets = 0
    st.title("Twitter Scraping")
    menu = ["Home","About","Search","Display","Download"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice=="Home":
        st.balloons()
        st.write('''This app is a Twitter Scraping web app created using Streamlit. 
             It scrapes the twitter data for the given hashtag/ keyword for the given period.
             The tweets are uploaded in MongoDB and can be dowloaded as CSV or a JSON file.''')

    elif choice=="About":
        st.balloons()
        with st.expander("Twitter Scrapper"):
            st.write('''Twitter Scraper will scrape the data from Public Twitter profiles.
                                It will collect the data about **date, id, url, tweet content, users/tweeters,reply count, 
                                retweet count, language, source, like count, followers, friends** and lot more information 
                                to gather the real facts about the Tweets.''')

        with st.expander("Snscraper"):
            st.write('''Snscrape is a scraper for social media services like *twitter, faceboook, instagram and so on*. 
                             It scrapes **user profiles, hashtages, other tweet information** and returns the discovered items from the relavent posts/tweets.''')

            # Info about MongoDB database
        with st.expander("Mondodb"):
            st.write('''MongoDB is an open source document database used for storing unstrcutured data. The data is stored as JSON like documents called BSON. 
                          It is used by developers to work esaily with real time data analystics, content management and lot of other web applications.''')

            # Info about Streamlit framework
        with st.expander("Streamlit"):
            st.write('''Streamlit is a **awesome opensource framwork used for buidling highly interactive sharable web applications*** in python language. 
                          Its easy to share *machine learning and datasciecne web apps* using streamlit.
                          It allows the app to load the large set of datas from web for manipulation and  performing expensive computations.''')
    elif choice=="Search":
        collection.delete_many({})

        with st.form(key='form1'):
            st.subheader("Tweet search Form").balloons()
            st.write("Entre the hastah or keyword to perform the twitter scraping:#")
            query = st.text_input('Hashtag or keyword')

            st.write("Enter the limit for the data scaping: Maximum limit is 1000 tweets")
            limit = st.number_input('Insert a number',min_value=0,max_value=1000,step=10)

            st.write("Enter the Starting date to scrap the Tweet data")
            start = st.date_input('Start date')
            end = st.date_input('End data')

            time.sleep(1)
            submit_button = st.form_submit_button(label="Tweet Scrap")

            time.sleep(1)
        if submit_button:
            st.success(f"Tweet hashtag{query} received for scraping".format(query))

            try:
                for tweet in sntwitter.TwitterTweetScraper(f'from:{query} since:{start} until:{end}').get_items():
                    if tweets == limit:
                        time.sleep(1)
                        break
                    else:
                        time.sleep(1)
                        new = {"date":tweet.date,"user":tweet.user.username,"url":tweet.url,
                               "followersCount":tweet.user.followersCount,"friendsCount":tweet.user.friendsCount,
                               "favouritesCount":tweet.user.favouritesCount,"mediaCount":tweet.user.mediaCount
                               }
                        collection.insert_one(new)
                        tweets += 1

                        time.sleep(1)
                    df = pd.DataFrame(list(collection.find()))
                    cnn = len(df)
                    time.sleep(1)
                    st.success(f"Total number of tweets scraped for the input query is = {cnn}".format(cnn))
            except Exception as e:
                print(f"An Error occured: {e}")
    elif choice =="Display":
        df = pd.DataFrame(list(collection.find()))
        st.dataframe(df).balloons()

    else:

        col1,col2 = st.columns(2)

        with col1:
            st.write("Download the tweet data as CSV file")
            df = pd.DataFrame(list(collection.find()))
            df.to_csv('Tweetscape.csv')

            def convert_df(data):
                return df.to_csv().encode('utf-8')
            csv = convert_df(df)
            st.download_button(
                label = "Download data as CSV",
                data = csv,
                file_name = 'Tweetscape.csv',
                mime = 'text/csv'
            )
            st.success("You've successfully Downloaded the data as CSV file").balloons()

        with col2:
            st.write("Download the tweet data as JSON file")
            twtjs = df.to_json(default_handler=str).encode()
            obj = json.loads((twtjs))
            js = json.dumps(obj,indent=4)
            st.download_button(
                label = "Download data as JSON",
                data = js,
                file_name='Tweetscape.js',
                mime='text/js'
            )
            st.success("You've successfully Downloaded the data as JSON file").balloons()
main()