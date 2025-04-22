import streamlit as st

def topbar():
    # トップバー
    st.markdown("""
        <style>
        .custom-topbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #ff6f61;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            z-index: 10000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        .custom-topbar .title {
            font-size: 20px;
            font-weight: bold;
        }

        .custom-topbar .search-button {
            background-color: white;
            color: #ff6f61;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            cursor: pointer;
        }

        .main-content {
            margin-top: 70px;
        }
        </style>

        <div class="custom-topbar">
            <div class="title">弓削商船高専 学内フリマ</div>
            <button class="search-button">🔍 検索</button>
        </div>
    """, unsafe_allow_html=True)


def bottom_nav():
    # ボトナビ
    st.markdown("""
        <style>
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50px;
            background-color: #f1f1f1;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #ccc;
            z-index: 9999;
        }
        .bottom-nav a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
            font-size: 16px;
        }
        </style>

        <div class="bottom-nav">
            <a href="/home" target="_self"">🏠 ホーム</a>
            <a href="/listing" target="_self">📦 出品</a>
            <a href="/mypage" target="_self">👤 マイページ</a>
        </div>
    """, unsafe_allow_html=True)
