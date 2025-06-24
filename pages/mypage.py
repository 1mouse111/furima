import streamlit as st
import time
from utils import *

# Global style
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)

topbar()

# WRAP CONTENT in margin div
st.markdown('<div class="main-content">', unsafe_allow_html=True)

for _ in range(9):
    st.header("asdasd")

st.number_input('wew')

# Close div
st.markdown('</div>', unsafe_allow_html=True)

bottom_nav()