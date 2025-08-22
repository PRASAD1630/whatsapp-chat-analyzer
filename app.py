import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("📊 WhatsApp Chat Analyzer")
st.sidebar.title("Upload Your Chat")

# ------------------------
# Upload file
# ------------------------
uploaded_file = st.file_uploader("Choose your WhatsApp chat (.txt)", type=["txt"])

if uploaded_file is not None:
    # Read file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocess
    df = preprocessor.preprocess(data)

    if df.empty:
        st.warning("No valid messages found in the uploaded chat!")
    else:
        st.dataframe(df.head(50))  # Show first 50 rows

        # Users list
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")
        selected_user = st.sidebar.selectbox("Show analysis for", user_list)

        if st.sidebar.button("Show Analysis"):

            # ------------------------
            # 1. Basic Stats
            # ------------------------
            num_messages, num_words, num_media = helper.fetch_stats(selected_user, df)
            num_links, all_links = helper.fetch_link_stats(selected_user, df)
            num_emojis, top_emojis = helper.fetch_emoji_stats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Messages", num_messages)
            col2.metric("Total Words", num_words)
            col3.metric("Media Shared", num_media)
            col4.metric("Links Shared", num_links)

            # ------------------------
            # 2. Most Busy Users
            # ------------------------
            if selected_user == "Overall":
                st.header("Most Active Users")
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='skyblue')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                st.dataframe(new_df)

            # ------------------------
            # 3. WordCloud
            # ------------------------
            st.header("Word Cloud")
            wc = helper.create_wordcloud(selected_user, df)
            if wc:
                fig, ax = plt.subplots()
                ax.imshow(wc)
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.info("No text available to generate WordCloud.")

            # ------------------------
            # 4. Most Common Words
            # ------------------------
            st.header("Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            if not most_common_df.empty:
                fig, ax = plt.subplots()
                ax.barh(most_common_df['word'], most_common_df['count'], color='purple')
                ax.invert_yaxis()
                st.pyplot(fig)
            else:
                st.info("No words found to display.")

            # ------------------------
            # 5. Emoji Stats
            # ------------------------
            st.header("Top Emojis Used")
            if top_emojis:
                st.table(top_emojis)
            else:
                st.info("No emojis found.")

            # ------------------------
            # 6. Shared Links
            # ------------------------
            if all_links:
                st.header("Shared Links")
                st.dataframe(all_links)
            else:
                st.info("No links found.")

            # ------------------------
            # 7. Daily Timeline
            # ------------------------
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            if not daily_timeline.empty:
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['date'], daily_timeline['message'], color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # ------------------------
            # 8. Monthly Timeline
            # ------------------------
            st.header("Monthly Timeline")
            monthly_timeline = helper.monthly_activity_map(selected_user, df)
            if not monthly_timeline.empty:
                fig, ax = plt.subplots()
                ax.plot(monthly_timeline['month'], monthly_timeline['message'], color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # ------------------------
            # 9. Weekly Activity
            # ------------------------
            st.header("Weekly Activity")
            week_activity = helper.weekly_activity_map(selected_user, df)
            if not week_activity.empty:
                fig, ax = plt.subplots()
                ax.bar(week_activity.index, week_activity.values, color='teal')
                plt.xticks(rotation='horizontal')
                st.pyplot(fig)

            # ------------------------
            # 10. Activity Heatmap
            # ------------------------
            st.header("Weekly Activity Heatmap")
            heatmap_data = helper.activity_heatmap(selected_user, df)
            if not heatmap_data.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(heatmap_data, ax=ax)
                st.pyplot(fig)
            else:
                st.info("Not enough data for heatmap.")
