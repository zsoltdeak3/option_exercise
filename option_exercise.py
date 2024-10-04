# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

def moneyness (type,strike,edsp):
  ITM = False
  if type == 'Call':
    int_val = edsp-strike
  else:
    int_val = strike-edsp
  mon = int_val/strike
  if int_val > 0:
    ITM = True

st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
st.session_state['method'] = st.sidebar.selectbox("",("Pro rata","Random scatter"),index=0)

st.sidebar.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Settlement prices</p>", unsafe_allow_html=True)
edsp = pd.DataFrame({'SYMBOL':['Und1', 'Und2'], 'EDSP':[1000,1200]})
edsp = edsp.set_index('SYMBOL')
st.session_state['edsp'] = st.sidebar.data_editor(edsp, disabled=('SYMBOL'), use_container_width=True)

threshold = st.sidebar.number_input('Exercise threshold', value=1, step=0.1,format="%.1f")

st.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Intstrument attributes</p>", unsafe_allow_html=True)
instruments = pd.DataFrame({'SYMBOL':['Opt1', 'Opt2', 'Opt3', 'Opt4'], 'Type':['Call', 'Call', 'Put','Put'], 'Contract size':[1000, 1000, 1000,1000], 'Strike':[500,400,300,200],'Underlying':['Und1','Und1','Und2','Und2']})
instruments = instruments.set_index('SYMBOL')
st.session_state['instruments'] = st.data_editor(instruments, disabled=('SYMBOL'), use_container_width=True)
