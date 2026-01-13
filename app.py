# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

company_list = [
    r'C:\\Users\\alona\\Desktop\\Data analytics\\S&P_resources\\individual_stocks_5yr\\AAPL_data.csv' , 
    r'C:\\Users\\alona\\Desktop\\Data analytics\\S&P_resources\\individual_stocks_5yr\\AMZN_data.csv' , 
    r'C:\\Users\\alona\\Desktop\\Data analytics\\S&P_resources\\individual_stocks_5yr\\GOOG_data.csv' , 
    r'C:\\Users\\alona\\Desktop\\Data analytics\\S&P_resources\\individual_stocks_5yr\\MSFT_data.csv'
    
]

list_of_dfs = []

for file in company_list:
    current_df = pd.read_csv(file)
    list_of_dfs.append(current_df)
all_data = pd.concat(list_of_dfs, ignore_index=True)

all_data['date'] = pd.to_datetime(all_data['date'])

st.set_page_config(page_title= "Stock Analysis Dashboard", layout = "wide")
tech_list= all_data['Name'].unique()
st.title("Tech Stock Analysis Dashboard")
st.sidebar.title("Choose a Company")
selected_company= st.sidebar.selectbox("Select a stock", tech_list)
company_df= all_data[all_data['Name']==selected_company]
company_df.sort_values('date', inplace=True)

## 1st plot:
st.subheader(f"1. Closing Prices of {selected_company} Over Time")
fig1= px.line(company_df, x = 'date', y= 'close',
        title = selected_company + 'closing prices over time' )
st.plotly_chart(fig1, use_container_width=True)

## 2nd plot:
st.subheader('2. Moving Averages (10,20,50) ')
ma_day=[10,20,50]

for ma in ma_day:
    company_df['close_'+str(ma)]= company_df['close'].rolling(ma).mean()
    
fig2= px.line(company_df, x = 'date', y= ['close', 'close_10', 'close_20', 'close_50'],
        title = selected_company + 'closing prices with moving average' )
st.plotly_chart(fig2, use_container_width=True)

## 3rd plot:
st.subheader('3. Daily returns for '+ selected_company)
company_df['Daily return in %']= company_df['close'].pct_change()*100

fig3= px.line(company_df, x = 'date', y= 'close',
        title = 'Daily return in (%)' )
st.plotly_chart(fig3, use_container_width=True)

## 4th plot:
st.subheader('4. Resampled Closing Price (Monthly / Quartely / Yearly')
company_df.set_index('date', inplace=True) 
Resample_option = st.radio('Select Resample Frequency', ['monthly', ' Quarterly', 'Yearly' ])

if Resample_option== 'monthly':
    resampled= company_df['close'].resample('M').mean()
elif Resample_option== 'Quarterly':
    resampled = company_df['close'].resample('Q').mean()
else: resampled = company_df['close'].resample('Y').mean()
    
fig4= px.line(resampled,
        title = selected_company + " " + Resample_option + 'Average closing price' )
st.plotly_chart(fig4, use_container_width=True)

##5th plot:
app = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['apple_close'] = app['close']
closing_price['amzn_close'] = amzn['close']
closing_price['google_close'] = google['close']
closing_price['msft_close'] = msft['close']

fig5, ax= plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', ax= ax)
st.pyplot(fig5)

st.markdown('---')
st.markdown('**Note**: This dashboard provides basic technical analysis of major tech stocks using Python and Streamlit ')
    

