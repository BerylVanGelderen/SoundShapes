import streamlit as st
def init(audio_features_in, thumbnails_loc_in, mp3_folder_in, album_covers_in):
    global audio_features
    global thumbnails_loc
    global mp3_folder
    global album_covers
    audio_features = audio_features_in
    thumbnails_loc = thumbnails_loc_in
    mp3_folder = mp3_folder_in
    album_covers = album_covers_in


def play_audio_in_sidebar(df_row):
    st.sidebar.image(df_row['thumbnail'], use_column_width=True, width= 200)
    st.sidebar.write(f"**{df_row['spotify track_name']}**  \n{df_row['spotify artist_name']}")
    st.sidebar.audio(f"{mp3_folder}/{df_row.name}.mp3", format="audio/mp3", autoplay=True, start_time=0)


def display_song_in_row(df_row):
    col_button, col_thumbnail, col_title, col_artist = st.columns([1.5, 2.5, 8,8], gap='small')
    col_thumbnail.image(df_row['thumbnail'], use_column_width=True)
    col_title.write(f"**{df_row['spotify track_name']}**")
    col_artist.write(f"{df_row['spotify artist_name']}")
    if col_button.button("▶️", df_row.name):
        play_audio_in_sidebar(df_row)

def write_context_explanation():
    st.subheader("Where and when would you listen to this music?")
    st.write("Listen to the song below.  \nCan you imagine a situation where you would listen to this music?  "
         "\nIf that is the case, where are you? Who is with you? What are you doing? Are you using headphones? What is your mood?  \n")



def write_pick_a_song_explanation():
    st.subheader("Pick a song that would also work in this situation.")
    st.write(
        "Imagine you are selecting songs for a playlist for the situation you just described. Which of the songs below would you include in that playlist too?")


def songs_to_display(audio_features, seed, n):
    df_songs_to_display= audio_features.sample(n, random_state = seed)[['spotify artist_name', 'spotify track_name']]
    if album_covers:
        df_songs_to_display['thumbnail'] = df_songs_to_display.index.map(lambda x: f'{thumbnails_loc}/{x}.jpg')
    else:
       df_songs_to_display['thumbnail'] = df_songs_to_display.index.map(lambda x: f'{thumbnails_loc}/{x}.svg')
    return df_songs_to_display