import streamlit as st
import pandas as pd
import numpy as np

st.session_state['ID'] = 0
st.set_page_config(
    layout="wide",
)
st.session_state['calc_type'] = st.selectbox('TYPE OF CALCULATION', options=['ItD', 'EoD'], index=0)

##### MARGIN PARAMETERS #####
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>IM_SINGLE_POSITION - QCCP</p>", unsafe_allow_html=True)
qccp_margins = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'LONG':[1000, 180, 130], 'SHORT':[950, 190, 145]})
qccp_margins = qccp_margins.set_index('SYMBOL')
st.session_state['qccp_margins'] = st.sidebar.data_editor(qccp_margins, disabled=('SYMBOL'), use_container_width=True)
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>ITD THEORETICAL PRICES - MITCH</p>", unsafe_allow_html=True)

