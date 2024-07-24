import os
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.write(st.session_state.user)
user_db_path = os.path.join(BASE_DIR, st.session_state.user + ".db")
connect_user = sqlite3.connect(user_db_path)
curs_user = connect_user.cursor()

html_style_string = '''<style>
@media (min-width: 576px)
section div.block-container {
  padding-left: 20rem;
}
section div.block-container {
  padding-left: 4rem;
  padding-right: 4rem;
  max-width: 80rem;
}  

</style>'''
st.markdown(html_style_string, unsafe_allow_html=True)

#
tab1, tab2, tab3 = st.tabs(["overview", "strategies", "modify strategy"])

with tab1:


    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

    st.line_chart(chart_data)
    data = {
        'stock': [row[0] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'quantity': [row[1] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'initial price per share': [row[2] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],
        'long/short': [row[3] for row in curs_user.execute("SELECT * FROM portfolio").fetchall()],

    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = st.dataframe(df,hide_index=True,use_container_width=True)

with tab2:
    st.title("simulated trading game")
    st.write("need to import table [docs.streamlit.io](https://docs.streamlit.io/).")



    data = {
        'strategy name': [row[0] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'location': [row[1] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'stock': [row[2] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'take profit': [row[3] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'stop loss': [row[4] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'minimum trade size': [row[5] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'maximum trade size': [row[6] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'minimum trade duration': [row[7] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'maximum duration': [row[8] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
        'trade frequency': [row[9] for row in curs_user.execute("SELECT * FROM strategy").fetchall()],
    }
    ##change the array in line 14 for the strategies true performance

    df = pd.DataFrame(data)
    event = st.dataframe(
        df,
        on_select='rerun',
        selection_mode='multi-row',
         hide_index = True,
        use_container_width=True
    )

    st.button("modify")
    st.button("delete", type="primary")
with tab3:
    option = st.selectbox(
        "Select the strategy you wish to modify",
        data["strategy name"])
    with open('user_terminal/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    with open('user_terminal/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    height = [20, 10]
    btns = custom_buttons_alt
    st.write("Adjust the strategy below then Hit Save")

    response_dict = code_editor("####strategy file path#####", height=height, buttons=btns, info=info_bar)
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code = response_dict['text']


    st.write(" #### add the trading logic widgets below####")
#
