from twitter import Twitter
import re
import pandas as pd
import nltk
nltk.download([
"names",
"stopwords",
"punkt",
])
from nltk.sentiment import SentimentIntensityAnalyzer
from streamlit_extras.metric_cards import style_metric_cards
import streamlit as st
import altair as alt
#pip install streamlit-extras nltk pandas tqdm 
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.figure_factory as ff



# Using "with" notation
with st.sidebar:
   st.header('Trend of Twitter Dashboard |TDD')
   st.subheader('Author Loai abdalslam ')
   st.text('The Twitter project aims to explore tweets, users and current trends in an analytical manner \n and more closely than ever before. \n The project is open source and all rights are reserved to my person \n under the right of creative development.')

st.write("# Trend of Twitter Dashboard | TTD ")
st.write("In this project we will use machine learning and stastical models to observer all trends and tweets in twitter and social media ")


twitter = Twitter()
twitter_df = twitter.getTrendsMetaData()
twitter_cards_data = (len(twitter_df[0]),sum(twitter_df[1]))

st.subheader("Trending Now Cards")

col1, col2, col3 = st.columns(3)
col1.metric(label="Total Trends", value=twitter_cards_data[0] )
col2.metric(label="Total Tweets", value=twitter_cards_data[1] )
style_metric_cards()





# Group data together
hist_data = twitter_df[1]
group_labels = twitter_df[0]




source = pd.DataFrame({
        'Tweets Count': hist_data,
        'Hashtags': group_labels
     })


st.subheader("Trending Now , check it")
bar_chart = alt.Chart(source).mark_bar().encode(
        y='Tweets Count',
        x=alt.X('Hashtags', axis=alt.Axis(labelAngle=-45)),
    )

st.altair_chart(bar_chart, use_container_width=True)


st.subheader("Sentiment Analysis For Trendy Tweets ")


col1, col2 = st.columns(2)
with col1:
    place = st.text_input(
        "Please set country within tweets",
        "Cairo",
        key="placeholder",
    )

with col2:
    number = st.number_input('Insert a number of tweets for each trend to fetch',3)







twitter_df = twitter.getTrendyTweets(place,number)



sia = SentimentIntensityAnalyzer()
sia_dict = {'positive':0,'neatral':0,'negative':0,'total':0}
for tweet in twitter_df.content:
    sia_x = sia.polarity_scores(tweet)
    sia_dict['positive'] += sia_x['pos']  
    sia_dict['negative'] += sia_x['neg'] 
    sia_dict['neatral'] += sia_x['neu'] 
    sia_dict['total'] += 1 


    
col1, col2, col3 = st.columns(3)
col1.metric(label="Positive 😀", value=sia_dict['positive'] )
col2.metric(label="Negative 🙁", value=sia_dict['negative'] )
col3.metric(label="Neatral 🙂", value=sia_dict['neatral'] )

style_metric_cards()
