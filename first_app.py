import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit.components.v1 as components
import time

def get_dom():
    return df["Date/Time"].dt.day

def sidebartitle():
    st.sidebar.title("Dataframes")

def showdf(uber, trip):
    if st.sidebar.checkbox('Show Uber dataframe'):
        chart_data = pd.read_csv(uber)
        chart_data["Date/Time"] = pd.to_datetime(chart_data["Date/Time"])
        datas = st.sidebar.selectbox('Comment souhaitez vous afficher les données :',('Original database','Classified by days of months','Classified by weekdays and hours'))
        if datas == 'Original database':
            st.title("Original database")
            chart_data
        if datas == 'Classified by days of months':
            st.title("Database classified by days of months")
            chart_data['Date/Time'] = chart_data['Date/Time'].dt.day
            chart_data
        if datas == 'Classified by weekdays and hours':
            st.title("Database classified by weekdays and hours")
            chart_data["Date/Time"] = chart_data["Date/Time"].dt.strftime('%A-%H')
            chart_data

    if st.sidebar.checkbox('Show Trips dataframe'):
        chart_data = pd.read_csv(trip)
        chart_data

def datauber():
    df =  pd.read_csv("uber-raw-data-apr14.csv")
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    return df

def presentation():
    st.title("IFRAME")
    components.iframe(uberplot_day(df,1))
    components.iframe(map_geographic(df))
    st.title("")
    st.title("Prediction Dashboard")
    st.text("This dashboard helps to predict result with better and interactive visuals")
    st.title("")
    st.title("")

def grouping(df):
    dom = get_dom()
    df['Day'] = dom
    d = df.groupby('Day',as_index=False).mean()
    return d 

def uberplot_day(df,c):
    hist_values = np.histogram(
            df["Date/Time"].dt.day, bins=30, range=(0.5,30.5))[0]
    if c == 1:
        st.bar_chart(hist_values)
    else:
        st.line_chart(hist_values)

def barplot_geographic(df):
    d = grouping(df)
    d = d[["Lat","Lon"]]
    st.bar_chart(d)

def map_geographic(df):
    a = pd.DataFrame(df[["Lat","Lon"]])
    a = a.rename(columns={"Lat":"lat","Lon":"lon"})
    st.map(a)

def tripmap_geographic(df,x,y):
    a = pd.DataFrame(df[[x,y]])
    a = a.rename(columns={x:"lat",y:"lon"})
    st.map(a)

def barplot_hour(df):
    hist_values = np.histogram(
            df["Date/Time"].dt.hour, bins=24, range=(0.5,24))[0]
    st.bar_chart(hist_values) 

def barplot_week(df):
    hist_values = np.histogram(
            df["Date/Time"].dt.weekday, bins=7, range=(-.5,6.5))[0]
    st.bar_chart(hist_values)

def trip_datetimes_plot(df,x,c):
    df[x] = df[x].map(pd.to_datetime)
    hist_values = np.histogram(
            df[x].dt.hour, bins=24, range=(-.5,23.5))[0]
    if c == 1:
        st.bar_chart(hist_values)
    else:
        st.line_chart(hist_values)

def barplot_vendors(df):
    hist_values = np.histogram(
            df["VendorID"], bins=2, range=(0.5,3))[0]
    st.bar_chart(hist_values)

def details(df,df_t):
    datas = st.selectbox("Which data do you want to analyze ?",("Uber","Trips"))
    st.title("")
    if (datas == "Uber"):
        
        st.title("Uber")
        st.header("Data depending of the days of the month")
        datas = st.selectbox("Choose the type of chart you want",("Histogramme","Line chart"))
        
        if (datas == "Histogramme"):
            uberplot_day(df,1)
        
        if (datas == "Line chart"):
            uberplot_day(df,2)

        st.header("Geographic coordinates")
        datas = st.selectbox("Choose the type of chart you want",("Bar plot","Map"))
        
        if (datas == "Bar plot"):
            barplot_geographic(df)
        
        if (datas == "Map"):
            map_geographic(df)
        
        st.header("Data depending on the hour of the day")
        barplot_hour(df)

        st.header("Data depending on the weekdays")
        barplot_week(df)


    if (datas == "Trips"):
        st.title("Trips")
        st.header("Geographic coordinates of pickups and drop offs")

        datas = st.selectbox("Choose the Map you want",("Pickup map","Dropoff map"))
        
        if (datas == "Pickup map"):
            tripmap_geographic(df_t,"pickup_latitude","pickup_longitude")
        
        if (datas == "Dropoff map"):
            tripmap_geographic(df_t,"dropoff_latitude","dropoff_longitude")
        
        st.header("Frequences of pickups and dropoffs")
        datas = st.selectbox("Choose the type of chart you want",("Histogramme","Line chart"))
        
        if (datas == "Histogramme"):
            st.text("Pickups")
            trip_datetimes_plot(df_t,"tpep_pickup_datetime",1)
            st.text("Dropoffs")
            trip_datetimes_plot(df_t,"tpep_pickup_datetime",1)

        if (datas == "Line chart"):
            st.text("Pickups")
            trip_datetimes_plot(df_t,"tpep_pickup_datetime",2)
            st.text("Dropoffs")
            trip_datetimes_plot(df_t,"tpep_pickup_datetime",2)
        
        st.header("Sales per vendors")
        barplot_vendors(df_t)


sidebartitle()
print(showdf("uber-raw-data-apr14.csv","ny-trips-data.csv"))
df = datauber()
df_t = pd.read_csv("ny-trips-data.csv")
presentation()
details(df,df_t)

                                              



