import streamlit as st
import sqlite3

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('userinfo.db')
c = conn.cursor()

# テーブルがなければ作成
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              pass TEXT,
              mail TEXT)''')
conn.commit()


# 入力フォームの作成
user_name = st.text_input("user名")
user_pass = st.text_input("userpass")
user_mail = st.text_input("usermail")

# 投稿ボタンが押されたときの動作
if st.button("createuser"):
    # アイテム情報をデータベースに保存
    c.execute("INSERT INTO users (name, pass, mail) VALUES (?, ?, ?)",
              (user_name, user_pass, user_mail))
    conn.commit()
    st.success("ユーザーが作成されました！") # Success message

st.header("登録済みのユーザー")
c.execute("SELECT id, name, pass, mail FROM users") # SELECT idも追加
users = c.fetchall()

if not users:
    st.info("まだユーザーが登録されていません。")
else:
    for user in users:
        # idも表示に含める
        st.write(f"ID: {user[0]}")
        st.write(f"username: {user[1]}")  # アイテム名
        st.write(f"pass: {user[2]}")      # 説明 (パスワードなので表示には注意)
        st.write(f"mail: {user[3]}")  # 価格
        st.write("---")