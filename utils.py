import pandas as pd
import streamlit as st
import docs
import warnings
import plotly.express as px
import plotly.graph_objects as go
from account import Account, Collection


warnings.simplefilter(action='ignore', category=UserWarning)

def to_collection(df, account_type):
    df = df.loc[df[docs.DU_ACCOUNT_TYPE]==account_type][[docs.DU_ACCOUNT_NAME, docs.DU_ACCOUNT_VALUE]]    
    collection={}
    accounts = dict(df.values)
    for name, value in accounts.items():
        collection.update({name:Account(name, value)})   
    # Collection(**collection).express_collection()
    return Collection(type=account_type ,**collection)
    

def upload_accounts(file):
    comp = pd.read_excel(file,  sheet_name=docs.DU_COMPENSATION)
    accounts = pd.read_excel(file,  sheet_name=docs.DU_ACCOUNTS)
    
    st.session_state['frequency'] = docs.FREQUENCIES[comp[docs.DU_FREQ].iloc[0]]
    st.session_state['comp'] = comp[docs.DU_AMOUNT].iloc[0]
    st.session_state['checkings'] = to_collection(accounts, docs.DU_CHECKINGS)
    st.session_state['pretax'] = to_collection(accounts, docs.DU_PRETAX)
    st.session_state['savings'] = to_collection(accounts, docs.DU_SAVINGS)
    st.session_state['investments'] = to_collection(accounts, docs.DU_INVESTMENTS)
    
    st.session_state['collections'] = [st.session_state['checkings'], st.session_state['pretax'], 
                                                st.session_state['savings'], st.session_state['investments']]
    
def upload_expenses(file):
    exp = pd.read_excel(file,  sheet_name=docs.DU_EXPENSES)
    st.session_state['expenses'] = exp.copy()

def upload_si(file):
    si = pd.read_excel(file,  sheet_name=docs.DU_SI)
    st.session_state['si'] = si.copy()
                
def upload_data():
    
    uploaded_file  = st.file_uploader(label="Upload your accounts setup document",type={"xlsx"})
    if uploaded_file  is not None:
        upload_accounts(uploaded_file)
        upload_expenses(uploaded_file)
        upload_si(uploaded_file)
        summarize_accounts()
        summarize_expenses()
        # with st.spinner('Generating accounts...'):
        #     try:
        #         upload_accounts(uploaded_file)
        #         upload_expenses(uploaded_file)
        #         upload_si(uploaded_file)
        #         summarize_accounts()
        #         summarize_expenses()
        #     except:
        #         st.error('Error: Please ensure the uploaded file follows the template guidelines', icon="🚨")
 
def value_chart(collections, count=True):
    counts = [x.count for x in collections]
    values = [x.value for x in collections]
    types = [x.type for x in collections]
    
    fig = px.bar(x=types, y=counts if count else values, color=types,  text_auto=True if count else "$,.0f")
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(title=None)
    fig.update_layout(showlegend=False)
    return fig
    

def summarize_accounts():
    st.markdown("---")
    st.header("📃 Accounts Summary")
    st.markdown("---")
    # show monthly pay
    c1, c2 = st.columns(2)
    st.session_state['monhtly_comp'] = st.session_state['frequency']*st.session_state['comp']
    c1.metric("Monthly Compensation (Post Tax, and Tax Deductions)", "${:,}".format(st.session_state['monhtly_comp']))
    c2.metric("Total Accounts Worth", "${:,}".format(sum([x.value for x in st.session_state['collections']])))

    fig1 = value_chart(st.session_state['collections'], count=True)
    fig2 = value_chart(st.session_state['collections'], count=False)
    
    tab1, tab2 = st.tabs(["Number of Accounts","Accounts Value"])
    with tab1:
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

def expenses_chart(perc=False):

    exp = st.session_state['expenses'].copy().sort_values(docs.DU_EXPENSE_AMOUNT, ascending=False) 
    
    
    if perc:
        exp["Waterfall"] = "relative"
        exp.iloc[0]["Waterfall"]="absolute"
        exp['Perc'] = exp[docs.DU_EXPENSE_AMOUNT]/st.session_state['monhtly_comp']
        exp.loc[len(exp)]=['Total',exp[docs.DU_EXPENSE_AMOUNT].sum(),'total',exp['Perc'] .sum()]
    
        fig = go.Figure()
        fig.add_trace(go.Waterfall(
            x=exp[docs.DU_EXPENSE_TYPE],
            measure = exp["Waterfall"],
            y = exp['Perc'],
            text=round(exp['Perc']*100,0).astype(str)+"%",
            # text_auto="$,.0f",
            ))
        
        fig.update_layout( waterfallgroupgap = 0.1)
    else:
        fig = px.bar(exp, x=docs.DU_EXPENSE_TYPE, y=docs.DU_EXPENSE_AMOUNT, text_auto="$,.0f")
        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_xaxes(title=None)
        fig.update_layout(showlegend=False)
    
    return fig

def summarize_expenses():
    st.markdown("---")
    st.header("📁 Expenses Summary")
    st.markdown("---")
    # show monthly pay
    c1, c2 = st.columns(2)
    total_expenses = st.session_state['expenses'][docs.DU_EXPENSE_AMOUNT].sum()
    c1.metric("Total Monthly Expenses", "${:,}".format(total_expenses))
    c2.metric("Expenses as % of Income", "{:.1%}".format(total_expenses/st.session_state['monhtly_comp']))
    
    fig1 = expenses_chart()
    fig2 = expenses_chart(perc=True)
    
    tab1, tab2 = st.tabs(["Expenses Amount","Expenses as % of Income"])
    with tab1:
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)