import streamlit as st
import sqlite3

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()

# Create a separate table for tags
c.execute('''CREATE TABLE IF NOT EXISTS tags (
            tagid INTEGER,
            tag_name TEXT UNIQUE NOT NULL
        )''')
conn.commit()

# 入力フォームの作成
tag_id = st.text_input("tag ID")
tag_name = st.text_input("tag name")

# 投稿ボタンが押されたときの動作
if st.button("createtag"):
    # アイテム情報をデータベースに保存
    c.execute("INSERT INTO tags (tagid, tag_name) VALUES (?, ?)",
              (tag_id, tag_name))
    conn.commit()
    st.success("tag added！") # Success message

st.header("tags")
c.execute("SELECT tagid, tag_name FROM tags") # SELECT idも追加
tags = c.fetchall()

if not tags:
    st.info("no tags")
else:
    for tag in tags:
        st.write(f"tag ID: {tag[0]}")
        st.write(f"tag name: {tag[1]}")
        st.write("---")