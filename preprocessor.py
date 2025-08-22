import re
import pandas as pd

def preprocess(data):
    """
    Preprocess WhatsApp chat text into a DataFrame.
    Works with most WhatsApp export formats.
    """

    # Regex pattern to match WhatsApp messages
    pattern = r'(\d{1,2}/\d{1,2}/\d{4}),\s(\d{1,2}:\d{2}\s?[apAP][mM])\s-\s(.*?):\s(.*)'
    matches = re.findall(pattern, data)

    parsed_data = []
    for date, time, user, message in matches:
        parsed_data.append([date, time, user, message])

    df = pd.DataFrame(parsed_data, columns=['date', 'time', 'user', 'message'])

    if df.empty:
        return df  # Return empty DataFrame if no matches

    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    # Extract additional time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day

    # Clean and convert time
    df['time'] = df['time'].str.replace('\u202f', '', regex=False)  # remove narrow no-break space
    df['hour'] = pd.to_datetime(df['time'], format='%I:%M%p', errors='coerce').dt.hour
    df['minute'] = pd.to_datetime(df['time'], format='%I:%M%p', errors='coerce').dt.minute

    return df
