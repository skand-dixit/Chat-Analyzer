from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
# Basic Statistics
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    # fetching the total number of message
    num_messages = df.shape[0]
    # fetching the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())
    # fetching the total number of media
    num_media = df[df["Message"]=="<Media omitted>\n"].shape[0]
    # fetching the total number of links
    links = []
    for message in df["Message"]:
        links.extend(extract.find_urls(message))
    
    return num_messages , len(words), num_media,len(links)

# Fetching Busiest User
def busy_user(df):
    x = df['User'].value_counts().head()
    df = (df['User'].value_counts() / df.shape[0] * 100).round(2).reset_index()
    df.rename(columns={'count': 'Percent'}, inplace=True)
    return x,df
    
# Fetching Word Cloud
def wordcloud(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    temp = df[df['User']!= 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)   
        return " ".join(y) 
        
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep = " "))
    return df_wc
    
# Fetching Most common Used Word
def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
        
    temp = df[df['User']!= 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    
    words = []
    
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

# Fetching Most common used Emoji and its % of use using Pie Chart
def emoji_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]   
        
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df 


# Fetching Daily timeline
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('Only_Date').count()['Message'].reset_index()

    return daily_timeline

# Fetching Weekly activity Map
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()

# Fetching Monthly activity Map
def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

#fetching Heatmap
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap