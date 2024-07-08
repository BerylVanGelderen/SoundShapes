import streamlit as st

st.set_page_config(page_title="SoundShapes", page_icon=":musical_note:" )

st.title("Welcome to SoundShapes!")
st.write("#### This demo is made for large screens. Chrome is the only supported browser.")
st.write("The survey is now closed. \nThank you for your interest in the SoundShapes!  \nBeryl")
col1, col2 = st.columns([1,1], gap= 'medium')
if col2.button("Participate in the study", use_container_width=True, ):
    st.switch_page("pages/user_study_pt1.py")
if col1.button(":rainbow-background[Explore the SoundShapes]", use_container_width=True, disabled=False):
    st.switch_page("pages/thumbnail_exploration.py")

