import pandas as pd
import streamlit as st
import random
import streamlit_display_functions as sdf

st.set_page_config(page_title="SoundShapes", page_icon=":musical_note:" )

if 'seed1' not in st.session_state:
    st.session_state.seed1 = random.randint(1, 1000)

if 'no_of_songs1' not in st.session_state:
    st.session_state.no_of_songs1 = 31


audio_features_loc = 'user_evaluation_app/static/dimensionality_reduced.csv'
audio_features = pd.read_csv(audio_features_loc, index_col='track_id')
thumbnails_loc = 'user_evaluation_app/static/album_covers'
mp3_folder = 'user_evaluation_app/static/mp3_previews'


global album_covers
album_covers = True

sdf.init(audio_features, thumbnails_loc, mp3_folder, album_covers)

songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed1, st.session_state.no_of_songs1)
target_song_index = songs_to_display.index[0]
target_song_df = songs_to_display.loc[[target_song_index]]
search_songs_df = songs_to_display.drop(target_song_index)

st.sidebar.title("Audio Player")

st.title("SoundShapes- test part 1")

sdf.write_context_explanation()

st.write("If you cannot think of a situation in which you would listen to this music, change the number below for new music.")
seed = st.number_input("Seed", min_value=1, max_value=1000, value=st.session_state.seed1)
if seed != st.session_state.seed1:
    st.session_state.seed1 = seed
    songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed1, 31)
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
    st.session_state.no_of_songs1 += 10
    songs_to_display = sdf.songs_to_display(audio_features, st.session_state.seed1, st.session_state.no_of_songs1)
    target_song_index = songs_to_display.index[0]
    target_song_df = songs_to_display.loc[[target_song_index]]
    search_songs_df = songs_to_display.drop(target_song_index)
    search_songs_df.tail(10).apply(sdf.display_song_in_row, axis=1)
st.write("---")

col1, col2 = st.columns([4,16])
if col2.button(":rainbow-background[**Done! go to part 2!**]", use_container_width=True):
    st.switch_page("pages/explanation.py")

if col1.button("Go back", use_container_width=True):
    st.switch_page("main.py")