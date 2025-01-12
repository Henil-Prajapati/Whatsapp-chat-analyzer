import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


from helper import most_common_words, daily_timeline

st.sidebar.subheader('Whatsapp Chat Analyzer')
st.title('Exported chat details')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.write(df)


    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove(' D2D SEM-5')
    user_list.sort()
    user_list.insert(0, "Overall")  # Group-level Analysis

    selected_user = st.sidebar.selectbox("Show analysis with respect to users", user_list)

    if st.sidebar.button("Show Analysis"):
        #state area
        num_messages, words , num_image_messages , num_document_message , num_links = helper.fetch_states(selected_user, df)
        st.title("Top Statistics")
        col1, col2 ,col3 , col4 , col5= st.columns(5)


        with col1:

            st.header("Total Msg")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_image_messages)

        with col4:
            st.header("document")
            st.title(num_document_message)

        with col5:
            st.header("links shared")
            st.title(num_links)


        #Monthly_timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user , df)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(timeline['time'], timeline['message'] , color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily timeline")
        daily_timeline  = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation= 40)
        st.pyplot(fig)

        #Daily_activity

        st.title("Activity map")
        col1 , col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index , busy_day.values, color='blue')
            plt.xticks(rotation= 45)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(8, 7))
            ax.bar(busy_month.index, busy_month.values, color='orange')
            st.pyplot(fig)


        #activity heatmap
        st.title("Weekly activity map")

        activity_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(activity_heatmap, annot=True, cmap='YlGnBu', ax=ax)
        st.pyplot(fig)



        #find the busiest users in the group(Group Level)
        if selected_user == "Overall":
            st.title("Most busy users")
            x , new_df = helper.most_busy_users(df)
            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values , color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig , ax  = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig , ax = plt.subplots()
        plt.xticks(rotation = 'vertical')
        ax.barh(most_common_df['Word'], most_common_df['Frequency'] , color = 'green')
        st.pyplot(fig)


        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig , ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)

