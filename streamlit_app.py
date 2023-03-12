import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import base64
import numpy as np

#Webpage Title
st.title('All Time NSMQ Winners')
st.sidebar.header('User Input Features')

#Load Dataframe
excel_file = 'NSMQ.xlsx'
sheet_name = 'Data'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:D',
                   header=0)

df_status = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='F:G',
                   header=0)

df_status.dropna(inplace=True)

#Create filters on sidebar
status = df['Status'].unique().tolist()
wins = df['Wins'].unique().tolist()

wins_selection = st.sidebar.slider('Wins:',
                           min_value=min(wins),
                           max_value=max(wins),
                           value=(min(wins),max(wins)))

status_selection = st.sidebar.multiselect('Status:',
                                          status,
                                          default = status)


mask = (df['Wins'].between(*wins_selection)) & (df['Status'].isin(status_selection))
number_of_results = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_results}*')

#Display image
image = Image.open('/Users/shawshank/Documents/Streamlit/NSMQ.png')
st.image(image,
         width=200)

#Group dataframe after selection
df_grouped_schools = df[mask].groupby(by=['School']).count()[['Wins']]
df_grouped_schools = df_grouped_schools.reset_index()

bar_chart = px.bar(df_grouped_schools,
                  x='Wins',
                  y='School',
                  text='Wins',
                  color_discrete_sequence=['#F63366']*len(df_grouped_schools),
                  template= 'plotly_white')

bar_chart.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title = None)

st.plotly_chart(bar_chart)
