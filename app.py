import streamlit as st
import pandas as pd
import preprocessor, helper, Overall_Analysis
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df=df, region_df=region_df)

st.sidebar.image('Olympic_image.jfif')
st.sidebar.header("OLYMPIC ANALYSIS")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis','Athlete wise Analysis')

)

#st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    year, country = helper.country_year_list(df)
    # Dropdown bar for country and years
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df=df, year=selected_year, country=selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "Overall Performace")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year)+ " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    editions, cities, sports, events, athletes, nations = Overall_Analysis.analysis(df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)       
    with col3:
        st.header("Countries")
        st.title(nations)


    nations_over_time = helper.data_over_time(df, col='region')
    st.title("Graph1")

    fig = plt.figure()
    plt.plot(nations_over_time['Edition'], nations_over_time['region'])
    plt.xlabel("Years")
    plt.ylabel("Number of Countries")
    st.pyplot(fig)

    #------------#
    event_over_time = helper.data_over_time(df, col = 'Event')
    st.title("Graph2")

    fig = plt.figure()
    plt.plot(event_over_time['Edition'], event_over_time['Event'], color= 'orange')
    plt.xlabel("Years")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

    #-------------#

    athlete_over_time = helper.data_over_time(df, col = 'Name')
    st.title("Graph3")

    fig = plt.figure()
    plt.plot(athlete_over_time['Edition'], athlete_over_time['Name'], color= 'blue')
    plt.xlabel("Years")
    plt.ylabel("Number of Players")
    st.pyplot(fig)

    #----------------#

    st.title("TOP 20 Most Successful Athlete")
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sports_list)
    sport_to_show = helper.most_succesful(df, selected_sport)
    st.table(sport_to_show)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Country's Year-wise Medal Count")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.country_year_wise_tally(df, selected_country)

    fig = plt.figure()
    plt.plot(country_df['Year'], country_df['Medal'], color='green')
    plt.xlabel('Year')
    plt.ylabel(selected_country+' Medal Count')
    st.pyplot(fig)

    
    # Generating a heatmap
    st.title("Heatmap of " + selected_country+ " (Medal Count)")
    pt = helper.country_heatmap(df, selected_country)

    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    top10_df = helper.country_best_performer(df, selected_country)
    st.title(selected_country + "'s Top 10 Performers")
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    st.title("Distribution of Age")
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])

    overall_age = athlete_df['Age'].dropna()
    gold_dist = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_dist = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_dist = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([overall_age, gold_dist, silver_dist, bronze_dist],
                         ['Overall_Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                         show_hist=False, show_rug=False )
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)

    #--------------#

    st.title('Medals Analysis wrt Weight and Height')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()

    selected_sport = st.selectbox('Select a Sport', sports_list)
    temp_df = helper.athlete_vs_height(df, selected_sport)
    fig, ax = plt.subplots()
    sns.scatterplot(x = temp_df['Weight'],y= temp_df['Height'],
                    hue = temp_df['Medal'],
                    style= temp_df['Sex'],
                    s = 60)
    st.pyplot(fig)

    #------------#
    st.title("Male vs Female Participation")
    final = helper.male_vs_female_participation(df)

    fig = plt.figure()
    plt.plot(final['Year'], final['Male'])
    plt.plot(final['Year'],final['Female'])
    plt.legend(["Male", "Female"], loc="lower right")
    plt.xlabel("Years")
    plt.ylabel("Participants")
    st.pyplot(fig)

    
    
