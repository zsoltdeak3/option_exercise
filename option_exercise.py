# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>IM_SINGLE_POSITION - QCCP</p>", unsafe_allow_html=True)
st.sidebar.selectbox("Client option exercise approach",("Random scatter","Pro rata"))

qccp_margins = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'LONG':[1000, 180, 130], 'SHORT':[950, 190, 145]})
qccp_margins = qccp_margins.set_index('SYMBOL')
st.session_state['qccp_margins'] = st.sidebar.data_editor(qccp_margins, disabled=('SYMBOL'), use_container_width=True)
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>ITD THEORETICAL PRICES - MITCH</p>", unsafe_allow_html=True)
theor_prices = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'THEORETICAL PRICE':[9500., 5.3, 3.2],
                            'CONTRACT SIZE':[1000, 5, 5]})
theor_prices = theor_prices.set_index('SYMBOL')
st.session_state['theor_prices'] = st.sidebar.data_editor(theor_prices, disabled=('SYMBOL', 'CONTRACT SIZE'))
