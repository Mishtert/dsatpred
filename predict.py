import streamlit as st
# Importing module and initializing setup
from pycaret.classification import *
# Import basic libraries
import pandas as pd
import numpy as np
import my_utility as mr

# Importing app libraries
import layout as lt
import os
import pickle

# Loading the saved model
dt_saved = load_model('dt_saved_02232021')
# dt_saved = pickle.load(open('dt_saved_02232021.pkl', 'rb'))


cols_to_keep = [
    'team_name',
    'disposition_code',
    'disposition_category_code',
    'account_status',
    'handled_agent',
    'customer_segment',
    'prior_transaction_status_before_contact',
    'payment_method',
    'partner_name',
    'delivery_method',
    'payer_name',
    'tenuredship',
    'contact_channel',
    'handled_site',
    'corridor',
    'nps'
]


def get_pred():
    data_input_mthd = st.sidebar.radio("Select Data Input Method", ('Upload a CSV file','Copy-Paste text'))
    if data_input_mthd == 'Copy-Paste text':
        st.info("Yet to be implemented. Please select CSV upload option")
    else:
        lt.ss.df, lt.ss.txt = lt.check_input_method(data_input_mthd)

        lt.space_header()
        data_unseen = lt.ss.df.copy()

        mr.clean_header(data_unseen)
        st.write(data_unseen.head(5))

        data_unseen.dropna(how="all", inplace=True)
        data_unseen.dropna(how='all', axis=1)
        if data_unseen.shape[0] > 0:
            data_unseen = data_unseen[data_unseen['contact_channel'] != 'email']
            data_unseen['handled_agent'] = data_unseen['handled_agent'].str.replace('@remitly.com', '')
            other_sites = ['MNL', 'MGA', 'ORK']
            data_unseen = data_unseen[~data_unseen.handled_site.isin(other_sites)]
            data_unseen = data_unseen.dropna(axis=0, subset=['handled_site'])
            data_unseen['nps'] = data_unseen['csat_survey_response_1_csat'].apply(
                lambda x: 1 if x < 3 else 0 if x > 3 else -1)
            # data_unseen = data_unseen[data_unseen['nps'] != -1]
            print(data_unseen.shape)

            data_unseen = data_unseen[cols_to_keep]

            # generate predictions on unseen data
            predictions = predict_model(dt_saved, data=data_unseen, probability_threshold=0.184)

            st.success('Potential Customer Experience Predicted!!!')
            st.write(predictions.head(5))

            #drop score column


            lt.display_header(
                header='Statistics on predicted data')  # Raw data header
            lt.space_header()
            ## Statistics on predicted data
            dsat_pred_tp = predictions[(predictions['nps'] == 1) & (predictions['Label'] == 1)]
            dsat_pred_fp = predictions[(predictions['nps'] == 0) & (predictions['Label'] == 1)]
            dsat_pred_fn = predictions[(predictions['nps'] == 1) & (predictions['Label'] == 0)]
            dsat_pred_tn = predictions[(predictions['nps'] == 0) & (predictions['Label'] == 0)]

            actual_dsat = (len(predictions[predictions['nps'] == 1]) / len(data_unseen)) * 100
            actual_csat = (len(predictions[predictions['nps'] == 0]) / len(data_unseen)) * 100
            actual_neutral = (len(predictions[predictions['nps'] == -1]) / len(data_unseen)) * 100

            neutral_as_dsat = predictions[(predictions['nps'] == -1) & (predictions['Label'] == 1)]
            neutral_as_csat = predictions[(predictions['nps'] == -1) & (predictions['Label'] == 0)]

            neutral_as_dsat_percent = (len(neutral_as_dsat) / len(data_unseen)) * 100
            neutral_as_csat_percent = (len(neutral_as_csat) / len(data_unseen)) * 100

            tp_percent = (len(dsat_pred_tp) / len(data_unseen)) * 100
            fp_percent = (len(dsat_pred_fp) / len(data_unseen)) * 100
            fn_percent = (len(dsat_pred_fn) / len(data_unseen)) * 100
            tn_percent = (len(dsat_pred_tn) / len(data_unseen)) * 100

            st.write('True Positive : Actual NPS - Detractor | Predicted NPS - Detractor')
            st.write('False Positive: Actual NPS - Promoter  | Predicted NPS - Detractor')
            st.write('False Negative: Actual NPS - Detractor | Predicted NPS - Promoter')
            st.write('True Negative : Actual NPS - Promoter  | Predicted NPS - Promoter \n')

            st.write('Actual Detractor Percent:', round(actual_dsat, 2))
            st.write('Actual Promoter Percent:', round(actual_csat, 2))
            st.write('Actual Neutral Percent:', round(actual_neutral, 2), '\n')

            st.write('True Positive Percent(Correctly Identified as DSATs):', round(tp_percent, 2))
            # st.write('False Positive Percent:', round(fp_percent, 2))
            st.write('False Negative Percent(Incorrectly Identified as CSATs):', round(fn_percent, 2))
            # st.write('True Negative Percent:', round(tn_percent, 2), '\n')

            # st.markdown('**One of The Potential Reasons for High False Positives**')
            # st.write('Neutrals Predicted as Detractor:', round(neutral_as_dsat_percent, 2))
            # st.write('Neutrals Predicted as Promoter:', round(neutral_as_csat_percent, 2), '\n')

            lt.ss.pred_df = predictions
            lt.ss.to_download_report = True

            ################### Downloading Section ###########################
            if lt.ss.to_download_report:
                lt.display_header(header='Download Report Section')  # Report Section header
                lt.space_header()
                # button_download = st.button('Generate CSV File')
                st.info('File successfully generated, click the links below to download.')
                st.markdown(lt.get_table_download_link(lt.ss.pred_df), unsafe_allow_html=True)

    return


def write():
    get_pred()
    st.success('success!!')
