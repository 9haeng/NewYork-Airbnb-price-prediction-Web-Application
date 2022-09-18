import pickle
from time import sleep
import pandas as pd
import os
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from streamlit_autorefresh import st_autorefresh
import xgboost
import shap
import matplotlib.pyplot as plt
# import pyautogui
import json
import requests
from PIL import Image
import time
import webbrowser

def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

lottie_loading = load_lottiefile('travel.json')

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def data_transform(df_summary, df_final):
    for idx, col in enumerate(df_summary):
        if idx == 0:
            if df_summary[col].values[0] == 'Bronx':
                df_final['neighbourhood_group_Bronx'] = 1
            elif df_summary[col].values[0] == 'Brooklyn':
                df_final['neighbourhood_group_Brooklyn'] = 1
            elif df_summary[col].values[0] == 'Manhattan':
                df_final['neighbourhood_group_Manhattan'] = 1
            elif df_summary[col].values[0] == 'Queens':
                df_final['neighbourhood_group_Queens'] = 1
            elif df_summary[col].values[0] == 'Staten Island':
                df_final['neighbourhood_group_Staten Island'] = 1
        elif idx == 1:
            if df_summary[col].values[0] == 'Entire home/apt':
                df_final['room_type_Entire home/apt'] = 1
            elif df_summary[col].values[0] == 'Private room':
                df_final['room_type_Private room'] = 1
            elif df_summary[col].values[0] == 'Shared room':
                df_final['room_type_Shared room'] = 1
                    
        elif idx == 2:
            df_final['minimum_nights'] = df_summary[col].values[0]
        elif idx == 3:
            df_final['availability_365'] = df_summary[col].values[0]
        elif idx == 4:
            df_final['number_of_reviews'] = df_summary[col].values[0]
        elif idx == 5:
            df_final['reviews_per_month'] = df_summary[col].values[0]
        elif idx == 6:
            df_final['calculated_host_listings_count'] = df_summary[col].values[0]
        elif idx == 7:
            df_final['days_since_last_review'] = df_summary[col].values[0]

def feature_importance(model, data):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data.values)  
    chart_data = pd.DataFrame(shap_values, columns=data.columns)
    chart_data.T.sort_values(by=0, ascending=False).rename(columns={0: 'Feature Importances'}).plot.barh()
    plt.savefig('feature_importance.png', bbox_inches='tight')


def predict_model(model, data):
    global result
    result = model.predict(data.values)[0]
    return result



CSV_FILEPATH = os.path.join(os.getcwd(), 'airbnb_ML.csv') 
model = pickle.load(open('model.sav', 'rb'))
df = pd.read_csv(CSV_FILEPATH)

st.set_page_config(page_title="Newyork Airbnb Price Predcition Web Service",
    page_icon="🗽",
    layout="wide")


st.title('NYC Airbnb price prediction 🗽')


if st.button('Guide'):
    st.success('''
    Welcome to our NYC Airbnb Accommodation Price Prediction service 😄  \n
    In order to predict the price of the accommodation you are interested in, you must select at least the neighborhood and room type information. \n
    Also, if you want to get a more accurate estimate of your accommodation price, please fill in the options that you need to enter as a numeric type. \n
    If you have successfully found out the price of your accommodation, check out the 'Browse Airbnb' button at the bottom to find the real accommodation that matches your interests! \n
    Bon voyage! ✈️
    ''')

neighbourhood_group = ['-','Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']
roomtype = ['-','Entire home/apt', 'Private room', 'Shared room']
reviews_answer = ['-','Yes', "No thanks"]


# To activate summary
summary = 0

# Get neighbourhood group information

select_neighbourhood = st.selectbox('Choose the neighbourhood group you are interested in', neighbourhood_group)
if select_neighbourhood == neighbourhood_group[0]:
    pass
else:
    st.write('You chose', select_neighbourhood)
    summary += 1

# Get room type information

select_roomtype = st.selectbox('Choose the room type you are interested in', roomtype)
if select_roomtype == roomtype[0]:
    pass
else:
    st.write('You chose', select_roomtype)
    summary += 1

# Get minimum nights information

choose_minimum_nights = st.selectbox('Do you have the desired number of minimum nights for the accommodation you are looking for?', reviews_answer)

if choose_minimum_nights == reviews_answer[2]:
    choose_minimum_nights = round(df['minimum_nights'].median(),2)
    summary += 1
elif choose_minimum_nights == reviews_answer[1]:
    st.write('Please enter the desired number of minimum nights between 1 and 15.')
    choose_minimum_nights = st.number_input('FYI, around 3 minimum nights are asked for each accommodation on average.', min_value=1, max_value=15, format='%d')
    st.write('You chose', choose_minimum_nights, 'days as minimum nights.')
    summary += 1


# Get availability 365 information

choose_availability_365 = st.selectbox('Do you have the desired number of the total number of days bookable during the year?', reviews_answer)

if choose_availability_365 == reviews_answer[2]:
    choose_availability_365 = round(df['minimum_nights'].median(),2)
    summary += 1
elif choose_availability_365 == reviews_answer[1]:
    st.write('Please enter a value between 0 and 365 to calculate the popularity of the accommodation you are looking for.')
    st.write('The higher values, the easier it is to book.')
    choose_availability_365 = st.number_input('i.e. if all the available days are rented out, then the listing’s occupancy rate is 100%.', min_value=0, max_value=365, format='%d')
    st.write('You chose', choose_availability_365, 'days bookable during the year.')
    summary += 1

# Get number of reviews information

choose_number_of_reviews = st.selectbox('Do you have the desired number of reviews for the accommodation you are looking for?', reviews_answer)

if choose_number_of_reviews == reviews_answer[2]:
    choose_number_of_reviews = round(df['number_of_reviews'].median(),2)
    summary += 1
elif choose_number_of_reviews == reviews_answer[1]:
    st.write('Please enter the desired number of reviews between 0 and 60.')
    choose_number_of_reviews = st.number_input('FYI, 10 reviews exist for each accommodation on average.', min_value=0, max_value=60, format='%d')
    st.write('You chose', choose_number_of_reviews, 'reviews for your accomodation.')
    summary += 1

# Get reviews per month information

choose_reviews_per_month = st.selectbox('Do you have the desired number of reviews per month for the accommodation you are looking for?', reviews_answer)

if choose_reviews_per_month == reviews_answer[2]:
    choose_reviews_per_month = round(df['reviews_per_month'].median(),2)
    summary += 1
elif choose_reviews_per_month == reviews_answer[1]:
    st.write('Please enter the desired number of reviews per month between 0 and 5.')
    st.write('It means the higher the value, the higher the average number of reservations made per month.')
    choose_reviews_per_month = st.number_input('FYI, 0.9 reviews exist per month per accommodation on average.', min_value=0.0, max_value=5.0, format='%.2f')
    st.write('You chose', round(choose_reviews_per_month,2), 'reviews per month for your accomodation.')
    summary += 1

# Get calculated host listings

choose_calculated_host_listings = st.selectbox('Do you have the desired number of calculated host listings for the accommodation you are looking for?', reviews_answer)

if choose_calculated_host_listings == reviews_answer[2]:
    choose_calculated_host_listings = round(df['calculated_host_listings_count'].median(),2)
    summary += 1
elif choose_calculated_host_listings == reviews_answer[1]:
    st.write('Please enter the desired number of calculated host listings between 1 and 5.')
    st.write("This value can be related to the host's experience and expertise.")
    choose_calculated_host_listings = st.number_input('FYI, 1.2 host listings for each host on average.', min_value=1.0, max_value=5.0, format='%.2f')
    st.write('You chose', round(choose_calculated_host_listings,2), 'host listings per host for your accommodation.')
    summary += 1


# Get days since last review

choose_days_since_last_review = st.selectbox('Do you have the desired number of days since last review for the accommodation you are looking for?', reviews_answer)

if choose_days_since_last_review == reviews_answer[2]:
    choose_days_since_last_review = round(df['days_since_last_review'].mean(),2)
    summary += 1
elif choose_days_since_last_review == reviews_answer[1]:
    st.write('Please enter the desired number of days since last review between 0 and 365.')
    st.write("This value may be related to the popularity of the accommodation.")
    choose_days_since_last_review = st.number_input('FYI, 181 days passed since the last review was created for each accommodation on average.', min_value=0, max_value=365, format='%d')
    st.write('You chose', round(choose_days_since_last_review,2), 'days passed since the last review.')
    summary += 1

if summary == 8:

    st.header('This is a summary of all the information you have entered!')
    st.write('Please review whether you have filled in the information about the accommodation you want properly.')

    summary_list = [select_neighbourhood, select_roomtype, choose_minimum_nights, choose_availability_365, choose_number_of_reviews, 
                        choose_reviews_per_month, choose_calculated_host_listings, choose_days_since_last_review]

    name = ['Neighbourhood', 'Room type', 'Minimum nights', 'Availability 365', 'Number of reviews',
            'Reviews per month' , 'Calculated host listings', 'Days since last review']
    global df_summary
    df_summary = pd.DataFrame({'Feature': name, 'Value':summary_list})

    col1, col2, col3, col4 = st.columns(4)
    collist1 = [col1, col2 ,col3, col4]
    for idx, col in enumerate(collist1):
        col.metric(name[idx], summary_list[idx])

    col5, col6, col7, col8 = st.columns(4)
    collist2 = [col5, col6 ,col7, col8]
    for idx, col in enumerate(collist2):
        col.metric(name[idx+4], summary_list[idx+4])

    df_summary = df_summary.T

    header = df_summary.iloc[0]
    df_summary = df_summary[1:]

    df_summary.rename(columns=header, inplace=True)

    df_final_category = ['neighbourhood_group_Bronx', 'neighbourhood_group_Brooklyn', 'neighbourhood_group_Manhattan',
                'neighbourhood_group_Queens', 'neighbourhood_group_Staten Island',	'room_type_Entire home/apt',
                'room_type_Private room', 'room_type_Shared room', 'minimum_nights', 'number_of_reviews',
                'reviews_per_month', 'calculated_host_listings_count',	'availability_365',	'days_since_last_review']
    df_final = pd.DataFrame({x:0 for x in df_final_category}, index=[0])

    total = st.slider('If you drag this slider all the way to the right, we will predict the accommodation price very soon!', 0, 100, 1)

    if total == 100:
        with st_lottie_spinner(lottie_loading, height=500):
            time.sleep(3.5)
            total = 0        
        summary += 1


if summary == 9:
   
    data_transform(df_summary, df_final)
    predict_model(model, df_final)
    # with st.spinner('Please wait...'):          
    if result < 0:
        st.write('We could not predict the proper accommodation price based on the information entered.')
    else:
        st.header('The estimated accommodation price based on the information entered is')
        global price
        price = round(result, 2)
        st.write(price, '$')

        feature_importance(model, df_final)
        image = Image.open('feature_importance.png')
        st.image(image, caption='Feature Importance based on information')


if st.button('Browse Airbnb'):
    try:     
        url = f'https://www.airbnb.co.kr/s/{select_neighbourhood}--New-York--NY--United-States/homes?price_max={price*1386}&search_type=filter_change&room_types%5B%5D={select_roomtype}'
        webbrowser.open_new_tab(url)
    except:
        st.warning('I guess you did not fill in all the information needed 🤔')


# disable refresh feature since streamlit didn't support pyautogui yet.

# if st.button("Clear All"):
#     st_autorefresh(interval=2000, limit=2)



