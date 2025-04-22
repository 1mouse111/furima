import streamlit as st
import sqlite3

from utils import *

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()

# テーブルがなければ作成
c.execute('''CREATE TABLE IF NOT EXISTS items
             (name TEXT, description TEXT, price INTEGER)''')
conn.commit()

# ハンバーガーメニューの削除
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    </style>
""", unsafe_allow_html=True)

# トップバーの表示
topbar()


st.markdown("<p style='margin-top: -50px;'>出品一覧</p>", unsafe_allow_html=True)

# データベースからアイテム情報を取得
c.execute("SELECT * FROM items")
items = c.fetchall()

# アイテム情報を表示
for item in items:
    st.subheader(item[0])  # アイテム名
    st.write(item[1])      # 説明
    st.write(f"価格: ¥{item[2]}")  # 価格
    st.write("---")

st.markdown('</div>', unsafe_allow_html=True)




bottom_nav()


# 接続を閉じる
conn.close()
