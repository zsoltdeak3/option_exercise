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
theor_prices = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'THEORETICAL PRICE':[9500., 5.3, 3.2],
                            'CONTRACT SIZE':[1000, 5, 5]})
theor_prices = theor_prices.set_index('SYMBOL')
st.session_state['theor_prices'] = st.sidebar.data_editor(theor_prices, disabled=('SYMBOL', 'CONTRACT SIZE'))
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>EOD PRICES- MITCH OR QCCP REPORTS</p>", unsafe_allow_html=True)
eod_prices = pd.DataFrame({'SYMBOL':['Future', 'Call', 'Put'], 'EOD PRICE T':[9650., 5.5, 3.1],
                          'EOD PRICE T-1':[9300., 4.1, 2.5]})
eod_prices = eod_prices.set_index('SYMBOL')
st.session_state['eod_prices'] = st.sidebar.data_editor(eod_prices, disabled=('SYMBOL'))
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>BROKER PARAMETERS - B/O</p>", unsafe_allow_html=True)
if st.session_state['calc_type'] == 'ItD':
    st.session_state['mm_buffer'] = st.sidebar.number_input(label='MM Buffer', min_value=0.,max_value=1., value=0.25, step=0.01, format='%.2f', help='MM = max(LONG, SHORT) * (1+ MM Buffer). Note that theoretical price will be added for options')
    st.session_state['im_buffer'] = st.sidebar.number_input(label='IM Buffer', min_value=st.session_state['mm_buffer'],max_value=1.,value=st.session_state['mm_buffer'], step=0.01, format='%.2f', help='IM = max(LONG, SHORT) * (1+ IM Buffer). Note that theoretical price will be added for options')
elif st.session_state['calc_type'] == 'EoD':
    st.session_state['mm_buffer'] = st.sidebar.number_input(label='MM Buffer', min_value=0.,max_value=1., value=0.25, step=0.01, format='%.2f', help='MM = max(LONG, SHORT) * (1+ MM Buffer). Note that EoD premium will be added for options')
    st.session_state['im_buffer'] = st.sidebar.number_input(label='IM Buffer', min_value=st.session_state['mm_buffer'],max_value=1.,value=st.session_state['mm_buffer'], step=0.01, format='%.2f', help='IM = max(LONG, SHORT) * (1+ IM Buffer). Note that EoD premium will be added for options')    
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>IM AND MM - COMPUTED BY B/O & SENT TO F/O</p>", unsafe_allow_html=True)
fit_margins = pd.DataFrame(st.session_state['qccp_margins'].max(axis=1))
fit_margins.columns = ['MM']
fit_margins = fit_margins.assign(**{'MM':np.multiply(fit_margins.MM, 1 + st.session_state['mm_buffer']), 'IM':np.multiply(fit_margins.MM, 1 + st.session_state['im_buffer'])})
if st.session_state['calc_type'] == 'ItD':
    fit_margins = fit_margins.assign(**{'MM':np.where(fit_margins.index=='Future', fit_margins.MM, np.add(fit_margins.MM, st.session_state['theor_prices']['THEORETICAL PRICE'])), 
                                        'IM':np.where(fit_margins.index=='Future', fit_margins.IM, np.add(fit_margins.IM, st.session_state['theor_prices']['THEORETICAL PRICE']))})
elif st.session_state['calc_type'] == 'EoD':
    fit_margins = fit_margins.assign(**{'MM':np.where(fit_margins.index=='Future', fit_margins.MM, np.add(fit_margins.MM, st.session_state['eod_prices']['EOD PRICE T'])), 
                                        'IM':np.where(fit_margins.index=='Future', fit_margins.IM, np.add(fit_margins.IM, st.session_state['eod_prices']['EOD PRICE T-1']))})   
st.session_state['fit_margins'] = fit_margins
st.sidebar.dataframe(st.session_state['fit_margins'], use_container_width=True)
st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>CLIENT  COLLATERAL - B/O & F/O</p>", unsafe_allow_html=True)
sod_collateral = pd.DataFrame({'CLIENT': ['Client 1', 'Client 2', 'Client 3'],
                              'COLLATERAL': [2000000, 2000000, 2000000]},
                            index= np.arange(3))
sod_collateral = sod_collateral.set_index('CLIENT')
st.session_state['sod_collateral'] = st.sidebar.data_editor(sod_collateral, disabled=('CLIENT'), use_container_width=True)

st.sidebar.markdown("<p style='text-align: center;'font-size:18px;'>CM COLLATERAL AT CCP</p>", unsafe_allow_html=True)
sod_collateral_ccp = pd.DataFrame({'COLLATERAL ACCOUNT': ['OSA'],
                                   'COLLATERAL': [2000000]},
                                  index= np.arange(1))
sod_collateral_ccp = sod_collateral_ccp.set_index('COLLATERAL ACCOUNT')
st.session_state['sod_collateral_ccp'] = st.sidebar.data_editor(sod_collateral_ccp, disabled=('COLLATERAL ACCOUNT'), use_container_width=True)

##### SoD OPEN POSITION #####
st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>SoD OPEN POSITION</p>", unsafe_allow_html=True)
prev_day_pos = pd.DataFrame({'SYMBOL': ['Future', 'Call', 'Put', 'Future', 'Call', 'Put', 'Future', 'Call', 'Put'],
                              'CLIENT': ['Client 1', 'Client 1', 'Client 1', 'Client 2', 'Client 2', 'Client 2', 'Client 3', 'Client 3', 'Client 3'],
                              'QUANTITY': [0., 0., 0., 0., 0., 0., 0., 0., 0.]},
                            index= np.arange(9))

with st.expander('Click to input SoD client portfolios'):
    st.session_state['prev_day_pos'] = st.data_editor(prev_day_pos, 
                                                      disabled=('SYMBOL', 'CLIENT'),
                                                     use_container_width=True, hide_index=True)
    st.text_area("",
                 """ Clients' net position at SoD. To be mantained by B/O system and disseminated to F/O at SoD.
                         - Quantity: Positive amount indicates long net position whereas negative indices short net position.
                    """, disabled=True, height=1)

##### ORDER FORM #####
with st.container():
  buff, col, buff2 = st.columns([1,2,1])
  col.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>ORDER/TRADE SUBMISSION</p>", unsafe_allow_html=True)
  with col.expander('Click to open form'):
    st.session_state['new_client']  = st.selectbox('Client ID', options=['Client 1', 'Client 2', 'Client 3'], index=0)
    st.session_state['new_instrument'] = st.selectbox('Symbol', options=st.session_state['qccp_margins'].index, index=0)
    st.session_state['new_quantity'] = st.number_input(label='Quantity', min_value=1, value=1)
    st.session_state['new_price'] = st.number_input(label='Price' ,min_value=0., step=0.001, value=st.session_state['theor_prices'].loc[st.session_state['new_instrument']]['THEORETICAL PRICE'], format='%.3f')
    st.session_state['new_side']  = st.selectbox('Side', options=['Buy', 'Sell'], index=0)
    st.session_state['new_type']  = st.selectbox('Type', options=['Order', 'Trade'], index=0)
    st.text_area("",
                 """ Use 'Order' to submit outstanding orders (either placed on T or carried forward orders from T-1) and 'Trade' for executed trades.""",
                 disabled=True)
    submit_button = st.button(label='Submit')

  if submit_button:
    st.session_state['ID'] += 1
    new_pos = pd.DataFrame({'CLIENT': st.session_state['new_client'], 
                            'SYMBOL': st.session_state['new_instrument'],
                            'QUANTITY': st.session_state['new_quantity'],
                            'PRICE': st.session_state['new_price'],
                            'SIDE': st.session_state['new_side']},
                          index = [st.session_state['ID']])

    if st.session_state['new_type'] == 'Order':
      new_pos = new_pos.assign(**{'INITIAL MARGIN': np.where((st.session_state['new_instrument']!='Future') & (st.session_state['new_side']=='Buy'), 0.,
                                                             st.session_state['new_quantity'] * st.session_state['fit_margins'].loc[st.session_state['new_instrument']]['IM'])})
      new_pos = new_pos.assign(**{'PENDING PREMIUM': np.where(st.session_state['new_instrument']=='Future', 0.,
                                                              np.where(st.session_state['new_side'] == 'Buy', -1, 1) * st.session_state['new_quantity'] * st.session_state['new_price'] * st.session_state['theor_prices'].loc[st.session_state['new_instrument']]['CONTRACT SIZE'])})
      new_pos = new_pos.assign(**{'CURRENT BUYING POWER':st.session_state['client_bp'].loc[st.session_state['new_client']]['BUYING POWER'],
                                  'TOTAL REQUIREMENT': np.absolute(np.minimum(np.add(np.multiply(-1, new_pos['INITIAL MARGIN']), new_pos['PENDING PREMIUM']), 0))})
      new_pos = new_pos.assign(**{'STATUS': np.where(new_pos['CURRENT BUYING POWER'] > new_pos['TOTAL REQUIREMENT'], 'ACCEPTED', 'REJECTED')})
        
      if 'orders' not in st.session_state.keys():
        st.session_state['orders'] = new_pos
      else:
        st.session_state['orders'] = pd.concat([st.session_state['orders'], new_pos], axis=0, ignore_index= True)
    elif st.session_state['new_type'] == 'Trade':
        new_pos = new_pos.assign(**{'PENDING PREMIUM': np.where(st.session_state['new_instrument']=='Future', 0.,
                                                                np.where(st.session_state['new_side'] == 'Buy', -1, 1) * st.session_state['new_quantity'] * st.session_state['new_price'] * st.session_state['theor_prices'].loc[st.session_state['new_instrument']]['CONTRACT SIZE'])})

        if 'trades' not in st.session_state.keys():                               
            st.session_state['trades'] = new_pos
        else:
            st.session_state['trades'] = pd.concat([st.session_state['trades'], new_pos], axis=0, ignore_index= True)
            


##### CVM/RVM CALCULATION SoD POSITION #####
st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos'].set_index('SYMBOL').join(st.session_state['eod_prices'], how='left')
st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos_calc'].join(st.session_state['theor_prices'], how='left')
st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos_calc'].reset_index()

if st.session_state['calc_type'] == 'EoD':
    st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos_calc'][['SYMBOL', 'CLIENT', 'QUANTITY', 'EOD PRICE T-1', 'EOD PRICE T', 'CONTRACT SIZE']]
    
elif st.session_state['calc_type'] == 'ItD':
    st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos_calc'][['SYMBOL', 'CLIENT', 'QUANTITY', 'EOD PRICE T-1', 'THEORETICAL PRICE', 'CONTRACT SIZE']]

st.session_state['prev_day_pos_calc'] = st.session_state['prev_day_pos_calc'][st.session_state['prev_day_pos_calc']['QUANTITY'] !=0]
if st.session_state['calc_type'] == 'EoD':
    st.session_state['prev_day_pos_calc'] =st.session_state['prev_day_pos_calc'].assign(**{'RVM': np.where(st.session_state['prev_day_pos_calc'].SYMBOL!='Future', 0.,
                                                                                                           np.multiply(np.multiply(st.session_state['prev_day_pos_calc'].QUANTITY,
                                                                                                                       st.session_state['prev_day_pos_calc']['CONTRACT SIZE']),
                                                                                                           np.subtract(st.session_state['prev_day_pos_calc']['EOD PRICE T'],st.session_state['prev_day_pos_calc']['EOD PRICE T-1']))),
                                                                                           'PENDING PREMIUM': 0.})
elif st.session_state['calc_type'] == 'ItD':
    st.session_state['prev_day_pos_calc'] =st.session_state['prev_day_pos_calc'].assign(**{'CVM': np.where(st.session_state['prev_day_pos_calc'].SYMBOL!='Future', 0.,
                                                                                                           np.multiply(np.multiply(st.session_state['prev_day_pos_calc'].QUANTITY,
                                                                                                                                   st.session_state['prev_day_pos_calc']['CONTRACT SIZE']),
                                                                                                                       np.subtract(st.session_state['prev_day_pos_calc']['THEORETICAL PRICE'],st.session_state['prev_day_pos_calc']['EOD PRICE T-1']))),
                                                                                           'PENDING PREMIUM': 0.})

if (st.session_state['calc_type'] == 'EoD') & ((st.session_state['prev_day_pos_calc'].shape[0]>0) or ('trades' in st.session_state.keys())):
    st.divider()
    st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>REALIZED VARIATION MARGIN - BREAK DOWN</p>", unsafe_allow_html=True)
elif (st.session_state['calc_type'] == 'ItD') & ((st.session_state['prev_day_pos_calc'].shape[0]>0) or ('trades' in st.session_state.keys())):
    st.divider()
    st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>CONTINGENT VARIATION MARGIN & PENDING PREMIUM - BREAK DOWN</p>", unsafe_allow_html=True)
with st.expander('Click to see break down'):
    if st.session_state['prev_day_pos_calc'].shape[0]:
        if st.session_state['calc_type'] == 'EoD':
            st.markdown("<p style='text-align: center;'font-size:18px;'>SoD OPEN POSITION - RVM CALCULATION </p>", unsafe_allow_html=True)
            st.dataframe(st.session_state['prev_day_pos_calc'].drop(columns=['PENDING PREMIUM']), use_container_width=True, hide_index=True)
            st.text_area("",
                         """ Realized Variation Margin (RVM) should be computed EoD by B/O system to MtM futures positons carried forward from previous days to EoD official settlement price.
                         RVM = Quantity * Contract Size * (EoD Price T - EoD Price T-1)""", disabled=True)
        elif st.session_state['calc_type'] == 'ItD':        
            st.markdown("<p style='text-align: center;'font-size:18px;'>SoD OPEN POSITION - CVM CALCULATION </p>", unsafe_allow_html=True) 
            st.dataframe(st.session_state['prev_day_pos_calc'].drop(columns=['PENDING PREMIUM']), use_container_width=True, hide_index=True)
            st.text_area("",""" Contingent Variation Margin (CVM) should be computed ItD by F/O system for futures positons carried forward from previous days as a component of Buying Power computation.
                         CVM = Quantity * Contract Size * (ItD Theoretical Price - EoD Price T-1)""", disabled=True)

    if 'trades' in st.session_state.keys():
        if ('EOD PRICE T' in st.session_state['trades'].columns):
            st.session_state['trades'] = st.session_state['trades'].drop(columns=['EOD PRICE T', 'CONTRACT SIZE'])
        elif ('THEORETICAL PRICE' in st.session_state['trades'].columns):
            st.session_state['trades'] = st.session_state['trades'].drop(columns=['THEORETICAL PRICE', 'CONTRACT SIZE'])
        if st.session_state['calc_type'] == 'EoD':
            st.session_state['trades'] = st.session_state['trades'].set_index('SYMBOL').join(st.session_state['eod_prices'][['EOD PRICE T']], how='left')
            st.session_state['trades'] = st.session_state['trades'].join(st.session_state['theor_prices'][['CONTRACT SIZE']], how='left')
            st.session_state['trades'] =  st.session_state['trades'].reset_index()
            
            st.session_state['trades'] = st.session_state['trades'].assign(**{'RVM': np.where(st.session_state['trades']['SYMBOL']!='Future', 0.,
                                                                                                np.multiply(np.multiply(np.multiply(np.where(st.session_state['trades']['SIDE'] == 'Buy', 1, -1), st.session_state['trades']['QUANTITY']),
                                                                                                                                    st.session_state['trades']['CONTRACT SIZE']),
                                                                                                                                    np.subtract(st.session_state['trades']['EOD PRICE T'], st.session_state['trades']['PRICE'])))
                                                                                                })
            st.session_state['trades'] = st.session_state['trades'][['CLIENT', 'SYMBOL', 'QUANTITY', 'PRICE', 'SIDE', 'EOD PRICE T', 'CONTRACT SIZE', 'RVM', 'PENDING PREMIUM']]
            st.session_state['day_trades'] = st.session_state['trades'].assign(**{'QUANTITY': np.where(st.session_state['trades']['SIDE']=='Buy',
                                                                                                   st.session_state['trades']['QUANTITY'],
                                                                                                   np.multiply( st.session_state['trades']['QUANTITY'], -1))})
            st.session_state['day_trades'] = st.session_state['day_trades'].pivot_table(index=['CLIENT', 'SYMBOL'],
                                                                                        values=['QUANTITY', 'PENDING PREMIUM', 'RVM'],
                                                                                        aggfunc='sum')
            st.markdown("<p style='text-align: center;'font-size:18px;'>EXECUTED TRADES - RVM CALCULATION</p>", unsafe_allow_html=True)
            st.dataframe(st.session_state['trades'], use_container_width=True, hide_index=True)
            st.text_area("",
                         """ Realized Variation Margin (RVM) should be computed EoD by B/O system to MtM each trade on futures to EoD official settlement price.
                         RVM = Quantity * Contract Size * (EoD Price T - Execution Price)
Pending Premium should be computed EoD by B/O system for trades in options, to compute the premium settlement as part of the clearing obligations:
                         Pending Premium = Quantity * Contract Size * Execution Premium""", disabled=True)
        elif st.session_state['calc_type'] == 'ItD':
            st.dataframe(st.session_state['trades'])
            st.dataframe(st.session_state['prev_day_pos_calc'])
            st.session_state['trades'] = st.session_state['trades'].set_index('SYMBOL').join(st.session_state['theor_prices'], how='left')
            st.session_state['trades'] =  st.session_state['trades'].reset_index()
            
            st.session_state['trades'] = st.session_state['trades'].assign(**{'CVM': np.where(st.session_state['trades']['SYMBOL']!='Future', 0.,
                                                                                                np.multiply(np.multiply(np.multiply(np.where(st.session_state['trades']['SIDE'] == 'Buy', 1, -1), st.session_state['trades']['QUANTITY']),
                                                                                                                                    st.session_state['trades']['CONTRACT SIZE']),
                                                                                                                                    np.subtract(st.session_state['trades']['THEORETICAL PRICE'], st.session_state['trades']['PRICE'])))
                                                                                                })
            st.session_state['trades'] = st.session_state['trades'][['CLIENT', 'SYMBOL', 'QUANTITY', 'PRICE', 'SIDE', 'THEORETICAL PRICE', 'CONTRACT SIZE', 'CVM', 'PENDING PREMIUM']]
            st.session_state['day_trades'] = st.session_state['trades'].assign(**{'QUANTITY': np.where(st.session_state['trades']['SIDE']=='Buy',
                                                                                                       st.session_state['trades']['QUANTITY'],
                                                                                                       np.multiply( st.session_state['trades']['QUANTITY'], -1))})
            st.session_state['day_trades'] = st.session_state['day_trades'].pivot_table(index=['CLIENT', 'SYMBOL'],
                                                                                        values=['QUANTITY', 'PENDING PREMIUM', 'CVM'],
                                                                                        aggfunc='sum')
        
            st.markdown("<p style='text-align: center;'font-size:18px;'>EXECUTED TRADES - CVM CALCULATION</p>", unsafe_allow_html=True)
            st.dataframe(st.session_state['trades'], use_container_width=True, hide_index=True)
            st.text_area("",
                         """ Contingent Variation Margin (CVM) should be computed ItD by F/O system for each trade on futures as a component of Buying Power computation.
                         CVM = Quantity * Contract Size * (ItD Theoretical Price - Execution Price)
 Pending Premium should be computed both ItD by F/O system for trades in options, as a component of Buying Power computation:
                         Pending Premium = Quantity * Contract Size * Execution Premium""", 
                         disabled=True)
        st.session_state['day_trades'] = st.session_state['day_trades'].reset_index()
       
if 'day_trades' in st.session_state.keys():
    if st.session_state['calc_type'] == 'EoD':
        prev_day_subset = st.session_state['prev_day_pos_calc'][['CLIENT', 'SYMBOL', 'RVM', 'PENDING PREMIUM', 'QUANTITY']]
        st.session_state['open_pos'] = pd.concat([prev_day_subset, st.session_state['day_trades']], ignore_index=True)
        st.session_state['open_pos'] = st.session_state['open_pos'].pivot_table(index=['CLIENT', 'SYMBOL'], 
                                                                                      values=['QUANTITY', 'PENDING PREMIUM', 'RVM'], 
                                                                                      aggfunc='sum')
    elif st.session_state['calc_type'] == 'ItD':
        prev_day_subset = st.session_state['prev_day_pos_calc'][['CLIENT', 'SYMBOL', 'CVM', 'PENDING PREMIUM', 'QUANTITY']]
        st.session_state['open_pos'] = pd.concat([prev_day_subset, st.session_state['day_trades']], ignore_index=True)
        st.session_state['open_pos'] = st.session_state['open_pos'].pivot_table(index=['CLIENT', 'SYMBOL'], 
                                                                                      values=['QUANTITY', 'PENDING PREMIUM', 'CVM'], 
                                                                                      aggfunc='sum')
    st.session_state['open_pos'] =st.session_state['open_pos'].reset_index()
else:
    if st.session_state['calc_type'] == 'EoD':
        st.session_state['open_pos'] = st.session_state['prev_day_pos_calc'][['CLIENT', 'SYMBOL', 'RVM', 'PENDING PREMIUM', 'QUANTITY']]
    elif st.session_state['calc_type'] == 'ItD':
        st.session_state['open_pos'] = st.session_state['prev_day_pos_calc'][['CLIENT', 'SYMBOL', 'CVM', 'PENDING PREMIUM', 'QUANTITY']]
if 'open_pos' in st.session_state.keys():
    st.session_state['open_pos'] = st.session_state['open_pos'].set_index('SYMBOL')
    st.session_state['open_pos'] = st.session_state['open_pos'].join(st.session_state['fit_margins'][['MM']], how='left')
    st.session_state['open_pos'] = st.session_state['open_pos'].reset_index()
    st.session_state['open_pos'] = st.session_state['open_pos'].assign(**{'MAINTENANCE MARGIN': np.abs(np.where((st.session_state['open_pos']['SYMBOL']!='Future') & (st.session_state['open_pos']['QUANTITY']>0), 0.,
                                                                                                                 np.multiply(st.session_state['open_pos']['QUANTITY'], st.session_state['open_pos']['MM'])))})
    if st.session_state['calc_type'] == 'EoD':
        st.session_state['open_pos'] = st.session_state['open_pos'].assign(**{'TOTAL REQUIREMENT': st.session_state['open_pos']['MAINTENANCE MARGIN']})
    elif st.session_state['calc_type'] == 'ItD':   
        st.session_state['open_pos'] = st.session_state['open_pos'].assign(**{'TOTAL REQUIREMENT':np.abs(np.subtract(np.add(np.minimum(st.session_state['open_pos'].CVM, 0), st.session_state['open_pos']['PENDING PREMIUM']),
                                                                                                                     st.session_state['open_pos']['MAINTENANCE MARGIN']))})
        
    st.session_state['open_pos'] = st.session_state['open_pos'].drop(columns=['MM'])
##### OUTSTANDING ORDERS #####
if 'orders' in st.session_state.keys():
    st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>OUTSTANDING ORDERS</p>", unsafe_allow_html=True)
    with st.expander('Click to display outstanding orders'):
        st.dataframe(st.session_state['orders'], use_container_width=True, hide_index=True)
        st.text_area("",
                     """Margin requirements for outstanding order should be computed ItD by F/O system and EoD by B/O system.
                        - Initial Margin: Applicable to futures and short option positions -> IM = Quantity * Instrument's IM.
                        - Pending Premium: Negative (margin requirement) for long options and positive (credit) for short options -> Pending Premium = Quantity * Contract Size * Premium (equal to order price or reference price for market orders).
                        - Current Buying Power: Client's buying power when order was submitted.
                        - Total Requirement: abs(min(Pending Premium - Initial Margin, 0))
                        - Status: Accepted if Current Buying Power > Total Requirement. Otherwise Rejected (Rejected orders won't have an impact on buying power calculation).
                    """, disabled=True, height=1)
##### CLIENT-BROKER & BROKER-CCP OPEN POSITION - BREAK DOWN #####
if st.session_state['open_pos'].shape[0]>0:
    st.divider()
    st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>CLIENT-BROKER & BROKER-CCP OPEN POSITION - BREAK DOWN</p>", unsafe_allow_html=True)
    with st.expander('Click to see break down'):
        with st.container():
            cli, ccp = st.columns([1,1])
            if st.session_state['open_pos'].shape[0]:
                if st.session_state['calc_type'] == 'EoD':
                    cli.markdown("<p style='text-align: center;'font-size:18px;'>BROKER - CLIENT OPEN POSITION</p>", unsafe_allow_html=True)
                    cli.dataframe(st.session_state['open_pos'][['CLIENT', 'SYMBOL', 'QUANTITY', 'RVM', 'PENDING PREMIUM', 'MAINTENANCE MARGIN', 'TOTAL REQUIREMENT']], use_container_width=True, hide_index=True)
                    cli.text_area("",
                                 """- Quantity: Net quantity at Client/Instrument level, aggregating previous day SoD open position and trades submitted within the day.
 - RVM: Realized Variation Margin aggregated at Client/Instrument level (Both computed for SoD open position and trades submitted within the day).
 - Pending Premium: Aggregated pending premiums at Client/Instrument level, computed for each executed trade on options.
 - Maintenance Margin: Quantity * Instrument's MM
 - Total Requirements: EoD total requirements will be equal to Maintenance Margin as RVM and Pending Premium will be settled versus client's collateral.""",
                                  disabled=True)
                    ccp.markdown("<p style='text-align: center;'font-size:18px;'>BROKER/CM - CCP OPEN POSITION</p>", unsafe_allow_html=True)
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos'].pivot_table(index=['SYMBOL'],
                                                                                                values= ['QUANTITY', 'RVM', 'PENDING PREMIUM'],
                                                                                                aggfunc ='sum')
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].reset_index()
                    st.session_state['open_pos_ccp'] =  st.session_state['open_pos_ccp'].set_index('SYMBOL').join(st.session_state['theor_prices'][['CONTRACT SIZE']], how='left')
                    st.session_state['open_pos_ccp'] =  st.session_state['open_pos_ccp'].join(st.session_state['eod_prices'][['EOD PRICE T']], how='left')
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].reset_index()
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].assign(**{'CLEARING ACCOUNT': 'OSA',
                                                                                                  'NLV': np.where( st.session_state['open_pos_ccp']['SYMBOL']!='Future',
                                                                                                                  np.multiply(st.session_state['open_pos_ccp']['QUANTITY'],
                                                                                                                              np.multiply(st.session_state['open_pos_ccp']['EOD PRICE T'],
                                                                                                                                          st.session_state['open_pos_ccp']['CONTRACT SIZE'])), 0.)
                                                                                                 })
                    ccp.dataframe(st.session_state['open_pos_ccp'][['CLEARING ACCOUNT', 'SYMBOL', 'QUANTITY', 'EOD PRICE T', 'CONTRACT SIZE', 'RVM', 'NLV', 'PENDING PREMIUM']],
                                  use_container_width=True, hide_index=True)
                    ccp.text_area("",
                                 """- Quantity: Net quantity at Clearging Account/Instrument level, aggregating client/house net quantity at clearing/margin account level.
 - RVM: Realized Variation Margin aggregated at Clearing Account/Instrument level.
 - NLV: Computed for open positions in options (both long (positive) and short (negative)). 
         NLV = Quantity * Contract Size * EoD Price T.
 - Pending Premium: Aggregated pending premiums at Clearing Account/Instrument level.""",
                                  disabled=True)
                elif st.session_state['calc_type'] == 'ItD':
                    cli.markdown("<p style='text-align: center;'font-size:18px;'>BROKER - CLIENT OPEN POSITION</p>", unsafe_allow_html=True)
                    cli.dataframe(st.session_state['open_pos'][['CLIENT', 'SYMBOL', 'QUANTITY', 'CVM', 'PENDING PREMIUM', 'MAINTENANCE MARGIN', 'TOTAL REQUIREMENT']], use_container_width=True, hide_index=True)
                    cli.text_area("",
                                 """- Quantity: Net quantity at Client/Instrument level, aggregating previous day SoD open position and trades submitted within the day.
 - CVM: Contingent Variation Margin aggregated at Client/Instrument level (Both computed for SoD open position and trades submitted within the day).
 - Pending Premium: Aggregated pending premiums at Client/Instrument level, computed for each executed trade on options.
 - Maintenance Margin: Quantity * Instrument's MM
 - Total Requirements: ItD total requirements will be equal to: MM = abs(min(min(CVM, 0) + Pending Premium - Maintenance Margin, 0))""",
                                  disabled=True)
                    ccp.markdown("<p style='text-align: center;'font-size:18px;'>BROKER/CM - CCP OPEN POSITION</p>", unsafe_allow_html=True)
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos'].pivot_table(index=['SYMBOL'],
                                                                                                values= ['QUANTITY', 'CVM', 'PENDING PREMIUM'],
                                                                                                aggfunc ='sum')
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].reset_index()
                    st.session_state['open_pos_ccp'] =  st.session_state['open_pos_ccp'].set_index('SYMBOL').join(st.session_state['theor_prices'], how='left')
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].reset_index()
                    st.session_state['open_pos_ccp'] = st.session_state['open_pos_ccp'].assign(**{'CLEARING ACCOUNT': 'OSA',
                                                                                                  'NLV': np.where( st.session_state['open_pos_ccp']['SYMBOL']!='Future',
                                                                                                                  np.multiply(st.session_state['open_pos_ccp']['QUANTITY'],
                                                                                                                              np.multiply(st.session_state['open_pos_ccp']['THEORETICAL PRICE'],
                                                                                                                                          st.session_state['open_pos_ccp']['CONTRACT SIZE'])), 0.)
                                                                                                 })
                    ccp.dataframe(st.session_state['open_pos_ccp'][['CLEARING ACCOUNT', 'SYMBOL', 'QUANTITY', 'THEORETICAL PRICE', 'CONTRACT SIZE', 'CVM', 'NLV', 'PENDING PREMIUM']],
                                  use_container_width=True, hide_index=True)
                    ccp.text_area("",
                                 """- Quantity: Net quantity at Clearging Account/Instrument level, aggregating client/house net quantity at clearing/margin account level.
 - CVM: Contingent Variation Margin aggregated at Clearing Account/Instrument level.
 - NLV: Computed for open positions in options (both long (positive) and short (negative)). 
         NLV = Quantity * Contract Size * Theoretical Price.
 - Pending Premium: Aggregated pending premiums at Clearing Account/Instrument level.""",
                                  disabled=True)
##### CLIENT-BROKER & BROKER-CCP OPEN POSITION - SETTLEMENT #####
if st.session_state['open_pos'].shape[0]>0:
    if st.session_state['calc_type'] == 'ItD':
        pass
    elif st.session_state['calc_type'] == 'EoD':
        st.divider()
        st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>CLIENT-BROKER & BROKER-CCP SETTLEMENTS</p>", unsafe_allow_html=True)
        with st.expander('Click to see EoD settlement'):
            with st.container():
                cli, ccp = st.columns([1,1])
                if st.session_state['open_pos'].shape[0]:
                    st.session_state['client_settlement'] = st.session_state['open_pos'].pivot_table(index=['CLIENT'],
                                                                                                     values=['RVM', 'PENDING PREMIUM'],
                                                                                                     aggfunc='sum')
                    st.session_state['client_settlement'] = st.session_state['client_settlement'].assign(**{'TOTAL SETTLEMENT': np.add(st.session_state['client_settlement'].RVM,
                                                                                                                                       st.session_state['client_settlement']['PENDING PREMIUM'])})
                        
                    cli.markdown("<p style='text-align: center;'font-size:18px;'>BROKER - CLIENT SETTLEMENT</p>", unsafe_allow_html=True)
                    cli.dataframe(st.session_state['client_settlement'],use_container_width=True)
                    cli.text_area("",
                                  """- RVM: Realized Variation Margin aggregated at Client level.
- Pending Premium: Aggregated pending premiums at Client level.
- Total Settlement: RVM + Pending Premium""",
                                      disabled=True)
                    st.session_state['ccp_settlement'] = st.session_state['open_pos_ccp'].pivot_table(index=['CLEARING ACCOUNT'],
                                                                                                      values=['RVM', 'PENDING PREMIUM'],
                                                                                                      aggfunc='sum')
                    st.session_state['ccp_settlement'] = st.session_state['ccp_settlement'].assign(**{'TOTAL SETTLEMENT': np.add(st.session_state['ccp_settlement'].RVM,
                                                                                                                                 st.session_state['ccp_settlement']['PENDING PREMIUM'])})
                        
                    ccp.markdown("<p style='text-align: center;'font-size:18px;'>BROKER/CM - CCP SETTLEMENT</p>", unsafe_allow_html=True)
                    ccp.dataframe(st.session_state['ccp_settlement'],use_container_width=True)
                    ccp.text_area("",
                                  """- RVM: Realized Variation Margin aggregated at Clearing/Margin Account level.
- Pending Premium: Aggregated pending premiums at Clearing/Margin Account level.
- Total Settlement: RVM + Pending Premium""",
                                      disabled=True)
##### CLIENT-BROKER & BROKER-CCP OPEN POSITION - COLLATERAL #####
if st.session_state['open_pos'].shape[0]>0:
    st.divider()
    st.markdown("<p style='text-align: center; font-size: 22px; font-weight: bold;'>CLIENT-BROKER & BROKER-CCP COLLATERAL BALANCE</p>", unsafe_allow_html=True)
    with st.expander('Click to see results'):
        with st.container():
            cli, ccp = st.columns([1,1])
            # Client - Broker
            st.session_state['client_bp'] = st.session_state['sod_collateral']
            if st.session_state['open_pos'].shape[0]:
                open_pos_req = st.session_state['open_pos'].pivot_table(index=['CLIENT'], values=['TOTAL REQUIREMENT'],
                                                                        aggfunc='sum')
                st.session_state['client_bp'] = st.session_state['client_bp'].join(open_pos_req, how='left')
                st.session_state['client_bp'] = st.session_state['client_bp'].rename(columns={'TOTAL REQUIREMENT': 'OPEN POSITION REQ'})
            else:
                st.session_state['client_bp'] = st.session_state['client_bp'].assign(**{'OPEN POSITION REQ': 0.})
            if 'orders' in st.session_state.keys():
                accepted_orders = st.session_state['orders'][st.session_state['orders'].STATUS=='ACCEPTED']
                if accepted_orders.shape[0]:
                    accepted_orders = accepted_orders.pivot_table(index=['CLIENT'], values=['TOTAL REQUIREMENT'],
                                                                  aggfunc='sum')
                    st.session_state['client_bp'] = st.session_state['client_bp'].join(accepted_orders, how='left')
                    st.session_state['client_bp'] = st.session_state['client_bp'].rename(columns={'TOTAL REQUIREMENT': 'OUTSTANDING ORDERS REQ'})
                else:
                    st.session_state['client_bp'] = st.session_state['client_bp'].assign(**{'OUTSTANDING ORDERS REQ': 0.})
            else:
                st.session_state['client_bp'] = st.session_state['client_bp'].assign(**{'OUTSTANDING ORDERS REQ': 0.})
                
            st.session_state['client_bp'] = st.session_state['client_bp'].fillna(0)
         
            if st.session_state['calc_type'] == 'ItD':
                st.session_state['client_bp'] = st.session_state['client_bp'].assign(**{'BUYING POWER': np.maximum(np.subtract(st.session_state['client_bp'].COLLATERAL,
                                                                                                                               np.add(st.session_state['client_bp']['OPEN POSITION REQ'],
                                                                                                                                      st.session_state['client_bp']['OUTSTANDING ORDERS REQ'])), 0)})
                cli.markdown("<p style='text-align: center;'font-size:18px;'>BROKER - CLIENT COLLATERAL BALANCE</p>", unsafe_allow_html=True)
                cli.dataframe(st.session_state['client_bp'],use_container_width=True)
                cli.text_area("",
                              """ItD client's buying power will be used for pre-trade controls (F/O system) and to monitor client's collateral consumption (B/O system).

- Collateral: Client's collateral position (cash value of the collateral posted by the client). Updates on this value should be sent from B/O system to F/O  system.
- Open Position Req: Total requirements computed for outstanding open positions at client level.
- Outstanding Orders Req: Total requirements computed for outstanding orders at client level.
- Buying Power: Collateral - Open Position Req - Outstandin Orders Req.""",
                                      disabled=True)
            elif st.session_state['calc_type'] == 'EoD':
                st.session_state['client_bp'] = st.session_state['client_bp'].join(st.session_state['client_settlement'][['TOTAL SETTLEMENT']], how='left')
                st.session_state['client_bp'] =  st.session_state['client_bp'].fillna(0)
                st.session_state['client_bp'] = st.session_state['client_bp'].assign(**{'AVAILABLE COLLATERAL': np.maximum(np.add(np.subtract(st.session_state['client_bp'].COLLATERAL,
                                                                                                                                                          np.add(st.session_state['client_bp']['OPEN POSITION REQ'],
                                                                                                                                                                 st.session_state['client_bp']['OUTSTANDING ORDERS REQ'])),
                                                                                                                                              st.session_state['client_bp']['TOTAL SETTLEMENT']),
                                                                                                                                       0),
                                                                                       'NEXT DAY COLLATERAL POS': np.add(st.session_state['client_bp'].COLLATERAL, st.session_state['client_bp']['TOTAL SETTLEMENT'])})
                cli.markdown("<p style='text-align: center;'font-size:18px;'>BROKER - CLIENT COLLATERAL BALANCE/NEXT DAY BUYING POWER</p>", unsafe_allow_html=True)
                cli.dataframe(st.session_state['client_bp'],use_container_width=True)
                cli.text_area("",
                              """- Collateral: Client's collateral position (cash value of the collateral posted by the client) before EoD settlement.
- Open Position Req: Total requirements computed for outstanding open positions at client level.
- Outstanding Orders Req: Total requirements computed for outstanding orders at client level.
- Total Settlement: Clearing obligations settlement amount at client level.
- Available Collateral: Collateral - Open Position Req - Outstanding Orders Req + Total Settlement.
- Next Day Collateral Pos: Collateral + Total Settlement.""",
                                      disabled=True)
            # Broker - CCP:
            if 'open_pos_ccp' in st.session_state.keys():
                st.session_state['ccp_col_balance'] = st.session_state['sod_collateral_ccp']
                st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].assign(**{'IM': st.session_state['open_pos']['MAINTENANCE MARGIN'].sum(axis=0) * 0.2})
                if st.session_state['calc_type'] == 'ItD':
                    aggregated_req = st.session_state['open_pos_ccp'].pivot_table(index=['CLEARING ACCOUNT'], values=['CVM', 'NLV'], aggfunc='sum')
                    st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].join(aggregated_req, how='left')
                    st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].assign(**{'TOTAL LIABILITIES': np.subtract(np.add( st.session_state['ccp_col_balance']['CVM'],
                                                                                                                                                st.session_state['ccp_col_balance']['NLV']),
                                                                                                                                         st.session_state['ccp_col_balance']['IM'])})
                elif st.session_state['calc_type'] == 'EoD':
                    aggregated_req = st.session_state['open_pos_ccp'].pivot_table(index=['CLEARING ACCOUNT'], values=['NLV'], aggfunc='sum')
                    st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].join(aggregated_req, how='left')
                    st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].assign(**{'TOTAL LIABILITIES': np.subtract( st.session_state['ccp_col_balance']['NLV'],
                                                                                                                                         st.session_state['ccp_col_balance']['IM'])})
                # Required collateral
                st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].assign(**{'REQUIRED COLLATERAL': np.abs(np.minimum(np.add(st.session_state['ccp_col_balance']['TOTAL LIABILITIES'],
                                                                                                                                                    st.session_state['ccp_col_balance']['COLLATERAL']), 0))})
                st.session_state['ccp_col_balance'] = st.session_state['ccp_col_balance'].assign(**{'AVAILABLE COLLATERAL': np.maximum(np.add(st.session_state['ccp_col_balance']['TOTAL LIABILITIES'],
                                                                                                                                              st.session_state['ccp_col_balance']['COLLATERAL']), 0)})    
                ccp.markdown("<p style='text-align: center;'font-size:18px;'>BROKER/CM - CCP COLLATERAL BALANCE</p>", unsafe_allow_html=True)
                ccp.dataframe(st.session_state['ccp_col_balance'],use_container_width=True)
                ccp.text_area("",
                              """- Collateral: CM's collateral position in the corresponding collateral account (cash value of the collateral posted by the CM).
- IM: IM figures computed by CCP at margin account level and aggregated at collateral account level (Filtered HVaR model applied. It won't be replicable by B/O system).
- CVM: CVM aggregated at collateral account level (applicable just ItD).
- NLV: NLV aggregated at collateral account level.
- Total Liabilities: EoD -> Total Liabilities = IM + NLV / ItD -> Total Liabilities = IM + CVM + NLV.
- Required Collateral: abs(min(Collateral + Total Liabilities, 0)).
- Available Collateral: max(Collateral + Total Liabilities, 0).""", disabled=True)
