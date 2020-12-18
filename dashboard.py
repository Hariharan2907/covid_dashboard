import streamlit as st
import pandas as pd
import altair as alt
import datetime 
import calendar 
import os
port = int(os.environ.get("PORT", 5000))
pd.set_option('mode.chained_assignment', None)
st.cache(persist=True)
url="https://data.cdc.gov/api/views/muzy-jte6/rows.csv?accessType=DOWNLOAD" #dataset
#function for loading data
def load_data():
    df_filter=pd.read_csv(url,error_bad_lines=False, usecols=["Jurisdiction of Occurrence","MMWR Year","MMWR Week","Week Ending Date","All Cause","COVID-19 (U071, Multiple Cause of Death)","COVID-19 (U071, Underlying Cause of Death)"])
    return df_filter
df_filter = load_data()

pop = pd.read_csv("Population.csv") #population for each state
us_pop = 328239523

st.title("All Cause Deaths and COVID-19 Deaths in the United States for 2019-2020")
st.markdown("-----")


#Cleaning data
merged = pd.merge(df_filter,pop,left_on='Jurisdiction of Occurrence', right_on = 'States')
merged['month'] = pd.DatetimeIndex(merged['Week Ending Date']).month
merged['month_name'] = merged['month'].apply(lambda x: calendar.month_abbr[x])
merged['date'] = pd.DatetimeIndex(merged['Week Ending Date']).date
merged['date'] = pd.to_datetime(merged['date'],format = '%Y-%m-%d')
merged['MMWR Year'] = merged['date'].dt.year
merged['MM-DD'] = merged['date'].dt.strftime('%m-%d')
merged['COVID-19 (U071, Multiple Cause of Death)'] = merged['COVID-19 (U071, Multiple Cause of Death)'].fillna(0)
merged['COVID-19 (U071, Underlying Cause of Death)'] = merged['COVID-19 (U071, Underlying Cause of Death)'].fillna(0)
merged['Population'] = merged['Population'].str.replace(',','').astype(float)
merged['capita_allcause'] = (merged['All Cause']/merged['Population']) * 1000
merged['capita_covid'] = (merged['COVID-19 (U071, Multiple Cause of Death)']/merged['Population']) * 1000

#United States dataframe 
us_df = df_filter[df_filter['Jurisdiction of Occurrence']=='United States']
us_df['Population'] = 328239523
us_df['Capita'] = (us_df['All Cause']/us_df['Population']) * 1000
us_df['Capita_COVID'] = (us_df['COVID-19 (U071, Multiple Cause of Death)']/us_df['Population']) * 1000
us_df['date'] = pd.DatetimeIndex(us_df['Week Ending Date']).date
us_df['date'] = pd.to_datetime(us_df['date'],format = '%Y-%m-%d')
us_df['MMWR Year'] = us_df['date'].dt.year
us_df['MM-DD'] = us_df['date'].dt.strftime('%m-%d')
us_df['month'] = pd.DatetimeIndex(us_df['Week Ending Date']).month
us_df['month_name'] = us_df['month'].apply(lambda x: calendar.month_abbr[x])
us_df_rem = us_df.tail(6)
us_df.drop(us_df.tail(5).index,inplace=True)


#Graphs for entire United States
#All Cause Death graph - USA
st.header("All Cause Deaths for the United States of America")
us_allcause = alt.Chart(us_df,width=1000,height=400).transform_fold(['MMWR Year']).mark_line().encode(
    x=alt.X('MMWR Week', axis = alt.Axis(title='Week Number')),
    y=alt.Y('Capita', axis = alt.Axis(title = 'Capita per 1000')),
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()


us_allcause1 = alt.Chart(us_df,width=1000,height=400).transform_fold(['MMWR Year']).mark_circle().encode(
    x='MMWR Week',
    y='Capita',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

us_allcause2 = alt.Chart(us_df_rem,width=1000,height=400).transform_fold(['MMWR Year']).mark_line(strokeDash=[5,5]).encode(
    x='MMWR Week',
    y='Capita',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

us_allcause3 = alt.Chart(us_df_rem,width=1000,height=400).transform_fold(['MMWR Year']).mark_circle().encode(
    x='MMWR Week',
    y='Capita',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()
st.altair_chart(us_allcause+us_allcause1 + us_allcause2 + us_allcause3)

#COVID-19 Death graph - USA
st.header("COVID-19 Deaths for the United States of America")
us_covid = alt.Chart(us_df,width=1000,height=400).transform_fold(['MMWR Year']).mark_line().encode(
    x=alt.X('MMWR Week', axis = alt.Axis(title='Week Number')),
    y=alt.Y('Capita_COVID', axis = alt.Axis(title = 'Capita per 1000')),
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()


us_covid1 = alt.Chart(us_df,width=1000,height=400).transform_fold(['MMWR Year']).mark_circle().encode(
    x='MMWR Week',
    y='Capita_COVID',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()

us_covid2 = alt.Chart(us_df_rem,width=1000,height=400).transform_fold(['MMWR Year']).mark_line(strokeDash=[5,5]).encode(
    x='MMWR Week',
    y='Capita_COVID',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

us_covid3 = alt.Chart(us_df_rem,width=1000,height=400).transform_fold(['MMWR Year']).mark_circle().encode(
    x='MMWR Week',
    y='Capita_COVID',
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

st.altair_chart(us_covid + us_covid1 + us_covid2 + us_covid3)
st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.")


#Graphs for selected U.S. States
st.header("Select a State to view the All Cause and COVID-19 Deaths")
state = st.selectbox("Select state",merged['Jurisdiction of Occurrence'].unique())
state_df = merged[merged['Jurisdiction of Occurrence']==state]
state_df.drop(state_df.tail(5).index,inplace=True)
merged_rem = merged[merged['Jurisdiction of Occurrence']==state].tail(6)


#All cause death graph
st.header(f"All Cause Deaths for {state}")
all_cause1 =  alt.Chart(state_df,width=1000,height=400).transform_fold(['MMWR Year']).mark_line().encode( 
    x=alt.X('MMWR Week', axis = alt.Axis(title='Week Number')),
    y=alt.Y('capita_allcause', axis = alt.Axis(title = 'Capita per 1000')),
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")), #discrete unordered category :N 
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

all_cause2 = alt.Chart(state_df,width=1000,height=400).mark_circle().encode( 
    x='MMWR Week',
    y='capita_allcause',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

all_cause3 = alt.Chart(merged_rem,width=1000,height=400).mark_line(strokeDash = [5,5]).encode( 
    x='MMWR Week',
    y='capita_allcause',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

all_cause4 = alt.Chart(merged_rem,width=1000,height=400).mark_circle().encode( 
    x='MMWR Week',
    y='capita_allcause',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','All Cause','MMWR Year']
).interactive()

st.altair_chart(all_cause1 + all_cause2 + all_cause3 + all_cause4)

#Covid-19 Deaths graph
st.header(f"COVID-19 Deaths for {state}")

covid1 =  alt.Chart(state_df,width=1000,height=400).mark_line().encode( 
    x=alt.X('MMWR Week', axis = alt.Axis(title='Week Number')),
    y=alt.Y('capita_covid', axis = alt.Axis(title = 'Capita per 1000')),
    color=alt.Color('MMWR Year:N',legend=alt.Legend(title="Year")),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()

covid2 =  alt.Chart(state_df,width=1000,height=400).mark_circle().encode( 
    x='MMWR Week',
    y='capita_covid',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()

covid3 = alt.Chart(merged_rem,width=1000,height=400).mark_line(strokeDash = [5,5]).encode( 
    x='MMWR Week',
    y='capita_covid',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()

covid4 = alt.Chart(merged_rem,width=1000,height=400).mark_circle().encode( 
    x='MMWR Week',
    y='capita_covid',
    color=alt.Color('MMWR Year:N'),
    tooltip=['MM-DD','COVID-19 (U071, Multiple Cause of Death)','MMWR Year']
).interactive()

st.altair_chart(covid1 + covid2 + covid3 + covid4)
st.markdown(" :warning: Note that the number of deaths reported in this graph may be incomplete due to lag in time (approx. 6 - 8 weeks) between the time the death occured and when the death certificate is completed.")




#Display Datasets
st.header("View Datasets")
st.markdown("**Provisonal counts of all cause deaths by week the deaths occured, by state, and by all causes of death. This dataset also includes weekly provisional counts of death for COVID-19, as underlying or multiple cause of death.**")
if st.checkbox(f"Click to view the dataset for {state}", False):
    st.write(merged[merged['Jurisdiction of Occurrence']==state])
if st.checkbox("Click to view the dataset for all states", False):
    st.write(merged)
if st.checkbox("Click to view dataset for the United States", False):
    st.write(us_df)
st.write("Data Source: Weekly Counts of Deaths by State and Select Causes, 2019-2020, https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/muzy-jte6")
