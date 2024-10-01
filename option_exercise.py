# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
add_selectbox = st.sidebar.selectbox("",("Pro rata","Random scatter"),index=0)

st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>Intstrument attributes</p>", unsafe_allow_html=True)
instruments = pd.DataFrame({'SYMBOL':['Opt1', 'Opt2', 'Opt3', 'Opt4'], 'Type':['Call', 'Call', 'Put','Put'], 'Contract multiplier':[1000, 1000, 1000,1000]})
instruments = intstruments.set_index('SYMBOL')
st.session_state['instruments'] = st.sidebar.data_editor(instruments, disabled=True, use_container_width=True)

st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>ITD THEORETICAL PRICES - MITCH</p>", unsafe_allow_html=True)
theor_prices = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'THEORETICAL PRICE':[9500., 5.3, 3.2],
                            'CONTRACT SIZE':[1000, 5, 5]})
theor_prices = theor_prices.set_index('SYMBOL')
st.session_state['theor_prices'] = st.sidebar.data_editor(theor_prices, disabled=('SYMBOL', 'CONTRACT SIZE'))
