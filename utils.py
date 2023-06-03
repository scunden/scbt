import pandas as pd
import streamlit as st
import docs
import warnings
import plotly.express as px
from account import Account, Collection


warnings.simplefilter(action='ignore', category=UserWarning)

def to_collection(file, sheet_name):
    df = pd.read_excel(file,  sheet_name=sheet_name)     
    collection={}
    accounts = dict(df.values)
    for name, value in accounts.items():
        collection.update({name:Account(name, value)})   
    # Collection(**collection).express_collection()
    return Collection(type=sheet_name ,**collection)
    

def import_data():
    uploaded_file  = st.file_uploader(label="Upload your accounts setup document",type={"xlsx"})
    if uploaded_file  is not None:
        with st.spinner('Generating accounts...'):
            try:
                comp = pd.read_excel(uploaded_file,  sheet_name=docs.DU_COMPENSATION)

                st.session_state['frequency'] = docs.FREQUENCIES[comp[docs.DU_FREQ].iloc[0]]
                st.session_state['comp'] = comp[docs.DU_AMOUNT].iloc[0]
                st.session_state['checkings'] = to_collection(uploaded_file, docs.DU_CHECKINGS)
                st.session_state['pretax'] = to_collection(uploaded_file, docs.DU_PRETAX)
                st.session_state['savings'] = to_collection(uploaded_file, docs.DU_SAVINGS)
                st.session_state['investments'] = to_collection(uploaded_file, docs.DU_INVESTMENTS)
                
                st.session_state['collections'] = [st.session_state['checkings'], st.session_state['pretax'], 
                                                st.session_state['savings'], st.session_state['investments']]
                
                summarize_accounts()
            except:
                st.error('Error: Please ensure the uploaded file follows the template guidelines', icon="🚨")
 
def value_chart(collections, count=True):
    counts = [x.count for x in collections]
    values = [x.value for x in collections]
    types = [x.type for x in collections]
    
    fig = px.bar(x=types, y=counts if count else values, color=types,  text_auto=True if count else "$,.0f")
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_layout(showlegend=False)
    return fig
    

def summarize_accounts():
    st.markdown("---")
    st.header("📃 Accounts Summary")
    st.markdown("---")
    # show monthly pay
    c1, c2 = st.columns(2)
    comp =  st.session_state['frequency']*st.session_state['comp']
    c1.metric("Monthly Compensation (Post Tax, and Tax Deductions)", "${:,}".format(comp))
    c2.metric("Total Accounts Worth", "${:,}".format(sum([x.value for x in st.session_state['collections']])))

    fig1 = value_chart(st.session_state['collections'], count=True)
    fig2 = value_chart(st.session_state['collections'], count=False)
    
    tab1, tab2 = st.tabs(["Number of Accounts","Accounts Value"])
    with tab1:
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
