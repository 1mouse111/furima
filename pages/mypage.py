import streamlit as st
import sqlite3
from utils import *

# Global style
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)
side_nav()

current_user_id = st.session_state.current_user
conn = sqlite3.connect('userinfo.db')
c = conn.cursor()
c.execute("SELECT name,mail FROM users where id=?",(current_user_id,))
user=c.fetchone()
conn.close()
st.markdown("<h2 style='margin-top: 10px; text-align: center;'>マイページ</h2>", unsafe_allow_html=True)
st.text(f"ユーザ名: {user[0]}")
st.text(f"ユーザメイル: {user[1]}")
st.page_link("pages/favourite.py", label="📦 好みの商品")
st.page_link("pages/forgot.py", label="👤 パスワード変更")
# profile
# forgot pass
# favourite


# Close div
st.markdown('</div>', unsafe_allow_html=True)
