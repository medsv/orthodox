import streamlit as st

def show_footer():
    st.markdown(
        """
        <hr>
        <p style="text-align: left; color: gray;">
        <small>
        2026, С.В. Медведев, engpython@yandex.ru
        </small>
        </p>
        """,
        unsafe_allow_html=True
    )