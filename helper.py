import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import string
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

# ------------------------
# BASIC STATS
# ------------------------
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    num_words = sum([len(str(msg).split()) for msg in df['message']])
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    return num_messages, num_words, num_media_messages

# ------------------------
# MOST BUSY USERS
# ------------------------
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x, df_percent

# ------------------------
# WORD CLOUD
# ------------------------
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    df = df[df['message'] != '<Media omitted>']
    df = df[df['message'] != 'This message was deleted']
    text = " ".join(df['message'].astype(str))
    if not text.strip():
        return None
    wc = WordCloud(width=500, height=500, min_font_size=18, background_color='white').generate(text)
    return wc

# ------------------------
# MOST COMMON WORDS
# ------------------------
def most_common_words(selected_user, df, top_n=20):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    df = df[df['message'] != '<Media omitted>']
    df = df[df['message'] != 'This message was deleted']

    words = []
    for message in df['message']:
        message = re.sub(r"http\S+", "", str(message))
        for word in message.lower().split():
            word = word.strip(string.punctuation)
            if word and word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(top_n), columns=['word','count'])
    return most_common_df

# ------------------------
# LINK STATS
# ------------------------
def fetch_link_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    messages = " ".join(df['message'].astype(str))
    urls = re.findall(r'https?://\S+', messages)
    return len(urls), urls

# ------------------------
# EMOJI STATS
# ------------------------
def fetch_emoji_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    messages = " ".join(df['message'].astype(str))
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002700-\U000027BF"
                               u"\U0001F900-\U0001F9FF"
                               "]+", flags=re.UNICODE)
    emojis_found = emoji_pattern.findall(messages)
    emoji_counter = Counter(emojis_found)
    return sum(emoji_counter.values()), emoji_counter.most_common(10)

# ------------------------
# TIMELINES
# ------------------------
def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    if df.empty:
        return pd.DataFrame(columns=['date','message'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    daily = df.groupby('date').count()['message'].reset_index()
    return daily

def monthly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user']==selected_user]
    if df.empty:
        return pd.DataFrame(columns=['month','message'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month').count()['message'].reset_index()
    monthly['month'] = monthly['month'].astype(str)
    return monthly

# ------------------------
# WEEKLY ACTIVITY
# ------------------------
def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    if df.empty:
        return pd.Series(dtype=int)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()

# ------------------------
# HEATMAP
# ------------------------
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    if df.empty:
        return pd.DataFrame()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    pivot = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
    return pivot
