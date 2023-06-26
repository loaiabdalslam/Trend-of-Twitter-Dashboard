

import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as snstwitter


class Twitter:
    
    def __init__(self):
          self.meta_data = []
          self.trendy_feed=[]

    def feed(self,search_item,place,n_tweets):
        scrapper = snstwitter.TwitterSearchScraper(f'{search_item} near:"{place}" within:100km')
        tweets = []
        for i,tweet in enumerate(scrapper.get_items()):
            data = [
            tweet.date,
            tweet.content,
            tweet.user.username,
            tweet.likeCount,
            tweet.retweetCount,
            search_item
            ]
            tweets.append(data)
            if i >n_tweets:
                break
                
        return tweets
    
    
    def trendyFeed(self,place,n_tweets):
        tweets = []
        feed = snstwitter.TwitterTrendsScraper()
        self.trendy_feed=feed
        for trend in feed.get_items():
            trend = self.feed(trend.name,place,n_tweets)
            for tweet_raw in trend:
                tweets.append(tweet_raw)
        return tweets
    
    
    def getTrendyTweets(self,place,n_tweets):
        tweets = self.trendyFeed(place,n_tweets)
        
        return pd.DataFrame(tweets,columns=['date','content','username','likeCount','retweetCount','trend'])
    
    def getSearchedTweets(self,search_item,place,n_tweets):
        tweets = self.feed(search_item,place,n_tweets)
        return pd.DataFrame(tweets,columns=['date','content','username','likeCount','retweetCount','trend'])
    
    def getTrendsMetaData(self):
        meta_data_names=[]
        meta_data_numbers=[]
        feed = snstwitter.TwitterTrendsScraper()
        for trend in feed.get_items():
            try:
                if 'K' in trend.metaDescription:
                       count = int(float(trend.metaDescription.replace('K', '').replace('Tweets','').replace(',','')) * 1000)
                else:
                       count= int(float(trend.metaDescription.replace('K', '').replace('Tweets','').replace(',','')))
            except:
                pass
 
            meta_data_names.append(trend.name) 
            meta_data_numbers.append(count) 

        return meta_data_names,meta_data_numbers
    