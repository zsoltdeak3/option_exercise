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
    int_val = max(0, edsp - strike) if option_type == "Call" else max(0, strike - edsp)
    moneyness_perc = (int_val / strike)
    ITM = moneyness_perc > 0 if option_type == "Call" else moneyness_perc < 0
    return int_val, moneyness_perc, ITM

### SIDEBAR ###

#st.sidebar.markdown("<h4 style='text-align: center; font-size:18px; margin-bottom: -200px;'>Client option exercise approach</h4>", unsafe_allow_html=True)
st.session_state['example'] = st.sidebar.selectbox("Type of example",("Single instrument","Multi instrument"),index=0)

### SINGLE INSTRUMENT ###

if st.session_state['example'] == "Single instrument":

  st.session_state['method'] = st.sidebar.selectbox("Client option exercise approach",("Pro rata","Random scatter"),index=0)
  
  #threshold = st.sidebar.number_input('CCP exercise threshold (%)',min_value=0.0, value=1.0, step=0.1,format="%.1f")
  # Exercise fees
  CCPexercisefee = st.sidebar.number_input('CCP exercise fee (QAR)',min_value=0.00, value=0.50, step=0.01,format="%.2f")
  Brokerexercisefee = st.sidebar.number_input('Broker exercise fee (QAR)',min_value=0.00, value=0.50, step=0.01,format="%.2f")

  ###Editable option attributes###
  st.sidebar.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Option Attributes</p>", unsafe_allow_html=True)
  if 'instrument' not in st.session_state:
    instrument = {'Attribute': ['Symbol', 'Type', 'Contract size', 'Strike', 'Underlying', 'EDSP'],
                  'Value': ['Opt1', 'Call', 1000, 500, 'Und1', 1200]}
    st.session_state['instrument'] = pd.DataFrame(instrument) 
  edited_instrument = st.sidebar.data_editor(st.session_state['instrument'].set_index('Attribute'), use_container_width=True)
  st.session_state['instrument'].update(edited_instrument.reset_index())

  ###Let's calculate option parameters###
  option_type = st.session_state['instrument'].loc[1,'Value']
  strike = float(st.session_state['instrument'].loc[3,'Value'])
  settlement_price = float(st.session_state['instrument'].loc[5,'Value'])
  intrinsic, moneyess_perc, inthemoney = moneyness(option_type,strike,settlement_price)
  moneyess_perc = round(moneyess_perc*100,2)

  settlement_parameters = pd.DataFrame({'Attribute':['Moneyness','Intrinsic value','Is in the money'],'Value':[f'{moneyess_perc}%',intrinsic,inthemoney]})
  st.session_state['settlement_parameters'] = st.sidebar.data_editor(settlement_parameters,hide_index=True, disabled=(['Attribute','Value']), use_container_width=True)

  exercise_button = st.sidebar.button(label='Settlement calculation')
  
  ### MAIN SCREEN ###
  
  st.markdown(
    """
    <div style="
        background-color: #f0f0f0;
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 18px;
        border: 1px solid #ddd;">
        <b>Step 1:</b> QCCP disseminates the Option EDSP prices through sFTP report after 12:15pm </div>
    """,unsafe_allow_html=True)

  c1, c2, c3 = st.columns([1,3,1])
  
  #     EDSP

  st.session_state['edsp_df'] = pd.DataFrame({'Underlying':['ABC'], 'EDSP':[1000]})
  st.session_state['edsp_df_woi'] = st.session_state['edsp_df'].set_index('Underlying')
  c2.markdown(
    """
    <p style="text-align: center; margin-top: 15px; margin-bottom: 5px; font-size: 16px;">
        Option expiry settlement prices (EDSP)
    </p>
    """,
    unsafe_allow_html=True)
  c2.data_editor(st.session_state['edsp_df_woi'], use_container_width=True)

  st.markdown(
    """
    <div style="
        background-color: #f0f0f0;
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 18px;
        border: 1px solid #ddd;">
        <b>Step 2:</b> As trading stops with expiring instruments at 12:15pm, the final positions are known for both client and house accounts. The decision to exercise or not can be made. </div>
    """,unsafe_allow_html=True)

  #   Broker positions

  st.markdown("<p style='text-align: center; margin-top: 15px; margin-bottom: 5px;'font-size:16px;'>Broker Positions in FO system (editable)</p>", unsafe_allow_html=True)
  
  broker_pos = {'Account':['Client1', 'Client2', 'Client3', 'Client4','House'],'Account type':['Client', 'Client', 'Client', 'Client','House'], 'SYMBOL':['Opt1', 'Opt1', 'Opt1', 'Opt1','Opt1'], 'Net position':[10, 10, -15,-12, 19]}
  st.session_state['broker_pos'] = pd.DataFrame(broker_pos)
  
  edited_broker_pos = st.data_editor(st.session_state['broker_pos'].set_index('Account'), disabled=(['SYMBOL','Client']), use_container_width=True)
  st.session_state['broker_pos'].update(edited_broker_pos.reset_index())
  #   CCP position

  st.markdown("<p style='text-align: center; margin-top: 15px; margin-bottom: 5px;'font-size:16px;'>Broker Positions in CCP (non-editable)</p>", unsafe_allow_html=True)
  
  st.session_state['net_client_pos'] = st.session_state['broker_pos'][st.session_state['broker_pos']['Account type'] == 'Client']['Net position'].sum()
  st.session_state['net_house_pos'] = st.session_state['broker_pos'][st.session_state['broker_pos']['Account type'] == 'House']['Net position'].sum()

  ccp_pos = {'CCP account':['Net omnibus', 'House'], 'SYMBOL':['Opt1','Opt1'], 'Net position': [st.session_state['net_client_pos'],st.session_state['net_house_pos']]}
  st.session_state['ccp_pos'] = pd.DataFrame(ccp_pos.set_index('CCP account'))
  edited_ccp_pos = st.data_editor(st.session_state['ccp_pos'],disabled=(['CCP account','SYMBOL','Net position']),use_container_width=True)
  st.session_state['ccp_pos'].update(edited_ccp_pos.reset_index())

  ### To decide if options should be exercised ###
  st.markdown(
    """
    <div style="
        background-color: #f0f0f0;
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 18px;
        border: 1px solid #ddd;">
        <b>Step 3:</b> Determine whether to exercise options. </div>
    """,unsafe_allow_html=True)
    #Empty line
  st.markdown("<p style='text-align: center; margin-top: 5px; margin-bottom: 5px;'font-size:16px;", unsafe_allow_html=True)  
  if decision_table not in session_state:  
      decision_table = pd.concat([])  
    ### SETTLEMENT FLOWS ###
  st.markdown(
    """
    <div style="
        background-color: #f0f0f0;
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 18px;
        border: 1px solid #ddd;">
        <b>Step 4:</b> Calculate settlement flows. </div>
    """,unsafe_allow_html=True)
 
  if exercise_button:

    colu1, colu2 = st.columns([1,1])
    #First part left
    if intrinsic > CCPexercisefee:
      colu1.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>CCP settlement</p>", unsafe_allow_html=True)
      st.session_state['ccp_settlement'] = round(st.session_state['net_client_pos'] * intrinsic,2)
      st.session_state['pre_ccp_pos2'] = pd.DataFrame({'Moneyness':[f'{moneyess_perc}%'],'Settlement':[st.session_state['ccp_settlement']]})
      st.session_state['ccp_pos2'] = pd.concat([st.session_state['ccp_pos'],st.session_state['pre_ccp_pos2']],axis=1).set_index('CCP account')
      st.session_state['ccp_pos2'] = colu1.dataframe(st.session_state['ccp_pos2'], use_container_width=True)
      
      #First part right
      colu2.markdown("<p style='text-align: center; margin-bottom: -10px;'font-size:18px;'>Broker settlement</p>", unsafe_allow_html=True)

### MULTI INSTRUMENT ###
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
