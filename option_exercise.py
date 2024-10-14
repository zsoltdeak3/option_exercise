# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:30:40 2024

@author: zsolt
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

def moneyness (option_type,strike,edsp):
  ITM = False
  if option_type == 'Call':
    int_val = edsp-strike
  else:
    int_val = strike-edsp
  mon = int_val/strike
  if int_val > 0:
    ITM = True
  return int_val, mon, ITM

#st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
st.session_state['example'] = st.sidebar.selectbox("Type of example",("Single instrument","Multi instrument"),index=0)

if st.session_state['example'] == "Single instrument":

  st.session_state['method'] = st.sidebar.selectbox("Client option exercise approach",("Pro rata","Random scatter"),index=0)
  
  threshold = st.sidebar.number_input('Exercise threshold (%)',min_value=0.0, value=1.0, step=0.1,format="%.1f")

  ###Editable option attributes###
  st.sidebar.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Option Attributes</p>", unsafe_allow_html=True)
  instrument = pd.DataFrame({'Attribute':['Symbol','Type','Contract size','Strike','Underlying', 'EDSP'],'Value':['Opt1','Call',1000,500,'Und1',1200]})
  st.session_state['instrument'] = st.sidebar.data_editor(instrument,hide_index=True, disabled=['Attribute'], use_container_width=True)

  ###Let's calculate option parameters###
  option_type = st.session_state['instrument'][st.session_state['instrument']['Attribute'] == 'Type']['Value'].values[0]
  strike = float(st.session_state['instrument'][st.session_state['instrument']['Attribute'] == 'Strike']['Value'].values[0])
  settlement_price = float(st.session_state['instrument'][st.session_state['instrument']['Attribute'] == 'EDSP']['Value'].values[0])
  intrinsic, moneyess_perc, inthemoney = moneyness(option_type,strike,settlement_price)
  moneyess_perc = round(moneyess_perc*100,2)

  settlement_parameters = pd.DataFrame({'Attribute':['Moneyness','Intrinsic value','Is in the money'],'Value':[f'{moneyess_perc}%',intrinsic,inthemoney]})
  st.session_state['settlement_parameters'] = st.sidebar.data_editor(settlement_parameters,hide_index=True, disabled=(['Attribute','Value']), use_container_width=True)
  
  #Client positions
  c1, c2, c3 = st.columns([1,3,1])
  st.session_state['client_pos'] = pd.DataFrame({'Client':['Client1', 'Client2', 'Client3', 'Client4'], 'SYMBOL':['Opt1', 'Opt1', 'Opt1', 'Opt1'], 'Net position':[10, 10, -15,-12]})
  st.session_state['client_pos_woi'] = st.session_state['client_pos'].set_index('Client')
  c2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Client Positions</p>", unsafe_allow_html=True)
  c2.data_editor(st.session_state['client_pos_woi'], disabled=(['SYMBOL','Client']), use_container_width=True)

  #CCP position
  st.session_state['net_client_pos'] = st.session_state['client_pos']['Net position'].sum()
  st.session_state['ccp_pos'] = pd.DataFrame({'CCP account':['Net omnibus'], 'SYMBOL':['Opt1'], 'Net position': [st.session_state['net_client_pos']]})
  st.session_state['ccp_pos_woi'] = st.session_state['ccp_pos'].set_index('CCP account')
  c2.data_editor(st.session_state['ccp_pos_woi'],disabled=(['CCP account','SYMBOL','Net position']),use_container_width=True)

  exercise_button = c2.button(label='Settlement calculation')
  if exercise_button:

    colu1, colu2 = st.columns([1,1])
    #First part left
    if moneyess_perc >= threshold:
      colu1.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>CCP settlement</p>", unsafe_allow_html=True)
      st.session_state['ccp_settlement'] = round(st.session_state['net_client_pos'] * intrinsic,2)
      st.session_state['pre_ccp_pos2'] = pd.DataFrame({'Moneyness':[f'{moneyess_perc}%'],'Settlement':[st.session_state['ccp_settlement']]})
      st.session_state['ccp_pos2'] = pd.concat([st.session_state['ccp_pos'],st.session_state['pre_ccp_pos2']],axis=1).set_index('CCP account')
      st.session_state['ccp_pos2'] = colu1.dataframe(st.session_state['ccp_pos2'], use_container_width=True)
      
      #First part right
      colu2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Broker settlement</p>", unsafe_allow_html=True)
   
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
  c1, c2, c3 = st.columns([1,3,1])
  client_pos = pd.DataFrame({'Client':['Client1', 'Client2', 'Client3', 'Client4'], 'SYMBOL':['Opt1', 'Opt1', 'Opt1', 'Opt1'], 'Net position':[10, 10, -15,-12]})
  client_pos = client_pos.set_index('Client')
  c2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Client Positions</p>", unsafe_allow_html=True)
  st.session_state['client_pos'] = c2.data_editor(client_pos, disabled=(['SYMBOL','Client']), use_container_width=True)
