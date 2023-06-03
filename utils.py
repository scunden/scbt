import pandas as pd
import streamlit as st
import docs
import warnings
from account import Account, Collection


warnings.simplefilter(action='ignore', category=UserWarning)

def to_collection(file, sheet_name):
    df = pd.read_excel(file,  sheet_name=sheet_name)        
    return Collection(**dict(df.values))
    

def import_data():
    uploaded_file  = st.file_uploader(label="Upload your accounts setup document",type={"xlsx"})
    if uploaded_file  is not None:
        comp = pd.read_excel(uploaded_file,  sheet_name=docs.DU_COMPENSATION)

        st.session_state['frequency'] = docs.FREQUENCIES[comp[docs.DU_FREQ].iloc[0]]
        st.session_state['comp'] = comp[docs.DU_AMOUNT].iloc[0]
        st.session_state['checkings'] = to_collection(uploaded_file, docs.DU_CHECKINGS)
        st.session_state['pretax'] = to_collection(uploaded_file, docs.DU_PRETAX)
        st.session_state['savings'] = to_collection(uploaded_file, docs.DU_SAVINGS)
        st.session_state['investments'] = to_collection(uploaded_file, docs.DU_INVESTMENTS)
        