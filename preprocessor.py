import re
import pandas as pd

def preprocess(data):
    pattern = r'\[\d{2}/\d{2}/\d{2}, \d{2}:\d{2}:\d{2}\]'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create the DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean and convert 'message_date'
    df['message_date'] = df['message_date'].str.strip('[]')
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M:%S')

    # Rename column
    df.rename(columns={'message_date': 'date_time'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # Check if entry has at least 2 values after splitting
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    # Drop 'user_message' column if no longer needed
    df.drop(columns=['user_message'], inplace=True)

    # Add additional datetime columns
    df['day_name'] = df['date_time'].dt.day_name()
    df['only_date'] = df['date_time'].dt.date
    df['year'] = df['date_time'].dt.year
    df['month_num'] = df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
