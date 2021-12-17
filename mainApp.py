## mysql
# https://dev.mysql.com/doc/mysql-getting-started/en/
# https://docs.streamlit.io/knowledge-base/tutorials/databases/mysql

## multipage
# https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4

## put it on the internet
# https://towardsdatascience.com/show-your-ml-project-to-the-internet-in-minutes-2a7bc3167bd0

## aesthetic
# https://blog.streamlit.io/introducing-theming/
# https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/3

## change the sliders
# https://github.com/andfanilo/streamlit-custom-slider

## https://stackoverflow.com/questions/8671808/matplotlib-avoiding-overlapping-datapoints-in-a-scatter-dot-beeswarm-plot

import surveyView
import resultsView
import distributionView
import streamlit as st
import numpy as np


import psycopg2
#import mysql.connector

def init_connection():
#    return mysql.connector.connect(**st.secrets["mysql"])
    return psycopg2.connect(host = "localhost",port = 5432,database = "gaze_database",user = "postgres", password = os.environ['PASSWORD_KEY'])

conn = init_connection()

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def insert_into_table(ggt,man1,man2,man3,man4,man5,man6,man7,man8,man9,man10,man11,man12,man13):
    try:
        conn = init_connection()
        cur = conn.cursor()

        query = """INSERT INTO gaze_table (ggt,man1,man2,man3,man4, man5,man6,man7,man8,man9,man10,man11,man12,man13)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        row = (ggt,man1,man2,man3,man4, man5,man6,man7,man8,man9,man10,man11,man12,man13)
        cur.execute(query, row)
        conn.commit()
        print("Record inserted successfully into table")

    #except mysql.connector.Error as error:
    #    print("Failed to insert into MySQL table {}".format(error))

    finally:
        if conn.is_connected():
            cur.close()
            conn.close()
            print("MySQL connection is closed")


def jitter(start, end, num):
    res = []
    for j in range(num):
        res.append(np.random.randint(start, end))
    return res

raw_code = '''SELECT count(*), AVG(man1) man1, AVG(man2) man2, AVG(man3) man3, AVG(man4) man4, AVG(man5) man5, AVG(man6) man6, AVG(man7) man7, AVG(man8) man8, AVG(man9) man9, AVG(man10) man10, AVG(man11) man11, AVG(man12) man12, AVG(man13) man13 FROM gaze_table GROUP BY ggt'''
df = run_query(raw_code)








## potentially randomize order

#st.sidebar.image('images/start here.png')
"""
# Male vs. Female Gaze
Brief description of project blah blah blah.
"""
st.sidebar.title('Survey')

ggtReponse = st.sidebar.radio('please self identify (hahaha)',['girl/gay/they', 'other'])
ggt = 'female' if ggtReponse == 'girl/gay/they' else 'male'

st.sidebar.write("How attractive do you personally find:")

rating1 = st.sidebar.slider('Adam Driver', 0, 100, 44)
rating2 = st.sidebar.slider('Ryan Reynolds', 0, 100, 45)
rating3 = st.sidebar.slider('Dev Patel', 0, 100, 46)
rating4 = st.sidebar.slider('Pete Davidson', 0, 100, 47)
rating5 = st.sidebar.slider('Robert Pattinson', 0, 100, 48)
rating6 = st.sidebar.slider('Michael Cera', 0, 100, 49)
rating7 = st.sidebar.slider('Donald Glover', 0, 100, 50)
rating8 = st.sidebar.slider('Harry Styles', 0, 100, 51)
rating9 = st.sidebar.slider('Chris Hemsworth', 0, 100, 52)
rating10 = st.sidebar.slider('Benedict Cumberbatch', 0, 100, 53)
rating11 = st.sidebar.slider('John Krasinski', 0, 100, 54)
rating12 = st.sidebar.slider('Timothee Chalamet', 0, 100, 55)
rating13 = st.sidebar.slider('Michael B. Jordan', 0, 100, 56)


st.sidebar.title("Submit responses to project's database ✨for science ✨")
agree = st.sidebar.checkbox('Submit')




if agree:
     st.sidebar.write('Thank you!')
     ## submit answers to database
     #insert_into_table(ggt,rating1,rating2,rating3,rating4)

     PAGES = {
         "Individual View": surveyView,
         "Everyone": resultsView,
         "Distribution": distributionView

     }

     st.sidebar.title('See Results Below!!!!! ')

     selection = st.sidebar.radio("", list(PAGES.keys()))
     page = PAGES[selection]
     page.app(df, rating1,rating2,rating3,rating4, rating5, rating6, rating7, rating8, rating9,rating10, rating11, rating12, rating13)
else:
    surveyView.app(df, rating1,rating2,rating3,rating4, rating5, rating6, rating7, rating8, rating9,rating10, rating11, rating12, rating13)
