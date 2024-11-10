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
    ITM = moneyness_perc > 0
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

  #settlement_parameters = pd.DataFrame({'Attribute':['Moneyness','Intrinsic value','Is in the money'],'Value':[f'{moneyess_perc}%',intrinsic,inthemoney]})
  #st.session_state['settlement_parameters'] = st.sidebar.data_editor(settlement_parameters,hide_index=True, disabled=(['Attribute','Value']), use_container_width=True)

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
        <b>Step 1:</b> BO system receives the instrument details in the morning through MITCH. Some of the details must be decoded from the SYMBOL (please see TOM doc) </div>
    """,unsafe_allow_html=True)
    
  ###Editable option attributes###
  st.markdown("<p style='text-align: center; margin-top: 15px; margin-bottom: 5px;'font-size:16px;'>Instrument details (editable)</p>", unsafe_allow_html=True)
  instruments = pd.DataFrame({'SYMBOL':['Opt1'], 'Type':['Call'], 'Contract size':[1000], 'Strike':[500],'Underlying':['ABC']})
  instruments = instruments.set_index('SYMBOL')
  st.session_state['instruments'] = st.data_editor(instruments, disabled=('SYMBOL'), use_container_width=True)
    
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
        <b>Step 2:</b> QCCP disseminates the Option EDSP prices through sFTP report after 12:15pm </div>
    """,unsafe_allow_html=True)

  c1, c2, c3 = st.columns([1,3,1])
  
  #     EDSP
  edsp_df = pd.DataFrame({'Underlying':['ABC'], 'EDSP':[1000]}).set_index('Underlying')
  c2.markdown(
    """
    <p style="text-align: center; margin-top: 15px; margin-bottom: 5px; font-size: 16px;">
        Option expiry settlement prices - EDSP (editable)
    </p>
    """,
    unsafe_allow_html=True)
  st.session_state['edsp_df'] = c2.data_editor(edsp_df, use_container_width=True)

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
        <b>Step 3:</b> As trading stops with expiring instruments at 12:15pm, the final positions are known for both client and house accounts. The decision to exercise or not can be made. </div>
    """,unsafe_allow_html=True)

  #   Broker positions

  st.markdown("<p style='text-align: center; margin-top: 15px; margin-bottom: 5px;'font-size:16px;'>Broker Positions in BO system (editable)</p>", unsafe_allow_html=True)
  
  broker_pos = {'Account':['Client1', 'Client2', 'Client3', 'Client4','House'],'Account type':['Client', 'Client', 'Client', 'Client','House'], 'Symbol':['Opt1', 'Opt1', 'Opt1', 'Opt1','Opt1'], 'Net position':[10, 10, -15,-12, 19]}
  broker_pos = pd.DataFrame(broker_pos).set_index('Account')
  
  st.session_state['broker_pos'] = st.data_editor(broker_pos, disabled=(['SYMBOL','Client']), use_container_width=True)
  # st.session_state['broker_pos'].update(edited_broker_pos.reset_index())
  #   CCP position

  st.markdown("<p style='text-align: center; margin-top: 15px; margin-bottom: 5px;'font-size:16px;'>Broker Positions in CCP (non-editable)</p>", unsafe_allow_html=True)
  
  st.session_state['net_client_pos'] = st.session_state['broker_pos'][st.session_state['broker_pos']['Account type'] == 'Client']['Net position'].sum()
  st.session_state['net_house_pos'] = st.session_state['broker_pos'][st.session_state['broker_pos']['Account type'] == 'House']['Net position'].sum()

  ccp_pos = {'Account':['Client', 'House'],'Account type':['Net omnibus', 'House'], 'SYMBOL':['Opt1','Opt1'], 'Net position': [st.session_state['net_client_pos'],st.session_state['net_house_pos']]}
  st.session_state['ccp_pos'] = pd.DataFrame(ccp_pos)
  edited_ccp_pos = st.data_editor(st.session_state['ccp_pos'].set_index('Account'),disabled=(['CCP account','SYMBOL','Net position']),use_container_width=True)
  st.session_state['ccp_pos'].update(edited_ccp_pos)

  ### To decide if options should be exercised ###
  st.markdown(
    """
    <div style="
        background-color: #f0f0f0;
        margin-bottom: 10px;
        padding: 10px; 
        border-radius: 10px;
        text-align: center;
        color: black;
        font-size: 18px;
        border: 1px solid #ddd;">
        <b>Step 4:</b> Determine whether to exercise options. </div>
    """,unsafe_allow_html=True)
    #Empty line
  moneyness_df = st.session_state['broker_pos'].set_index('Symbol').join(st.session_state['instruments'][['Strike', 'Contract size']], how='left')
  moneyness_df = moneyness_df.join(st.session_state['edsp_df'][['EDSP']], how='left')
  moneyness_df ['Moneyness'] = np.divide(moneyness_df['Strike'],moneyness_df['EDSP'])
  moneyness_df = moneyness_df.reset_index(drop=False)
  st.dataframe(moneyness_df, hide_index=True)
  ifexercise = st.button(label='Decide if exercise')  
  st.markdown("<p style='text-align: center; margin-top: 5px; margin-bottom: 5px;'font-size:16px;", unsafe_allow_html=True)
  
  if ifexercise:
      
      ###Let's calculate option parameters###
      
      option_type = st.session_state['instrument'].loc['Type','Value']
      strike = float(st.session_state['instrument'].loc['Strike','Value'])
      settlement_price = float(st.session_state['instrument'].loc['EDSP','Value'])
      intrinsic, moneyess_perc, inthemoney = moneyness(option_type,strike,settlement_price)
      moneyess_perc = round(moneyess_perc*100,2)
      
      st.table(st.session_state['broker_pos'])

    
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
        <b>Step 5:</b> Calculate settlement flows. </div>
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
