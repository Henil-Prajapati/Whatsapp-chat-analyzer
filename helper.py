from urlextract import URLExtract
import wordcloud
import pandas as pd
from collections import Counter
import emoji

# Initialize URL extractor
extract = URLExtract()

def fetch_states(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the number of total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of image messages (using substring match for "image omitted")
    num_image_message = df[df['message'].str.contains('image omitted', na=False)].shape[0]

    # Fetch the number of document messages
    num_document_message = df[df['message'].str.contains('document omitted', na=False)].shape[0]

    # Fetch the number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_image_message, num_document_message, len(links)


def most_busy_users(df):
    # Check if 'user' column exists
    if 'user' not in df.columns:
        raise ValueError("The 'user' column is missing from the DataFrame. Please check preprocessing.")

    # Calculate the most busy users
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'count': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = wordcloud.WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    #here in below code we are doing filtering as well as stop_words
    # Filter out specific rows

    temp = df[df['user'] != 'd2d sem-5']
    temp = temp[temp['message'] != '<image omitted>\n']

    # Load stopwords with utf-8 encoding
    with open('gujarati_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    # Define additional words to avoid
    avoid_words = {'‎', 'het', 'ane', 'che', 'hai', 'kya', 'na', 'hu', 'ke', 'te', '😂', 'ā', 'ma', 'to', 'su', 'ne',
                   '2', 'nahi', 'na', 'nai', '.', 'not', 'ommitted', 'che', 'to', 'e', 'jo', 'maṭe', 'kāraṇ', 'paṇ',
                   'nahi', 'to', 'pachī', 'thī', 'sudhī', 'shu', 'huṁ', 'tame', 'tamāre', 'tamāro', 'apṇuṁ', 'apṇī',
                   'apṇā', 'ena', 'ene', 'enā', 'āvā', 'āvī', 'āve', 'āvyo', 'kyā', 'kyāre', 'kām', 'kāṭho', 'kāḷā',
                   'kāḷī', 'kāṭhe', 'kārṇā', 'kar', 'kari', 'kare', 'karyo', 'karine', 'karvā', 'karavā', 'karīne',
                   'kariyā', 'kariyāṭhe', 'kariyāṭho', 'sāruṁ', 'sāri', 'sāryo', 'sāryuṁ', 'sāra', 'sāryā', 'sārye',
                   'sāryī', 'sāryaṇuṁ', 'sāryāchhe', 'sāryāṭho', 'sāryāṭhe', 'sāryoṭī', 'sāroṭuṁ', 'sāroṭī', 'bāḷak',
                   'bāḷako', 'bāḷakne', 'bāḷaknā', 'pīluṁ', 'pīlā', 'pīlāo', 'pīlānī', 'pīlānā', 'tamām', 'saru',
                   'vadhu', 'vāḍā', 'vāḍī', 'vāḍāṁ', 'vāḍho', 'vāḍhī', 'vāḍī', 'vāḍhīne', 'vāḍhiyā', 'vāḍhyā',
                   'vāḍāṇuṁ', 'vāḍyā', 'vāḍyāchhe', 'vāḍāṭī', 'vāḍāṭhe', 'vāḍāṭho', 'vāḍāṭīchhe', 'vāḍāṭīne',
                   'vāḍāṭīnā', 'vāḍāṭīnuṁ', 'vāḍāṭīnāthī', 'vāḍāṭīnāne', 'vāḍāṭīnāchoṭuṁ', 'vāḍāṭīnāchoṭe',
                   'vāḍāṭīnāchoṭā', 'vāḍāṭīnāchoṭe', 'vāḍāṭīnāchoṭāchhe', 'vāḍāṭīnāchoṭāthī', 'toh', '  <this ', 'ae',
                   'badha', 'me', 'ala', 'meh', 'kai', 'tu', 'koi', 'aa', 'ek', 'ha', 'kale', 'nathi', 'pan', 'te',
                   'vāḍāṭīnāchoṭāyāchhe', 'vāḍāṭīnā', 'thi', 'ni', 'and', '•', 'j', 'bhai'}

    # Initialize an empty list to store words
    words = []

    # Process each message in the filtered DataFrame
    for message in temp['message']:
        for word in message.lower().split():
            # Check if word is not a stop word and not in avoid_words list
            if word not in stop_words and word not in avoid_words:
                words.append(word)
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc




def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out specific rows
    temp = df[df['user'] != 'd2d sem-5']
    temp = temp[temp['message'] != '<image omitted>\n']

    # Load stopwords with utf-8 encoding
    with open('gujarati_stopwords.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().splitlines()

    # Define additional words to avoid
    avoid_words = {'‎', 'het', 'ane', 'che', 'hai', 'kya', 'na', 'hu', 'ke', 'te', '😂', 'ā', 'ma', 'to', 'su', 'ne',
                   '2', 'nahi', 'na', 'nai', '.', 'not', 'ommitted', 'che', 'to', 'e', 'jo', 'maṭe', 'kāraṇ', 'paṇ',
                   'nahi', 'to', 'pachī', 'thī', 'sudhī', 'shu', 'huṁ', 'tame', 'tamāre', 'tamāro', 'apṇuṁ', 'apṇī',
                   'apṇā', 'ena', 'ene', 'enā', 'āvā', 'āvī', 'āve', 'āvyo', 'kyā', 'kyāre', 'kām', 'kāṭho', 'kāḷā',
                   'kāḷī', 'kāṭhe', 'kārṇā', 'kar', 'kari', 'kare', 'karyo', 'karine', 'karvā', 'karavā', 'karīne',
                   'kariyā', 'kariyāṭhe', 'kariyāṭho', 'sāruṁ', 'sāri', 'sāryo', 'sāryuṁ', 'sāra', 'sāryā', 'sārye',
                   'sāryī', 'sāryaṇuṁ', 'sāryāchhe', 'sāryāṭho', 'sāryāṭhe', 'sāryoṭī', 'sāroṭuṁ', 'sāroṭī', 'bāḷak',
                   'bāḷako', 'bāḷakne', 'bāḷaknā', 'pīluṁ', 'pīlā', 'pīlāo', 'pīlānī', 'pīlānā', 'tamām', 'saru',
                   'vadhu', 'vāḍā', 'vāḍī', 'vāḍāṁ', 'vāḍho', 'vāḍhī', 'vāḍī', 'vāḍhīne', 'vāḍhiyā', 'vāḍhyā',
                   'vāḍāṇuṁ', 'vāḍyā', 'vāḍyāchhe', 'vāḍāṭī', 'vāḍāṭhe', 'vāḍāṭho', 'vāḍāṭīchhe', 'vāḍāṭīne',
                   'vāḍāṭīnā', 'vāḍāṭīnuṁ', 'vāḍāṭīnāthī', 'vāḍāṭīnāne', 'vāḍāṭīnāchoṭuṁ', 'vāḍāṭīnāchoṭe',
                   'vāḍāṭīnāchoṭā', 'vāḍāṭīnāchoṭe', 'vāḍāṭīnāchoṭāchhe', 'vāḍāṭīnāchoṭāthī', 'toh', '  <this ', 'ae',
                   'badha', 'me', 'ala', 'meh', 'kai', 'tu', 'koi', 'aa', 'ek', 'ha', 'kale', 'nathi', 'pan', 'te',
                   'vāḍāṭīnāchoṭāyāchhe', 'vāḍāṭīnā', 'thi', 'ni', 'and', '•', 'j', 'bhai'}

    # Initialize an empty list to store words
    words = []

    # Process each message in the filtered DataFrame
    for message in temp['message']:
        for word in message.lower().split():
            # Check if word is not a stop word and not in avoid_words list
            if word not in stop_words and word not in avoid_words:
                words.append(word)

    # Count word frequencies
    word_counts = Counter(words)

    # Convert to DataFrame for better display
    most_common_df = pd.DataFrame(word_counts.most_common(20), columns=['Word', 'Frequency'])
    return most_common_df



def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:  # Replace 'message' with the actual column name containing text
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_dict = {e: emojis.count(e) for e in set(emojis)}
    emoji_df = pd.DataFrame(emoji_dict.items(), columns=['Emoji', 'Count']).sort_values(by='Count', ascending=False)
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Convert 'date' to datetime if it isn't already
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')

    # Extract 'month' and 'year' from the 'date' column
    df['month'] = df['date_time'].dt.month
    df['year'] = df['date_time'].dt.year

    # Group by 'year' and 'month'
    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    # Create a 'time' column in the format 'month-year'
    timeline['time'] = timeline['month'].astype(str) + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    day_count = df['day_name'].value_counts()
    return day_count

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    pivot_table = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count')
    return pivot_table
