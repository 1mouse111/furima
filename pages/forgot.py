# import streamlit as st

# # 初期化
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# mail_db=[]
# # ログインフォームの表示
# st.title("メイルアドレス検索")
# mail = st.text_input("メイルアドレス")
# if st.button("検索"):
#     if mail in mail_db:
#         st.session_state.logged_in = True
#         st.success("ログイン成功！")
#         st.rerun()
#     else:
#         st.error("ユーザーIDまたはパスワードが間違っています。")
# st.page_link("pages/forgot.py", label="パスワードを忘れましたか?")

# # ログイン成功したら自動で home.py に遷移
# if st.session_state.logged_in:
#     st.switch_page("pages/home.py")

import streamlit as st

def password_reset_page():
    st.title("Password Reset")
    st.write("To reset your password, submit your username or your email address below. If we can find you in the database, an email will be sent to your email address, with instructions how to get access again.")

    # Use st.session_state to manage the state of whether the form has been submitted
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    if not st.session_state.form_submitted:
                # --- Search by Email Address ---
        st.subheader("Search by email address")
        with st.form(key="email_form"):
            email_address = st.text_input("Email address")
            submit_email = st.form_submit_button("Search")

            if submit_email:
                # In a real application, you would add logic here to check the email
                # and send an email. For this example, we just set the flag.
                if email_address and "@" in email_address: # Simple email format check
                    st.session_state.form_submitted = True
                    st.rerun()
                else:
                    st.warning("Please enter a valid email address.")

    else:
        # This block is shown after the form is submitted
        st.write("If you supplied a correct email address then an email should have been sent to you.")
        st.write("It contains easy instructions to confirm and complete this password change. If you continue to have difficulty, please contact the site administrator.")

        # You can add a "Continue" button if needed, which might reset the state or navigate elsewhere
        if st.button("Continue"):
            st.session_state.form_submitted = False # Allows resubmission or hides the message
            st.switch_page("app.py")


if __name__ == "__main__":
    password_reset_page()