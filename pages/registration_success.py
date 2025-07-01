import streamlit as st
from utils import *


if 'registered_email_for_confirmation' not in st.session_state:
    st.switch_page("app.py")

no_top()
side_button()
st.title("登録完了")

st.success("ユーザー登録が完了しました！")
registered_email = st.session_state.registered_email_for_confirmation

st.write(f"ご登録いただいたメールアドレス **{registered_email}** に確認コードを送信しました。")
st.write("メールをご確認の上、指示に従ってアカウントを有効化してください。")

st.markdown("---")

# ログインページに戻るボタン
if st.button("ログインページへ"):
    # メールアドレスをセッションステートからクリア（一度表示したら不要なため）
    if 'registered_email_for_confirmation' in st.session_state:
        del st.session_state.registered_email_for_confirmation
    st.switch_page("app.py") # メインのログインページ (app.py) へ遷移