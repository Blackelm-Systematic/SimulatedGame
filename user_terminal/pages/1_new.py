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

custom_buttons_alt = '''[{
    "name": "Copy",
    "feather": "Copy",
    "hasText": true,
    "alwaysOn": true,
    "commands": ["copyAll", 
                 ["infoMessage", 
                  {
                   "text":"Copied to clipboard!",
                   "timeout": 2500, 
                   "classToggle": "show"
                  }
                 ]
                ],
    "style": {"top": "-0.25rem", "right": "0.4rem"}
  },{
    "name": "Run",
    "feather": "Play",
    "primary": true,
    "hasText": true,
    "showWithIcon": true,
    "commands": ["submit"],
    "style": {"bottom": "0.44rem", "right": "0.4rem"}
  }]'''



@st.experimental_dialog("Create a new trading strategy")
def logic(name):
    st.write(f"set the trading logic for {name}")
    ##add bot logic widgets here
    if st.button("add"):
        st.rerun()


st.title("Create a new trading strategy here")
name = st.text_input("enter bot name here")

height = [19, 22]
language = "python"
theme = "default"
shortcuts = "vscode"
focus = False
btns = custom_buttons_alt

# construct props dictionary (->Ace Editor)
response_dict = code_editor("", height=height, lang=language, theme=theme, shortcuts=shortcuts,
                            focus=focus, buttons=btns )

if response_dict['type'] == "submit" and len(response_dict['text']) != 0:
    st.code(response_dict['text'], language=response_dict['lang'])

    repo.update_file("test.py", "it works", response_dict['text'], branch="main")

#####
if st.button("impliment"):
    pass
    #logic(name)

# else:
#     f"{st.session_state.logic['name']} has now been added (this is when the strat are added to sql)"
#     if st.button("ok"):
#         st.write(st.session_state)
#         st.rerun()
