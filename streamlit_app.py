# Data manipulation
import numpy as np
import datetime as dt
import pandas as pd
import geopandas as gpd

# Database and file handling
import os

# Data visualization
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import ollama

import streamlit as st

from bokeh.plotting import figure
from streamlit_bokeh import streamlit_bokeh

path_cda = '\\CuriosityDataAnalytics'
path_wd = path_cda + '\\wd'
path_data = path_wd + '\\data'

# App config
#----------------------------------------------------------------------------------------------------------------------------------#
# Page config
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    img[data-testid="stLogo"] {
                height: 6rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title("What's new in Streamlit 1.43?")
st.divider()

with st.sidebar:
    st.logo(path_cda + '\\logo.png', size='large')
    st.empty()
#
#

def page1():
    st.header(':one: st.chat_input accept files')

    with st.expander('Chatbot Code'):
        st.code('''
    import streamlit as st
    import pandas as pd
    import ollama

    sel_accept_file = st.pills('accept_file=', [False, True, 'multiple'])
    sel_file_type = st.pills('file_Type=', [None, 'csv', 'png'])

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("What can I help with?", accept_file=sel_accept_file, file_type=sel_file_type):

        text_prompt = user_prompt.text
        full_prompt = text_prompt
        if user_prompt["files"]:
            file_prompt = pd.read_csv(user_prompt.files[0])
            full_prompt = f'Question is <{text_prompt}>. File is <{file_prompt.to_dict(orient='records')}>'

        # User
        st.session_state.messages.append({"role": "user", "content": full_prompt})

        with st.chat_message("user"):
            st.markdown(text_prompt)
            if user_prompt["files"]:
                st.dataframe(file_prompt.head())

        # Model
        with st.chat_message("assistant"):
            response = ollama.chat(model='gemma2',
                                messages=[
                                        {"role": m["role"], "content": m["content"]}
                                        for m in st.session_state.messages
                                    ],
                                    stream=True)

            stream_content = ''
            def catch_stream(response):
                nonlocal stream_content
                for chunk in response:
                    stream_content += chunk['message']['content']
                    yield chunk['message']['content']

            stream = catch_stream(response)
            st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": stream_content})
        ''')

    sel_accept_file = st.pills('accept_file=', [False, True, 'multiple'])
    sel_file_type = st.pills('file_Type=', [None, 'csv', 'png'])

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("What can I help with?", accept_file=sel_accept_file, file_type=sel_file_type):

        text_prompt = user_prompt.text
        full_prompt = text_prompt
        if user_prompt["files"]:
            file_prompt = pd.read_csv(user_prompt.files[0])
            full_prompt = f'Question is <{text_prompt}>. File is <{file_prompt.to_dict(orient='records')}>'

        # User
        st.session_state.messages.append({"role": "user", "content": full_prompt})

        with st.chat_message("user"):
            st.markdown(text_prompt)
            if user_prompt["files"]:
                st.dataframe(file_prompt.head())

        # Model
        with st.chat_message("assistant"):
            response = ollama.chat(model='gemma2',
                                messages=[
                                        {"role": m["role"], "content": m["content"]}
                                        for m in st.session_state.messages
                                    ],
                                    stream=True)

            stream_content = ''
            def catch_stream(response):
                nonlocal stream_content
                for chunk in response:
                    stream_content += chunk['message']['content']
                    yield chunk['message']['content']

            stream = catch_stream(response)
            st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": stream_content})


def page2():
    st.header(':two: st.column_config')
    st.subheader('JSON column')

    st.code("""
        import streamlit as st

        data = {
            "managers": [
                {
                    "manager_name": "Alice Johnson",
                    "employees": ["John Smith"]
                },
                {
                    "manager_name": "Bob Harris",
                    "employees": ["Sarah Lee", "James Wilson"]
                },
                {
                    "manager_name": "Catherine Martinez",
                    "employees": ["David Thomas", "Emily White", "Michael Brown", "Linda Green"]
                }
            ]
        }

        st.dataframe(
            data,
            column_config={"json": st.column_config.JsonColumn(width="large")},
            hide_index=True,
        )

    """)
    data = {
        "managers": [
            {
                "manager_name": "Alice Johnson",
                "employees": ["John Smith"]
            },
            {
                "manager_name": "Bob Harris",
                "employees": ["Sarah Lee", "James Wilson"]
            },
            {
                "manager_name": "Catherine Martinez",
                "employees": ["David Thomas", "Emily White", "Michael Brown", "Linda Green"]
            }
        ]
    }

    st.dataframe(
        data,
        column_config={"json": st.column_config.JsonColumn(width="large")},
        hide_index=True,
    )

    st.divider()
    st.subheader('Preconfigured column format options')
    st.code("""
        import streamlit as st
        import pandas as pd

        df = pd.DataFrame([[10.999] * 10], columns=[f'col{i+1}' for i in range(10)])
        st.dataframe(df,
                    column_config={
                            "col1": st.column_config.NumberColumn(label='None', format=None),
                            "col2": st.column_config.NumberColumn(label='plain', format="plain"),
                            "col3": st.column_config.NumberColumn(label='localized', format="localized"),
                            "col4": st.column_config.NumberColumn(label='percent', format="percent"),
                            "col5": st.column_config.NumberColumn(label='dollar', format="dollar"),
                            "col6": st.column_config.NumberColumn(label='euro', format="euro"),
                            "col7": st.column_config.NumberColumn(label='accounting', format="accounting"),
                            "col8": st.column_config.NumberColumn(label='compact', format="compact"),
                            "col9": st.column_config.NumberColumn(label='scientific', format="scientific"),
                            "col10": st.column_config.NumberColumn(label='engineering', format="engineering")
                    }
        )
    
    """)
    df = pd.DataFrame([[10.999] * 10], columns=[f'col{i+1}' for i in range(10)])
    st.dataframe(df,
                 column_config={
                        "col1": st.column_config.NumberColumn(label='None', format=None),
                        "col2": st.column_config.NumberColumn(label='plain', format="plain"),
                        "col3": st.column_config.NumberColumn(label='localized', format="localized"),
                        "col4": st.column_config.NumberColumn(label='percent', format="percent"),
                        "col5": st.column_config.NumberColumn(label='dollar', format="dollar"),
                        "col6": st.column_config.NumberColumn(label='euro', format="euro"),
                        "col7": st.column_config.NumberColumn(label='accounting', format="accounting"),
                        "col8": st.column_config.NumberColumn(label='compact', format="compact"),
                        "col9": st.column_config.NumberColumn(label='scientific', format="scientific"),
                        "col10": st.column_config.NumberColumn(label='engineering', format="engineering")
                 }
    )
    st.code("""
        df = pd.DataFrame([[10.999] * 10], columns=[f'col{i+1}' for i in range(10)])
        st.dataframe(df,
                    column_config={
                            "col1": st.column_config.ProgressColumn(label='None', format=None),
                            "col2": st.column_config.ProgressColumn(label='plain', format="plain"),
                            "col3": st.column_config.ProgressColumn(label='localized', format="localized"),
                            "col4": st.column_config.ProgressColumn(label='percent', format="percent"),
                            "col5": st.column_config.ProgressColumn(label='dollar', format="dollar"),
                            "col6": st.column_config.ProgressColumn(label='euro', format="euro"),
                            "col7": st.column_config.ProgressColumn(label='accounting', format="accounting"),
                            "col8": st.column_config.ProgressColumn(label='compact', format="compact"),
                            "col9": st.column_config.ProgressColumn(label='scientific', format="scientific"),
                            "col10": st.column_config.ProgressColumn(label='engineering', format="engineering")
                    }
        )
    """)
    st.dataframe(df,
                 column_config={
                        "col1": st.column_config.ProgressColumn(label='None', format=None),
                        "col2": st.column_config.ProgressColumn(label='plain', format="plain"),
                        "col3": st.column_config.ProgressColumn(label='localized', format="localized"),
                        "col4": st.column_config.ProgressColumn(label='percent', format="percent"),
                        "col5": st.column_config.ProgressColumn(label='dollar', format="dollar"),
                        "col6": st.column_config.ProgressColumn(label='euro', format="euro"),
                        "col7": st.column_config.ProgressColumn(label='accounting', format="accounting"),
                        "col8": st.column_config.ProgressColumn(label='compact', format="compact"),
                        "col9": st.column_config.ProgressColumn(label='scientific', format="scientific"),
                        "col10": st.column_config.ProgressColumn(label='engineering', format="engineering")
                 }
    )
    st.code("""
        df = pd.DataFrame([[dt.datetime(2025,1,1)] * 5], columns=[f'col{i+1}' for i in range(5)])
        st.dataframe(df,
                    column_config={
                            "col1": st.column_config.DatetimeColumn(label='None', format=None),
                            "col2": st.column_config.DatetimeColumn(label='localized', format="localized"),
                            "col3": st.column_config.DatetimeColumn(label='distance', format="distance"),
                            "col4": st.column_config.DatetimeColumn(label='calendar', format="calendar"),
                            "col5": st.column_config.DatetimeColumn(label='iso8601', format="iso8601")
                    }
        )  
    """)
    df = pd.DataFrame([[dt.datetime(2025,1,1)] * 5], columns=[f'col{i+1}' for i in range(5)])
    st.dataframe(df,
                 column_config={
                        "col1": st.column_config.DatetimeColumn(label='None', format=None),
                        "col2": st.column_config.DatetimeColumn(label='localized', format="localized"),
                        "col3": st.column_config.DatetimeColumn(label='distance', format="distance"),
                        "col4": st.column_config.DatetimeColumn(label='calendar', format="calendar"),
                        "col5": st.column_config.DatetimeColumn(label='iso8601', format="iso8601")
                 }
    )  
    st.code("""
        df = pd.DataFrame([[dt.datetime(2025,1,1)] * 5], columns=[f'col{i+1}' for i in range(5)])
        st.dataframe(df,
                    column_config={
                            "col1": st.column_config.DateColumn(label='None', format=None),
                            "col2": st.column_config.DateColumn(label='localized', format="localized"),
                            "col3": st.column_config.DateColumn(label='distance', format="distance"),
                            "col4": st.column_config.DateColumn(label='calendar', format="calendar"),
                            "col5": st.column_config.DateColumn(label='iso8601', format="iso8601")
                    }
        )  
    """)
    df = pd.DataFrame([[dt.datetime(2025,1,1)] * 4], columns=[f'col{i+1}' for i in range(4)])
    st.dataframe(df,
                 column_config={
                        "col1": st.column_config.DateColumn(label='None', format=None),
                        "col2": st.column_config.DateColumn(label='localized', format="localized"),
                        "col3": st.column_config.DateColumn(label='distance', format="distance"),
                        "col4": st.column_config.DateColumn(label='iso8601', format="iso8601")
                 }
    )
    st.code("""
        df = pd.DataFrame([[dt.time(11,35,00)] * 3], columns=[f'col{i+1}' for i in range(3)])
        st.dataframe(df,
                    column_config={
                            "col1": st.column_config.TimeColumn(label='None', format=None),
                            "col2": st.column_config.TimeColumn(label='localized', format="localized"),
                            "col3": st.column_config.TimeColumn(label='iso8601', format="iso8601")
                    }
        )  
    """)
    df = pd.DataFrame([[dt.time(11,35,00)] * 3], columns=[f'col{i+1}' for i in range(3)])
    st.dataframe(df,
                 column_config={
                        "col1": st.column_config.TimeColumn(label='None', format=None),
                        "col2": st.column_config.TimeColumn(label='localized', format="localized"),
                        "col3": st.column_config.TimeColumn(label='iso8601', format="iso8601")
                 }
    )  



def page3():
    st.header(':three: st.dataframe')

    df = pd.read_csv(f'{path_data}\\sample_data.csv')

    sel_row_height = st.slider('', 10, 50, 30)
    st.code("""
        import streamlit as st
        import pandas as pd

        df = pd.read_csv('sample_data.csv')

        st.dataframe(df, row_height=""" + str(sel_row_height) +""")
    """)
    st.dataframe(df, row_height=sel_row_height)


def page4():
    st.header(':four: streamlit-bokeh')
    st.code("""
        import streamlit as st
        from bokeh.plotting import figure
        from streamlit_bokeh import streamlit_bokeh

        df = pd.DataFrame({
            "Date": ["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05",
                    "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09", "2024-03-10"],
            "Stock A": [100, 102, 98, 105, 107, 110, 108, 112, 115, 118],
            "Stock B": [95, 97, 96, 99, 101, 103, 104, 106, 109, 111]
        })

        p = figure(x_axis_label="Date", y_axis_label="Price", x_range=df["Date"].tolist(), width=100, height=30)
        p.line(df["Date"], df["Stock A"], legend_label="Stock A", line_width=2, color="blue")
        p.circle(df["Date"], df["Stock A"], size=6, color="blue", fill_alpha=0.5)
        p.line(df["Date"], df["Stock B"], legend_label="Stock B", line_width=2, color="red")
        p.square(df["Date"], df["Stock B"], size=6, color="red", fill_alpha=0.5)

        streamlit_bokeh(p, use_container_width=True, theme="streamlit", key="stock_chart")
        
    """)


    df = pd.DataFrame({
        "Date": ["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05",
                "2024-03-06", "2024-03-07", "2024-03-08", "2024-03-09", "2024-03-10"],
        "Stock A": [100, 102, 98, 105, 107, 110, 108, 112, 115, 118],
        "Stock B": [95, 97, 96, 99, 101, 103, 104, 106, 109, 111]
    })

    p = figure(x_axis_label="Date", y_axis_label="Price", x_range=df["Date"].tolist(), width=100, height=30)
    p.line(df["Date"], df["Stock A"], legend_label="Stock A", line_width=2, color="blue")
    p.circle(df["Date"], df["Stock A"], size=6, color="blue", fill_alpha=0.5)
    p.line(df["Date"], df["Stock B"], legend_label="Stock B", line_width=2, color="red")
    p.square(df["Date"], df["Stock B"], size=6, color="red", fill_alpha=0.5)

    streamlit_bokeh(p, use_container_width=True, theme="streamlit", key="stock_chart")


    


pg = st.navigation([st.Page(page1, title='st.chat_input'),
                    st.Page(page2, title='st.column_config'),
                    st.Page(page3, title='st.dataframe'),
                    st.Page(page4, title='streamlit-bokeh')])
pg.run()