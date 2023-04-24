import streamlit
import pandas as pd
import requests as r
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list.set_index('Fruit', inplace=True)

fruityvice_response = r.get("https://fruityvice.com/api/fruit/watermelon")

streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal  🥣 ')
streamlit.text('Kale, Spinach & Rocket Smoothie 🥗')
streamlit.text('Hard-Boiled Free-Range Egg 🐔')
streamlit.text('Avocado Toast 🥑🍞')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Multi select
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# selects only requested fruits
show_fruits = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(show_fruits)


#fruit input for fruityvice api
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    #fruity vice api data normalized into df
    fruityvice_response = r.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
    norm_fruityvice = pd.json_normalize(fruityvice_response.json())
    streamlit.dataframe(norm_fruityvice)

except URLError as e:
  streamlit.error()

# stopping for debug
streamlit.stop()

# snowflake connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()

streamlit.header("Fruit load list contains:")
streamlit.dataframe(my_data_row)

# add fruit text entry
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.text(f'Thanks for adding {add_my_fruit}')

my_cur.execute(f"insert into fruit_load_list values ('{add_my_fruit}')")
