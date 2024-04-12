import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import functions


st.set_page_config(page_title="Whatsapp Chat Analyzer", page_icon="whatsapp.ico",layout="wide")
st.title("Whatsapp Chat Analyzer")
st.text("Upload your Whatsapp Chat file in 24-Hour time format")
# st.sidebar.title("Upload File")

uploaded_file = st.file_uploader("Chose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)
    
    # featching users
    user_list = df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.selectbox("Select User",user_list)
    
    if st.button("Start"):
        num_messages , words ,num_media, links= functions.fetch_stats(selected_user,df)
        
        with st.container():
            col1 , col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)    
            with col3:
                st.header("Total Media")
                st.title(num_media) 
            with col4:
                st.header("Total Links")
                st.title(links) 
                
            if selected_user == 'Overall':
                st.title("Most Busy User")
                x , new_df = functions.busy_user(df)
                fig , ax = plt.subplots()
                
                col1, col2 = st.columns(2)
                with col1:
                    ax.bar(x.index,x.values)
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)    
                with col2:
                    st.dataframe(new_df,width=500, height=400)
            
            # Word Cloud
            st.title("Word Cloud")   
            df_wc = functions.wordcloud(selected_user, df)
            fig , ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
            
            # most common words
            st.title("Most Common Words")
            most_common = functions.most_common_words(selected_user,df)
            fig,ax = plt.subplots()
            ax.barh(most_common[0],most_common[1])
            plt.xticks(rotation='vertical')
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(most_common,width=500, height=500)  
            with col2:
                st.pyplot(fig)
            
            # Emoji Stats
            st.title("Emoji Stats")
            emoji_df = functions.emoji_stats(selected_user,df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df,width=500, height=500)  
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels = emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
            
            # DAily Timeline
            st.title("Daily Timeline")
            daily_timeline = functions.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['Only_Date'], daily_timeline['Message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = functions.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = functions.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Fetching heatmap
            st.title("Weekly Activity Map")
            user_heatmap = functions.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
            
            