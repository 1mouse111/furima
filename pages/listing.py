import streamlit as st
import sqlite3

from utils import *


# ハンバーガーメニューの削除
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)

# トップバーの表示
topbar()

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()

# テーブルがなければ作成
c.execute('''CREATE TABLE IF NOT EXISTS items
             (name TEXT, description TEXT, price INTEGER)''')
conn.commit()


# 入力フォームの作成
item_name = st.text_input("アイテム名")
item_description = st.text_area("アイテムの説明")
item_price = st.number_input("価格", min_value=0)

# 投稿ボタンが押されたときの動作
if st.button("アイテムを投稿"):
    # アイテム情報をデータベースに保存
    c.execute("INSERT INTO items (name, description, price) VALUES (?, ?, ?)",
              (item_name, item_description, item_price))
    conn.commit()

    st.switch_page("pages/home.py")

bottom_nav()
