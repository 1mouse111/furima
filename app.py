import streamlit as st
import sqlite3
from utils import *
import hashlib
no_top()
side_button()
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
# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('userinfo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              pass TEXT,
              mail TEXT UNIQUE)''')
conn.commit()

c.execute("SELECT id,mail, pass FROM users") # SELECT idも追加
users_data = c.fetchall()
users_dict={row[1]:{'password_hash': row[2], 'id': row[0]} for row in users_data}
# 初期化

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if 'registration_message' in st.session_state:
    st.session_state.registration_message = {"type": None, "content": None}


# ログインフォームの表示
st.title("ログインページ")
user_mail_input = st.text_input("メールアドレス")
password_input = st.text_input("パスワード", type="password")
col1, col2= st.columns(2)
with col1:
    if st.button("ログイン"):
        if user_mail_input in users_dict:
            input_password_hash = hashlib.sha256(password_input.encode()).hexdigest()
            if users_dict[user_mail_input]['password_hash']==input_password_hash:
                st.session_state.logged_in = True
                st.session_state.current_user=users_dict[user_mail_input]['id']
                st.success("ログイン成功！")
                conn.close()
                st.rerun()
            else:
                st.error("メールアドレスまたはパスワードが間違っています。")
        else:
            st.error("メールアドレスまたはパスワードが間違っています。")
with col2:
    if st.button("登録"):
        conn.close()
        st.switch_page("pages/register.py")

st.page_link("pages/forgot.py", label="パスワードを忘れましたか?")

# ログイン成功したら自動で home.py に遷移
if st.session_state.logged_in:
    conn.close()
    st.switch_page("pages/home.py")
if conn:
    conn.close()
