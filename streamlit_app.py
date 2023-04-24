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

# normalized df function

def get_fruityvice_data(this_fruit_choice):
  #fruity vice api data normalized into df
  fruityvice_response = r.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")
  return pd.json_normalize(fruityvice_response.json())

#fruit input for fruityvice api
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    norm_fruityvice = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(norm_fruityvice)

except URLError as e:
  streamlit.error()

# stopping for debug
# streamlit.stop()

# snowflake connector

streamlit.header("View our fruit options - Add you Favs!")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
 
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    return f'Thanks for adding {new_fruit}'

if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# add fruit text entry
add_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_snowflake(add_fruit))
  my_cnx.close()
