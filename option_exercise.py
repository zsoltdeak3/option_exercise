# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
st.session_state['method'] = st.sidebar.selectbox("",("Pro rata","Random scatter"),index=0)

st.sidebar.markdown("<p style='text-align: center; margin-bottom: -30px;'font-size:18px;'>Intstrument attributes</p>", unsafe_allow_html=True)
instruments = pd.DataFrame({'SYMBOL':['Opt1', 'Opt2', 'Opt3', 'Opt4'], 'Type':['Call', 'Call', 'Put','Put'], 'Contract multiplier':[1000, 1000, 1000,1000]})
instruments = instruments.set_index('SYMBOL')
st.session_state['instruments'] = st.sidebar.data_editor(instruments, disabled=('SYMBOL'), use_container_width=True)

st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>Prices</p>", unsafe_allow_html=True)
instruments = pd.DataFrame({'SYMBOL':['Opt1', 'Opt2', 'Opt3', 'Opt4'], 'Type':['Call', 'Call', 'Put','Put'], 'Contract multiplier':[1000, 1000, 1000,1000]})
instruments = instruments.set_index('SYMBOL')
st.session_state['instruments'] = st.sidebar.data_editor(instruments, disabled=('SYMBOL'), use_container_width=True)
