import streamlit as st
import sqlite3
import rmtop

rmtop.notop()

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('userinfo.db')
c = conn.cursor()
c.execute("SELECT id,name, pass FROM users") # SELECT idも追加
users_data = c.fetchall()
users_dict={row[1]:{'password': row[2], 'id': row[0]} for row in users_data}
# 初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ログインフォームの表示
st.text("testoo")
st.title("ログインページ")
user_id_input = st.text_input("ユーザーID")
password_input = st.text_input("パスワード", type="password")

if st.button("ログイン"):
    if user_id_input in users_dict:
        if users_dict[user_id_input]['password']==password_input:
            st.session_state.logged_in = True
            st.session_state.current_user=users_dict[user_id_input]['id']
            st.success("ログイン成功！")
            st.rerun()
    else:
        st.error("ユーザーIDまたはパスワードが間違っています。")
        
st.page_link("pages/forgot.py", label="パスワードを忘れましたか?")

# ログイン成功したら自動で home.py に遷移
if st.session_state.logged_in:
    st.switch_page("pages/home.py")
