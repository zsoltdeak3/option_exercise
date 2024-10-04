# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

def moneyness (type,strike,edsp):
  ITM = False
  if type == 'Call':
    int_val = edsp-strike
  else:
    int_val = strike-edsp
  mon = int_val/strike
  if int_val > 0:
    ITM = True

#st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
st.session_state['example'] = st.sidebar.selectbox("Type of example",("Single instrument","Multi instrument"),index=0)

if st.session_state['example'] == "Single instrument":

  st.session_state['method'] = st.sidebar.selectbox("Client option exercise approach",("Pro rata","Random scatter"),index=0)
  
  threshold = st.sidebar.number_input('Exercise threshold (%)',min_value=0.0, value=1.0, step=0.1,format="%.1f")


  st.sidebar.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Option Attributes</p>", unsafe_allow_html=True)
  instrument = pd.DataFrame({'Attribute':['Symbol','Type','Contract size','Strike','Underlying', 'EDSP'],'Value':['Opt1','Call',1000,500,'Und1',1200]})
  instrument = instrument.set_index('Attribute')
  st.session_state['instrument'] = st.sidebar.data_editor(instrument, disabled=('Attribute'), use_container_width=True)
  
  #Client positions
  c1, c2, c3 = st.columns([1,3,1])
  client_pos = pd.DataFrame({'Client':['Client1', 'Client2', 'Client3', 'Client4'], 'SYMBOL':['Opt1', 'Opt1', 'Opt1', 'Opt1'], 'Net position':[10, 10, -15,-12]})
  client_pos = client_pos.set_index('Client')
  c2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Client Positions</p>", unsafe_allow_html=True)
  st.session_state['client_pos'] = c2.data_editor(client_pos, disabled=(['SYMBOL','Client']), use_container_width=True)
else:
  
  st.session_state['method'] = st.sidebar.selectbox("Client option exercise approach",("Pro rata","Random scatter"),index=0)
  
  threshold = st.sidebar.number_input('Exercise threshold (%)',min_value=0.0, value=1.0, step=0.1,format="%.1f")
  
  col1, col2 = st.columns([2,1])
  #First part left
  col1.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Intstrument attributes</p>", unsafe_allow_html=True)
  instruments = pd.DataFrame({'SYMBOL':['Opt1', 'Opt2', 'Opt3', 'Opt4', 'Opt5', 'Opt6'], 'Type':['Call', 'Put', 'Call','Put', 'Call','Put'], 'Contract size':[1000, 1000, 1000,1000, 1000,1000], 'Strike':[500,500,500,500,500,500],'Underlying':['ABC','ABC','DEF','DEF','GHI','GHI']})
  instruments = instruments.set_index('SYMBOL')
  st.session_state['instruments'] = col1.data_editor(instruments, disabled=('SYMBOL'), use_container_width=True)
  
  #First part right
  col2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Settlement prices</p>", unsafe_allow_html=True)
  edsp = pd.DataFrame({'SYMBOL':['ABC','DEF','GHI'], 'EDSP':[1000,1200,1300]})
  edsp = edsp.set_index('SYMBOL')
  st.session_state['edsp'] = col2.data_editor(edsp, disabled=('SYMBOL'), use_container_width=True)
  
  #st.sidebar.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Settlement prices</p>", unsafe_allow_html=True)
  #edsp = pd.DataFrame({'SYMBOL':['Und1'], 'EDSP':[1000]})
  #edsp = edsp.set_index('SYMBOL')
  #st.session_state['edsp'] = st.sidebar.data_editor(edsp, disabled=('SYMBOL'), use_container_width=True)
  
  #Client positions
  c1, c2, c3 = st.columns([1,1,1])
  client_pos = pd.DataFrame({'Client':['Client1', 'Client2', 'Client3', 'Client4'], 'SYMBOL':['Opt1', 'Opt1', 'Opt1', 'Opt1'], 'Net position':[10, 10, -15,-12]})
  client_pos = client_pos.set_index('Client')
  c2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Client Positions</p>", unsafe_allow_html=True)
  st.session_state['client_pos'] = c2.data_editor(client_pos, disabled=(['SYMBOL','Client']), use_container_width=True)
