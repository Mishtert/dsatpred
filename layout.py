import pandas as pd
import streamlit as st
import SessionState
import input_output as io
import base64
from io import BytesIO
from pathlib import Path
import time
import gc
import layout as lt

gc.enable()


def reverse_sidebar():
    """
    function to reverse sidebar position

    """
    html = """
      <style>
        .reportview-container {
          flex-direction: row-reverse;
        }

        header > .toolbar {
          flex-direction: row-reverse;
          left: 1rem;
          right: auto;
        }

        .sidebar .sidebar-collapse-control,
        .sidebar.--collapsed .sidebar-collapse-control {
          left: auto;
          right: 0.3rem;
        }

        .sidebar .sidebar-content {
          transition: margin-right .3s, box-shadow .3s;
        }

        .sidebar.--collapsed .sidebar-content {
          margin-left: auto;
          margin-right: -21rem;
        }

        @media (max-width: 991.98px) {
          .sidebar .sidebar-content {
            margin-left: auto;
          }
          .sidebar.sidebar-width{
            8px
          }
        }
      </style>
    """
    st.markdown(html, unsafe_allow_html=True)


st.cache()


def display_app_header(main_txt, sub_txt, is_sidebar=False):
    """
    function to display major headers at user interface
    Parameters
    ----------
    main_txt: str -> the major text to be displayed
    sub_txt: str -> the minor text to be displayed
    is_sidebar: bool -> check if its side panel or major panel
    """

    html_temp = f"""
    <div style = "background.color:#2484BF; padding:1px">
    <h1 style = "color:white; text_align:center;"> {main_txt} </h1>
    <p style = "color:white; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html=True)
    else:
        st.markdown(html_temp, unsafe_allow_html=True)


def display_side_panel_header(txt):
    """
    function to display minor headers at side panel
    Parameters
    ----------
    txt: str -> the text to be displayed
    """
    st.sidebar.markdown(f'## {txt}')


# session state
ss = SessionState.get(output_df=pd.DataFrame(),
                      df_raw=pd.DataFrame(),
                      _model=None,
                      text_col='text',
                      is_file_uploaded=False,
                      to_download_report=False,
                      df=pd.DataFrame(),
                      txt='Paste the text to analyze here',
                      default_txt='Paste the text to analyze here',
                      pred_df=None)


def display_header(header):
    """
    function to display minor headers at user interface main panel
    Parameters
    ----------
    header: str -> the major text to be displayed
    """

    # view clean data
    html_temp = f"""
    <div style = "background.color:#070E44; padding:8px">
    <h4 style = "color:white;text_align:center;"> {header} </h5>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)


def space_header():
    """
    function to create space using html
    Parameters
    ----------
    """
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.cache()


def check_input_method(data_input_mthd):
    """
    function check user input method if uploading or pasting
    Parameters
    ----------
    data_input_mthd: str -> the default displayed text for decision making
    """

    if data_input_mthd == 'Copy-Paste text':
        df, ss.txt = io.get_input(ss_text=ss.txt)

    else:
        df, ss.txt = io.get_input(is_batch=True, ss_text=ss.txt)
        if df.shape[0] > 0:
            # ss.is_batch_process = True
            ss.is_file_uploaded = True

    return df, ss.txt


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="Report.csv" >Download csv file</a>'

    return href

