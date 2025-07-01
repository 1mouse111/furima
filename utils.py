import streamlit as st

def side_nav():
    st.markdown("""
        <style>
        [data-testid="stHeader"] {
            display: none;
        }
        div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
    st.sidebar.page_link("pages/home.py", label="🏠 ホーム", icon=None)
    st.sidebar.page_link("pages/listing.py", label="📦 出品", icon=None)
    st.sidebar.page_link("pages/mylisting.py", label="📦 私出品", icon=None)
    st.sidebar.page_link("pages/mypage.py", label="👤 マイページ", icon=None)
def no_top():
    st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)
def side_button():
    st.markdown("""
            <style>
                div[data-testid="stColumn"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="stColumn"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)