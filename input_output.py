import streamlit as st
import pandas as pd


def get_input(ss_text, is_batch=False, text_column="text"):
    """
    function get input from user either by uploading a csv file of  pasting text
    Parameters
    ----------
    ss_text: string
    is_batch: bool
    text_column: str -> the columnn name for creating pd.DataFrame is _is_batch is False
    """
    if is_batch:
        uploaded_file = st.file_uploader("Choose a CSV file to upload", type="csv")

        if uploaded_file is not None:
            st.success('File successfully uploaded!!!')
            df = pd.read_csv(uploaded_file)
            return df, ss_text
        else:
            st.info('Kindly upload a csv file')
            return pd.DataFrame(), ss_text

    else:
        ss_text = st.text_area('Text to analyze', ss_text)
        df = pd.DataFrame(data=[ss_text], columns=[text_column])
        return df, ss_text
