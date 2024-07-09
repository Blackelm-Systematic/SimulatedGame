import os.path
import streamlit_authenticator as stauth

import streamlit as st
import pandas as pd
import numpy as np
import random
from code_editor import code_editor
import json
from github import Github
g=Github("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")
repo=g.get_repo("Blackelm-Systematic/SimulatedGame")

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
if "login" not in st.session_state:
    st.session_state.login=False


if st.session_state.login==True:
    @st.experimental_dialog("Create a new trading strategy")
    def logic(name,code):
        st.write(f"set the trading logic for {name}")
        ##add bot logic widgets here
        if st.button("add"):
            repo.create_file(str(random.randint(0, 5000)) + ".py", "it works", code, branch="main", )
            st.rerun()


    st.title("Create a new trading strategy here")
    name = st.text_input("enter bot name here")
    ###

    with open('user_terminal/pages/resources/example_custom_buttons_bar_adj.json') as json_button_file_alt:
        custom_buttons_alt = json.load(json_button_file_alt)

    with open('user_terminal/pages/resources/example_info_bar.json') as json_info_file:
        info_bar = json.load(json_info_file)

    height = [20, 22]
    btns = custom_buttons_alt
    st.write("Program your strategy below then Hit Save")


    response_dict = code_editor("", height=height,   buttons=btns, info=info_bar)
    if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
        code=response_dict['text']
        logic(name,code)
    elif  response_dict['type'] == "submit" and len(response_dict['text']) == 0:
        st.warning('Add your strategy before Hitting Save', icon="⚠️")

    #####

