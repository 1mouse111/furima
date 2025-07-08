import streamlit as st
import sqlite3
import io # For displaying images
from utils import *
if 'logged_in' not in st.session_state:
    st.switch_page("app.py")
else:
    st.text("current user:{id} ".format(id=st.session_state.current_user))
side_nav()

# --- Database Initialization ---
# SQLite データベースに接続（なければ新しく作成）
conn = sqlite3.connect('items.db')
c = conn.cursor()
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

st.markdown("<h2 style='margin-top: 20px; text-align: center;'>出品一覧</h2>", unsafe_allow_html=True)

# データベースからアイテム情報とタグ情報を取得
c.execute("""
    SELECT
        items.itemid,
        items.name,
        items.picture,
        items.price,
        items.number,
        items.availability
    FROM
        items
    WHERE
        items.availability = 1
    ORDER BY
        items.itemid DESC
""")
items_summary = c.fetchall()
conn.close()

# アイテム情報を表示
if items_summary:
    for i,item in enumerate(items_summary):
        item_id, item_name, picture_blob, price, number, availability = item

        with st.container(border=True):
            st.subheader(item_name)
            col1, col2 =st.columns(2)
            with col1:
                if picture_blob:
                    # st.image requires a file-like object or path, or bytes for supported formats
                    st.image(io.BytesIO(picture_blob), caption=item_name, width=200)
                else:
                    st.write("画像なし")
            with col2:
                st.write(f"**価格:** ¥{price:,}")
                st.write(f"**在庫数:** {number}")

            if st.button(f"詳細を見る", key=f"details_{item_id}"):
                st.session_state.selected_item_id = item_id 
                st.switch_page("pages/item_detail.py") 
else:
    st.info("まだ出品されたアイテムはありません。")

# 接続を閉じる
