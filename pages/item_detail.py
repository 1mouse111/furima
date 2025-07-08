import streamlit as st
import sqlite3
import io

from utils import * 

side_nav()
# --- Check Login and Session State ---
if 'logged_in' not in st.session_state:
    st.switch_page("app.py") # Redirect to login if not logged in
else:
    st.text("current user:{id} ".format(id=st.session_state.current_user))

# Check if an item ID was passed from the previous page
if 'selected_item_id' not in st.session_state:
    st.error("表示するアイテムが選択されていません。")
    if st.button("アイテム一覧に戻る"):
        st.switch_page("pages/home.py") # Go back to the home page
    st.stop() # Stop execution if no item is selected

item_id = st.session_state.selected_item_id

# --- Database Connection and Data Fetching ---
conn = sqlite3.connect('items.db')
c = conn.cursor()

# Fetch all details for the selected item, including tags
c.execute("""
    SELECT
        items.itemid,
        items.name,
        items.description,
        items.price,
        items.picture,
        items.number,
        items.availability,
        items.userid, -- Include userid if you want to display seller info
        GROUP_CONCAT(tags.tag_name, ', ') AS tags
    FROM
        items
    LEFT JOIN
        item_tags ON items.itemid = item_tags.itemid
    LEFT JOIN
        tags ON item_tags.tagid = tags.tagid
    WHERE
        items.itemid = ?
    GROUP BY
        items.itemid
""", (item_id,))
item_details = c.fetchone()

conn.close()

# --- Display Item Details ---
if item_details:
    item_id, item_name, description, price, picture_blob, number, availability, userid, tags = item_details

    st.title(item_name)
    
    # Display image prominently
    if picture_blob:
        # st.image requires a file-like object or path, or bytes for supported formats
        st.image(io.BytesIO(picture_blob), caption=item_name, width=200)
    else:
        st.write("このアイテムには画像がありません。")

    st.markdown("---") # Separator

    st.subheader("商品説明")
    st.write(description)

    st.subheader("価格")
    st.write(f"**¥{price:,}**") # Bold and format price

    st.subheader("在庫数")
    st.write(f"{number} 個")

    st.subheader("ステータス")
    st.write(f"{'販売中' if availability == 1 else '売り切れ'}")

    st.subheader("タグ")
    if tags:
        st.write(f"{tags}")
    else:
        st.write("なし")

    st.subheader("出品者情報")
    st.write(f"出品者ID: {userid}") # You might want to fetch and display actual user name here

    st.markdown("---") # Separator

    # Button to go back to the item list
    if st.button("アイテム一覧に戻る"):
        st.switch_page("pages/home.py") # Adjust this if your main page is named differently
else:
    st.error("お探しのアイテムは見つかりませんでした。")