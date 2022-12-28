import streamlit
import pandas
import requests 
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🍪 Omega 3 & Blueberry Oatmeaal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 🍞 Avocado Toast')

streamlit.header('🍌🍉 Build Your Own Fruit Smoothie 🥝🍓')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
## debug my_fruit_list
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick fruit to include
# streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))

# let's put a DEFAULT pick list here so they can pick fruit to include
# streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])

# let's filter pick list as per selected
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

try:

   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
    
    streamlit.write('The user entered ', fruit_choice)

              # basic1 import requests 
              # basic1 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
              # basic1 streamlit.text(fruityvice_response.json()) #just writes the raw json data to the screen

    #import requests 
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
              # basic2 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
              # basic1 streamlit.text(fruityvice_response.json()) #just writes the raw json data to the screen

    # normalised json output to rows & columns
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

    # display on screen
    streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()

# don't run anything past here while we troubleshoot
streamlit.stop()

# snowflake.connector 
# import snowflake.connector

# debug - check credentials via snowflake.connector 
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# retrieve data from snowflake via snowflake.connector 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")

#my_data_row = my_cur.fetchone() #just pick one row
my_data_row = my_cur.fetchall() #just pick one row

streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# Allow end user to add fruit to fruit_load_list
add_my_fruit = streamlit.text_input('What fruit would you like to add??','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# add inputted fruit to fruit_load_list table
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
