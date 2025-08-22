import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import string

# ------------------------
# BASIC STATS
# ------------------------
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    words = []
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    for message in df['message']:
        words.extend(message.split())

    return len(words), num_media_messages

# ------------------------
# MOST BUSY USERS
# ------------------------
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df_percent

# ------------------------
# WORD CLOUD
# ------------------------
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message'] != '<Media omitted>']
    df = df[df['message'] != 'This message was deleted']

    text = ' '.join(df['message'].astype(str))

    wc = WordCloud(width=500, height=500, min_font_size=18, background_color='white')
    wordcloud = wc.generate(text)

    return wordcloud

# ------------------------
# MOST COMMON WORDS
# ------------------------
import nltk
from nltk.corpus import stopwords

# Download stopwords once
nltk.download('stopwords')

# Use stopwords from NLTK
stop_words = set(stopwords.words('english'))


# MOST COMMON WORDS
# ------------------------
def most_common_words(selected_user, df, top_n=20):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message'] != '<Media omitted>']
    df = df[df['message'] != 'This message was deleted']

    words = []

    for message in df['message']:
        message = re.sub(r"http\S+", "", message)  # remove URLs
        for word in message.lower().split():
            word = word.strip(string.punctuation)
            if word and word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(top_n), columns=['word', 'count'])
    return most_common_df


# ------------------------
# LINK STATS
# ------------------------
def fetch_link_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    messages = " ".join(df['message'].tolist())
    url_pattern = r'https?://\S+'
    urls = re.findall(url_pattern, messages)
    return len(urls), urls

# ------------------------
# EMOJI STATS
# ------------------------
def fetch_emoji_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    messages = " ".join(df['message'].tolist())

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

def most_common_emojis(selected_user, df, top_n=10):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    messages = " ".join(df['message'].tolist())

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
    return emoji_counter.most_common(top_n)

# ------------------------
# TIMELINES
# ------------------------
def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    daily = df.groupby('date').count()['message'].reset_index()
    return daily

def monthly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    monthly = df.groupby('month').count()['message'].reset_index()
    return monthly

# ------------------------
# WEEKLY ACTIVITY
# ------------------------
def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Ensure 'date' is datetime and 'day_name' is created
    df['day_name'] = df['date'].dt.day_name()

    return df['day_name'].value_counts()


# ------------------------
# HEATMAP
# ------------------------
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Create required columns
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour

    pivot = df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
    return pivot











