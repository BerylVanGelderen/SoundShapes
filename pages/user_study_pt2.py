import pandas as pd
import streamlit as st
import random
import streamlit_display_functions as sdf

st.set_page_config(page_title="SoundShapes", page_icon=":musical_note:" )

if 'seed2' not in st.session_state:
    st.session_state.seed2 = random.randint(1, 1000)

if 'no_of_songs2' not in st.session_state:
    st.session_state.no_of_songs2 = 31

audio_features_loc = 'user_evaluation_app/static/dimensionality_reduced.csv'
audio_features = pd.read_csv(audio_features_loc, index_col='track_id')
thumbnails_loc = 'user_evaluation_app/static/thumbnails/20240623_thumbnails_tsne_4698_600px'
mp3_folder = 'user_evaluation_app/static/mp3_previews'

global album_covers
album_covers = False

sdf.init(audio_features, thumbnails_loc, mp3_folder, album_covers)

songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed2, st.session_state.no_of_songs2)
target_song_index = songs_to_display.index[0]
target_song_df = songs_to_display.loc[[target_song_index]]
search_songs_df = songs_to_display.drop(target_song_index)

st.sidebar.title("Audio Player")

st.title("SoundShapes- study part 2")

st.write("For part 2, we are going to do exactly the same thing as in part 1. Using the button below, you can go back "
         "to see the explanation again, but don't worry: sometimes it's best to just dive in!")
if st.button("See explanation", use_container_width=False):
    st.switch_page("pages/explanation.py")


st.write("---")
sdf.write_context_explanation()
st.write("If you cannot think of a situation in which you would listen to this music, change the number below for new music.")
seed = st.number_input("Seed", min_value=1, max_value=1000, value=st.session_state.seed2)
if seed != st.session_state.seed2:
    st.session_state.seed2 = seed
    st.session_state.no_of_songs2 = 31
    songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed2, st.session_state.no_of_songs2)
    target_song_index = songs_to_display.index[0]
    target_song_df = songs_to_display.loc[[target_song_index]]
    search_songs_df = songs_to_display.drop(target_song_index)
st.write("---")

target_song_df.apply(sdf.display_song_in_row, axis=1)
st.write("---")

sdf.write_pick_a_song_explanation()
st.write("  \n")

search_songs_df.apply(sdf.display_song_in_row, axis=1)

st.write("  \n")
if st.button("Show more songs"):
    st.session_state.no_of_songs2 += 10
    songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed2, st.session_state.no_of_songs2)
    target_song_index = songs_to_display.index[0]
    target_song_df = songs_to_display.loc[[target_song_index]]
    search_songs_df = songs_to_display.drop(target_song_index)
    search_songs_df.tail(10).apply(sdf.display_song_in_row, axis=1)

st.write("---")
col1, col2 = st.columns([4,16], gap = 'large')
if col1.button("Go back", use_container_width=True):
    st.switch_page("pages/user_study_pt1.py")
col2.page_link("https://survey.uu.nl/jfe/form/SV_cAYMM8oafTGvruK", label=":rainbow-background[🎈 Done!  🎈  \n 🎵 **Go to the questionnaire** 🎵]", use_container_width=True)
