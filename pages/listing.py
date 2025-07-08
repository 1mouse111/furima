import streamlit as st
import sqlite3

from utils import *

side_nav()

# ハンバーガーメニューの削除

# トップバーの表示

# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()

# テーブルがなければ作成
c.execute('''CREATE TABLE IF NOT EXISTS items (
                itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER,
                name TEXT,
                picture BLOB,
                description TEXT,
                price INTEGER,
                number INTEGER,
                availability INTEGER
            )''')
# Create a separate table for tags
c.execute('''CREATE TABLE IF NOT EXISTS tags (
            tagid INTEGER,
            tag_name TEXT UNIQUE NOT NULL
        )''')

# Create a junction table to link items and tags
c.execute('''CREATE TABLE IF NOT EXISTS item_tags (
            itemid INTEGER,
            tagid INTEGER,
            PRIMARY KEY (itemid, tagid),
            FOREIGN KEY (itemid) REFERENCES items(itemid) ON DELETE CASCADE,
            FOREIGN KEY (tagid) REFERENCES tags(tagid) ON DELETE CASCADE
        )''')
conn.commit()

def get_all_tags():
    c.execute("SELECT tag_name FROM tags ORDER BY tag_name")
    return [row[0] for row in c.fetchall()]

all_tags=get_all_tags()

# 入力フォームの作成
st.header("新しいアイテムを出品する")

item_name = st.text_input("アイテム名")
selected_tags=st.multiselect(
    "タグを選択 (複数選択可)",
    options=all_tags
)
item_picture = st.file_uploader("アイテムの画像(任意)", type=["png", "jpg", "jpeg"])
item_description = st.text_area("アイテムの説明")
item_price = st.number_input("価格", min_value=0, step=100)
item_number = st.number_input("在庫数", min_value=1, step=1)
#demo
if 'current_user' not in st.session_state:
    st.warning("アイテムを出品するにはログインが必要です。")

# 投稿ボタンが押されたときの動作
if st.button("アイテムを投稿"):
    if not item_name or not item_description or item_price is None or item_number is None:
        st.error("すべての必須項目を入力してください。")
    else:
        # Convert image to bytes if uploaded, otherwise set to None
        image_bytes = item_picture.read() if item_picture else None
        
        # Set availability to "available" (e.g., 1 for available, 0 for unavailable)
        availability_status = 1 
        
        # Get the current user ID from session state
        user_id = st.session_state.current_user
        
        try:
            # 1. Save item information to the 'items' table
            # If image_bytes is None, SQLite will store NULL in the BLOB column
            c.execute("INSERT INTO items (userid, name, picture, description, price, number, availability) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (user_id, item_name, image_bytes, item_description, item_price, item_number, availability_status))
            
            # 2. Get the itemid of the newly inserted item
            last_item_id = c.lastrowid

            # 3. Save selected tags to the 'item_tags' table
            if selected_tags and last_item_id:
                # Get tagids for the selected tag names
                placeholders = ','.join('?' * len(selected_tags))
                c.execute(f"SELECT tagid FROM tags WHERE tag_name IN ({placeholders})", selected_tags)
                tag_ids_to_insert = c.fetchall()

                # Create a list of (itemid, tagid) pairs
                item_tag_pairs = [(last_item_id, tag_id[0]) for tag_id in tag_ids_to_insert]
                
                # Insert the pairs into the 'item_tags' table
                c.executemany("INSERT INTO item_tags (itemid, tagid) VALUES (?, ?)", item_tag_pairs)

            # 4. Commit changes to the database
            conn.commit()

            st.success("アイテムが正常に投稿されました！")
            # st.rerun() # Refresh the page to clear the form

        except sqlite3.Error as e:
            st.error(f"データベースエラーが発生しました: {e}")

conn.close()

