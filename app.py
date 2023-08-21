import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="FIFA",
    page_icon="👋",
    layout="wide"
)

st.markdown(
        "<h1 style='text-align: center; color: blue;'>Fifa Streamlit App</h1>",
        unsafe_allow_html=True,
    )

def main():
    with open("database.csv", "r") as file:
        st.session_state.df = pd.read_csv(file)

    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
    )

    if not edited_df.equals(st.session_state.df):
        edited_df.to_csv("database.csv", index=False)

    with open("database.csv", "rb") as file:
        _ = st.download_button(
            label="Download csv",
            data=file,
            file_name="database.csv",
            mime="application/csv"
        )

if __name__ == "__main__":
    main()
