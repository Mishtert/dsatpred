import streamlit as st
import layout as lt
import predict
import base64
import SessionState
import input_output as io
import base64


import streamlit as st
# Importing module and initializing setup
from pycaret.classification import *
# Import basic libraries
import pandas as pd
import numpy as np
import my_utility as mr


LOGO_IMAGE = "logo.png"
st.markdown(
    """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float:right;
        }
        </style>
        """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
        <div class="container">
            <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
       </div>
        """,
    unsafe_allow_html=True
)

hide_footer_style = """
<style>
.reportview-container .main footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

# reverse sidebar
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


# # Main panel title
# display_app_header(main_txt='Voice of Customer Analytics',
#                    sub_txt='Understand Survey Return Verbatim or Customer Feedback !!!')
# Side panel title
display_app_header(main_txt='Navigation ', sub_txt='Select Options as Required', is_sidebar=True)

# display_side_panel_header(txt='Select:')
data_input_mthd = st.sidebar.radio("Select Data Input Method", ('Copy-Paste text', 'Upload a CSV file'))

#Credits
st.sidebar.subheader("About App")
st.sidebar.text("Understand Quality of Interaction")
st.sidebar.text("Proactively Manage Customer Experience")
st.sidebar.subheader("Design & Development")
st.sidebar.text("Mishtert T")


# Loading the saved model
dt_saved = load_model('dt_saved_02232021')

ss.df, ss.txt = check_input_method(data_input_mthd)





################### Downloading Section ###########################
if ss.to_download_report:
    lt.display_header(header='Download Report Section')  # Report Section header
    lt.space_header()
    # button_download = st.button('Generate CSV File')
    st.info('File successfully generated, click the links below to download.')
    st.markdown(lt.get_table_download_link(lt.ss.pred_df), unsafe_allow_html=True)
