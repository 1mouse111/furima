import streamlit as st
import sqlite3
from utils import *
import hashlib
no_top()
side_button()
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

if 'registration_message' not in st.session_state:
    st.session_state.registration_message = {"type": None, "content": None}

# 入力フォームの作成
user_name = st.text_input("ユーザー名", key="user_name_input")
user_mail = st.text_input("メールアドレス (@yuge.kosen-ac.jp ドメインのみ)", key="user_mail_input")
user_pass = st.text_input("パスワード", type="password", key="user_pass_input")
confirm_pass = st.text_input("パスワードの確認", type="password", key="confirm_pass_input")


# ボタンを横並びにするためにカラムを使用
col1, col2 = st.columns(2)

with col1:
    # 登録ボタン
    if st.button("アカウントを登録"):
        # メッセージをリセット
        st.session_state.registration_message = {"type": None, "content": None}

        # バリデーションチェック
        if not user_mail.endswith("@yuge.kosen-ac.jp"):
            st.session_state.registration_message = {"type": "error", "content": "エラー: メールアドレスは '@yuge.kosen-ac.jp' ドメインである必要があります。"}
        elif user_pass != confirm_pass:
            st.session_state.registration_message = {"type": "error", "content": "エラー: パスワードと確認用パスワードが一致しません。"}
        elif not user_name:
            st.session_state.registration_message = {"type": "error", "content": "エラー: ユーザー名は必須です。"}
        elif not user_pass:
            st.session_state.registration_message = {"type": "error", "content": "エラー: パスワードは必須です。"}
        else:
            # メールアドレスの重複チェック
            c.execute("SELECT * FROM users WHERE mail = ?", (user_mail,))
            existing_user = c.fetchone()
            if existing_user:
                st.session_state.registration_message = {"type": "error", "content": "エラー: このメールアドレスは既に登録されています。"}
            else:
                # パスワードをハッシュ化
                hashed_pass = hashlib.sha256(user_pass.encode()).hexdigest()

                try:
                    # ユーザー情報をデータベースに保存
                    c.execute("INSERT INTO users (name, pass, mail) VALUES (?, ?, ?)",
                              (user_name, hashed_pass, user_mail))
                    conn.commit()
                    conn.close()
                    st.session_state.registration_message = {"type": None, "content": None}
                    st.session_state.registered_email_for_confirmation = user_mail
                    st.switch_page("pages/registration_success.py")

                except sqlite3.Error as e:
                    st.session_state.registration_message = {"type": "error", "content": f"データベースエラーが発生しました: {e}"}

with col2:
    # 戻るボタン
    if st.button("戻る"):
        conn.close() # データベース接続を閉じる
        st.switch_page("app.py") # ログインページへ遷移 (main.pyがログインページの場合)

# メッセージをボタンの下に表示
if st.session_state.registration_message["content"]:
    st.error(st.session_state.registration_message["content"])

# データベース接続を閉じる (Streamlitアプリのライフサイクルでは通常不要だが、明示的に閉じる場合)
if conn:
    conn.close()