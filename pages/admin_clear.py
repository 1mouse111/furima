import streamlit as st
import sqlite3
import time # Although not strictly used for delay here, often useful with reruns

st.set_page_config(layout="centered", page_title="DB 完全クリアユーティリティ")

st.title("データベース完全クリアユーティリティ")
st.warning("⚠️ **最終確認:** これらの操作は、選択されたテーブルを完全に削除し、再作成します。これにより、すべてのデータが失われ、IDシーケンスがリセットされます。")

# --- Session State Initialization for messages ---
if 'users_cleared' not in st.session_state:
    st.session_state.users_cleared = False
if 'items_cleared' not in st.session_state:
    st.session_state.items_cleared = False
if 'tags_cleared' not in st.session_state:
    st.session_state.tags_cleared = False

# --- Display persistent success messages ---
if st.session_state.users_cleared:
    st.success("ユーザーテーブルが完全にクリアされ、IDシーケンスがリセットされました。")
    st.session_state.users_cleared = False # Reset the flag
if st.session_state.items_cleared:
    st.success("アイテムテーブルが完全にクリアされ、IDシーケンスがリセットされました。")
    st.session_state.items_cleared = False # Reset the flag
if st.session_state.tags_cleared:
    st.success("タグテーブルが完全にクリアされ、IDシーケンスがリセットされました。")
    st.session_state.tags_cleared = False # Reset the flag

# --- users.db のクリア ---
conn_users = None
try:
    conn_users = sqlite3.connect('userinfo.db')
    c_users = conn_users.cursor()

    st.subheader("ユーザーテーブル (userinfo.db)")
    
    if st.button("ユーザーテーブルを完全にクリア", key="clear_users_hard_btn"):
        c_users.execute("DROP TABLE IF EXISTS users")
        c_users.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            pass TEXT,
                            mail TEXT)
                        ''')
        conn_users.commit()
        st.session_state.users_cleared = True

        st.rerun()

except sqlite3.Error as e:
    st.error(f"ユーザーデータベースの操作中にエラーが発生しました: {e}")
finally:
    if conn_users:
        conn_users.close()

st.markdown("---") # 区切り線

# --- items.db のクリア ---
conn_items = None
try:
    conn_items = sqlite3.connect('items.db')
    c_items = conn_items.cursor()

    st.subheader("アイテム、タグテーブル (items.db)")

    if st.button("アイテムテーブルを完全にクリア", key="clear_items_hard_btn"):
        # Dropping item_tags first to ensure no foreign key issues with items table
        c_items.execute("DROP TABLE IF EXISTS item_tags")
        c_items.execute("DROP TABLE IF EXISTS items")
        
        c_items.execute('''CREATE TABLE items (
                            itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                            userid INTEGER,
                            name TEXT,
                            picture BLOB,
                            description TEXT,
                            price INTEGER,
                            number INTEGER,
                            availability INTEGER
                        )''')
        c_items.execute('''CREATE TABLE item_tags (
                            itemid INTEGER,
                            tagid INTEGER,
                            PRIMARY KEY (itemid, tagid),
                            FOREIGN KEY (itemid) REFERENCES items(itemid) ON DELETE CASCADE,
                            FOREIGN KEY (tagid) REFERENCES tags(tagid) ON DELETE CASCADE
                        )''')
        conn_items.commit()
        st.session_state.items_cleared = True

        st.rerun()

    if st.button("タグテーブルを完全にクリア", key="clear_tags_hard_btn"):
        c_items.execute("DROP TABLE IF EXISTS tags")
        c_items.execute('''CREATE TABLE tags (
                            tagid INTEGER PRIMARY KEY AUTOINCREMENT,
                            tag_name TEXT UNIQUE NOT NULL
                        )''')
        conn_items.commit()
        st.session_state.tags_cleared = True

        st.rerun()

except sqlite3.Error as e:
    st.error(f"アイテムデータベースの操作中にエラーが発生しました: {e}")
finally:
    if conn_items:
        conn_items.close()