import streamlit as st
import sqlite3
import io # For displaying images

from utils import *
if 'current_user' not in st.session_state:
    st.warning("このページを表示するにはログインが必要です。デモ用のユーザーIDを使用します。")
else:
    st.text("current user:{id} ".format(id=st.session_state.current_user))
if "logged_in" not in st.session_state:
    st.warning("not logged in")
else:
    st.text("logged in")
# --- Database Initialization ---
# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()
side_nav()
# テーブルがなければ作成 (念のため、全ページでテーブル構造を定義しておくのが安全)
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

# --- Streamlit UI Setup ---

# トップバーの表示
# topbar()

st.markdown("<h2 style='margin-top: 20px; text-align: center;'>出品一覧</h2>", unsafe_allow_html=True)

# データベースからアイテム情報とタグ情報を取得
c.execute("""
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
    GROUP BY
        items.itemid
    ORDER BY
        items.itemid DESC
""")
items = c.fetchall()

# アイテム情報を表示
if items:
    for item in items:
        item_id, item_name, description, price, picture_blob, number, availability, tags = item

        st.subheader(item_name)

        if picture_blob:
            # st.image requires a file-like object or path, or bytes for supported formats
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

# 接続を閉じる
conn.close()
