import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Choose your WhatsApp chat (.txt)", type=["txt"])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis for", user_list)

    if st.sidebar.button("Show Analysis"):

        # 1. Basic Stats
        num_messages = helper.fetch_stats(selected_user, df)
        media_messages = df[df['message'] == '<Media omitted>']
        if selected_user != "Overall":
            media_messages = media_messages[media_messages['user'] == selected_user]
        num_media_messages = media_messages.shape[0]

        num_links, all_links = helper.fetch_link_stats(selected_user, df)
        num_emojis, top_emojis = helper.fetch_emoji_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_messages[0])
        with col2:
            st.metric("Media Shared", num_media_messages)
        with col3:
            st.metric("Links Shared", num_links)
        with col4:
            st.metric("Emojis Used", num_emojis)

        # 2. Most Busy Users (Only for Overall)
        if selected_user == "Overall":
            st.header("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values, color='skyblue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.dataframe(new_df)

        # 3. Wordcloud
        st.header("Word Cloud")
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # 4. Top Words
        st.header("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        # Example: Assuming most_common_df has columns 'word' and 'count'
        ax.barh(most_common_df['word'], most_common_df['count'], color='purple')

        plt.xticks(rotation='horizontal')
        st.pyplot(fig)

        # 5. Emoji Table
        st.header("Top Emojis Used")
        if top_emojis:
            st.table(top_emojis)
        else:
            st.write("No emojis found.")

        # 6. Links
        if all_links:
            st.header("Shared Links")
            st.dataframe(all_links)

        # 7. Daily Timeline
        st.header("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # 8. Monthly Timeline
        st.header("Monthly Timeline")
        monthly_timeline = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['month'], monthly_timeline['message'], color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # 9. Activity Map - Day of Week
        st.header("Weekly Activity")
        week_activity = helper.weekly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(week_activity.index, week_activity.values, color='teal')
        plt.xticks(rotation='horizontal')
        st.pyplot(fig)

        # 10. Activity Map - Monthly
        st.header("Day-wise Activity")
        day_activity = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(day_activity['month'], day_activity['message'], color='crimson')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # 11. Heatmap
        st.header("Weekly Activity Heatmap")
        heatmap_data = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, ax=ax)
        st.pyplot(fig)












