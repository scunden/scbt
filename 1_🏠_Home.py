import streamlit as st
import docs
from account import Account, Collection
import utils

st.set_page_config(
        page_title="SCBT",
        page_icon="💸",
    )

def main():
    st.title('💸 SC Budget Tool')
    st.markdown("""---""")
    st.header("🎲 Data Upload")    
    utils.upload_data()

if __name__=="__main__":
    main()