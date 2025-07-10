import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

# dataframe creation

#sql connection
mydb = psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database = "phonepe_data",
                        password = "Planck00725"
                        )
cursor = mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type",
                                               "Transaction_count","Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type",
                                               "Transaction_count","Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3,columns=("States","Years","Quarter","Brands",
                                               "Transaction_count","Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4,columns=("States","Years","Quarter","District",
                                               "Transaction_count","Transaction_amount"))

#map_transactiion_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5,columns=("States","Years","Quarter","District",
                                               "Transaction_count","Transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6,columns=("States","Years","Quarter","District",
                                               "RegisteredUsers","AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes",
                                               "Transaction_count","Transaction_amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes",
                                               "Transaction_count","Transaction_amount"))

#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes",
                                               "RegisteredUsers"))



def Transaction_amount_count_Y(df, year, context="default"):

    tacy = df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg.sort_values("Transaction_amount", ascending=False), 
                        x="States", y="Transaction_amount", 
                        title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Magenta)
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=90, margin=dict(b=200))
        st.plotly_chart(fig_amount, use_container_width=True, key=f"{context}_amount_{year}_{id(df)}")

    with col2:
        fig_count = px.bar(tacyg.sort_values("Transaction_count", ascending=False), 
                        x="States", y="Transaction_count", 
                        title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl)
        fig_count.update_layout(height=650, width = 600, xaxis_tickangle=90, margin=dict(b=200))
        st.plotly_chart(fig_count, use_container_width=True, key=f"{context}_count_{year}_{id(df)}")
    
    col1 , col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.text)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale = "ylgnbu",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                    height=600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1, key=f"{context}_india_map_amount_{year}_{id(df)}")

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale = "ylgnbu",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                    height=600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2, key=f"{context}_india_map_count_{year}_{id(df)}")

    return tacy

import json
def Transaction_amount_count_Y_Q(df, quarter, context="default"):
    tacy = df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    tacyg.reset_index(inplace = True)

    col1, col2= st.columns(2)
    with col1:

        fig_amount_1 = px.bar(tacyg.sort_values("Transaction_amount", ascending=False), 
                        x="States", y="Transaction_amount", 
                        title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Burg_r, 
                            )
        fig_amount_1.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_amount_1, key=f"{context}_amount_Q{quarter}_{id(df)}")
    
    with col2:

        fig_count_1 = px.bar(tacyg.sort_values("Transaction_count", ascending=False), 
                        x="States", y="Transaction_count", 
                        title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl)
        fig_count_1.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_count_1, key=f"{context}_count_Q{quarter}_{id(df)}")


    col1 ,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.text)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1_ta = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale = "ylgnbu",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name= "States", title= f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                    height=600, width = 600)
        fig_india_1_ta.update_geos(visible = False)
        st.plotly_chart(fig_india_1_ta, key=f"{context}_india_ta_Q{quarter}_{id(df)}")

    with col2:

        fig_india_2_tc = px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale = "ylgnbu",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name= "States", title= f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                    height=600, width = 600)
        fig_india_2_tc.update_geos(visible = False)
        st.plotly_chart(fig_india_2_tc, key=f"{context}_india_tc_Q{quarter}_{id(df)}")

    return tacy


def Aggre_Tran_Transaction_Type(df, state, context="default"):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
    tacyg.reset_index(inplace = True)

    col1 ,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names= "Transaction_type", values = "Transaction_amount",
                        width = 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5)
        st.plotly_chart(fig_pie_1, key=f"{context}_pie_amount_{state}_{id(df)}")

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names= "Transaction_type", values = "Transaction_count",
                        width = 600, title= f"{state.upper()} TRANSACTION COUNT", hole = 0.5)
        st.plotly_chart(fig_pie_2, key=f"{context}_pie_count_{state}_{id(df)}")

#Aggre_user_analysis_1
def Aggre_user_plot_1(df, year):
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop = True, inplace= True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1 = px.bar(aguyg, x = "Brands", y= "Transaction_count", title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 800, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1, key=f"aggre_user_brands_{year}_{id(df)}")

    return aguy

# Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True, inplace= True)

    aguyq = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyq.reset_index(inplace= True)

    fig_bar_2 = px.bar(aguyq, x = "Brands", y= "Transaction_count", title = f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width = 800, color_discrete_sequence= px.colors.sequential.haline_r)
    st.plotly_chart(fig_bar_2, key=f"aggre_user_brands_Q{quarter}_{id(df)}")

    return aguyq

# #Aggre_user_analysis_3
# def Aggre_user_plot_3(df, state):
#     auyqs = df[df["States"] == state]
#     auyqs.reset_index(drop = True, inplace= True)

#     fig_line_2 = px.line(auyqs, x = "Brands", y= "Transaction_count", title = f"{state} BRANDS TRANSACTION COUNT, PERCENTAGE",
#                         width = 1000, hover_name= "Percentage", markers = True)
#     st.plotly_chart(fig_line_2, key=f"aggre_user_line_{state}_{id(df)}")

#     return auyqs

# Map_Insurance_District
def Map_insur_District(df, state, context="default"):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1 ,col2 = st.columns(2)
    with col1:
        fig_bar_m_1 = px.bar(tacyg, x= "Transaction_amount", y= "District", orientation= 'h', height= 600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_m_1, key=f"{context}_district_amount_{state}_{id(df)}")
    with col2:
        fig_bar_m_2 = px.bar(tacyg, x= "Transaction_count", y= "District", orientation= 'h', height= 600, 
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Agsunset)
        st.plotly_chart(fig_bar_m_2, key=f"{context}_district_count_{state}_{id(df)}")

#map_user_analysis_1
def map_user_plot_1(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop = True, inplace= True)

    muyg = pd.DataFrame(muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x = "States", y= ["RegisteredUsers", "AppOpens"], title =f"{year} REGISTEREDUSERS APPOPENS",
                        height= 800 ,width = 1000, markers = True)
    st.plotly_chart(fig_line_1, key=f"map_user_line_{year}_{id(df)}")

    return muy

#map_user_analysis_2
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace= True)

    muyqg = pd.DataFrame(muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x = "States", y= ["RegisteredUsers", "AppOpens"], title =f"{df["Years"].min()} YEARS {quarter} QUARTER REGISTEREDUSERS APPOPENS",
                        height= 800 ,width = 1000, markers = True, color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1, key=f"map_user_line_Q{quarter}_{id(df)}")

    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace= True)

    col1 ,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x= "RegisteredUsers", y="District", orientation= 'h',
                                    title= f"{states.upper()} REGISTERED USER",color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1, key=f"map_user_reg_{states}_{id(df)}")

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x= "AppOpens", y="District", orientation= 'h',
                                    title= f"{states.upper()} APPOPENS", color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2, key=f"map_user_app_{states}_{id(df)}")

    return muyqs

# top_insur_analysis
def Top_insurance_plot_1(df, state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop=True, inplace=True)
    
    # Check if filtered data is empty
    if tiy.empty:
        st.warning(f"No data found for state: {state}")
        return tiy
    
    # Group by Pincodes for summary data
    tiyg = tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Use the original data (tiy) for Quarter-based visualization
        fig_top_insur_bar_1 = px.bar(tiy, x="Quarter", y="Transaction_amount", 
                                    hover_data=["Pincodes"], height=650, width=650, 
                                    title=f"{state.upper()} TRANSACTION AMOUNT BY QUARTER",
                                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
        fig_top_insur_bar_1.update_layout(xaxis_title="Quarter", yaxis_title="Transaction Amount")
        st.plotly_chart(fig_top_insur_bar_1, key=f"top_insur_amount_{state}_{id(df)}")

    with col2:
        fig_top_insur_bar_2 = px.bar(tiy, x="Quarter", y="Transaction_count", 
                                    hover_data=["Pincodes"], height=650, width=650, 
                                    title=f"{state.upper()} TRANSACTION COUNT BY QUARTER",
                                    color_discrete_sequence=px.colors.sequential.Burgyl_r)
        fig_top_insur_bar_2.update_layout(xaxis_title="Quarter", yaxis_title="Transaction Count")
        st.plotly_chart(fig_top_insur_bar_2, key=f"top_insur_count_{state}_{id(df)}")
    

#top_user_analysis
def top_user_plot_1(df, year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace= True)

    tuyg = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1 =  px.bar(tuyg, x= "States", y="RegisteredUsers", color= "Quarter",width= 1000, height= 800,
                                    hover_name= "States", color_discrete_sequence= px.colors.sequential.Burgyl,
                                    title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1, key=f"top_user_reg_{year}_{id(df)}")

    return tuy

#top_user_analysis_2
def top_user_plot_2(df, state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop = True, inplace= True)

    fig_top_plot_2 =  px.bar(tuys, x= "Quarter", y="RegisteredUsers", color= "RegisteredUsers",width= 1000, height= 800,
                                    hover_data= "Pincodes", color_continuous_scale= px.colors.sequential.Magenta,
                                    title="REGISTEREDUSERS, PINCODES, QUARTER")
    st.plotly_chart(fig_top_plot_2, key=f"top_user_state_{state}_{id(df)}")

#sql connection
def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host= "localhost",
                            user= "postgres",
                            port= "5432",
                            database = "phonepe_data",
                            password = "Planck00725"
                            )
    cursor = mydb.cursor()

    #plot_1
    query_1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "transaction_amount"))

    col1 ,col2 = st.columns(2)
    with col1:    

        fig_amount = px.bar(df_1, hover_name= "states",
                            x="states", y="transaction_amount", 
                            title="TOP 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                            )
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=45)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount DESC
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "transaction_amount"))

    with col2:
        fig_amount_2 = px.bar(df_2, hover_name= "states",
                            x="states", y="transaction_amount", 
                            title="LAST 10 OF TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                            )
        fig_amount_2.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query_3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount;
                    '''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "transaction_amount"))

    fig_amount_3 = px.bar(df_3, hover_name= "states",
                        y="states", x="transaction_amount", orientation= 'h', 
                        title="AVERAGE OF TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        )
    fig_amount_3.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host= "localhost",
                            user= "postgres",
                            port= "5432",
                            database = "phonepe_data",
                            password = "Planck00725"
                            )
    cursor = mydb.cursor()

    #plot_1
    query_1 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "transaction_count"))

    col1 ,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, hover_name= "states",
                            x="states", y="transaction_count", 
                            title="TOP 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                            )
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=45)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count DESC
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "transaction_count"))

    with col2:
        fig_amount_2 = px.bar(df_2, hover_name= "states",
                            x="states", y="transaction_count", 
                            title="LAST 10 OF TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                            )
        fig_amount_2.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query_3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count;'''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "transaction_count"))

    fig_amount_3 = px.bar(df_3, hover_name= "states",
                        y="states", x="transaction_count", orientation= 'h', 
                        title="AVERAGE OF TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        )
    fig_amount_3.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(host= "localhost",
                            user= "postgres",
                            port= "5432",
                            database = "phonepe_data",
                            password = "Planck00725"
                            )
    cursor = mydb.cursor()

    query_1 = f'''SELECT districts, SUM("registeredusers") AS registeredusers
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY registeredusers DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("districts", "registeredusers"))

    col1 ,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, hover_name= "districts",
                            x="districts", y="registeredusers", 
                            title="TOP 10 OF REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                            )
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=45)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2 = f'''SELECT districts, SUM("registeredusers") AS registeredusers
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY registeredusers ASC
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("districts", "registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, hover_name= "districts",
                            x="districts", y="registeredusers", 
                            title="BOTTOM 10 REGISTERED USER",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                            )
        fig_amount_2.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query_3 = f'''SELECT districts, AVG("registeredusers") AS registeredusers
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY registeredusers DESC
                    LIMIT 10;
                    '''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("districts", "registeredusers"))

    fig_amount_3 = px.bar(df_3, hover_name= "districts",
                        y="districts", x="registeredusers", orientation= 'h', 
                        title="AVERAGE OF REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        )
    fig_amount_3.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name, state):
    mydb = psycopg2.connect(host= "localhost",
                            user= "postgres",
                            port= "5432",
                            database = "phonepe_data",
                            password = "Planck00725"
                            )
    cursor = mydb.cursor()

    query_1 = f'''SELECT districts, SUM("appopens") AS appopens
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY appopens DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("districts", "appopens"))
    
    col1 ,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, hover_name= "districts",
                            x="districts", y="appopens", 
                            title="TOP 10 OF APP OPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                            )
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=45)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2 = f'''SELECT districts, SUM("appopens") AS appopens
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY appopens ASC
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("districts", "appopens"))

    with col2:
        fig_amount_2 = px.bar(df_2, hover_name= "districts",
                            x="districts", y="appopens", 
                            title="BOTTOM 10 APP OPENS",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                            )
        fig_amount_2.update_layout(height=650, width = 600, xaxis_tickangle=90)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query_3 = f'''SELECT districts, AVG("appopens") AS appopens
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY appopens DESC
                    '''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("districts", "appopens"))

    fig_amount_3 = px.bar(df_3, hover_name= "districts",
                        y="districts", x="appopens", orientation= 'h', 
                        title="AVERAGE OF APP OPENS",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        )
    fig_amount_3.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(host= "localhost",
                            user= "postgres",
                            port= "5432",
                            database = "phonepe_data",
                            password = "Planck00725"
                            )
    cursor = mydb.cursor()

    query_1 = f'''SELECT states, SUM("registeredusers") AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers DESC
                    LIMIT 10;'''

    cursor.execute(query_1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns = ("states", "registeredusers"))

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, hover_name= "states",
                            x="states", y="registeredusers", 
                            title="TOP 10 OF REGISTERED USERS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                            )
        fig_amount.update_layout(height=650, width = 600, xaxis_tickangle=45)
        st.plotly_chart(fig_amount)

    #plot_2
    query_2 = f'''SELECT states, SUM("registeredusers") AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers ASC
                    LIMIT 10;'''

    cursor.execute(query_2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns = ("states", "registeredusers"))

    fig_amount_2 = px.bar(df_2, hover_name= "states",
                        x="states", y="registeredusers", 
                        title="BOTTOM 10 REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, 
                        )
    fig_amount_2.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_2)

    #plot_3
    query_3 = f'''SELECT states, AVG("registeredusers") AS registeredusers
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY registeredusers DESC
                    '''

    cursor.execute(query_3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns = ("states", "registeredusers"))

    fig_amount_3 = px.bar(df_3, hover_name= "states",
                        y="states", x="registeredusers", orientation= 'h', 
                        title="AVERAGE OF REGISTERED USERS",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, 
                        )
    fig_amount_3.update_layout(height=650, width = 600, xaxis_tickangle=90)
    st.plotly_chart(fig_amount_3)



#Streamlit

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select = option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Admin\OneDrive\Desktop\project_nemo\925868040s.png"))

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\Admin\OneDrive\Desktop\project_nemo\gettyimages-1238107792-612x612.jpg"),width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\Admin\OneDrive\Desktop\project_nemo\assam-india-may-phonepe-upi-payments-recharge-transfer-app-assam-india-may-phonepe-upi-payments-recharge-transfer-app-190812176.webp"))

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Anlaysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select the Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1 ,col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(), Aggre_insurance["Years"].min())
            
            tac_Y = Transaction_amount_count_Y(Aggre_insurance, years, "aggregated_insurance")
            
            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters, "aggre_insur_Q") 

        elif method == "Transaction Analysis":
            
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years,"aggre_trans")

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State ", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_Type(Aggre_tran_tac_Y, states, "aggre_trans_state")

            col1 , col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters, "aggre_trans_Q") 

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty ", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_Type(Aggre_tran_tac_Y_Q, states, "aggre_trans_st_ty")
            
        elif method == "User Analysis":
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(), Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)

            col1 , col2 = st.columns(2)
            with col1:

                quarters = st.slider("Select The Quarter_1", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters) 

            # col1, col2 = st.columns(2)
            # with col1:
            #     states = st.selectbox("Select The State ", Aggre_user_Y_Q["States"].unique())

            # Aggre_user_plot_3(Aggre_user_Y_Q, states)



    with tab2:
        method_2 = st.radio("Select the Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
             
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_mi", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min())
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years, "map_insur")
        
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())

            Map_insur_District(map_insur_tac_Y, states,"map_insur_st")

            col1 , col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarter_mi", map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(), map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters,"map_insur_Q") 

            col1, col2 = st.columns(2)
            with col1:
                
                states = st.selectbox("Select The State_mip ", map_insur_tac_Y["States"].unique())
            Map_insur_District(map_insur_tac_Y_Q, states,"map_insur_mip")
            
        elif method_2 == "Map Transaction":
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_mt", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min())
            map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years, "map_insur")
        
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mt", map_tran_tac_Y["States"].unique())

            Map_insur_District(map_tran_tac_Y, states ,"map_insur_st")

            col1 , col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarter_mt", map_tran_tac_Y["Quarter"].min(), map_tran_tac_Y["Quarter"].max(), map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters,"map_insur_Q") 

            col1, col2 = st.columns(2)
            with col1:
                
                states = st.selectbox("Select The State_mtp ", map_tran_tac_Y_Q["States"].unique())
            Map_insur_District(map_tran_tac_Y_Q, states,"map_insur_mip")

        elif method_2 == "Map User":
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_mu", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
            map_user_Y = map_user_plot_1(map_user, years)

            col1 , col2 = st.columns(2)
            with col1:
                
                quarters = st.slider("Select The Quarter_mu", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters) 

            col1, col2 = st.columns(2)
            with col1:
                
                states = st.selectbox("Select The State_mup ", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, states)

    with tab3:
        method_3 = st.radio("Select the Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_ti", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min())
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                    states = st.selectbox("Select The State", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", 
                                    int(top_insur_tac_Y["Quarter"].min()), 
                                    int(top_insur_tac_Y["Quarter"].max()), 
                                    int(top_insur_tac_Y["Quarter"].min()))

            top_insur_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters, "top_insur")

        elif method_3 == "Top Transaction":
           
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_tt", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min())
            top_tran_tac_Y = Transaction_amount_count_Y(top_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                
                states = st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())
            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1, col2 = st.columns(2)

            with col1:
                quarters = st.slider("Select The Quarter", 
                                    int(top_tran_tac_Y["Quarter"].min()), 
                                    int(top_tran_tac_Y["Quarter"].max()), 
                                    int(top_tran_tac_Y["Quarter"].min()))
                
                top_tran_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)
                

        elif method_3 == "Top User":
            col1 ,col2 = st.columns(2)
            with col1:
                
                years = st.slider("Select The Year_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
            top_user_tac_Y = top_user_plot_1(top_user, years)

            col1, col2 = st.columns(2)
            with col1:
                
                states = st.selectbox("Select The State_tu", top_user_tac_Y["States"].unique())
            top_user_plot_2(top_user_tac_Y, states)

elif select == "TOP CHARTS":
    
    question = st.selectbox("Select the Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered Users of Map user",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User"
                                                    ])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
    
    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
    
    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")
    
    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
    
    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
    
    elif question == "8. Registered Users of Map user":

        states = st.selectbox("Select the State" , map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":

        states = st.selectbox("Select the State" , map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_registered_user("map_user", states)

    elif question == "10. Registered users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")