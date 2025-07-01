import streamlit as st
import sqlite3
import io # For displaying images

# Assuming utils.py contains topbar() and bottom_nav()
from utils import *

# --- IMPORTANT: Hide default Streamlit header FIRST ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {display: none;}
    .stApp { padding-top: 70px; } /* Ensure content is not hidden by fixed topbar */
    </style>
""", unsafe_allow_html=True)

# --- Topbar Display ---


# --- Database Initialization (for table creation if needed) ---
# This part is generally placed at the top of each page for robustness,
# but if tables are guaranteed to exist, it can be minimized.
conn = sqlite3.connect('items.db')
c = conn.cursor()

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
c.execute('''CREATE TABLE IF NOT EXISTS tags (
                tagid INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE NOT NULL
            )''')
c.execute('''CREATE TABLE IF NOT EXISTS item_tags (
                itemid INTEGER,
                tagid INTEGER,
                PRIMARY KEY (itemid, tagid),
                FOREIGN KEY (itemid) REFERENCES items(itemid) ON DELETE CASCADE,
                FOREIGN KEY (tagid) REFERENCES tags(tagid) ON DELETE CASCADE
            )''')
conn.commit()
conn.close() # Close connection after table creation checks


# --- Get Current User ID ---
# Check if a user is logged in (assuming st.session_state.current_user holds the user ID)
if 'current_user' not in st.session_state:
    st.warning("このページを表示するにはログインが必要です。デモ用のユーザーIDを使用します。")

current_user_id = st.session_state.current_user


def get_user_items_with_tags(user_id):
    """
    Fetches items listed by a specific user with their associated tags from the database.
    This function has its own connection management and is cached.
    """
    conn_fetch = sqlite3.connect('items.db') # Open connection inside cached function
    c_fetch = conn_fetch.cursor()
    
    c_fetch.execute("""
        SELECT
            items.itemid,
            items.name,
            items.description,
            items.price,
            items.picture,
            items.number,
            items.availability,
            GROUP_CONCAT(tags.tag_name, ', ') AS tags
        FROM
            items
        LEFT JOIN
            item_tags ON items.itemid = item_tags.itemid
        LEFT JOIN
            tags ON item_tags.tagid = tags.tagid
        WHERE
            items.userid = ? -- Filter by current user ID
        GROUP BY
            items.itemid
        ORDER BY
            items.itemid DESC
    """, (user_id,)) # Pass user_id as a tuple for the WHERE clause
    
    items_data = c_fetch.fetchall()
    conn_fetch.close() # Close connection after fetching
    return items_data

# --- Main Content Display ---
st.markdown(f"<h2 style='margin-top: 20px; text-align: center;'>あなたの出品アイテム (ユーザーID: {current_user_id})</h2>", unsafe_allow_html=True)


# Fetch items using the cached function, passing the current_user_id
items = get_user_items_with_tags(current_user_id)

# アイテム情報を表示
if items:
    for item in items:
        item_id, item_name, description, price, picture_blob, number, availability, tags = item

        st.subheader(item_name)

        if picture_blob:
            st.image(io.BytesIO(picture_blob), caption=item_name, width=200)

        st.write(description)
        st.write(f"**価格:** ¥{price}")
        st.write(f"**在庫数:** {number}")
        st.write(f"**ステータス:** {'販売中' if availability == 1 else '売り切れ'}")

        if tags:
            st.write(f"**タグ:** {tags}")
        else:
            st.write("**タグ:** なし")
        st.write("---")

else:
    st.info("まだ出品されたアイテムはありません。")

# --- Footer Navigation ---
side_nav()