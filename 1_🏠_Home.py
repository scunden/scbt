import streamlit as st
import docs
from account import Account, Collection
import utils

st.set_page_config(
        page_title="SCBT",
        page_icon="💸",
    )

def set_compensation():
    st.markdown("""---""") 
    st.header("💵 Compensation Structure")
    c1, c2 = st.columns(2)
    freq = c1.selectbox(label="Select Compensation Frequency", options=list(docs.FREQUENCIES.keys()), help=docs.FREQ_HELP)
    comp = c2.number_input(label="Enter Post-Tax {} Compensation".format(freq), help=docs.COMP_HELP)
    return freq, comp

def account_structure():
    st.markdown("""---""") 
    st.header("📁 Number of Accounts")
    st.write("Enter the number of accounts you have per account type below")
    c1, c2, c3 = st.columns(3)
    pt = c1.number_input(label="Pre-Tax Accounts", max_value=5, step=1, value=3, help=docs.PRE_TAX_HELP)
    savings = c2.number_input(label="Savings Accounts", max_value=5, step=1, value=1, help=docs.CS_HELP)
    inv = c3.number_input(label="Investments Accounts", max_value=10, step=1, value=3, help=docs.INV_HELP)
    # if st.button("Save", use_container_width=True):
    checkings, pretax, savings, investments = generate_all_collections(pt, savings, inv)
        
    return checkings, pretax, savings, investments
  

def create_accounts(noa, account_type):
    c1, c2 = st.columns(2)
    accounts={}
    for n in range(1, noa+1):
        key=account_type+str(n)
        name = c1.text_input(label="Enter {} Account {} Name".format(account_type, n))
        value = c2.number_input(label="Account {} Current Value".format(n), min_value=0, step=1000, value=1000, key=key)
        accounts.update({key:(name, value)})
        
    return accounts

def create_collection(noa, account_type="Pre-Tax", icon="1️⃣"):
    st.subheader("{} {} Accounts".format(icon, account_type))
    c1, c2 = st.columns(2)
    accounts = create_accounts(noa, account_type)
    collection={}
    for key in accounts.keys():
        name, value = accounts[key]
        collection.update({name:Account(name, value)})
        
    return Collection(**collection)
        
def generate_all_collections(pt, sav, inv):
    st.markdown("""---""")
    st.header("⚙️ Initialize Accounts")
    st.write("Enter the current value of each account")
    c1, c2, c3 = st.columns(3)
    
    checkings = create_collection(1, account_type="Checkings")
    pretax = create_collection(pt, account_type="Pre-Tax", icon="2️⃣")
    savings = create_collection(sav, account_type="Savings", icon="3️⃣")
    investments = create_collection(inv, account_type="Investments", icon="4️⃣")
    
    if ([pt, sav, inv] != [pretax.count, savings.count, investments.count]) or not all([pretax.valid, savings.valid, investments.valid]):
        st.error('Error: Please ensure accounts have unique names within account type', icon="🚨")
    else:
        st.markdown('---')
        if st.button("Save Accounts", use_container_width=True):
            st.session_state['checkings'] = checkings
            st.session_state['pretax'] = pretax
            st.session_state['savings'] = savings
            st.session_state['investments'] = investments
            st.success('Accounts saved successfully!', icon="✅")
            
        
    return checkings, pretax, savings, investments

def import_method():
    st.header("🎲 Data Upload")
    option = st.selectbox(label="Select your prefred upload method",options=[docs.DU_MANUAL, docs.DU_EXCEL])
    return option

def main():
    st.title('💸 SC Budget Tool')
    option = import_method()
    
    if option == docs.DU_MANUAL:
        freq, comp = set_compensation()
        checkings, pretax, savings, investments = account_structure()
    else:
        utils.import_data()

if __name__=="__main__":
    main()