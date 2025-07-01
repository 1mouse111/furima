import streamlit as st

from utils import *


# ハンバーガーメニューの削除
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)


# トップバーの表示
side_nav()