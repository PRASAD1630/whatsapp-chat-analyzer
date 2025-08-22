import re
import pandas as pd

def preprocess(data):
    # Define regex pattern to match WhatsApp message lines
    pattern = r'(\d{1,2}/\d{1,2}/\d{4}),\s(\d{1,2}:\d{2}\u202f?[ap]m)\s-\s(.*?):\s(.*)'
    matches = re.findall(pattern, data)

    # Build DataFrame
    parsed_data = []
    for date, time, author, message in matches:
        parsed_data.append([date, time, author, message])

    df = pd.DataFrame(parsed_data, columns=['date', 'time', 'user', 'message'])

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Extract time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['time'] = df['time'].str.replace('\u202f', '')  # remove narrow no-break space
    df['hour'] = pd.to_datetime(df['time'], format='%I:%M%p').dt.hour
    df['minute'] = pd.to_datetime(df['time'], format='%I:%M%p').dt.minute

    return df
