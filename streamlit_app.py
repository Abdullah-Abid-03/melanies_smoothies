# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("Customize Your Smoothie")

name_on_order = st.text_input("Name on Smoothie:")

# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = (
    session
    .table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    [row["FRUIT_NAME"] for row in my_dataframe.collect()],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
else:
    ingredients_string = ""

submit = st.button("Submit Order")

if submit:
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    session.sql(my_insert_stmt).collect()

    # ✅ Confirmation message with name
    st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

