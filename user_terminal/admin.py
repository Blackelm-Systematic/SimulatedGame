import os
import sqlite3
import subprocess

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

new=open("user_terminal/compiler_location.txt")
compiler_location=new.readline()
st.session_state.user=st.session_state.user

st_autorefresh()

connect_stock = sqlite3.connect("user_terminal/stock_prices.db",check_same_thread=False)
curs_stock = connect_stock.cursor()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_db_path = os.path.join(BASE_DIR, "credentials.db")
connect_credentials = sqlite3.connect(cred_db_path,check_same_thread=False)

curs_credentials = connect_credentials.cursor()

connect_exchange = sqlite3.connect( "user_terminal/exchange.db" ,check_same_thread=False)
curs_exchange = connect_exchange.cursor()
process_handle = None

# Start market function
if 'process_handle' not in st.session_state:
    st.session_state.process_handle = None

# Start market function
def start_market():
    if st.session_state.process_handle is None:
        # Start the process and store the handle in session state
        st.session_state.process_handle = subprocess.Popen([compiler_location, "user_terminal/scheduler.py"])
        st.write("Market started.")

    else:
        st.write("Market is already running.")

# Stop market function
def stop_market():
    if st.session_state.process_handle is not None:
        # Terminate the process
        st.session_state.process_handle.terminate()
        st.session_state.process_handle = None
        st.write("Market stopped.")
    else:
        st.write("Market is not running.")

tile4 = st.container(height=220)
tile4.title("Macro event")
start, stop ,reset= tile4.columns([1, 1,1])
with start:
    if st.button("start market",use_container_width=True):
        start_market()
with stop:
    if st.button("stop market",use_container_width=True):
        stop_market()
with reset:
    if st.button("reset market", use_container_width=True):
        print("reset")
        subprocess.run([compiler_location,"user_terminal/reset.py"])

col1, col2, col3, col4 = tile4.columns([1, 1, 1, 1])
with col1:
    if st.button("macro 1",use_container_width=True):
        pass
with col2:
    if st.button("macro 2",use_container_width=True):
        pass
with col3:
    if st.button("macro 3",use_container_width=True):
        pass
with col4:
    if st.button("macro 4",use_container_width=True):
        pass

name = [row[0] for row in curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
stock = st.selectbox("Select which stock you would like to use the strategy on", name)
# nicegui_url = "http://localhost:808"+str(name.index(stock))
# components.iframe(nicegui_url, height=600, scrolling=False)

try:
    data={"bid": [row[0] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "ask":[row[1] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "last trade price":[row[2] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()],
          "time":[row[3] for row in curs_stock.execute(f"SELECT * FROM [{stock}]").fetchall()]}


    chart_data = pd.DataFrame( data)
    chart_data.set_index('time', inplace=True)
    st.line_chart(chart_data, height=570,use_container_width=True,color=["#ffffff","#000000","#c4a466"])

except:
    space_fill=st.container(height=570)
    space_fill.title("Loading...")

row1col1,row1col2 = st.columns([3,2])
def tuple_to_array(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( x )
        array.append( temp )  #3D array
    return array
def tuple_to_array_str(tuple):
    array=[]
    for data in  tuple:
        temp = []  # creates 2d array for all credentials
        for x in data:
            temp.append( str(x) )
        array.append( temp )  #3D array

    return array



with row1col1:
    tile11 = row1col1.container(height=750)

    table_names = [row[0] for row in
                   curs_stock.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    # User selects the stock table
    selected_stock = tile11.selectbox("Select which stock you would like to use the strategy on", table_names, key="50")

    # Fetch data for each column
    try:
        bid_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_prices = [row[3] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
        bid_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='buy' ORDER BY ask_bid_price_per_share DESC").fetchall()]
        ask_volumes = [row[4] for row in curs_exchange.execute(
            f"SELECT * FROM active_orders WHERE stock='{selected_stock}' AND buy_or_sell='sell' ORDER BY ask_bid_price_per_share ASC").fetchall()]
    except sqlite3.Error as e:
        tile11.warning("Loading....")
    # Sorting and preparing the data is now handled by the SQL queries
    try:
        # Plotting the data
        fig, ax = plt.subplots()

        # Plot the bid data
        ax.fill_between(bid_prices, bid_volumes, color='green', alpha=0.5, step='post', label='Bid')

        # Plot the ask data
        ax.fill_between(ask_prices, ask_volumes, color='red', alpha=0.5, step='post', label='Ask')

        # Formatting the plot
        ax.set_xlabel('Price')
        ax.set_ylabel('Volume')
        ax.set_title(f'Bid-Ask Spread for {selected_stock}')
        ax.legend()

        ax.grid(True)

        # Display the plot in Streamlit
        tile11.pyplot(fig)

    except:
        tile11.warning("Loading....")
    try:
        buy_volume = curs_exchange.execute(
            "SELECT SUM(quantity) FROM active_orders WHERE buy_or_sell='buy'"
        ).fetchone()[0] or 0

        sell_volume = curs_exchange.execute(
            "SELECT SUM(quantity) FROM active_orders WHERE buy_or_sell='sell'"
        ).fetchone()[0] or 0

        total_volume = buy_volume + sell_volume
        buy_percentage = (buy_volume / total_volume) * 100 if total_volume != 0 else 0
        sell_percentage = (sell_volume / total_volume) * 100 if total_volume != 0 else 0
        tile11.write(f"Buyers to Sellers Ratio: {buy_volume / sell_volume if sell_volume != 0 else float('inf'):.10f}")
    except sqlite3.Error as e:
        st.warning("Loading....")

with row1col2:
    tile12 = row1col2.container(height=750)
    tile12.title("12 view strategy")

    tile12.write()
    strat=[]
    for user in [row[0] for row in curs_credentials.execute("SELECT username From Credentials").fetchall()]:
        try:
            conn_user=sqlite3.connect("user_terminal/"+user+"/"+user+".db")
            curs_user = conn_user.cursor()
            for x in (tuple_to_array_str(curs_user.execute("SELECT * from strategy").fetchall())):
                x.insert(0,user)
                strat.append(x)
        except:
            tile12.warning("Loading....")
    df = pd.DataFrame(strat)
    tile12.dataframe(df, use_container_width=True )






tile22 = st.container(height=710)
tile22.title("Bid-Ask spread")
tab1, tab2 = tile22.tabs(["active orders", "past orders"])

with tab1:
    df = pd.DataFrame(curs_exchange.execute("SELECT * FROM active_orders ORDER BY ROWID DESC").fetchall())

    st.dataframe(df,use_container_width=True, hide_index=True)

with tab2:
    df = pd.DataFrame(curs_exchange.execute("SELECT * FROM past_orders ORDER BY ROWID DESC").fetchall())

    st.dataframe(df,use_container_width=True, hide_index=True)

# URL where NiceGUI is hosted

