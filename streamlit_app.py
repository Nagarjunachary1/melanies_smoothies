# Import python packages
import streamlit as st
import requests
import pandas as pd

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom smoothie!
  """
)

name_on_order = st.text_input("Name on smoothie");
st.write("Order Name="+name_on_order)

cnx =st.connection("snowflake")
session =cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)


ingerdient_list =st.multiselect(
    "choose up to 6 ingerdients",
    my_dataframe,
    max_selections=6
);

if ingerdient_list:
    ingredients_string = '';

    for fruit_chosen in ingerdient_list:
        ingredients_string+=fruit_chosen+' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen +" Nutrion Info")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    st.write("ingerdient_string="+ingredients_string);

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")    



#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)


