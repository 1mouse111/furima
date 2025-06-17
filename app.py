import streamlit as st

# 初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ログインフォームの表示
st.title("ログインページ")
user_id = st.text_input("ユーザーID")
password = st.text_input("パスワード", type="password")

if st.button("ログイン"):
    if user_id == "User" and password == "Pass":
        st.session_state.logged_in = True
        st.success("ログイン成功！")
        st.rerun()
    else:
        st.error("ユーザーIDまたはパスワードが間違っています。")
        
st.page_link("pages/forgot.py", label="パスワードを忘れましたか?")


# ログイン成功したら自動で home.py に遷移
if st.session_state.logged_in:
    st.switch_page("pages/home.py")