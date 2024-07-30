import numpy as np
import pandas as pd

def medal_telly_f(df):
    medal_tally = df.drop_duplicates(subset= ['Team', 'NOC', 'Games','Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally =medal_tally.groupby('NOC').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze'] 
    return medal_tally
  
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset= ['Team', 'NOC', 'Games','Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    if flag == 1:
        end_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending = True).reset_index()
    else:
        end_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    end_df['Total'] = end_df['Gold']+end_df['Silver']+end_df['Bronze']
    return end_df

def participating_nations_over_time(df):
    nation_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns= {'index': 'Edition', 'Year': 'No of countries'}, inplace = True)
    return nation_over_time

def data_over_time(df, col):
    nation_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nation_over_time.rename(columns= {'index': 'Edition', 'Year': col}, inplace = True)
    return nation_over_time

def most_succesful(df, sport):
    temp_df = df.dropna(subset = ['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        x = temp_df['Name'].value_counts().reset_index()
        x.rename(columns={'index':'Name', 'Name': 'Medals'}, inplace = True)
        x = pd.merge(x, temp_df, on = 'Name', how= 'left') 
        new_one = x.drop_duplicates(subset= ['Name', 'Medals'])
        new_one.rename(columns = {'region':'Country'}, inplace = True)
        return new_one.head(20)[['Name', 'Medals', 'Country']]
    
    else:
        x =temp_df['Name'].value_counts().reset_index()
        x.rename(columns={'index':'Name', 'Name': 'Medals'}, inplace=True)
        x = pd.merge(x, temp_df, on = 'Name', how= 'left') 
        new_one = x.drop_duplicates(subset= ['Name', 'Medals'])
        new_one.rename(columns = {'region':'Country'}, inplace = True)
        return new_one.head(20)[['Name', 'Medals', 'Country']]

def country_year_wise_tally(df, country):
    temp_df = df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace = True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_heatmap(df, country):
    temp_df = df.dropna(subset= ['Medal'])
    temp_df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace = True)

    new_df = temp_df[temp_df['region'] == country]
    pivot_table = new_df.pivot_table(index = 'Sport', columns='Year', values= 'Medal', aggfunc='count').fillna(0)
    return pivot_table

def country_best_performer(df, country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index()
    x.rename(columns={'index':'Name', 'Name': 'Medal'}, inplace = True)
    x = pd.merge(x, temp_df, on = 'Name', how= 'left')
    new_one = x.drop_duplicates(subset= ['Name','Medal_x'])
    new_one.rename(columns = {'Medal_x':'Medals'}, inplace = True)

    return new_one.head(10)[['Name', 'Medals']]

def athlete_vs_height(df, sport):
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace = True)

    temp_df1 = athlete_df[athlete_df['Sport'] == sport] 
    return temp_df1

def male_vs_female_participation(df):
    athlete_df = df.drop_duplicates(subset = ['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = pd.merge(men, female, on = 'Year', how= 'left')
    final.rename(columns={'Name_x':'Male', 'Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace= True)

    return final

