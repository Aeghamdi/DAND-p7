#!/usr/bin/env python
# coding: utf-8

# **Gathering Data**

# In[503]:


#importing the needed libraries
import tweepy
import requests
import pandas as pd
import json
import time
from functools import reduce
import matplotlib.pyplot as pl
import seaborn as sns
import math
import re


# In[504]:


#reading the twitter-archive-enhanced.csv file using pandas library
data_csv = pd.read_csv('twitter-archive-enhanced.csv')
data_csv.head(10)


# In[505]:


#download image-predictions.tsv using the Requests library
Data_url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
rs = requests.get(Data_url)

with open(Data_url.split('/')[-1], mode = 'wb') as file:
    file.write(rs.content)
    
#Reading tweet image predictions TSV file
data_img = pd.read_csv('image-predictions.tsv', sep='\t')
data_img.head(10)


#  I will not use twitter API but this is the needed steps.

# In[506]:


import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)


# since i am not going to use twitter API i have to read the JSON file.

# In[507]:


data_list = []
with open('tweet-json.txt', 'r', encoding='utf-8') as json_file:
    for line in json_file:
        Json_Record = json.loads(line)
        
        #dictionaries
        data_list.append({'tweet_id': Json_Record['id'],'retweet_count': Json_Record['retweet_count'],
                        'favorite_count': Json_Record['favorite_count'],' ':Json_Record['created_at'],
                        'language':Json_Record['lang'],'display_text_range': Json_Record['display_text_range'],
                        'source':Json_Record['source']})
#align rows and column labels using pandas DataFrame
tweets_data = pd.DataFrame(data_list, columns = ['tweet_id', 'retweet_count', 'favorite_count','creat_date','language','display_text_range','source'])

#to check the result
tweets_data.info()
tweets_data.head(10)


# ## Assessing Data
# 
# **First**
# 
# *  twitter-archive-enhanced.csv

# In[508]:


#print rows 
data_csv.head(4)


# In[509]:


#summary of the dataset
data_csv.info()


# In[510]:


#simple statistics for every column in the dataset
data_csv.describe()


# In[511]:


#to know how many name do we have
print("name count is {}".format(data_csv['name'].count()))


# In[512]:


#print all values count of the name column to check the nature of the data in this coulmn
data_csv['name'].value_counts()


# In[513]:


#check if there is a null values in tweet id column
print("NULL count of name is {}".format(data_csv['name'].isnull().sum()))


# **Good News: No null values in name column.**

# In[514]:


#to know how many ID do we have
print("IDs count is {}".format(data_csv['tweet_id'].count()))


# In[515]:


#print all values count of the ID column to check if there is any dublication or not, because its an ID and should be unique
data_csv['tweet_id'].value_counts()


# **Good News: The tweet ID is unique**

# In[516]:


#check if there is a null values in tweet id column
print("NULL count of tweet ID is {}".format(data_csv['tweet_id'].isnull().sum()))


# **Good News: No null values in tweet ID column.**

# **Second**
# 
# *  image-predictions.tsv

# In[517]:


#summary of the dataset
data_img.info()


# In[518]:


#simple statistics for every column in the dataset
data_img.describe()


# In[519]:


#printing sample of the data
data_img.head(7)


# In[520]:


print("count of tweet ID: {}".format(data_img['tweet_id'].count()))


# In[521]:


#print all values count of the ID column to check if there is any dublication or not, because its an ID and should be unique
data_img['tweet_id'].value_counts()


# In[522]:


#check if there is a null values in tweet id column
print("NULL count of tweet ID is {}".format(data_img['tweet_id'].isnull().sum()))


# **Good News: No null values in tweet ID column.**

# In[523]:


print("count of jpg urls: {}".format(data_img['jpg_url'].count()))


# In[524]:


#print all values count of the name column to check the nature of the data in this coulmn
data_img['jpg_url'].value_counts()


# In[525]:


#check if there is a null values in jpg url column
print("NULL count of tweet ID is {}".format(data_img['jpg_url'].isnull().sum()))


# **Good News: No null values in jpg url column. but some pictures are duplicated**

# **Third**
# 
# *  tweet-json.txt

# In[526]:


#summary of the dataset
tweets_data.info()


# In[527]:


#simple statistics for every column in the dataset
tweets_data.describe()


# In[528]:


#printing sample of the data
tweets_data.head(10)


# In[529]:


print("count of tweet id: {}".format(tweets_data['tweet_id'].count()))


# In[530]:


#print all values count of the name column to check the nature of the data in this coulmn
tweets_data['tweet_id'].value_counts()


# In[531]:


#check if there is a null values in tweet id column
print("NULL count of tweet ID is {}".format(tweets_data['tweet_id'].isnull().sum()))


# **Good News: No null values in tweet ID column.**

# ## Quality
# 
# **Points on the data quality and what needed to be done:**
# 
# * name column has some unrealistic values  that need to be cleaned, "none" and "a".
# * the datatype of timestamp column is object, it should be date.
# * the datatype of created_at column is object, it should be date.
# * the rating numerator is integers, it will be more acurate if it is floating and we have to show the double values that changed to decimal because of the data type.
# * Some values of rating numerator was double(floting) but converted to decimal once we read the csv file so we need to fix this manually.
# * the datatype of tweet_id is int, it should be object.
# * some of the jpg urls are duplicated.
# * the source of the tweet needs to be extracted from source column.
# 
# 
# ## Tidiness
# **What we should do now to have a cleaned data to be used in analysis and visulazation phases:**
# 
# * creating the new column for the dogg stage because the last 4 columns regarding the dogg stage is not easy to analyze, gathering all of it into one new column would be better.
# * dropping unnecessary columns. 
# * merge the 3 data sets so we can work with one cleaned data set.
# 

# ## Cleaning

# **Before we can srart cleaning we have to create 3 new files for the 3 data sets we have**

# In[532]:


#creating new ile for every data set to apply the changes in :
data_csv_new=data_csv.copy()
data_img_new=data_img.copy()
tweets_data_new=tweets_data.copy()


# **Define**
# * name column has some unrelastic vaules that need to be cleaned, "none" and "a".

# In[533]:


#before
print(data_csv_new.query('name in ["None" , "a"]'))


# **Code**

# In[534]:


data_csv_new=data_csv_new.query('name not in ["None" , "a"]')


# **Test**

# In[535]:


#After
print(data_csv_new.query('name in ["None" , "a"]'))


# **Define**
# * the datatype of timestamp column is object, it should be date.

# In[536]:


#Before
data_csv_new.info()


# **Code**

# In[537]:


#using to date pandas function
data_csv_new['timestamp'] = pd.to_datetime(data_csv_new['timestamp'])


# **Test**

# In[538]:


#After
data_csv_new.info()


# **Define**
# * the datatype of created_at column is object, it should be date.

# In[539]:


#Before
tweets_data_new.info()


# **Code**

# In[540]:


tweets_data_new['creat_date'] = pd.to_datetime(tweets_data_new['creat_date']) 


# **Test**

# In[541]:


#After
tweets_data_new.info()


# **Define**
# * the rating numerator is integers, it will be more acurate if it is floating and we have to show the double values that changed to decimal because of the data type.

# In[542]:


#Befor
data_csv_new.info()


# **Code**

# In[543]:


#converting from int to float
data_csv_new.rating_numerator = data_csv_new.rating_numerator.astype(float)
data_csv_new.rating_denominator = data_csv_new.rating_denominator.astype(float)


# **Test**

# In[544]:


#After
data_csv_new.info()


# **Define**
# * ome values of rating numerator was double(floting) but converted to decimal once we read the csv file so we need to fix this manually.

# **Code**

# In[545]:


data_csv_new[data_csv_new.text.str.contains(r"(\d+\.\d*\/\d+)")][['text', 'rating_numerator']]


# In[546]:


#writing the exact flouting rate from the sourse csv file

data_csv_new.loc[(data_csv_new.tweet_id == 883482846933004288), 'rating_numerator'] = 13.5

data_csv_new.loc[(data_csv_new.tweet_id == 832215909146226688), 'rating_numerator'] = 9.75

data_csv_new.loc[(data_csv_new.tweet_id == 786709082849828864), 'rating_numerator'] = 9.75

data_csv_new.loc[(data_csv_new.tweet_id == 778027034220126208), 'rating_numerator'] = 11.27


# **Test**

# In[547]:


#After
data_csv_new[data_csv_new.text.str.contains(r"(\d+\.\d*\/\d+)")][['text', 'rating_numerator']]


# **Define**
# * the datatype of tweet_id is int, it should be object.

# In[548]:


#Before
data_csv_new.info()


# **Code**

# In[549]:


data_csv_new.tweet_id = data_csv_new.tweet_id.astype(object)
data_img_new.tweet_id   = data_img_new.tweet_id.astype(object)
tweets_data_new.tweet_id =  tweets_data_new.tweet_id.astype(object)


# **Test**

# In[550]:


#After
data_csv_new.info()


# **Define**
# * some of the jpg urls are duplicated.

# In[551]:


#Before
data_img_new['jpg_url'].value_counts()


# **Code**

# In[552]:


#remove duplication
data_img_new = data_img_new.drop_duplicates(['jpg_url'], keep='first')


# **Test**

# In[553]:


#After
data_img_new['jpg_url'].value_counts()


# **Define**
# * the source of the tweet needs to be extracted from source column.
# 

# In[554]:


#Before
print(data_csv_new['source'])


# **Code**

# In[555]:


#https://stackoverflow.com/questions/44191658/replace-value-in-pandas
data_csv_new['source'] = data_csv_new['source'].apply(lambda s: re.findall('>(.*)<', s)[0]) 


# **Test**

# In[556]:


#After
print(data_csv_new['source'])


# **Tidiness**
# * creating the new column for the dog stage.

# In[557]:


data_csv_new['stage'] = data_csv_new[data_csv_new.columns[-4:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)

data_csv_new['stage'] = data_csv_new['stage'].map(lambda x: x.lstrip('None,').rstrip(''))

data_csv_new['stage'].unique().tolist()


# In[558]:


tempp={'':"None",
       'doggo,None,None,None':"doggo",
 'puppo':"puppo",
 'pupper,None':"pupper",
 'floofer,None,None':"floofer",
 'doggo,None,pupper,None':"pupper"}

data_csv_new['stage'].replace(tempp, inplace=True)


# In[559]:


data_csv_new['stage'].unique()


# * dropping unnecessary columns. 
# 

# In[560]:


data_img_new.drop(['img_num','p1','p1_conf','p1_dog','p2','p2_conf','p2_dog','p3','p3_conf','p3_dog'],1, inplace=True)
data_csv_new.drop(['retweeted_status_id','in_reply_to_status_id','in_reply_to_user_id','retweeted_status_user_id','retweeted_status_user_id','retweeted_status_timestamp','expanded_urls','puppo','floofer','pupper','doggo'],1, inplace=True)
tweets_data_new.drop(['source'],1, inplace=True)


# In[561]:


data_csv_new.info()
data_img_new.info()
tweets_data_new.info()


# In[562]:


data_sets=[data_csv_new,data_img_new,tweets_data_new]
all_date = reduce(lambda  left,right: pd.merge(left,right,on=['tweet_id'],how='inner'), data_sets)


# In[563]:


all_date.describe()


# In[564]:


all_date.info()


# In[565]:


all_date.head(5)


# In[566]:


Master_data_set =all_date.to_csv('twitter_archive_master.csv')


# ## Analysis and Visualization

# In[567]:


pl.figure(figsize=(9,5), dpi = 100)

pl.xlabel('type of source', fontsize = 13)
pl.ylabel('count of tweets', fontsize=13)
pl.title('Tweet Source', fontsize=13)
pl.hist(all_date['source'], rwidth = 0.8, bins =37, color='red')

pl.show()


# **The most used resouce of tweets is: twitter for iphone**

# In[568]:


fig, axes = pl.subplots(2,figsize = (16,6))
fig.suptitle("rating_numerator Vs (retweet,favorite)",fontsize=14)

sns.regplot(x=all_date['rating_numerator'], y=all_date['retweet_count'],color='c',ax=axes[0])
sns.regplot(x=all_date['rating_numerator'], y=all_date['favorite_count'],color='c',ax=axes[1])

sns.set_style("whitegrid")


# **Once the rating is high both of the retweet and favorate counts will be high too. (Positive relationship)**

# In[569]:


all_date.groupby(all_date["timestamp"].dt.month)['tweet_id'].count().plot.bar(figsize=(14,5),color=(0.2, 0.4, 0.6, 0.6))
pl.xlabel('Month', fontsize = 13)
pl.ylabel('count of tweets', fontsize=13)
pl.title('Month of tweet', fontsize=16)

pl.show()


# **December has the largest number of tweets, folloed by November then January.**

# In[570]:



all_date.groupby(all_date["stage"])['tweet_id'].count().plot.bar(figsize=(14,5),color=(0.9, 0.7, 0.3, 0.8))
pl.xlabel('stage', fontsize = 13)
pl.ylabel('count of tweets', fontsize=13)
pl.title('Count based on stage', fontsize=16)

pl.show()


# **Most of the stages were not inserted in the data set but for the existing once pupper is the most common followed by Dpggo then Puppo then Floofer.**

# In[571]:


all_date.plot( x='retweet_count', y='favorite_count', kind='scatter', figsize=(14,5),color='skyblue')
pl.title('favorites VS retweetS')
pl.xlabel('retweet_count') 
pl.ylabel('favorite_count')


# **December has the largest number of tweets, followed by November then January.**

# ## References : 
# 
# 
# * https://www.pythoncentral.io/introduction-to-tweepy-twitter-for-python/
# * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html
# * https://www.pythonforbeginners.com/requests/using-requests-in-python
# * https://stackoverflow.com/questions/49823631/pythonic-way-of-applying-regex-to-all-columns-of-dataframe
# * https://stackoverflow.com/questions/41681693/pandas-isnull-sum-with-column-headers
# * https://www.geeksforgeeks.org/python-pandas-dataframe-drop_duplicates/
# * https://stackoverflow.com/questions/30164054/raw-string-and-regular-expression-in-python
# * https://python-graph-gallery.com/barplot/
# * https://www.programiz.com/python-programming/methods/list/append
# * https://docs.python.org/2/library/re.html
# * https://stackoverflow.com/questions/33098383/merge-multiple-column-values-into-one-column-in-python-pandas/33098470
# 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




